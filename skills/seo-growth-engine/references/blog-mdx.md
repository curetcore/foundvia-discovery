> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Blog MDX a escala — Implementación

Setup de blog MDX en Next.js App Router con frontmatter, internal linking y categorías.

---

## Estructura

```
content/blog/
    [slug].mdx              # Frontmatter + contenido Markdown
```

---

## Frontmatter standard

```yaml
---
title: "Título optimizado para SEO (50-60 chars)"
description: "Meta description (150-160 chars)"
publishedAt: "2026-03-15"
author: "Nombre Autor"
tags: ["tag1", "tag2", "tag3"]
featured: false
---
```

---

## 4 categorías de artículos

| Categoría | Cantidad | Keywords | Ejemplo |
|-----------|----------|----------|---------|
| Guías de herramientas | 1 por tool | "[tool name] gratis" | "Generador de bio para Instagram" |
| Comparativas | 1 por competidor | "[brand] vs [comp]" | "Brand vs Beacons" |
| Guías por nicho | 1 por nicho | "[producto] para [nicho]" | "Link in bio para músicos" |
| How-to / Tips | Evergreen | "cómo [acción]", "mejores [X]" | "Cómo aumentar clicks en tu bio" |

---

## Reglas

1. **800-1200 palabras** por artículo (ni corto ni relleno)
2. **Pirámide invertida** — respuesta directa en primer párrafo (BLUF)
3. **Internal linking obligatorio** — cada artículo enlaza a 2-3 páginas internas
4. **Fechas escalonadas** — 2-3 días entre artículos (no parecer spam de batch)
5. **CTAs naturales** — 1 CTA en medio + 1 al final
6. **Cross-links a tools, nichos y comparativas** — crear red densa

---

## Internal linking matrix

```
Blog guía de tool    → /tools/[slug]            (link directo a la herramienta)
Blog comparativa     → /vs/[competitor]         (link a comparativa interactiva)
Blog guía de nicho   → /para/[nicho]            (link a landing page del nicho)
Blog how-to          → /tools/ + /para/ + /vs/  (links múltiples)
```

---

## Cantidad recomendada

- **20 artículos iniciales** (4 batches de 5)
- 4-8 nuevos por mes

---

## Setup MDX en Next.js

```bash
npm install @next/mdx @mdx-js/loader @mdx-js/react gray-matter
```

```ts
// next.config.ts
import createMDX from "@next/mdx";

const withMDX = createMDX({
  options: {
    remarkPlugins: [],
    rehypePlugins: [],
  },
});

export default withMDX({
  pageExtensions: ["ts", "tsx", "md", "mdx"],
});
```

```ts
// lib/posts.ts
import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

const postsDirectory = path.join(process.cwd(), "content/blog");

export function getPostSlugs() {
  return fs.readdirSync(postsDirectory)
    .filter((f) => f.endsWith(".mdx"))
    .map((f) => f.replace(/\.mdx$/, ""));
}

export function getPostBySlug(slug: string) {
  const fullPath = path.join(postsDirectory, `${slug}.mdx`);
  const fileContents = fs.readFileSync(fullPath, "utf8");
  const { data, content } = matter(fileContents);

  return {
    slug,
    frontmatter: data as {
      title: string;
      description: string;
      publishedAt: string;
      author: string;
      tags: string[];
      featured?: boolean;
    },
    content,
  };
}

export function getAllPosts() {
  return getPostSlugs()
    .map(getPostBySlug)
    .sort((a, b) =>
      new Date(b.frontmatter.publishedAt).getTime() -
      new Date(a.frontmatter.publishedAt).getTime()
    );
}
```

---

## Page dinámica

```tsx
// src/app/blog/[slug]/page.tsx
import { getPostBySlug, getPostSlugs } from "@/lib/posts";
import { notFound } from "next/navigation";
import { compileMDX } from "next-mdx-remote/rsc";

export function generateStaticParams() {
  return getPostSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  if (!post) return {};

  return {
    title: post.frontmatter.title,
    description: post.frontmatter.description,
  };
}

export default async function BlogPost({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  if (!post) return notFound();

  const { content } = await compileMDX({
    source: post.content,
    options: { parseFrontmatter: false },
  });

  return (
    <article className="prose mx-auto py-12">
      <h1>{post.frontmatter.title}</h1>
      <time dateTime={post.frontmatter.publishedAt}>
        {new Date(post.frontmatter.publishedAt).toLocaleDateString("es-ES")}
      </time>
      {content}
    </article>
  );
}
```

---

## Trampa: artículos sin internal linking

Un artículo aislado (sin links a otras páginas del sitio) tiene ~3x menos retorno SEO que uno bien linkeado. Todo artículo debe linkear:

- **Tools** mencionadas en el contenido
- **Niche pages** relacionadas
- **Comparativas** si menciona competidores
- **Pillar page** del cluster (si aplica — ver skill `seo-content-strategy`)
- 1-2 artículos hermanos relacionados

Si tu artículo termina y no linkeaste a 3+ páginas internas, falta linking.
