---
name: video-editor-commands
title: "Video Editor Commands"
author: cherry_blackcloud
category: Content Creation
users: 22
source: https://higgsfield.ai/supercomputer/marketplace/skills/bdbf86a9-ccc8-4221-a44b-e98f548e580b
extracted: modal SKILL.md (via claude-in-chrome) — single file
relacionado: [[video-stitching]], [[video-advanced-pipelines]] — mismo autor, superconjunto de comandos
---

# Video Editor Commands Protocol (V19)
Parsea y ejecuta bloques de comando estructurados para pipelines de manipulación de video (bridge, loop, extend, split, stitch).

## Critical Rules
- **URL IS THE ONLY SOURCE** — nunca sustituir/adivinar el video.
- **NO GENERATION WITHOUT PERMISSION** — presentar plan y esperar "go"/"yes". Mostrar prompt corregido = solo feedback.
- **Tool failure = HARD STOP** — no narrar éxito ni fabricar URLs/IDs. Chequear artifact store (puede estar de un turno previo); si no, reintentar una vez; si falla, decir exactamente qué step falló.
- **Preview before stitch** — postear preview URL, preguntar "Happy? Shall I stitch?". Nunca auto-stitchear.
- **Audio** — `input_audio` solo dentro de `params` (NO role:audio en medias → HTTP 500). Solo MP3.
- **Aspect ratio / resolution** — auto-detectar de Clip 1 vía ffprobe (aspect_ratio, resolution params; nunca custom width/height). Mín 720p.
- **Seedance 2.0** — duración mín 4s máx 15s.
- **Trim** — `ffmpeg -ss start -to end -i input.mp4 -c copy out.mp4` (antes de extraer frames).
- **Reuse** — chequear /tmp/ antes de re-descargar (archivos persisten en la sesión).
- **Frame extraction** — ffprobe duración → `-ss (dur - frame_dur)`. NUNCA `-sseof` (falla en cortos/VFR).
- **Matchcut model** — kling3_0, duration:3, sin resolution/aspect_ratio params, medias [start_image, end_image].
- **Prompt standards** — empezar con "@Image1 MUST be the first frame.", terminar con "@Image2 MUST be the final frame."
- **Element slot limits** — Seedance 2.0 máx 9 slots (2 frames + audio = 3-4 fijos, máx 5-6 element tokens). NSFW fallback: remover el último element token y reintentar.
- **Asset retrieval** — `higgsfield_attachments_list` solo devuelve subidos por el usuario, no generados.
- **Media type refs en higgsfield_generate** — image job → `type:"image_job"`; video job → `type:"seedance_2_0_job"` etc.; fresh upload → `media_input`.

## Pipelines
- **BRIDGE:** resolver URLs → download → ffprobe Clip1 → extraer Frame A (último de Clip1) + Frame B (primero de Clip2) → si audio: tails MP3 → upload frames → frame preview+enhance → matchcut on (default: SIFT → kling3_0 start+end duration:3) / off (seedance_2_0) → preview → stitch (Clip1→Bridge→Clip2).
- **LOOP:** Frame A (último) + Frame B (primero del mismo clip) → bridge → orden original→bridge (nunca bridge primero).
- **EXTEND:** extraer último frame → seedance_2_0 (sin matchcut) → orden original→extensión.
- **SPLIT:** ClipA (0→split), ClipB (split→end) → Frame A (último de A) + Frame B (primero de B) → audio centrado en split → orden ClipA→bridge→ClipB.
- **AUTODETECT:** PySceneDetect → encontrar el corte de mayor diferencia visual (OpenCV HSV histogram, HISTCMP_CORREL) → bridge.
- **SCENE_INSPECT:** PySceneDetect → primeros max_cuts (hasta 4) → mostrar pares Frame A/B con URLs full-res → preguntar cuáles trabajar.
- **STITCH:** remover frames duplicados en cada join. Kling 3.0 output 30fps → forzar `-r FPS` en re-encode.

## SIFT-Driven Camera Moves (matchcut)
Correr SIFT en Frame A+B, filtrar distance < 0.7*n.distance, promediar keypoints → ancla. Mapear el centro SIFT a trayectoria de cámara: upper→"camera tilts", lower→"camera tilts", left/right→"camera pans", center→"camera pushes".

## Audio Mixing (post-stitch, con ffmpeg — no re-generar)
- `amix` siempre con `normalize=0` (evita auto-ducking agresivo).
- Voiceover ducking: `adelay` (ms) + `volume=enable='lt(t,START)'`.
- Synthesised SFX (si CDN bloqueado): `pip install --break-system-packages pedalboard numpy scipy soundfile`.
- **Crossfade full-track (NumPy, más preciso que amix/afade):** extraer audio_A.wav/audio_B.wav (`-vn -ac 2 -ar 44100`) → soundfile.read → linspace fade_out/fade_in de 1s en los bordes → np.concatenate → sf.write → re-mux `ffmpeg -i concated.mp4 -i mixed_final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k`.

## Audio Scoring Rules
Scene markers (beat dentro de 100ms del corte → skip marker melódico) · percussion uniforme (no acentuar cortes) · dialogue duck a ~15% bajo voz (webrtcvad/silero-vad; VO cuenta como diálogo) · derived rhythm (time_sig:derived → intervalos de PySceneDetect, gap más corto) · execution limit 60s por task de síntesis.

## Google Flow Composer format
GLOBAL INIT (Genre/Mood/Instrumentation/Tempo/Vocal/Total Duration=match exacto video/Parameters) → TIMELINE alineada a cortes → LYRICS (prefijo "Lyrics:", 2-4 líneas/30s) → SOUND DESIGN → append "Open Google Flow →".
