> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Tool Pages — Implementación

Estructura completa de `/tools/[slug]` para herramientas gratuitas.

---

## Estructura de archivos

```
src/config/tools.ts                          # Config data-driven
src/app/tools/page.tsx                       # Hub page
src/app/tools/[slug]/
    page.tsx                                 # Server: metadata + JSON-LD
    [ComponentName].tsx                      # Client: "use client", la herramienta
    opengraph-image.tsx                      # OG image dinámico
    [extras].ts                              # Templates, data, etc.
```

---

## Config pattern

```ts
// src/config/tools.ts
export interface ToolConfig {
  slug: string;
  title: string;
  metaTitle: string;
  description: string;
  heroText: string;
  icon: string;            // Nombre del icono Lucide
  category: string;
  keywords: string[];
  faq: { q: string; a: string }[];
  relatedTools: string[];
}

export const TOOLS: ToolConfig[] = [
  {
    slug: "qr-generator",
    title: "Generador de QR",
    metaTitle: "Generador de QR gratis — Brand",
    description: "Generá códigos QR personalizados gratis. Sin login, sin marca de agua.",
    heroText: "Creá tu código QR en 5 segundos",
    icon: "QrCode",
    category: "Utilities",
    keywords: ["generador qr gratis", "crear codigo qr", "qr personalizado"],
    faq: [
      { q: "¿Es gratis?", a: "Sí, 100%. Sin login, sin watermark." },
      // ...
    ],
    relatedTools: ["url-shortener", "barcode-generator"],
  },
  // 4 tools iniciales
];

export function getToolBySlug(slug: string) {
  return TOOLS.find((t) => t.slug === slug);
}

export function getAllToolSlugs() {
  return TOOLS.map((t) => t.slug);
}
```

---

## JSON-LD para tools

```ts
// Incluir en la page.tsx del tool
const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";

const schemas = [
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: tool.title,
    description: tool.description,
    applicationCategory: "UtilityApplication",
    operatingSystem: "Web",
    offers: {
      "@type": "Offer",
      price: "0",
      priceCurrency: "USD",
    },
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: tool.faq.map((f) => ({
      "@type": "Question",
      name: f.q,
      acceptedAnswer: { "@type": "Answer", text: f.a },
    })),
  },
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Brand", item: baseUrl },
      { "@type": "ListItem", position: 2, name: "Herramientas", item: `${baseUrl}/tools` },
      { "@type": "ListItem", position: 3, name: tool.title, item: `${baseUrl}/tools/${tool.slug}` },
    ],
  },
];
```

---

## Página server + client component

```tsx
// src/app/tools/[slug]/page.tsx (Server)
import { getToolBySlug, getAllToolSlugs } from "@/config/tools";
import { QRGeneratorClient } from "./QRGenerator";
import { notFound } from "next/navigation";

export function generateStaticParams() {
  return getAllToolSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const tool = getToolBySlug(slug);
  if (!tool) return {};

  return {
    title: tool.metaTitle,
    description: tool.description,
    keywords: tool.keywords,
  };
}

export default async function ToolPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const tool = getToolBySlug(slug);
  if (!tool) return notFound();

  return (
    <main>
      <h1>{tool.title}</h1>
      <p>{tool.heroText}</p>

      {/* Client component con la lógica interactiva */}
      <QRGeneratorClient />

      {/* FAQ section */}
      <section>
        <h2>Preguntas frecuentes</h2>
        {tool.faq.map((f) => (
          <details key={f.q}>
            <summary>{f.q}</summary>
            <p>{f.a}</p>
          </details>
        ))}
      </section>
    </main>
  );
}
```

```tsx
// src/app/tools/[slug]/QRGenerator.tsx (Client)
"use client";

export function QRGeneratorClient() {
  // Lógica interactiva de la herramienta
  return <div>{/* ... */}</div>;
}
```

---

## CTA al final de cada tool

Después de que el usuario obtiene su resultado, mostrar CTA natural:

> **Tu QR está listo.** ¿Querés trackear cuánta gente lo escanea? **Crea tu cuenta gratis** y conectalo a tu Brand.

Conversión típica: 3-8% de usuarios que llegan al tool crean cuenta. No es spam — el valor entregado primero, el CTA después.
