---
name: Proyecto NORA — Agencia IA
description: Plataforma de generación de contenido publicitario con IA. Videos UGC, creatividades de marca, pipeline LTX 2.3.
type: project
originSessionId: 4a01ef39-4a8b-4c79-b31e-ac7dfa912eb5
---
NORA es una plataforma/agencia de marketing con IA que produce videos UGC testimoniales y creatividades para marcas.

**Pipeline video UGC completo (8 pasos + upscale):**
1. Cargar marca desde Supabase
2. Concepto UGC
3. Libreto (~28 palabras para ~14s de video)
4. Voz TTS con Cartesia Sonic 3 → WAV → Supabase Storage
5. Prompt LTX-Video 2.3
6. INSERT creatividad en Supabase (estado: `para_ejecucion`, origen: `ugc`)
7. Render: `node nora-pipelines/scripts/comfy-t2v-ugc.mjs --once --id=N`
8. Post-producción Remotion: subtítulos karaoke Whisper + pack de cierre

**Config LTX 2.3:**
- Modelo: ltx-2-3-22b-dev-Q4_K_M.gguf
- Resolución base: 576×1024 (9:16)
- FPS: 24 (stage 1) / 30 (mejor lip-sync)
- CFG: 1.5 (stage 1) / 1.2 (validado 2026-03-27)
- LoRA: ltx-2.3-22b-distilled-lora-384 (0.5)
- Render en PC-2 (RTX 5080 16GB, ~5-8 min)

**Marcas activas:** Equos Seguros, Meser (entre otras en Supabase)

**PC-2:** conta@192.168.1.26 (Windows, OpenSSH, Whisper Python 3.12 CUDA, Remotion en C:\Users\conta\remotion-nora\)

**Why:** Plataforma propia de agencia IA para producción masiva de contenido publicitario.
**How to apply:** Para cualquier video UGC, usar skill nora-video-ugc. Para prompts LTX usar nora-prompt-ltxvideo.
