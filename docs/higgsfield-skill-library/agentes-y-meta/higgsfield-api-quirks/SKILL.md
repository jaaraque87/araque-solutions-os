---
name: higgsfield-api-quirks
title: "Higgsfield API Quirks"
author: cherry_blackcloud
category: Content Creation
users: 71
source: https://higgsfield.ai/supercomputer/marketplace/skills/3cd0be0f-d44e-4bdf-ba80-b0a87cffe20a
extracted: modal SKILL.md (via claude-in-chrome) — single file
relevante: alto — comportamiento no documentado y workarounds de 500 en `higgsfield_generate`
---

# Higgsfield API Quirks
Fallas model-specific y requisitos de payload que difieren del schema estándar de `higgsfield_generate`.

## Seedance 2.0
- **Audio input (evitar 500):** NO pasar audio con `role:"audio"` dentro de `medias` (dispara HTTP 500 consistente). Correcto: dentro de `params` → `input_audio: {"id":"<id>","type":"media_input","url":"<url>"}`.
- **Resolution/Aspect Ratio:** ignora `width`/`height` numéricos precisos (default a 1:1 si se fuerza). DEBE usar `aspect_ratio` ("21:9", "16:9", "9:16").
- **Reference limits:** límite duro de **9 reference slots** totales (medias array + element tokens `<<<element_id>>>`). Un matchcut típico consume varios.

## Kling 3.0
- **Matchcut incompatibilities:** soporta matchcuts (`role:"start_image"` + `role:"end_image"`), pero es **incompatible con element tokens** cuando se usa `end_image`. No pasar tokens `<<<id>>>` en un Kling con end_image.
- **Framerate output:** output nativo 30fps. Si se puentea material 24fps, re-encode fuerte (`ffmpeg -r 24`).
