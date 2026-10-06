# Module decisions — October 6, 2026

All eleven entrypoints and their local references were inspected. This is an editorial/source review and a controlled helper review, not certification of every module in every agent. The English focused modules keep their existing names and paths for discoverability. The flagship remains the default entrypoint; no forced merger makes users load the entire pack.

| Module | Decision | Corrected behavior | Validation boundary |
|---|---|---|---|
| foundvia-discovery | Keep and correct | Bounded audit; independent search/training; provider-specific noindex; actionable reports | Python fixture suite; eight text-artifact A/B scenarios reviewed |
| seo-ai-geo | Keep and correct | Optional llms.txt; no citation-format guarantees; generic OpenAI noindex scope | Source review; flagship reasoning cases cover overlapping policies |
| seo-slug-dates | Keep corrected migration | Real content dates; no synthetic history or identical-date penalty | Executable date helper checks |
| seo-technical | Correct | Rendering assets accessible; field vs lab data; no ranking claims for security headers | Source review; audit helper covers a bounded subset |
| seo-on-page | Correct | Editorial titles/descriptions; intentional canonical policy; useful links without quotas | Source review; helper metadata/canonical tests |
| seo-content-strategy | Correct | Original demand/proof; no word-count or date-change percentage rules | Source review; flagship launch/date cases |
| seo-local | Correct | Real eligible locations; truthful details; no self-serving review-star shortcut | Source review; no live Business Profile actions tested |
| seo-analytics | Correct | Parse exact hosts; clicks/sessions/conversions distinct; investigate traffic-loss evidence | Source review; flagship attribution/drop cases |
| seo-growth-engine | Correct; advanced only | One useful experiment, not mass niche/article quotas or forecasts | Source review; no publishing/outreach executed |
| seo-nextjs-implementation | Correct | Escaped JSON-LD; route-specific canonical; meaningful queries retained; unknown schema facts omitted | Six actual helper tests with React; no full Next.js app build certification |
| seo-audit-website | Withdraw old workflow; optional adapter | Rewritten report review; no remote shell install, automatic delegation, or vendor-score claims | Source review only; no squirrelscan compatibility claimed |

## Material changes and migration

The old third-party scanner instructions and unsafe/inaccurate implementation templates were replaced with original scoped guidance. Historical versions remain in Git history; do not copy them back as current recommendations. The references now explain acceptance and verification instead of untested traffic forecasts. The earlier synthetic-date functions were already withdrawn; this objective retains the truthful replacement.

The Next.js helper still requires an actual application to supply React and Next.js types. Replace all example defaults. Shared metadata now omits canonical/openGraph.url without a supplied route URL; add the route URL at the page. `getCanonicalUrl(path, removeParams)` keeps query parameters by default; pass specific tracking parameters to delete. Review existing callers before deployment. Unknown dateModified, author URL, and offer availability are no longer invented.

The Python report version is 0.2.0. Additive fields are location, priority, confidence, and verification; existing status/evidence/action remain. OpenAI-specific noindex output is deliberately narrower than Google's grammar. Consumers should not treat info/unknown as a complete bot-access pass.

## Primary-source ledger

Checked October 6, 2026. These sources support provider behavior; our module selection and report priorities are product decisions, not provider requirements.

| Source | Decision it supports |
|---|---|
| [Google robots specification](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec) | Group selection, common matching, 500 KiB processing limit, distinct error handling |
| [Google robots metadata](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag) | Google noindex scope and readable directives |
| [OpenAI bots](https://developers.openai.com/api/docs/bots) | Independent search/training/user-action crawler roles |
| [OpenAI publisher FAQ](https://help.openai.com/en/articles/12627856-publishers-and-developers-faq) | Generic noindex and ChatGPT referral attribution; no extrapolation to undocumented header scopes |
| [Google AI guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | No special AI discovery files/schema prerequisite |
| [Google updates](https://developers.google.com/search/updates) | FAQ rich-result removal and llms.txt clarification |
| [Titles](https://developers.google.com/search/docs/appearance/title-link) / [snippets](https://developers.google.com/search/docs/appearance/snippet) | Descriptive editorial metadata instead of mandatory character cutoffs |
| [Helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | Original reader value; no prescribed word count or fake freshness |
| [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies) | Avoid scaled search manipulation, doorway pages, and link spam |
| [Business eligibility](https://support.google.com/business/answer/13763036) / [LocalBusiness](https://developers.google.com/search/docs/appearance/structured-data/local-business) / [reviews](https://developers.google.com/search/docs/appearance/structured-data/review-snippet) | Real eligible businesses and review-feature limits |
| [Web Vitals](https://web.dev/articles/vitals) | Field thresholds and measurement context |
| [Next.js JSON-LD](https://nextjs.org/docs/app/guides/json-ld) | Escape script embedding; validate real schema |
| [Third-party SEO advice](https://developers.google.com/search/docs/fundamentals/third-party-seo) | Verify vendor findings; scores do not establish rankings |
| [MDN HSTS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security) / [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) | Security-control semantics; deployment-specific review |

## Verified scope

A clean project installation using Skills CLI 1.7.0 copies the whole flagship folder and runs its JSON/Markdown helper against a local fixture. The Python fixture suite passes 31 tests; the Next.js helper passes six actual React/URL/schema tests; the date helper passes 11 assertions. All eleven skill structures and 41 local Markdown files pass structural/link checks. Agent results are limited to Codex CLI 0.157.0, gpt-6-astra, supplied-artifact reasoning: 24/24 case sets pass in each condition, with no demonstrated uplift. Local checks used Python 3.14.7, Node 24.20.0, and Node 22.18.0 with React 19.2.0. CI is configured for Python 3.10, which was not executed locally, and Node 22.18; remote candidate CI has not run. No ranking, real bot/CDN access, organic traffic, third-party compatibility, full Next.js app build, automatic skill selection, or release on main is established.
