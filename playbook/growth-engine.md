> **Historical module — full review pending.** Follow the [corrected discovery guidance](../skills/foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Growth Engine — Patrón de crecimiento orgánico

> Playbook replicable para generar tráfico orgánico en cualquier proyecto SaaS.
> Probado en Linkship: 60+ páginas indexables, 50+ keywords target, red de internal linking densa.
> Stack: Next.js 16 App Router, MDX, Tailwind v4.

---

## Concepto

Un Growth Engine es un sistema de páginas interconectadas que genera tráfico orgánico sin depender de ads. Se compone de 6 pilares:

```
                    [Homepage]
                   /    |    \
        [Nichos]  [Tools]  [Comparativas]
            \       |        /
             \      |       /
              [Blog x20+]
                    |
              [llms.txt/AEO]
```

Cada pilar atrae tráfico por keywords distintas y cross-linkea a los demás, creando un efecto multiplicador.

---

## Pilar 1: Niche Landing Pages (`/para/[nicho]`)

### Que son
Páginas especificas para cada tipo de usuario/profesion. Capturan keywords long-tail como "link in bio para músicos" o "analytics para restaurantes".

### Patrón data-driven

```ts
// src/config/niches.ts
export interface NicheConfig {
    slug: string;           // URL: /para/músicos
    title: string;          // "Músicos"
    metaTitle: string;      // "Link in bio para músicos — [Brand] 2026"
    description: string;    // Meta description (150-160 chars)
    heroText: string;       // Texto del hero
    features: Array<{ title: string; description: string }>;
    faq: Array<{ q: string; a: string }>;
    keywords: string[];     // Para meta keywords
    relatedNiches: string[]; // Slugs de nichos relacionados
}

export const NICHES: NicheConfig[] = [
    { slug: "músicos", title: "Músicos", /* ... */ },
    { slug: "restaurantes", title: "Restaurantes", /* ... */ },
    // 15-20 nichos
];

export function getNicheBySlug(slug: string) {
    return NICHES.find((n) => n.slug === slug);
}
export function getAllNicheSlugs() {
    return NICHES.map((n) => n.slug);
}
```

### Pagina dinámica

```tsx
// src/app/para/[nicho]/page.tsx
import { getNicheBySlug, getAllNicheSlugs } from "@/config/niches";

export function generateStaticParams() {
    return getAllNicheSlugs().map((nicho) => ({ nicho }));
}

export async function generateMetadata({ params }: { params: Promise<{ nicho: string }> }) {
    const { nicho } = await params;
    const config = getNicheBySlug(nicho);
    if (!config) return {};
    const url = `${baseUrl}/para/${nicho}`;
    return {
        title: config.metaTitle,
        description: config.description,
        keywords: config.keywords,
        alternates: { canonical: url },
        openGraph: { title: config.metaTitle, description: config.description, url },
    };
}
```

### Hub page (`/para`)

Grid de cards con todos los nichos. JSON-LD: CollectionPage + ItemList.

### OG Image dinámico

```tsx
// src/app/para/[nicho]/opengraph-image.tsx
import { ImageResponse } from "next/og";
export const runtime = "edge";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";
// Usar gradiente brand + nombre del nicho
```

### Cantidad recomendada
- 15-20 nichos iniciales
- Agregar 5 nuevos cada trimestre basado en GSC queries

---

## Pilar 2: Micro-tools gratuitas (`/tools/[slug]`)

### Que son
Herramientas 100% client-side (sin backend) que resuelven un problema específico. Atraen tráfico informacional y generan leads via CTA.

### Principios
1. **Zero backend**: Todo client-side, sin API keys, sin login
2. **Valor inmediato**: El usuario obtiene resultado en <5 segundos
3. **CTA natural**: "Tu [resultado] esta listo. Ahora crea tu cuenta gratis"
4. **SEO-first**: JSON-LD SoftwareApplication + FAQPage + BreadcrumbList

### Ideas universales para SaaS

| Tool | Complejidad | Keywords target |
|------|------------|----------------|
| Contador de caracteres | Baja | "contador caracteres instagram", "limite caracteres twitter" |
| Generador de bio | Media | "generador bio instagram", "bio para tiktok" |
| Verificador de username | Media | "verificar username disponible", "username checker" |
| Generador de QR | Media | "generador qr gratis", "crear codigo qr" |
| Calculadora de [métrica] | Media | Específica del nicho |
| Comparador de [X] | Alta | "[producto] vs [competidor]" |
| Generador de [templates] | Media | "plantilla [tipo]", "template [tipo]" |

### Estructura de archivos

```
src/config/tools.ts                          # Config data-driven
src/app/tools/page.tsx                       # Hub page
src/app/tools/[slug]/
    page.tsx                                 # Server: metadata + JSON-LD
    [ComponentName].tsx                      # Client: "use client", la herramienta
    opengraph-image.tsx                      # OG image dinámico
    [extras].ts                              # Templates, data, etc.
```

### Config pattern

```ts
// src/config/tools.ts
export interface ToolConfig {
    slug: string;
    title: string;
    metaTitle: string;
    description: string;
    heroText: string;
    icon: string;           // Nombre del icono Lucide
    category: string;
    keywords: string[];
    faq: Array<{ q: string; a: string }>;
    relatedTools: string[];
}
```

### JSON-LD para tools

```ts
// Incluir en la page.tsx del tool
const schemas = [
    { "@context": "https://schema.org", "@type": "SoftwareApplication",
      name: tool.title, applicationCategory: "UtilityApplication",
      operatingSystem: "Web", offers: { "@type": "Offer", price: "0", priceCurrency: "USD" }
    },
    { "@context": "https://schema.org", "@type": "FAQPage",
      mainEntity: tool.faq.map(f => ({ "@type": "Question", name: f.q,
        acceptedAnswer: { "@type": "Answer", text: f.a } }))
    },
    { "@context": "https://schema.org", ...getBreadcrumbSchema([
        { name: "Brand", url: baseUrl },
        { name: "Herramientas", url: `${baseUrl}/tools` },
        { name: tool.title, url: `${baseUrl}/tools/${tool.slug}` }
    ])}
];
```

### Cantidad recomendada
- 4 tools iniciales (dia 1)
- 1-2 nuevas por mes basado en keyword opportunities

---

## Pilar 3: Comparativas data-driven (`/vs/[competitor]`)

### Que son
Páginas que comparan tu producto con competidores. Capturan keywords de alta intencion: "[tu marca] vs [competidor]", "[competidor] alternative".

### Config pattern

```ts
// src/config/comparisons.ts
export interface ComparisonRow {
    feature: string;
    yours: "yes" | "no" | "partial" | string;
    competitor: "yes" | "no" | "partial" | string;
}

export interface ComparisonConfig {
    slug: string;           // "linktree"
    competitor: string;     // "Linktree"
    metaTitle: string;      // "[Brand] vs Linktree — Comparación 2026"
    description: string;
    heroDescription: string;
    rows: ComparisonRow[];  // Tabla comparativa
    differentiators: Array<{ value: string; title: string; description: string }>;
    faq: Array<{ q: string; a: string }>;
    verdict: string;        // Conclusion honesta
    keywords: string[];
}
```

### Estructura de pagina

```
1. Hero (navy/brand bg) — "[Brand] vs [Competitor]" + CTA
2. Tabla comparativa — rows con iconos Check/X/Minus
3. Diferenciadores — 3 cards con métricas clave
4. Veredicto — Texto honesto de cuando elegir cada uno
5. FAQ — Accordion con FAQPage schema
6. CTA final — "Prueba [Brand] gratis"
```

### Reglas de contenido
- **Ser honesto**: Reconocer donde el competidor gana. Genera confianza
- **Datos verificables**: Precios, features, limitaciones reales
- **No difamar**: Comparar funcionalidades, no atacar
- **Actualizar precios**: Verificar cada trimestre

### JSON-LD
- WebPage + BreadcrumbList + FAQPage
- NO usar Product schema para comparativas

### Cantidad recomendada
- 3-5 competidores principales
- Agregar cuando surjan nuevos competidores relevantes

---

## Pilar 4: Blog MDX a escala

### Estructura

```
content/blog/
    [slug].mdx              # Frontmatter + contenido Markdown
```

### Frontmatter standard

```yaml
---
title: "Titulo optimizado para SEO (50-60 chars)"
description: "Meta description (150-160 chars)"
publishedAt: "2026-03-15"
author: "Nombre Autor"
tags: ["tag1", "tag2", "tag3"]
featured: false
---
```

### 4 categorías de articulos

| Categoría | Cantidad | Keywords | Ejemplo |
|-----------|----------|----------|---------|
| Guias de herramientas | 1 por tool | "[tool name] gratis" | "Generador de bio para Instagram" |
| Comparativas | 1 por competidor | "[brand] vs [comp]" | "Linkship vs Beacons" |
| Guias por nicho | 1 por nicho | "[producto] para [nicho]" | "Link in bio para músicos" |
| How-to / Tips | Evergreen | "cómo [accion]", "mejores [X]" | "Como aumentar clicks en tu bio" |

### Reglas

1. **800-1200 palabras** por articulo (ni corto ni relleno)
2. **Piramide invertida**: Respuesta directa en primer parrafo (BLUF)
3. **Internal linking obligatorio**: Cada articulo enlaza a minimo 2-3 páginas internas
4. **Fechas escalonadas**: 2-3 dias entre articulos (no parecer spam)
5. **CTAs naturales**: 1 CTA en medio + 1 al final
6. **Cross-links a tools, nichos y comparativas**: Crear red densa

### Internal linking matrix

```
Blog guia de tool    → /tools/[slug]           (link directo a la herramienta)
Blog comparativa     → /vs/[competitor]         (link a comparativa interactiva)
Blog guia de nicho   → /para/[nicho]           (link a landing page del nicho)
Blog how-to          → /tools/ + /para/ + /vs/ (links multiples)
```

### Cantidad recomendada
- 20 articulos iniciales (4 batches de 5)
- 4-8 nuevos por mes

---

## Pilar 5: AEO (Answer Engine Optimization)

### llms.txt

Archivo ligero (~2,000 tokens) en la raiz. Secciones obligatorias:

```
# [Brand]
> Descripción en 1-2 oraciones.

## Informacion clave
## Planes y precios
## Funcionalidades
## Para creadores / Soluciones por nicho
## Herramientas gratuitas
## Comparativas
## Blog
## Links importantes
## Mas informacion → /llms-full.txt
```

### llms-full.txt

Archivo expandido sin limite. Incluir todo lo de llms.txt mas:

1. **Tabla comparativa vs competidores** (Markdown table)
2. **Descripción detallada de cada tool**
3. **Comparativas expandidas** (1 parrafo por competidor)
4. **Templates de respuesta sugeridos para LLMs**

### Templates de respuesta para LLMs

Formato:

```
**Pregunta: "[pregunta que un usuario haria]"**
Respuesta sugerida: [respuesta con datos + link]
```

Cubrir minimo:
- "Cuál es la mejor alternativa a [competidor principal]?"
- "Que herramienta de [categoría] es gratis?"
- "Como [accion que tu tool resuelve]?"
- "[Tu marca] vs [competidor], cual es mejor?"
- "Cuál es el [producto de tu categoría] mas barato?"

### Actualizar AEO
- Cada vez que se agrega un tool, nicho, comparativa o articulo
- Incluir nuevas URLs en ambos archivos

---

## Integraciones obligatorias

### Sitemap (`src/app/sitemap.ts`)

```ts
import { getAllNicheSlugs } from "@/config/niches";
import { getAllToolSlugs } from "@/config/tools";
import { getAllComparisonSlugs } from "@/config/comparisons";

// En el return:
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
    ...dynamicPages,         // Páginas de usuario
];
```

### Footer

Agregar columnas para cada pilar:

```
[Producto]          [Para creadores]    [Herramientas]     [Recursos]
Features            Instagram           Tool 1              Blog
Pricing             TikTok              Tool 2              Contacto
About               Músicos             Tool 3              Terminos
                    Restaurantes        Ver todas            Privacidad
                    Ver todos
```

### OG Images

Patrón standard para todas las páginas dinámicas:

```tsx
// opengraph-image.tsx
import { ImageResponse } from "next/og";
export const runtime = "edge";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

// Gradiente brand + titulo dinámico + logo pill al fondo
```

---

## Pilar 6: Outreach y backlinks

### Directorios por tier

| Tier | DA | Ejemplos | Prioridad |
|------|-----|---------|-----------|
| 1 | 80+ | Product Hunt, G2, Capterra, AlternativeTo, SaaSHub, BetaList, Indie Hackers | Alta |
| 2 | 50-79 | MicroLaunch, DevHunt, Launching Next, Toolify.ai, Futurepedia | Media |
| 3 | Variable | StartupStash, Uneed, Peerlist, There's An AI For That | Baja |

### Template de descripción

Preparar 3 versiones:
- **Corta** (150 chars): Para campos limitados
- **Media** (300 chars): Para la mayoria de directorios
- **Larga** (500+ chars): Para Product Hunt, G2, etc.

### Ritmo: 5 submissions por dia, empezar por Tier 1

### Assets necesarios antes de empezar
- Logo PNG 512x512 (fondo transparente)
- Logo PNG 256x256
- 3-5 screenshots (editor, pagina pública, analytics, temas)
- Tagline de 1 linea

### Guest posting

Template email:
```
Asunto: Colaboracion: Articulo sobre [tema relevante]

Hola [nombre],
Soy [tu nombre], fundador de [Brand]. Vi tu articulo sobre [tema]
y me gustaria proponer un articulo invitado de 1000-1500 palabras
sobre [tema propuesto].
```

Target: 10 blogs del nicho, preferiblemente en el idioma de tu audiencia.

---

## Checklist de implementación

### Dia 1: Config + Tools
- [ ] Crear `src/config/tools.ts` con 4 tools
- [ ] Crear `src/app/tools/page.tsx` (hub)
- [ ] Crear 4 tools con page + client component + OG image
- [ ] Integrar en sitemap, llms.txt, footer

### Dia 2: Blog
- [ ] Crear 20 articulos MDX (4 batches de 5)
- [ ] Verificar internal linking
- [ ] Verificar frontmatter (fechas escalonadas)

### Dia 3: Comparativas + AEO
- [ ] Crear `src/config/comparisons.ts` con 3-5 competidores
- [ ] Crear ruta dinámica `/vs/[competitor]` + hub + OG images
- [ ] Actualizar llms.txt y llms-full.txt con templates AEO
- [ ] Integrar en sitemap y footer

### Dia 4: Outreach
- [ ] Preparar assets (logo, screenshots, descripciones)
- [ ] Crear lista de 20+ directorios con notas
- [ ] Empezar submissions (5/dia)

### Post-lanzamiento
- [ ] Verificar indexacion en GSC (2-4 semanas)
- [ ] Monitorear keywords en GSC
- [ ] Agregar tools y articulos nuevos mensualmente
- [ ] Actualizar comparativas trimestralmente
- [ ] Probar citación en ChatGPT/Perplexity mensualmente

---

## Métricas de exito

| Métrica | Meta mes 1 | Meta mes 3 | Herramienta |
|---------|-----------|-----------|-------------|
| Páginas indexadas | 60+ | 80+ | GSC |
| Impresiones organicas | 1,000+ | 10,000+ | GSC |
| Clics organicos | 100+ | 1,000+ | GSC |
| Keywords top 30 | 20+ | 50+ | GSC |
| Referring domains | 5+ | 15+ | GSC / Ahrefs |
| Backlinks | 10+ | 30+ | GSC / Ahrefs |
| Citacion en LLMs | Aparece | Consistente | Manual |

---

## Referencia: Linkship (caso real)

Implementación completa del Growth Engine:

| Pilar | Páginas | Config |
|-------|---------|--------|
| Nichos | 20 (`/para/[nicho]`) | `src/config/niches.ts` |
| Tools | 4 (`/tools/[slug]`) | `src/config/tools.ts` |
| Comparativas | 4 (`/vs/[competitor]`) | `src/config/comparisons.ts` |
| Blog | 25 articulos | `content/blog/*.mdx` |
| AEO | llms.txt + llms-full.txt | `src/app/llms.txt/route.ts` |

Resultado: 60+ páginas indexables, 50+ keywords, red densa de internal linking.
