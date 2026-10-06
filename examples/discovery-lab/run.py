"""Run a loopback-only before/after example. Python 3.10+, no dependencies."""
import argparse
import html
import json
from pathlib import Path
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[2]
AUDITOR = ROOT / 'skills/foundvia-discovery/scripts/discovery_audit.py'
NOINDEX = '<meta name="robots" content="noindex">'


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    blocked = True
    origin = ''

    def page():
        return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>How to put your music links in one Instagram bio</title>
<meta name="description" content="A practical checklist for sharing music, shows and contact links in one public page.">
<link rel="canonical" href="{html.escape(origin)}/guide">
{NOINDEX if blocked else ''}
</head><body><main>
<h1>How to put your music links in one Instagram bio</h1>
<p>Make one public page with your streaming, upcoming show and contact links. Add that page's URL to your Instagram profile.</p>
<ol><li>Gather your current music and show URLs.</li>
<li>Add clear labels: Listen, Next show, Contact.</li>
<li>Open each link on your phone while signed out.</li>
<li>Paste the public page URL in your profile and test it again.</li></ol>
<p>Check outdated show dates regularly. This demo does not connect to Instagram or create a page for you.</p>
</main></body></html>'''

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path in ('/', '/guide'):
                body, kind = page(), 'text/html'
            elif self.path == '/robots.txt':
                body = f'User-agent: *\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: GPTBot\nDisallow: /\n\nSitemap: {origin}/sitemap.xml\n'
                kind = 'text/plain'
            elif self.path == '/sitemap.xml':
                body = f'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{origin}/guide</loc></url></urlset>'
                kind = 'application/xml'
            else:
                self.send_error(404)
                return
            encoded = body.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', kind + '; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    origin = f'http://127.0.0.1:{server.server_port}'
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    started = time.perf_counter()
    try:
        results = {}
        first_report_seconds = None
        for stage in ('before', 'after', 'clean'):
            blocked = stage == 'before'
            (output / (stage + '.html')).write_text(page(), encoding='utf-8')
            for fmt, suffix in (('json', 'json'), ('markdown', 'md')):
                proc = subprocess.run([sys.executable, str(AUDITOR), origin + '/guide', '--format', fmt, '--fail-on-block'], capture_output=True, text=True, timeout=30)
                if proc.returncode not in (0, 1):
                    raise RuntimeError(proc.stderr or 'Auditor failed')
                (output / (stage + '.' + suffix)).write_text(proc.stdout, encoding='utf-8')
                if fmt == 'json':
                    results[stage] = {'exit_code': proc.returncode, 'report': json.loads(proc.stdout)}
                    if stage == 'before':
                        first_report_seconds = time.perf_counter() - started
        summary = {
            'kind': 'controlled-local-fixture-not-growth-evidence',
            'python': sys.version.split()[0],
            'first_json_report_seconds': round(first_report_seconds, 4),
            'timing_scope': 'Server ready to first CLI JSON report; excludes prerequisite installation, reading and human actions.',
            'stages': {stage: {'exit_code': item['exit_code'], 'blocks': [f['check'] for f in item['report']['findings'] if f['status'] == 'block']} for stage, item in results.items()},
        }
        (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
        return summary
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='outputs-local/discovery-lab')
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2))
