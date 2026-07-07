---
name: higgsfield-prompt-architect
title: "Higgsfield Prompt Architect"
author: visual_intelligence
category: custom (Creative & Marketing)
source: https://higgsfield.ai/supercomputer/marketplace/skills/93583be6-aab1-4242-b1ec-34ac01a85414
extracted: modal SKILL.md (via claude-in-chrome) — single file, sin references
---

# Higgsfield Prompt Architect
Capa de selección de modelo y estructura de prompt para Higgsfield. Trabaja junto a: `cinematic-motion-language` (prompts de video con motion/lens), `cinematic-scene-generation` (ángulos/insertos desde una imagen ref).

## Step 1 — Selección de modelo
El error #1 es el mismatch de modelo.
**Imagen:** Soul 2.0 (fashion editorial, retrato, aesthetics culturales, beauty, lifestyle) · Nano Banana Pro (producto, lifestyle, food, still life, e-commerce) · Soul Cinema (retrato cinematográfico, personaje dramático, single-frame film-quality) · Flux 2 / Flux Kontext (artístico, concept art, stylized, diseño gráfico) · Seedream 5 / 4.5 (imagen comercial, color vibrante, ilustrativo) · GPT Image 2 (cualquier imagen con **texto legible** — infografías, branded assets, posters) · Wan 2.2 Image (fotografía painterly, fine art portrait, profundidad cinematográfica).
**Video (guía rápida):** Cinematic narrative/film → Cinema Studio 3.0 · Ads/UGC/talking heads/product demos → Seedance 2.0 · Movimiento de personaje suave/realismo físico → Kling 3.0 / 2.5 Turbo · Escenas atmosféricas/entornos/naturaleza → Veo 3.1 · High-concept/surreal → Sora 2 · Anime/stylized/motion expresivo → Wan 2.5 / 2.6.

## Step 2 — Arquitectura del prompt (en este orden)
1. SUBJECT (quién/qué, específico) · 2. ACTION/STATE · 3. ENVIRONMENT · 4. LIGHTING (calidad, dirección, temperatura) · 5. MOOD/TONE · 6. COLOR PALETTE · 7. TECHNICAL (lente, aspect ratio, params).
La diferencia entre genérico y sobresaliente está casi siempre en la **línea del sujeto** (edad, expresión, ropa específica, postura, estado emocional).

## Step 3 — Vocabulario de imagen
**Luz:** Golden hour (ámbar cálido, sombras largas) · Blue hour (azul/púrpura, melancolía) · Hard directional (sombras duras, drama) · Soft diffused/overcast (parejo, flattering) · Rim/backlight (separación, halo) · Practical (fuente visible en cuadro) · Chiaroscuro (contraste extremo, painterly) · Neon/gels (vibrante, urbano) · Rembrandt (triángulo de luz, gravitas).
**Paleta:** warm/golden (nostalgia, lujo) · cool (moderno, clínico, noche) · teal & orange (Hollywood, comercial) · desaturado/muted (editorial, serio) · pastel/washed (dreamy, feminino) · monocromo · neon/vibrante (nightlife, Gen Z) · earth tones (orgánico, natural).
**Textura (Nano/Soul):** fabric (brushed cotton, washed denim, raw silk) · skin (natural texture, pores visible, no retouching) · surfaces (matte anodized aluminum, hand-thrown ceramic, weathered oak, polished marble).

## Step 4 — Aspect ratios
1:1 (grid IG, producto) · 4:5 (feed IG óptimo) · 9:16 (TikTok/Reels/Shorts) · 16:9 (YouTube/desktop/ads horizontales) · 21:9 (cine ultra-wide) · 2:3 (print, Pinterest, editorial).

## Step 5 — Diagnóstico de generación fallida
| Síntoma | Causa | Fix |
|---|---|---|
| Genérico/olvidable | sujeto vago | agregar edad, expresión, ropa, postura, estado |
| Luz plana/fake | sin dirección de luz | golden hour / hard key upper-left / backlight |
| Fondo desordenado | sin dirección de fondo | "shallow DoF, background soft bokeh" o nombrarlo |
| Estética equivocada | mismatch de modelo | cambiar modelo (Soul cultural, Flux artístico) |
| Colores turbios | sin paleta | agregar temperatura/tono/grading |
| Texto ilegible | modelo equivocado | GPT Image 2 + placement explícito |
| Motion antinatural (video) | sin descriptor de movimiento | invocar cinematic-motion-language |
| Anatomía rota (manos/cara) | artefacto generativo | negative prompt; Edit/inpainting quirúrgico |
| Prompt largo incoherente | sobre-especificación | recortar a los 10 descriptores clave |
| Estilo deriva entre gens | sin ancla de estilo | referencia estética en una frase, primera en el prompt |

## Output Format
```
HIGGSFIELD PROMPT BLOCK
Model: [modelo] · Type: [Image/Video] · Aspect ratio: [ratio]
Prompt: [subject → environment → lighting → mood → color → technical]
Negative prompt: [issues, style rejections, artifacts]
Variation A: [misma sujeto, otra luz/mood]
Variation B: [misma intención, otro modelo]
Skill handoff: → cinematic-scene-generation / cinematic-motion-language
```

## Workflow
1. Identificar goal (imagen/video, foto/stylized, producto/retrato/escena). 2. Elegir modelo (+1 frase de rationale). 3. Construir prompt (subject-first). 4. Output del Prompt Block (2 variaciones + handoff). 5. Diagnosticar si muestran un fallo.
