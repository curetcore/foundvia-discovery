> **Historical module — full review pending.** Follow the [corrected discovery guidance](../skills/foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Local SEO

> Cubre Google Business Profile, NAP, schema local, multi-location, y landing pages locales.
> Stack: Next.js 16 App Router, React 19 RSC.

---

## Google Business Profile (GBP)

### Setup completo

| Campo | Requerido | Notas |
|-------|-----------|-------|
| Nombre del negocio | Si | Nombre legal, sin keywords extra |
| Categoría principal | Si | Lo mas específico posible |
| Categorías adicionales | No | Hasta 9, relevantes |
| Direccion | Si (si fisico) | Exacta, consistente con NAP |
| Area de servicio | Si (si no fisico) | Ciudades/regiones que sirves |
| Teléfono | Si | Número local preferido |
| Website | Si | URL de la pagina principal o local |
| Horario | Si | Incluyendo feriados |
| Descripción | Si | 750 chars, keyword natural al inicio |
| Fotos | Si | Min 10: exterior, interior, equipo, productos |
| Logo | Si | Cuadrado, fondo transparente |

### Optimización continua

| Accion | Frecuencia | Impacto |
|--------|------------|---------|
| Google Posts | Semanal | Medio |
| Responder reviews | Dentro de 24h | Alto |
| Fotos nuevas | Mensual | Medio |
| Q&A (preguntar y responder) | Inicial + mensual | Medio |
| Actualizar horarios feriados | Antes de cada feriado | Bajo |
| Verificar informacion | Mensual | Alto |

### Reviews

- Responder TODAS las reviews (positivas y negativas)
- Reviews negativas: agradecer, reconocer, ofrecer solucion
- Nunca pedir reviews a cambio de descuentos (viola TOS)
- Crear un flow post-compra que invite a dejar review

---

## NAP Consistency

**NAP** = Name, Address, Phone. Debe ser identico en TODOS los lugares.

### Donde verificar consistencia

| Plataforma | Prioridad |
|------------|-----------|
| Google Business Profile | Critica |
| Website (footer, contacto) | Critica |
| Apple Maps | Alta |
| Bing Places | Alta |
| Yelp | Media |
| Facebook | Media |
| Directorios locales | Media |
| Yellow Pages | Baja |

### Formato canonico

Elegir UN formato y usarlo siempre:

```
Curet LLC
123 Main St, Suite 100
Santo Domingo, DN 10100
+1 (809) 555-1234
```

**NO mezclar**: "123 Main Street" en un lugar y "123 Main St." en otro.

---

## LocalBusiness JSON-LD

### Componente genérico

```tsx
// components/local-business-schema.tsx
import type { LocalBusiness, WithContext } from "schema-dts";

interface LocalBusinessProps {
  type?: string; // "Restaurant", "ShoeStore", "Dentist", etc.
  name: string;
  description: string;
  url: string;
  telephone: string;
  email?: string;
  address: {
    street: string;
    city: string;
    state: string;
    postalCode: string;
    country: string;
  };
  geo: {
    latitude: number;
    longitude: number;
  };
  image?: string;
  priceRange?: string; // "$", "$$", "$$$", "$$$$"
  openingHours?: OpeningHours[];
  aggregateRating?: {
    ratingValue: number;
    reviewCount: number;
  };
}

interface OpeningHours {
  dayOfWeek: string | string[];
  opens: string; // "09:00"
  closes: string; // "18:00"
}

export function LocalBusinessSchema(props: LocalBusinessProps) {
  const jsonLd: WithContext<LocalBusiness> = {
    "@context": "https://schema.org",
    "@type": (props.type ?? "LocalBusiness") as "LocalBusiness",
    name: props.name,
    description: props.description,
    url: props.url,
    telephone: props.telephone,
    ...(props.email && { email: props.email }),
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
    ...(props.image && { image: props.image }),
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
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
    />
  );
}
```

### Uso

```tsx
<LocalBusinessSchema
  type="Restaurant"
  name="La Cocina de Maria"
  description="Restaurante dominicano con los mejores platos tipicos"
  url="https://lacocinademmaria.com"
  telephone="+18095551234"
  address={{
    street: "Av. Winston Churchill 100",
    city: "Santo Domingo",
    state: "DN",
    postalCode: "10100",
    country: "DO",
  }}
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

## Multi-Location Pattern

### Config

```ts
// lib/locations.ts
export interface Location {
  slug: string;
  name: string;
  address: {
    street: string;
    city: string;
    state: string;
    postalCode: string;
    country: string;
  };
  geo: { latitude: number; longitude: number };
  phone: string;
  hours: { dayOfWeek: string | string[]; opens: string; closes: string }[];
}

export const locations: Location[] = [
  {
    slug: "santo-domingo",
    name: "Brand - Santo Domingo",
    address: {
      street: "Av. Winston Churchill 100",
      city: "Santo Domingo",
      state: "DN",
      postalCode: "10100",
      country: "DO",
    },
    geo: { latitude: 18.4861, longitude: -69.9312 },
    phone: "+18095551234",
    hours: [
      { dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], opens: "09:00", closes: "18:00" },
    ],
  },
  // ... mas locations
];
```

### Páginas por location

```tsx
// app/locations/[slug]/page.tsx
import { locations } from "@/lib/locations";
import { LocalBusinessSchema } from "@/components/local-business-schema";
import { notFound } from "next/navigation";
import type { Metadata } from "next";

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return locations.map((loc) => ({ slug: loc.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const location = locations.find((l) => l.slug === slug);
  if (!location) return {};

  return {
    title: `${location.name} - Direccion, horario y contacto`,
    description: `Visita ${location.name} en ${location.address.street}, ${location.address.city}. Horario, teléfono y como llegar.`,
    alternates: {
      canonical: `/locations/${slug}`,
    },
  };
}

export default async function LocationPage({ params }: Props) {
  const { slug } = await params;
  const location = locations.find((l) => l.slug === slug);
  if (!location) return notFound();

  return (
    <main>
      <LocalBusinessSchema
        name={location.name}
        description={`Sucursal de Brand en ${location.address.city}`}
        url={`${process.env.NEXT_PUBLIC_BASE_URL}/locations/${slug}`}
        telephone={location.phone}
        address={location.address}
        geo={location.geo}
        openingHours={location.hours}
      />
      <h1>{location.name}</h1>
      {/* Contenido unico por location: mapa, equipo local, reviews locales */}
    </main>
  );
}
```

### Organization padre

```tsx
// app/layout.tsx - schema de organizacion padre
import type { Organization, WithContext } from "schema-dts";

const orgJsonLd: WithContext<Organization> = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Brand",
  url: "https://brand.com",
  logo: "https://brand.com/logo.png",
  // Sub-organizations (locations)
  subOrganization: [
    {
      "@type": "LocalBusiness",
      name: "Brand - Santo Domingo",
      url: "https://brand.com/locations/santo-domingo",
    },
    {
      "@type": "LocalBusiness",
      name: "Brand - Santiago",
      url: "https://brand.com/locations/santiago",
    },
  ],
};
```

---

## Reviews Integration

### AggregateRating + Individual Reviews

```tsx
// components/reviews-schema.tsx
import type { Product, WithContext } from "schema-dts";

interface Review {
  author: string;
  rating: number;
  text: string;
  date: string;
}

interface ReviewsSchemaProps {
  productName: string;
  averageRating: number;
  reviewCount: number;
  reviews: Review[];
}

export function ReviewsSchema(props: ReviewsSchemaProps) {
  const jsonLd: WithContext<Product> = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: props.productName,
    aggregateRating: {
      "@type": "AggregateRating",
      ratingValue: props.averageRating,
      reviewCount: props.reviewCount,
      bestRating: 5,
      worstRating: 1,
    },
    review: props.reviews.slice(0, 5).map((r) => ({
      "@type": "Review" as const,
      author: { "@type": "Person" as const, name: r.author },
      reviewRating: {
        "@type": "Rating" as const,
        ratingValue: r.rating,
        bestRating: 5,
      },
      reviewBody: r.text,
      datePublished: r.date,
    })),
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
    />
  );
}
```

---

## Local Landing Pages

Para negocios de servicio que cubren multiples ciudades sin oficina fisica.

### URL pattern

```
/servicios/[servicio]/[ciudad]
/plomeria/santo-domingo
/plomeria/santiago
/plomeria/punta-cana
```

### Reglas para contenido unico

Cada pagina local DEBE tener contenido unico (no solo cambiar el nombre de la ciudad):

- Mencion de barrios/zonas especificas
- Testimonial de un cliente local
- Foto del equipo/trabajo en esa ciudad
- Estadistica local relevante
- Referencia a landmarks locales
- Horario específico para esa zona

---

## Verificación

| Que verificar | Herramienta | Frecuencia |
|---------------|-------------|------------|
| GBP completo y correcto | Google Business dashboard | Mensual |
| NAP consistency | Manual audit | Trimestral |
| Knowledge Panel | Buscar nombre de negocio | Mensual |
| Local pack (3-pack) | Buscar "[servicio] + [ciudad]" | Semanal |
| LocalBusiness schema | Rich Results Test | Post-deploy |
| Reviews | GBP dashboard | Diario (responder) |
| Competitor local | Buscar keywords locales | Mensual |
