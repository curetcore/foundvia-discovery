# Run a discovery audit

Python 3.10+; standard library only. From the repository root, the short entry point forwards all audit arguments and exit codes:

```bash
python3 discovery.py audit https://example.com
python3 discovery.py practice
```

The original standalone helper remains available:

```bash
python3 skills/foundvia-discovery/scripts/discovery_audit.py https://example.com
python3 skills/foundvia-discovery/scripts/discovery_audit.py https://example.com --format json > audit.json
python3 skills/foundvia-discovery/scripts/discovery_audit.py https://example.com --timeout 5 --fail-on-block
```

| Option | Behavior |
|---|---|
| `--format markdown` | Human-readable evidence and next actions (default) |
| `--format json` | Resources, timestamps, findings, and limitations |
| `--timeout N` | Per-network-operation timeout in seconds; default 10, maximum 30. Not a whole-run deadline |
| `--fail-on-block` | Exit 1 for an observed block; default completion exits 0 |

Invalid input exits 2. `unknown` findings do not trigger `--fail-on-block`; this option is not a complete SEO CI gate.

## Checked

- One page: final HTTP response, HTML title/description/H1, canonical links, relevant noindex metadata and response headers, JSON-LD element presence.
- Final origin's `/robots.txt`: common bot-group selection, wildcard and end-anchor rules, longest-match selection, equal-rule Allow precedence, empty rules, and percent-encoding normalization.
- One sitemap declared in robots on the same origin, or `/sitemap.xml`: XML parsing, root type, and audited-URL membership for a URL set. Sitemap index children are not fetched.

Rules for Googlebot and OAI-SearchBot are evaluated independently. GPTBot access is informational: training preference is not a search-discovery failure. A missing Google robots file with a non-429 4xx is reported according to Google's documented handling. Other unverified bot behavior remains unknown.

Google uses the first 500 KiB of robots.txt. Other crawler behavior for files beyond that size is unknown here. Generic HTML noindex is reported separately for OpenAI; Google-specific scopes and response-header extensions are not assumed to have equivalent OpenAI support.

Each finding includes location, status, evidence, priority, confidence, next action, and verification. Observed blocks use P1, warnings/unknowns P2, and information P3. Passing checks have no action priority. These are preflight triage labels, not ranking scores; the user must confirm whether a restriction is intentional.

## Limits you should understand

This is a **small preflight**, not a full crawler or ranking forecast. Up to three resources are fetched, plus HTTP redirects, with a 1 MiB cap per response. Resources that exceed the cap are unknown. Only `text/plain` 200 robots responses are evaluated conservatively. Robots parser behavior covers common documented patterns, not every vendor extension or cached-policy state. Redirected cross-origin robots scopes need manual review.

Requests use `FoundviaDiscovery/0.1`, not a spoofed crawler identity. A pass cannot establish that a real bot passes a CDN/WAF. TLS verification remains enabled. The helper sends no API keys or browser-session cookies; URLs must not contain credentials. Do not put private query tokens in audit URLs or publish raw reports containing sensitive paths.

Malformed sitemap declarations are skipped with evidence. Same-origin uses scheme, hostname, and effective port; the helper rejects cross-origin sitemap redirects before following them. This is its bounded scope, not a claim that cross-origin sitemaps are invalid. Redirect URLs are validated before requests, including credential rejection.

No JavaScript rendering, real-user Core Web Vitals, sitemap recursion, canonical target requests, HTTP Link canonical parsing, whole-site orphan detection, or Search Console inspection. HTML findings apply only to the initial response. JSON-LD presence does not validate its content. No indexing, traffic, citations, or conversions are confirmed.

If the request fails, the helper reports the response problem instead of inventing missing metadata. An intentional login or private page should not be made public to turn an audit green.

## Verification

The automated tests use a local HTTP server with redirects, noindex headers, oversized HTML, errors, and an independently declared sitemap. No live service is needed:

```bash
python3 -m unittest discover -s tests -v
```

For actual indexing, use authorized Search Console URL Inspection. For rendered metadata and schema, inspect a rendered browser page and the relevant validation tool. Read [primary-source guidance](../skills/foundvia-discovery/references/discovery.md).
