---
name: asset-extraction
title: "Asset Extraction"
author: highriseseal1504
category: Content Creation
source: https://higgsfield.ai/supercomputer/marketplace/skills/08443c6d-3c75-472c-b847-ab6d32f83655
extracted: modal SKILL.md (via claude-in-chrome) — single file, sin references
---

# Asset Extraction Workflow
Cuando el usuario pide PNGs aislados, elementos UI u objetos con fondo transparente.

## Trigger
- Pide cards/objetos/elementos con fondo transparente.
- Se queja de bordes pobres o detalle perdido al usar `higgsfield_remove_background` directo sobre una escena compleja.
- Necesita superponer varios elementos generados limpiamente (compositing).

## Pasos
1. **Generar sobre chroma-key verde:** en vez de extraer un objeto de una escena compleja, generar el objeto *solo* sobre green screen (`higgsfield_generate_image`, `gpt_image_2`). En el prompt:
   - "isolated on a solid, uniform, bright chroma-key green background."
   - "Absolutely NO shadow, no glow, and no lighting gradient on the background. The green background must be perfectly flat/uniform."
   - "Razor-sharp, extremely clean, distinct, and well-defined borders against the green background."
   - Para cards UI: "flat, perfectly straight (0 degrees rotation)".
2. **Remover fondo:** pasar el `media_id` del green-screen a `higgsfield_remove_background` (fondo uniforme = corte perfecto).
3. **Entregar:** subir el output con `higgsfield_upload` y entregar el PNG transparente.

## Pitfalls
- **Baking drop shadows:** si el prompt incluye "soft drop shadow", la sombra cae sobre el verde y arruina el corte.
- **Objetos superpuestos:** si necesitás assets individuales, generarlos en requests 1:1 separados, no todos agrupados.
