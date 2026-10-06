---
name: seo-content-strategy
description: Diseña estrategia de contenido SEO — BLUF, content clusters (hub & spoke), passage-level ranking, E-E-A-T, keyword research por intent, FAQ optimization, content briefs y cadencia de actualización. Use this skill whenever the user asks about blog strategy, content planning, what to write, keyword research, content clusters, pillar pages, E-E-A-T signals, author bios, FAQ pages, or content calendar — even if they don't mention "SEO" explicitly.
---

> **Historical module — full review pending.** Follow the [corrected discovery guidance](../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Content Strategy

Estrategia de contenido para SEO + GEO. Aplica a blog, docs, landing pages y product pages. Probado en producción sobre Linkship y Karrito.

---

## Cuándo invocar este skill

- El usuario pide diseñar una estrategia de contenido o blog
- Hay que decidir qué escribir, en qué orden, cómo organizarlo
- Pregunta sobre content clusters, pillar pages, hub & spoke
- Necesita keyword research o priorización
- Hay que escribir un content brief antes de publicar
- E-E-A-T review, author bios, signals de autoridad
- FAQ pages para AI Overviews / featured snippets
- Cadencia de actualización de contenido existente

Para implementación técnica de FAQ schema, usar `seo-ai-geo`. Para meta tags y headings, usar `seo-on-page`. Para playbook end-to-end (tools, blog, comparativas, outreach), usar `seo-growth-engine`.

---

## BLUF Framework (Bottom Line Up Front)

Patrón militar adaptado a contenido web y AI search. **Regla**: responder primero, explicar después.

### Por qué funciona

1. **AI extraction** — LLMs toman el primer párrafo para respuestas
2. **Featured snippets** — Google extrae la primera definición
3. **User behavior** — 80% de usuarios deciden en los primeros 5 segundos
4. **Bounce rate** — sin valor inmediato, se van

### Estructura BLUF

```
[Respuesta directa en 1-2 oraciones]

[Contexto y matices en 2-3 oraciones]

[Detalles expandidos en secciones H2]
```

### Ejemplo: "¿Qué es INP?"

```markdown
# Qué es INP

**INP (Interaction to Next Paint)** mide la latencia de la interacción
más lenta del usuario durante su sesión. Un buen INP es menor a 200ms.

INP reemplazó a FID como Core Web Vital en marzo 2024. A diferencia de
FID que solo medía la primera interacción, INP mide TODAS las interacciones
y reporta la peor (percentil 98).

## Cómo medir INP
...
```

---

## Passage-Level Ranking

Google puede rankear secciones individuales de una página (passages), no solo la página completa. Cada H2 debe ser autosuficiente.

### Reglas para passages

1. **H2 descriptivo** — incluir keyword de la sección
2. **Primera oración BLUF** — responder la pregunta implícita del H2
3. **Auto-contenido** — se puede leer sin contexto del resto de la página
4. **200-400 palabras** por sección es óptimo
5. **Sin referencias internas** — evitar "como mencionamos arriba"

---

## Content Clusters (Hub and Spoke)

### Modelo

```
                    [Pillar Page]
                    /    |    \
                   /     |     \
            [Spoke 1] [Spoke 2] [Spoke 3]
```

- **Pillar page**: tema amplio, 2,000-4,000 palabras, linkea a todos los spokes
- **Spoke page**: subtema específico, 1,000-2,000 palabras, linkea al pillar

### Ejemplo SaaS (Analytics)

```
Pillar: /blog/guia-analytics-ecommerce
  ├── Spoke: /blog/metricas-ecommerce-esenciales
  ├── Spoke: /blog/como-medir-conversion-rate
  ├── Spoke: /blog/google-analytics-4-ecommerce
  ├── Spoke: /blog/atribucion-marketing-ecommerce
  └── Spoke: /blog/dashboards-kpis-ecommerce
```

### Reglas de linking

- Pillar linkea a TODOS los spokes (tabla de contenidos o links en contexto)
- Cada spoke linkea al pillar Y a 1-2 spokes relacionados
- Anchor text descriptivo (NO "leer más")
- Links bidireccionales siempre

---

## E-E-A-T para SaaS

E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) aplica a TODAS las queries desde 2024. No es un factor de ranking directo pero influye en quality raters.

### Acciones por signal

| Signal | Acciones concretas |
|--------|-------------------|
| **Experience** | Case studies de clientes reales, screenshots del producto, demos interactivas, métricas de uso ("50,000 usuarios confían en nosotros") |
| **Expertise** | Author bios con credenciales, contenido técnico profundo, terminología correcta del dominio, actualizaciones frecuentes |
| **Authoritativeness** | Links desde sitios del nicho, mencionado en publicaciones, partnerships visibles, premios/certificaciones |
| **Trustworthiness** | HTTPS obligatorio, política de privacidad, términos de servicio, información de contacto real, reviews verificadas |

### Author bio component (Person schema)

```tsx
import type { Person, WithContext } from "schema-dts";

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
      <script type="application/ld+json"
              dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <img src={author.image} alt={author.name} className="w-12 h-12 rounded-full" />
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
- Respuestas de 40-60 palabras (óptimo para snippets)
- Primera oración responde la pregunta directamente
- FAQPage schema obligatorio (ver skill `seo-ai-geo`)
- Máximo 10 FAQs por página (Google puede ignorar más)

### Sources para preguntas

1. **GSC Performance** — queries con impresiones altas y CTR bajo = oportunidad
2. **People Also Ask** — preguntas relacionadas en Google
3. **Soporte al cliente** — tickets y chats frecuentes
4. **Reviews** — dudas comunes de compradores
5. **Reddit / Quora** — preguntas sobre tu nicho

---

## Keyword Research

### Flujo

```
1. Seed keywords (5-10 del dominio)
     ↓
2. Expansión (GSC, Ahrefs, brave-search)
     ↓
3. Categorización por intent
     ↓
4. Priorización (volumen × dificultad × relevancia)
     ↓
5. Mapping a páginas existentes o nuevas
```

### Categorización por intent

| Intent | Señales | Tipo de página | Ejemplo |
|--------|---------|----------------|---------|
| Informational | "qué es", "cómo", "por qué" | Blog, guía | "qué es INP" |
| Commercial | "mejor", "top", "vs", "review" | Comparación, lista | "mejor herramienta SEO" |
| Transactional | "comprar", "precio", "plan" | Product, pricing | "miapp precios" |
| Navigational | marca, nombre producto | Home, product | "miapp login" |

### Keyword mapping

```
Keyword                          → Página              → Intent
"analytics ecommerce"            → /features/analytics → Commercial
"cómo medir conversion rate"     → /blog/medir-cr      → Informational
"miapp precios"                  → /precios            → Navigational
"herramienta bi ecommerce"       → /                   → Commercial
```

Plantilla de content brief antes de escribir + cadencia de actualización: [`references/content-brief-template.md`](./references/content-brief-template.md)

---

## Content Update Cadence (resumen)

| Tipo de contenido | Frecuencia | Señal de update |
|-------------------|------------|-----------------|
| Evergreen (guías, how-tos) | Cada 6 meses | Verificar datos, links, screenshots |
| Year-specific ("SEO 2026") | Anual | Cambiar año, datos nuevos |
| Product pages | Con cada release | Features nuevas, precios |
| Blog posts | Cada 3-6 meses | GSC position bajando |
| Pricing | Con cambios de precio | Siempre actual |

Detalles + señales de cuándo actualizar: [`references/content-brief-template.md`](./references/content-brief-template.md)

---

## Verificación

| Qué verificar | Herramienta | Frecuencia |
|---------------|-------------|------------|
| Keyword rankings | GSC Performance | Semanal |
| Content freshness | Manual review | Mensual |
| Cluster coverage | Content inventory | Trimestral |
| E-E-A-T signals | Manual audit | Trimestral |
| FAQ performance | GSC (queries de pregunta) | Mensual |
| Competitor gap | Ahrefs / brave-search | Trimestral |

---

## Referencias técnicas profundas

- [`references/content-brief-template.md`](./references/content-brief-template.md) — Template completo de content brief antes de escribir + tabla detallada de cadencia de actualización + señales de "hay que actualizar"
