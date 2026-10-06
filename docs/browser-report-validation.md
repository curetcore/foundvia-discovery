# Browser report validation — 2026-10-06

The HTML export reuses the Python auditor findings and scope; it does not add crawler or ranking verification.

## Automated checks

- Python: 56 tests passed locally, including three HTML regressions for escaping, embedded assets/accessibility structure and strict CLI exit status.
- Repository integrity: 75 Markdown files checked; flagship template, font and font license are required package files.
- `git diff --check`: passed.

## Browser checks

Chrome opened a report generated from the recorded Karrito child-sitemap audit (06 Oct 2026, 20:30 UTC). UNKNOWN remained visible for the child response exceeding the 1 MiB limit, and coverage remained incomplete.

- UNKNOWN filter showed 1 of 16 findings.
- BLOCK filter showed 0 of 16 and the empty-state explanation.
- All filter restored 16 findings.
- Enter on the native UNKNOWN summary collapsed its details.
- At 390 px and 320 px, document width equalled viewport width; no horizontal overflow was observed.
- Desktop and 390 px screenshots were inspected. The temporary viewport override was reset.

Print styles and before/after-print handlers are included, but an actual print/PDF export was not tested. Other browsers, screen-reader navigation and physical mobile devices remain unverified. The report interface is English. The exported file embeds its font and license and uses no external display resources; clicked resource links require a connection.
