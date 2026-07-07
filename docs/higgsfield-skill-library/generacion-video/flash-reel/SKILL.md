---
name: flash-reel
title: "Flash Reel"
author: bossanimaciones
category: Creative-marketing
users: 294
source: https://higgsfield.ai/supercomputer/marketplace/skills/2fb958ef-2359-4d70-bf36-72b17838b477
extracted: modal SKILL.md (via claude-in-chrome) — single file
relevante: alto para reels de Milivoy (estética flash + pipeline 8 escenas). OJO: el SKILL trae refs hardcodeadas del PROPIO autor (5 media IDs de "the man") — NO reusar; sustituir por refs de Milivoy.
---

# Flash Reel — 30s Cinematic Reel (9:16)
Genera un reel cinematográfico de ~30s en 9:16 desde un prompt (setting + vibe + storyline). 8 clips de ~3.75s. Estética flash 2000s.

## GOLDEN RULE — References over text
Toda la identidad viene EXCLUSIVAMENTE de imágenes de referencia. En los prompts referirse a personajes solo como "the man from the reference images" / "the woman from the girl reference". **NUNCA describir la apariencia física de un personaje en el texto del prompt.** El outfit del protagonista se recoge del usuario (descripción + foto de referencia de outfit), no se hardcodea.

## La receta de estética flash (el prompt de imagen — reusable, oro)
> Shot on 35mm film camera Kodak Portra 400 pushed to 800, ISO 800, f/5.6, 1/60s shutter speed. Harsh on-camera flash, creating flat frontal illumination with a sharp shadow behind and specular highlights on skin and fabric. Teal-cyan shadows, slightly warm midtones, desaturated green-blue color grade, visible film grain, mild halation around bright points. Amateur flash photography aesthetic, 2000s snapshot style, raw unretouched look. Not digital, not illustration, not CGI. 9:16 vertical frame.

El prompt describe SOLO: escena/entorno, mood, y estética de cámara/film. La identidad la aportan las refs.

## Virality de la Escena 1 (scroll-stopping, no un retrato limpio)
Cara medio tragada por la sombra, solo un ojo/pómulo captado por el flash · mano/dedos demoníacos saliendo del vacío · ángulo muy bajo mirando hacia arriba con media sonrisa cruel · media cara iluminada, la otra disuelta en negro absoluto con un elemento sobrenatural · peligro fatal inminente (arma a punto de golpear el cuello mientras el sujeto está inconsciente de ello).

## ask_user_question
**DO ask:** Setting · Vibe/mood · Storyline hint (opcional) · Clothing/look del protagonista · Foto de referencia de outfit (upload, 1 archivo).
**NEVER ask:** aspect ratio (siempre 9:16) · modelo (imagegen_2_0 imágenes, kling3_0 video) · resolución (1080p) · nº de clips (siempre 8 → ~30s) · si incluir al hombre (siempre, ≥5 de 8 escenas) · style string (siempre la estética flash 35mm).

## Pipeline
**STEP 1 — Recoger inputs** (ask_user_question con 5 preguntas).
**STEP 2 — Scene breakdown:** exactamente 8 escenas. Escena 1 virality-engineered (extreme close-up, mirada directa). Escenas 2-8: al menos un personaje cada una (nada solo-entorno). Las 8 comparten vibe/estética — NO historia lineal, solo consistencia temática. ~2 oraciones por escena. Asignar character_present + qué REF usar. Distribuir REFs sin repetir consecutivo.
**STEP 2.5 — Story verification gate (OBLIGATORIO):** presentar el breakdown completo al usuario (nº escena, si aparece el hombre, qué REF, descripción, motion planeado) y preguntar: looks good / cambiar escenas específicas / reescribir todo. Solo avanzar tras confirmación explícita.
**STEP 3 — Generar 8 starting frames** (imagegen_2_0 / GPT Image 2, 9:16). Generar 4 variantes × 8 escenas = 32 imágenes ANTES de pedir selección. Batch size 4 por wave. Subir cada variante vía higgsfield_upload (los paths locales NO renderizan en el web client). Presentar como batches cronológicos etiquetados 1A/1B/1C/1D... El usuario elige una por escena. Pasar TODAS las refs del personaje juntas en `images[]` para cada escena de personaje.
**STEP 4 — Animar cada frame vía Kling 3.0:** 5s cada uno SIEMPRE, 1080p (`mode:"pro"`), 9:16, `generate_audio:false`. Lecciones: Kling 3.0 con `role:"start_image"` + `type:"image_job"` FUNCIONA; con `role:"image"` o `kling_element_ids` IGNORA el input y genera gente random. Kling 2.6 también ignora. Motion prompts CORTOS (1 oración, una moción, una dirección). NUNCA "frozen moment"/"static shot" (peores artefactos); usar "Subject stands still, barely breathing. Very slow subtle...". Siempre prefijar "Extremely slow and smooth". Generar 2 variantes de video por escena. Submit 8 jobs en una llamada.
**STEP 4.5 — QC pass:** ffprobe cada clip (~5s), extraer 3 frames (inicio/medio/fin) y revisar caras derretidas/disueltas. Redo con prompt simplificado si falla. Usuario = QC final.
**STEP 5 — Entregar clips individuales:** NO stitchear; el usuario ensambla. Presentar links CDN uno por escena.

## Motion prompts por escena (usar exacto)
1. slow zoom in a la cara · 2. slow zoom in al sujeto · 3. slow zoom out revelando entorno · 4. slow pan left · 5. slow tilt up · 6. slow zoom out · 7. slow zoom in a los sujetos · 8. slow pan right. (Todos prefijados "Extremely slow and smooth".)

## Output spec
MP4 H.264 · 1080×1920 (9:16) · ~30s · 30fps · sin audio (el usuario pone su música) · hard cuts cada ~3.75s.

## Credit optimization
imagegen_2_0 para imágenes (fuerte adherencia a refs) · kling3_0 para video (más fotorrealista i2v, usa start_image) · generate_audio:false en todos · 5s/clip · 8 clips = cap de concurrencia, todo en una wave.

## Error handling
Fallo/glitch imagegen → regenerar esa escena. Kling con shake → motion prompt más simple. Kling 422 (moderación) → retry una vez simplificado. Concat con codec mismatch → re-encode `ffmpeg -i clip.mp4 -c:v libx264 -crf 18` antes de concat.
