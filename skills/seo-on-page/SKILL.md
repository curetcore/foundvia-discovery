---
name: seo-on-page
description: Optimiza meta tags, headings, URLs, imágenes, Open Graph y internal linking para SEO on-page en Next.js. Use this skill whenever the user mentions title tags, meta descriptions, generateMetadata, Open Graph, Twitter Cards, OG images, heading hierarchy (H1/H2/H3), URL structure, alt text, anchor text, canonical tags, or social sharing previews — even if they don't explicitly say "SEO on-page".
---

> **Historical module — full review pending.** Follow the [corrected discovery guidance](../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# SEO On-Page

Cubre meta tags, headings, URLs, imágenes, Open Graph y linking interno. Stack: Next.js 16 App Router, React 19 RSC.

---

## Cuándo invocar este skill

- El usuario pide optimizar `<title>` y meta descriptions
- Hay que escribir `generateMetadata` para una ruta nueva
- Se está configurando Open Graph / Twitter Cards / OG images
- Se reportan thumbnails feos al compartir links en redes sociales
- El usuario pregunta por estructura de headings (H1/H2/H3)
- Hay dudas sobre URL slugs, anchor text, o internal linking
- Hay que escribir alt text para imágenes

Para Core Web Vitals, sitemap y security headers, usar el skill `seo-technical`. Para JSON-LD (FAQ, Product, Organization), usar `seo-nextjs-implementation`.

---

## Title Tags

### Patrones por tipo de página

| Tipo | Patrón | Ejemplo |
|------|--------|---------|
| Home | `Brand — Tagline` | `MiApp — BI para ecommerce LATAM` |
| Producto | `Producto — Categoría \| Brand` | `Nike Air Max — Zapatillas \| TiendaX` |
| Blog | `Título del Post \| Brand` | `Guía de SEO 2026 \| MiApp` |
| Categoría | `Categoría — Descripción \| Brand` | `Zapatillas deportivas \| TiendaX` |
| Landing | `Beneficio Principal — Brand` | `Aumenta ventas 3x — MiApp` |
| Pricing | `Precios y Planes \| Brand` | `Precios y Planes \| MiApp` |
| Feature SaaS | `Feature — Qué hace \| Brand` | `Analytics — Métricas en tiempo real \| MiApp` |

### Reglas

- **Máx 60 caracteres** (Google trunca a ~580px)
- Keyword principal al inicio
- Brand al final separado con `|` o `—`
- Sin duplicados en todo el sitio
- Sin ALL CAPS ni keyword stuffing

---

## Meta Descriptions

### Patrones por tipo

| Tipo | Patrón |
|------|--------|
| Producto | `Descripción + beneficio + CTA. Precio si aplica.` |
| Blog | `Resumen del valor + gancho. "Aprendé cómo..."` |
| Landing | `Beneficio principal + prueba social + CTA.` |
| Categoría | `Qué encontrarás + cantidad + diferenciador.` |

### Reglas

- **150-160 caracteres** (Google trunca a ~920px)
- Incluir keyword principal naturalmente
- CTA al final: "Descubre cómo", "Empezá gratis", "Ver precios"
- Sin comillas dobles (Google las elimina)
- Única por página

---

## Heading Hierarchy

```
H1 — Título principal (1 por página, ÚNICO)
  H2 — Secciones principales
    H3 — Subsecciones
      H4 — Detalles (raro, evitar)
```

### Reglas

- **UN solo H1** por página
- H1 contiene la keyword principal
- H2s son autosuficientes (passage-level ranking — cada H2 puede aparecer como resultado independiente en Google)
- No saltar niveles (H1 → H3 sin H2)
- Descriptivos, no genéricos. ❌ "Nuestros servicios" → ✅ "Servicios de análisis para ecommerce"

### Ejemplo de estructura de blog post

```
H1: Cómo optimizar SEO para Next.js en 2026
  H2: Core Web Vitals — las métricas que importan
    H3: LCP — velocidad de carga
    H3: INP — interactividad
    H3: CLS — estabilidad visual
  H2: Structured data con JSON-LD
    H3: Product schema
    H3: FAQ schema
  H2: Optimización para AI search
    H3: llms.txt
    H3: robots.txt para bots de IA
```

---

## `generateMetadata` (Next.js App Router)

### Layout-level (template)

```tsx
// app/layout.tsx
import type { Metadata } from "next";

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";

export const metadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: {
    default: "Brand — Tagline",
    template: "%s | Brand", // Páginas hijas heredan: "Título | Brand"
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

Patrones para páginas estáticas y dinámicas (con datos de DB): [`references/generate-metadata.md`](./references/generate-metadata.md)

---

## URL Structure

### Reglas

| Regla | Bueno | Malo |
|-------|-------|------|
| Lowercase | `/productos/nike-air` | `/Productos/Nike_Air` |
| Hyphens | `/guia-seo-2026` | `/guia_seo_2026` |
| 3-5 palabras | `/blog/optimizar-seo-nextjs` | `/blog/como-optimizar-el-seo-para-nextjs-en-2026-guia-completa` |
| Sin parámetros | `/productos/zapatos` | `/productos?cat=zapatos` |
| Sin extensiones | `/contacto` | `/contacto.html` |
| Sin trailing slash | `/precios` | `/precios/` |

### Trailing slash consistency

```ts
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  trailingSlash: false, // Elegí UNO y mantené consistencia
};

export default nextConfig;
```

---

## Image Optimization (next/image)

```tsx
import Image from "next/image";

// Hero (above the fold) — priority obligatorio
<Image src="/hero.webp" alt="..." width={1200} height={630} priority sizes="100vw" />

// Galería de producto — sizes responsive
<Image src={product.image} alt={`${product.name} — vista frontal`}
       width={800} height={800} sizes="(max-width: 768px) 100vw, 50vw" />

// Thumbnail
<Image src={product.thumbnail} alt={product.name}
       width={300} height={300} sizes="(max-width: 768px) 50vw, 25vw" />
```

### Reglas de alt text

| Tipo | Alt text | Ejemplo |
|------|----------|---------|
| Producto | Nombre + variante + contexto | `Nike Air Max 90 blanco, vista lateral` |
| Blog | Descripción del contenido | `Gráfico de Core Web Vitals mostrando LCP, INP y CLS` |
| Decorativa | Vacío (no omitir el atributo) | `alt=""` |
| Logo | Nombre de la marca | `Logo de MiApp` |
| Persona | Nombre + rol | `María García, CEO de Curet LLC` |

---

## Open Graph + Twitter Cards

OG y Twitter Cards controlan cómo se ve tu sitio cuando alguien comparte un link en redes. **Sin OG = thumbnail genérico, ~50% menos CTR en redes sociales.**

### Specs por plataforma

| Plataforma | Tamaño | Aspect Ratio |
|------------|--------|--------------|
| Open Graph (Facebook, LinkedIn) | 1200x630 | 1.91:1 |
| Twitter Card | 1200x628 | 1.91:1 |
| LinkedIn | 1200x627 | 1.91:1 |

### OG image dinámico con `next/og`

```tsx
// app/og/route.tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get("title") ?? "Brand";

  return new ImageResponse(
    (
      <div style={{ /* ... */ }}>
        {title}
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
```

Implementación completa de OG dinámico (con descripciones, gradientes, fonts custom) y uso en `generateMetadata`: [`references/og-images.md`](./references/og-images.md)

---

## Internal Linking

### Reglas

- **2-5 links internos** por página de contenido
- Anchor text descriptivo (NUNCA "click acá", "leer más")
- Linking bidireccional entre páginas relacionadas
- Hub pages (pillar) linkean a spoke pages y viceversa
- Footer con links a páginas principales

### Anchor text — bueno vs malo

| Bueno | Malo |
|-------|------|
| `guía completa de SEO técnico` | `click acá` |
| `optimizar Core Web Vitals` | `leer más` |
| `planes y precios de MiApp` | `ver precios` |

Componente `RelatedLinks` y patrón de links relacionados: [`references/internal-linking.md`](./references/internal-linking.md)

---

## Verificación

| Qué verificar | Herramienta | Frecuencia |
|---------------|-------------|------------|
| Title y meta description | Google Rich Results Test | Post-deploy |
| Open Graph | [opengraph.xyz](https://opengraph.xyz), Facebook Debugger | Post-deploy |
| Twitter Card | Twitter Card Validator | Post-deploy |
| Heading hierarchy | Lighthouse accessibility audit | Semanal |
| Broken internal links | GSC Coverage, Screaming Frog | Mensual |
| Image alt text | Lighthouse accessibility | Semanal |
| URL structure | GSC URL Inspection | Post-cambio |

---

## Referencias técnicas profundas

- [`references/generate-metadata.md`](./references/generate-metadata.md) — Patrones completos de `generateMetadata` para layouts, páginas estáticas y páginas dinámicas con datos de DB
- [`references/og-images.md`](./references/og-images.md) — `next/og` `ImageResponse` completo, gradientes, fonts custom, integración con `generateMetadata`
- [`references/internal-linking.md`](./references/internal-linking.md) — Componente `RelatedLinks`, hub-and-spoke linking, footer patterns
