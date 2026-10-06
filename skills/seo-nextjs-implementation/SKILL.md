---
name: seo-nextjs-implementation
description: Implement route-specific Next.js App Router metadata, truthful structured data, canonical URLs, robots, and sitemaps in an authorized codebase. Use for concrete Next.js implementation; inspect the installed version and validate affected routes before claiming compatibility.
---

# Next.js discovery implementation

Inspect package versions, route conventions, existing metadata, and repository instructions before editing. Reuse the app's implementation rather than replacing it with a template. Audit-only requests authorize proposed changes, not edits or deployment.

## Metadata and canonical URLs

Keep shared defaults in the layout and route-specific title, description, URL, and canonical on the actual page. A layout cannot infer every child route. Do not canonicalize all pages to the homepage. Confirm file-based metadata precedence and existing title templates before adding another suffix.

[scripts/seo.ts](scripts/seo.ts) is an optional copyable helper requiring Next.js metadata types and React. Replace all Brand/example.com/yourhandle defaults before use. Its generateMetadata() now omits canonical/openGraph.url unless a route URL is provided. getCanonicalUrl(path, removeParams) preserves query parameters by default; explicitly list tracking parameters to remove. Review callers migrating from the old strip-all-query behavior.

## Structured data

Choose a schema that describes visible real content; verify feature eligibility separately. The JsonLd component escapes less-than characters before script embedding. Use genuine dates, prices, authors, availability, and ratings. Unknown dateModified, author URLs, and availability are omitted instead of invented. FAQPage remains an optional schema export, not a promise of Google FAQ rich results.

## Robots and sitemaps

Preserve private routes and training policy. Keep rendering assets accessible. Build sitemap entries from real canonical public routes and actual content dates. Treat crawler access, indexing, ranking, and AI referrals as separate checks.

## Verification and handoff

Run the app's typecheck/build and inspect affected rendered routes, metadata, schema, robots, and sitemap. Test dynamic routes, missing records, and query-dependent pages. Local helper tests do not establish full framework/build compatibility. Distinguish local changes, deployment, and live verification; do not promise rich results in a fixed number of weeks.

Sources: [Next.js metadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata), [safe JSON-LD](https://nextjs.org/docs/app/guides/json-ld).
