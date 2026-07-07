---
name: cinematic-flow-project-rules
title: "Cinematic Flow Project Rules"
author: cherry_blackcloud
category: Personal And Specialized
version: 1.1.0
source: https://higgsfield.ai/supercomputer/marketplace/skills/86227aba-956f-4c7d-8380-2e79d6a658e7
extracted: modal SKILL.md (via claude-in-chrome) — single file
nota: overrides project-specific de cinematic-flow para el proyecto personal "Cyber-noir Elbaph Siege" del autor. Los Roster UUIDs son personajes privados (no reusables). Los learnings generales SÍ sirven.
---

# Cinematic Flow Project Rules
Learnings específicos de proyecto que modifican/extienden la skill base `cinematic-flow`.

## Video Continuation Workaround (GENERAL — muy útil)
Seedance 2.0 NO soporta continuación video-a-video nativa (rechaza `role:"start_video"`). Workflow:
1. Extraer el ÚLTIMO FRAME del video más reciente con ffmpeg: `ffmpeg -sseof -0.1 -i '<url>' -vframes 1 -update 1 /tmp/clipN_last_frame.jpg -y`
2. Subir el frame vía `higgsfield_upload`.
3. Pasarlo como `@Image1` en Seedance 2.0 con `role:"image"`.
4. Inyección de prompt obligatoria: `@Image1 is the EXACT opening frame. Reproduce this frame pixel-perfect as frame 0. Do NOT alter, recolor...`
5. Mantener el prompt de continuación simple, enfocado en la acción que sigue.
6. Añadir el video resultante a la lista de artifacts apenas completa.

## Combat Action Constraints (GENERAL)
- **Limb Specificity:** Action = intent + named technique + explicit limb + contact point. Nunca moves vagos ("attacks", "fights").
- **Target Reaction:** los personajes a punto de recibir un ataque deben estar reaccionando activamente (bracing, dodging, counter-moving).

## Format Defaults (de este proyecto)
1:1 aspect · 1080p · 4s por clip (salvo que el diálogo pida más).

## Audio Stitching Continuity (GENERAL)
Para secuencias stitcheadas con música continua (ej. dark techno rave), especificar el mismo bloque Audio en cada clip. Ej: `Audio: Dark techno, 140 BPM, F minor, heavy kick drum every beat.` Terminar SIEMPRE el bloque Audio con: `Clip ends clean on the downbeat, ready to continue seamlessly into the next clip.`

## Roster UUIDs (privados del autor — NO reusables)
@cher, @ka, @Shinigami, @hatlessshinigami, @queenofspades, @MsYurei, @Tengusd2, @nop, @kap, @On — personajes/elementos del proyecto Elbaph Siege.
