---
name: seo-growth-engine
description: Diseña e implementa un Growth Engine completo para SaaS — niche landing pages (`/para/[nicho]`), micro-tools gratuitas (`/tools/[slug]`), comparativas data-driven (`/vs/[competitor]`), blog MDX a escala, AEO con llms.txt, y outreach a directorios. Use this skill whenever the user mentions programmatic SEO, niche pages, tools landing pages, comparison pages, alternative pages, blog at scale, MDX blog, Product Hunt, directory submissions, backlinks strategy, or asks how to scale organic traffic from zero — even if they don't say "growth engine".
---

> **Historical module — full review pending.** Follow the [corrected discovery guidance](../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Growth Engine

Sistema completo de páginas interconectadas para generar tráfico orgánico sin ads. Probado en Linkship: 60+ páginas indexables, 50+ keywords target, red densa de internal linking. Stack: Next.js 16 App Router, MDX, Tailwind v4.

---

## Cuándo invocar este skill

- El usuario tiene un SaaS y quiere tráfico orgánico desde cero
- Pregunta sobre programmatic SEO o páginas data-driven
- Quiere crear niche pages (`/para/musicos`), tools (`/tools/qr-generator`), comparativas (`/vs/linktree`)
- Plan de blog content a escala (20+ artículos en bloque)
- Outreach a directorios (Product Hunt, G2, Capterra)
- Tiene producto pero no estrategia de distribución

Para SEO técnico (CWV, sitemap), usar `seo-technical`. Para `llms.txt` y AI bots, usar `seo-ai-geo`. Para fechas distribuidas en sitios con 50+ páginas programáticas, usar `seo-slug-dates`.

---

## Concepto

Un Growth Engine es un sistema de páginas interconectadas que genera tráfico orgánico sin depender de ads. Se compone de **6 pilares**:

```
                    [Homepage]
                   /    |    \
        [Nichos]  [Tools]  [Comparativas]
            \       |        /
             \      |       /
              [Blog x20+]
                    |
              [llms.txt / AEO]
                    |
                [Outreach]
```

Cada pilar atrae tráfico por keywords distintas y cross-linkea a los demás, creando un efecto multiplicador.

---

## Reglas clave

1. **Data-driven primero** — cada pilar empieza con un `config.ts` con la data, NO con páginas hardcoded
2. **Internal linking denso** — cada página linkea a 2-5 páginas relacionadas. Sin esto, los pilares quedan isla
3. **OG image dinámico por página** — cada URL tiene su propia preview en redes
4. **Fechas distribuidas por slug** (anti-batch signal) — usar el skill `seo-slug-dates` cuando haya 50+ páginas programáticas
5. **Honestidad en comparativas** — reconocer dónde el competidor gana. Genera confianza
6. **Outreach es serial, no paralelo** — 5 submissions/día, empezando por Tier 1

---

## Pilar 1: Niche Landing Pages (`/para/[nicho]`)

Páginas específicas para cada tipo de usuario/profesión. Capturan keywords long-tail tipo "link in bio para músicos" o "analytics para restaurantes".

### Patrón básico

```ts
// src/config/niches.ts
export interface NicheConfig {
  slug: string;          // "musicos"
  title: string;         // "Músicos"
  metaTitle: string;     // "Link in bio para músicos — Brand 2026"
  description: string;   // 150-160 chars
  heroText: string;
  features: { title: string; description: string }[];
  faq: { q: string; a: string }[];
  keywords: string[];
  relatedNiches: string[];
}

export const NICHES: NicheConfig[] = [
  { slug: "musicos", title: "Músicos", /* ... */ },
  { slug: "restaurantes", title: "Restaurantes", /* ... */ },
  // 15-20 nichos
];
```

### Cantidad recomendada

- **15-20 nichos** iniciales
- Agregar 5 nuevos cada trimestre basado en GSC queries

Implementación completa de páginas dinámicas, hub page (`/para`), y OG image dinámico: [`references/niche-pages.md`](./references/niche-pages.md)

---

## Pilar 2: Micro-tools gratuitas (`/tools/[slug]`)

Herramientas 100% client-side (sin backend) que resuelven un problema específico. Atraen tráfico informacional y generan leads via CTA.

### Principios

1. **Zero backend** — todo client-side, sin API keys, sin login
2. **Valor inmediato** — el usuario obtiene resultado en <5 segundos
3. **CTA natural** — "Tu [resultado] está listo. Ahora creá tu cuenta gratis"
4. **SEO-first** — JSON-LD `SoftwareApplication` + `FAQPage` + `BreadcrumbList`

### Ideas universales para SaaS

| Tool | Complejidad | Keywords target |
|------|-------------|-----------------|
| Contador de caracteres | Baja | "contador caracteres instagram" |
| Generador de bio | Media | "generador bio instagram" |
| Verificador de username | Media | "username checker" |
| Generador de QR | Media | "generador qr gratis" |
| Comparador de [X] | Alta | "[producto] vs [competidor]" |

### Cantidad recomendada

- **4 tools iniciales** (día 1)
- 1-2 nuevas por mes basado en keyword opportunities

Estructura de archivos completa, `config/tools.ts` pattern, JSON-LD para tools: [`references/tool-pages.md`](./references/tool-pages.md)

---

## Pilar 3: Comparativas (`/vs/[competitor]`)

Páginas que comparan tu producto con competidores. Capturan keywords de alta intención: "[tu marca] vs [competidor]", "[competidor] alternative".

### Estructura de página

```
1. Hero — "[Brand] vs [Competitor]" + CTA
2. Tabla comparativa — rows con iconos Check/X/Minus
3. Diferenciadores — 3 cards con métricas clave
4. Veredicto — texto honesto de cuándo elegir cada uno
5. FAQ — accordion con FAQPage schema
6. CTA final — "Probá Brand gratis"
```

### Reglas de contenido

- **Ser honesto** — reconocer dónde el competidor gana
- **Datos verificables** — precios, features, limitaciones reales
- **No difamar** — comparar funcionalidades, no atacar
- **Actualizar precios** — verificar cada trimestre

### Cantidad recomendada

- **3-5 competidores** principales
- Agregar cuando surjan nuevos competidores relevantes

Config pattern + JSON-LD (WebPage + BreadcrumbList + FAQPage, NO Product schema): [`references/comparison-pages.md`](./references/comparison-pages.md)

---

## Pilar 4: Blog MDX a escala

### 4 categorías de artículos

| Categoría | Cantidad | Keywords | Ejemplo |
|-----------|----------|----------|---------|
| Guías de herramientas | 1 por tool | "[tool name] gratis" | "Generador de bio para Instagram" |
| Comparativas | 1 por competidor | "[brand] vs [comp]" | "Linkship vs Beacons" |
| Guías por nicho | 1 por nicho | "[producto] para [nicho]" | "Link in bio para músicos" |
| How-to / Tips | Evergreen | "cómo [acción]", "mejores [X]" | "Cómo aumentar clicks en tu bio" |

### Reglas

1. **800-1200 palabras** por artículo (ni corto ni relleno)
2. **Pirámide invertida** — respuesta directa en primer párrafo (BLUF)
3. **Internal linking obligatorio** — cada artículo enlaza a 2-3 páginas internas
4. **Fechas escalonadas** — 2-3 días entre artículos (no parecer spam)
5. **CTAs naturales** — 1 CTA en medio + 1 al final

### Cantidad recomendada

- **20 artículos iniciales** (4 batches de 5)
- 4-8 nuevos por mes

Frontmatter standard, internal linking matrix, MDX setup: [`references/blog-mdx.md`](./references/blog-mdx.md)

---

## Pilar 5: AEO (Answer Engine Optimization)

`llms.txt` con secciones específicas para Growth Engine + templates de respuesta para LLMs. Para implementación técnica de `llms.txt`, usar el skill `seo-ai-geo`.

### Estructura recomendada de `llms.txt` para Growth Engine

```
# [Brand]
> Descripción en 1-2 oraciones.

## Información clave
## Planes y precios
## Funcionalidades
## Para creadores / Soluciones por nicho
## Herramientas gratuitas
## Comparativas
## Blog
## Links importantes
## Más información → /llms-full.txt
```

### Templates de respuesta para LLMs en `llms-full.txt`

Cubrir mínimo:
- "¿Cuál es la mejor alternativa a [competidor principal]?"
- "¿Qué herramienta de [categoría] es gratis?"
- "¿Cómo [acción que tu tool resuelve]?"
- "[Tu marca] vs [competidor], ¿cuál es mejor?"
- "¿Cuál es el [producto de tu categoría] más barato?"

---

## Pilar 6: Outreach y backlinks

### Directorios por tier

| Tier | DA | Ejemplos | Prioridad |
|------|-----|---------|-----------|
| 1 | 80+ | Product Hunt, G2, Capterra, AlternativeTo, SaaSHub, BetaList, Indie Hackers | Alta |
| 2 | 50-79 | MicroLaunch, DevHunt, Launching Next, Toolify.ai, Futurepedia | Media |
| 3 | Variable | StartupStash, Uneed, Peerlist, There's An AI For That | Baja |

### Ritmo: 5 submissions/día, empezar por Tier 1

### Assets necesarios antes de empezar

- Logo PNG 512x512 (fondo transparente)
- Logo PNG 256x256
- 3-5 screenshots (editor, página pública, analytics, temas)
- Tagline de 1 línea
- 3 versiones de descripción: corta (150 chars), media (300 chars), larga (500+ chars)

Template de email para guest posting + lista expandida de directorios: [`references/outreach.md`](./references/outreach.md)

---

## Integraciones obligatorias

### Sitemap

```ts
// src/app/sitemap.ts
return [
  ...staticPages,
  ...comparisonIndex,      // /vs           (priority: 0.8)
  ...comparisonPages,      // /vs/[slug]    (priority: 0.8)
  ...toolsIndex,           // /tools        (priority: 0.8)
  ...toolPages,            // /tools/[slug] (priority: 0.7)
  ...nicheIndex,           // /para         (priority: 0.8)
  ...nichePages,           // /para/[slug]  (priority: 0.7)
  ...blogIndex,            // /blog         (priority: 0.8)
  ...blogPages,            // /blog/[slug]  (priority: 0.7)
];
```

### Footer con columnas por pilar

```
[Producto]    [Para creadores]   [Herramientas]   [Recursos]
Features      Instagram          Tool 1            Blog
Pricing       TikTok             Tool 2            Contacto
About         Músicos            Tool 3            Términos
              Restaurantes       Ver todas         Privacidad
              Ver todos
```

---

## Checklist de implementación

### Día 1: Config + Tools
- [ ] Crear `src/config/tools.ts` con 4 tools
- [ ] Crear `src/app/tools/page.tsx` (hub)
- [ ] Crear 4 tools con page + client component + OG image
- [ ] Integrar en sitemap, `llms.txt`, footer

### Día 2: Blog
- [ ] Crear 20 artículos MDX (4 batches de 5)
- [ ] Verificar internal linking
- [ ] Verificar frontmatter (fechas escalonadas)

### Día 3: Comparativas + AEO
- [ ] Crear `src/config/comparisons.ts` con 3-5 competidores
- [ ] Crear ruta dinámica `/vs/[competitor]` + hub + OG images
- [ ] Actualizar `llms.txt` y `llms-full.txt` con templates AEO
- [ ] Integrar en sitemap y footer

### Día 4: Outreach
- [ ] Preparar assets (logo, screenshots, descripciones)
- [ ] Crear lista de 20+ directorios con notas
- [ ] Empezar submissions (5/día)

### Post-lanzamiento
- [ ] Verificar indexación en GSC (2-4 semanas)
- [ ] Monitorear keywords en GSC
- [ ] Agregar tools y artículos nuevos mensualmente
- [ ] Actualizar comparativas trimestralmente
- [ ] Probar citación en ChatGPT/Perplexity mensualmente

---

## Métricas de éxito

| Métrica | Meta mes 1 | Meta mes 3 | Herramienta |
|---------|-----------|-----------|-------------|
| Páginas indexadas | 60+ | 80+ | GSC |
| Impresiones orgánicas | 1,000+ | 10,000+ | GSC |
| Clics orgánicos | 100+ | 1,000+ | GSC |
| Keywords top 30 | 20+ | 50+ | GSC |
| Referring domains | 5+ | 15+ | GSC / Ahrefs |
| Backlinks | 10+ | 30+ | GSC / Ahrefs |
| Citación en LLMs | Aparece | Consistente | Manual |

---

## Caso real: Linkship

| Pilar | Páginas | Config |
|-------|---------|--------|
| Nichos | 20 (`/para/[nicho]`) | `src/config/niches.ts` |
| Tools | 4 (`/tools/[slug]`) | `src/config/tools.ts` |
| Comparativas | 4 (`/vs/[competitor]`) | `src/config/comparisons.ts` |
| Blog | 25 artículos | `content/blog/*.mdx` |
| AEO | `llms.txt` + `llms-full.txt` | `src/app/llms.txt/route.ts` |

Resultado: 60+ páginas indexables, 50+ keywords, red densa de internal linking.

---

## Referencias técnicas profundas

- [`references/niche-pages.md`](./references/niche-pages.md) — Implementación completa de `/para/[nicho]` con `generateStaticParams`, `generateMetadata`, hub page con CollectionPage + ItemList, OG image dinámico
- [`references/tool-pages.md`](./references/tool-pages.md) — Estructura de archivos, `config/tools.ts`, JSON-LD para tools (SoftwareApplication + FAQPage + BreadcrumbList)
- [`references/comparison-pages.md`](./references/comparison-pages.md) — `ComparisonConfig` interface, estructura de página completa, JSON-LD pattern (WebPage + BreadcrumbList + FAQPage, NO Product)
- [`references/blog-mdx.md`](./references/blog-mdx.md) — Frontmatter standard, 4 categorías, internal linking matrix, MDX setup en Next.js
- [`references/outreach.md`](./references/outreach.md) — Lista expandida de directorios, template de email guest posting, assets requeridos
