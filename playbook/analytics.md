> **Historical module — full review pending.** Follow the [corrected discovery guidance](../skills/foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# SEO Analytics

> Cubre Google Search Console, Core Web Vitals monitoring, AI referral tracking, rank tracking, y cadencia de auditorías.
> Integraciones: PostHog MCP, web-vitals library, GSC API.

---

## Google Search Console Setup

### Verificación

| Metodo | Mejor para |
|--------|------------|
| DNS TXT record | Dominios en Cloudflare/Vercel |
| HTML file upload | Cualquier hosting |
| Meta tag | Si no tienes acceso a DNS |
| Google Analytics | Si ya tienes GA4 |
| Google Tag Manager | Si ya tienes GTM |

### Post-verificación

1. Enviar sitemap: `https://tudominio.com/sitemap.xml`
2. Verificar indexacion: URL Inspection tool
3. Solicitar indexacion de páginas criticas
4. Configurar notificaciones por email

---

## Key Reports en GSC

| Report | Que muestra | Frecuencia de revision | Accion |
|--------|-------------|----------------------|--------|
| **Performance** | Clicks, impressions, CTR, position | Semanal | Identificar keywords ganando/perdiendo |
| **Coverage/Indexing** | Páginas indexadas vs excluidas | Semanal | Fixear errores de indexacion |
| **Core Web Vitals** | LCP, INP, CLS por URL | Semanal | Optimizar páginas en rojo |
| **Sitemaps** | Estado de sitemaps enviados | Post-deploy | Verificar que se proceso |
| **Links** | Top linking sites, top linked pages | Mensual | Identificar oportunidades |
| **Manual Actions** | Penalizaciones manuales | Semanal | Resolver inmediatamente |
| **Security Issues** | Malware, hacking | Semanal | Resolver inmediatamente |
| **URL Inspection** | Estado de URL individual | Bajo demanda | Debug de indexacion |
| **Removals** | URLs removidas temporalmente | Mensual | Limpieza |

---

## Métricas Clave

### Métricas primarias

| Métrica | Target | Como mejorar |
|---------|--------|-------------|
| Organic clicks | Crecimiento MoM | Mejorar CTR (titles, descriptions) |
| Impressions | Crecimiento MoM | Mas contenido, mas keywords |
| Average CTR | > 3% (depende de posicion) | Mejorar titles y descriptions |
| Average position | < 10 para keywords target | Contenido mas profundo, mas backlinks |
| Indexed pages | = páginas publicadas | Sitemap correcto, sin errores |

### Métricas de negocio

| Métrica | Formula | Target |
|---------|---------|--------|
| Organic traffic share | Organic / Total * 100 | > 40% para content sites |
| Organic conversion rate | Conversions / Organic sessions | Depende del vertical |
| Revenue from organic | Transacciones organicas | Crecimiento trimestral |
| Cost per organic acquisition | SEO investment / Organic conversions | Decrecimiento |

---

## Core Web Vitals Monitoring (RUM)

### web-vitals + PostHog

```tsx
// lib/web-vitals.ts
import { onCLS, onINP, onLCP, onFCP, onTTFB } from "web-vitals";
import type { Metric } from "web-vitals";

function sendToAnalytics(metric: Metric) {
  // PostHog event
  if (typeof window !== "undefined" && window.posthog) {
    window.posthog.capture("web_vital", {
      name: metric.name,
      value: metric.value,
      rating: metric.rating, // "good" | "needs-improvement" | "poor"
      delta: metric.delta,
      id: metric.id,
      navigationType: metric.navigationType,
      url: window.location.href,
    });
  }

  // Tambien loguear en consola en dev
  if (process.env.NODE_ENV === "development") {
    console.log(`[CWV] ${metric.name}: ${metric.value} (${metric.rating})`);
  }
}

export function reportWebVitals() {
  onCLS(sendToAnalytics);
  onINP(sendToAnalytics);
  onLCP(sendToAnalytics);
  onFCP(sendToAnalytics);
  onTTFB(sendToAnalytics);
}
```

### Uso en layout

```tsx
// app/layout.tsx
"use client"; // Solo el componente de tracking

import { useEffect } from "react";
import { reportWebVitals } from "@/lib/web-vitals";

export function WebVitalsReporter() {
  useEffect(() => {
    reportWebVitals();
  }, []);

  return null;
}
```

```tsx
// app/layout.tsx (Server Component)
import { WebVitalsReporter } from "./web-vitals-reporter";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        {children}
        <WebVitalsReporter />
      </body>
    </html>
  );
}
```

### Dashboard PostHog

Crear dashboard con estos graficos:

| Grafico | Tipo | Filtro |
|---------|------|--------|
| LCP distribution | Histogram | name = "LCP" |
| INP distribution | Histogram | name = "INP" |
| CLS distribution | Histogram | name = "CLS" |
| CWV by page | Table | Group by URL |
| CWV trend | Line | Last 30 days |
| Poor CWV % | Number | rating = "poor" |

---

## AI Referral Tracking

### Identificar tráfico de AI search

| Referrer | Source |
|----------|--------|
| `chatgpt.com` | ChatGPT web |
| `chat.openai.com` | ChatGPT legacy |
| `perplexity.ai` | Perplexity |
| `you.com` | You.com |
| `bing.com/chat` | Copilot |
| `gemini.google.com` | Gemini |
| `claude.ai` | Claude |

### Tracking con PostHog

```tsx
// lib/ai-referral.ts
export function trackAIReferral() {
  if (typeof window === "undefined") return;

  const referrer = document.referrer;
  const aiSources = [
    { domain: "chatgpt.com", source: "chatgpt" },
    { domain: "chat.openai.com", source: "chatgpt" },
    { domain: "perplexity.ai", source: "perplexity" },
    { domain: "you.com", source: "you" },
    { domain: "bing.com", source: "copilot" },
    { domain: "gemini.google.com", source: "gemini" },
    { domain: "claude.ai", source: "claude" },
  ];

  const match = aiSources.find((s) => referrer.includes(s.domain));

  if (match && window.posthog) {
    window.posthog.capture("ai_referral", {
      source: match.source,
      referrer,
      landing_page: window.location.pathname,
    });
  }
}
```

---

## Rank Tracking

### Keyword list structure

| Categoría | Ejemplos | Frecuencia de tracking |
|-----------|----------|----------------------|
| Branded | "tuapp", "tuapp login" | Semanal |
| Non-branded head | "analytics ecommerce" | Semanal |
| Non-branded long tail | "cómo medir conversion rate ecommerce" | Quincenal |
| Local | "analytics ecommerce dominicana" | Semanal |
| Competitor | "[competidor] alternativa" | Mensual |

### GSC Performance como rank tracker

```
GSC > Performance > Queries
- Filtrar por pagina específica
- Comparar periodos (28d vs 28d anterior)
- Exportar CSV para tracking histórico
```

---

## Competitor Analysis

### Areas a analizar

| Area | Que buscar | Herramienta |
|------|-----------|-------------|
| Keywords | Que keywords rankean | brave-search MCP, Ahrefs |
| Content gap | Temas que cubren y tu no | Ahrefs Content Gap |
| Technical | Speed, CWV, mobile | PageSpeed Insights |
| Backlinks | De donde reciben links | Ahrefs, Moz |
| Schema | Que tipos de schema usan | Rich Results Test |
| AI presence | Aparecen en ChatGPT/Perplexity | Preguntar directamente |

### Content gap analysis

```
1. Listar competidores (3-5)
2. Extraer sus top 50 páginas organicas
3. Categorizar por tema
4. Identificar temas que cubren y tu no
5. Priorizar por volumen de búsqueda
6. Crear content briefs para los gaps
```

---

## SEO Audit Cadence

### Semanal (15 min)

- [ ] Revisar GSC Performance (clicks, position)
- [ ] Verificar Core Web Vitals en GSC
- [ ] Revisar errores de indexacion
- [ ] Chequear manual actions

### Mensual (1 hora)

- [ ] Análisis de keywords (ganando/perdiendo)
- [ ] Revisar contenido con CTR bajo
- [ ] Verificar NAP consistency (si local)
- [ ] Actualizar contenido con datos viejos
- [ ] Revisar backlinks nuevos/perdidos
- [ ] Chequear AI referral traffic

### Trimestral (4 horas)

- [ ] Audit técnico completo (squirrelscan)
- [ ] Content gap analysis vs competidores
- [ ] E-E-A-T review de páginas principales
- [ ] Schema audit (todos los tipos)
- [ ] Internal linking audit
- [ ] Update content clusters

### Semestral (1 dia)

- [ ] Keyword research completo
- [ ] Content strategy review
- [ ] Competitor deep analysis
- [ ] GBP optimization (si local)
- [ ] llms.txt y robots.txt review
- [ ] Performance benchmark completo

### Anual

- [ ] Estrategia SEO completa para el año
- [ ] Presupuesto de contenido
- [ ] Evaluar herramientas y stack
- [ ] Training del equipo en cambios de Google

---

## Verificación

| Que verificar | Herramienta | Frecuencia |
|---------------|-------------|------------|
| GSC accesible y verificado | GSC dashboard | Unica vez |
| Sitemap enviado y procesado | GSC Sitemaps | Post-deploy |
| web-vitals RUM flowing | PostHog dashboard | Semanal |
| AI referral tracking | PostHog events | Mensual |
| Audit schedule cumplido | Checklist interno | Mensual |
| Competitor monitoring | brave-search + manual | Trimestral |
