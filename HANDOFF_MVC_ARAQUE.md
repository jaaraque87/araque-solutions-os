# HANDOFF — Music Video Creator / UGC Pipeline ARAQUE SOLUTIONS
_Actualizado: 5 julio 2026. Pégale este archivo a Claude en cualquier PC para continuar._

## ESTADO ACTUAL (todo funcionando)
- **ComfyDeploy org `araquesolutions`** (login Google jaaraque87). Todo vive en la nube — no hay nada instalado localmente.
- **Máquina "LTX TODO EN UNO's Machine"** (`385499ef-14be-4a75-9ab5-4617913e9e4d`), **versión 26 activa** con:
  - Pack `comfyui-vrgamedevgirl` rama `dev/music-video-builder-ui-test-v9` commit `d6dde1fd` (4 jul, incluye fix GGUF del creador)
  - `llama-cpp-python 0.3.40+cu131` (rueda del fork **JamePeng**, release `v0.3.40-cu131-linux-20260607`) — NO usar abetlen (máx 0.3.19, no soporta Gemma 4)
  - Librerías CUDA 12+13 registradas vía `/etc/ld.so.conf.d/` + ldconfig (fix del error `libcudart.so.12 not found`)
  - `audio-separator`, FFmpeg, todos los modelos en el volumen
- **Workflows importados en ComfyDeploy**: "LTX2.3 MVC Prompt Creator V5.1", "LTX2.3 MVC I2V V5.2", "LTX2.3 MVC T2V V5.2" (de la rama v9 del repo vrgamegirl19/comfyui-vrgamedevgirl)
- **Parte 1 PROBADA Y FUNCIONANDO**: prompts de Naia generados. Parte 2 (I2V) configurada y lanzada el 5 jul (~2 p.m.).

## SOP POR VIDEO (~15 min manuales, desde cualquier navegador)
1. ElevenLabs: voz con guion (voz KENZA VOZ, modelo v3, speed 0.90, stability 50, similarity 100). Etiquetas [excited] SOLO en ElevenLabs; en el workflow va el texto limpio.
2. Workflow **Prompt Creator V5.1** → Start ComfyUI (L40S) → UI: subir audio, FPS 24, Min 3, Max 6, Bias 0.3, spanish, SRT ON, pegar guion limpio en Full Lyrics + bloques Style/Story/Subject → Apply Settings → Save Text Files → cerrar → Run (~2 min).
   - Si da "prompt count does not match SRT scene count": re-Run (semilla nueva) o recortar el silencio final del MP3.
3. Workflow **I2V V5.2** → Start ComfyUI (60 min) → Open UI → verificar modelos (ya commiteados), botón **Paste From Step 1** → Apply Part 2 Settings → Run. Render 30-60 min. Resultado en `output/`.

## CONFIG I2V V5.2 (ya aplicada; por si hay que rehacerla)
- Modelos: LTX `LTX-2.3-22B-distilled-1.1-Q6_K.gguf` · VAEs `LTX23_video/audio_vae_bf16` · Gemma clip `sikaworld` · text projection bf16 · upscaler `x2-1.1` · Z-Image `z_image_turbo_bf16` + `qwen_3_4b` + `ae.safetensors` · LLM `supergemma4-26b-...-Q4_K_M.gguf`
- LTX LoRA: ON, count 1, `ltx-2.3-id-lora-talkvid-3k.safetensors` @ 0.8, Two-Pass ON, sin trigger
- Main: SRT ON · FPS 24 · **1080×1920 vertical** · Z-Image LoRA OFF (hasta tener el de Naia)
- OJO: usar el JSON `I2V_V5.2.json`, NO el `_remake_mode` (ese trae los modelos personales del creador y es solo para rehacer clips sueltos).

## BLOQUES DE TEXTO (Parte 1, campaña Araque Solutions con Naia)
- Guion limpio: "¿Sabes cuánto le cuesta a una marca producir un solo video con actores? Casting, rodaje, estudio... semanas de espera. ¡Con Araque Solutions eso se acabó! Somos una agencia de contenido con inteligencia artificial: creamos videos UGC con influencers virtuales, listos para tus redes en días... no en meses. Sin casting, sin rodajes, sin complicaciones. Contenido ilimitado, tu marca siempre activa, por una fracción del costo. Araque Solutions: el futuro del contenido ya está aquí. Escríbenos... y pruébalo hoy."
- Subject (Naia): "Naia Cruz, a stunning woman aged 25-29, short sleek black bob haircut with straight ends at jaw length, olive green hazel eyes, pale olive skin with warm undertone and realistic skin texture with visible pores, oval face with natural full lips and soft cheekbones, curvy hourglass figure with defined waist, wearing an elegant black fitted top, small gold hoop earrings and a delicate gold 'N' pendant necklace, natural glowy makeup. She is always speaking directly to the camera, lips clearly moving, warm confident expression." + Locations: luxury Miami apartment / rooftop golden hour / hotel suite.
- Style: UGC iPhone selfie testimonial, vertical, handheld, cara siempre visible hablando a cámara (bloques completos en el chat del 5 jul).

## PENDIENTES (siguiente sesión)
1. **LoRA Z-Image de NAIA**: hay dataset de 40+ fotos (generadas con GPT Images 2 desde el character sheet) EN EL PC PRINCIPAL — preguntar carpeta. Receta del Discord: imágenes en 9:16 (aspect ratio del video final), ~6000 steps (3000 no basta, dato de Jazmaan). Entrenadores en el repo v9: `zimage_dataset_creator` + `Z-ImageTurbo_SpeedLoraTrainer_V1`. Ejemplo del creador: HF `vrgamedevgirl84/BlondeFemaleZimageLora`.
2. **Video Builder UI** (app `flow_automation` de la rama v9): referencias con fotos reales, storyboard, B-roll, no-lipsync scenes. El creador publicó update del Builder el 5 jul (instrucciones LLM editables) — actualizar el pack al instalar.
3. Importar `I2V_V5.2_remake_mode` como workflow aparte (rehacer escenas sueltas).
4. Naia como marca aparte: influencer de viajes/hoteles con TT/IG propios — este pipeline es la base (cambiar guion+locations por campaña).

## TRUCOS TÉCNICOS (para Claude en el otro PC)
- Dashboard ComfyDeploy: la página de detalle de máquina CONGELA Chrome. Usar API same-origin: `GET /api/machine/{id}`, `PATCH /api/machine/serverless/{id}` (parcial, dispara rebuild), `GET /api/machine/serverless/{id}/versions?limit=N`, `GET /api/volume/private-models`. Vía javascript_tool con fetch desde cualquier página de la app.
- Import de workflows sin file picker: en `workflows?view=import`, inyectar JSON con DataTransfer + input.files + evento change (fetch desde raw.githubusercontent, tiene CORS abierto).
- Builds de la máquina: 15 min (con caché) a 3 h (sin caché). `build_log`/`updated_at` NO se actualizan durante el build — no asumir colgado.
- Nodo `VRGDG_LlamaCppDoctor` = diagnóstico exacto de llama-cpp en sesión.
- Sesiones: el usuario usa GPU L40S. El render sigue corriendo aunque se cierre el navegador; solo manda el reloj de la sesión.
