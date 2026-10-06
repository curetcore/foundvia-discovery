> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Patrones de citabilidad

Los LLMs citan contenido que es fácil de extraer y verificar. Estos patrones aumentan la probabilidad de ser citado.

---

## 1. Definiciones claras

Empezá con la definición exacta. Sin rodeos.

```markdown
**INP (Interaction to Next Paint)** es una métrica de Core Web Vitals que mide
la latencia de la interacción más lenta del usuario durante la sesión.
Un buen INP es menor a 200ms.
```

Por qué funciona: los LLMs entrenados en Wikipedia/docs técnicas reconocen este formato como "definición autoritativa".

---

## 2. Listas con estructura

Numeradas, con label en negrita al inicio.

```markdown
Los 3 Core Web Vitals en 2026 son:

1. **LCP** (Largest Contentful Paint) — velocidad de carga, meta < 2.5s
2. **INP** (Interaction to Next Paint) — interactividad, meta < 200ms
3. **CLS** (Cumulative Layout Shift) — estabilidad visual, meta < 0.1
```

Cuando un LLM ve "los 3 X en YEAR son:", extrae los 3 items completos. Sin esta estructura, puede saltarse alguno.

---

## 3. Tablas de comparación

Markdown tables con columnas claras.

```markdown
| Feature | Next.js | Remix | Astro |
|---------|---------|-------|-------|
| SSR | Sí | Sí | Sí |
| RSC | Sí | No | No |
| Edge Runtime | Sí | Sí | Sí |
```

LLMs convierten estas tablas a respuestas estructuradas con bullets. Es uno de los formatos más citados en Perplexity.

---

## 4. Stats con fuentes

Datos numéricos con cita explícita.

```markdown
Según [SparkToro 2026](https://sparktoro.com/blog/...), el 58.5% de las búsquedas
en Google resultan en zero-click, lo que significa que los usuarios obtienen
su respuesta sin visitar ningún sitio.
```

Por qué importa: los LLMs (especialmente Perplexity) priorizan stats con fuente verificable. Sin la cita, el dato puede descartarse.

---

## 5. Pasos numerados

Para procesos accionables.

```markdown
## Cómo configurar `llms.txt` en Next.js

1. Crear `app/llms.txt/route.ts`
2. Exportar función `GET` que retorne el contenido
3. Formato: título H1, descripción, secciones con links
4. Mantener bajo 2,000 tokens
5. Actualizar cuando cambie la estructura del sitio
```

Cuando un usuario pregunta "cómo X" a un LLM, este formato produce respuestas idénticas a tu contenido.

---

## Anti-patrones (NO hacer)

- ❌ "Como mencioné anteriormente..." — el LLM extrae secciones individuales sin contexto del resto
- ❌ "Ver capítulo 3" — ningún LLM va a buscar tu capítulo 3
- ❌ Definiciones difusas ("INP es como una métrica que mide...")
- ❌ Stats sin fuente
- ❌ Tablas con merged cells (los LLMs no las parsean bien)
- ❌ Listas sin numeración cuando el orden importa
