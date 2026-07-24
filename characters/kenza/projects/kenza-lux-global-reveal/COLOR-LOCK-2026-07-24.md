# KENZA-BUSA-01 — Color Lock

Date: 2026-07-24

## Canon

- Master accent material: metallic fuchsia `#F22987`.
- Master motorcycle plates:
  - `00-kenza-busa-canon-blue-hour.png`
  - `01-ignition-blue-hour-v2.png`
- Lighting may change brightness and reflections, but the painted accent must
  remain in the same fuchsia hue family. It must not become racing red, orange,
  purple, or a different pink.

## Corrected V3 plates

Use these instead of their V2 counterparts:

- Shot 2:
  `02-kenza-front-breeze-v3-colorlock.png`
- Shot 6 start:
  `06a-kenza-hair-start-v3-colorlock.png`
- Shot 6 end:
  `06b-kenza-hair-end-v3-colorlock.png`
- Shot 7:
  `07-origin-global-blue-hour-v3-colorlock.png`

Shot 5 does not expose motorcycle fairing paint and needs no color correction.

## Method

The V3 files use a deterministic hue lock restricted to the visible motorcycle
area. The method preserves:

- motorcycle geometry;
- fairing-line placement;
- wheels and controls;
- Kenza's face and body;
- wardrobe;
- camera position;
- background and exposure.

Generative color-edit tests were rejected because they changed motorcycle
geometry. Do not use generative inpainting merely to correct the fairing color.

## LTX rule

All prompts must include:

> Preserve the exact metallic-fuchsia `#F22987` accent lines and rim pinstripes
> from the source plate. Do not shift them toward red, orange, purple, or another
> pink. Do not redraw or relocate any stripe.

The LTX output must be rejected if the fairing color or stripe placement changes
between frames.
