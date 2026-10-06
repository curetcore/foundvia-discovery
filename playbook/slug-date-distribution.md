# Truthful content dates

The earlier hash-based date distribution advice is withdrawn. There is no evidence here that identical dates create a special “batch penalty,” and a stable hash does not make an invented date true.

Use the actual publication and significant content-update dates from your CMS, database, frontmatter, or verified version history. Pages published together may correctly share a date. A build, CSS change, or deployment does not automatically mean all content changed.

For sitemap lastmod, [Google asks for the last significant update](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap). It ignores sitemap priority and changefreq. If a reliable date is unavailable, omit optional metadata instead of inventing history.

## Helper and migration

[`contentDates`](../skills/seo-slug-dates/scripts/dates.ts) accepts explicit records. The previous slugToDates/slugToPublishedDate/slugToModifiedDate API has been removed because it generated unsupported dates. Existing consumers must migrate deliberately:

```ts
import { contentDates } from "./dates";

const dates = contentDates({
  publishedAt: page.publishedAt,
  updatedAt: page.lastSignificantContentUpdate,
});

// JSON-LD: omit undefined values.
const article = { datePublished: dates.datePublished, dateModified: dates.dateModified };
// Sitemap: omit lastModified if dates.dateModified is undefined.
```

Recover dates from actual records. Do not replace historical synthetic values with a fresh synthetic range. If a date is unknown, omit it; do not claim it happened today. Invalid or future dates and modification dates before publication are rejected by the helper.
