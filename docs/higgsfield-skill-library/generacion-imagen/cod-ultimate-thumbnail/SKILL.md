---
name: cod-ultimate-thumbnail
title: "Cod Ultimate Thumbnail"
author: gothic_butterfly_turbo
category: Content Creation
source: https://higgsfield.ai/supercomputer/marketplace/skills/1036bbd9-2fbe-4452-ae57-3b7e2cca201c
extracted: modal SKILL.md (via claude-in-chrome) — single file
note: workflow personal/nicho (miniaturas de Call of Duty para el creador "Quix").
---

# CoD Ultimate Thumbnail Workflow
Pipeline de producción para Quix: render 3D + compositing de entorno + enhancement agresivo. Trigger: el usuario da un screenshot de arma (y opcional un fondo) y pide una miniatura.

## Pipeline
**Fase 1 — Blender Render:** modelo `nano_banana_2`. Convertir gráficos planos del juego en render fotorreal estilo Blender Cycles. PBR materials (metales glossy, glows emisivos, SSS en plásticos), three-point lighting (soft key, fill, rim). Look: "Blender Cycles path-traced render, ultra-detailed photorealistic 3D model."
**Fase 2 — Composite:** `imagegen_2_0` (o `nano_banana_2` si importa preservar píxeles exactos). Colocar el render en el fondo; matchear temperatura de color y dirección de luz del entorno al arma/manos.
**Fase 3 — Quix Enhancement:** foreground (arma) sharpening agresivo, bordes razor-crisp; background vibrante con leve radial zoom blur para enfocar el arma; SIN viñeta (Quix prefiere limpio, brillante, punchy).

## Prompt unificado (pass 1)
```
Composite the weapon inspect from reference 1 onto the environment in reference 2.
RE-RENDER the weapon as a high-end 3D Blender Cycles render:
- Transform the [camo] into a PBR material with metallic reflectivity and soft emissive glows.
- Preserve the exact first-person silhouette and hand placement from reference 1.
- Apply studio lighting to the weapon: soft highlights on upper surfaces, subtle rim light.
ENVIRONMENT & COMPOSITION:
- Place the weapon naturally into the [background map] from reference 2.
- Match lighting color temperature and direction from the background onto weapon/hands.
- Foreground weapon aggressively sharpened, razor-crisp.
- Slight radial zoom blur on the background to draw focus to the weapon.
- Boost vibrancy/saturation, sky vivid, background environment slightly controlled.
Absolutely NO text, NO UI, NO HUD, NO minimap, NO vignette, NO dark edges. Clean YouTube thumbnail.
```

## Modelo/params
Generator: `imagegen_2_0` (GPT Image 2, mejor control texto/detalle y preservación de silueta) o `nano_banana_2`. Resolución alta (obligatorio para el sharpness de Quix). Quality: high. Aspect: 16:9.
**Medias:** [0] = screenshot arma; [1] = screenshot fondo/mapa.

## Pitfalls
No sobre-blurear el fondo (subtle). El foco es el arma (sharpening/contraste centrados ahí).
