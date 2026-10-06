# Foundvia Discovery

Proyecto open source de [Foundvia](https://foundvia.dev) para ayudar a que tu SaaS sea descubierto en Google y ChatGPT.

## Empieza con tu sitio

```bash
git clone https://github.com/ronaldships/foundvia-discovery.git
cd foundvia-discovery
python3 skills/foundvia-discovery/scripts/discovery_audit.py https://tu-sitio.com
```

Necesitas Python 3.10+. Sin API keys ni dependencias externas.

Recibirás problemas observados, evidencia y el próximo paso. El auditor revisa el HTML inicial, robots.txt y un sitemap; no confirma indexación ni ejecuta JavaScript.

## Úsalo como skill

```bash
npx skills add ronaldships/foundvia-discovery --skill foundvia-discovery
```

Pídele a tu agente:

> Usa foundvia-discovery para auditar mi SaaS, corregir los bloqueos en mi repo y proponer una página útil para buscar mis primeras 100 visitas. Separa los cambios locales del despliegue.

100 visitas es una meta medible, no una promesa. Cuenta sesiones de Google orgánico y ChatGPT por separado; no confundas visitas con usuarios que pagan.

La entrada principal y la nueva skill están en inglés. Los módulos originales en español siguen disponibles y muestran su estado de revisión en el [README principal](README.md#advanced-modules).

[Guía en inglés](playbook/first-100-visits.md) · [Cómo funciona el auditor](docs/auditor.md) · [Comparación de skills](docs/skill-review.md) · [Contribuir](CONTRIBUTING.md)
