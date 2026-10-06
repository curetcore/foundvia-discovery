---
name: seo-slug-dates
description: Audit publication dates, dateModified, and sitemap lastmod for truthful source records, and migrate away from synthetic slug-derived history. Use when page dates are generated, inaccurate, or reset on every build.
---

# Truthful content dates

This skill keeps its existing name for discoverability but withdraws the former hash-based date-distribution approach. Deterministic invented dates are still invented. Shared dates are valid when the underlying events happened together.

Inspect callers of publishedAt, updatedAt, datePublished, dateModified, and sitemap lastmod. Use actual CMS, database, frontmatter, or verified content history; a deployment timestamp is not automatically a significant content-update timestamp. Preserve real dates. Omit optional dates when no reliable record exists.

Use [scripts/dates.ts](scripts/dates.ts) to validate explicit date records. It exports contentDates; the old slug-generated-date functions have been removed. Update callers intentionally and run the project's typecheck/build before deployment. Document the migration rather than silently changing dates across a live site.

Check displayed dates, schema, and sitemap consistently. Confirm chronology and meaningful content changes; do not require dates to differ across pages. No ranking or citation improvement is promised.

Source: [Google sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap). See [migration explanation](../../playbook/slug-date-distribution.md).
