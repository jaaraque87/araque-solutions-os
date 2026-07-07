---
name: seedance-prompting-skills-for-cinematic-films
title: "Seedance Prompting Skills For Cinematic Films"
author: hokusai_rock_the_mighty
category: Content Creation
users: 1120
source: https://higgsfield.ai/supercomputer/marketplace/skills/72c93716-bb0d-4e29-abf8-82165359570f
extracted: modal SKILL.md (via claude-in-chrome) — single file
relevante: MUY alto — realismo cinematográfico grounded para Seedance 2.0 (la skill más popular de la categoría)
---

# Seedance Prompting — Cinematic Films
Genera prompts de cine fotorrealista para Seedance 2.0. **Cinematic realism se construye desde la contención, no el espectáculo.**

## Cuándo usar
Movimiento cinematográfico fotorrealista: "film-style scene", "realistic body movement", "grounded motion", "emotional close-up", "restrained performance", "driving/intimacy/action scene", "environmental interaction", "continuity reference". NO para animación/cartoon/motion design/UGC/podcast (→ deferir a la skill correspondiente en video-generation).

## Los 5 pilares de grounding (si falta uno → "AI cinema")
1. **Body weight & physics** — los actores tienen masa; el movimiento tiene fricción, momentum, fuerza de contacto.
2. **Environmental force** — viento, agua, gravedad, tela, textura empujan al actor.
3. **Emotional restraint** — micro-expresiones, beats sostenidos, respiración. Nada de telegrafiado facial exagerado.
4. **Camera as observer** — la lente tiene presencia física (peso, respiración, drift). No es un dron ni un dios.
5. **Continuity anchors** — dirección de luz, vestuario, hora del día, posición de props persisten entre shots.

## Estructura de 6 bloques (el ORDEN es load-bearing)
```
[STYLE & MOOD]
[SHOT DIRECTION]
[ACTOR BEHAVIOR]
[ENVIRONMENTAL FORCE]
[CAMERA BEHAVIOR]
[AUDIO]
```

**Block 1 — Style & Mood (1 línea):** léxico de director de foto, film stock/DP si lo dieron. ✓ "35mm anamorphic, naturalistic skin tones, soft window light, muted teal-and-amber palette." ✗ "Cinematic, beautiful, dramatic, epic." (los stacks de adjetivos aplanan).

**Block 2 — Shot Direction (1 oración):** acción destilada: sujeto, verbo, objeto, ubicación. ✓ "A woman in her forties leans against a kitchen counter, reading a folded letter."

**Block 3 — Actor Behavior (2-3 oraciones):** aquí vive el grounding. Siempre incluir: (a) **weight cue** (dónde se asienta la masa: "weight on her right hip", "shoulders dropped"); (b) **micro-action** (movimiento involuntario pequeño: "she swallows", "his jaw tightens once"); (c) **held beat** (quietud con intención). **Prohibido:** "tears stream down her face" → "her eyes glass over; she does not blink"; "he runs furiously" → "he breaks into a run, shoulder leading, arms compact"; "smiles widely" → "the corner of her mouth lifts, then settles".

**Block 4 — Environmental Force (1-2 oraciones):** qué empuja al actor (sin esto = actor en vacío = soundstage). Categorías: Air (viento en pelo/tela/polvo) · Water (peso de lluvia, sheeting) · Gravity (transferencia de peso, hip-shift, contacto silla/pared/piso) · Surface (compliance del piso, textura de pared) · Light source (dónde está, si se mueve: faros que pasan, vela, persianas). ✓ "Wind from the open window lifts the left edge of her hair; the curtain breathes inward once."

**Block 5 — Camera Behavior (1 oración):** la cámara es un cuerpo con peso, intención y límites. Léxico que Seedance entiende: "Locked-off static frame" · "Slow handheld breathing, micro-drift" · "Dolly-in at walking pace, ending in medium close-up" · "Slow push from medium to close-up over 6 seconds" · "Rack focus from foreground hand to background eyes". **Prohibido:** "epic sweeping drone shot" (weightless/videojuego), "cinematic camera movement" (vago→floaty), "360-degree rotation" (rompe continuidad/morph).

**Block 6 — Audio (1 línea):** Seedance genera audio nativo. Ambient primero, luego línea vocal. ✓ "Ambient: distant traffic, refrigerator hum, paper rustling. No dialogue." Silencio: "Ambient: room tone only. No dialogue, no music."

## Patrones por tipo de escena (críticos)
- **Driving (interior):** lockear cámara o handheld muy suave; cámara agresiva en cabina = music video. Luz de faroles barriendo la cara en bandas rítmicas.
- **Emotional close-up:** NO lágrimas ni grief telegrafiado; la performance vive en el held beat y la micro-action. Slow push de medium a tight close-up terminando en los ojos.
- **Action/foot chase:** stride compacto, brazos tucked, hombro liderando; Seedance sobre-renderiza "sprinting" como bouncy action-hero. Handheld a altura de hombro, dos pasos atrás, respirando con la zancada.
- **Intimacy:** se construye desde la NO-acción; resistir agregar beso/lágrima/línea susurrada. Static frame, shallow focus en el punto de contacto (frentes).
- **Environmental interaction (weather as character):** el viento debe moldear MÚLTIPLES elementos (pelo, abrigo, pasto, gaviotas) — viento de un solo elemento = falso.

## Continuity — multi-shot (copiar anchors VERBATIM en cada prompt)
- **Lighting anchor:** misma fuente y dirección ("Late-afternoon window light from screen-left").
- **Wardrobe anchor:** descripción completa idéntica ("Navy wool coat, gray scarf, no jewelry").
- **Time-of-day anchor:** explícito ("Overcast late afternoon, ~4pm light").
- **Geography anchor:** dónde quedó el actor al final del shot previo.
- **Audio bed anchor:** misma firma ambiental en todos los interiores.
Para identidad visual (misma cara entre shots) usar el patrón `<<<element_id>>>` de video-generation.

## Submission (Seedance 2.0)
```json
higgsfield_generate({"requests":[{"type":"generation","model":"seedance_2_0","media_type":"video","params":{"prompt":"<six-block>","duration":8,"aspect_ratio":"21:9","generate_audio":true}}]})
```
Defaults cine: `aspect_ratio` 21:9 (anamórfico) o 16:9; 9:16 solo si piden vertical. `duration` 6-10s single shots, 4-5s hard cuts, 12-15s solo escenas held (intimacy, environmental). `generate_audio` siempre true.

## Failure modes → Fix
| Síntoma | Causa | Fix |
|---|---|---|
| Actor flotando / sin peso | falta weight cue en Block 3 | "weight settled on her right hip" / "hand braced on counter" |
| Pelo/tela/entorno estáticos | falta environmental force (Block 4) | añadir línea de wind/gravity/surface |
| Cara sobre-actuada | verbos "cries/smiles widely/rages" | micro-actions: "swallows once", "corner of mouth lifts then settles" |
| Cámara vuela/swoops | "sweeping/epic/drone/cinematic movement" | léxico específico: "locked-off", "slow handheld", "dolly-in at walking pace" |
| Escena = soundstage | sin Block 4 NI audio bed | añadir Block 4 y Block 6 completos |
| Continuity drift | sin anchors repetidos | copiar los 5 anchors verbatim en cada prompt |
| Driving = music video | cámara se mueve demasiado | lockear frame; solo handheld breathing suave |

## Output discipline
Devolver solo: descripción plain-language de lo hecho ("Here's the held close-up at the kitchen window"). NUNCA pegar: el prompt de 6 bloques completo (salvo que lo pidan), internals/media IDs/element IDs, ni el framework ("I applied the five pillars…"). El usuario quiere el shot, no el método.

## Pitfalls
No apilar adjetivos en Block 1 · no escribir la emoción del actor como verbo (emerge de la contención) · no saltar Block 4 · no dar a la cámara libertad ilimitada (locked-off > drone el 90%) · no generar un shot por beat sin anchors · no usar esta skill para animación/UGC.
