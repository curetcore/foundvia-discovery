> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Comparison Pages — Implementación

Patrón completo para `/vs/[competitor]` data-driven y honesto.

---

## Config pattern

```ts
// src/config/comparisons.ts
export interface ComparisonRow {
  feature: string;
  yours: "yes" | "no" | "partial" | string;
  competitor: "yes" | "no" | "partial" | string;
}

export interface ComparisonConfig {
  slug: string;            // "linktree"
  competitor: string;      // "Linktree"
  metaTitle: string;       // "Brand vs Linktree — Comparación 2026"
  description: string;
  heroDescription: string;
  rows: ComparisonRow[];
  differentiators: { value: string; title: string; description: string }[];
  faq: { q: string; a: string }[];
  verdict: string;         // Conclusión honesta
  keywords: string[];
}

export const COMPARISONS: ComparisonConfig[] = [
  {
    slug: "linktree",
    competitor: "Linktree",
    metaTitle: "Brand vs Linktree — Comparación 2026",
    description: "Comparamos Brand y Linktree — features, precios, limitaciones reales. Honesto, sin spin.",
    heroDescription: "Cuál te conviene según tu caso",
    rows: [
      { feature: "Custom domain", yours: "yes", competitor: "yes" },
      { feature: "Analytics gratis", yours: "yes", competitor: "no" },
      { feature: "Custom themes", yours: "yes", competitor: "partial" },
      // ...
    ],
    differentiators: [
      { value: "$0", title: "Plan gratis sin límite de clicks", description: "..." },
    ],
    faq: [
      { q: "¿Puedo migrar de Linktree a Brand?", a: "Sí, en 2 minutos. Importás todos tus links." },
    ],
    verdict: "Linktree gana si querés simplicidad extrema y no te importa la marca de agua. Brand gana si necesitás analytics propias y custom domain gratis.",
    keywords: ["brand vs linktree", "linktree alternativa"],
  },
  // 3-5 competidores
];
```

---

## Estructura de página completa

```
1. Hero (navy/brand bg) — "[Brand] vs [Competitor]" + CTA
2. Tabla comparativa — rows con iconos Check/X/Minus
3. Diferenciadores — 3 cards con métricas clave
4. Veredicto — texto honesto de cuándo elegir cada uno
5. FAQ — accordion con FAQPage schema
6. CTA final — "Probá Brand gratis"
```

---

## JSON-LD pattern

**Importante**: usar `WebPage` + `BreadcrumbList` + `FAQPage`. **NO usar `Product` schema** para comparativas — Google lo interpreta como spam de e-commerce.

```ts
// src/app/vs/[competitor]/page.tsx
const schemas = [
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    name: comparison.metaTitle,
    description: comparison.description,
    url: `${baseUrl}/vs/${comparison.slug}`,
  },
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Brand", item: baseUrl },
      { "@type": "ListItem", position: 2, name: "Comparativas", item: `${baseUrl}/vs` },
      { "@type": "ListItem", position: 3, name: comparison.competitor, item: `${baseUrl}/vs/${comparison.slug}` },
    ],
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: comparison.faq.map((f) => ({
      "@type": "Question",
      name: f.q,
      acceptedAnswer: { "@type": "Answer", text: f.a },
    })),
  },
];
```

---

## Reglas de honestidad

Las comparativas que **mienten** generan más rebotes que conversiones. Reglas:

1. **Reconocer dónde el competidor gana** — si Linktree es más simple, decirlo. Esto genera trust
2. **Datos verificables** — si decís "$0/mes", debe ser cierto. Google detecta inconsistencias y desindexa
3. **No difamar** — comparar funcionalidades, NO atacar al competidor o su equipo
4. **Actualizar precios trimestralmente** — pricing cambia. Una comparativa con precio viejo es fake info

### El "verdict" honesto

Termina con un párrafo donde explicás claramente cuándo elegir cada uno. Ejemplo:

> **Linktree gana** si:
> - Querés la opción más conocida (familiaridad de los usuarios)
> - No te importa pagar $9/mes por features básicas
> - No necesitás custom domain
>
> **Brand gana** si:
> - Querés analytics gratis sin límite
> - Necesitás custom domain en plan gratis
> - Tu marca importa más que la familiaridad

Este patrón sube CTR a 12-18% vs ~5% de comparativas tipo "we beat them on everything".
