---
name: static-ads
title: "Static Ads"
author: manet_tomato
category: Content Creation
users: 452
source: https://higgsfield.ai/supercomputer/marketplace/skills/7baf8471-6a41-476a-bb21-18d111a8b908
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): generate-static-ad.py, generate-reformat.py
---

# Static Ads
Recrea un formato de ad ganador con el producto y copy propios de la marca. Output a `./brands/[brand-name]/static-ads/[output-name]/`.

## Workflow (10 steps)
**Step 1 — Select brand:** escanear `./brands/` por subfolders con `brand-identity/visual-guidelines.md`. Uno→usar y confirmar; varios→preguntar; ninguno→correr `/brand` primero.
**Step 2 — Upload ad format reference:** `mkdir brands/[brand]/static-ads/ad-references`, pedir al usuario que suelte el ad a recrear. Leer con Read tool y analizar INTERNAMENTE (no compartir): ad format type · layout structure · typography · copy framework (cada text slot y su rol) · product placement · brand signals. **Extraer layout zones** como fracciones de altura (0.0=top, 1.0=bottom): `text_zone`, `product_zone`, `button_zone`, `disclaimer_zone`. Ej: text 0.10-0.35, product 0.40-0.77, button 0.81-0.91, disclaimer 0.91-0.97.
**Step 3 — Product(s) + copy variation count:** buscar imágenes en orden: local (`product-images/`, `uploads/`) → website de la marca (`products.json` → WebFetch → curl download) → pedir al usuario. Mostrar qué se usará.
**Step 4 — Generate copy variations:** leer `visual-guidelines.md` + `products.json`; WebFetch la product page (fuente de verdad para benefits/claims/ingredientes/tono). Presentar variaciones numeradas mostrando SOLO los copy slots. Pedir "confirmed" o edits.
**Step 5 — Aspect ratio:** default 4:5; opciones 1:1, 3:4, 9:16, 16:9. Preguntar primario + adicionales.
**Step 6 — Name output:** slug formato-producto (ej. `iMessage-energy-gel`, `countdown-magnesium`).
**Step 7 — Create folder + write spec:** `static-ad-spec.json` con output_name, brand, product_name, reference_image, layout_zones, product_images, aspect_ratio, additional_aspect_ratios, variations (slug+prompt zone-based).
**Step 8 — Generate:** `python3 skills/references/generate-static-ad.py brands/[brand]/static-ads/[output-name] var-1` (una por variación). Product images = Image 1,2... a GPT-image-2. ~$0.12/imagen.
**Step 9 — Reformat** para aspect ratios adicionales (`generate-reformat.py`). No mencionar al usuario.
**Step 10 — Present:** listar files generados, ofrecer regenerar/ajustar copy/otro formato.

## Structure vs Brand (la regla central)
El ad de referencia es de OTRA marca — tratarlo SOLO como template estructural, nunca copiar sus elementos visuales.
- **Tomar de la referencia:** layout format, posiciones/proporciones de zonas, tipos de UI (toggles, countdown blocks, message bubbles).
- **Tomar de `visual-guidelines.md`:** TODO lo visual — background color, typeface/weights, accent colors (CTA, iconos). Antes de escribir cualquier prompt, leer visual-guidelines y nombrar explícitamente bg color + headline typeface de la marca.

## Prompt Construction (2 modos)
- **Mode A — Reference swap** (reference_image presente): Image 1 es el ad de referencia; override explícito de TODOS los elementos visuales de marca. "Use it as a structural template only — keep the layout format... override all colors/fonts with [brand]."
- **Mode B — Text-driven layout** (sin reference_image): product images son Image 1,2...; el prompt lleva todo el layout/brand/copy zone-by-zone.
- **Safe zones aplican a todo prompt en todo modo, sin excepción.**

## Prompt Template Reference (por formato)
iMessage/DM Conversation · Scarcity/Countdown Urgency · Ingredient Spotlight/Clean Label. Todos: "Use the attached images as brand reference for product design ONLY. Do NOT use polished ad layouts. Match exact product design/colors/typography..."

## Notes
El copy se ancla en la product page live (via product_url en products.json); el tono en visual-guidelines.md; correr `/brand` primero si faltan. El prompt template derivado del ad subido NUNCA se muestra al usuario (solo en el spec). Cada marca tiene su subfolder — múltiples marcas corren workflows independientes.
