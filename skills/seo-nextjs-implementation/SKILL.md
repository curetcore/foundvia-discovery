---
name: seo-nextjs-implementation
description: Implementa SEO completo en Next.js con código TypeScript listo para pegar — JSON-LD generators (Organization, Website, Article, FAQ, BreadcrumbList, SoftwareApplication, Product), `generateMetadata` patterns, helpers de canonical URLs y slugs, y componente `<JsonLd>` para structured data. Use this skill whenever the user asks for SEO code, JSON-LD examples, structured data implementation, schema.org markup, rich snippets, generateMetadata patterns, or boilerplate SEO TypeScript — even if they don't say "Next.js".
---

> **Historical module — full review pending.** Follow the [corrected discovery guidance](../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# SEO Implementation (Next.js)

Código TypeScript listo para pegar. Implementa rich snippets, JSON-LD y `generateMetadata` patterns. Stack: Next.js 16 App Router, React 19 RSC, TypeScript estricto.

---

## Cuándo invocar este skill

- El usuario pide código TypeScript de SEO listo para pegar
- Hay que implementar JSON-LD (Organization, Product, FAQ, Article, BreadcrumbList)
- Configurar `generateMetadata` desde cero
- Necesita helpers (canonical URL, truncate description, slug generator)
- Quiere rich snippets en Google (estrella de reviews, precio, FAQ)

Para **estrategia** de SEO técnico (no código), usar `seo-technical`. Para meta tags y on-page (no JSON-LD), usar `seo-on-page`.

---

## Resultado esperado en Google

```
Tu App — Descripción...
miapp.com
⭐⭐⭐⭐⭐ 4.9 (127 reseñas) · desde $0
Descripción de tu producto...
```

Esto requiere `SoftwareApplication` schema con `aggregateRating` + `Offer` válidos. **Solo agregar `aggregateRating` si tenés reviews reales** — Google penaliza fake reviews.

---

## Reglas clave

1. **Configuración env-driven** — `NEXT_PUBLIC_SITE_*` para portabilidad entre proyectos
2. **JSON-LD dentro de `<JsonLd data={...} />`** — wrapper consistente, no `<script>` raw cada vez
3. **Generators reutilizables** — un generator por tipo de schema (`generateOrganizationJsonLd`, etc.)
4. **NUNCA inventar `aggregateRating`** — Google penaliza
5. **TypeScript estricto** — sin `any`, usar `Record<string, unknown>` para JSON-LD opaco

---

## Setup inicial

### 1. Variables de entorno

```bash
# .env.local
NEXT_PUBLIC_SITE_NAME="MiApp"
NEXT_PUBLIC_SITE_URL="https://miapp.com"
NEXT_PUBLIC_SITE_TITLE="MiApp — Tagline"
NEXT_PUBLIC_SITE_DESCRIPTION="150-160 chars description"
NEXT_PUBLIC_TWITTER_HANDLE="@miapp"
NEXT_PUBLIC_CONTACT_EMAIL="hello@miapp.com"
NEXT_PUBLIC_LOCALE="es_DO"
```

### 2. Copiar `seo.ts`

El módulo completo (650+ líneas) está en [`scripts/seo.ts`](./scripts/seo.ts). Copiarlo a `src/lib/seo.ts`.

Incluye:
- `SEO_CONFIG` env-driven
- `generateMetadata()` para Next.js Metadata
- `generateOrganizationJsonLd()`, `generateWebsiteJsonLd()`, `generateArticleJsonLd()`, `generateBlogPostingJsonLd()`, `generateBreadcrumbJsonLd()`, `generateFAQJsonLd()`, `generateSoftwareApplicationJsonLd()`, `generateProductJsonLd()`
- Componente `<JsonLd>` para inyectar schemas
- Helpers: `absoluteUrl`, `truncateDescription`, `generateSlug`, `getCanonicalUrl`

---

## Componente Homepage SEO completo

```tsx
// src/components/seo/homepage-seo.tsx
import { JsonLd, generateFAQJsonLd, generateOrganizationJsonLd, generateWebsiteJsonLd, generateSoftwareApplicationJsonLd, SEO_CONFIG } from "@/lib/seo";

const FAQS = [
  { question: "¿Es gratis empezar?", answer: "Sí, plan gratis sin límite de tiempo." },
  { question: "¿Necesito tarjeta de crédito?", answer: "No para el plan gratis." },
  { question: "¿Puedo cancelar cuando quiera?", answer: "Sí, sin permanencia." },
];

export function HomepageSEO() {
  return (
    <>
      <JsonLd data={generateSoftwareApplicationJsonLd({
        category: "BusinessApplication",
        features: ["Feature 1", "Feature 2", "Feature 3"],
        pricing: {
          lowPrice: "0",
          highPrice: "29",
          priceCurrency: "USD",
          offerCount: 2,
        },
        // SOLO si tenés reviews reales:
        // rating: { ratingValue: "4.9", ratingCount: "127" },
      })} />
      <JsonLd data={generateOrganizationJsonLd({
        sameAs: [
          "https://twitter.com/miapp",
          "https://www.instagram.com/miapp",
        ],
      })} />
      <JsonLd data={generateWebsiteJsonLd()} />
      <JsonLd data={generateFAQJsonLd(FAQS)} />
    </>
  );
}
```

---

## Uso en `src/app/page.tsx`

```tsx
import { HomepageSEO } from "@/components/seo/homepage-seo";
import { generateMetadata as buildMetadata } from "@/lib/seo";

export const metadata = buildMetadata({
  title: "Inicio",
  description: "Descripción específica de la home, 150-160 chars.",
});

export default function HomePage() {
  return (
    <>
      <HomepageSEO />
      {/* Resto de tu página */}
    </>
  );
}
```

---

## JSON-LD por tipo de proyecto

| Tipo de proyecto | Schema principal | Extras |
|------------------|------------------|--------|
| SaaS / App web | `SoftwareApplication` | `Organization`, `FAQPage` |
| E-commerce | `Product`, `ItemList` | `BreadcrumbList`, `AggregateRating` |
| Blog | `Article`, `BlogPosting` | `Person` (autor) |
| Negocio local | `LocalBusiness` | `OpeningHours`, `Address` (ver `seo-local`) |
| Curso / Educación | `Course` | `Instructor`, `Provider` |
| Evento | `Event` | `Location`, `Performer` |

---

## Verificar Rich Snippets

| Herramienta | URL |
|-------------|-----|
| Google Rich Results Test | [search.google.com/test/rich-results](https://search.google.com/test/rich-results) |
| Schema Validator | [validator.schema.org](https://validator.schema.org/) |

---

## Tiempo de indexación

- Google tarda **2-4 semanas** en mostrar rich snippets después de detectar el schema
- Podés acelerar solicitando indexación en Google Search Console
- `aggregateRating` puede tardar hasta 6 semanas en aparecer

---

## Checklist de implementación

- [ ] Crear `.env.local` con `NEXT_PUBLIC_SITE_*` configuradas
- [ ] Copiar [`scripts/seo.ts`](./scripts/seo.ts) a `src/lib/seo.ts`
- [ ] Crear `src/components/seo/homepage-seo.tsx`
- [ ] Editar FAQs reales en homepage-seo
- [ ] Agregar `<HomepageSEO />` en `src/app/page.tsx`
- [ ] Usar `generateMetadata` de `seo.ts` en cada `page.tsx`
- [ ] Agregar `BreadcrumbList` en páginas internas (ver `seo-technical`)
- [ ] Verificar con Rich Results Test post-deploy
- [ ] Solicitar indexación en GSC

---

## Bundled script

- [`scripts/seo.ts`](./scripts/seo.ts) — Módulo completo de SEO utilities (650+ líneas) con todos los generators de JSON-LD, `generateMetadata`, componente `<JsonLd>` y helpers. Listo para pegar en `src/lib/seo.ts`.
