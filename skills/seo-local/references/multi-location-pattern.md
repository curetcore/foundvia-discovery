> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Multi-Location Pattern + Landing Pages Locales + Reviews

Para negocios con múltiples sucursales o que sirven varias ciudades sin oficina física.

---

## Multi-Location Config

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
    name: "Brand — Santo Domingo",
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
  // ... más locations
];
```

---

## Páginas dinámicas por location

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
    title: `${location.name} — Dirección, horario y contacto`,
    description: `Visitá ${location.name} en ${location.address.street}, ${location.address.city}. Horario, teléfono y cómo llegar.`,
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
      {/* Contenido único por location: mapa, equipo local, reviews locales */}
    </main>
  );
}
```

---

## Organization padre con subOrganization

Para que Google entienda que las locations pertenecen a una marca paraguas:

```tsx
// app/layout.tsx — schema de organización padre
import type { Organization, WithContext } from "schema-dts";

const orgJsonLd: WithContext<Organization> = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Brand",
  url: "https://brand.com",
  logo: "https://brand.com/logo.png",
  subOrganization: [
    {
      "@type": "LocalBusiness",
      name: "Brand — Santo Domingo",
      url: "https://brand.com/locations/santo-domingo",
    },
    {
      "@type": "LocalBusiness",
      name: "Brand — Santiago",
      url: "https://brand.com/locations/santiago",
    },
  ],
};
```

---

## Landing Pages Locales (sin oficina física)

Para negocios de servicio que cubren múltiples ciudades sin oficina (plomeros, electricistas, consultores).

### URL pattern

```
/servicios/[servicio]/[ciudad]
/plomeria/santo-domingo
/plomeria/santiago
/plomeria/punta-cana
```

### Reglas para contenido único

Cada página local DEBE tener contenido único (no solo cambiar el nombre de la ciudad):

- Mención de barrios/zonas específicas
- Testimonio de un cliente local
- Foto del equipo/trabajo en esa ciudad
- Estadística local relevante
- Referencia a landmarks locales
- Horario específico para esa zona

**Trampa común**: copiar el mismo template y hacer find/replace de la ciudad. Google detecta esto como contenido duplicado y desindexa todas las versiones.

---

## Reviews Schema (AggregateRating + Individual Reviews)

```tsx
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
    <script type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
  );
}
```

> **CRÍTICO**: nunca inventar reviews. Google penaliza fake review schema severamente. Las reviews deben venir de un sistema verificable (Google Reviews API, Yotpo, Trustpilot).
