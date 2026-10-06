> **Historical module — full review pending.** Follow the [corrected discovery guidance](../skills/foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# SEO On-Page

> Cubre meta tags, headings, URLs, imágenes, Open Graph, y linking interno.
> Stack: Next.js 16 App Router, React 19 RSC, Tailwind v4.

---

## Title Tags

### Patrones por tipo de pagina

| Tipo | Patrón | Ejemplo |
|------|--------|---------|
| Home | `Brand - Tagline` | `MiApp - BI para ecommerce LATAM` |
| Producto | `Producto - Categoría \| Brand` | `Nike Air Max - Zapatillas \| TiendaX` |
| Blog | `Titulo del Post \| Brand` | `Guia de SEO 2026 \| MiApp` |
| Categoría | `Categoría - Descripción \| Brand` | `Zapatillas deportivas \| TiendaX` |
| Landing | `Beneficio Principal - Brand` | `Aumenta ventas 3x - MiApp` |
| Pricing | `Precios y Planes \| Brand` | `Precios y Planes \| MiApp` |
| SaaS Feature | `Feature - Que Hace \| Brand` | `Analytics - Métricas en tiempo real \| MiApp` |

### Reglas

- **Max 60 caracteres** (Google trunca a ~580px)
- Keyword principal al inicio
- Brand al final separado con `|` o `-`
- Sin duplicados en todo el sitio
- Sin ALL CAPS ni keyword stuffing

---

## Meta Descriptions

### Patrones por tipo

| Tipo | Patrón |
|------|--------|
| Producto | `Descripción + beneficio + CTA. Precio si aplica.` |
| Blog | `Resumen del valor + gancho. "Aprende como..."` |
| Landing | `Beneficio principal + prueba social + CTA.` |
| Categoría | `Que encontraras + cantidad + diferenciador.` |

### Reglas

- **150-160 caracteres** (Google trunca a ~920px)
- Incluir keyword principal naturalmente
- CTA al final: "Descubre como", "Empieza gratis", "Ver precios"
- Sin comillas dobles (Google las elimina)
- Unica por pagina

---

## Heading Hierarchy

```
H1 - Titulo principal (1 por pagina, UNICO)
  H2 - Secciones principales
    H3 - Subsecciones
      H4 - Detalles (raro, evitar)
```

### Reglas

- **UN solo H1** por pagina
- H1 contiene keyword principal
- H2s son autosuficientes (passage-level ranking)
- No saltar niveles (H1 -> H3 sin H2)
- Descriptivos, no genéricos ("Nuestros servicios" -> "Servicios de análisis para ecommerce")

### Ejemplo estructura de blog post

```
H1: Como optimizar SEO para Next.js en 2026
  H2: Core Web Vitals: las métricas que importan
    H3: LCP - velocidad de carga
    H3: INP - interactividad
    H3: CLS - estabilidad visual
  H2: Structured data con JSON-LD
    H3: Product schema
    H3: FAQ schema
  H2: Optimización para AI search
    H3: llms.txt
    H3: robots.txt para bots de IA
```

---

## generateMetadata Patterns

### Layout-level (template)

```tsx
// app/layout.tsx
import type { Metadata } from "next";

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";

export const metadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: {
    default: "Brand - Tagline",
    template: "%s | Brand", // Páginas hijas heredan: "Titulo | Brand"
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

### Pagina estática

```tsx
// app/precios/page.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Precios y planes", // Se convierte en "Precios y planes | Brand"
  description: "Planes desde $29/mes. Prueba gratis 14 dias sin tarjeta. Cancela cuando quieras.",
  alternates: {
    canonical: "/precios",
  },
};
```

### Pagina dinámica

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
    description: product.description?.slice(0, 160) ?? `Compra ${product.name} al mejor precio.`,
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

---

## URL Structure

### Reglas

| Regla | Bueno | Malo |
|-------|-------|------|
| Lowercase | `/productos/nike-air` | `/Productos/Nike_Air` |
| Hyphens | `/guia-seo-2026` | `/guia_seo_2026` |
| 3-5 palabras | `/blog/optimizar-seo-nextjs` | `/blog/como-optimizar-el-seo-para-nextjs-en-2026-guia-completa` |
| Sin parametros | `/productos/zapatos` | `/productos?cat=zapatos` |
| Sin extensiones | `/contacto` | `/contacto.html` |
| Sin trailing slash | `/precios` | `/precios/` |

### Trailing slash consistency

```ts
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  trailingSlash: false, // Elegir UNO y mantener consistencia
};

export default nextConfig;
```

---

## Image Optimization

### next/image best practices

```tsx
import Image from "next/image";

// Hero (above the fold)
<Image
  src="/hero.webp"
  alt="Descripción precisa del contenido de la imagen"
  width={1200}
  height={630}
  priority
  sizes="100vw"
/>

// Producto (galeria)
<Image
  src={product.image}
  alt={`${product.name} - vista frontal`}
  width={800}
  height={800}
  sizes="(max-width: 768px) 100vw, 50vw"
  className="rounded-lg"
/>

// Thumbnail (lista)
<Image
  src={product.thumbnail}
  alt={product.name}
  width={300}
  height={300}
  sizes="(max-width: 768px) 50vw, 25vw"
/>
```

### Reglas de alt text

| Tipo | Alt text | Ejemplo |
|------|----------|---------|
| Producto | Nombre + variante + contexto | `Nike Air Max 90 blanco, vista lateral` |
| Blog | Descripción del contenido | `Grafico de Core Web Vitals mostrando LCP, INP y CLS` |
| Decorativa | Vacio (no omitir) | `alt=""` |
| Logo | Nombre de la marca | `Logo de MiApp` |
| Persona | Nombre + rol | `Maria Garcia, CEO de Curet LLC` |

---

## Open Graph Images

### next/og ImageResponse

```tsx
// app/og/route.tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get("title") ?? "Brand";
  const description = searchParams.get("description") ?? "";

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
        <div style={{ fontSize: 64, fontWeight: "bold", marginBottom: 20 }}>
          {title}
        </div>
        {description && (
          <div style={{ fontSize: 28, opacity: 0.8 }}>{description}</div>
        )}
        <div
          style={{
            fontSize: 24,
            marginTop: "auto",
            opacity: 0.6,
          }}
        >
          brand.com
        </div>
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
```

### Uso en generateMetadata

```tsx
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const product = await prisma.product.findUnique({ where: { slug } });

  return {
    openGraph: {
      images: [
        {
          url: `/og?title=${encodeURIComponent(product?.name ?? "")}&description=${encodeURIComponent(product?.description?.slice(0, 100) ?? "")}`,
          width: 1200,
          height: 630,
        },
      ],
    },
  };
}
```

### Especificaciones OG

| Plataforma | Tamano | Aspect Ratio |
|------------|--------|--------------|
| Open Graph | 1200x630 | 1.91:1 |
| Twitter Card | 1200x628 | 1.91:1 |
| LinkedIn | 1200x627 | 1.91:1 |

---

## Internal Linking

### Reglas

- **2-5 links internos** por pagina de contenido
- Anchor text descriptivo (NO "click aquí", "leer mas")
- Linking bidireccional entre páginas relacionadas
- Hub pages (pillar) linkan a spoke pages y viceversa
- Footer con links a páginas principales

### Patrón de links relacionados

```tsx
// components/related-links.tsx
interface RelatedLink {
  href: string;
  title: string;
}

export function RelatedLinks({ links }: { links: RelatedLink[] }) {
  return (
    <nav aria-label="Articulos relacionados" className="mt-12 border-t pt-8">
      <h2 className="text-lg font-semibold mb-4">Tambien te puede interesar</h2>
      <ul className="space-y-2">
        {links.map((link) => (
          <li key={link.href}>
            <a href={link.href} className="text-primary hover:underline">
              {link.title}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
```

### Anchor text guidelines

| Bueno | Malo |
|-------|------|
| `guia completa de SEO técnico` | `click aquí` |
| `optimizar Core Web Vitals` | `leer mas` |
| `planes y precios de MiApp` | `ver precios` |

---

## Verificación

| Que verificar | Herramienta | Frecuencia |
|---------------|-------------|------------|
| Title y meta description | Google Rich Results Test | Post-deploy |
| Open Graph | opengraph.xyz, Facebook Debugger | Post-deploy |
| Twitter Card | Twitter Card Validator | Post-deploy |
| Heading hierarchy | Lighthouse accessibility audit | Semanal |
| Broken internal links | GSC Coverage, Screaming Frog | Mensual |
| Image alt text | Lighthouse accessibility | Semanal |
| URL structure | GSC URL Inspection | Post-cambio |
