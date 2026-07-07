---
name: nike-air-force-ad
title: "Nike Air Force Ad"
author: nashbeluga1412
category: Content Creation
users: 9
source: https://higgsfield.ai/supercomputer/marketplace/skills/ec4bff33-b6ab-46bf-9454-ec133107ceb8
extracted: modal SKILL.md (via claude-in-chrome) — single file
nota: prompt validado específico (product reveal AF1). El VALOR general reusable es la estructura de 6 shots + transiciones dramáticas + audio SFX-only para product reveals cinematográficos de calzado/producto.
---

# Nike Air Force 1 — Cinematic Product Reveal Ad
Genera un reveal cinematográfico de 15s de un sneaker. 9:16, Seedance 2.0, cámara motion-control, audio SFX-only. Trigger: "nike air force ad", "AF1 ad".

## Parameters
Model `seedance_2_0` · aspect 9:16 (TikTok/Reels/Shorts) · duration 15s · `generate_audio: true` (SFX-only, sin speech) · palette White #FFFFFF / Jet black #0A0A0A / Warm silver #C0C0C0 · camera Bot&Dolly motion-control.

## Shot Structure (6 shots — patrón reusable para product reveals)
- 0-2.5s **Extreme macro** leather toe box (perforaciones con hard rim light, dolly push-in 3cm).
- 2.5-5s **Hero float** 3/4 angle (flotando en black void, orbital sweep 45°, three-point lighting).
- 5-7.5s **Outsole tread macro** (pivot-point, crane descent 4cm, volumetric shaft light).
- 7.5-10s **Low-angle levitation** (tilteado 15° sobre superficie negra reflectante, lift-and-rotate 30°).
- 10-12.5s **Paired beauty shot** (ambos sobre gradient void, drift lock-on con micro horizon tilt).
- 12.5-13.7s **Wordmark closer** ("AIR FORCE 1" centrado en black void) + 1.3s tail freeze.

## Transitions (dramáticas entre shots)
1→2 DRAMATIC PUSH-THROUGH (a través del eyelet al void) · 2→3 DRAMATIC OBJECT MORPH (chrome dust dissolve) · 3→4 DRAMATIC LIGHT SWEEP (warm silver ray) · 4→5 Bot&Dolly snap (frame-perfect lock) · 5→6 DRAMATIC PARTICLE DISSOLVE (silver chrome → wordmark).

## Audio Design (SFX por timecode)
0.5s deep resonant bass thump · 1.5s subtle leather creak · 2.5s atmospheric whoosh (push-through) · crystalline chime (morph) · 7.5-10s low rumble build · 10s sharp impact hit (snap) · 12.5s specular flash chime (wordmark) · 13.7-15s ambient drone hold to tail.

## Prompt (patrón clave)
`CRITICAL: Animate as ONE single continuous full-frame 9:16 cinematic film — each shot occupies the complete frame...` (choreography shot-by-shot con transiciones y timecodes; MANDATORY SILENT TAIL PAUSE 13.7-15s pixel-idéntico). **Nota de marca:** "All apparel marks, wordmarks, and brand identifiers are original generic designs" (evita infracción).

## Execution
`higgsfield_generate(requests=[{"type":"generation","media_type":"video","model":"seedance_2_0","params":{"prompt":"<above>","aspect_ratio":"9:16","duration":15,"generate_audio":true}}])`

## Variants
Colorway swap (white→Triple Black) · Horizontal (16:9 para YouTube/web hero) · Short cut (10s, dropear shots 3 y 5) · With product photo (upload → medias media_input con @Image1 anchor).
