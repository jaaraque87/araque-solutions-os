---
name: storyboard-generation
title: "Storyboard Generation"
author: otty
category: Personal And Specialized
source: https://higgsfield.ai/supercomputer/marketplace/skills/111b3559-685b-45df-80aa-e9b7f8cc124b
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# Storyboard & Presentation Slide Generation
Reglas para generar slides de presentación y storyboards multi-panel (típicamente con `imagegen_2_0`).

## Reglas
- **Strict Containment:** el prompt debe instruir explícitamente que TODAS las photo cards, bloques de texto y elementos UI queden enteramente dentro del slide. Ej: "All photo cards fully inside slide boundaries, nothing cropped."
- **Resolution & Aspect Ratio:** usar `aspect_ratio: "16:9"` (o el formato pedido) y `resolution: "1k"` o `"2k"` (1080p) con `imagegen_2_0` para legibilidad de texto y layouts nítidos.
- **Layout Definition:** delinear filas y columnas en el prompt. Ej: `LAYOUT: 2 rows. Row 1: two equal columns (E1 left, E2 right)...`
- **Reference Adherence:** si se replica/modifica un layout existente, instruir mantener el layout exacto.
- **Timeline Bars:** para shot continuo o secuencia multi-escena, pedir barra de timeline gradiente. Ej: "Timeline bar at very bottom: gradient line from left (slow) to right (fast), labeled..."
- **Consistency:** mantener luz, hora del día y contexto ambiental consistentes entre paneles del mismo slide.
- **Complex Storyboards (Film/Video):** usar un prompt JSON estructurado con directivas estrictas de formato (ej. fondo `#1a1a1a`).
- **Camera Movement Overlays:** pedir explícitamente flechas y diagramas dibujados directamente sobre los paneles ("curved cyan arc arrow showing orbit", "bold arrow...").
- **Empty Panels for Re-use:** para un panel placeholder estructural: "COMPLETELY EMPTY dark panel — solid dark charcoal background, NO photo, NO person, NO image. Just the frame."
