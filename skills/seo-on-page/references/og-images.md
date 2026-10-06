> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Open Graph Images — `next/og`

Implementación completa de OG dinámico con `ImageResponse` de Next.js.

---

## Por qué OG images dinámicos

OG images estáticas (un PNG fijo) son útiles para la home. Pero para blog posts, productos o landing pages, querés que cada URL tenga **su propia imagen** con el título correcto.

Beneficio: cuando alguien comparte `/blog/guia-seo-2026` en Twitter o Slack, el preview muestra "Guía de SEO 2026" en grande — no el OG genérico del sitio. CTR sube ~30-50% en redes sociales.

---

## Endpoint base con `next/og`

```tsx
// app/og/route.tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get("title") ?? "Brand";
  const description = searchParams.get("description") ?? "";

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          padding: "60px",
          background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
          color: "white",
        }}
      >
        <div style={{ fontSize: 64, fontWeight: "bold", marginBottom: 20 }}>
          {title}
        </div>
        {description && (
          <div style={{ fontSize: 28, opacity: 0.8 }}>{description}</div>
        )}
        <div
          style={{
            fontSize: 24,
            marginTop: "auto",
            opacity: 0.6,
          }}
        >
          brand.com
        </div>
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
```

### Notas críticas

- `runtime = "edge"` es **obligatorio** — `next/og` solo funciona en edge
- El JSX de `ImageResponse` NO es React real, es Satori. Solo soporta un subset de CSS:
  - ✅ Flexbox, gradientes, opacity, padding, margin, fontSize, fontWeight
  - ❌ Grid, animations, transforms complejos, custom fonts sin importar
- **Variable fonts NO funcionan en Satori** — usar fonts estáticas (`.woff2` o `.ttf`)
- El path al endpoint debe ser absoluto cuando lo referenciás en metadata (con `metadataBase` configurado, los relativos funcionan)

---

## OG image como archivo de Next 15+

En lugar de un endpoint, podés usar el patrón `opengraph-image.tsx` por ruta:

```tsx
// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image({ params }: { params: { slug: string } }) {
  // Podés hacer fetch de la DB acá
  const post = await getPost(params.slug);

  return new ImageResponse(
    (
      <div style={{ /* ... */ }}>
        {post.title}
      </div>
    ),
    { ...size }
  );
}
```

Next.js automáticamente lo asocia a la ruta correspondiente y lo agrega al `<head>` como OG image.

---

## Uso en `generateMetadata`

```tsx
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = await prisma.post.findUnique({ where: { slug } });

  return {
    openGraph: {
      images: [
        {
          url: `/og?title=${encodeURIComponent(post?.title ?? "")}&description=${encodeURIComponent(post?.excerpt?.slice(0, 100) ?? "")}`,
          width: 1200,
          height: 630,
        },
      ],
    },
  };
}
```

Si usás el patrón `opengraph-image.tsx` por ruta, no necesitás declarar nada en `generateMetadata` — Next.js lo asocia automático.

---

## Verificación post-deploy

| Plataforma | Validador |
|------------|-----------|
| Open Graph (Facebook) | [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) |
| Twitter Card | [Card Validator](https://cards-dev.twitter.com/validator) |
| LinkedIn | [Post Inspector](https://www.linkedin.com/post-inspector/) |
| Generic OG preview | [opengraph.xyz](https://opengraph.xyz) |

> **Tip**: si Facebook cachea una versión vieja, usá "Scrape Again" en el debugger. Si Twitter no actualiza, esperá 7 días o cambiá el path.
