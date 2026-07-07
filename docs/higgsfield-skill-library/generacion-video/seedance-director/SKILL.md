---
name: seedance-director
title: "Seedance Director"
author: joshhoole
source: https://higgsfield.ai/supercomputer/marketplace/skills/45486f8e-c46f-43cc-b067-6394023aa9de
extracted: modal SKILL.md (via claude-in-chrome)
note: tiene references/strategy-guide.md (ver archivo aparte).
---

# Seedance Director
Generador de prompts de precisión para video cinematográfico/comercial/artístico con **Seedance 2.0**.

## 🧭 Las 5 Leyes Operativas (ADN de todo prompt Seedance 2.0)
1. **Temporal Anchoring (partición de timeline):** nunca instrucciones abiertas. Cada secuencia dividida por segundos exactos (ej. `(0:00-0:02)`).
2. **Transition Directives:** especificar cómo conectan los planos (`whip pan`, `smash cut`, `match cut`, `continuous follow`).
3. **Camera & Lens Grammar:** focales exactas (`50mm`, `macro`, `anamorphic`) y estados de cámara (`tripod-locked`, `Steadicam drift`, `crane up`, `orbit clockwise`).
4. **Material Physics & Textures:** dictar propiedades (`refractive highlights`, `condensate droplets`, `natural gravity and inertia`).
5. **Global Constraints Block:** reglas positivas y negativas en el prompt (`NO morphing, NO artificial glow, NO extra subjects`).

## 🛠️ Presets estéticos
**Estilos/moods:** Premium Studio Commercial (alto contraste, materiales glossy, fondo oscuro limpio) · Gritty Cinematic Realism (handheld, físicas orgánicas, piel realista) · Surreal & Abstract CGI (partículas, energía, formaciones procedurales) · Artisan Calligraphic Flatlay (top-down, grano de papel, tinta cálida) · Keynote Dark Motion (vector minimalista, gradientes vibrantes, mucho negative space).
**Cámara/lente:** Anamorphic (wide, flares horizontales, bokeh oval) · Macro/Micro (DoF finísima, texturas magnificadas) · Steadicam Float (drift suave constante) · Kinetic Crane Rise (movimiento por momentum) · Locked Focus Pull (tripod estático, foreground→background).
**Iluminación:** Golden Hour Backlight · Neon Noir Studio (teal/azul + neón) · Chiaroscuro (alto contraste, una key raking) · Soft Daylight Overhead (rayos volumétricos, sombras mínimas).

## 📝 Arquetipos de prompt (elegir uno)
**Type A — Chronological Shot List (narrativa multi-shot):** ← el que sirve para el reel de Kumar
```
[STYLE ANCHOR] {estilo, cámara, luz, color grading}
[GLOBAL LOCK] {identidades, outfits, parámetros de consistencia}
Shot 1 (0:00-0:02): {acción, ángulo/movimiento, lente, transición a Shot 2}
Shot 2 (0:02-0:04): {...}
Shot N (Time): {hero hold, frame final, estabilización}
[AUDIO] {SFX y ambiente ligados a timestamps}
[NEGATIVE PROMPT] {low quality, blurry, flat lighting, morphing, face distortion}
```
**Type B — Time-Flow Reveal (producto/CGI comercial):** "Ultra realistic cinematic product commercial of [PRODUCT]…" con bloques 0-3/3-6/6-9/9-12/12-15 sec + AUDIO + NEGATIVE.
**Type C — Dual-Frame Seamless Transition:** puentea dos imágenes (`@Image1` inicio, `@Image2` final) con S1-S5 por segundos + AUDIO + CONSTRAINTS.

## 🚀 Workflow interactivo
1. **Context Gathering:** pedir concepto core; si hay imagen/doc, extraer detalles.
2. **Structural Options Match:** con `ask_user_question` elegir Archetype/Style/Duration (o sugerir el mejor).
3. **Technical Directing:** generar el prompt copy-pasteable en bloque markdown con cinematografía precisa.
4. **Explanation & Handoff:** explicar brevemente las "decisiones directoriales" (por qué tal cámara/timing).
