---
name: premium-ad-posters
title: "Premium Ad Posters"
author: highriseseal1504
category: Content Creation
users: 7
source: https://higgsfield.ai/supercomputer/marketplace/skills/afffa734-d5f3-4cd7-93de-2566ad3ea25a
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): examples.md
---

# Premium Ad and Poster Design
Reglas y prompts para generar posters promocionales high-end, ad creatives retail/tech, Meta Ads.

## Model Route
- **Primary: `imagegen_2_0` (GPT Image 2.0)** — los posters viven o mueren por fidelidad de tipografía, precisión de hardware, disciplina de layout. Forzar `quality:"high"` y `resolution:"2k"` (crucial para texto/glyphs/seams de hardware nítidos).
- **Fallback: `flux_2` (Flux 2) o `nano_banana_2`** — si imagegen_2_0 topa rate limits/safety/unavailable. Para flux_2 usar prompts descriptivos detallados con instrucciones de layout embebidas (no usa control estructural).
- **Aspect ratios:** 1:1 (Meta feed/carousels) · 9:16 (Stories/Reels/TikTok) · 4:5 (IG feed) · 3:4 (poster vertical) · 16:9 (banner landscape).

## Technical & Realism Checklist (steerear activamente al modelo)
1. **Hardware Integrity & Mechanical Symmetries:** problema = smartwatches con bezels asimétricos, coronas warpeadas/"derretidas". Regla: "Perfect mechanical symmetry, uniform bezels, clearly defined mechanical parts. The electronic crown [detalle]..."
2. **Screen-Layer UI Integration (no flat stickers):** problema = gráficos de pantalla que parecen pegados. Regla: "Render the interface beneath the watch crystal glass. Include subtle natural glare, reflection..."
3. **Anatomical Normalcy:** problema = muñecas sin huesos, joints blandos, dedos distorsionados. Regla: "Clearly defined wrist bone anatomy (ulnar protrusion), natural knuckles, realistic skin pores..."
4. **Background Artifact Safeguards:** problema = teclados/gadgets en el fondo con teclas warpeadas. Regla: "Clean uncluttered desk in the background. If any objects like keycaps are in the soft out-of-focus [area, keep proportions correct]."
5. **High-Contrast Typography Layouts:** problema = captions sobre texturas claras sin contraste. Regla: "All text overlay must use clean, modern, dark sans-serif typography with high contrast. Include subtle [shadow/backing]."
6. **Reference Mapping vs Target Format:** cuando dan una referencia estética de OTRO device (ej. iPhone lock screen) para un producto distinto, extraer y mapear SOLO las propiedades estéticas (tipografía, color blocking, texturas, formas de UI) al formato/entorno del producto pedido.

## Prompt Structure Template
```
[Subject/Hero]: [producto + hand/model en detalle nítido, con detalles anatómicos/estructurales para prevenir warping]
[Style]: [premium product photography, soft window light, airy kitchen/office counters, narrow DOF...]
[Instructions]: [mechanical symmetries, watch strap lugs definitions, screen depth realism...]
[Text]: [bloques textuales entre comillas — headline, subline, subtitle — con tamaños/pesos/color exactos]
[Constraints]: aspect ratio [1:1/9:16], no warped buttons, no melted casings, no blurred text, no [artifacts]
```
