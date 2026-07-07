# Graffiti — neón dibujado sobre la escena oscurecida

**Cuándo usarlo:** energía nocturna/urbana con clase; temas tech con actitud; cuando la
escena real del clip suma (no se reemplaza el fondo: se APAGA y se pinta encima).
**Fuente:** disección preview Shorts Studio "Graffiti" (Higgsfield) 2026-07-05 ·
**Validado:** parcial (test 2026-07-05: mundo/motivos/encuadres ✓ — los 5 motivos neón
incluida la secuencia túnel salieron bien y el filtro lo deja pasar. GAP: el ambiente no
oscureció lo suficiente, la escena queda muy presente en vez de silueta; el próximo uso
refuerza 'the room lights DROP almost completely, near-total darkness' o corrige por
turn-by-turn)

## Bloque de estilo (va literal en el prompt, en inglés)

Keep my talking face, lip-sync and real footage exactly as they are — my real scene
(desk, laptop, mic) stays but the whole environment DARKENS to near-black, lit only by
me, as if the room lights dropped. Over and around this darkness, GLOWING NEON GRAFFITI
draws itself in real time: fluorescent paint strokes, neon wireframe doodles and glowing
scribbles in hot pink, electric blue, acid green, yellow and red — hand-drawn energy,
visible draw-on animation, soft neon glow and slight bloom. The real scene stays faintly
visible in silhouette. Never flat vector: everything glows like real neon and wet
fluorescent paint on black.

## Estados de fondo

Un motivo de neón por frase, redibujándose en cada beat (el draw-on ES la transición):
trazos rosa fluor / wireframe de objeto literal (monitor, etc.) azul-naranja / scribbles
verdes-rosas rodeando la cabeza / TÚNEL de marcos concéntricos azul-amarillo en
perspectiva (el beat más espectacular — usarlo en el beat de mayor peso) / círculos
concéntricos blancos + trazos rojos. Rotar motivos entre clips de una serie.

## Sujeto: reframing dirigido

Igual que Patterned: posición y escala cambian por beat CON LÓGICA DECLARADA derivada
del guion (close = claim/remate; chico dentro del túnel = beat de contexto/asombro;
medium = desarrollo). El cambio de encuadre cae junto con el redibujado del neón.
Escribir la lógica en una línea en el prompt doc antes de generar.

## Captions (POST — nunca via Omni)

Frase acumulativa en blanco, tipografía marker/brush manuscrita bold con glow suave
(text-shadow blanco + leve bloom), centrada en tercio bajo, sin caja. Quemadas en post
con timestamps medidos (arquitectura de dos capas: Omni NO genera texto).

## Doodads

Los dibujos de neón SON los doodads: el objeto literal a la frase se dibuja como
wireframe de neón (monitor, manito, átomo) en POSICIÓN VARIABLE por beat — arriba,
costado, esquina — nunca siempre centrado.

## Refs

`refs/ref_*.jpg` (preview original). Solo lectura para el prompt — NO adjuntar como
IMAGE_REF (tiñe al sujeto).

## QA específico

- La escena real debe seguir leyéndose en silueta (si desaparece del todo, es otro estilo).
- El neón debe tener glow/bloom real, no líneas vectoriales planas.
- Draw-ons sincronizados a arranques de frase; cara siempre iluminada y legible.
- TEXT RULES estrictas en el prompt: cero texto de Omni.
