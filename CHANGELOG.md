# Changelog

Todos los cambios notables de este repo se documentan acá.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

### Added
- Standalone HTML audit export with embedded Geist, responsive layout, status filters, expandable evidence, print styles and safe escaping; three regression tests.
- Opt-in bounded child-sitemap inspection (`--sitemap-children 0–5`) with observed membership and explicit partial/error coverage; 10 regression tests.
- Recorded live Codex tool-use smoke checks on two public projects and an inaccessible control, with requests, responses, helper output, and catalog-warning disclosure.
- Report coverage summary, skipped HTML checks, and optional `--require-complete` exit status for automation.
- Beginner troubleshooting, clearer status tables, reproducible issue form, and pull request template.
- Offline local-link/package checks and CI coverage for Python 3.10 and 3.14.

### Fixed
- Inaccessible resources now retain the underlying error and group unchecked findings instead of repeated UNKNOWN sections.
- Canonical and sitemap membership comparisons normalize equivalent root URLs without collapsing non-root paths or query strings.
- Simplified first-run and skill installation commands; historical evaluation records are explicitly identified as snapshots.


## [3.0.0] — 2026-10-06

### Added
- Foundvia Discovery branding, English landing page, Spanish introduction, visual discovery path, and first-100-visits guide.
- Self-contained `foundvia-discovery` skill with standard-library Python audit helper, scoped findings, JSON output, and controlled HTTP tests.
- Public skill comparison with pinned sources and honest evaluation status; behavioral cases, community templates, and distribution drafts.

### Changed
- Corrected search/training crawler separation, optional llms.txt guidance, and unsupported AI/FAQ claims.
- Explicitly marked remaining legacy chapters and references as pending full review.
- Updated agent routing, installation instructions, and contribution guidance.

### Removed / migration
- **Breaking:** hash-generated date helpers (`slugToDates`, `slugToPublishedDate`, `slugToModifiedDate`) removed. Use `contentDates` with actual source records; see `playbook/slug-date-distribution.md`.
- Removed unverified growth forecasts from the landing page.

## [2.0.0] — 2026-05-10

**BREAKING**: refactor completo a arquitectura tri-capa (playbook + agent + skills).

### Added

- **`agents/seo-marketing.md`** — agente decision-framework autocontenido con matriz de delegación a 10 sub-skills. Instalable en `~/.claude/agents/` para usar con Claude Code.
- **`skills/`** — 10 sub-skills instalables con `SKILL.md` + frontmatter YAML válido + `references/` (cuando aplica) + `scripts/` (cuando aplica):
  - `seo-technical` — CWV, crawlability, security headers (3 references)
  - `seo-on-page` — meta tags, OG, internal linking (3 references)
  - `seo-ai-geo` ⭐ — llms.txt, AI bots, citabilidad (3 references)
  - `seo-content-strategy` — BLUF, clusters, E-E-A-T (1 reference)
  - `seo-local` — GBP, NAP, multi-location (1 reference)
  - `seo-analytics` — GSC, RUM, AI tracking (sin references)
  - `seo-growth-engine` ⭐ — niche pages, tools, comparativas, blog, outreach (5 references)
  - `seo-slug-dates` — anti-batch signal (`scripts/dates.ts` bundled)
  - `seo-nextjs-implementation` — JSON-LD generators (`scripts/seo.ts` bundled)
  - `seo-audit-website` — squirrelscan CLI (con attribution clara al upstream)
- **`playbook/`** — 9 `.md` educacionales movidos a carpeta dedicada (sin frontmatter, para humanos)
- **`examples/`** — placeholder para casos reales de Linkship/Karrito (próxima versión)
- **Descriptions pushy** en todos los skills siguiendo el patrón "Use this skill whenever..." del skill-creator de Anthropic

### Changed

- **`seo.ts`** — env-driven (`NEXT_PUBLIC_SITE_*`) en lugar de hardcoded. Eliminado todo branding de proyecto privado. Movido a `skills/seo-nextjs-implementation/scripts/seo.ts`.
- **README.md** — actualizada estructura del repo y links cruzados a `playbook/*.md`
- **Acentos correctos en todos los `.md`** del playbook (Técnico, métrica, búsqueda, etc.)
- **Headers internos limpios** — eliminada la línea "Skill del agente `seo-marketing`" de los archivos del playbook (era jerga interna que no aplica al lector externo)
- **Conteo de pilares reconciliado** — `_index.md` y README dicen "10 pilares" consistente
- **Growth Engine: 5 → 6 pilares** — corregido el diagrama ASCII para incluir Outreach que ya estaba como Pilar 6
- **`bg-base-200` y `text-base-content/*`** — reemplazados por clases Tailwind v4 puras (`bg-zinc-200`, `text-zinc-500`)

### Removed

- **`SKILL.md`** del root — consolidado en `skills/seo-nextjs-implementation/SKILL.md`
- **`seo.ts`** del root — movido a `skills/seo-nextjs-implementation/scripts/seo.ts`
- **`generateBookJsonLd`** y **`generateBlogListJsonLd`** — específicos de un proyecto privado, eliminados
- **Referencia a `ECOSYSTEM.md`** en `_index.md` — el archivo nunca existió
- **Hardcoded "LectorAI"** en `seo.ts` — todas las referencias eliminadas

### Migration guide (v1 → v2)

Si estabas usando `seo.ts` desde la raíz del repo:

1. **Actualizar imports**: `seo.ts` ahora vive en `skills/seo-nextjs-implementation/scripts/seo.ts`
2. **Configurar env vars**: agregar `NEXT_PUBLIC_SITE_NAME`, `NEXT_PUBLIC_SITE_URL`, etc. (ver `SEO_CONFIG`)
3. **Si usabas `generateBookJsonLd`**: lo eliminamos. Replicalo con `generateProductJsonLd` o crealo manualmente
4. **Si usabas `generateBlogListJsonLd`**: lo eliminamos. Crealo manualmente con el patrón de `Blog` schema

Si estabas leyendo los `.md` desde la raíz:

- Todos están ahora en `playbook/` con el mismo nombre. Los links del README ya apuntan ahí.

Si querés instalar el agente y skills en Claude Code:

```bash
# Copiar agente
cp agents/seo-marketing.md ~/.claude/agents/

# Copiar skills
cp -r skills/seo-* ~/.claude/skills/
```

Después en Claude Code, el agente `seo-marketing` se puede invocar con la matriz de decisión completa.

---

## [1.0.0] — 2026-04-XX

### Added

- Versión inicial del playbook con 11 archivos `.md` planos en la raíz
- `seo.ts` con generators de JSON-LD
- README con tabla de pilares y guía de uso
- Prompt para LLMs (Claude/ChatGPT/Cursor) en README

### Notas

Esta versión publicó el contenido tal cual estaba en uso interno en Curetcore. La v2.0.0 lo refactoriza para uso público real.
