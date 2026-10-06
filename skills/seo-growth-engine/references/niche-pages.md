> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Niche Landing Pages — Implementación

Patrón completo para `/para/[nicho]` data-driven en Next.js App Router.

---

## Config data-driven

```ts
// src/config/niches.ts
export interface NicheConfig {
  slug: string;            // URL: /para/musicos
  title: string;           // "Músicos"
  metaTitle: string;       // "Link in bio para músicos — Brand 2026"
  description: string;     // Meta description (150-160 chars)
  heroText: string;        // Texto del hero
  features: Array<{ title: string; description: string }>;
  faq: Array<{ q: string; a: string }>;
  keywords: string[];      // Para meta keywords
  relatedNiches: string[]; // Slugs de nichos relacionados
}

export const NICHES: NicheConfig[] = [
  { slug: "musicos", title: "Músicos", /* ... */ },
  { slug: "restaurantes", title: "Restaurantes", /* ... */ },
  // 15-20 nichos
];

export function getNicheBySlug(slug: string) {
  return NICHES.find((n) => n.slug === slug);
}

export function getAllNicheSlugs() {
  return NICHES.map((n) => n.slug);
}
```

---

## Página dinámica

```tsx
// src/app/para/[nicho]/page.tsx
import { getNicheBySlug, getAllNicheSlugs } from "@/config/niches";

export function generateStaticParams() {
  return getAllNicheSlugs().map((nicho) => ({ nicho }));
}

export async function generateMetadata({ params }: { params: Promise<{ nicho: string }> }) {
  const { nicho } = await params;
  const config = getNicheBySlug(nicho);
  if (!config) return {};

  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";
  const url = `${baseUrl}/para/${nicho}`;

  return {
    title: config.metaTitle,
    description: config.description,
    keywords: config.keywords,
    alternates: { canonical: url },
    openGraph: {
      title: config.metaTitle,
      description: config.description,
      url,
    },
  };
}

export default async function Page({ params }: { params: Promise<{ nicho: string }> }) {
  const { nicho } = await params;
  const config = getNicheBySlug(nicho);
  if (!config) return notFound();

  return (
    <main>
      <h1>{config.title}</h1>
      {/* Hero, features, FAQ, related niches */}
    </main>
  );
}
```

---

## Hub page (`/para`)

Grid de cards con todos los nichos. JSON-LD: `CollectionPage` + `ItemList`.

```tsx
// src/app/para/page.tsx
import { NICHES } from "@/config/niches";
import type { CollectionPage, ItemList, WithContext } from "schema-dts";

export default function NichesHubPage() {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";

  const jsonLd: WithContext<CollectionPage> = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: "Soluciones por nicho",
    url: `${baseUrl}/para`,
    mainEntity: {
      "@type": "ItemList",
      itemListElement: NICHES.map((niche, i) => ({
        "@type": "ListItem" as const,
        position: i + 1,
        url: `${baseUrl}/para/${niche.slug}`,
        name: niche.title,
      })),
    },
  };

  return (
    <main>
      <script type="application/ld+json"
              dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <h1>Brand para cada profesión</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {NICHES.map((niche) => (
          <a key={niche.slug} href={`/para/${niche.slug}`}>
            {/* Card */}
          </a>
        ))}
      </div>
    </main>
  );
}
```

---

## OG Image dinámico por nicho

```tsx
// src/app/para/[nicho]/opengraph-image.tsx
import { ImageResponse } from "next/og";
import { getNicheBySlug } from "@/config/niches";

export const runtime = "edge";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image({ params }: { params: { nicho: string } }) {
  const config = getNicheBySlug(params.nicho);

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          padding: "60px",
          background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
          color: "white",
        }}
      >
        <div style={{ fontSize: 48, opacity: 0.7 }}>Brand para</div>
        <div style={{ fontSize: 96, fontWeight: "bold" }}>
          {config?.title}
        </div>
      </div>
    ),
    { ...size }
  );
}
```

---

## Sin trampa de "templates duplicados"

Cada nicho debe tener contenido **realmente único** en `heroText`, `features`, `faq`. Si todos los nichos usan literalmente el mismo texto cambiando solo el título, Google detecta thin content y desindexa.

Mínimo de variación por nicho:
- Hero text con keyword del nicho integrada naturalmente
- 4-6 features con ejemplos específicos del vertical
- 3-5 FAQ con preguntas reales del nicho
