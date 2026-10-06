> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# `generateMetadata` — Patrones completos

Patrones de Next.js App Router para layouts, páginas estáticas y páginas dinámicas con datos de DB.

---

## Layout-level (template global)

Definí defaults globales en el layout root. Todas las páginas heredan a menos que sobrescriban.

```tsx
// app/layout.tsx
import type { Metadata } from "next";

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";

export const metadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: {
    default: "Brand — Tagline",
    template: "%s | Brand", // Páginas hijas: "Título | Brand"
  },
  description: "Descripción global del sitio, 150-160 chars.",
  openGraph: {
    type: "website",
    locale: "es_DO",
    siteName: "Brand",
    images: [{ url: "/og-default.png", width: 1200, height: 630 }],
  },
  twitter: {
    card: "summary_large_image",
    creator: "@handle",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};
```

### Notas

- `metadataBase` es crítico — sin él, los paths relativos en OG images fallan
- `template: "%s | Brand"` aplica solo cuando la página hija pasa un `title` string. Si pasa `title: { absolute: "..." }`, el template se ignora
- `googleBot.max-image-preview: "large"` es lo que permite que Google muestre tu hero en SERPs

---

## Página estática

Páginas que no dependen de datos dinámicos. Export `metadata` const directo.

```tsx
// app/precios/page.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Precios y planes", // Se convierte en "Precios y planes | Brand"
  description: "Planes desde $29/mes. Probá gratis 14 días sin tarjeta. Cancelá cuando quieras.",
  alternates: {
    canonical: "/precios",
  },
};

export default function PricingPage() {
  return <main>{/* ... */}</main>;
}
```

---

## Página dinámica con datos de DB

Cuando el contenido depende de un slug, ID o param. Usar `generateMetadata` async.

```tsx
// app/productos/[slug]/page.tsx
import type { Metadata } from "next";
import { prisma } from "@/lib/prisma";
import { notFound } from "next/navigation";

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const product = await prisma.product.findUnique({
    where: { slug },
    select: { name: true, description: true, images: true, price: true },
  });

  if (!product) return notFound();

  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";

  return {
    title: product.name,
    description:
      product.description?.slice(0, 160) ??
      `Comprá ${product.name} al mejor precio.`,
    alternates: {
      canonical: `${baseUrl}/productos/${slug}`,
    },
    openGraph: {
      title: product.name,
      description: product.description?.slice(0, 160) ?? "",
      type: "website",
      images: product.images?.[0]
        ? [{ url: product.images[0] as string, width: 1200, height: 630 }]
        : [],
    },
  };
}

export default async function ProductPage({ params }: Props) {
  const { slug } = await params;
  const product = await prisma.product.findUnique({ where: { slug } });
  if (!product) return notFound();

  return (
    <main>
      <h1>{product.name}</h1>
      {/* ... */}
    </main>
  );
}
```

### Notas sobre páginas dinámicas

- **`generateMetadata` corre en el servidor** — podés hacer queries de DB acá
- Next.js cachea automáticamente la query si la repetís en el componente — no hay doble fetch
- Si el dato viene de una API externa lenta, considerá llamar la query una sola vez con `React.cache()` y usarla en ambos lugares
- Devolver `notFound()` desde `generateMetadata` lanza el 404 antes de renderizar la página — UX mejor
