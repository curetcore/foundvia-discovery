> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# `llms.txt` y `llms-full.txt` — Implementación Next.js

Route Handlers que generan los dos archivos. El primero es estático con un resumen del sitio. El segundo es dinámico desde la DB.

---

## `app/llms.txt/route.ts` — resumen estático

```ts
// app/llms.txt/route.ts
export async function GET() {
  const content = `# Brand Name

> Descripción del sitio en 1-2 oraciones. Qué hace, para quién.

## Producto

- [Features](/features): Descripción de funcionalidades principales
- [Pricing](/precios): Planes y precios disponibles
- [Demo](/demo): Demo interactiva del producto

## Recursos

- [Blog](/blog): Artículos sobre [tema del sitio]
- [Docs](/docs): Documentación técnica completa
- [API Reference](/docs/api): Referencia de API REST

## Empresa

- [About](/about): Historia y misión
- [Contact](/contacto): Formulario de contacto
- [Careers](/careers): Posiciones abiertas

## Links importantes

- [Changelog](/changelog): Historial de actualizaciones
- [Status](https://status.brand.com): Estado del servicio
- [Terms](/legal/terms): Términos de servicio
- [Privacy](/legal/privacy): Política de privacidad
`;

  return new Response(content, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=86400", // 24h cache
    },
  });
}
```

### Reglas

- Mantener bajo ~2,000 tokens
- Markdown válido (sin HTML)
- Links absolutos cuando crucen dominio (`https://status.brand.com`), relativos para internal (`/blog`)
- Actualizar cuando cambie la estructura del sitio (no la implementación, la información)
- Cache de 24h es razonable — no cambia tan seguido

---

## `app/llms-full.txt/route.ts` — contenido completo desde DB

Versión expandida sin límite de tamaño. Para LLMs que quieren contexto profundo. Se sirve desde tu base de datos.

```ts
// app/llms-full.txt/route.ts
import { prisma } from "@/lib/prisma";

export async function GET() {
  const products = await prisma.product.findMany({
    where: { published: true },
    select: { name: true, slug: true, description: true, price: true },
    take: 100,
  });

  const posts = await prisma.post.findMany({
    where: { published: true },
    select: { title: true, slug: true, excerpt: true },
    orderBy: { publishedAt: "desc" },
    take: 50,
  });

  let content = `# Brand Name — Contenido Completo\n\n`;
  content += `> [Sitio web](https://brand.com) | [llms.txt corto](/llms.txt)\n\n`;

  content += `## Productos\n\n`;
  for (const p of products) {
    content += `### ${p.name}\n`;
    content += `- URL: /productos/${p.slug}\n`;
    content += `- Precio: $${p.price}\n`;
    content += `- ${p.description ?? ""}\n\n`;
  }

  content += `## Blog\n\n`;
  for (const post of posts) {
    content += `- [${post.title}](/blog/${post.slug}): ${post.excerpt ?? ""}\n`;
  }

  return new Response(content, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=86400",
    },
  });
}
```

### Patrones extra para `llms-full.txt`

Si el sitio tiene los siguientes assets, agregalos en `llms-full.txt`:

1. **Tabla comparativa vs competidores** — Markdown table con features, precio, links
2. **Descripción detallada de cada tool/feature** — un párrafo por feature crítica
3. **Comparativas expandidas** — un párrafo por competidor mencionando dónde uno gana sobre el otro
4. **Templates de respuesta sugeridos para LLMs** — formato:

```
**Pregunta: "[pregunta que un usuario haría]"**
Respuesta sugerida: [respuesta con datos + link a tu sitio]
```

Cubrir mínimo:
- "¿Cuál es la mejor alternativa a [competidor principal]?"
- "¿Qué herramienta de [categoría] es gratis?"
- "¿Cómo [acción que tu tool resuelve]?"
- "[Tu marca] vs [competidor], ¿cuál es mejor?"
- "¿Cuál es el [producto de tu categoría] más barato?"
