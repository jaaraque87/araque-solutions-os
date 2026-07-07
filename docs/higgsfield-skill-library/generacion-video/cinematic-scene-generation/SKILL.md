---
name: cinematic-scene-generation
title: "Cinematic Scene Generation"
author: joshhoole
category: Creative-marketing
source: https://higgsfield.ai/supercomputer/marketplace/skills/154f33e7-720a-499c-b658-85eeb183b6ad
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# Cinematic Scene Generation
Usa **Nano Banana Pro** para producir variaciones cinematográficas premium (ángulos alternativos + insert shots) a partir de una imagen de escena de referencia. Trigger: "cinematic scene generation", "generate angles and insert shots", "cinematographer angles".

## Inputs
- **Reference Image:** upload o un job previo.
- **Config:** Count (cantidad de ángulos + inserts, default 5 c/u) · Aspect Ratio (16:9, 2.39:1) · Style Variance ("Standard" = cinematografía continua realista / "Extreme" = modificaciones dramáticas).

## Workflow
**Step 1 — Pre-Generation Survey (obligatorio):** con `ask_user_question` preguntar antes de generar: cuántos ángulos+inserts · aspect ratio (16:9 Cinematic Landscape / 2.39:1 anamórfico) · Standard Coverage vs Extreme Variations.
**Step 2 — Resource Processing:** si subió imagen fresca, correr `higgsfield_upload` → URL+ID públicos (`media_input`). Reusar assets idénticos vía `artifact_get(key="upload:<sha256>")`.
**Step 3 — Prompt Crafting:** cada prompt DEBE embeber exacto el System Role Block (abajo).
**Step 4 — Parallel Batch:** bundle de todos los prompts en un batch concurrente con modelo `nano_banana_pro`. Para N ángulos + N inserts → `2*N` requests en paralelo. Respetar límites de concurrencia (si excede, batch en olas). No pollear completitud salvo dependencia downstream.
**Verificación:** confirmar al usuario que la generación de coverage alternativo se lanzó.

## Base System Role Block (embeber en CADA prompt, verbatim)
> You are a world-class Cinematographer and Master Gaffer. Your goal is to generate images that are indistinguishable from high-budget cinema.
> - **Optics:** default a sensores Arri Alexa 65 o Panavision Millennium DXL2. Usar focal lengths específicas.
> - **Lighting:** "Rembrandt lighting", "Negative Fill" o "Motivated Lighting". Alto rango dinámico.
> - **Color Science:** emulación custom Kodak Vision3 5219. Priorizar skin tones perfectos (naturales).
> - **Integration:** cada personaje perfectamente compuesto en el entorno con dirección/color de luz que matchea.

## Stylistic Modification Rules
- **Standard Coverage:** continuidad lógica, coverage profesional (wide master, medium, close-up, insert).
- **Extreme Coverage:** setups y luz más audaces, radicales, surreales; introducir ángulos/lentes no convencionales.
