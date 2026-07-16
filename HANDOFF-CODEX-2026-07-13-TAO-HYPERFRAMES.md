# Handoff Codex — Camila PROD001 / TAO + HyperFrames

Fecha: 2026-07-13 (America/Bogota)

## Resultado actual

Se reemplazó el flujo visual defectuoso por TAO LTX Director V2 con imagen y audio
reales por escena. Existen cinco clips activos en orden contractual `esc1..esc5`,
todos a 640x1152, 24 fps, con audio. La L40S quedó apagada.

La escena 2 original de TAO fue rechazada porque hizo un corte/zoom entre los
fotogramas 77 y 78. Se regeneró con la misma imagen anclada al primer y último
fotograma. La toma activa corregida tiene 225 fotogramas, delta máximo 0.00957 y
cero saltos duros.

## Clips activos (no están en git)

`C:\Users\SOPORTE2\Downloads\CAMILA_TAO_SCENES\`

- `esc1.mp4`
- `esc2.mp4` — toma corregida y aprobada para montaje
- `esc3.mp4` — piloto validado
- `esc4.mp4`
- `esc5.mp4`
- `esc2_rejected_jump.mp4` — evidencia rechazada; no usar

QA general antes de corregir escena 2: audio contra fuente con correlación de
envolvente 0.975–0.994 y desfase de 20–60 ms; articulación visible; identidad
estable. Reporte y fotogramas: `C:\Users\SOPORTE2\Downloads\CAMILA_TAO_QA\`.

## HyperFrames

Proyecto de ensamblaje creado, pero todavía NO lint/inspect/render:

`tools/content-reel-lab/outputs/camila-prod001-tao-final/`

Contiene los cinco clips, montaje fijo de 28.52 s, audio por escena, captions
españoles, CTA, transiciones que no solapan audio y kill determinista de captions.
La escena 5 conserva el audio desde 0; su salto inicial de dos cuadros queda bajo
el velo de transición. Próximo paso obligatorio:

1. `hyperframes lint`
2. `hyperframes validate`
3. `hyperframes inspect --time 0,2.68,11.76,18.40,23.90,28.40`
4. corregir cualquier error visual
5. render MP4 final 1080x1920, 24 fps
6. volver a auditar orden de escenas, audio total y duplicados

Usar el binario local:

`tools/content-reel-lab/node_modules/.bin/hyperframes.cmd`

FFmpeg/ffprobe disponibles en:

`C:\Users\SOPORTE2\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\`

## Automatización implementada en git (cambios todavía sin commit)

### TAO

`tools/tao-director/render_scene.py`

- sube foto + audio exactos;
- crea timeline determinista con seed fijo;
- usa `ceil(duracion * 24)` para no cortar voz;
- encola, monitorea, descarga y escribe manifest con SHA-256;
- `--dry-run` materializa el prompt sin GPU.

Pruebas: `tools/tao-director/test_render_scene.py` — 3/3 OK.

### Builder anterior

`tools/builder-orchestrator/`

- segmentos nuevos por copia profunda;
- limpia outputs heredados;
- hashes imagen/audio y fingerprint por escena;
- rechaza clips recuperados de slot equivocado;
- rechaza rutas duplicadas antes del stitch.

Pruebas: 11/11 OK.

## Estado git

Hay cambios sin commit. No hacer reset ni checkout. Revisar `git status` y conservar
los cambios del usuario. Los outputs y assets generados no deben commitearse.

## Decisión técnica

Arquitectura recomendada para agencia masiva:

`kit/contrato -> TAO por escena -> QA automático -> HyperFrames -> master final`

TAO genera actuación/lipsync. HyperFrames solo ensambla y añade captions, overlays,
CTA, música/SFX y export. Nunca volver a confiar en el orden de render: el montaje
se resuelve por `scene_id + hash`, no por nombre remoto ni por orden de finalización.
