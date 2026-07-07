---
name: video-split-stitch
title: "Video Split Stitch"
author: cherry_blackcloud
category: Content Creation
users: 12
source: https://higgsfield.ai/supercomputer/marketplace/skills/904de0e6-06e4-40aa-b4c5-06615c7cbf1c
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): scripts/split_utils.py
---

# Video Split Stitch Pipeline
Analiza un video para encontrar los frames consecutivos MÁS diferentes, lo parte ahí, y genera una transición AI seamless para re-unir las partes.

## Inputs
Video Reference (HTTPS URL o path local .mp4) · Bridging Prompt (opcional, describe acción/movimiento durante la transición AI).

## Workflow
1. **Initialize:** crear `/tmp/split_stitch_<timestamp>` aislado.
2. **Download/Locate:** si es HTTPS → `curl -o input.mp4 "URL"`; si local → copiar/symlink como input.mp4.
3. **Visual Difference Analysis:** `python3 split_utils.py analyze input.mp4` → extraer de stdout: `split_frame` (índice antes del cambio), `time_sec` (timestamp del boundary), `width/height/fps`.
4. **Present for approval:** mostrar boundary frame/timestamp; avisar que se extraerá frame_a (@split_frame) y frame_b (@split_frame+1); ESPERAR aprobación.
5. **Extract & split:** `python3 split_utils.py split input.mp4 <split_frame>` → produce frame_a.png, frame_b.png, part1.mp4, part2.mp4.
6. **Upload frames:** `higgsfield_upload` de frame_a.png y frame_b.png → media IDs/URLs públicos (obligatorio).
7. **Generate AI bridge:** `higgsfield_generate` con seedance_2_0. `params.medias` = ambos frames como `{role:"image", data:{id, type:"media_input"}}`. `params.prompt` = prompt del usuario o descriptivo referenciando las 2 imágenes. **NO usar transition words** (dissolve/fade/morph/blend/wipe) — usar phrasing positivo. Resolution logic: si source height=1080→"1080p", 720→"720p", 480→"480p". aspect_ratio match del original (9:16/16:9). Respetar concurrencia del plan.
8. **Final review & assembly:** pollear `higgsfield_job_status` hasta completar → presentar part1/part2/bridge → preguntar si stitchear los 3 (part1→bridge→part2) en un video unificado. Registrar files/logs/job IDs en artifacts.
