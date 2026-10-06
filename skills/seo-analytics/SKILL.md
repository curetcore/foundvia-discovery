---
name: seo-analytics
description: Configura monitoreo SEO completo — Google Search Console (GSC), Core Web Vitals RUM con web-vitals + PostHog, AI referral tracking (ChatGPT, Perplexity, Claude), rank tracking, competitor analysis y cadencia de auditorías. Use this skill whenever the user asks about Search Console setup, GSC reports, web-vitals tracking, RUM monitoring, AI traffic tracking, ChatGPT referrals, rank tracking, SEO audit cadence, or competitor SEO analysis — even if they don't say "analytics".
---

> **Historical module — full review pending.** Follow the [corrected discovery guidance](../foundvia-discovery/references/discovery.md) before applying these examples. Do not invent dates, treat training bots as search bots, require llms.txt/FAQ markup, count all Bing as Copilot, or use word counts as ranking rules.

# SEO Analytics

Cubre Google Search Console, Core Web Vitals monitoring, AI referral tracking, rank tracking y cadencia de auditorías. Stack: Next.js 16, PostHog, web-vitals.

---

## Cuándo invocar este skill

- Setup inicial de Google Search Console (verificación, sitemap)
- Implementar web-vitals RUM (real user monitoring)
- Trackear tráfico desde ChatGPT/Perplexity/Claude (AI referrals)
- Configurar rank tracking de keywords clave
- Análisis competitivo (content gap, keywords)
- Definir cadencia de auditorías SEO

Para fixear problemas detectados en GSC (CWV, indexación), usar `seo-technical`. Para auditorías automatizadas con CLI, usar `seo-audit-website`.

---

## Reglas clave

1. **Verificar GSC el día 1 del proyecto** — sin GSC, ranking decisions son a ciegas
2. **RUM > Lighthouse** — Lighthouse mide en condiciones ideales, RUM mide a usuarios reales
3. **Trackear AI referrers explícitamente** — Google Analytics no los etiqueta bien por default
4. **Auditar semanal lo crítico, mensual lo táctico, trimestral lo estratégico**
5. **Comparar periodos en GSC** — los números absolutos sin comparación son ruido

---

## Google Search Console Setup

### Verificación

| Método | Mejor para |
|--------|------------|
| DNS TXT record | Dominios en Cloudflare/Vercel |
| HTML file upload | Cualquier hosting |
| Meta tag | Si no tenés acceso a DNS |
| Google Analytics | Si ya tenés GA4 |
| Google Tag Manager | Si ya tenés GTM |

### Post-verificación

1. Enviar sitemap: `https://tudominio.com/sitemap.xml`
2. Verificar indexación con URL Inspection tool
3. Solicitar indexación de páginas críticas
4. Configurar notificaciones por email

---

## Reports clave en GSC

| Report | Qué muestra | Frecuencia | Acción |
|--------|-------------|------------|--------|
| **Performance** | Clicks, impressions, CTR, position | Semanal | Identificar keywords ganando/perdiendo |
| **Coverage / Indexing** | Páginas indexadas vs excluidas | Semanal | Fixear errores de indexación |
| **Core Web Vitals** | LCP, INP, CLS por URL | Semanal | Optimizar páginas en rojo |
| **Sitemaps** | Estado de sitemaps enviados | Post-deploy | Verificar que se procesó |
| **Links** | Top linking sites, top linked pages | Mensual | Identificar oportunidades |
| **Manual Actions** | Penalizaciones manuales | Semanal | Resolver inmediatamente |
| **Security Issues** | Malware, hacking | Semanal | Resolver inmediatamente |
| **URL Inspection** | Estado de URL individual | Bajo demanda | Debug de indexación |

---

## Métricas clave

### Primarias

| Métrica | Target | Cómo mejorar |
|---------|--------|-------------|
| Organic clicks | Crecimiento MoM | Mejorar CTR (titles, descriptions) |
| Impressions | Crecimiento MoM | Más contenido, más keywords |
| Average CTR | > 3% (depende de posición) | Mejorar titles y descriptions |
| Average position | < 10 para keywords target | Contenido más profundo, más backlinks |
| Indexed pages | = páginas publicadas | Sitemap correcto, sin errores |

### De negocio

| Métrica | Fórmula | Target |
|---------|---------|--------|
| Organic traffic share | Organic / Total × 100 | > 40% para content sites |
| Organic conversion rate | Conversions / Organic sessions | Depende del vertical |
| Revenue from organic | Transacciones orgánicas | Crecimiento trimestral |
| Cost per organic acquisition | SEO investment / Organic conversions | Decrecimiento |

---

## Core Web Vitals Monitoring (RUM)

### `web-vitals` + PostHog

```ts
// lib/web-vitals.ts
import { onCLS, onINP, onLCP, onFCP, onTTFB } from "web-vitals";
import type { Metric } from "web-vitals";

function sendToAnalytics(metric: Metric) {
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
// app/web-vitals-reporter.tsx
"use client";
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

Crear dashboard con estos gráficos:

| Gráfico | Tipo | Filtro |
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

```ts
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

### Lista de keywords (estructura)

| Categoría | Ejemplos | Frecuencia tracking |
|-----------|----------|---------------------|
| Branded | "miapp", "miapp login" | Semanal |
| Non-branded head | "analytics ecommerce" | Semanal |
| Non-branded long tail | "cómo medir conversion rate ecommerce" | Quincenal |
| Local | "analytics ecommerce dominicana" | Semanal |
| Competitor | "[competidor] alternativa" | Mensual |

### GSC Performance como rank tracker (gratis)

```
GSC > Performance > Queries
- Filtrar por página específica
- Comparar periodos (28d vs 28d anterior)
- Exportar CSV para tracking histórico
```

---

## Competitor Analysis

### Áreas a analizar

| Área | Qué buscar | Herramienta |
|------|-----------|-------------|
| Keywords | Qué keywords rankean | brave-search MCP, Ahrefs |
| Content gap | Temas que cubren y vos no | Ahrefs Content Gap |
| Technical | Speed, CWV, mobile | PageSpeed Insights |
| Backlinks | De dónde reciben links | Ahrefs, Moz |
| Schema | Qué tipos de schema usan | Rich Results Test |
| AI presence | Aparecen en ChatGPT/Perplexity | Preguntar directamente |

### Content gap analysis (workflow)

1. Listar competidores (3-5)
2. Extraer sus top 50 páginas orgánicas
3. Categorizar por tema
4. Identificar temas que cubren y vos no
5. Priorizar por volumen de búsqueda
6. Crear content briefs para los gaps (ver `seo-content-strategy`)

---

## SEO Audit Cadence

### Semanal (15 min)

- [ ] Revisar GSC Performance (clicks, position)
- [ ] Verificar Core Web Vitals en GSC
- [ ] Revisar errores de indexación
- [ ] Chequear manual actions

### Mensual (1 hora)

- [ ] Análisis de keywords (ganando/perdiendo)
- [ ] Revisar contenido con CTR bajo
- [ ] Verificar NAP consistency (si local)
- [ ] Actualizar contenido con datos viejos
- [ ] Revisar backlinks nuevos/perdidos
- [ ] Chequear AI referral traffic

### Trimestral (4 horas)

- [ ] Audit técnico completo (squirrelscan — ver `seo-audit-website`)
- [ ] Content gap analysis vs competidores
- [ ] E-E-A-T review de páginas principales
- [ ] Schema audit (todos los tipos)
- [ ] Internal linking audit
- [ ] Update content clusters

### Semestral (1 día)

- [ ] Keyword research completo
- [ ] Content strategy review
- [ ] Competitor deep analysis
- [ ] GBP optimization (si local)
- [ ] `llms.txt` y `robots.txt` review
- [ ] Performance benchmark completo

### Anual

- [ ] Estrategia SEO completa para el año
- [ ] Presupuesto de contenido
- [ ] Evaluar herramientas y stack
- [ ] Training del equipo en cambios de Google

---

## Verificación

| Qué verificar | Herramienta | Frecuencia |
|---------------|-------------|------------|
| GSC accesible y verificado | GSC dashboard | Única vez |
| Sitemap enviado y procesado | GSC Sitemaps | Post-deploy |
| `web-vitals` RUM flowing | PostHog dashboard | Semanal |
| AI referral tracking | PostHog events | Mensual |
| Audit schedule cumplido | Checklist interno | Mensual |
| Competitor monitoring | brave-search + manual | Trimestral |
