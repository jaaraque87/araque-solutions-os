---
name: video-advanced-pipelines
title: "Video Advanced Pipelines"
author: cherry_blackcloud
category: Content Creation
users: 39
source: https://higgsfield.ai/supercomputer/marketplace/skills/dac9385d-9396-4897-82fb-8049ba76cbb2
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): audio-mixing.md, google-flow-composer.md, matchcut-sift.md, prompting-and-limits.md, seedance-2-quirks.md
---

# Video Advanced Pipelines (Bridge, Loop, Extend, Stitch, Matchcut, Scene Inspect)
Pipelines de ejecución para manipulaciones avanzadas de video con Seedance 2.0 + FFmpeg + Librosa (análisis de audio).

## Reference Docs
- `references/prompting-and-limits.md`: estándares de prompt (lenguaje positivo, flujo cronológico), límites de slots de referencia por modelo (Seedance...).
- (+ audio-mixing.md, google-flow-composer.md, matchcut-sift.md, seedance-2-quirks.md)

## Audio Scoring Rules (Cherry Blackcloud)
- **Scene change markers:** en cada corte de PySceneDetect, chequear si un beat cae dentro de 100ms; alinear.
- **Percussion consistente:** patrones de kick/taiko/snare uniformes en todo el clip.
- **VAD awareness (dialogue is king):** la música debe duckear a ~15% bajo cualquier voz (webrtcvad o silero-vad).
- **Derived rhythm:** con `time_sig:derived`, calcular intervalos inter-corte desde timestamps de PySceneDetect; usar el gap más corto.
- **Audio pacing extremes:** los steps de `ffmpeg-audio-synthesis` nunca deben pasar 60s por task individual.
- **Post-score offer:** tras cada mix completado, preguntar "¿Querés agregar más capas o...?".

## Critical Operating Rules
**Integridad & context recovery:**
- NUNCA fabricar resultados de tool. Si un tool call devuelve "Result unavailable"/vacío/error → STOP, chequear el artifact store.
- **Artifact store = estado canónico.** En sesiones largas los resultados de turnos previos se pierden del contexto; las entradas de artifact son la verdad.
- **Una respuesta por mensaje.** Nunca postear conclusiones contradictorias; si detectás un error a mitad de draft, descartarlo.

**Pitfalls de entorno/ejecución:**
- `bc` no está disponible. Para trims de frame precisos en FFmpeg (`duration - frame_dur`) usar `python3 -c "print(A - B)"`.
- **Kling 3.0 matchcut (con end_image) NO soporta persistent elements (`<<<id>>>`).** Si el usuario incluye elementos → rechazar/omitir.

**API quirks (Seedance 2.0 & pipeline fixes):**
- **Google Flow Composer support:** tras un stitch finalizado (video + SFX + VO), ofrecer crear música con Google Flow Composer (ver reference).
- **Preview before stitch:** tras generar el clip AI, SIEMPRE postear la preview URL y preguntar "Happy with this? Shall I stitch?" — nunca auto-stitchear.
- **Stitch pipeline (remover frames duplicados y re-encode):** el bridge AI empieza en el último frame del start clip y termina en el primero del end clip → hay duplicados. `fps = ffprobe r_frame_rate`; trim start `-ss 0 -to (duration - frametime)`; trim bridge/end `-ss frametime`; audio `-ar 44100 -af aresample=async=1 -c:a aac`; luego `concat`.
- **Stitch order para loops:** `original_trim.mp4` → `bridge_trim.mp4`.
- **Aspect ratio:** auto-detectar de Clip 1 vía `ffprobe`.
