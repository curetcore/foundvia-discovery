"""Bounded child sitemap membership, coverage, and transport regressions."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/foundvia-discovery/scripts/discovery_audit.py'
spec = importlib.util.spec_from_file_location('child_audit', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
ORIGIN = 'https://example.com'


def index(locations):
    return '<sitemapindex>' + ''.join('<sitemap><loc>' + x + '</loc></sitemap>' for x in locations) + '</sitemapindex>'


def urls(locations):
    return '<urlset>' + ''.join('<url><loc>' + x + '</loc></url>' for x in locations) + '</urlset>'


class SitemapChildrenTests(unittest.TestCase):
    def report(self, locations, children, limit=2):
        calls = []
        def fetch(target, timeout, same_origin_only=False):
            calls.append((target, same_origin_only))
            if target == ORIGIN + '/':
                body, kind = '<title>Public product</title>', 'text/html'
            elif target.endswith('/robots.txt'):
                body, kind = 'User-agent: *\nAllow: /', 'text/plain'
            elif target.endswith('/sitemap.xml'):
                body, kind = index(locations), 'application/xml'
            else:
                body, kind = children[target], 'application/xml'
            if isinstance(body, dict):
                return dict(url=target, body='', content_type=kind, **body)
            return dict(url=target, status=200, body=body, error=None, truncated=False, content_type=kind)
        with patch.object(m, 'fetch', side_effect=fetch):
            report = m.audit(ORIGIN, sitemap_children=limit)
        return report, calls

    def membership(self, report):
        return next(f for f in report['findings'] if f['check'] == 'sitemap-membership')

    def test_target_in_second_child_and_root_url_equivalence(self):
        a,b = ORIGIN+'/a.xml', ORIGIN+'/b.xml'
        report,calls = self.report([a,b], {a:urls([ORIGIN+'/other']), b:urls([ORIGIN])})
        self.assertEqual(self.membership(report)['status'], 'pass')
        self.assertEqual(report['sitemap_coverage']['matching_sitemaps'], [b])
        self.assertEqual(self.membership(report)['location'], ORIGIN+'/sitemap.xml')
        self.assertEqual(report['sitemap_coverage']['children_parsed'], 2)
        self.assertTrue(all(scoped for target,scoped in calls if target.endswith('.xml')))

    def test_missing_from_limited_sample_is_not_whole_index_warning(self):
        a,b = ORIGIN+'/a.xml', ORIGIN+'/b.xml'
        report,calls = self.report([a,b], {a:urls([ORIGIN+'/other'])}, limit=1)
        self.assertEqual(self.membership(report)['status'], 'info')
        self.assertEqual(report['sitemap_coverage']['membership'], 'not_verified')
        self.assertTrue(report['sitemap_coverage']['partial'])
        self.assertNotIn(b, [target for target,_ in calls])

    def test_missing_from_all_children_warns_without_indexing_claim(self):
        a = ORIGIN+'/a.xml'
        report,_ = self.report([a], {a:urls([ORIGIN+'/other'])})
        self.assertEqual(self.membership(report)['status'], 'warn')
        self.assertEqual(report['sitemap_coverage']['membership'], 'not_found')
        self.assertIn('does not prove indexing', self.membership(report)['action'])

    def test_failed_child_keeps_cause_and_makes_membership_unknown(self):
        a = ORIGIN+'/a.xml'
        report,_ = self.report([a], {a:dict(status=None,error='Connection timed out',truncated=False)})
        self.assertEqual(self.membership(report)['status'], 'unknown')
        self.assertTrue(report['summary']['incomplete'])
        child = next(f for f in report['findings'] if f['check']=='sitemap-child')
        self.assertIn('Connection timed out', child['evidence'])

    def test_found_target_does_not_hide_another_failed_child(self):
        a,b = ORIGIN+'/a.xml', ORIGIN+'/b.xml'
        report,_ = self.report([a,b], {a:urls([ORIGIN]),b:dict(status=503,error=None,truncated=False)})
        self.assertEqual(self.membership(report)['status'], 'pass')
        self.assertTrue(report['summary']['incomplete'])
        self.assertTrue(report['sitemap_coverage']['partial'])

    def test_untrusted_locations_are_not_fetched_and_do_not_erase_coverage_gap(self):
        a = ORIGIN+'/a.xml'
        locations=['https://other.example/a.xml','https://user:password@example.com/private.xml','https://[bad',ORIGIN+'/sitemap.xml',a,a]
        report,calls = self.report(locations,{a:urls([ORIGIN+'/other'])})
        self.assertEqual([t for t,_ in calls if t.endswith('/a.xml')],[a])
        self.assertEqual(len(calls),4)
        self.assertEqual(self.membership(report)['status'],'info')
        self.assertNotIn('password', m.markdown(report))

    def test_nested_index_is_not_recursively_fetched(self):
        a,b = ORIGIN+'/a.xml',ORIGIN+'/b.xml'
        report,calls = self.report([a],{a:index([b])})
        self.assertNotIn(b,[t for t,_ in calls])
        self.assertEqual(report['sitemap_coverage']['children_parsed'],0)
        self.assertEqual(self.membership(report)['status'],'info')

    def test_malformed_and_oversized_child_are_unknown(self):
        a = ORIGIN+'/a.xml'
        for body in ('not XML',dict(status=200,error=None,truncated=True)):
            with self.subTest(body=body):
                report,_ = self.report([a],{a:body})
                self.assertEqual(self.membership(report)['status'],'unknown')

    def test_default_option_does_not_fetch_children(self):
        a = ORIGIN+'/a.xml'
        report,calls = self.report([a],{},limit=0)
        self.assertEqual(len(calls),3)
        self.assertEqual(report['sitemap_coverage']['membership'],'not_checked')
        self.assertNotIn('sitemap-membership',[f['check'] for f in report['findings']])

    def test_invalid_child_budget_rejected_before_network(self):
        for limit in (-1,6,1.5):
            with self.subTest(limit=limit), patch.object(m,'fetch') as fetch:
                with self.assertRaises(ValueError):m.audit(ORIGIN,sitemap_children=limit)
                fetch.assert_not_called()
        proc=subprocess.run([sys.executable,str(SCRIPT),ORIGIN,'--sitemap-children','6'],capture_output=True,text=True)
        self.assertEqual(proc.returncode,2)
        self.assertIn('between 0 and 5',proc.stderr)
