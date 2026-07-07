# tools/omni-flash — capa de ejecución Windows para la skill `omni-edit`

Réplica local del tooling que la skill espera (`generate_video.py --batch jobs.json`),
construida para este PC (Windows, Python 3.13 vía `py`, sin venvs). 2026-07-05.

## Requisitos
- `py` (Python 3.13 ✓ instalado), `ffmpeg`/`ffprobe` (✓ instalados, winget Gyan build)
- **GEMINI_API_KEY** en el `.env` raíz del repo (misma key que usa tts-ugc). → PENDIENTE: está vacía.
  Se obtiene en Google AI Studio. Nunca se commitea.

## Comandos

```bat
:: single
py tools\omni-flash\generate_video.py --video in.mp4 --prompt "..." --output out.mp4 --aspect-ratio 9:16

:: batch (el modo que usa la skill)
py tools\omni-flash\generate_video.py --batch jobs.json --concurrency 3

:: turn-by-turn sobre una generación aprobada (leer interaction_id del .meta.json del PARENT
:: y VERIFICAR su contenido antes — regla de la skill: nunca mapear por posición del log)
py tools\omni-flash\generate_video.py --video in.mp4 --prompt "..." --output out_v2.mp4 --previous-interaction-id <id>

:: retime + remux de voz original (OBLIGATORIO tras conversión de aspecto / mundo total)
py tools\omni-flash\remux_voice.py render_omni.mp4 fuente_con_voz.mp4 final.mp4
```

Cada render guarda `<output>.meta.json` con `interaction_id` (siempre).

## Notas de adaptación (vs. el entorno original de la skill)
- La skill referencia venvs unix (`~/.venvs/omni-flash`, `~/.venvs/fwhisper`). Aquí no hay venvs:
  `generate_video.py` es stdlib puro. Para **beats word-level** usar la transcripción de
  HyperFrames (skill `hyperframes-media`, comando `transcribe` con Whisper) o el SRT que ya
  genera el MVC de ComfyDeploy; si algún día se quiere faster-whisper: `py -m pip install faster-whisper`.
- El modelo/endpoint viven en el bloque CONFIG de `generate_video.py` (`OMNI_MODEL`,
  `OMNI_API_BASE` como env vars opcionales). Si Google renombra campos, se toca solo ahí.
- Errores de filtro se reportan como `[FILTRO/BLOQUEO]` → aplicar el protocolo de diagnóstico
  de la skill (retry → sonda otro video → sonda de control → bisect).

## Integración en el pipeline ARAQUE
```
ElevenLabs (voz) → LTX/MVC ComfyDeploy (clips por escena) → omni-edit (restyle batch, 1 estilo/serie)
    → remux_voice.py (voz original) → HyperFrames (ensamble + captions + mix)
```
Primer piloto sugerido: 2-3 escenas del render de Naia (2026-07-05) + estilo `patterned`
(el único validado). QA: identidad primero, lipsync 6 puntos, texto letra por letra.
