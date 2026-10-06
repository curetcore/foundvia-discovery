# Discovery audit

URL: http://127.0.0.1:60326/guide
Checked: 2026-10-06T18:10:46.157454+00:00

## PASS · page-response

Location: http://127.0.0.1:60326/guide
Priority: none · Confidence: observed

HTTP 200 HTML at http://127.0.0.1:60326/guide

Next: No response blocker observed for this user agent.

Verify: Re-fetch the intended public URL; confirm the final status and HTML response.

## PASS · noindex:Googlebot

Location: http://127.0.0.1:60326/guide
Priority: none · Confidence: observed

No applicable noindex observed in initial response.

Next: Confirm rendered metadata if JavaScript modifies the page.

Verify: Inspect initial and rendered metadata plus response headers; verify only authorized changes on the published page.

## INFO · noindex:OAI-SearchBot

Location: http://127.0.0.1:60326/guide
Priority: P3 · Confidence: observed

No generic noindex meta observed; provider-specific headers and scoped directives are not verified.

Next: OpenAI documents generic noindex meta for excluding links; preserve intentional exclusions and verify current publisher guidance.

Verify: Inspect initial and rendered metadata plus response headers; verify only authorized changes on the published page.

## PASS · title

Location: http://127.0.0.1:60326/guide
Priority: none · Confidence: observed

How to put your music links in one Instagram bio

Next: Use a descriptive title; character counts are not ranking requirements.

Verify: Inspect the initial and rendered page; confirm that the content describes the actual product.

## PASS · description

Location: http://127.0.0.1:60326/guide
Priority: none · Confidence: observed

A practical checklist for sharing music, shows and contact links in one public page.

Next: Describe the page accurately; search engines may choose their own snippet.

Verify: Inspect the initial and rendered page; confirm that the content describes the actual product.

## PASS · h1

Location: http://127.0.0.1:60326/guide
Priority: none · Confidence: observed

1 H1 elements in initial HTML.

Next: Check rendered headings for a clear main topic; multiple H1s are not an automatic ranking failure.

Verify: Inspect the initial and rendered page; confirm that the content describes the actual product.

## PASS · canonical

Location: http://127.0.0.1:60326/guide
Priority: none · Confidence: observed

http://127.0.0.1:60326/guide

Next: Review intended canonical; another URL can be intentional. HTTP Link headers are not checked.

Verify: Compare the intended canonical with the rendered link and redirect destination.

## INFO · structured-data

Location: http://127.0.0.1:60326/guide
Priority: P3 · Confidence: observed

0 JSON-LD script elements in initial HTML.

Next: Validate contents and rendered output. Presence alone does not prove valid or eligible schema.

Verify: Validate actual JSON-LD contents and rendered markup against the eligible page type.

## PASS · robots:Googlebot

Location: http://127.0.0.1:60326/robots.txt
Priority: none · Confidence: observed

Allowed — allow: /

Next: Review accidental restrictions and verify CDN bot access separately.

Verify: Re-fetch robots.txt and evaluate the intended path for this bot; verify real bot/CDN access separately.

## PASS · robots:OAI-SearchBot

Location: http://127.0.0.1:60326/robots.txt
Priority: none · Confidence: observed

Allowed — allow: /

Next: Review accidental restrictions and verify CDN bot access separately.

Verify: Re-fetch robots.txt and evaluate the intended path for this bot; verify real bot/CDN access separately.

## INFO · robots:GPTBot

Location: http://127.0.0.1:60326/robots.txt
Priority: P3 · Confidence: observed

Disallowed — disallow: /

Next: Training policy is independent of search; preserve the publisher's choice.

Verify: Re-fetch robots.txt and evaluate the intended path for this bot; verify real bot/CDN access separately.

## PASS · sitemap

Location: http://127.0.0.1:60326/sitemap.xml
Priority: none · Confidence: observed

1 URLs; audited URL present.

Next: This samples one file. Include intended canonical URLs; missing membership is not an indexing prohibition.

Verify: Parse the intended sitemap and inspect canonical membership; use authorized Search Console for indexing evidence.

## Limits

- Initial responses only; no JavaScript rendering or actual bot impersonation.
- One page, robots.txt, one same-origin sitemap; 1 MiB per response. Cross-origin sitemap redirects are not followed.
- Google robots rules use the first 500 KiB; large-file handling for other providers is not verified.
- OpenAI generic noindex meta is checked; its support for scoped meta and X-Robots-Tag is not assumed.
- No indexing, ranking, citation, conversion, or Core Web Vitals verification.
- Robots evaluator covers common rules; vendor-specific behavior and cached policies need separate verification.
