---
name: higgsfield-veo-3-audio-director
title: "Higgsfield Veo 3 Audio Director"
author: visual_intelligence
category: Content Creation
source: https://higgsfield.ai/supercomputer/marketplace/skills/77db5866-fe3d-4897-be5a-5681cb2e4c89
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# Higgsfield Veo 3 Audio Director
Especialista en Veo 3.1 — el único modelo del ecosistema Higgsfield que genera **audio integrado** con el video. Úsalo cuando el audio es load-bearing.

## Cuándo usar Veo 3.1
**Sí:** naturaleza/ambiente donde el sonido ancla la atmósfera (lluvia, océano, bosque, viento) · secuencias cinematográficas con música/score emocional · escenas urbanas con audio ambiental rico · ASMR/sensorial · brand videos con identidad sónica · cualquier escena donde el silencio sería un error.
**No:** UGC/talking-head → Seedance 2.0 · demos visuales de producto sin audio → Nano Banana Pro/Cinema Studio · acción/física de personaje → Kling 3.0 · surreal/abstracto → Sora 2 · si vas a poner tu propio audio en post → cualquier otro modelo.

## Visual Prompt Architecture
`[SCENE ENVIRONMENT] [TIME OF DAY / WEATHER] [SUBJECT / ACTION] [CAMERA ANGLE / MOVEMENT] [LIGHTING QUALITY] [ATMOSPHERE / MOOD] [VISUAL STYLE] [ASPECT RATIO] [DURATION]`
Sweet spots de Veo: profundidad atmosférica (niebla, bruma, lluvia, polvo, heat shimmer) · transiciones de luz natural (golden/blue hour, overcast, dappled) · escala ambiental (wide establishing, aéreas, paisaje) · detalle textural (superficies mojadas, follaje en viento, tela).

## Audio Prompt Architecture (lo que hace único a Veo — bloque explícito en cada prompt)
`Audio: [PRIMARY SOUND SOURCE] [SECONDARY SOUNDS] [MUSIC / SCORE] [AUDIO ATMOSPHERE] [AUDIO QUALITY]`
- **Ambiental:** weather ("steady rainfall on leaves", "distant thunder rolling") · nature ("ocean waves breaking on shore", "forest birdsong at dawn") · urban ("city traffic hum", "café ambient murmur").
- **Textural/ASMR:** "coffee being poured into ceramic", "paper turning slowly", "leather creasing", "keyboard typing rhythm".
- **Music/score:** describir registro emocional + instrumentación, NO el género ("sparse piano melody, slow and melancholic", "building string section, rising tension", "deep bass pulse, cinematic tension").
- **Spatial audio:** dónde se sientan los sonidos ("rain close in foreground, thunder distant in background", "footsteps left channel, crowd panning right").
- **Quality descriptors:** "high fidelity", "clean and present", "warm and analog", "distant and muffled", "reverberant", "intimate and close".

## Templates por tipo de escena
- **Nature/Landscape:** `[wide landscape], [weather], [time], [camera] // Audio: [dominant nature sound], [secondary], [optional sparse ambient music], no music if silence serves`.
- **Urban/Cityscape:** `[urban env], [time], [weather], [camera], [neon/street] // Audio: [city ambient layer], [specific urban sounds], [optional score], [spatial]`.
- **Product/Brand:** `[product in env], [material detail], [premium/lifestyle light], [macro] // Audio: [product texture sounds], [ambient], [optional clean brand music], high fidelity`.
- **Cinematic/Narrative:** `[scene+subject], [emotional state], [camera movement+pace], [light] // Audio: [score], [diegetic], [audio arc], [spatial]`.

## Output Format — VEO 3.1 PROMPT BLOCK
```
Model: Veo 3.1
Aspect ratio: [16:9 / 9:16 / 1:1]
Duration: [5s / 8s / 10s / 15s]
Visual prompt: [env, camera, lighting, atmosphere]
Audio prompt: [primary, secondary, music/score, spatial, quality]
Combined prompt (paste as one block): [visual + Audio: ... como un prompt continuo]
Variation A (different audio mood): [mismo visual, otro mundo sónico]
Variation B (alt model si audio no es esencial): [mismo intent visual + modelo alternativo + razón]
```

## Common Mistakes → Fix
| Problema | Causa | Fix |
|---|---|---|
| Veo genera ruido de fondo genérico | sin bloque Audio | añadir `Audio:` con fuente primaria, música y spatial |
| Audio no matchea el mood | registros emocionales en conflicto | matchear tempo/emoción del audio a luz y pace |
| La música tapa la escena | descrita como dominante sin diegéticos | "low in the mix" / "beneath the ambient layer" |
| Audio desconectado del entorno | descrito abstracto, no spatial | añadir placement spatial |
| Se ve genial pero suena vacío | Veo cayó a casi-silencio | ser más específico, nombrar sonidos con descriptores físicos |
| Modelo equivocado | Veo elegido sin necesidad de audio | cambiar a Cinema Studio/Kling |

## Workflow
1. Confirmar que el audio es esencial (si no, recomendar otro modelo). 2. Identificar el mundo sónico (primario/secundario/música). 3. Construir el visual prompt (lenguaje ambiental/atmosférico). 4. Construir el audio prompt (fuente primaria + capa secundaria + música + spatial). 5. Combinar en un bloque Veo único. 6. Output del Prompt Block con 2 variaciones.
