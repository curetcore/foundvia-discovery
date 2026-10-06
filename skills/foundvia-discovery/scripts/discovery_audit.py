#!/usr/bin/env python3
"""Bounded initial-response discovery audit. Python 3.10+, standard library only."""
import argparse
import datetime as dt
import http.client
from html.parser import HTMLParser
import json
import re
import sys
import urllib.error
import urllib.parse as url
import urllib.request
import xml.etree.ElementTree as ET

MAX_BYTES = 1024 * 1024
USER_AGENT = "FoundviaDiscovery/0.1 (+https://github.com/ronaldships/foundvia-discovery)"
BOTS = ("Googlebot", "OAI-SearchBot", "GPTBot")
GOOGLE_ROBOTS_BYTES = 500 * 1024


def clean_url(value):
    if any(character.isspace() or ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError("URL whitespace/control characters must be percent-encoded.")
    parts = url.urlsplit(value)
    if parts.scheme not in ("http", "https") or not parts.hostname or parts.username or parts.password:
        raise ValueError("Use an http(s) URL without credentials.")
    _ = parts.port  # Validate malformed ports before requesting.
    return url.urlunsplit(parts._replace(fragment="", path=parts.path or "/"))


def same_origin(left, right):
    def origin(value):
        p = url.urlsplit(clean_url(value))
        return p.scheme, p.hostname.lower(), p.port if p.port is not None else (443 if p.scheme == "https" else 80)
    return origin(left) == origin(right)


class ScopedRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, origin=None):
        self.origin = origin

    def redirect_request(self, request, fp, code, message, headers, newurl):
        clean_url(newurl)
        if self.origin and not same_origin(self.origin, newurl):
            raise ValueError("Redirect outside the permitted sitemap origin was not followed.")
        return super().redirect_request(request, fp, code, message, headers, newurl)


def fetch(target, timeout, same_origin_only=False):
    try:
        request = urllib.request.Request(target, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"})
        try:
            opener = urllib.request.build_opener(ScopedRedirect(target if same_origin_only else None))
            response = opener.open(request, timeout=timeout)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            raw = response.read(MAX_BYTES + 1)
            headers = response.headers
            return {
                "url": response.geturl(), "status": response.code,
                "content_type": headers.get_content_type(),
                "x_robots_tag": headers.get_all("X-Robots-Tag", []),
                "body": raw[:MAX_BYTES].decode(headers.get_content_charset() or "utf-8", errors="replace"),
                "truncated": len(raw) > MAX_BYTES, "error": None,
            }
    except (urllib.error.URLError, http.client.HTTPException, TimeoutError, OSError, ValueError, LookupError) as exc:
        return {"url": target, "status": None, "body": "", "truncated": False, "error": str(exc)}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = []
        self.in_title = False
        self.h1 = 0
        self.description = []
        self.canonicals = []
        self.robots = []
        self.jsonld = 0
        self.base = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "base" and self.base is None:
            self.base = a.get("href")
        elif tag == "meta":
            name = (a.get("name") or "").lower()
            if name == "description":
                self.description.append(a.get("content") or "")
            if name in ("robots", "googlebot", "oai-searchbot", "gptbot"):
                self.robots.append((name, a.get("content") or ""))
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower().split():
            self.canonicals.append(a.get("href") or "")
        elif tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self.jsonld += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


def robots_groups(text):
    groups, agents, rules, sitemaps = [], [], [], []
    for line in text.lstrip("\ufeff").splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        field, value = (v.strip() for v in line.split(":", 1))
        field = field.lower()
        if field == "sitemap":
            sitemaps.append(value)
        elif field == "user-agent":
            if rules:
                groups.append((agents, rules))
                agents, rules = [], []
            # Product tokens exclude trailing version/wildcard decorations.
            token = re.match(r"^[a-z_-]+", value.lower())
            agents.append("*" if value == "*" else token[0] if token else "")
        elif field in ("allow", "disallow") and agents:
            # Empty rules have no effect but still separate the next group.
            rules.append((field, value))
    if agents:
        groups.append((agents, rules))
    return groups, sitemaps


def normalize_path(value):
    # Decode percent-encoded ASCII unreserved bytes; retain reserved slash etc.
    def decoded(match):
        char = chr(int(match.group(1), 16))
        return char if re.fullmatch(r"[A-Za-z0-9._~-]", char) else match.group(0).upper()
    return re.sub(r"%([0-9a-fA-F]{2})", decoded, url.quote(value, safe="/%?=&:+,;@!$*'()[]~"))


def robots_decision(text, bot, target):
    groups, _ = robots_groups(text)
    candidates = []
    for agents, rules in groups:
        lengths = [len(a) for a in agents if a and a != "*" and a in bot.lower()]
        if lengths or "*" in agents:
            candidates.append((max(lengths, default=0), rules))
    specificity = max((size for size, _ in candidates), default=-1)
    parts = url.urlsplit(target)
    path = normalize_path((parts.path or "/") + ("?" + parts.query if parts.query else ""))
    matches = []
    for size, rules in candidates:
        if size != specificity:
            continue
        for field, raw in rules:
            if not raw or not raw.startswith("/"):
                continue
            pattern = normalize_path(raw)
            anchored = pattern.endswith("$")
            core = pattern[:-1] if anchored else pattern
            expression = "^" + ".*".join(re.escape(p) for p in core.split("*")) + ("$" if anchored else "")
            if re.search(expression, path):
                matches.append((len(core.replace("*", "").encode("utf-8")), field == "allow", field + ": " + raw))
    winner = max(matches, default=(0, True, "No matching non-empty rule"))
    return winner[1], winner[2]


def noindex_evidence(page, headers, bot):
    results = []
    for agent, value in page.robots:
        if agent in ("robots", bot.lower()) and any(p.strip().lower() in ("noindex", "none") for p in value.split(",")):
            results.append("meta " + agent + ": " + value)
    for value in headers:
        agent = "robots"
        for part in value.split(","):
            scoped = re.match(r"^\s*([\w-]+)\s*:\s*(.*)$", part)
            if scoped and scoped[1].lower() not in ("unavailable_after", "max-snippet", "max-image-preview", "max-video-preview"):
                agent, directives = scoped[1].lower(), scoped[2]
            else:
                directives = part
            if agent in ("robots", bot.lower()) and re.fullmatch(r"\s*(noindex|none)\s*", directives, re.I):
                results.append("X-Robots-Tag: " + value)
    return results


def audit(target, timeout=10):
    target = clean_url(target)
    findings, resources = [], []

    def record(check, status, evidence, action):
        verification = {
            "page-response": "Re-fetch the intended public URL; confirm the final status and HTML response.",
            "noindex": "Inspect initial and rendered metadata plus response headers; verify only authorized changes on the published page.",
            "robots": "Re-fetch robots.txt and evaluate the intended path for this bot; verify real bot/CDN access separately.",
            "sitemap": "Parse the intended sitemap and inspect canonical membership; use authorized Search Console for indexing evidence.",
            "canonical": "Compare the intended canonical with the rendered link and redirect destination.",
            "structured-data": "Validate actual JSON-LD contents and rendered markup against the eligible page type.",
        }.get(check.split(":")[0], "Inspect the initial and rendered page; confirm that the content describes the actual product.")
        findings.append(dict(check=check, status=status, evidence=evidence, action=action,
                             location=resources[-1]["url"] if resources else target,
                             priority={"block": "P1", "unknown": "P2", "warn": "P2", "info": "P3", "pass": None}[status],
                             confidence="not_checked" if status == "unknown" else "observed",
                             verification=verification))

    def request(location, same_origin_only=False):
        result = fetch(location, timeout, same_origin_only=True) if same_origin_only else fetch(location, timeout)
        resources.append({k: v for k, v in result.items() if k != "body"})
        return result

    response = request(target)
    final = response["url"]
    if response["error"] or response["status"] != 200 or response["truncated"] or response.get("content_type") not in ("text/html", "application/xhtml+xml"):
        record("page-response", "unknown" if response["error"] or response["truncated"] else "block",
               str({k: v for k, v in response.items() if k not in ("body", "x_robots_tag")}),
               "Inspect this response manually. Verify the intended public HTML page before diagnosing discovery.")
    else:
        record("page-response", "pass", "HTTP 200 HTML at " + final, "No response blocker observed for this user agent.")
        page = Page()
        page.feed(response["body"])
        for bot in ("Googlebot", "OAI-SearchBot"):
            evidence = noindex_evidence(page, response.get("x_robots_tag", []), bot)
            # Google documents scoped metadata and headers. OpenAI documents generic
            # noindex meta; do not present Google's full directive grammar as its policy.
            if bot == "OAI-SearchBot":
                generic = ["meta robots: " + v for a, v in page.robots if a == "robots" and "noindex" in [s.strip().lower() for s in v.split(",")]]
                record("noindex:" + bot, "block" if generic else "info", "; ".join(generic) or "No generic noindex meta observed; provider-specific headers and scoped directives are not verified.",
                       "OpenAI documents generic noindex meta for excluding links; preserve intentional exclusions and verify current publisher guidance.")
                continue
            record("noindex:" + bot, "block" if evidence else "pass", "; ".join(evidence) or "No applicable noindex observed in initial response.",
                   "Confirm whether exclusion is intentional; remove only on pages meant for search." if evidence else "Confirm rendered metadata if JavaScript modifies the page.")
        title = " ".join(" ".join(page.title).split())
        record("title", "pass" if title else "warn", title or "No title in initial HTML.", "Use a descriptive title; character counts are not ranking requirements.")
        record("description", "pass" if any(page.description) else "warn", "; ".join(page.description) or "No meta description in initial HTML.", "Describe the page accurately; search engines may choose their own snippet.")
        record("h1", "pass" if page.h1 else "warn", str(page.h1) + " H1 elements in initial HTML.", "Check rendered headings for a clear main topic; multiple H1s are not an automatic ranking failure.")
        base = url.urljoin(final, page.base or "")
        canonicals = [url.urljoin(base, value) for value in page.canonicals if value]
        record("canonical", "pass" if canonicals == [final] else "warn", ", ".join(canonicals) or "No canonical link in initial HTML.", "Review intended canonical; another URL can be intentional. HTTP Link headers are not checked.")
        record("structured-data", "info", str(page.jsonld) + " JSON-LD script elements in initial HTML.", "Validate contents and rendered output. Presence alone does not prove valid or eligible schema.")
    origin = url.urlunsplit(url.urlsplit(final)._replace(path="", query="", fragment=""))
    robots = request(origin + "/robots.txt")
    robots_ok = robots["status"] == 200 and not robots["truncated"] and robots.get("content_type") == "text/plain"
    for bot in BOTS:
        if robots_ok:
            rules = robots["body"]
            if bot == "Googlebot":
                rules = rules.encode("utf-8")[:GOOGLE_ROBOTS_BYTES].decode("utf-8", errors="ignore")
            elif len(rules.encode("utf-8")) > GOOGLE_ROBOTS_BYTES:
                record("robots:" + bot, "unknown", "robots.txt exceeds 500 KiB; this provider's size handling was not verified.", "Review the provider's parser limits and reduce the file without changing intended policy.")
                continue
            allowed, evidence = robots_decision(rules, bot, final)
            if bot == "Googlebot" and len(robots["body"].encode("utf-8")) > GOOGLE_ROBOTS_BYTES:
                evidence += " (Google's first 500 KiB only)"
            status = ("pass" if allowed else "block") if bot != "GPTBot" else "info"
            record("robots:" + bot, status, ("Allowed — " if allowed else "Disallowed — ") + evidence,
                   "Training policy is independent of search; preserve the publisher's choice." if bot == "GPTBot" else "Review accidental restrictions and verify CDN bot access separately.")
        else:
            google_missing = bot == "Googlebot" and robots["status"] is not None and 400 <= robots["status"] < 500 and robots["status"] != 429
            record("robots:" + bot, "info" if google_missing else "unknown", "robots.txt HTTP " + str(robots["status"]) + (" — Google treats this 4xx as no robots restrictions." if google_missing else " — rule access was not evaluated."), "Inspect robots content, errors, redirects, and CDN policy. Do not assume search visibility.")
    _, declared = robots_groups(robots["body"] if robots_ok else "")
    candidates = []
    skipped = []
    for candidate in declared:
        try:
            candidate = clean_url(candidate)
            if same_origin(origin, candidate):
                candidates.append(candidate)
            else:
                skipped.append("Declared cross-origin sitemap not fetched.")
        except ValueError:
            skipped.append("Malformed sitemap declaration ignored.")
    if skipped:
        record("sitemap-selection", "info", " ".join(dict.fromkeys(skipped)), "Review declared sitemap locations manually; cross-origin sitemaps can be valid but are outside this helper's scope.")
    sitemap_url = candidates[0] if candidates else origin + "/sitemap.xml"
    sitemap = request(sitemap_url, same_origin_only=True)
    try:
        if sitemap["status"] != 200 or sitemap["truncated"]:
            raise ValueError("HTTP " + str(sitemap["status"]) + "; truncated=" + str(sitemap["truncated"]))
        root = ET.fromstring(sitemap["body"])
        kind = root.tag.split("}")[-1]
        if kind not in ("urlset", "sitemapindex"):
            raise ValueError("Unexpected XML root: " + kind)
        entries = [(element.text or "").strip() for element in root.iter() if element.tag.split("}")[-1] == "loc"]
        if kind == "sitemapindex":
            record("sitemap", "info", "Sitemap index with " + str(len(entries)) + " children. Children not fetched.", "Inspect the appropriate child to check inclusion of the audited URL.")
        else:
            record("sitemap", "pass" if final in entries else "warn", str(len(entries)) + " URLs; audited URL " + ("present." if final in entries else "not found in this file."), "This samples one file. Include intended canonical URLs; missing membership is not an indexing prohibition.")
    except (ValueError, ET.ParseError) as exc:
        record("sitemap", "unknown", str(exc), "Inspect the intended XML sitemap. Missing or unparsed sitemap does not prove indexing failure.")
    return dict(version="0.2.0", requested_url=target, final_url=final,
                checked_at=dt.datetime.now(dt.timezone.utc).isoformat(), resources=resources, findings=findings,
                limits=["Initial responses only; no JavaScript rendering or actual bot impersonation.", "One page, robots.txt, one same-origin sitemap; 1 MiB per response. Cross-origin sitemap redirects are not followed.", "Google robots rules use the first 500 KiB; large-file handling for other providers is not verified.", "OpenAI generic noindex meta is checked; its support for scoped meta and X-Robots-Tag is not assumed.", "No indexing, ranking, citation, conversion, or Core Web Vitals verification.", "Robots evaluator covers common rules; vendor-specific behavior and cached policies need separate verification."])


def markdown(report):
    lines = ["# Discovery audit", "", "URL: " + report["final_url"], "Checked: " + report["checked_at"], ""]
    for finding in report["findings"]:
        lines += ["## " + finding["status"].upper() + " · " + finding["check"], "", "Location: " + finding["location"],
                  "Priority: " + (finding["priority"] or "none") + " · Confidence: " + finding["confidence"], "",
                  finding["evidence"], "", "Next: " + finding["action"], "", "Verify: " + finding["verification"], ""]
    return "\n".join(lines + ["## Limits", ""] + ["- " + item for item in report["limits"]])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--timeout", type=float, default=10, help="Seconds per request (0 < timeout <= 30)")
    parser.add_argument("--fail-on-block", action="store_true", help="Exit 1 if an observed discovery block is found")
    args = parser.parse_args()
    if not 0 < args.timeout <= 30:
        parser.error("Timeout must be between 0 and 30 seconds.")
    try:
        report = audit(args.url, args.timeout)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, ensure_ascii=False) if args.format == "json" else markdown(report))
    return int(args.fail_on_block and any(f["status"] == "block" for f in report["findings"]))


if __name__ == "__main__":
    sys.exit(main())
