---
name: seo-technical
description: Audita y optimiza el SEO técnico de un proyecto Next.js — Core Web Vitals (LCP/INP/CLS), crawlability (robots.ts, sitemap.ts), security headers, page speed y arquitectura del sitio. Use this skill whenever the user mentions Core Web Vitals, lighthouse scores, slow page loads, INP issues, robots.txt, sitemap, security headers, HSTS, CSP, canonical URLs, mobile usability, or asks for an SEO technical audit — even if they don't explicitly say "SEO".
---

> **Historical module — full review pending.** Follow the [corrected discovery guidance](../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# SEO Técnico

Stack base: Next.js 16 App Router, React 19 RSC, Tailwind v4. Las técnicas aplican a cualquier framework moderno; los snippets son Next.js específicos.

---

## Cuándo invocar este skill

- El usuario pide auditar/optimizar Core Web Vitals (LCP, INP, CLS)
- Lighthouse o PageSpeed Insights muestran scores bajos
- El sitio tiene problemas de crawlability (sitemap, robots, indexación)
- Hay que configurar `robots.ts`, `sitemap.ts`, security headers desde cero
- Se reporta lentitud de carga o jank en interacciones
- El usuario pregunta por mobile usability, HTTPS, redirects o canonical URLs

Para AI bots y `llms.txt`, ver el skill `seo-ai-geo`. Para meta tags, OG, e internal linking, ver `seo-on-page`.

---

## Core Web Vitals 2026

| Métrica | Bueno | Necesita mejora | Malo | Herramienta |
|---------|-------|-----------------|------|-------------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5s – 4.0s | > 4.0s | PageSpeed Insights |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms – 500ms | > 500ms | Chrome UX Report |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 – 0.25 | > 0.25 | Lighthouse |

> **IMPORTANTE**: INP reemplazó a FID en marzo 2024. Nunca referenciar FID — está deprecado.

---

## Reglas clave

1. **Above-the-fold en Server Components** — el contenido crítico se renderiza en servidor (RSC) para LCP rápido. Sin "use client" en hero, headings principales, CTAs above-the-fold.
2. **`priority` obligatorio en hero image** — `next/image` desactiva lazy loading y agrega `<link rel="preload">` automáticamente.
3. **Fuentes con `display: swap` + `adjustFontFallback`** — evita FOIT y reduce CLS de fuentes.
4. **Dimensiones explícitas siempre** — `width` y `height` en imágenes, videos, iframes. Sin excepciones.
5. **`useTransition` para handlers costosos** — operaciones síncronas largas en main thread destruyen INP.
6. **Estructura plana (≤3 clicks)** — ninguna página importante a más de 3 clicks del home.
7. **Security headers son ranking signal** — HSTS, X-Frame-Options, X-Content-Type-Options en producción.

---

## Quick wins por métrica

### LCP rápido (≤2.5s)

```tsx
// app/page.tsx — hero image con priority
import Image from "next/image";

export default function Home() {
  return (
    <Image
      src="/hero.webp"
      alt="Descripción del hero"
      width={1200}
      height={630}
      priority
      sizes="100vw"
    />
  );
}
```

```tsx
// app/layout.tsx — fuentes optimizadas
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  preload: true,
  adjustFontFallback: true,
});
```

Detalles completos (preload de recursos, RSC para above-the-fold, preconnect): [`references/cwv-deep-dive.md`](./references/cwv-deep-dive.md)

### INP rápido (≤200ms)

```tsx
"use client";
import { useTransition } from "react";

export function SearchFilter({ onFilter }: { onFilter: (q: string) => void }) {
  const [isPending, startTransition] = useTransition();
  return (
    <input
      type="search"
      onChange={(e) => {
        startTransition(() => onFilter(e.target.value));
      }}
      aria-busy={isPending}
    />
  );
}
```

Patrones avanzados (dynamic imports, web workers, virtualización): [`references/cwv-deep-dive.md`](./references/cwv-deep-dive.md)

### CLS bajo (≤0.1)

```tsx
// Dimensiones explícitas siempre
<Image src="/photo.webp" alt="..." width={800} height={600} />
<video width={640} height={360} />
<iframe width={560} height={315} />
```

`size-adjust` y skeletons con dimensiones fijas: [`references/cwv-deep-dive.md`](./references/cwv-deep-dive.md)

---

## Crawlability (resumen)

Crear `app/robots.ts` y `app/sitemap.ts` en el App Router. El sitemap debe combinar páginas estáticas + dinámicas desde la base de datos.

```ts
// app/robots.ts — versión mínima
import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";
  return {
    rules: [{
      userAgent: "*",
      allow: "/",
      disallow: ["/api/", "/admin/", "/_next/", "/private/"],
    }],
    sitemap: `${baseUrl}/sitemap.xml`,
    host: baseUrl,
  };
}
```

> Para reglas de AI bots (GPTBot, ClaudeBot, PerplexityBot, etc.), usar el skill `seo-ai-geo`.

`sitemap.ts` con páginas dinámicas + arquitectura de URLs + breadcrumbs con schema: [`references/crawlability.md`](./references/crawlability.md)

---

## Security Headers + Canonical URLs

```ts
// middleware.ts — headers críticos para SEO
import { type NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  response.headers.set(
    "Strict-Transport-Security",
    "max-age=63072000; includeSubDomains; preload"
  );
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");

  return response;
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

Permissions-Policy completo, canonical URLs, multi-idioma, streaming con Suspense, page speed strategies: [`references/security-headers.md`](./references/security-headers.md)

---

## Checklist consolidado

### LCP
- [ ] Hero image con `priority` en `next/image`
- [ ] Fuentes con `display: "swap"` y `adjustFontFallback`
- [ ] Contenido above-the-fold en Server Component (sin `"use client"`)
- [ ] Sin JavaScript bloqueante antes del LCP element
- [ ] Preconnect a orígenes de terceros críticos
- [ ] Imágenes en WebP/AVIF (`next/image` lo hace automático)

### INP
- [ ] Handlers costosos usan `useTransition`
- [ ] Componentes pesados con `dynamic()` import
- [ ] Sin operaciones síncronas largas (>50ms) en main thread
- [ ] Listas largas con virtualización (`react-window` o `tanstack-virtual`)
- [ ] Debounce en inputs de búsqueda (~300ms)

### CLS
- [ ] Imágenes/videos con `width` y `height` explícitos
- [ ] Fuentes con `display: swap` + `size-adjust`
- [ ] Ads/embeds en contenedores con aspect ratio fijo
- [ ] Sin inserción dinámica above-the-fold
- [ ] Skeletons con dimensiones idénticas al contenido final

### Crawl + Security
- [ ] `app/robots.ts` con disallow para `/api/`, `/admin/`, `/_next/`
- [ ] `app/sitemap.ts` combina páginas estáticas y dinámicas
- [ ] HSTS, X-Frame-Options, X-Content-Type-Options en `middleware.ts`
- [ ] Canonical URLs en `generateMetadata` de todas las rutas dinámicas
- [ ] Estructura plana — ninguna URL importante a más de 3 clicks del home

---

## Verificación

| Qué verificar | Herramienta | Frecuencia |
|---------------|-------------|------------|
| Core Web Vitals | PageSpeed Insights, GSC CWV report | Semanal |
| Crawlability | GSC Coverage report | Semanal |
| Sitemap | `curl sitemap.xml`, GSC Sitemaps | Post-deploy |
| Security headers | securityheaders.com | Mensual |
| `robots.txt` | `curl /robots.txt` | Post-deploy |
| Page speed | Lighthouse CI, WebPageTest | Semanal |
| Mobile usability | GSC Mobile Usability | Mensual |

---

## Referencias técnicas profundas

- [`references/cwv-deep-dive.md`](./references/cwv-deep-dive.md) — Optimización detallada de LCP, INP y CLS con ejemplos completos
- [`references/crawlability.md`](./references/crawlability.md) — `robots.ts`, `sitemap.ts` dinámico, arquitectura del sitio, breadcrumbs con schema
- [`references/security-headers.md`](./references/security-headers.md) — Middleware completo, canonical URLs multi-idioma, streaming con Suspense, estrategias de page speed
