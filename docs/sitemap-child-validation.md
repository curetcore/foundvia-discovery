# Child sitemap inspection validation

October 6, 2026. The opt-in `--sitemap-children N` option addresses a limitation observed during live agent checks: the helper previously reported an index without checking page membership in its children.

## Behavior

The default still performs the original three-resource audit. With a limit of 1–5, the helper reads at most that many unique same-origin child files at one level. It rejects unsafe locations and cross-origin redirects, preserves child errors, and distinguishes a partial sample from a complete eligible-index check. Finding a URL proves only sitemap listing.

## Validation

- 53 Python tests passed locally on Python 3.14.7, including 10 new regressions for second-child membership, root URL equivalence, request limits, duplicate/unsafe/self-referencing locations, nested indexes, malformed/oversized responses, retained errors, and CLI argument rejection.
- Live foundvia.dev audit with limit 3: one child parsed, homepage found, 9 PASS / 5 INFO, no warnings or unknowns.
- Live karrito.app audit with limit 3: two children parsed and homepage found in sitemap-static.xml. sitemap-products.xml exceeded the helper's 1 MiB cap; report retained one UNKNOWN and incomplete/partial coverage. The cap is a tool inspection limit, not a declaration that the sitemap is invalid.
- Existing JSON fields remain; version 0.4.0 adds sitemap_coverage. Earlier frozen agent/benchmark records remain historical snapshots.

These are helper behavior checks and live response samples, not a new agent-selection benchmark, whole-site crawl, indexing verification, or growth result. Remote CI results are attached to the publishing pull request.
