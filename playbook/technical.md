> **Historical module — full review pending.** Follow the [corrected discovery guidance](../skills/foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# SEO Técnico

> Cubre Core Web Vitals, crawlability, page speed, seguridad, y arquitectura del sitio.
> Stack: Next.js 16 App Router, React 19 RSC, Tailwind v4.

---

## Core Web Vitals 2026

| Métrica | Bueno | Necesita mejora | Malo | Herramienta |
|---------|-------|-----------------|------|-------------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5s - 4.0s | > 4.0s | PageSpeed Insights |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms | Chrome UX Report |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 | Lighthouse |

> **IMPORTANTE**: INP reemplazó a FID en marzo 2024. NUNCA referenciar FID.

---

## Optimización LCP

LCP mide el tiempo que tarda el elemento mas grande visible en renderizar. Causas principales de LCP lento:

### 1. Imágenes hero sin prioridad

```tsx
// app/page.tsx
import Image from "next/image";

export default function Home() {
  return (
    <Image
      src="/hero.webp"
      alt="Descripción del hero"
      width={1200}
      height={630}
      priority // Desactiva lazy loading, agrega preload
      sizes="100vw"
    />
  );
}
```

### 2. Fuentes que bloquean render

```tsx
// app/layout.tsx
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  display: "swap", // Muestra fallback mientras carga
  preload: true,
  adjustFontFallback: true, // Reduce CLS de fuentes
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

### 3. Server Components para contenido critico

```tsx
// app/products/[slug]/page.tsx (Server Component por defecto)
import { prisma } from "@/lib/prisma";

// Contenido critico se renderiza en el servidor = LCP rápido
export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const product = await prisma.product.findUnique({ where: { slug } });

  return (
    <main>
      <h1>{product?.name}</h1>
      {/* Contenido above-the-fold renderizado en servidor */}
    </main>
  );
}
```

### 4. Preload de recursos criticos

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <head>
        <link rel="preload" href="/hero.webp" as="image" type="image/webp" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://cdn.example.com" />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### Checklist LCP

- [ ] Hero image con `priority` en next/image
- [ ] Fuentes con `display: "swap"` y `adjustFontFallback`
- [ ] Contenido above-the-fold en Server Component
- [ ] Sin JavaScript bloqueante antes del LCP element
- [ ] Preconnect a orígenes de terceros criticos
- [ ] Imágenes en WebP/AVIF (next/image lo hace automático)

---

## Optimización INP

INP mide la latencia de la interacción mas lenta del usuario. Aplica a clicks, taps, y keyboard input.

### 1. useTransition para operaciones pesadas

```tsx
"use client";
import { useTransition } from "react";

export function SearchFilter({ onFilter }: { onFilter: (q: string) => void }) {
  const [isPending, startTransition] = useTransition();

  return (
    <input
      type="search"
      onChange={(e) => {
        startTransition(() => {
          onFilter(e.target.value); // No bloquea el input
        });
      }}
      aria-busy={isPending}
    />
  );
}
```

### 2. Dynamic imports para componentes pesados

```tsx
import dynamic from "next/dynamic";

// Solo carga cuando se necesita
const HeavyChart = dynamic(() => import("@/components/chart"), {
  loading: () => <div className="h-64 animate-pulse bg-zinc-200 rounded-lg" />,
  ssr: false, // No renderizar en servidor si es interactivo
});
```

### 3. Web Workers para calculo pesado

```tsx
"use client";
import { useCallback } from "react";

export function DataProcessor() {
  const processData = useCallback((data: unknown[]) => {
    const worker = new Worker(new URL("../workers/process.ts", import.meta.url));
    worker.postMessage(data);
    worker.onmessage = (e) => {
      // Resultado sin bloquear main thread
      console.log(e.data);
      worker.terminate();
    };
  }, []);

  return <button onClick={() => processData([])}>Procesar</button>;
}
```

### Checklist INP

- [ ] Handlers de eventos usan `useTransition` para operaciones costosas
- [ ] Componentes pesados con `dynamic()` import
- [ ] Sin operaciones sincronas largas (> 50ms) en main thread
- [ ] Listas largas usan virtualización (react-window / tanstack-virtual)
- [ ] Debounce en inputs de búsqueda (300ms)

---

## Optimización CLS

CLS mide cambios inesperados en el layout. Causas principales:

### 1. Dimensiones explícitas en imágenes y videos

```tsx
// SIEMPRE especificar width y height
<Image src="/photo.webp" alt="..." width={800} height={600} />

// Para videos
<video width={640} height={360} />

// Para iframes (embeds)
<iframe width={560} height={315} />
```

### 2. Font size-adjust para fallback

```css
/* globals.css - Tailwind v4 */
@theme {
  --font-sans: "Inter", system-ui, sans-serif;
}

/* Si usas @font-face manual */
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter.woff2") format("woff2");
  font-display: swap;
  size-adjust: 107%; /* Ajustar al fallback para evitar CLS */
}
```

### 3. Skeletons con dimensiones fijas

```tsx
// Skeleton que ocupa el mismo espacio que el contenido final
function ProductCardSkeleton() {
  return (
    <div className="w-full h-80 animate-pulse rounded-lg bg-zinc-200" />
  );
}
```

### Checklist CLS

- [ ] Todas las imágenes/videos tienen width y height explícitos
- [ ] Fuentes usan `display: swap` con `size-adjust`
- [ ] Ads/embeds tienen contenedores con aspect ratio fijo
- [ ] Sin inserción dinámica de contenido above-the-fold
- [ ] Skeletons con las mismas dimensiones que el contenido final

---

## Arquitectura del sitio

### Estructura plana (2-3 clicks)

```
/                          (Home)
├── /productos/            (Categoría)
│   ├── /productos/zapatos (Subcategoria)
│   │   └── /productos/zapatos/nike-air-max (Producto)
│   └── /productos/camisas
├── /blog/                 (Blog index)
│   └── /blog/guia-seo     (Post)
├── /precios/              (Pricing)
└── /contacto/             (Contacto)
```

**Regla**: Ninguna pagina importante a mas de 3 clicks del home.

### Breadcrumbs con schema

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
                <a href={item.href} className="hover:text-primary">
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

---

## Crawlability

### robots.ts (Next.js App Router)

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
      // Bots de IA que generan tráfico (permitir)
      {
        userAgent: ["GPTBot", "OAI-SearchBot", "ChatGPT-User"],
        allow: "/",
        disallow: ["/api/", "/admin/"],
      },
      {
        userAgent: ["ClaudeBot", "PerplexityBot", "Applebot-Extended"],
        allow: "/",
        disallow: ["/api/", "/admin/"],
      },
      // Bots de scraping/training (bloquear)
      {
        userAgent: ["CCBot", "Google-Extended", "FacebookBot"],
        disallow: "/",
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
    host: baseUrl,
  };
}
```

### sitemap.ts (estático + dinámico)

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

---

## Page Speed

### Estrategias por prioridad

| Estrategia | Impacto | Esfuerzo |
|------------|---------|----------|
| Server Components (RSC) | Alto | Bajo |
| Streaming con Suspense | Alto | Bajo |
| next/image con WebP/AVIF | Alto | Bajo |
| Dynamic imports | Medio | Bajo |
| next/font con swap | Medio | Bajo |
| Route handlers para API | Medio | Medio |
| Edge Runtime donde aplique | Medio | Medio |
| Bundle analysis + tree shaking | Alto | Medio |
| Redis caching | Alto | Alto |

### Streaming con Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from "react";
import { SlowComponent } from "@/components/slow-component";

export default function Dashboard() {
  return (
    <main>
      <h1>Dashboard</h1>
      {/* Contenido critico renderiza inmediato */}
      <p>Bienvenido al dashboard</p>

      {/* Contenido lento se streamea despues */}
      <Suspense fallback={<div className="h-64 animate-pulse bg-zinc-200 rounded-lg" />}>
        <SlowComponent />
      </Suspense>
    </main>
  );
}
```

---

## Security Headers (Ranking Signal)

```ts
// middleware.ts
import { type NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // HSTS - Forzar HTTPS (ranking signal de Google)
  response.headers.set(
    "Strict-Transport-Security",
    "max-age=63072000; includeSubDomains; preload"
  );

  // Prevenir clickjacking
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");

  // Permissions Policy
  response.headers.set(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=(self)"
  );

  return response;
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

---

## Canonical URLs

```tsx
// app/productos/[slug]/page.tsx
import type { Metadata } from "next";

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";

  return {
    alternates: {
      canonical: `${baseUrl}/productos/${slug}`,
      // Para sitios multi-idioma
      languages: {
        "es": `${baseUrl}/es/productos/${slug}`,
        "en": `${baseUrl}/en/productos/${slug}`,
      },
    },
  };
}
```

---

## Verificación

| Que verificar | Herramienta | Frecuencia |
|---------------|-------------|------------|
| Core Web Vitals | PageSpeed Insights, GSC CWV report | Semanal |
| Crawlability | GSC Coverage report | Semanal |
| Sitemap | `curl sitemap.xml`, GSC Sitemaps | Post-deploy |
| Security headers | securityheaders.com | Mensual |
| robots.txt | `curl /robots.txt` | Post-deploy |
| Page speed | Lighthouse CI, WebPageTest | Semanal |
| Mobile usability | GSC Mobile Usability | Mensual |
