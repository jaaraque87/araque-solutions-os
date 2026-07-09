# Video Builder UI (vrgdg) — Guía operativa ARAQUE (mapeada de 19 capturas + video, 2026-07-08)

El Builder corre DENTRO de la sesión ComfyDeploy (no requirió update de pack). Proyectos en `/comfyui/output/<nombre>/` (⚠ verificar persistencia entre sesiones — respaldar la carpeta del proyecto al cerrar).

## Mapa de la UI

**Top bar:** Video Type (**Singing / Speaking (short film) / No lip sync**) · Quick Save · Wizard · Storyboard Builder · Reference Builder · Line Mapping · LLM Runner · Prompt Options · Stop · Download Models · Clear Memory.

**Menu (pipeline batch):** New/Load/Save Project · Settings · **Gemma T2I All → Gemma Video All → Image All → Render All → Stitch Preview → Build Full Video** · **Remake Mode** (rehacer escenas sueltas) · Auto save.

**Panel izquierdo:** Scenes (cards con estado T2I/I2V/VID) · Tools (**puente con Prompt Creator**: Open/Send To/Import Data From + Agent) · Post Process (**LUTs .cube con preview / Film Grain / FX Overlays** — light leaks por escena).

**Panel derecho por escena:** Scene (label, Freeze SRT timing, start/end, Import Prompt JSON / I2V Motion Notes, Use VRGDG text context files) · **Image** (motores: ZImage / Ernie / Krea 2 / **Flow/GPT** / Enhance / +Custom; Models = z_image_turbo_bf16 + qwen_3_4b + ae; LLM supergemma4-26b + Vision Gemma; subtabs Image Settings / LLM Prompting) · **Video** (modos por escena: **I2V / T2V / Reference to Video / Ingredients to Video**; "Use custom video models/settings/LoRAs for this scene" = overrides POR ESCENA de LoRAs/FPS/size/seed/trigger; GGUF Q6_K + VAE bf16 + gemma-3-12b sikaworld + text_projection) · **Audio** (Scene Audio: drag mp3 POR ESCENA → va a LTX para lipsync y al stitching final; o silencio de N seg; aparte Timeline Audio global).

**Timeline:** pista BASE + pista INSERTS (b-roll superpuesto) · Set In/Out · Snap beats · waveform · notas por escena/línea/timeline · Bulk · +Segment/+Insert.

**Diálogos clave:**
- **Reference Builder Target** (4 modos): I2V/T2V Text Mapping (solo texto) · Flux/Nano Image References (imágenes de referencia para esos motores) · **LTX Reference to Video (workflow MSR LoRA — referencia visual directa al render)** · Ingredients to Video.
- **Line Mapping** (⚠ configurar Reference Builder ANTES): Step 1 Transcribe (Transcribe Existing / **Create Scenes From Lines** con stable-ts / Import SRT) → Step 2 Review + Map Performers (por línea: performer / no-lip-sync / no-character) → Manual Timing.
- **Storyboard Builder:** Still shot flow (Intimate character shots = 8 composiciones) · Image aesthetic · **Global consistency phrase** (Gemma la preserva en TODOS los prompts — outfit/joyas van aquí) · Global/facial performance + custom facial text · Story Layer (arco, strength) · por escena: Subjects, Setting, Shot Type, acciones Gemma/GPT · Export Prompt Files.
- **Prompt Options:** editar/recargar los .txt finales (T2I e I2V) + **Find/Replace pensado para triggers de LoRA** ("the woman" → `naiacruz`) con preview.
- **LLM Runner:** Gemma Local (n_gpu_layers 99 en L40S) / Ollama / LM Studio / API; prompts con referencia de imagen requieren LLM con visión.
- **Prompt Creator embebido:** página completa (Whisper/SRT, min/max/bias, User Inputs con botones Gemma4/**Use GPT** por bloque, ConceptPrompts JSON + I2V Motion Notes editables, draft al proyecto).

## SOP ARAQUE — vocero hablado (proyecto naiapresentacion)

1. **Video Type: Speaking (short film)**
2. Abrir proyecto → cargar audio del guion (Timeline Audio o por escena)
3. **Reference Builder PRIMERO** → target "I2V/T2V Text Mapping" → subject `naiacruz` (la identidad la pone el LoRA Z-Image; el modo MSR Reference-to-Video queda para v2)
4. **Line Mapping** → Create Scenes From Lines (stable-ts) → Map Performers (naiacruz en todas; b-roll = no-lip-sync)
5. **Storyboard Builder** → consistency phrase: `fitted plain white ribbed t-shirt, delicate gold "N" pendant necklace, small gold hoop earrings, natural glowy makeup` → still flow Intimate character shots → facial: natural expressive
6. Menu → **Gemma T2I All** → Prompt Options → **Find/Replace "the woman" → naiacruz** (T2I + I2V ✓)
7. Image tab → verificar dónde se activa el **Z-Image LoRA `naiacruz_zimage_v1` (Image Settings)** · Video tab → custom LoRAs: **talkvid @ 0.8** · 1080×1920 · FPS 24
8. **Image All** → QA de frames (identidad) → re-tirar sueltos si hace falta
9. **Render All** → **Stitch Preview** → **Build Full Video** (en re-builds: Keep current video seeds)

## Changelog del creador (Discord, commit `4cfc788` — POSTERIOR al pack de la máquina)

**🔑 MÉTODO MSR — cita textual: "But now you don't need a ltx lora! Just use this method!"** — Reference-to-Video con start frame (= I2V) + **character ref sheet** que mantiene al personaje consistente en toda escena: si el start frame es un close-up y la cámara abre, LTX inventa el cuerpo/outfit — el ref sheet se lo dicta. Sustituye el LoRA de personaje para video. El Reference Builder ahora genera sheets de 3 paneles estrictos (cara close-up / cintura / cuerpo completo).

Otras mejoras relevantes (requieren actualizar pack a ≥4cfc788):
- **Instrucciones Gemma editables** por escena/globales/presets reusables para T2I, I2V, T2V, RTV, Ingredients
- **Advanced Node Settings por modo de video** (samplers, manual sigmas, I2V inplace strength/bypass) — cada modo guarda lo suyo
- **No-lip-sync mejorado**: los prompts ya no fuerzan canto/lipsync en escenas visuales
- **Fix scene-video recovery**: renders completados que quedaban en carpeta temporal sin cargar al proyecto (≈ nuestro síntoma "run 100% sin video final")
- **Fix doble post-procesado** en stitching (LUT/grain aplicados dos veces = escenas desaturadas)
- **Fix Ernie** usando imágenes de proyectos viejos
- Beat mode en transcripción · previews grandes en Reference Builder · link a guía de soporte

## RECETA MSR (Reference-to-Video sin LoRA de personaje) — del video del creador 07-07

1. Reference Builder → subject → **Reference Type: "MSR LoRA Reference"** → cargar/generar **character sheet de 3 paneles** (cara close-up / torso / cuerpo completo — "imperativo" según el creador)
2. Pestaña Video → modo **Reference to Video** → Video Settings → ✅ **"Use scene image as 2nd ref image"** (la imagen de la escena entra como segunda referencia = actúa de start frame)
3. **Warm up Frames = 0** (evita distorsión inicial y sincroniza el primer frame con la imagen)
4. Create Video. Resultado: identidad y outfit estables aunque la cámara abra el plano (el defecto del I2V puro: LTX pierde identidad en paneos verticales sin referencia global del cuerpo)
⚠ Requiere el archivo del MSR LoRA en el volumen — el botón HF de la UI está DESACTUALIZADO; el link correcto está en el Discord (o usar "Download Models" del Builder).

## Otras perlas de los 5 demos (docs local-*.md de esta carpeta)
- **ID-LoRA pipeline** (id lora.mp4): cortos con diálogo multi-personaje + **clonación de voz por muestra de audio** por personaje; Scene Casting con auto-duración desde los diálogos. Orden obligatorio: Story Layer/diálogos ANTES de Scene Casting. Usar el ID-LoRA principal (caldescenes), NO el de celebridades. Botones superiores del Storyboard = obsoletos, ignorar.
- **Beat Mode** (Line Mapping → Create Scenes From Lines): segment mode Beat, resolution 0.7, include instrumental gaps — "no perfecto pero suficiente para LTX".
- **Generación de referencias in-UI**: usar motor **Z-Image para fotorrealismo** — el creador advierte que Flow/GPT y Nano Banana tienden a caricaturizar los sheets.
- **Instrucciones LLM editables** (T2I/I2V/T2V/RTV/Ingredients + presets): "Gemma isn't the smartest model" — instrucciones CORTAS y simples.
- **FlowGPT manual mode**: botón **"Import Latest Download"** asigna la última descarga del navegador a la escena activa y avanza — puente semi-manual para meter imágenes de ChatGPT escena por escena (verificar si funciona con sesión cloud).

## Verificar en vivo (huecos que las capturas no muestran)
- Dónde exactamente se selecciona el LoRA Z-Image en Image Settings del Builder (¿mismo panel que I2V V5.2?)
- Si Flow/GPT (motores browser) aparece deshabilitado en cloud (esperado: sí)
- Persistencia del proyecto al cerrar la sesión (¿/comfyui/output está en volumen o es efímero?) → respaldar carpeta al terminar SIEMPRE
- Costo/tiempo real de Image All + Render All para ~4 escenas
