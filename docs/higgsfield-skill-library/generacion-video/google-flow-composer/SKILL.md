---
name: google-flow-composer
title: "Google Flow Composer (Lyria 3 Pro)"
author: cherry_blackcloud
category: Content Creation
source: https://higgsfield.ai/supercomputer/marketplace/skills/26bbdda4-6410-4eec-ac66-35ee4bfd45fd
extracted: modal SKILL.md (via claude-in-chrome)
references: lyria-3-pro-fixes.md (NO extraída)
relevante: música/soundtrack para reels generados
---

# Google Flow Composer (Lyria 3 Pro)
Protocolo para escribir prompts de generación de audio para Google Flow, como soundtrack de video generado. Estructura altamente detallada (matrix + timeline).

## 1. Global Initialization Matrix (precede a toda la timeline; declarar Total Duration explícito)
```
Genre & Style: [género/era, ej. "1980s dark synthwave"]
Mood & Ambiance: [tono emocional, ej. "tense, gritty"]
Instrumentation: [instrumentos core, o "Instrumental" para vetar voces]
Tempo & Rhythm: [velocidad, ej. "Slow 55 BPM"]
Vocal Profile: [género, rango, idioma, o "None"]
Total Duration: [MM:SS]
Parameters: [Beat rate: X BPM | Song key: X | negative_prompt: "..."]
```

## 2. Timeline Chronology
Formato: `[MM:SS - MM:SS] [Structural Tag]: [Production Instructions]`
- Alinear timestamps EXACTO con los cortes y pacing del video.
- **No overlapping markers:** no poner hit markers abstractos justo antes de un bloque; tejer los drop hits al inicio del bloque. Ej: `[0:13 - 0:18] Bridge: Explosive sub-bass impact opens the segment, then glitch pulse...`
- **Hard Stop Syntax:** marker terminal explícito al final. Ej: `[0:34] End: Hard cut all stems to absolute digital silence.`

## 3. Lyrics & Vocals
- Preceder bloques cantados/rapeados con prefijo `Lyrics:`.
- Longitud proporcional (~2-4 líneas por 30s).
- Modificadores en brackets sobre la línea (ej. `[Spoken Intro]`).
- Layering/backing en paréntesis justo después de la línea principal `( )`.

## 4. Sound Design & FX
Frases de textura descriptivas que matchean lo visual ("muffled vinyl crackle", "tape stop", etc.).

## 5. Delivery Workflow
Tras escribir un prompt de audio de Google Flow, SIEMPRE anexar exactamente:
`[Open Google Flow →](https://www.flowmusic.app/session?t=true)`
