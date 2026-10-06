> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Security Headers, Canonical URLs y Page Speed

Middleware completo, canonical URLs multi-idioma, streaming con Suspense, estrategias de page speed.

---

## Security Headers (Ranking Signal)

Google premia explícitamente sitios con HSTS configurado. Los demás headers son críticos para evitar penalizaciones por seguridad débil.

```ts
// middleware.ts
import { type NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // HSTS — forzar HTTPS (ranking signal de Google)
  response.headers.set(
    "Strict-Transport-Security",
    "max-age=63072000; includeSubDomains; preload"
  );

  // Prevenir clickjacking
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");

  // Permissions Policy (deshabilitar APIs sensibles por defecto)
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

### Notas sobre cada header

| Header | Función |
|--------|---------|
| `Strict-Transport-Security` | Fuerza HTTPS por 2 años, incluye subdominios, lista de preload |
| `X-Frame-Options: DENY` | Previene que el sitio se cargue en iframes (clickjacking) |
| `X-Content-Type-Options: nosniff` | Evita que el browser intente "adivinar" el MIME type |
| `Referrer-Policy: strict-origin-when-cross-origin` | Limita info enviada en `Referer` cross-origin |
| `Permissions-Policy` | Whitelist de Web APIs disponibles (camera, mic, geo, etc.) |

---

## Canonical URLs

Canonical evita contenido duplicado. Crítico cuando una misma página es accesible por múltiples URLs (con/sin query string, paginación, parámetros de tracking).

```tsx
// app/productos/[slug]/page.tsx
import type { Metadata } from "next";

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://example.com";

  return {
    alternates: {
      canonical: `${baseUrl}/productos/${slug}`,
      // Multi-idioma con hreflang
      languages: {
        "es": `${baseUrl}/es/productos/${slug}`,
        "en": `${baseUrl}/en/productos/${slug}`,
      },
    },
  };
}
```

---

## Page Speed — Estrategias por prioridad

| Estrategia | Impacto | Esfuerzo |
|------------|---------|----------|
| Server Components (RSC) | Alto | Bajo |
| Streaming con Suspense | Alto | Bajo |
| `next/image` con WebP/AVIF | Alto | Bajo |
| Dynamic imports | Medio | Bajo |
| `next/font` con swap | Medio | Bajo |
| Route handlers para API | Medio | Medio |
| Edge Runtime donde aplique | Medio | Medio |
| Bundle analysis + tree shaking | Alto | Medio |
| Redis caching | Alto | Alto |

---

## Streaming con Suspense

Renderizá lo crítico inmediato y streameá lo lento después. El usuario ve algo útil mientras los componentes pesados cargan.

```tsx
// app/dashboard/page.tsx
import { Suspense } from "react";
import { SlowComponent } from "@/components/slow-component";

export default function Dashboard() {
  return (
    <main>
      <h1>Dashboard</h1>
      {/* Contenido crítico — renderiza inmediato */}
      <p>Bienvenido al dashboard</p>

      {/* Contenido lento — se streamea después */}
      <Suspense fallback={<div className="h-64 animate-pulse rounded-lg bg-zinc-200" />}>
        <SlowComponent />
      </Suspense>
    </main>
  );
}
```

El fallback debe tener las mismas dimensiones que el contenido final para evitar CLS.

---

## Verificación de cambios

| Qué | Cómo |
|-----|------|
| Headers en producción | `curl -I https://tudominio.com` |
| Score de seguridad | [securityheaders.com](https://securityheaders.com) |
| Canonical correcto | `view-source:` y buscar `<link rel="canonical">` |
| Multi-idioma | `<link rel="alternate" hreflang="...">` en `<head>` |
| Streaming funcional | DevTools → Network → ver chunks llegando progresivamente |
