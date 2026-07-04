---
name: niche-radar
description: "Research de nicho con datos verificables y GRATIS (sin Sandcastles): recolecta métricas reales de YouTube Shorts vía yt-dlp y de Instagram/TikTok vía navegador asistido, separa winners de losers con datos, baja transcripts, y alimenta la metodología hook-machine para extraer patrones y fórmulas. Usar cuando se pida: research de un canal o nicho, analizar competencia con datos reales, qué está funcionando en el nicho de un cliente, radar de canales, o alimentar hook-machine sin pagar Sandcastles."
---

# NICHE-RADAR — datos reales del nicho, sin suscripciones

Reemplaza la capa de datos de Sandcastles con fuentes verificables a costo $0. La filosofía (de Kallaway): el contenido es **datos + psicología** — los datos dicen qué ya funcionó; la psicología predice qué volverá a funcionar. Este radar aporta los datos; `hook-machine` aporta el análisis; `hook-lab` aporta la conversión.

## Capa de datos por plataforma

### YouTube Shorts — automatizado (preferido)
```bash
node tools/niche-radar/scripts/yt-shorts-radar.mjs --channel "@handle" --max 60 --winners 8 --client <slug>
```
Extrae por canal: ranking completo por views, detalle de winners (views, likes, comments, engagement %, duración) y transcripts de los winners. Salida: `radar.json` + `report.md` + `transcripts/`. Requiere yt-dlp (winget) y Node 22+. Todo dato es público y reproducible — cualquiera puede verificar el número abriendo el link.

### Instagram / TikTok — asistido por navegador
No hay API pública sana. El flujo es el que haría un investigador humano, con Claude operando el Chrome del dueño (sesión conectada):
1. Abrir el perfil público del canal a estudiar.
2. Recorrer el grid y registrar: URL, caption/título, view count visible, fecha aproximada.
3. Ordenar, detectar la línea winner/loser (gap natural), registrar en `radar.json` con el mismo esquema que YouTube.
4. Para transcripts de winners: el dueño descarga el clip (o autoriza descarga puntual) → transcribir con Whisper local (skill `hyperframes-media`, comando `transcribe`, $0).

Límites honestos: es más lento que una API, los view counts de IG a veces solo se ven logueado, y no se automatiza a escala (no somos un scraper — volumen bajo, ritmo humano).

## Metodología de análisis (delegada a hook-machine)

Con los datos recolectados, aplicar los pasos 3-6 de `.claude/skills/hook-machine/SKILL.md`:
- Winners vs losers por gap natural de views; filtrar sospecha de pauta (engagement < 2% con views altos).
- Extraer el hook hablado de cada transcript (donde termina "retener" y empieza "entregar").
- Patrones mínimos: psicología, trigger words, estructura gramatical — por canal, luego síntesis cruzada.
- Librería de fórmulas mad-lib con views de respaldo + rúbrica personalizada (8 principios universales + hallazgos del nicho).

Todo se vuelca al cliente: `tools/hook-lab/clients/<slug>/swipe.md` (research acumulado) y `hooks.json` (batería para producción). El filtro final siempre es hook-lab: nivel de conciencia del avatar comprador + modo ALCANCE vs CONVERSIÓN.

## Los 4 no-negociables del sistema (síntesis Kallaway, para operar con clientes)

1. **Constancia**: mínimo 3-5 videos/semana por cuenta — nuestro `render-batch.mjs` existe para esto.
2. **Hipótesis por video**: cada pieza prueba UN cambio deliberado (hook, layout, formato) y se anota qué se probó — sin experimento no hay aprendizaje.
3. **Tráfico → oferta alineada**: views sin conversión es hobby caro. Cada cuenta necesita CTA intencional y camino medible a la venta (UTM/DM/código) — ver modos en hook-lab.
4. **No parar**: la habilidad compone alrededor del rep ~50; la mayoría abandona en el ~25. El sistema existe para sostener el ritmo cuando los resultados aún no llegan.

Y el principio de remix: no se necesita originalidad total — se identifica la combinación que ya funciona en el nicho (formato, tema, hook, estructura, edición) y se cambian 2-3 piezas con el giro propio del cliente. Innovación enfocada, tasa de acierto alta.

## Reglas

- Solo datos públicos, ritmo humano, volumen bajo. Nada de credenciales de terceros ni evasión de bloqueos.
- Descargas de clips: solo puntuales, para análisis de transcript, con OK del dueño.
- Los runs de radar por cliente SÍ se comitean (activo de la agencia); los clips descargados NO.
