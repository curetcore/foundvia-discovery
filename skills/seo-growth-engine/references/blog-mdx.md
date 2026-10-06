# A tested tutorial, not a publishing quota

Start with one task a customer needs to complete. Reproduce the steps in the actual product/version, then write the direct answer, prerequisites, steps, expected result, failure cases, and relevant next resource. A tutorial's length follows its task; do not fabricate publication history or inflate the page count.

For an MDX app, inspect its existing loader and trusted content source. Follow the installed Next.js MDX conventions rather than mixing loaders from unrelated examples. MDX can contain executable code; do not compile untrusted user submissions as trusted server content.

Use truthful title, summary, author, publishedAt, and optional significant updatedAt records. Validate records with the date helper where suitable. Resolve route records safely and return a real not-found response for missing content. Keep the same URL and dates in visible content, metadata, and schema.

Acceptance: build the app, open an actual article and a missing slug, verify metadata/dates/links, and reproduce the tutorial's result. No traffic forecast follows from publishing it.

Source: [Next.js MDX](https://nextjs.org/docs/app/guides/mdx).
