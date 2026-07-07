---
name: video-stitching
title: "Video Stitching"
author: cherry_blackcloud
category: Content Creation
users: 33
source: https://higgsfield.ai/supercomputer/marketplace/skills/bf5a11e9-f1a6-460c-8dc3-cd85b2ea2a1c
extracted: modal SKILL.md (via claude-in-chrome) — single file
relevante: alto — puentear dos videos con transición AI (aplica a producción de reels)
---

# Video Stitching / Bridging
Puentear dos videos con un clip de transición AI seamless (extraer último frame de V1 + primer frame de V2 → generar bridge → concatenar).

## 1. Asset Retrieval Quirks
`higgsfield_attachments_list` SOLO devuelve archivos subidos por el usuario, NO videos generados. Para videos generados: pedir al usuario las Asset URLs (`https://higgsfield.ai/asset/video/<job_id>`) o job_ids; usar `higgsfield_job_status` para resolver a URLs playables.

## 2. Frame Extraction
Descargar los videos y usar ffmpeg:
- **Último frame de V1:** `ffprobe` para la duración, luego `ffmpeg -y -i v1.mp4 -ss <duration-0.5> -vframes 1 -update 1 -q:v 2 start.jpg`. **NO usar `-sseof`** (falla en clips cortos/VFR).
- **Primer frame de V2:** `ffmpeg -y -i v2.mp4 -vframes 1 -update 1 -q:v 2 end.jpg`. Subir ambos frames con `higgsfield_upload`.

## 3. Model Quirks (la doc oficial tiene inexactitudes sobre soporte de end_image)
- **Kling 3.0 (`kling3_0`):** SÍ soporta start_image Y end_image. Usar para bridging de alta calidad. `duration` mínimo 3s.
- **Seedance 2.0 (`seedance_2_0`):** NO soporta end_image. Pasar ambos frames como roles `image` + prompt "One continuous uncut shot. Must start exactly with image 1 and must end exactly with image 2."
- **Wan 2.7 (`wan2_7`):** NO soporta end_image (pasar end frame como role `image` da target estilístico pero no garantiza).
- **Kling 2.6 (`kling2_6`) y Seedance 1.5 (`seedance1_5`):** soportan start y end frames nativos.

## 5. Generation Payload
```json
{"model":"kling3_0","params":{"duration":3,"prompt":"One continuous uncut shot","medias":[{"role":"start_image","data":{"id":"<upload_id_1>","type":"media_input"}},{"role":"end_image","data":{"id":"<upload_id_2>","type":"media_input"}}]}}
```

## 6. Video Concatenation (lossless)
Reusar V1 y V2 ya descargados (no re-descargar) · descargar el bridge local · crear `list.txt` con `file '/path/to/clip.mp4'` por línea · `ffmpeg -y -f concat -safe 0 -i list.txt -c copy final.mp4` · subir con `higgsfield_upload`. Para chains de N clips (3 clips = 2 bridges): disparar todos los bridge jobs en paralelo, combinar en un solo concat.

## 7. Audio Blending
Para que el bridge lleve el audio de V1 a V2: extraer último 1s de audio V1 (`ffmpeg -y -sseof -1 -i v1.mp4 -vn -acodec pcm_s16le audio1.wav`) y primer 1s de V2 (`ffmpeg -y -i v2.mp4 -t 1 -vn -acodec pcm_s16le audio2.wav`); subir ambos. En Seedance 2.0 pasar audio vía param top-level `input_audio` (NO en medias — dispara HTTP 500): `params: { input_audio: { id, type:"media_input", url } }`. Prompt steering: "@Audio1 blends into @Audio2 in one continuous uncut sound logically."
