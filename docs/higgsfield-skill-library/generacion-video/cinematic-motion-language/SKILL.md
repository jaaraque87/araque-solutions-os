---
name: cinematic-motion-language
title: "Cinematic Motion Language"
author: tariki
source: https://higgsfield.ai/supercomputer/marketplace/skills/5bb14576-3d59-4478-8755-7eab4ba5582a
extracted: modal SKILL.md (via claude-in-chrome)
note: tiene references/implied-off-screen-motion.md (ver aparte).
---

# Cinematic Motion Language
Sistema de lenguaje de 5 pilares para prompts de video de precisión cinematográfica. **Principio core:** reemplazar cada descriptor vago por una analogía física, coordenada espacial, medida temporal o restricción — el modelo entiende física, geometría, secuencia y constraint, NO adjetivos.

## Los 5 pilares
1. **Camera Contract:** declarar el comportamiento de cámara como regla dura ANTES de todo. Ej: "Static locked-off camera. Zero movement. No pan, no zoom, no dolly, no shake." · "Slow push-in only — 10% scale change over the full duration." Reforzar siempre en el negative prompt.
2. **Motion Physics Anchor:** dar a cada elemento en movimiento una referencia de velocidad del mundo físico, no un adjetivo. Analogías: "like dust suspended in honey", "like embers floating in still air". Medidas temporales: "one full revolution across the 10-second clip", "the pace of a clock's hour hand". **Nunca** usar "slow/fast/gentle/subtle" solos.
3. **Spatial Zoning:** dividir el frame en regiones nombradas con reglas explícitas. Ej: "Left third: pure black, no light, no particles, no movement." · "Right two-thirds: all action contained here." Cross-referenciar en negative prompt.
4. **Lens Behavior Sequence:** describir foco/DoF como evento narrativo (trigger → shift → state → return → repeat). Vocabulario: shallow DoF, focus-breathing, rack focus, bokeh silhouette, lens plane crossing, anamorphic rendering.
5. **Negative Space as Compositional Tool:** nombrar áreas vacías como decisiones de diseño intencionales. "Sacred emptiness — the left third is a deliberate compositional weight." Reforzar en negative prompt.

## Template de prompt
```
CAMERA: [static / push / drift / handheld — regla dura]
ASPECT RATIO: [21:9 / 16:9 / 9:16]
DURATION: [X seconds]
Style & Mood: [registro visual + atmósfera en una línea]
Narrative: [una frase — qué pasa]
Action:
- Subject: [quién/qué, posición en frame, estado emocional]
- Motion: [speed anchor — analogía física + medida temporal]
- Secondary motion: [partículas/tela/humo — su propio anchor]
Lens:
- Focal feel: [wide / normal / telephoto]
- Focus event: [cause → shift → state → return → repeat]
- DoF: [shallow / deep / breathing]
Lighting: [nº de fuentes, dirección, calidad, temperatura de color]
Spatial Zones:
- [region]: [rule]
Audio: [textura de sonido, no género musical]
Quality suffixes: [photoreal, film grain, anamorphic, 8K detail]
Negative Prompt: [movimientos de cámara, violaciones espaciales, rechazos de estilo, violaciones de movimiento]
```

## Vocabulario clave
- **Cámara:** static locked-off / handheld drift / slow push-in / crane reveal / whip pan / zero movement.
- **Velocidad:** suspended in honey / floating in still air / cathedral smoke / hour-hand pace / imperceptibly slow.
- **Lente/foco:** shallow DoF / focus-breathing / rack focus / bokeh silhouette / lens plane crossing / anamorphic.
- **Luz:** single key light / directional warm / chiaroscuro / golden-amber / deep shadow / no fill / no ambient.
- **Negative space:** sacred emptiness / pure black void / no light bleed / deliberate composition.

## Ejemplo trabajado — Dervish Shot
Camera: Static locked-off, zero movement. Motion anchor: la mano traza un arco de rotación completo en 10s (pace de la aguja horaria). Lens event: partículas cruzan el lens plane → foco a partículas (sharp, glowing) → mano se suaviza a bokeh. Zonas: left third negro puro / right two-thirds toda la acción / foreground plane capa de partículas. Luz: single warm key desde arriba-derecha, chiaroscuro profundo, golden-amber sobre negro. Negative: camera movement, pan, zoom, dolly, shake, fast motion, particles on the left side.
