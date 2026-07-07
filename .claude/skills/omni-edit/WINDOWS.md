# Adaptador Windows (este PC) — léeme antes de ejecutar la skill

Esta skill fue escrita en el entorno unix de Paul/Morfeo. En este repo la capa de
ejecución equivalente vive en **`tools/omni-flash/`** (README completo ahí). Mapa:

| La skill dice | En este PC es |
|---|---|
| `generate_video.py --batch jobs.json --concurrency 3` | `py tools\omni-flash\generate_video.py --batch jobs.json --concurrency 3` |
| venv `~/.venvs/omni-flash` + key en env | Python `py` del sistema + `GEMINI_API_KEY` en el `.env` raíz |
| `~/.venvs/fwhisper` (faster-whisper word-level) | skill `hyperframes-media` → `transcribe` (Whisper), o el SRT del MVC de ComfyDeploy |
| skill `/gemini-omni-flash-api` | el bloque CONFIG de `tools/omni-flash/generate_video.py` |
| retime + remux voz (regla fija) | `py tools\omni-flash\remux_voice.py render.mp4 fuente.mp4 final.mp4` |
| `/omni-hook` (QA checklist heredado) | NO instalada — usar el QA propio de cada `style.md` + reglas de SKILL.md §Reglas |
| `docs/formats/oe-sticker-punch.md` | NO incluido en el zip — pedírselo a Paul si se usa "Sticker Punch" literal |

Pendientes conocidos: `GEMINI_API_KEY` vacía en `.env` (llenarla antes del primer run);
falta `oe-sticker-punch.md` y la skill `omni-hook` (pedir a Paul/Morfeo).
Piloto sugerido: escenas del render Naia 2026-07-05 + estilo `patterned` (único validado).
