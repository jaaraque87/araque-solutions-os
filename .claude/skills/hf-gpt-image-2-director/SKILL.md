---
name: hf-gpt-image-2-director
title: "Gpt Image 2 Director"
author: crococopter
source: https://higgsfield.ai/supercomputer/marketplace/skills/34798858-5c85-472f-9500-01c9e4f9fcd7
extracted: modal SKILL.md (via claude-in-chrome) — single file, sin references
description: "Director de prompts para GPT Image 2 (imagegen_2_0): retratos, posters con texto 95%+, character sheets, 2K nativo. Usar al generar imagenes/datasets de Naia o Kenza con GPT Images 2."
---

# GPT Image 2 Pro Director
Director de prompts de producción para GPT Image 2 (modelo `imagegen_2_0`). Es reasoning-aware: interpreta instrucciones en lenguaje natural por capas. **Escribir el prompt final SIEMPRE en inglés** (las explicaciones al usuario en cualquier idioma).

## Capacidades a explotar
- **Text rendering 95%+** (Latin, chino, japonés, coreano, árabe) → posters, UI mockups, signage. *(← el superpoder para el texto rojo del reel)*
- **2K nativo** (+ upscale 4K) — nunca rellenar con "8K, ultra HD, masterpiece".
- **Aspect ratios 3:1 a 1:3** — siempre especificar (default 1:1).
- **Consistencia de personaje** entre imágenes secuenciales (multi-view sheets, edición iterativa).
- **Edición en lenguaje natural** — recuerda generaciones previas en la conversación.
- **Reasoning integration** — infiere detalles contextuales (clima, datos, lógica espacial).

## Limitaciones (workarounds)
- Logos de marca poco confiables → componer en post, no prometer logo exacto.
- Control de estilo menos granular que Midjourney → compensar con lenguaje descriptivo.
- Velocidad 30-60s por imagen.
- Content policy más estricta que open-source.
- Texto chico a baja resolución puede fallar → mantenerlo corto, alto contraste.

## Fórmula core
`[Style/Medium] + [Subject] + [Environment] + [Lighting] + [Composition] + [Technical Specs]`
Complejo: Style → Subject → Environment → Lighting → Composition → Text requirements → Color → Aspect ratio.

## Best practices
- **Escribir como director, no lista de keywords.** Bad: "beautiful woman, 8K, masterpiece". Good: "A portrait of a woman in her late twenties, lit by a single softbox from camera-left…".
- **Front-load** lo importante (el modelo pesa las primeras ~50 palabras): estilo, sujeto, mood al inicio.
- **Constraints negativos** solo si hace falta al final: "No text overlay, no watermark, no border."
- **Siempre especificar aspect ratio al final:** `Aspect ratio [x:x].` (9:16 vertical social, 16:9 horizontal, 3:4/4:5 editorial, 1:1 feed, 2.39:1/3:1 cine, 2:3 poster).
- **Iterar en la misma conversación:** "Make the sky more dramatic", "Shift subject to left third", "Change typography color to gold".

## Texto en imágenes (el superpoder)
Reglas: copy exacto verbatim (no dejar que invente) · posición (upper-left, centered, bottom-right) · font style (bold sans-serif, elegant serif, handwritten, condensed display) · color y contraste (white on dark) · líneas cortas · para spelling crítico añadir "Text must be sharp, legible, and correctly spelled."
Template: `The [position] of the image displays the text "[EXACT COPY]" in [font style], [color], on a [background].`

## Playbooks por caso
1. **Cinematic portrait:** Style→Lighting→Subject→Mood→Camera→AR. Nombrar setup de luz, mood anchor ("like a still from a Denis Villeneuve film"), contraste de sombras, foco.
2. **Poster/ilustración con texto:** Mood→Background→Visual→Composición→Texto→AR. Nombrar layout (S-curve, radial, grid), listar cada elemento, negative space, texto verbatim.
3. **Character reference sheet:** nombrar cada vista (front/side/back/3/4), estados de expresión, swatch de paleta, fondo blanco limpio, grid.
4. **UI/social mockup:** nombrar device+OS, cada elemento UI, texto verbatim, string inusual como accuracy check, dark/light mode.
5. **Creative/narrativo:** concepto fuerte con anclas, textos que estresen el render, estilo de ilustración claro, tono.

## Output obligatorio (por request)
1. Director's read (1 frase) · 2. Prompt strategy (qué playbook y por qué) · 3. Final prompt en inglés listo para pegar · 4. Text accuracy notes · 5. 2-3 iteration suggestions.

## Self-repair checklist
Style en la 1ª frase · sujeto físico concreto · fuente y calidad de luz nombradas · estrategia de composición · aspect ratio al final · si hay texto: copy exacto + posición + legibilidad · sin keyword filler · un solo mood anchor · no prometer logo exacto.

## Fortalezas/debilidades
Excelente: poster multi-línea (95%+), UI mockup legible. Fuerte: retrato cine, infografía con reasoning. Bueno: character sheet. Débil: logo de marca exacto (componer en post), control fino de estética fílmica, iteración rápida (esperar 30-60s).
