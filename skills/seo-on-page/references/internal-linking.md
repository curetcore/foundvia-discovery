> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Internal Linking

Componentes y patrones para crear una red densa de links internos.

---

## Por qué importa

Internal linking transfiere "link equity" entre páginas y le dice a Google qué páginas son las más importantes del sitio. Es de los factores SEO más controlables y subutilizados.

**Regla básica**: cada página de contenido debe tener entre 2 y 5 links internos a páginas relacionadas.

---

## Componente `RelatedLinks`

```tsx
// components/related-links.tsx
interface RelatedLink {
  href: string;
  title: string;
}

export function RelatedLinks({ links }: { links: RelatedLink[] }) {
  return (
    <nav aria-label="Artículos relacionados" className="mt-12 border-t pt-8">
      <h2 className="text-lg font-semibold mb-4">También te puede interesar</h2>
      <ul className="space-y-2">
        {links.map((link) => (
          <li key={link.href}>
            <a
              href={link.href}
              className="text-blue-600 hover:underline"
            >
              {link.title}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
```

---

## Patrón Hub and Spoke

Una **pillar page** (hub) cubre un tema amplio (~2,000-4,000 palabras). Las **spoke pages** cubren subtemas específicos (~1,000-2,000 palabras).

```
                    [Pillar: Guía de Analytics]
                    /        |         \
                   /         |          \
        [Spoke 1]       [Spoke 2]      [Spoke 3]
   "Métricas core"  "Conversion rate"  "GA4 setup"
```

### Reglas de linking

- **Pillar → spokes**: pillar linkea a TODOS los spokes (en tabla de contenidos o en contexto)
- **Spoke → pillar**: cada spoke linkea de vuelta al pillar
- **Spoke ↔ spoke**: cada spoke linkea a 1-2 spokes hermanos
- Anchor text descriptivo (NO "leer más")
- Links bidireccionales siempre

Para estrategia completa de content clusters, usar el skill `seo-content-strategy`.

---

## Anchor text — guidelines

Anchor text es el texto clickeable del link. Google lo usa para entender de qué va la página destino.

### Bueno vs malo

| Bueno | Malo |
|-------|------|
| `guía completa de SEO técnico` | `click acá` |
| `optimizar Core Web Vitals` | `leer más` |
| `planes y precios de MiApp` | `ver precios` |
| `cómo medir conversion rate en GA4` | `este artículo` |

### Reglas

- Descriptivo — el lector debe saber a dónde va sin contexto adicional
- Natural — no spammy, no overoptimized
- Variado — si una misma página tiene 5 links entrantes, usá 5 anchor texts ligeramente distintos
- No keyword stuffing — Google penaliza anchor text exacto repetido excesivamente

---

## Footer con links a páginas principales

El footer es el último lugar donde Google busca señales de estructura del sitio. Aprovechalo:

```
Producto         Recursos        Empresa         Legal
─────────       ─────────       ─────────       ─────────
Features         Blog            About           Términos
Pricing          Docs            Contacto        Privacidad
Integraciones    Casos de uso    Carreras        Cookies
Changelog        Comunidad       Newsletter
```

### Reglas para footer

- Mínimo 3-4 columnas temáticas
- Cada columna 4-6 links
- Links a páginas legales (terms, privacy, cookies) — Google espera ver esto en footer
- Sitemap XML linked desde footer es bonus (no crítico)
