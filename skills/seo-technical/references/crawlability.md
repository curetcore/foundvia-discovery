> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Crawlability

`robots.ts`, `sitemap.ts` dinámico, arquitectura del sitio, breadcrumbs con schema.

---

## `robots.ts` (Next.js App Router)

Versión completa con bots tradicionales. Para reglas de AI bots (GPTBot, ClaudeBot, PerplexityBot), usar el skill `seo-ai-geo`.

```ts
// app/robots.ts
import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";

  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/api/", "/admin/", "/_next/", "/private/"],
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
    host: baseUrl,
  };
}
```

---

## `sitemap.ts` (estático + dinámico)

```ts
// app/sitemap.ts
import type { MetadataRoute } from "next";
import { prisma } from "@/lib/prisma";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";

  // Páginas estáticas
  const staticPages: MetadataRoute.Sitemap = [
    { url: baseUrl, lastModified: new Date(), changeFrequency: "weekly", priority: 1 },
    { url: `${baseUrl}/precios`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.8 },
    { url: `${baseUrl}/contacto`, lastModified: new Date(), changeFrequency: "yearly", priority: 0.5 },
  ];

  // Páginas dinámicas desde DB
  const products = await prisma.product.findMany({
    select: { slug: true, updatedAt: true },
    where: { published: true },
  });

  const productPages: MetadataRoute.Sitemap = products.map((p) => ({
    url: `${baseUrl}/productos/${p.slug}`,
    lastModified: p.updatedAt,
    changeFrequency: "weekly" as const,
    priority: 0.7,
  }));

  const posts = await prisma.post.findMany({
    select: { slug: true, updatedAt: true },
    where: { published: true },
  });

  const blogPages: MetadataRoute.Sitemap = posts.map((p) => ({
    url: `${baseUrl}/blog/${p.slug}`,
    lastModified: p.updatedAt,
    changeFrequency: "monthly" as const,
    priority: 0.6,
  }));

  return [...staticPages, ...productPages, ...blogPages];
}
```

> Para sitios con 50+ páginas programáticas y `lastModified` distribuido por slug (anti-batch signal), ver el skill `seo-slug-dates`.

---

## Arquitectura del sitio

### Estructura plana (≤3 clicks)

```
/                                            (Home)
├── /productos/                              (Categoría)
│   ├── /productos/zapatos                   (Subcategoría)
│   │   └── /productos/zapatos/nike-air-max  (Producto)
│   └── /productos/camisas
├── /blog/                                   (Blog index)
│   └── /blog/guia-seo                       (Post)
├── /precios/                                (Pricing)
└── /contacto/                               (Contacto)
```

**Regla**: ninguna página importante a más de 3 clicks del home.

---

## Breadcrumbs con schema

```tsx
// components/breadcrumbs.tsx
import type { BreadcrumbList, WithContext } from "schema-dts";

interface Crumb {
  name: string;
  href: string;
}

export function Breadcrumbs({ items }: { items: Crumb[] }) {
  const jsonLd: WithContext<BreadcrumbList> = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: item.name,
      item: `${process.env.NEXT_PUBLIC_BASE_URL}${item.href}`,
    })),
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <nav aria-label="Breadcrumb" className="text-sm text-zinc-500">
        <ol className="flex items-center gap-2">
          {items.map((item, i) => (
            <li key={item.href} className="flex items-center gap-2">
              {i > 0 && <span>/</span>}
              {i < items.length - 1 ? (
                <a href={item.href} className="hover:text-blue-600">
                  {item.name}
                </a>
              ) : (
                <span aria-current="page">{item.name}</span>
              )}
            </li>
          ))}
        </ol>
      </nav>
    </>
  );
}
```

El schema `BreadcrumbList` aparece en SERPs como ruta de navegación (`Home > Productos > Zapatos > Nike`), mejorando CTR.
