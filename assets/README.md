# Foundvia visual assets

These assets identify Foundvia Discovery. The README has theme-specific covers and a vertical evidence → change → verification diagram. Essential instructions also remain selectable Markdown.

| Piece | Editable source | Static SVG | PNG export |
|---|---|---|---|
| Dark cover, 1200 × 760 | [Source](sources/discovery-cover-dark.svg) | [SVG](discovery-cover-dark.svg) | [PNG](discovery-cover-dark.png) |
| Light cover, 1200 × 760 | [Source](sources/discovery-cover-light.svg) | [SVG](discovery-cover-light.svg) | [PNG](discovery-cover-light.png) |
| Dark diagram, 640 × 780 | [Source](sources/discovery-path-dark.svg) | [SVG](discovery-path-dark.svg) | [PNG](discovery-path-dark.png) |
| Light diagram, 640 × 780 | [Source](sources/discovery-path-light.svg) | [SVG](discovery-path-light.svg) | [PNG](discovery-path-light.png) |
| GitHub social preview, 1280 × 640 | [Source](sources/social-preview.svg) | [SVG](social-preview.svg) | [PNG](social-preview.png) |
| Real report excerpt, 640 × 760 | [HTML view](report-example.html) | Not applicable | [Browser capture](report-example.png) |

## Provenance and export

The unchanged dark/light logos come from the [approved brand inventory](../docs/brand.md). The flame and original wordmark paths are preserved. Only the graphic canvas and surrounding copy differ between themes. The approved visual direction informs restrained zinc surfaces, legible connectors and written state labels; no private application code was copied.

Geist Version 1.401 is the unmodified Latin WOFF2 retained from the O2 public-font inventory. Its embedded copyright identifies The Geist Project Authors; the source font is licensed under [SIL OFL 1.1](fonts/OFL.txt), whose upstream text was checked at [vercel/geist-font](https://github.com/vercel/geist-font/blob/main/OFL.txt). The logo's existing wordmark outlines are not replaced with Geist.

The editable SVGs use text and the bundled font. Final SVGs outline that text, so GitHub rendering does not depend on installed fonts. There are no scripts, foreignObject elements or remote active resources in the graphics. The logo's image data is embedded locally.

Regenerate SVGs from the repository root with Python plus `fonttools[woff]` installed in a development environment:

```bash
python3 tools/build_brand_assets.py
```

Rasterize the final SVGs with any SVG renderer, preserving the declared dimensions. These tooling dependencies are only for asset authoring; the auditor still has no runtime dependencies. PNG exports are included for hosts that do not support SVG or theme switching.

The report capture is a browser screenshot of `report-example.html`. Its evidence and action are taken verbatim from the [O4 generated before report](../examples/discovery-lab/sample-results/before.json). It is explicitly a finding excerpt, not the full CLI report, and it demonstrates no traffic.

The social preview is a separate composition, under GitHub's 1 MB limit. It is prepared for a later approved repository setting change; inclusion here does not configure the live social card. [GitHub guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview).

Code/docs remain MIT; fonts retain OFL. Identifying brand use does not grant a separate trademark license. Do not rebrand your own product using these logos.
