> **Historical module — full review pending.** Follow the [corrected discovery guidance](../../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# Core Web Vitals — Deep Dive

Optimización detallada de LCP, INP y CLS con ejemplos completos.

---

## Optimización LCP

LCP mide el tiempo que tarda el elemento más grande visible en renderizar. Causas principales de LCP lento:

### 1. Imágenes hero sin prioridad

```tsx
// app/page.tsx
import Image from "next/image";

export default function Home() {
  return (
    <Image
      src="/hero.webp"
      alt="Descripción del hero"
      width={1200}
      height={630}
      priority // Desactiva lazy loading, agrega preload
      sizes="100vw"
    />
  );
}
```

### 2. Fuentes que bloquean render

```tsx
// app/layout.tsx
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",          // Muestra fallback mientras carga
  preload: true,
  adjustFontFallback: true, // Reduce CLS de fuentes
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

### 3. Server Components para contenido crítico

```tsx
// app/products/[slug]/page.tsx (Server Component por defecto)
import { prisma } from "@/lib/prisma";

// Contenido crítico se renderiza en el servidor = LCP rápido
export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const product = await prisma.product.findUnique({ where: { slug } });

  return (
    <main>
      <h1>{product?.name}</h1>
      {/* Contenido above-the-fold renderizado en servidor */}
    </main>
  );
}
```

### 4. Preload de recursos críticos

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <head>
        <link rel="preload" href="/hero.webp" as="image" type="image/webp" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://cdn.example.com" />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

---

## Optimización INP

INP mide la latencia de la interacción más lenta del usuario. Aplica a clicks, taps, y keyboard input.

### 1. `useTransition` para operaciones pesadas

```tsx
"use client";
import { useTransition } from "react";

export function SearchFilter({ onFilter }: { onFilter: (q: string) => void }) {
  const [isPending, startTransition] = useTransition();

  return (
    <input
      type="search"
      onChange={(e) => {
        startTransition(() => {
          onFilter(e.target.value); // No bloquea el input
        });
      }}
      aria-busy={isPending}
    />
  );
}
```

### 2. Dynamic imports para componentes pesados

```tsx
import dynamic from "next/dynamic";

// Solo carga cuando se necesita
const HeavyChart = dynamic(() => import("@/components/chart"), {
  loading: () => <div className="h-64 animate-pulse rounded-lg bg-zinc-200" />,
  ssr: false, // No renderizar en servidor si es interactivo
});
```

### 3. Web Workers para cálculo pesado

```tsx
"use client";
import { useCallback } from "react";

export function DataProcessor() {
  const processData = useCallback((data: unknown[]) => {
    const worker = new Worker(new URL("../workers/process.ts", import.meta.url));
    worker.postMessage(data);
    worker.onmessage = (e) => {
      // Resultado sin bloquear main thread
      console.log(e.data);
      worker.terminate();
    };
  }, []);

  return <button onClick={() => processData([])}>Procesar</button>;
}
```

### 4. Virtualización para listas largas

Listas con cientos o miles de items deben virtualizarse para mantener INP bajo. Opciones: `react-window`, `@tanstack/react-virtual`, o `virtua` (más moderno).

---

## Optimización CLS

CLS mide cambios inesperados en el layout. Causas principales:

### 1. Dimensiones explícitas en imágenes y videos

```tsx
// SIEMPRE especificar width y height
<Image src="/photo.webp" alt="..." width={800} height={600} />

// Para videos
<video width={640} height={360} />

// Para iframes (embeds)
<iframe width={560} height={315} />
```

### 2. `font-display: swap` + `size-adjust`

```css
/* globals.css — Tailwind v4 */
@theme {
  --font-sans: "Inter", system-ui, sans-serif;
}

/* Si usás @font-face manual */
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter.woff2") format("woff2");
  font-display: swap;
  size-adjust: 107%; /* Ajustar al fallback para evitar CLS */
}
```

`next/font` aplica `adjustFontFallback: true` automáticamente — usalo en lugar de `@font-face` manual cuando sea posible.

### 3. Skeletons con dimensiones fijas

```tsx
// Skeleton que ocupa el mismo espacio que el contenido final
function ProductCardSkeleton() {
  return (
    <div className="w-full h-80 animate-pulse rounded-lg bg-zinc-200" />
  );
}
```

La regla: el skeleton debe ocupar **exactamente** el mismo espacio que el contenido cargado. Diferencia de altura entre skeleton y contenido = CLS.

### 4. Sin inserción dinámica above-the-fold

Banners, cookie bars, ads, popups que aparecen *después* del render inicial empujan el contenido y disparan CLS. Reservar espacio con un contenedor de altura fija o esconderlos hasta scroll.
