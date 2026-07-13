# HANDOFF EJECUTIVO → CODEX · 2026-07-13
_Pipeline UGC talking-head (vocera IA) sobre ComfyDeploy + V9 Video Builder. Objetivo: automatizar producción de reels UGC que convierten, con research-first y voceras consistentes. Este doc = estado real, fallas con solución, y tareas de automatización concretas._

---

## 1. RESUMEN EJECUTIVO (léelo primero)

**Lo que FUNCIONA hoy, de punta a punta:** research de nicho → hooks puntuados → guion Kallaway → imágenes GPT Images 2 (still por escena) → audio Gemini TTS (voz anclada por vocera) → **orquestador headless** que monta el proyecto en el Builder por API (pairing por código) → render por escena en L40S → clips 1080×1920 con audio y lipsync → stitching. **La identidad consistente y el lipsync YA se logran** cuando se respetan 3 reglas de oro (abajo). El Video Builder NO era el problema; los fallos eran parámetros mal puestos, ya diagnosticados.

**Estado de la Producción 001 (clínica dental, Dra. Camila Rey):** 4/5 escenas correctas (identidad fiel + lipsync + movimiento vivo). **Falla puntual: esc5 (CTA) sin lipsync** por sonrisa fija en el still (solución concreta en §4). Falta: regenerar/ajustar esc5, render de las 5 con seed fijo, Build Full Video, post (HyperFrames).

**La gran oportunidad de automatización:** el render (Render All / Build Full Video) sigue siendo un clic humano en la UI. Todo lo demás ya es headless. Cerrar ese último tramo = producción 100% automática (§5, tarea A1).

---

## 2. LO QUE HEMOS LOGRADO

### Infra (estable)
- Máquina **"LTX TODO EN UNO"** (id `385499ef-14be-4a75-9ab5-4617913e9e4d`, org `araquesolutions`), versión **v34** (`vrgdg-prompt-metadata-fix`). Builder V9 100% funcional tras la saga de fixes (755 null-workflow + prompt-metadata; ver `docs/vrgdg/HANDOFF-BUILDER-DEBUG.md`).
- GPU de trabajo: **L40S** (la A10G de 24GB NO alcanza para el LTX 22B — usar siempre L40S).
- API interna ComfyDeploy (cookies same-origin): `GET /api/sessions` → campo `.url` = túnel de la sesión. La página de detalle de máquina CONGELA Chrome → operar por API.

### Orquestador headless (Fase B) — LO MÁS VALIOSO
`tools/builder-orchestrator/montar_proyecto.py`. Monta un proyecto completo del Builder por API desde un "kit" local:
```
py tools\builder-orchestrator\montar_proyecto.py --tunnel <URL> --kit "<carpeta_kit>" --name <PROYECTO>
```
- Lee `escN_*.png` + `audio-por-escena/escN_*.mp3` + `i2v_prompts.txt` (formato `I2VN=...`).
- **Pairing garantizado por código** (assert esc_img == esc_aud == N).
- Sube imágenes vía `save_scene_image` **y** `archive_scene_image` (fix SameFileError), audios vía `save_scene_audio`, arma segmentos sobre el esquema real (`load_session`) y guarda con `save_session`.
- Rutas API descubiertas: `/vrgdg/music_builder/{new_project,load_session,save_scene_image,archive_scene_image,save_scene_audio,save_session,list_projects,generate_i2v}` (doc completa en `docs/vrgdg/FASE-B-ORQUESTADOR.md`).

### Producción validada end-to-end
Research (niche-radar) → 10 hooks puntuados → h03 "¿Te truena la mandíbula?" (score 9, respaldo 26K) → guion Kallaway → 5 stills Camila (GPT Images 2) → VO Gemini TTS "Leda" 28.52s en 5 cortes por palabra → kit → montaje headless → render.

---

## 3. WORKFLOWS / COMPONENTES QUE SÍ DAN BUENOS RESULTADOS

| Componente | Estado | Nota |
|---|---|---|
| **V9 Video Builder** (workflow "LTX2.3 MVC I2V", nodo Video Builder) | ✅ El motor de talking-head. Render por escena con audio conditioning = lipsync real | Modo `Speaking (short film)` |
| Workflow de escena **`LTX2.3_ID_lora_API.json`** (pack, UsedForUIDoNotTouch) | ✅ es el que ejecuta el I2V; modelos LTX 2.3 22B Q8/Q6 GGUF + audio VAE | 2 pass, sampler euler_ancestral |
| **MVC Prompt Creator V5.1 / I2V V5.2** | ✅ probados 5-jul (lipsync nativo audio-condicionado) | vía workspace |
| **Gemini TTS** (`gemini-3.1-flash-tts-preview`, voces prebuilt p.ej. "Leda") | ✅ voz anclada por vocera, por-segmento, loudnorm -16 | skill `tts-ugc` |
| **GPT Images 2** para stills por escena | ✅ identidad consistente entre stills (misma persona) | skill `hf-gpt-image-2-director` |
| **niche-radar + hook-lab/hook-machine** | ✅ research con datos reales, hooks puntuados | research-first obligatorio |
| **Orquestador montar_proyecto.py** | ✅ montaje headless perfecto | Fase B |

---

## 4. FALLAS ACTUALES (con causa raíz y SOLUCIÓN concreta)

### FALLA #1 — esc5 (CTA) sin lipsync ← ACTIVA, bloquea entrega Prod001
- **Síntoma:** en esc5 la boca mantiene una sonrisa con dientes fija los 4.6s; no articula el habla (verificado con dense mouth strip: esc4 articula, esc5 no).
- **Causa raíz:** el still fuente `esc5_cta` es una **sonrisa amplia con dientes** + prompt "big genuine warm smile". LTX I2V, ante un still con expresión fuerte, la conserva y el audio conditioning (más débil) NO logra abrir/articular los labios.
- **SOLUCIÓN (2 opciones, probar B primero = gratis):**
  - **B (rápida):** editar `i2v_prompts.txt` línea `I2V5=` → quitar "big genuine warm smile", poner `speaking warmly to camera, natural mouth movement, lips parted mid-sentence, relaxed friendly expression`. Re-render solo esc5.
  - **A (robusta):** regenerar el still del CTA en GPT Images con **boca de hablar** (labios relajados, apenas separados, cálida pero NO sonrisa congelada). Re-render solo esc5.
- **Regla derivada:** en TODA escena hablada el still debe tener boca neutra/entreabierta "mid-speech"; la sonrisa grande solo en beats SIN audio (freeze/CTA estático).

### FALLA #2 — Render sigue siendo un clic humano (no headless)
- **Síntoma:** montar es automático, pero **Render All** y **Build Full Video** requieren que un humano abra el Builder y haga clic.
- **Causa raíz:** el render se dispara con `queuePrompt` desde el JS del Builder; aún no replicamos esa submission por API.
- **SOLUCIÓN:** ver §5 tarea A1 (replicar el POST `/prompt` con el workflow de escena + `extra_data.extra_pnginfo.workflow` que el fix v34 ya normaliza).

### FALLA #3 — Seed fijo NO está en el orquestador (se inyecta a mano)
- **Síntoma:** `montar_proyecto.py` setea video_type/width/height/fps pero **NO** el seed. El seed fijo (clave para identidad consistente) se inyecta hoy con un script inline aparte.
- **SOLUCIÓN:** ver §5 tarea A2 (mergear inyección de `i2v_video_settings.seed=69, seed_mode=fixed` en el orquestador).

### FALLA #4 — Persistencia de outputs
- `/comfyui/output` NO persiste entre sesiones. Hay que remontar el proyecto (2 min) y **descargar los clips antes de cerrar**. El volumen (private-models) SÍ persiste.

### Fallas resueltas (histórico, no repetir)
- Drift de identidad entre escenas → era **seed en `randomize`**; con `seed 69 fixed` identidad ~85-90% fiel. ✅
- Lipsync desincronizado esc2+ → `custom_audio_timeline_start` mal (ponía posición global; debe ser 0 por escena). ✅ (commit 756c71b)
- Look robótico/estatua → prompts v1 imponían "STATIC/minimal movement"; v2 dirige actuación (micro expressions, blinks). ✅ (commit 1283ee0)
- SameFileError en Render All → subir imagen también como preview (`archive_scene_image`). ✅ (commit 2f70d29)

---

## 5. OPORTUNIDADES DE AUTOMATIZACIÓN → TAREAS PARA CODEX (específicas)

### A1 — Render headless (cerrar el último tramo manual) · ALTO IMPACTO
**Meta:** disparar Render All + Build Full Video por API, sin abrir la UI.
**Cómo:** el Builder somete cada escena con `POST /prompt` (ComfyUI) usando el workflow `LTX2.3_ID_lora_API.json` parametrizado por escena (imagen aprobada, audio, prompt, seed). El fix v34 ya inyecta `extra_data.extra_pnginfo.workflow` para no crashear (nodo 755 / VHS 273).
**Pasos concretos:**
1. Capturar el body real de `queuePrompt` del Builder (DevTools → Network mientras se hace Render de 1 escena) o leerlo del JS `VRGDG_MusicVideoBuilderUI.js` (buscar `queuePrompt`/`/prompt`).
2. Replicar en el orquestador: por cada escena, cargar el template JSON, setear nodos (LoadImage=approved, LoadAudio=custom_audio, CLIPTextEncode=i2v_prompt, RandomNoise=seed 69), `POST /prompt`, poll `/history/{id}`.
3. Descubrir la ruta de "Build Full Video" (concatena `rendered_scene_videos/*` + audio) — buscar en `VRGDG_MusicVideoBuilderNodes.py` la función de stitch final.
**Entregable:** `tools/builder-orchestrator/render_headless.py --tunnel <U> --project <P>` que deja el FINAL en `/comfyui/output/<P>/` y lo descarga.

### A2 — Mergear seed fijo + settings de calidad en el orquestador · RÁPIDO
En `montar_proyecto.py`, tras armar `session`, escribir:
```python
session["i2v_video_settings"] = {**(session.get("i2v_video_settings") or {}),
    "seed": 69, "seed_mode": "fixed", "seedMode": "fixed", "seed_behavior": "fixed",
    "width": 1080, "height": 1920, "fps": 24}
```
(Hoy esto se hace con script inline; debe quedar en el script y commitear.)

### A3 — Validador de kit anti-fallas · PREVIENE #1
Pre-flight que RECHACE el kit si una escena hablada trae still con sonrisa amplia:
- Heurística simple: detección de sonrisa/dientes (área clara en la zona boca) en `escN_*.png`; si es escena hablada y supera umbral → warning "still con sonrisa fija, riesgo de no-lipsync".
- Y validar que cada `I2VN=` NO contenga "big smile/grin" en escenas habladas.
**Entregable:** `--validate` en el orquestador que corre antes de subir.

### A4 — Plantilla de kit + generación asistida · ESCALA A CLIENTES
Formalizar el "kit" como contrato (carpeta con `escN_*.png`, `audio-por-escena/escN_*.mp3` con duración en el nombre, `i2v_prompts.txt`). Script que, dado guion + timestamps (faster-whisper), corte el VO por palabra y arme la carpeta. Base para que la Plataforma (Fase C) lo genere sola.

### A5 — Post automatizado (HyperFrames) · CIERRA EL PRODUCTO
Encadenar tras el FINAL: overlay del hook (0-2.5s), captions por frase (whisper), SFX (skill `sfx-ugc`), música (skill `music-ugc`). Skills ya existen en `.claude/skills/` (hyperframes, sfx-ugc, tts-ugc). Falta el orquestador que las llame en secuencia sobre el mp4 del Builder.

---

## 6. REGLAS DE ORO (no romper — pagadas con errores)
1. **Seed FIJO** por vocera/serie → identidad consistente (independiente de LoRA).
2. **Still de escena hablada = boca neutra/entreabierta**, nunca sonrisa amplia → lipsync articula.
3. **`custom_audio_timeline_start = 0`** por escena (offset dentro del audio, no posición global).
4. Prompts I2V con dirección de actuación (micro expressions, blinks), no "STATIC/minimal movement".
5. Stills pre-recortados 9:16 EXACTO (1080×1920), altura>ancho verificado.
6. Cortes de audio SOLO en límites de palabra (faster-whisper); escenas ≤ ~9-10s.
7. Voz ≠ cara jamás cambia en una misma vocera (regla de marca del dueño).
8. **L40S siempre** (no A10G); descargar outputs antes de cerrar; apagar al terminar; NO gastar APIs sin OK del dueño (presupuesto ~$15).

---

## 7. PENDIENTES / SIGUIENTE
1. **Cerrar Prod001**: fix esc5 (§4 #1, opción B) → render 5 escenas seed fijo → Build Full Video → descargar → post.
2. Ejecutar tareas A1-A2 (headless render + seed en orquestador) = producción sin humano.
3. LoRA de personaje = upgrade premium (misma cara entre VIDEOS distintos / ángulos extremos), NO bloqueante. Dataset Naia curado listo (36 imgs); Camila necesitaría dataset equivalente.
4. Plataforma ARAQUE (Fase C): envolver todo, research-first obligatorio (`docs/PLATAFORMA-ARAQUE-SPEC.md`).

**Docs clave:** `docs/vrgdg/FASE-B-ORQUESTADOR.md`, `docs/vrgdg/HANDOFF-BUILDER-DEBUG.md`, `tools/hook-lab/clients/clinica-dental/produccion-001/PRUEBA-BARATA-IDENTIDAD.md` (diagnósticos seed+lipsync), `memory/comfydeploy-mvc-vrgdg.md` (infra+reglas), `HANDOFF-2026-07-12.md`.
