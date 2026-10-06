"""Behavior tests against controlled HTTP responses, not copy or ranking promises."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/foundvia-discovery/scripts/discovery_audit.py"
spec = importlib.util.spec_from_file_location("discovery", SCRIPT)
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)


class RobotsTests(unittest.TestCase):
    def decide(self, text, bot="Googlebot", path="/public"):
        return discovery.robots_decision(text, bot, "https://example.com" + path)[0]

    def test_specific_group_does_not_inherit_wildcard(self):
        rules = "User-agent: *\nDisallow: /\nUser-agent: OAI-SearchBot\nAllow: /"
        self.assertFalse(self.decide(rules))
        self.assertTrue(self.decide(rules, "OAI-SearchBot"))

    def test_equal_groups_merge_and_allow_wins_tie(self):
        rules = "User-agent: Googlebot\nDisallow: /a\nUser-agent: googlebot\nAllow: /a"
        self.assertTrue(self.decide(rules, path="/a"))

    def test_longest_rule_wildcard_and_end_anchor(self):
        rules = "User-agent: *\nDisallow: /*.pdf$\nAllow: /public/"
        self.assertFalse(self.decide(rules, path="/report.pdf"))
        self.assertTrue(self.decide(rules, path="/report.pdf?download=1"))
        self.assertTrue(self.decide(rules, path="/public/report.pdf"))

    def test_empty_rules_bom_comments_and_case_sensitive_paths(self):
        rules = "\ufeffUser-Agent: *\nDisallow:\nDisallow: /Private # note"
        self.assertTrue(self.decide(rules, path="/private"))
        self.assertFalse(self.decide(rules, path="/Private"))

    def test_percent_encoding_unreserved_and_reserved(self):
        self.assertFalse(self.decide("User-agent: *\nDisallow: /a", path="/%61"))
        self.assertTrue(self.decide("User-agent: *\nDisallow: /a/b", path="/a%2Fb"))

    def test_training_policy_independent(self):
        rules = "User-agent: *\nAllow: /\nUser-agent: GPTBot\nDisallow: /"
        self.assertTrue(self.decide(rules, "OAI-SearchBot"))
        self.assertFalse(self.decide(rules, "GPTBot"))

    def test_empty_rule_still_starts_new_group(self):
        rules = "User-agent: Googlebot\nDisallow:\nUser-agent: GPTBot\nDisallow: /"
        self.assertTrue(self.decide(rules))

    def test_version_and_wildcard_agent_decorations_match_product_token(self):
        for agent in ("Googlebot/1.2", "Googlebot*"):
            self.assertFalse(self.decide("User-agent: " + agent + "\nDisallow: /"))

    def test_empty_agent_is_not_a_wildcard(self):
        self.assertTrue(self.decide("User-agent:\nDisallow: /"))


class MetadataTests(unittest.TestCase):
    def test_unencoded_whitespace_and_control_characters_rejected(self):
        for value in ("https://bad host/", "https://example.com/a b", "https://example.com/\n"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                discovery.clean_url(value)
    def test_unknown_directive_does_not_match_noindex_substring(self):
        page = discovery.Page()
        page.feed('<meta name="robots" content="not-noindex">')
        self.assertFalse(discovery.noindex_evidence(page, [], "Googlebot"))

    def test_bot_targeted_noindex_is_not_generic(self):
        page = discovery.Page()
        page.feed('<META NAME="googlebot" content="noindex"><meta name="description" content="Useful">')
        self.assertTrue(discovery.noindex_evidence(page, [], "Googlebot"))
        self.assertFalse(discovery.noindex_evidence(page, [], "OAI-SearchBot"))
        self.assertFalse(discovery.noindex_evidence(discovery.Page(), ["gptbot: noindex"], "Googlebot"))

    def test_generic_header_and_meta_none(self):
        page = discovery.Page()
        self.assertTrue(discovery.noindex_evidence(page, ["noindex, nofollow"], "Googlebot"))
        page.feed('<meta name="robots" content="none">')
        self.assertTrue(discovery.noindex_evidence(page, [], "OAI-SearchBot"))

    def test_multiple_scopes_in_one_header(self):
        page = discovery.Page()
        headers = ["googlebot: index, oai-searchbot: noindex"]
        self.assertFalse(discovery.noindex_evidence(page, headers, "Googlebot"))
        self.assertTrue(discovery.noindex_evidence(page, headers, "OAI-SearchBot"))

    def test_credentials_and_invalid_scheme_rejected(self):
        for value in ("file:///etc/passwd", "https://user:password@example.com", "example.com", "https://example.com:bad"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                discovery.clean_url(value)


class ResourceFailureTests(unittest.TestCase):
    def test_protocol_errors_report_unknown_instead_of_crashing(self):
        import http.client
        with patch.object(discovery.urllib.request.OpenerDirector, "open", side_effect=http.client.BadStatusLine("invalid response")):
            result = discovery.fetch("https://example.com/", 1)
        self.assertIsNone(result["status"])
        self.assertIn("invalid response", result["error"])
    def report(self, robots_status=404, sitemap_body="invalid XML"):
        def fake_fetch(target, timeout, same_origin_only=False):
            if target.endswith("robots.txt"):
                return dict(url=target, status=robots_status, body="", error=None, truncated=False, content_type="text/plain")
            if target.endswith("sitemap.xml"):
                return dict(url=target, status=200, body=sitemap_body, error=None, truncated=False, content_type="application/xml")
            return dict(url=target, status=200, body="<title>Product</title>", error=None, truncated=False, content_type="text/html")
        with patch.object(discovery, "fetch", side_effect=fake_fetch):
            return {f["check"]: f for f in discovery.audit("https://example.com")["findings"]}

    def test_missing_robots_is_not_assumed_openai_pass(self):
        report = self.report()
        self.assertEqual(report["robots:Googlebot"]["status"], "info")
        self.assertEqual(report["robots:OAI-SearchBot"]["status"], "unknown")

    def test_rate_limit_and_server_error_remain_unknown(self):
        for code in (429, 503):
            with self.subTest(code=code):
                self.assertEqual(self.report(code)["robots:Googlebot"]["status"], "unknown")

    def test_invalid_xml_not_indexing_failure(self):
        self.assertEqual(self.report()["sitemap"]["status"], "unknown")

    def test_sitemap_index_does_not_claim_url_missing(self):
        report = self.report(sitemap_body='<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>https://example.com/child.xml</loc></sitemap></sitemapindex>')
        self.assertEqual(report["sitemap"]["status"], "info")
        self.assertIn("Children not fetched", report["sitemap"]["evidence"])


class Fixture(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        origin = "http://" + self.headers["Host"]
        status, kind, headers = 200, "text/html", {}
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/public")
            self.end_headers()
            return
        if self.path == "/credential-redirect":
            self.send_response(302)
            self.send_header("Location", "http://user:password@" + self.headers["Host"] + "/public")
            self.end_headers()
            return
        if self.path == "/robots.txt":
            kind = "text/plain"
            body = "User-agent: *\nAllow: /\nUser-agent: GPTBot\nDisallow: /\nSitemap: " + origin + "/custom.xml"
        elif self.path == "/custom.xml":
            kind = "application/xml"
            body = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>' + origin + '/public</loc></url></urlset>'
        elif self.path == "/large":
            body = "x" * (discovery.MAX_BYTES + 1)
        elif self.path == "/error":
            status, body = 503, "Unavailable"
        else:
            body = '<title>Public product</title><meta name="description" content="A useful tool"><h1>Product</h1><link rel="canonical" href="' + origin + '/public">'
            if self.path == "/excluded":
                headers["X-Robots-Tag"] = "noindex"
        self.send_response(status)
        self.send_header("Content-Type", kind + "; charset=utf-8")
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body.encode())


class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Fixture)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.origin = "http://127.0.0.1:" + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def findings(self, path):
        report = discovery.audit(self.origin + path, timeout=2)
        self.assertEqual(len(report["resources"]), 3)
        return {f["check"]: f for f in report["findings"]}

    def test_redirect_and_declared_sitemap(self):
        findings = self.findings("/redirect")
        self.assertEqual(findings["page-response"]["status"], "pass")
        self.assertEqual(findings["sitemap"]["status"], "pass")
        self.assertEqual(findings["robots:GPTBot"]["status"], "info")

    def test_noindex_block_and_fail_exit(self):
        findings = self.findings("/excluded")
        self.assertEqual(findings["noindex:Googlebot"]["status"], "block")
        result = subprocess.run([sys.executable, str(SCRIPT), self.origin + "/excluded", "--format", "json", "--fail-on-block"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertTrue(json.loads(result.stdout)["findings"])

    def test_failed_response_does_not_report_missing_metadata(self):
        findings = self.findings("/error")
        self.assertEqual(findings["page-response"]["status"], "block")
        self.assertNotIn("title", findings)

    def test_truncated_response_unknown_not_clean_pass(self):
        findings = self.findings("/large")
        self.assertEqual(findings["page-response"]["status"], "unknown")
        self.assertNotIn("canonical", findings)

    def test_credential_redirect_is_not_followed(self):
        report = discovery.audit(self.origin + "/credential-redirect", timeout=2)
        self.assertEqual(report["findings"][0]["status"], "unknown")
        self.assertIn("without credentials", report["resources"][0]["error"])

    def test_findings_have_actionable_json_and_markdown_fields(self):
        report = discovery.audit(self.origin + "/excluded", timeout=2)
        finding = next(f for f in report["findings"] if f["check"] == "noindex:Googlebot")
        self.assertEqual(finding["priority"], "P1")
        self.assertEqual(finding["confidence"], "observed")
        self.assertEqual(finding["location"], self.origin + "/excluded")
        self.assertTrue(finding["verification"])
        self.assertIn("Verify:", discovery.markdown(report))
        self.assertEqual(json.loads(json.dumps(report)), report)

    def test_openai_header_support_is_not_assumed(self):
        findings = self.findings("/excluded")
        self.assertEqual(findings["noindex:Googlebot"]["status"], "block")
        self.assertEqual(findings["noindex:OAI-SearchBot"]["status"], "info")


class ScopeTests(unittest.TestCase):
    def fake_report(self, robots_body):
        def fake_fetch(target, timeout, same_origin_only=False):
            body = robots_body if target.endswith("robots.txt") else '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"/>' if target.endswith("sitemap.xml") else '<title>Product</title>'
            return dict(url=target, status=200, body=body, error=None, truncated=False,
                        content_type="text/plain" if target.endswith("robots.txt") else "text/html")
        with patch.object(discovery, "fetch", side_effect=fake_fetch):
            return {f["check"]: f for f in discovery.audit("https://example.com")["findings"]}

    def test_malformed_sitemap_declaration_does_not_abort_audit(self):
        findings = self.fake_report("User-agent: *\nAllow: /\nSitemap: https://[broken\nSitemap: https://other.example/sitemap.xml")
        self.assertIn("Malformed", findings["sitemap-selection"]["evidence"])
        self.assertIn("sitemap", findings)

    def test_default_ports_are_same_origin(self):
        self.assertTrue(discovery.same_origin("https://example.com", "https://EXAMPLE.com:443/map.xml"))
        self.assertFalse(discovery.same_origin("https://example.com", "http://example.com/map.xml"))
        self.assertFalse(discovery.same_origin("https://example.com", "https://example.com:0/map.xml"))

    def test_google_rules_after_500_kib_are_not_applied(self):
        rules = "User-agent: *\nAllow: /\n" + "#" * discovery.GOOGLE_ROBOTS_BYTES + "\nDisallow: /"
        findings = self.fake_report(rules)
        self.assertEqual(findings["robots:Googlebot"]["status"], "pass")
        self.assertIn("500 KiB", findings["robots:Googlebot"]["evidence"])
        self.assertEqual(findings["robots:OAI-SearchBot"]["status"], "unknown")

    def test_cross_origin_sitemap_redirect_is_rejected_before_request(self):
        handler = discovery.ScopedRedirect("https://example.com/map.xml")
        request = discovery.urllib.request.Request("https://example.com/map.xml")
        with self.assertRaisesRegex(ValueError, "outside"):
            handler.redirect_request(request, None, 302, "Found", {}, "https://other.example/map.xml")
        self.assertIsNotNone(handler.redirect_request(request, None, 302, "Found", {}, "https://example.com/new.xml"))


if __name__ == "__main__":
    unittest.main()
