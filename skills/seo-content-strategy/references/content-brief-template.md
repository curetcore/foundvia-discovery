> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Content Brief Template + Cadencia de actualización

Antes de escribir cualquier pieza de contenido nueva, llenar este brief.

---

## Template

```markdown
## Content Brief: [Título]

**URL target**: /blog/[slug]
**Keyword principal**: [keyword] (vol: X, KD: Y)
**Keywords secundarias**: [lista]
**Intent**: Informational / Commercial / Transactional
**Word count**: 1,500-2,000
**Cluster**: [Pillar page] o standalone

### Estructura H2

1. [H2] — qué es / definición (BLUF)
2. [H2] — por qué importa
3. [H2] — cómo hacerlo (pasos)
4. [H2] — errores comunes
5. [H2] — herramientas recomendadas
6. [H2] — FAQ (3-5 preguntas)

### CTAs

- Primary: [acción deseada]
- Secondary: [otra acción]

### Fuentes a citar

- [URL 1]
- [URL 2]

### Competencia

- [URL competidor 1] — qué cubre
- [URL competidor 2] — qué cubre
- **Diferenciador nuestro**: [qué podemos ofrecer que ellos no]
```

---

## Cadencia de actualización

| Tipo de contenido | Frecuencia | Señal de update |
|-------------------|------------|-----------------|
| Evergreen (guías, how-tos) | Cada 6 meses | Verificar datos, links, screenshots |
| Year-specific ("SEO 2026") | Anual (crear versión nueva) | Cambiar año, datos nuevos |
| Product pages | Con cada release | Features nuevas, precios |
| Blog posts | Cada 3-6 meses | GSC position bajando |
| Landing pages | Trimestral | A/B test results, conversion data |
| Pricing | Con cambios de precio | Siempre actual |
| Legal (terms, privacy) | Anual o con cambios | Compliance |

---

## Señales de que hay que actualizar

1. **Position promedio cayendo en GSC** — últimos 28 días vs anteriores
2. **Contenido con fecha vieja visible** — "Guía 2024" en 2026
3. **Screenshots de UI desactualizada**
4. **Links rotos** (curl o Screaming Frog)
5. **Datos estadísticos de hace más de 12 meses**

---

## Workflow de update

1. Identificar contenido con CTR < 2% o position cayendo (GSC)
2. Comparar con competidores top 3 en SERP — qué cubren ellos que tu no
3. Aplicar cambios: agregar secciones faltantes, refrescar stats, actualizar año
4. Cambiar `dateModified` en JSON-LD (no `datePublished`)
5. Solicitar reindexación en GSC URL Inspection
6. Esperar 2-4 semanas para ver impacto

---

## Trampa común: "actualizar = republish"

Algunos creen que cambiar la fecha de publicación da boost. **NO**. Google detecta cuando cambiás `datePublished` sin cambios reales en el contenido y lo penaliza.

Reglas honestas:
- Si cambiaste >30% del contenido → actualizá `dateModified`, mantené `datePublished` original
- Si reescribiste completamente → considerá una URL nueva con redirect 301 desde la vieja
- NUNCA cambies `datePublished` retroactivamente sin cambios reales
