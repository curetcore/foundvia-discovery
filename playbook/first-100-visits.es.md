# Tus primeras 100 visitas

Una página útil, un bloqueo comprobado y una forma clara de medir.

La meta es **100 sesiones medidas desde Google orgánico y referencias observadas de ChatGPT**, contadas por separado. No son 100 personas únicas ni 100 clientes. No hay un plazo prometido.

La [guía completa en inglés](first-100-visits.md) es el recorrido principal. No necesitas elegir entre 11 skills.

| Paso | Qué haces | Qué debe salir | Cómo lo compruebas |
|---|---|---|---|
| 1. Revisar | Ejecutas el auditor en una página pública | Reporte con evidencia y siguiente acción | Abres esa página sin sesión en tu móvil |
| 2. Corregir | Quitas un bloqueo accidental, si existe | Cambio pequeño y revisable | Comparas el reporte antes y después del despliegue autorizado |
| 3. Inspeccionar | Verificas tu sitio en Search Console e inspeccionas la URL | Estado y problema concreto, si lo hay | Separas prueba en vivo de estado indexado |
| 4. Ayudar | Respondes una pregunta real con un ejemplo probado | Una página que resuelve una tarea | Sigues sus instrucciones y pruebas sus enlaces |
| 5. Compartir | Preparas una respuesta donde sea relevante | Un aporte útil, con enlace solo si ayuda | Revisas las reglas y obtienes aprobación para publicar en nombre de otra persona |
| 6. Medir | Anotas sesiones y resultados por semana | Registro sin duplicados | No sumas clicks de Google con sesiones de analytics |

## Empieza aquí

Necesitas Git y Python 3.10+ instalados. En tu terminal:

```bash
git clone https://github.com/ronaldships/foundvia-discovery.git
cd foundvia-discovery
python3 skills/foundvia-discovery/scripts/discovery_audit.py https://tu-sitio.com > audit-before.md
```

Cambia la URL por tu página pública y abre `audit-before.md` en tu editor. Si ya tienes el repositorio, ejecuta solo la última línea dentro de su carpeta. En Windows, tu comando puede ser `py -3`.

Para practicar sin tocar tu web:

```bash
python3 examples/discovery-lab/run.py
```

Abre `outputs-local/discovery-lab/before.md` y `after.md`. El ejercicio elimina un `noindex` accidental y conserva bloqueado GPTBot: permitir búsquedas y permitir entrenamiento son decisiones distintas. El servidor se cierra al terminar. Esto demuestra el cambio técnico; no demuestra visitas ni recomendaciones.

## Qué copiar

- [Hoja de lanzamiento](../templates/launch-worksheet.md): pregunta, página, evidencia y próxima acción.
- [Registro semanal CSV](../templates/weekly-tracker.csv): sesiones, registros, activación y clientes de pago separados.
- [Definiciones de medición](../templates/measurement.md): fechas, atribución y reglas de conteo.
- [Límites del auditor](../docs/auditor.md): no ejecuta JavaScript ni confirma indexación.

Si no hay bloqueos observados, pasa a mejorar la respuesta para el usuario. No cambies configuraciones solo para conseguir un reporte “más verde”. Un resultado desconocido requiere revisión, no asumir que todo pasó.

Las instrucciones oficiales y sus fuentes están junto a cada paso en la [guía completa](first-100-visits.md), revisadas el 6 de octubre de 2026.
