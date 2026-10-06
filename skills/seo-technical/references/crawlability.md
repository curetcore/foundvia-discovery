# Crawl and indexing investigation

Record the requested URL, final URL/status, headers, robots response, initial and rendered metadata, canonical, and sitemap evidence. Use authorized Search Console inspection to distinguish a discovered page from an indexed page.

Compare bot-specific rules: the most specific matching group does not inherit wildcard disallows. Preserve private exclusions in appropriate groups. Google uses the first 500 KiB of robots.txt; do not apply rules beyond that bound. For another crawler, use its own documented behavior instead of generalizing Google's extensions or error handling.

Keep CSS, JavaScript, images, and framework resources needed for rendering accessible. Authentication protects private data; robots is not an access-control mechanism. An exclusion can prevent a crawler from reading noindex. A sitemap can aid discovery but cannot force indexing.

For canonical issues, compare equivalent content and the actual intended URL. Preserve meaningful query parameters. Align redirects, internal links, and sitemap entries; never point unrelated routes to the homepage. Verify the live route after deployment without claiming a recrawl deadline.

Sources: [robots specification](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec), [canonical guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls).
