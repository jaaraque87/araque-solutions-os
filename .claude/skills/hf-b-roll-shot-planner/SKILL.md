---
name: hf-b-roll-shot-planner
title: "B-Roll Shot Planner"
author: quincynb
category: Content Creation
source: https://higgsfield.ai/supercomputer/marketplace/skills/d4b0d9c7-7251-4ea0-80a4-cca157ad672b
extracted: modal SKILL.md (via claude-in-chrome) — single file
description: "Planifica 5 tomas B-roll en JSON desde una imagen ancla de estilo. Usar cuando un reel necesite B-roll coherente con la estetica del video principal."
---

# Cinematic B-roll Shot Planner (para NanoBanana)
Analiza el input del usuario y planea coberturas de B-roll cinematográficas. Devuelve **5 shots** por batch como JSON separados.

## Core Behavior
- **STYLE_ANCHOR Principle:** la primera imagen subida se vuelve el STYLE_ANCHOR.
- **Visual Baseline:** el STYLE_ANCHOR define foco, nivel de realismo/estilización, paleta de color, etc.
- **Consistency Gate:** mantener ese estilo bloqueado para todos los shots salvo que el usuario suba una imagen nueva Y pida explícitamente cambiar.
- **Prompt Rule:** en cada `prompt_text` afirmar explícitamente que el shot matchea el estilo visual exacto del anchor adjunto.

## Input Processing
**Case 1 — Imagen subida (primera o nuevo style guide):** inferir subject/entorno/mood/luz/estilo de la imagen → registrar como STYLE_ANCHOR activo → diseñar 5 B-roll shots nativos a ese mundo → mismo subject/mundo/estilo, variar ángulos, framings, lentes.
**Case 2 — Solo texto (sin imagen nueva):** usar el STYLE_ANCHOR activo para estilo/tono → el texto es la escena/acción focal → Shot 1 = match más directo al texto → Shots 2–5 = coverage de apoyo en la misma escena para continuidad de edición.

## Sequencing Logic (pensar como editor, no como prompt writer)
- **Story-supporting coverage:** integrar detalles, inserts, close-ups táctiles, cutaways ambientales, foco en objeto aislado, reaction frames.
- Si el usuario da una acción primaria: Shot 1 = acción principal clara; Shots 2–5 = close-ups, inserts táctiles (manijas, bisagras, partes móviles), elementos alrededor, frames secundarios.
- **Variety:** mezclar ángulos low/high, macro close-ups, wide establishing, POV.

## Output Structure
NO devolver un JSON grande con array "shots". Devolver **5 objetos JSON standalone**. Por cada shot:
1. Una línea de heading corta ARRIBA del bloque de código (fuera del code block), empezando con emoji apropiado y describiendo el evento del shot en texto plano (nunca "Shot 1" genérico).
2. Exactamente un fenced code block ```json``` con el objeto de ese shot.
3. Una línea en blanco antes del siguiente heading.

## JSON Schema (10 keys por shot)
`shot_name`, `camera_angle`, `framing`, `lens_mm`, `subject`, `action`, `location_cues`, `lighting`, `prompt_text`, `negative_prompt`.

## Field Constraints
- **camera_angle:** uno de: `eye_level`, `low_angle`, `high_angle`, `top_view`, `dutch_angle`, `over_the_shoulder`, `pov`.
- **framing:** uno de: `establishing_wide`, `wide`, `medium`, `medium_close_up`, `close_up`, `extreme_close_up`, `insert_detail`.
- **lens_mm:** focal realista como `"18"`, `"24"`, `"35"`, `"50"`, `"85"`, `"100"`.
- **subject:** identificación muy corta del elemento visual principal en foco.
- **action:** descripción en presente activo de estados/movimientos del sujeto.
- **location_cues:** descriptores visuales que matchean el entorno del anchor/escena.
- **lighting:** nota cinematográfica corta ("high-contrast cinematic key-light", "soft moody glow").
- **prompt_text:** orden rígido: 1) aserción explícita de que matchea el estilo visual exacto, 2) resto de la descripción del shot.
- **negative_prompt:** filtrar defectos ("distortions, warping, jitter...").
