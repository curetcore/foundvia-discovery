# Route-specific Next.js metadata

Inspect the installed version and existing layout/page exports. Use static metadata for stable content, and generateMetadata for data-dependent routes. Do not export both from the same segment. Confirm file-based metadata and inherited title templates before adding overrides.

```ts
import type { Metadata } from "next";

// Example for a real /pricing route; replace content and domain.
export const metadata: Metadata = {
  title: "Pricing",
  description: "Compare the current plans and their limits.",
  alternates: { canonical: "https://example.com/pricing" },
};
```

A root layout may supply metadataBase and defaults; it should not make every route canonical to the homepage. Query-dependent pages need an intentional canonical policy. Check the rendered title, description, canonical, and social metadata on representative child routes.

Use the optional [SEO helper](../../seo-nextjs-implementation/scripts/seo.ts) only after replacing its defaults and reviewing callers. It requires React and Next.js types; the helper tests do not replace an app build.

Source: [Next.js generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata).
