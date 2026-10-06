<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/discovery-cover-dark.svg">
  <img src="assets/discovery-cover-light.svg" alt="Foundvia Discovery. Publicaste tu producto. Ahora ayuda a que lo encuentren. Audita, corrige y verifica." width="1200">
</picture>

# Foundvia Discovery

**Detecta qué bloquea tus páginas públicas en Google y ChatGPT. Corrige un problema comprobado y mide el siguiente paso.**

Un toolkit open source de [Foundvia](https://foundvia.dev), creado por [Ronaldo Paulino](https://x.com/ronaldships). Incluye un auditor pequeño en Python, un skill para tu asistente y una guía para tus primeras 100 visitas.

[Empieza aquí](#ejecuta-tu-primera-auditoría) · [Primeras 100 visitas](playbook/first-100-visits.es.md) · [English](README.md)

**Python 3.10+ · Sin dependencias de ejecución · [Código y documentación MIT](LICENSE)**

## Ejecuta tu primera auditoría

Clona o descarga este repositorio con el botón **Code** de GitHub. Abre la carpeta descargada en tu terminal. Necesitas Python instalado; comprueba su versión con `python3 --version`.

Revisa **una página que quieras hacer pública**. Cambia la URL por la tuya:

```bash
python3 discovery.py audit https://example.com > audit.md
```

Abre `audit.md` en tu editor. Cada hallazgo incluye **evidencia, siguiente acción y cómo verificarla**. No necesitas cuenta ni API key.

El auditor lee la respuesta inicial, las reglas de robots y un sitemap. No ejecuta JavaScript, no se hace pasar por un crawler ni confirma indexación, posiciones o visitas. [Opciones y límites →](docs/auditor.md)

Para abrir el resultado en el navegador, exporta un archivo HTML:

```bash
python3 discovery.py audit https://example.com --format html > audit.html
```

Abre `audit.html`, filtra los hallazgos y despliega cada uno para leer la evidencia y el siguiente paso. Funciona sin conexión y trae su fuente incluida. La interfaz del reporte está en inglés.

## Entiende tu resultado

| Etiqueta | Qué significa | Siguiente paso |
|---|---|---|
| **BLOCK** | Una respuesta o directiva observada necesita revisión | Confirma si es intencional antes de cambiarla |
| **WARN** | Algo difiere de la configuración esperada | Revisa la evidencia; no demuestra pérdida de posiciones |
| **UNKNOWN** | La herramienta no pudo completar la revisión | Lee el error de acceso y vuelve a probar o usa otra fuente |
| **INFO** | Contexto o un límite de la revisión | No lo cuentes como una comprobación aprobada |
| **PASS** | No se observó un problema en esa comprobación | No confirma indexación ni tráfico |

Cada reporte empieza con un resumen de cobertura. Si no pudo leer el HTML, enumera las comprobaciones omitidas. Para automatizaciones, añade `--fail-on-block --require-complete` y rechaza tanto bloqueos observados como reportes incompletos. [Solución de problemas →](docs/troubleshooting.md)

### ¿Tu sitemap es un índice?

Revisa hasta tres archivos hijos para comprobar si incluyen la página auditada:

```bash
python3 discovery.py audit https://example.com --sitemap-children 3
```

El reporte indica dónde encontró la URL y si la cobertura es parcial o algún archivo falló. Estar en el sitemap no confirma indexación. [Cómo funciona →](docs/auditor.md#check-a-sitemap-indexs-children)

## Comprueba una corrección real

Prueba el ejercicio local:

```bash
python3 discovery.py practice
```

Abre `outputs-local/discovery-lab/before.md` y después `after.md`. El servidor temporal funciona en tu computadora y se cierra al terminar.

**Hallazgo del ejercicio:** una guía pública tiene una etiqueta HTML `noindex`. Esta captura muestra el hallazgo de Googlebot del reporte guardado, en una vista legible. [Reporte generado completo →](examples/discovery-lab/sample-results/before.md)

<img src="assets/report-example.png" alt="Extracto real del ejercicio local: bloqueo noindex para Googlebot; evidencia meta robots: noindex. Confirmar si la exclusión es intencional y quitarla solo en páginas públicas para búsqueda." width="640">

1. **Antes:** bloqueos noindex para Googlebot y OAI-SearchBot.
2. **Cambio:** quitar solo la etiqueta accidental.
3. **Después:** sin bloqueos observados en la página corregida ni al volver a auditarla.

GPTBot sigue bloqueado: entrenamiento y acceso para búsquedas son decisiones distintas. El ejercicio demuestra la corrección técnica; no demuestra crecimiento orgánico. [Cómo reproducirlo →](examples/discovery-lab/README.md)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/discovery-path-dark.svg">
  <img src="assets/discovery-path-light.svg" alt="Lee la evidencia, haz un cambio autorizado y vuelve a auditar para comparar. Un reporte sin bloqueos no prueba visitas." width="640">
</picture>

## Úsalo con tu asistente de código

Instala **solo el skill principal** con [Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add ronaldships/foundvia-discovery --skill foundvia-discovery
```

Después pídele:

> Usa foundvia-discovery para auditar https://TU-SITIO-PUBLICO.com. Muéstrame la evidencia y propón una corrección pequeña en mi repo. Conserva las áreas privadas y la preferencia de entrenamiento. Verifica el cambio y deja el despliegue separado.

El skill ayuda a revisar, corregir, planear una página útil y medir cuando tiene herramientas, evidencia y autorización. El auditor Python también funciona por su cuenta.

La instalación local por copia y la evaluación con casos suministrados se probaron con Codex CLI. Las instrucciones para otros agentes no son una certificación universal. En 48 respuestas evaluadas, tanto el skill como el modelo solo pasaron los criterios; no se demostró mejora en la tasa de aciertos. [Instalación →](docs/install.md) · [Evidencia →](docs/quality-results.md)

## Avanza hacia tus primeras 100 visitas

Empieza con una página útil y una pregunta real de tu audiencia.

1. Revisa el acceso y corrige un bloqueo accidental.
2. Responde la pregunta con un ejemplo probado.
3. Aporta donde sea relevante y esté permitido.
4. Revisa sesiones y resultados del producto cada semana.

La meta es **100 sesiones medidas desde Google orgánico y referencias observadas de ChatGPT**, separadas y luego sumadas. No son personas únicas, registros ni ventas. No hay plazo prometido ni respaldo de Google u OpenAI.

[Guía para empezar →](playbook/first-100-visits.es.md) · [Registro semanal →](templates/weekly-tracker.csv)

## Entiende qué demuestra cada herramienta

- **Auditor Python:** HTTP/HTML inicial, reglas comunes de robots y un sitemap del mismo origen. JavaScript, acceso del crawler real y cobertura de todo el sitio necesitan otras comprobaciones.
- **Trabajo con asistente:** propuestas o cambios acotados con tus herramientas y evidencia. Desplegar y verificar en vivo son pasos separados.
- **Search Console:** inspección y rendimiento reportados por Google. La prueba en vivo no garantiza indexación ni aparición.
- **Analytics:** sesiones y resultados según tus reglas documentadas. Referencias ausentes, UTMs copiados y datos faltantes limitan la atribución.

**Comprobaciones de calidad:** pruebas HTTP/parser/CLI, integridad del repositorio y ejercicio antes/después. CI revisa Python 3.10 y 3.14, además de los helpers Node. [Auditoría y validación actual](docs/audit-validation.md). [Validación O3](docs/quality-results.md) · [Validación O4](docs/first-visits-validation.md)

## Encuentra el próximo documento

- [Primeras 100 visitas](playbook/first-100-visits.es.md): resumen español con acceso al recorrido completo y sus fuentes.
- [Referencia del auditor](docs/auditor.md): comandos, campos y límites.
- [Hoja de lanzamiento](templates/launch-worksheet.md): pregunta, página y siguiente acción.
- [Definiciones de medición](templates/measurement.md): sesiones, clicks y pagos separados.
- [Skills avanzados](skills/README.md): consulta opcional después de tu primera auditoría.

## Construyámoslo con la comunidad

Si un hallazgo está mal, comparte un caso público mínimo, el comando y el resultado esperado frente al observado. Quita credenciales y datos de clientes antes de compartirlo.

Ejecuta las pruebas Python:

```bash
python3 -m unittest \
discover -s tests -v
```

Lee [CONTRIBUTING](CONTRIBUTING.md) para aportar. Si te ayudó a encontrar un problema real, una estrella ayuda a que otros builders lo descubran. Los aportes reproducibles lo hacen más útil.

---

Código y documentación: [MIT](LICENSE). Identidad de Foundvia: [procedencia de marca](docs/brand.md). Fuente Geist: [SIL OFL 1.1](assets/fonts/OFL.txt). [Gráficos editables y exports](assets/README.md).
