---
name: vinyl-print-graphics
title: "Vinyl Print Graphics"
author: kantenparis
category: Personal & Specialized
source: https://higgsfield.ai/supercomputer/marketplace/skills/b2136a41-8ca9-4490-b9bb-c5172ad4a606
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# Vinyl, Silhouette/Cricut Plotter & Silkscreen Design Guide
Workflow y prompts para generar diseños vector-compatibles listos para HTV, plotter de vinilo, serigrafía, stencils, stamps.

## Trigger
"HTV" / "Heat Transfer Vinyl" / "vinyl" / "plotter" / "cutter" / "Cricut" / "Silhouette" / "Silkscreen" / "screen printing" / "sérigraphie" / "stencil" / "stamp" / "linocut" / "woodblock print" (cuando el output es un gráfico standalone de print/apparel).

## Directivas operativas
**1. Regla vector-compatible (dura):** el corte físico de vinilo/serigrafía requiere **áreas planas y conectadas de tinta sólida**.
- **Fondos:** SIEMPRE especificar "flat, solid, plain white background" o "solid black background". Nunca grano de papel, drop shadows, foto.
- **Tinta/gráfico:** "solid pure black artwork", "high contrast monochrome vector graphic style", "flat 2D silhouette design".
- **Zero thresholding room:** decir al modelo "no grays, no colors, no gradients, no shading, no drop shadows, no t-shirt mockup, no fabric texture".

**2. Weeding & line-weight safeguards:** al cortar, un humano "weed"-ea el vinilo sobrante; líneas muy finas/sueltas se caen.
- **Stroke weight:** "thick clean lines, bold geometric solid paths, high contrast silhouettes".
- **Structural integration:** para diseños intrincados (spokes radiales, op-art, grids): "make paths continuous, avoid floating dust particles, widen fine lines for clean cuts, ensure lines connect".

## Ejecución
**Step 1 — Modelo:**
- `imagegen_2_0` (quality:high, resolution:2k) si requiere: tipografía precisa/coordenadas/brand names · ejes arquitectónicos, grids, rulers, borders · formas geométricas perfectas, simetría matemática.
- `nano_banana_2` (resolution:2k) si requiere: ilustración orgánica/hand-drawn, retratos, stencils, líneas botánicas · modificar/redirigir estilo de un gráfico subido.

**Step 2 — Prompt (4 pilares):** Subject · Style (monochrome vector, flat 2D screenprint, high-contrast silhouette, op-art bold line art) · Instructions (grid, border, tipografía, fuerza de línea) · Constraints ("no colors, no gray, no gradients, no shadows; background solid flat").

## Pitfalls → fix
| Pitfall | Causa | Fix |
|---|---|---|
| Tipografía borrosa/pixelada | settings estándar borronean letras chicas | forzar `imagegen_2_0`, quality high, resolution 2k |
| Gradientes/halftones | stippling o densidades de puntos que la cuchilla no corta | "absolutely no stippling, no screentones, no halftones, no tiny dots, solid black shapes only" |
| Specks flotantes sueltos | elementos desconectados se caen en la transferencia | "ensure all elements connect to a main central structure/axis/line, merge floaters" |
| Mockup en remera | el modelo pone el gráfico sobre una remera arrugada | "no garment mockup, no t-shirt mockup, no human model, flat scan design only" |

## Scaffolding de ejemplo (técnico/urban minimalist)
```
[Subject]: A minimalist 2D industrial graphic. Centered is [core subject].
[Style]: High-contrast monochrome vector style, clean flat black ink and pure white space.
[Instructions]: Bold and distinct geometric linework. A thin vertical structural axis runs alongside.
[Constraints]: Absolutely flat scan. Plain solid white screen background. No color, no gray, no halftones.
```
