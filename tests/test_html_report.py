"""Report packaging and escaping against untrusted fetched content."""
import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/foundvia-discovery/scripts/discovery_audit.py'
spec = importlib.util.spec_from_file_location('html_audit', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Tags(HTMLParser):
    def __init__(self):
        super().__init__(); self.tags=[]
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class HTMLReportTests(unittest.TestCase):
    def report(self):
        # Public-network access is deliberately unavailable in this fixture.
        from unittest.mock import patch
        def failed(target, timeout, same_origin_only=False):
            return dict(url=target,status=None,body='',error='Connection refused',truncated=False)
        with patch.object(m,'fetch',side_effect=failed):return m.audit('https://example.com')

    def test_source_text_cannot_create_executable_markup_or_links(self):
        r=self.report();payload='</script><img src=x onerror=alert(1)><script>alert(2)</script>'
        for field in ('check','evidence','action','verification','confidence','priority'):
            r['findings'][0][field]=payload
        r['findings'][0]['location']='javascript:alert(3)'
        r['summary']['scope']=payload
        rendered=m.html_report(r);tags=Tags();tags.feed(rendered)
        self.assertEqual(len([t for t,a in tags.tags if t=='script']),1)
        self.assertFalse(any(t=='img' or any(k.startswith('on') for k in a) for t,a in tags.tags))
        self.assertFalse(any(a.get('href','').startswith('javascript:') for _,a in tags.tags))
        self.assertIn('&lt;/script&gt;',rendered)

    def test_offline_assets_status_semantics_and_accessible_controls(self):
        rendered=m.html_report(self.report());tags=Tags();tags.feed(rendered)
        self.assertIn('data:font/woff2;base64,',rendered)
        self.assertIn('SIL OPEN FONT LICENSE',rendered)
        self.assertIn('Incomplete within the inspection scope',rendered)
        self.assertTrue(any(t=='p' and a.get('role')=='status' for t,a in tags.tags))
        self.assertEqual(len([t for t,a in tags.tags if a.get('data-status')=='unknown']),5)
        self.assertFalse(any(t in ('script','link') and ('src' in a or 'href' in a) for t,a in tags.tags))
        self.assertTrue(all(a.get('rel')=='noopener noreferrer' for t,a in tags.tags if t=='a'))

    def test_cli_html_flag_generates_report_and_preserves_strict_exit(self):
        proc=subprocess.run([sys.executable,str(SCRIPT),'http://127.0.0.1:1','--format','html','--require-complete','--timeout','1'],capture_output=True,text=True)
        self.assertEqual(proc.returncode,3,proc.stderr)
        self.assertIn('<!doctype html>',proc.stdout)
        self.assertIn('Connection refused',proc.stdout)
