---
name: hf-higgsfield-brand-visual-kit
title: "Higgsfield Brand Visual Kit"
author: visual_intelligence
category: Creative-marketing
users: 57
source: https://higgsfield.ai/supercomputer/marketplace/skills/a94d7b61-1470-4a8f-9b33-bdd5ee6257bd
extracted: modal SKILL.md (via claude-in-chrome) — single file
relevante: alto — consistencia visual de marca a escala en Higgsfield (aplicable a proyectos como POTROS/Milivoy)
description: "Sistema de consistencia visual de marca: routing de modelos, vocabulario de color, iluminacion, negativos y templates. Usar al definir el look de marca de un cliente de la agencia."
---

# Higgsfield Brand Visual Kit
Arquitecto de sistema de identidad visual: toma un brand brief y produce un **kit de prompts reusable** para consistencia visual en generaciones múltiples de Higgsfield (product shots, UGC, talking heads, campaña). NO genera imágenes — genera el sistema de prompts.

## Step 1: Brand brief intake (6 inputs — pedir lo que falte)
Brand name + categoría · Visual reference (2-3 adjetivos o imágenes) · Color palette (hex si se conocen, o en palabras) · Primary use cases (qué outputs necesitan) · What to avoid (elementos off-brand) · Character/spokesperson (sí/no, y si usa Soul ID).

## Step 2: Model Routing
| Content type | Modelo | Por qué |
|---|---|---|
| Product hero shots | Nano Banana Pro / Nano Banana 2 | mejor prompt adherence, color locking |
| Lifestyle/editorial | Soul 2.0 / Soul Cinema | Soul Cinema añade film grain + color depth |
| Brand character/spokesperson | Soul 2.0 + Soul ID | Soul ID lockea identidad |
| Cinematic campaign clips | Veo 3.1 Standard | máxima fidelidad, reference-to-video |
| UGC/social video | Veo 3.1 Fast / Kling 3.0 | iteración rápida |
| Talking head video | Lipsync Studio + Veo 3 | image→Soul ID→Veo 3 lipsync |
| Product placement/compositing | Banana Placement / Canvas | poner producto en escenas nuevas |
| High-volume social iterations | Seedance 2.0 | testear múltiples hooks/fondos |
**Regla:** nunca correr contenido de campaña por modelos Lite/Fast; reservar Standard/quality tier.

## Step 3: Color Palette Vocabulary (lo más importante para consistencia)
**Especificación de 3 capas (siempre en este orden):** 1. Background/environment color (tono dominante). 2. Key light color (fuente principal: cool/warm/neutral/gel). 3. Accent color (producto/ropa/prop que lleva la marca).
Ej skincare (ivory/sage/gold): Background "warm ivory linen surface, off-white matte background" · Key light "soft warm daylight from single window, no harsh shadows, cream diffusion" · Accent "matte gold packaging, dusty sage foliage accent, no additional colors".
**Soul Cinema color locking:** agregar línea de hex — `Color grading: match #F5EFE6 base tone, #8FAF8C sage accent, desaturated warm cast throughout`.

## Step 4: Default Lighting Setups (3 nombrados y reusables)
Naming: `[BrandName] Light 1: [función]`. Template: Light 1 — Hero Product (single soft source, temp+dirección, difusión, sin sombras duras, fill, fondo) · Light 2 — Editorial Lifestyle (ambient, source, shadow character, temp, atmósfera) · Light 3 — Cinematic Campaign (dramático, rim vs key, separación de fondo, gel, mood).

## Step 5: Negative Prompt Library
Base (todas las marcas): `low quality, blurry, watermark, text overlay, extra limbs, deformed hands, inconsistent lighting, over[saturated]...`. Agregar brand-specific: off-palette colors (+neon, oversaturated) · off-brand moods (dark, gritty, clinical, cheap, busy background) · off-brand aesthetics (generic stock photo, flat lighting, artificial skin).

## Step 6: 5 Prompt Templates reusables
Estructura: `[Shot type], [subject con color vocabulary], [action], [environment con paleta], [named lighting], [texture/material], [mood] // Negative: [library]`. Los 5: Hero product shot · Lifestyle con talent · Ingredient/detail · Cinematic campaign clip (Veo 3.1 Standard + reference image + Audio line) · Social/UGC vertical 9:16.

## Consistency Maintenance Rules
Siempre subir reference image con Veo 3.1/Soul Cinema (el texto solo deriva) · lockear el string de color vocabulary (copiar verbatim, no parafrasear) · Soul ID para cada humano recurrente (construir el profile antes de generar video) · nombrar el lighting setup en el prompt · testear la negative library primero (4 gens con y sin negatives).

## Output — BRAND VISUAL KIT (documento estructurado)
Model Map · Color Vocabulary (primary/secondary/accent/forbidden) · Lighting Setups (Light 1/2/3) · Negative Prompt Library (string completo) · Prompt Templates 1-5 con placeholders.

## What it does NOT do
No genera imágenes/videos (solo el sistema de prompts) · no garantiza consistencia (modelos probabilísticos, minimiza drift) · no cubre plataformas no-Higgsfield · no hace brand strategy/logo/identidad no-visual.
