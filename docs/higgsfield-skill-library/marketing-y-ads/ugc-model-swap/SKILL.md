---
name: ugc-model-swap
title: "UGC Model Swap"
author: minimalistonion1079
category: Personal And Specialized
users: 229
source: https://higgsfield.ai/supercomputer/marketplace/skills/7120097b-8e59-44c5-9ae3-f075eb73b92f
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# UGC Model Swap
Recrea cualquier UGC video corto con OTRA persona manteniendo todo lo demás (setting, acción, props, audio). Para reactions, challenges, reviews, tutorials, try-ons, unboxing.

## Model
**Siempre Seedance 2.0 (`seedance_2_0`).** NO usar Cinematic Studio 2.5 Motion Control (falla silenciosamente con refs). Kling 3.0 también falla.

## Step 1 — Analizar el video fuente
`video_analyze(video_source=<url>, category="analysis_templates")` para extraer: setting (location/lighting/background) · apariencia+outfit del personaje · secuencia de acción (como UNA escena continua, no scenes numeradas) · props · audio/diálogo.

## Step 2 — Character reference (opcional pero recomendado)
Si dan foto del reemplazo: subir vía `higgsfield_upload`, pasar como `medias: [{"role":"image","data":{"id":"...","type":"media_input"}}]`, referenciar con `@Image1` al inicio del prompt. Si no hay foto: describir en texto.

## Step 3 — Build the prompt (escena continua única, NO "Scene 1/Scene 2")
Estructura: [character description] · [setting] · [opening shot] · [continuous action, en orden, un flujo] · [camera rules: face lock] · [audio].
**Key rules:**
1. **Single scene, sin splits numerados** (confunde al modelo).
2. **Cara siempre en frame** — repetir explícito: "HER FACE IS ALWAYS IN FRAME. Camera locked on her face. Never tilts down. Never follows her hand."
3. **Props hyper-específicos** — prohibir variaciones: "just one cube, no bucket, no bowl, no container, no pile — only ONE standalone [prop]".
4. **Acciones físicas con body mechanics** — en vez de "she puts it between her knees": "she deliberately reaches her hand down and tucks the [prop] inside the waistband of her jeans, pushing...".
5. **Audio siempre** — `"generate_audio": true` + línea `Audio: "[line1]" / "[line2]" / [sound] / "[line3]" Natural room acoustics.`

## Step 4 — Generate
```json
higgsfield_generate({"requests":[{"type":"generation","model":"seedance_2_0","media_type":"video","params":{"prompt":"<full>","aspect_ratio":"9:16","duration":5,"generate_audio":true,"medias":[{"role":"image","data":{"id":"<media_id>","type":"media_input","url":"<url>"}}]}}]})
```
Omitir `medias` si no hay reference image.

## Batch variants
Múltiples requests en una llamada: distintas etnias/edades · distintos outfits · con/sin foto de referencia.

## Pitfalls → Fix
| Problema | Fix |
|---|---|
| Genera bucket/pile en vez de un prop | negative explícito "no bucket, no bowl, no container, no pile — only ONE standalone [prop]" |
| Cámara baja y sigue la mano | repetir face-lock inline Y al final del prompt |
| Personaje suelta el prop en vez de colocarlo | describir body mechanics completas |
| Kling 3.0 / Cinematic Studio 2.5 falla silencioso | usar Seedance 2.0 (único confiable) |
| Reference character no matchea | `role:"image"` (no start_image) + `@Image1` al inicio |
| Abre en location equivocada | "INTERIOR [room]" explícito arriba antes de la acción |
| Se parte en escenas desconectadas | quitar labels "Scene N", escribir un párrafo continuo |
```
