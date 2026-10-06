# Discovery checks

Use on public pages only. Crawlability, indexing, retrieval, citations, and visits are different stages.

## Google

Check the page loads signed out; main content is available; no accidental HTML or header `noindex` exists; crawler rules do not block required resources; internal links reach the page; and the sitemap names the preferred public URL. Use URL Inspection for indexing evidence if the owner has authorized access.

An allowed crawl does not guarantee indexing. A sitemap and repeated crawl requests do not force inclusion. Use truthful significant-update dates for `lastmod`; Google ignores sitemap `priority` and `changefreq`. Avoid using a robots exclusion as a way to hide private data or as a substitute for readable `noindex`.

## ChatGPT

`OAI-SearchBot` supports search; `GPTBot` supports potential training. Treat those preferences independently. `ChatGPT-User` handles certain user-initiated actions, does not determine search eligibility, and may not follow robots rules for those actions.

Check robots groups and hosting/firewall behavior. Specific bot groups need appropriate exclusions; never assume the wildcard group's disallows are inherited. Use current published crawler IP ranges if configuring access. Preserve the site's training preferences unless explicitly asked to change them.

OpenAI's publisher FAQ documents generic HTML `noindex` for excluding even link/title listings, which its crawler must be able to read. Do not assume all Google-specific metadata scopes or X-Robots-Tag extensions have equivalent OpenAI support. Report unsupported or untested provider behavior as unknown.

## Content and schema

Google does not require special AI schema or `llms.txt` for its generative search features. Do not treat a top-20 ranking as a universal prerequisite for citations. Use accurate structured data when appropriate for the actual page; never invent review counts or ratings. FAQs can help readers, but do not promise FAQ rich results: Google's 2026 changelog says the feature was removed.

## Official sources

- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/crawling-indexing/block-indexing
- https://developers.google.com/search/docs/crawling-indexing/robots/intro
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- https://developers.google.com/search/updates
- https://developers.openai.com/api/docs/bots
- https://help.openai.com/en/articles/12627856-publishers-and-developers-faq

Guidance checked October 6, 2026; recheck when advising on provider-specific behavior.
