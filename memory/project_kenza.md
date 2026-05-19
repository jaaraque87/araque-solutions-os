---
name: Proyecto Kenza — UGC Pipeline ARAQUE SOLUTIONS
description: Stack completo del influencer virtual Kenza + pipeline de producción UGC automatizado de 12 pasos + LTX 2.3 RunPod pipeline
type: project
originSessionId: 3e0c87e5-a84e-40d4-94af-35693ec06c7e
---
Kenza es una influencer virtual venezolano-ucraniana "Biker de Miami" con bob negro, ojos verdes, piel blanca/olive.

## Kenza UGC Pipeline v1 (activo desde 2026-05-14)

**Ubicación del proyecto:** `C:\Users\SOPORTE2\Documents\Kenza UGC Pipeline\`

**Archivos clave creados:**
- `.env.example` — template de todas las API keys
- `setup.py` — instalador de dependencias
- `run.py` — orchestrator principal con CLI
- `docs/guia-araque-solutions.html` — guía interactiva completa para operadores

**Stack de producción (pipeline 12 pasos):**
- Guión: Gemini Pro ($0.01)
- Imagen personaje + locación: GPT Image 2 vía fal.ai ($0.82 total)
- Morpheus scene frames: ComfyDeploy deployment `0b82e690-9a08-4d1f-85f8-28849d16caa4` ($0.50)
- TTS: Gemini `gemini-3.1-flash-tts-preview`, voz Leda ($0.02)
- Voice change: ElevenLabs STS `eleven_multilingual_sts_v2` ($0.06)
- Video clips: Kling Pro `fal-ai/kling-video/o3/pro/reference-to-video` ($1.20) ← paso más caro
- Lip-sync (opcional): Sync-3 `fal-ai/sync-lipsync/v3` ($0.60)
- Música: Suno V4.5 Plus vía Kie.ai KEY=`426c134b1ac3697c73851abf114f1878` ($0.06)
- Assembly: FFmpeg local ($0.00)
- Subtítulos (opcional): Submagic ($0.10)
- **Costo total sin opcionales: ~$2.77 | Con todo: ~$3.37**

**Modelo de negocio ARAQUE SOLUTIONS:**
- Precio recomendado lanzamiento: $497/mes por cliente
- Margen neto por cliente (60 videos/mes): ~$350/mes
- Target 5 clientes = $3,335/mes neto

**Scripts pendientes de escribir (12):**
brand_analyzer.py, guion.py, personaje.py, locacion.py, morpheus.py, tts.py, voice_change.py, kling.py, sync.py, music.py, assembly.py, subs.py

---

## LTX 2.3 RunPod Pipeline — Script v2.2 (2026-05-17)

**Script:** `C:\Users\SOPORTE2\Downloads\install_ltx23_runpod.sh` — v2.3 (2026-05-19)
**Workflow principal:** `C:\Users\SOPORTE2\Downloads\LTXREALISM.json` (VideoFlow LTX 2.3 All-in-One v3.0)
**Workflow I2V analizado:** `C:\Users\SOPORTE2\Downloads\LTX2.3_Music_Video_Creator_I2V_V5.1.json`

### Pod recomendado
- Template: **RunPod Pytorch 2.x.x** (NO el de ComfyUI)
- GPU: A6000 48GB mínimo / A100 80GB ideal
- Disco: 200-300 GB
- Acceso: `https://{POD_ID}-8888.proxy.runpod.net/proxy/8188/`

### Fixes aplicados (todos en el script):
- v2.0: Auto-instala ComfyUI, PyTorch cu121, repos HF correctos, Jupyter proxy
- v2.1: Parche model_patcher.py (Linear lazy), Gemma tokenizer, librosa, bypass UNETLoader null
- v2.2: Stack completo Music Video Creator, Z-Image Turbo, LLaMA/SuperGemma, 3 workflows MVC

### Modelos que instala el script automáticamente:
| Modelo | Tamaño | Fuente |
|---|---|---|
| ltx-2.3-22b-dev-fp8.safetensors | 29 GB | Lightricks/LTX-2.3-fp8 |
| LTX-2.3-22B-distilled-1.1-Q6_K.gguf | 21 GB | Abiray/LTX-2.3-22B-DISTILLED-1.1-GGUF |
| gemma_3_12B_it_fp4_mixed.safetensors | 9.45 GB | Comfy-Org/ltx-2 |
| ltx-2.3_text_projection_bf16.safetensors | 2.31 GB | Kijai/LTX2.3_comfy |
| LTX23_audio_vae_bf16.safetensors | 365 MB | Kijai/LTX2.3_comfy |
| LTX23_video_vae_bf16.safetensors | 1.45 GB | Kijai/LTX2.3_comfy |
| taeltx2_3.safetensors | 23.5 MB | Kijai/LTX2.3_comfy |
| ltx-av-step-1751000_vocoder_24K.safetensors | ~500 MB | Kijai/LTX2.3_comfy |
| ltx-2.3-spatial-upscaler-x1.5-1.0.safetensors | 1.09 GB | Lightricks/LTX-2.3 |
| ltx-2.3-spatial-upscaler-x2-1.0.safetensors | 996 MB | Lightricks/LTX-2.3 |
| ltx-2.3-spatial-upscaler-x2-1.1.safetensors | ~1 GB | Lightricks/LTX-2.3 |
| ltx-2.3-22b-distilled-lora-384-1.1.safetensors | 7.61 GB | Lightricks/LTX-2.3 |
| ltx-2.3-id-lora-talkvid-3k.safetensors | 1.13 GB | Comfy-Org/ltx-2.3 |
| LTX23_Enhancers_CrispSoft.safetensors | 672 MB | CivitAI v2849716 |
| LTX2.3_Crisp_Enhance.safetensors | — | vrgamedevgirl84 HF |
| LTX2.3_Soft_Enhance.safetensors | — | vrgamedevgirl84 HF |
| LTX2.3_Luxe_Sensual.safetensors | — | vrgamedevgirl84 HF ⭐ Kenza beauty |
| LTX2.3_Post_Apocalyptic.safetensors | — | vrgamedevgirl84 HF |
| LTX2.3_Wild_West.safetensors | — | vrgamedevgirl84 HF |
| LTX23-GalaxyAce.safetensors | 1.88 GB | CivitAI v2808759 |
| AmateurHour_01_rank16.safetensors | — | CivitAI v2844417 |
| z_image_turbo_bf16.safetensors | ~5 GB | dimitribarbot/Z-Image-Turbo-BF16 |
| qwen_3_4b.safetensors | ~3 GB | Comfy-Org/Qwen3 |
| ae.safetensors (FLUX VAE) | 335 MB | black-forest-labs/FLUX.1-schnell |
| supergemma4-26b-uncensored-fast-v2-Q4_K_M.gguf | 16.8 GB | juan1995-dev HF |
| Llama-3.2-3B-Instruct-Q4_K_M.gguf | ~2 GB | bartowski HF |
| tokenizer.model (Gemma) | — | Comfy-Org/ltx-2 |

### Modelos TODOENUNO — Sources confirmados (v2.3, 2026-05-19):
| Modelo | Fuente confirmada | Destino |
|---|---|---|
| ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors | Kijai/LTX2.3_comfy/diffusion_models/ | diffusion_models/ |
| LTX-2.3-22B-distilled-1.1-Q4_K_M.gguf | Abiray/LTX-2.3-22B-DISTILLED-1.1-GGUF (sustituye Q4_0) | diffusion_models/ |
| gemma_3_12B_it_fp8_scaled.safetensors | Comfy-Org/ltx-2/split_files/text_encoders/ (13.2 GB) | text_encoders/ |
| MelBandRoformer_fp16.safetensors | Kijai/MelBandRoFormer_comfy (456 MB) | audio_separator/ |
| mmproj-BF16.gguf | unsloth/gemma-4-26B-A4B-it-GGUF (1.19 GB) | llm/ |
| ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors | Lightricks/LTX-2.3-22b-IC-LoRA-Union-Control (654 MB) | loras/ |
| ltx-2-19b-ic-lora-detailer.safetensors | Lightricks/LTX-2-19b-IC-LoRA-Detailer | loras/ |
| ltx-2.3-id-lora-celebvhq-3k.safetensors | Comfy-Org/ltx-2.3/split_files/loras/ | loras/ |

### Modelos OPCIONAL (descarga manual):
- **gemma-3-12b-it-abliterated-sikaworld-high-fidelity-edition.safetensors** → `models/text_encoders/`
- **ltx-2.3-22b-distilled-1.1-Q4_0.gguf** → NO EXISTE públicamente; usar Q4_K_M instalado arriba

### Custom nodes instalados (16) — v2.3 corrección crítica:
ComfyUI-Manager, RES4LYF, ComfyUI-KJNodes, ComfyUI-VideoHelperSuite, ComfyUI-Impact-Pack,
rgthree-comfy, ComfyUI-Custom-Scripts, ComfyUI-Easy-Use, ComfyUI_essentials,
was-node-suite-comfyui, ComfyUI-GGUF, ComfyUI-Frame-Interpolation, ComfyUI-Unload-Model,
ComfyUI-MelBandRoFormer, comfyui-vrgamedevgirl,
**ComfyUI-PromptRelay** (kijai) ← CRÍTICO, faltaba — ya agregado al script 02

### Workflows instalados (5):
- `VideoFlow_LTX23_AllInOne_v3.json` — LTXREALISM base
- `LTX2.3_Music_Video_Creator_Prompt_Creator_V5.json` — genera prompts desde audio/letra
- `LTX2.3_Music_Video_Creator_T2V_V5.1.json` — Text→Video por escena
- `LTX2.3_Music_Video_Creator_I2V_V5.1.json` — Image→Video con Z-Image Turbo
- `LTX2.3TODOENUNO.json` — ⭐ ALL-IN-ONE: IC LoRA + voice ID + looping + MelBandRoformer

### Music Video Creator I2V — Nodos VRGDG descubiertos:
VRGDG_AudioCrop, VRGDG_BuildVideoOutputPath_General_SRT, VRGDG_CreateFinalVideo_SRT,
VRGDG_EasyMultiCyclingTextPicker, VRGDG_LatestSRTAutoLoader, VRGDG_LoadAudioFilePath,
VRGDG_LoadAudioSplit_SRTOnly, VRGDG_OptionalMultiLoraModelOnly, VRGDG_Part2WorkflowUI,
VRGDG_PromptSplitter_General, VRGDG_SuperGemmaGGUFChat, VRGDG_TrimImageBatch_SRTOnly

### Stack completo pip (vrgamedevgirl requirements.txt):
kornia, librosa, imageio, torchcodec, google-generativeai, av, stable-ts, demucs,
transformers, accelerate, huggingface_hub, voxcpm, llama-cpp-python

### Scripts modulares v2.3 — carpeta completa (2026-05-19):
**Ubicación:** `C:\Users\SOPORTE2\Downloads\LTX23_Scripts\`
- 00_config.sh — config compartida + helpers (source, no ejecutar)
- 01_sistema_comfyui.sh — apt + ComfyUI + PyTorch + patches (~5 min)
- 02_nodos_custom.sh — 16 nodos + pip stack (~10 min)
- 03_modelos_base.sh — checkpoint fp8 + encoders + VAEs (~55 GB)
- 04_modelos_mvc.sh — Music Video Creator (~70 GB)
- 05_modelos_todoenuno.sh — TODOENUNO exclusive (~58 GB)
- 06_loras.sh — LoRAs estilo + voice ID (~15 GB)
- 07_workflows.sh — instala + parchea JSONs
- 08_arranque.sh — genera start_comfyui.sh
- 09_verificacion.sh — checkea todo
- run_all.sh — orquestador con --base / --skip-tod / --from=N
- LEEME.txt — instrucciones completas
**Total: ~200 GB | Tiempo: ~4-5 horas en pod nuevo**

### TODOENUNO — Análisis completo (2026-05-19):
**Archivo:** `C:\Users\SOPORTE2\Downloads\LTX2.3TODOENUNO.json`
- 410 nodos, 76 tipos únicos
- Tiene instrucciones en ESPAÑOL dentro del workflow (presionar `9`)
- Modelos activos por defecto (no-bypassed): transformer_fp8_scaled + gemma_fp8_scaled + video_vae + audio_vae + MelBandRoformer + IC LoRA + Detailer + CelebVHQ
- GGUF Q4_0 está BYPASSED por defecto (no se necesita para arrancar)
- Script 07 parchea Q4_0 → Q4_K_M automáticamente en el JSON

**Atajos de teclado en ComfyUI:**
- `0` → botón "DISABLE EVERYTHING" (punto de inicio)
- `1` → Prompt | `2` → Video settings | `3` → Image inputs
- `4` → Audio | `5` → ControlNet | `6` → ID LoRA voz | `7` → Detailer/Upscaler
- `9` → Instrucciones completas en español

**Modos de uso para Kenza UGC:**
1. T2V básico: prompt solo
2. I2V (⭐): prompt + BANANA_PRO_00006_.png como ref
3. Lipsync (⭐⭐ IDEAL): prompt + foto Kenza + audio TTS
4. Voice clone: prompt + 5s audio referencia Kenza
5. FFLF: prompt + hasta 8 keyframes de control

**Primer test pendiente:** cargar TODOENUNO → presionar 9 → leer instrucciones → presionar 0 → presionar 2 (I2V con BANANA_PRO_00006_.png)

### Cómo ejecutar en pod nuevo (v2.3):
```bash
# 1. Subir toda la carpeta LTX23_Scripts/ + LTXREALISM.json + LTX2.3TODOENUNO.json
scp -r LTX23_Scripts/ root@{pod-ip}:/workspace/
# 2. Ejecutar:
cd /workspace/LTX23_Scripts && bash run_all.sh
# 3. Arrancar:
bash /workspace/start_comfyui.sh
# 4. Abrir: https://{POD_ID}-8888.proxy.runpod.net/proxy/8188/
```

---

## Stack anterior (imagen fija)

- Imagen fija: FLUX1 + LoRA kenza v3 (`kenza_lora_v3.safetensors`) — seed 52, strength 0.85, trigger word `kenza`
- Pipeline imagen: NanoBanana en morfeo.academy (ComfyUI Deploy)
- Video talking head: LTX-Video 2.3 Audio + ComfyUI en PC-2
- Voz TTS: Cartesia Sonic 3
- Post-producción: Remotion (PC-2) + Whisper + ffmpeg
- Almacenamiento: Supabase Storage

**Foto ganadora de referencia:** `BANANA_PRO_00006_.png` — Miami waterfront, crochet top blanco + denim, full body, golden hour, iPhone UGC.

**CRÍTICO — tono de piel:**
- En NanoBanana/kenza-nanababana-fullbody: usar `white skin` (produce la foto ganadora)
- En kenza-prompt-master (FLUX1 general): usa `light olive skin` — son contextos distintos

**Character sheet:** `turnaround_00001_.png` — 3 ángulos, linen beige + LV tote. Usar como imagen base en NanoBanana.

**LoRA LTX-Video 2.3 entrenada (2026-05-12):**
- Trainer: LTX-Video-Trainer (Lightricks oficial)
- Modelo base: LTXV_2B_0.9.6_DEV
- Steps: 500, rank 64, lr 1e-4, grad_accum 1
- Dataset: 13 videos 576x1024x65 frames
- Tiempo: 4.4 min en H100 SXM
- Archivos: `comfy_lora_weights_step_00500.safetensors` (ComfyUI ready)
- Ubicación local: `C:\Users\SOPORTE2\Downloads\kenza_lora\kenza_lora\checkpoints\`
- Trigger word: `kenza`, strength recomendada: 0.8
- **PENDIENTE: probar en ComfyUI PC-2**

**Baterías de outfits pendientes:**
- B: Linen blanco + shorts beige / South Beach boardwalk
- C: Leather jacket roja + denim / Wynwood street
- D: Gold sequin mini dress / Rooftop Miami noche
- E: Black bikini top + linen pants / Hotel pool
- F: Sports set negro / Brickell sunrise

**Why:** Proyecto de agencia de influencers IA, comparativo vs modelo Aitana López (The Clueless).
**How to apply:** Cuando se pida cualquier cosa de Kenza — prompts, video, batería — usar los skills instalados y respetar la foto base BANANA_PRO_00006_ como referencia visual.
