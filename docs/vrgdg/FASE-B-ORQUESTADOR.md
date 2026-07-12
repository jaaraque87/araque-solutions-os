# FASE B — Orquestador headless del V9 Video Builder (GO del dueño 2026-07-12)

## Descubrimiento clave (commit pack c26550f, verificado en código)
El Builder expone su API completa como rutas HTTP del servidor ComfyUI → **llamables por el túnel de sesión con curl/python, sin UI**. Rutas críticas (POST /vrgdg/music_builder/*):
- `new_project`, `save_project_as`, `save_session`, `load_session` — proyecto/estado completo
- `save_scene_image`, `save_scene_audio`, `save_project_audio`, `trim_scene_audio` — assets POR ESCENA (pairing garantizado por código; mata el error humano de la Producción 001)
- `generate_i2v`, `generate_chained_i2v`, `generate_t2i`, `generate_t2v` — RENDER headless
- `scan_scene_videos`, `restore_scene_video`, `extract_video_final_frame` — estado/resume
- post_process/* (film_grain, adjust, LUTs) — post por API
- `_save_builder_session(payload)` (VRGDG_MusicVideoBuilderNodes.py ~7268) crea la estructura: project_folder + images/ + prompts/ + context/; payload con audio_path, project_name/project_folder, escenas.
- GET `list_projects`, `model_defaults`, `workflow_runner/lora_list`, etc.

## Diseño del orquestador `tools/builder-orchestrator/montar_y_render.py`
Entrada: carpeta KIT (formato CAMILA-PROD001-KIT: escN_*.png + audio-por-escena/escN_*.mp3 + i2v_prompts.txt) + tunnel_url.
1. POST new_project → carpeta proyecto
2. Por escena N: save_scene_image + save_scene_audio (pares 1:1 por nombre de archivo)
3. save_session con timeline (duraciones = duración real de cada audio) + prompts I2V + settings (Speaking/I2V, 1080×1920 altura>ancho, talkvid 0.8, fit/contain, FPS 24)
4. generate_i2v por escena (o chained) → poll /prompt hasta cola 0 → scan_scene_videos
5. Paso final de stitch (localizar ruta "build full video" — pendiente identificar; fallback: descargar escenas + concat ffmpeg local con el audio maestro)
6. QA automático: orientación, duración, volumen por escena, frames de identidad
Payloads exactos: leer los fetch() en web/VRGDG_MusicVideoBuilderUI.js (buscar cada ruta) — la UI documenta el contrato.

## Contexto de la Producción 001 (por qué esto es prioridad)
Render manual falló 4/5 escenas por pairing humano cruzado (audio 4.00s en escena equivocada, segmento suelto 1.60s, escena 5 sin render, sin Build Full Video). Escena 1 (par correcto) salió PERFECTA → el motor funciona; la carga manual es el punto único de fallo que este orquestador elimina.

## Siguiente sesión de trabajo (cualquier PC/agente)
1. Extraer payloads de los fetch en el JS (gratis, local)
2. Escribir montar_y_render.py (stdlib, patrón tools/omni-flash)
3. Prueba húmeda con CAMILA-PROD001-KIT: sesión L40S (GO de gasto del dueño) → montar → render → QA → FINAL
4. Este script ES el motor de la Fase C (la app): la UI web solo llenará el KIT.
