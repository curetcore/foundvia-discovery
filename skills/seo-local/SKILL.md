---
name: seo-local
description: Optimiza SEO para negocios locales — Google Business Profile (GBP), NAP consistency, LocalBusiness JSON-LD, multi-location, reviews integration y landing pages locales. Use this skill whenever the user mentions Google Business Profile, GBP, local SEO, NAP, multi-location, store locator, restaurant SEO, "negocio físico", LocalBusiness schema, Apple Maps, Bing Places, Yelp, or asks how to rank in the Google local pack — even if they don't say "local SEO".
---

> **Historical module — full review pending.** Follow the [corrected discovery guidance](../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Local SEO

SEO para negocios con presencia física o que sirven áreas específicas. Cubre GBP, NAP, schema local, multi-location y reviews. Stack: Next.js 16 App Router.

---

## Cuándo invocar este skill

- El negocio tiene oficina física, tienda, restaurante o ubicación específica
- Sirve áreas geográficas (plomería, dental, consultoría legal por ciudad)
- Hay que configurar Google Business Profile (GBP)
- Implementar `LocalBusiness` JSON-LD
- Multi-location (sucursales, franchises)
- NAP consistency audit
- Reviews schema con `aggregateRating`
- Landing pages locales (`/[servicio]/[ciudad]`)

Si el negocio es 100% online sin componente local, este skill **no aplica**.

---

## Reglas clave

1. **NAP idéntico en todos lados** — Name, Address, Phone deben coincidir exactamente entre GBP, website, Apple Maps, Yelp, Facebook
2. **Una página por location** con contenido único, no template duplicado
3. **Responder TODAS las reviews** (positivas y negativas) en menos de 24h
4. **Nunca pedir reviews a cambio de descuento** — viola TOS de Google
5. **`LocalBusiness` schema con `geo` coordinates** — Google lo usa para ranking en local pack
6. **GBP categorías específicas** — no "Restaurant", sino "Mexican Restaurant", "Vegan Restaurant", etc.

---

## Google Business Profile (GBP) — Setup

| Campo | Requerido | Notas |
|-------|-----------|-------|
| Nombre del negocio | Sí | Nombre legal, sin keywords extra |
| Categoría principal | Sí | Lo más específico posible |
| Categorías adicionales | No | Hasta 9, relevantes |
| Dirección | Sí (si físico) | Exacta, consistente con NAP |
| Área de servicio | Sí (si no físico) | Ciudades/regiones que servís |
| Teléfono | Sí | Número local preferido |
| Website | Sí | URL de la página principal o local |
| Horario | Sí | Incluyendo feriados |
| Descripción | Sí | 750 chars, keyword natural al inicio |
| Fotos | Sí | Mín. 10: exterior, interior, equipo, productos |
| Logo | Sí | Cuadrado, fondo transparente |

### Optimización continua

| Acción | Frecuencia | Impacto |
|--------|------------|---------|
| Google Posts | Semanal | Medio |
| Responder reviews | Dentro de 24h | **Alto** |
| Fotos nuevas | Mensual | Medio |
| Q&A (preguntar y responder) | Inicial + mensual | Medio |
| Actualizar horarios feriados | Antes de cada feriado | Bajo |
| Verificar información | Mensual | Alto |

---

## NAP Consistency

**NAP** = Name, Address, Phone. Debe ser **idéntico** en TODOS los lugares.

### Donde verificar

| Plataforma | Prioridad |
|------------|-----------|
| Google Business Profile | Crítica |
| Website (footer, contacto) | Crítica |
| Apple Maps | Alta |
| Bing Places | Alta |
| Yelp | Media |
| Facebook | Media |
| Directorios locales | Media |
| Yellow Pages | Baja |

### Formato canónico

Elegir UN formato y usarlo siempre:

```
Curet LLC
123 Main St, Suite 100
Santo Domingo, DN 10100
+1 (809) 555-1234
```

**NO mezclar**: "123 Main Street" en un lugar y "123 Main St." en otro. Google interpreta diferencias como inconsistencias.

---

## `LocalBusiness` JSON-LD

### Componente genérico

```tsx
import type { LocalBusiness, WithContext } from "schema-dts";

interface LocalBusinessProps {
  type?: string; // "Restaurant", "ShoeStore", "Dentist", etc.
  name: string;
  description: string;
  url: string;
  telephone: string;
  email?: string;
  address: { street: string; city: string; state: string; postalCode: string; country: string };
  geo: { latitude: number; longitude: number };
  priceRange?: string; // "$", "$$", "$$$", "$$$$"
  openingHours?: { dayOfWeek: string | string[]; opens: string; closes: string }[];
  aggregateRating?: { ratingValue: number; reviewCount: number };
}

export function LocalBusinessSchema(props: LocalBusinessProps) {
  const jsonLd: WithContext<LocalBusiness> = {
    "@context": "https://schema.org",
    "@type": (props.type ?? "LocalBusiness") as "LocalBusiness",
    name: props.name,
    description: props.description,
    url: props.url,
    telephone: props.telephone,
    address: {
      "@type": "PostalAddress",
      streetAddress: props.address.street,
      addressLocality: props.address.city,
      addressRegion: props.address.state,
      postalCode: props.address.postalCode,
      addressCountry: props.address.country,
    },
    geo: {
      "@type": "GeoCoordinates",
      latitude: props.geo.latitude,
      longitude: props.geo.longitude,
    },
    ...(props.priceRange && { priceRange: props.priceRange }),
    ...(props.openingHours && {
      openingHoursSpecification: props.openingHours.map((oh) => ({
        "@type": "OpeningHoursSpecification" as const,
        dayOfWeek: oh.dayOfWeek,
        opens: oh.opens,
        closes: oh.closes,
      })),
    }),
    ...(props.aggregateRating && {
      aggregateRating: {
        "@type": "AggregateRating" as const,
        ratingValue: props.aggregateRating.ratingValue,
        reviewCount: props.aggregateRating.reviewCount,
      },
    }),
  };

  return (
    <script type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
  );
}
```

### Ejemplo de uso

```tsx
<LocalBusinessSchema
  type="Restaurant"
  name="La Cocina de María"
  description="Restaurante dominicano con los mejores platos típicos"
  url="https://lacocinademmaria.com"
  telephone="+18095551234"
  address={{ street: "Av. Winston Churchill 100", city: "Santo Domingo",
             state: "DN", postalCode: "10100", country: "DO" }}
  geo={{ latitude: 18.4861, longitude: -69.9312 }}
  priceRange="$$"
  openingHours={[
    { dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], opens: "11:00", closes: "22:00" },
    { dayOfWeek: ["Saturday", "Sunday"], opens: "10:00", closes: "23:00" },
  ]}
  aggregateRating={{ ratingValue: 4.7, reviewCount: 342 }}
/>
```

---

## Reviews

- Responder TODAS las reviews (positivas y negativas)
- Reviews negativas: agradecer, reconocer, ofrecer solución
- Nunca pedir reviews a cambio de descuentos (viola TOS)
- Crear flow post-compra que invite a dejar review (no obligatorio)

Para multi-location, landing pages locales (`/servicios/[ciudad]`), y `Reviews` schema con review individuales: [`references/multi-location-pattern.md`](./references/multi-location-pattern.md)

---

## Verificación

| Qué verificar | Herramienta | Frecuencia |
|---------------|-------------|------------|
| GBP completo y correcto | Google Business dashboard | Mensual |
| NAP consistency | Manual audit | Trimestral |
| Knowledge Panel | Buscar nombre de negocio | Mensual |
| Local pack (3-pack) | Buscar "[servicio] + [ciudad]" | Semanal |
| `LocalBusiness` schema | Rich Results Test | Post-deploy |
| Reviews | GBP dashboard | Diario (responder) |
| Competitor local | Buscar keywords locales | Mensual |

---

## Referencias técnicas profundas

- [`references/multi-location-pattern.md`](./references/multi-location-pattern.md) — Multi-location config con páginas dinámicas, `Organization` schema con `subOrganization`, landing pages locales por ciudad, y `Reviews` schema con review individuales
