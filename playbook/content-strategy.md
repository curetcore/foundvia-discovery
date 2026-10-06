> **Historical module — full review pending.** Follow the [corrected discovery guidance](../skills/foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Content Strategy

> Cubre BLUF, content clusters, E-E-A-T, keyword research, y cadencia de actualización.
> Aplica a páginas de contenido (blog, docs, landing pages, product pages).

---

## BLUF Framework (Bottom Line Up Front)

Patrón militar adaptado para contenido web y AI search. Regla: **responder primero, explicar despues**.

### Por que funciona

1. **AI extraction**: LLMs toman el primer parrafo para respuestas
2. **Featured snippets**: Google extrae la primera definición
3. **User behavior**: 80% de usuarios deciden en los primeros 5 segundos
4. **Bounce rate**: Si no ven valor inmediato, se van

### Estructura BLUF

```
[Respuesta directa en 1-2 oraciones]

[Contexto y matices en 2-3 oraciones]

[Detalles expandidos en secciones H2]
```

### Ejemplos por tipo

**Definición (qué es X)**:
```markdown
# Que es INP

**INP (Interaction to Next Paint)** mide la latencia de la interacción
mas lenta del usuario durante su sesion. Un buen INP es menor a 200ms.

INP reemplazó a FID como Core Web Vital en marzo 2024. A diferencia de
FID que solo media la primera interacción, INP mide TODAS las interacciones
y reporta la peor (percentil 98).

## Como medir INP
...
```

**How-to (como hacer X)**:
```markdown
# Como agregar SEO en Next.js

Para agregar SEO completo en Next.js: usa `generateMetadata` para meta tags,
JSON-LD para structured data, `sitemap.ts` para sitemap, y `robots.ts` para
control de crawlers. Toma ~30 minutos configurar todo.

## Paso 1: generateMetadata en layout.tsx
...
```

**Comparación (X vs Y)**:
```markdown
# Next.js vs Remix para SEO

Next.js es mejor para SEO en sitios con contenido dinámico y e-commerce
gracias a RSC, ISR, y la Metadata API nativa. Remix es mejor para apps
interactivas con formularios complejos.

| Aspecto | Next.js | Remix |
|---------|---------|-------|
| SSR | Si (RSC) | Si (loaders) |
...
```

---

## Passage-Level Ranking

Google puede rankear secciones individuales de una pagina (passages), no solo la pagina completa. Cada H2 debe ser autosuficiente.

### Reglas para passages

1. **H2 descriptivo**: Incluir keyword de la sección
2. **Primera oracion BLUF**: Responder la pregunta implicita del H2
3. **Auto-contenido**: Se puede leer sin contexto del resto de la pagina
4. **200-400 palabras** por sección es optimo
5. **Sin referencias internas**: Evitar "cómo mencionamos arriba"

### Ejemplo

```markdown
## Como optimizar INP en React

INP se optimiza evitando operaciones sincronas largas en el main thread.
Las tres técnicas mas efectivas son: useTransition para operaciones de
estado, dynamic imports para code splitting, y web workers para calculo
pesado.

### useTransition
Para operaciones que actualizan el estado pero no son urgentes...

### Dynamic imports
Componentes pesados que no son visibles en el viewport inicial...
```

Cada H2 puede aparecer como resultado de búsqueda independiente.

---

## Content Clusters (Hub and Spoke)

### Modelo

```
                    [Pillar Page]
                    /    |    \
                   /     |     \
            [Spoke 1] [Spoke 2] [Spoke 3]
```

- **Pillar page**: Tema amplio, 2,000-4,000 palabras, linkea a todos los spokes
- **Spoke page**: Subtema específico, 1,000-2,000 palabras, linkea al pillar

### Ejemplo SaaS (Analytics)

```
Pillar: /blog/guia-analytics-ecommerce
  ├── Spoke: /blog/métricas-ecommerce-esenciales
  ├── Spoke: /blog/como-medir-conversion-rate
  ├── Spoke: /blog/google-analytics-4-ecommerce
  ├── Spoke: /blog/atribución-marketing-ecommerce
  └── Spoke: /blog/dashboards-kpis-ecommerce
```

### Reglas de linking

- Pillar linkea a TODOS los spokes (tabla de contenidos o links en contexto)
- Cada spoke linkea al pillar Y a 1-2 spokes relacionados
- Anchor text descriptivo (NO "leer mas")
- Links bidireccionales siempre

### generateMetadata para cluster

```tsx
// app/blog/[slug]/page.tsx
// Incluir referencia al pillar en meta cuando es spoke
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = await prisma.post.findUnique({
    where: { slug },
    include: { pillar: true }, // Relación spoke -> pillar
  });

  return {
    title: post?.title,
    description: post?.excerpt,
    other: {
      // Ayuda a Google a entender la relación
      "article:section": post?.pillar?.title ?? post?.category,
    },
  };
}
```

---

## E-E-A-T para SaaS

E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) aplica a TODAS las queries desde 2024. No es un factor de ranking directo pero influye en quality raters.

### Acciones por signal

| Signal | Acciones concretas |
|--------|-------------------|
| **Experience** | Case studies de clientes reales, screenshots del producto, demos interactivas, métricas de uso ("50,000 usuarios confían en nosotros") |
| **Expertise** | Author bios con credenciales, contenido técnico profundo, terminologia correcta del dominio, actualizaciones frecuentes |
| **Authoritativeness** | Links desde sitios del nicho, mencionado en publicaciones, partnerships visibles, premios/certificaciones |
| **Trustworthiness** | HTTPS obligatorio, politica de privacidad, terminos de servicio, informacion de contacto real, reviews verificadas |

### Implementación en Next.js

```tsx
// components/author-bio.tsx
import type { Person, WithContext } from "schema-dts";

interface Author {
  name: string;
  role: string;
  image: string;
  url: string;
  description: string;
}

export function AuthorBio({ author }: { author: Author }) {
  const jsonLd: WithContext<Person> = {
    "@context": "https://schema.org",
    "@type": "Person",
    name: author.name,
    jobTitle: author.role,
    image: author.image,
    url: author.url,
    description: author.description,
  };

  return (
    <aside className="flex items-center gap-4 border-t pt-6 mt-8">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <img
        src={author.image}
        alt={author.name}
        className="w-12 h-12 rounded-full"
      />
      <div>
        <p className="font-medium">{author.name}</p>
        <p className="text-sm text-zinc-500">{author.role}</p>
      </div>
    </aside>
  );
}
```

---

## FAQ Optimization

FAQs son un formato privilegiado por AI Overviews y featured snippets.

### Reglas

- Preguntas reales (de GSC queries, soporte, reviews)
- Respuestas de 40-60 palabras (optimo para snippets)
- Primera oracion responde la pregunta directamente
- FAQPage schema obligatorio
- Maximo 10 FAQs por pagina (Google puede ignorar mas)

### Sources para preguntas

1. **GSC Performance**: Queries con impresiones altas y CTR bajo = oportunidad
2. **People Also Ask**: Preguntas relacionadas en Google
3. **Soporte al cliente**: Tickets y chats frecuentes
4. **Reviews**: Dudas comunes de compradores
5. **Reddit/Quora**: Preguntas sobre tu nicho

---

## Keyword Research

### Flujo

```
1. Seed keywords (5-10 del dominio)
     ↓
2. Expansión (herramientas: GSC, Ahrefs, brave-search MCP)
     ↓
3. Categorización por intent
     ↓
4. Priorización (volumen × dificultad × relevancia)
     ↓
5. Mapping a páginas existentes o nuevas
```

### Categorización por intent

| Intent | Señales | Tipo de pagina | Ejemplo |
|--------|---------|----------------|---------|
| Informational | "que es", "como", "por que" | Blog, guia | "qué es INP" |
| Commercial | "mejor", "top", "vs", "review" | Comparación, lista | "mejor herramienta SEO" |
| Transactional | "comprar", "precio", "plan" | Product, pricing | "tuapp precios" |
| Navigational | marca, nombre producto | Home, product | "tuapp login" |

### Keyword mapping

```
Keyword                          → Pagina              → Intent
"analytics ecommerce"            → /features/analytics → Commercial
"cómo medir conversion rate"     → /blog/medir-cr      → Informational
"tuapp precios"               → /precios            → Navigational
"herramienta bi ecommerce"       → /                   → Commercial
```

---

## Content Update Cadence

| Tipo de contenido | Frecuencia de actualización | Señal de update |
|-------------------|----------------------------|-----------------|
| Evergreen (guias, how-tos) | Cada 6 meses | Verificar datos, links, screenshots |
| Year-specific ("SEO 2026") | Anual (crear version nueva) | Cambiar año, datos nuevos |
| Product pages | Con cada release | Features nuevas, precios |
| Blog posts | Cada 3-6 meses | GSC position bajando |
| Landing pages | Trimestral | A/B test results, conversion data |
| Pricing | Con cambios de precio | Siempre actual |
| Legal (terms, privacy) | Anual o con cambios | Compliance |

### Señales de que hay que actualizar

1. Position promedio cayendo en GSC (ultimos 28 dias vs anteriores)
2. Contenido con fecha vieja visible ("Guia 2024")
3. Screenshots de UI desactualizada
4. Links rotos
5. Datos estadisticos de hace mas de 12 meses

---

## Content Brief Template

Para cada pieza de contenido nueva, crear un brief antes de escribir:

```markdown
## Content Brief: [Titulo]

**URL target**: /blog/[slug]
**Keyword principal**: [keyword] (vol: X, KD: Y)
**Keywords secundarias**: [lista]
**Intent**: Informational / Commercial / Transactional
**Word count**: 1,500-2,000
**Cluster**: [Pillar page] o standalone

### Estructura H2

1. [H2] - que es / definición (BLUF)
2. [H2] - por que importa
3. [H2] - como hacerlo (pasos)
4. [H2] - errores comunes
5. [H2] - herramientas recomendadas
6. [H2] - FAQ (3-5 preguntas)

### CTAs

- Primary: [accion deseada]
- Secondary: [otra accion]

### Fuentes a citar

- [URL 1]
- [URL 2]

### Competencia

- [URL competidor 1] - que cubre
- [URL competidor 2] - que cubre
- **Diferenciador nuestro**: [que podemos ofrecer que ellos no]
```

---

## Verificación

| Que verificar | Herramienta | Frecuencia |
|---------------|-------------|------------|
| Keyword rankings | GSC Performance | Semanal |
| Content freshness | Manual review | Mensual |
| Cluster coverage | Content inventory | Trimestral |
| E-E-A-T signals | Manual audit | Trimestral |
| FAQ performance | GSC (queries de pregunta) | Mensual |
| Competitor gap | Ahrefs / brave-search | Trimestral |
