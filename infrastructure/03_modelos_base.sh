#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  03_modelos_base.sh — Modelos base LTX 2.3 (~55 GB)                       ║
# ║  Qué hace: checkpoint fp8 · Gemma encoders · VAEs · upscalers · LoRA dist ║
# ║  Tiempo:   20-40 min según velocidad del pod                               ║
# ║  Espacio:  ~55 GB                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
source "$(dirname "$0")/00_config.sh"
set +e  # descargas no-fatales

echo -e "${W}"
echo "  ╔════════════════════════════════════════════╗"
echo "  ║  03 — Modelos Base LTX 2.3 (~55 GB) v2.3 ║"
echo "  ╚════════════════════════════════════════════╝"
echo -e "${N}"

step "PASO 3 — Modelos principales"
warn "Puede tomar 20-40 min según velocidad del pod"

mkdir -p "$MODELS_DIR/checkpoints"
mkdir -p "$MODELS_DIR/text_encoders"
mkdir -p "$MODELS_DIR/vae"
mkdir -p "$MODELS_DIR/latent_upscale_models"
mkdir -p "$MODELS_DIR/loras"

# ── CHECKPOINT fp8 (29.1 GB) ─────────────────────────────────────────────────
# El checkpoint principal del modelo. Lightricks/LTX-2.3-fp8
info "[1/9] Checkpoint fp8 (29.1 GB) — el más grande, empieza primero"
hf_dl "Lightricks/LTX-2.3-fp8" \
      "ltx-2.3-22b-dev-fp8.safetensors" \
      "checkpoints" \
    || warn "Checkpoint fp8 falló"

# ── TEXT ENCODERS ─────────────────────────────────────────────────────────────
# text_projection — proyecta embeddings de texto al espacio del modelo
info "[2/9] Text Projection bf16 (2.31 GB)"
hf_dl "Kijai/LTX2.3_comfy" \
      "text_encoders/ltx-2.3_text_projection_bf16.safetensors" \
      "text_encoders" \
    || warn "text_projection falló"

# Gemma 3 12B fp4 mixed (9.45 GB) — text encoder principal (modo eficiente)
info "[3/9] Gemma 3 12B fp4 mixed (9.45 GB)"
hf_dl "Comfy-Org/ltx-2" \
      "split_files/text_encoders/gemma_3_12B_it_fp4_mixed.safetensors" \
      "text_encoders" \
    || warn "Gemma fp4 falló"

# Gemma tokenizer.model — FIX "invalid tokenizer" ValueError
# Sin este archivo ComfyUI falla al cargar Gemma como text encoder
info "[4/9] Gemma tokenizer.model (FIX ValueError)"
hf_dl "Comfy-Org/ltx-2" \
      "split_files/text_encoders/tokenizer.model" \
      "text_encoders" \
    || warn "Gemma tokenizer falló — intentando fuente alternativa"
# Fallback
[ ! -f "$MODELS_DIR/text_encoders/tokenizer.model" ] && \
hf_dl "Lightricks/LTX-2.3" \
      "tokenizer.model" \
      "text_encoders" \
    || warn "tokenizer.model no disponible — pueden haber errores con Gemma"

# ── VAEs ──────────────────────────────────────────────────────────────────────
info "[5/9] Audio VAE bf16 (365 MB)"
hf_dl "Kijai/LTX2.3_comfy" \
      "vae/LTX23_audio_vae_bf16.safetensors" \
      "vae" \
    || warn "Audio VAE falló"

info "[5b] Video VAE bf16 (1.45 GB)"
hf_dl "Kijai/LTX2.3_comfy" \
      "vae/LTX23_video_vae_bf16.safetensors" \
      "vae" \
    || warn "Video VAE falló"

info "[5c] TAE (23.5 MB)"
hf_dl "Kijai/LTX2.3_comfy" \
      "vae/taeltx2_3.safetensors" \
      "vae" \
    || warn "TAE falló"

# ── UPSCALERS ─────────────────────────────────────────────────────────────────
info "[6/9] Upscaler x1.5 (1.09 GB)"
hf_dl "Lightricks/LTX-2.3" \
      "ltx-2.3-spatial-upscaler-x1.5-1.0.safetensors" \
      "latent_upscale_models" \
    || warn "Upscaler x1.5 falló"

info "[7/9] Upscaler x2 v1.0 (996 MB)"
hf_dl "Lightricks/LTX-2.3" \
      "ltx-2.3-spatial-upscaler-x2-1.0.safetensors" \
      "latent_upscale_models" \
    || warn "Upscaler x2 v1.0 falló"

info "[7b] Upscaler x2 v1.1 (requerido por workflows nuevos)"
hf_dl "Lightricks/LTX-2.3" \
      "ltx-2.3-spatial-upscaler-x2-1.1.safetensors" \
      "latent_upscale_models" \
    || warn "Upscaler x2 v1.1 falló"

# ── DISTILLED LoRA 1.1 (7.61 GB) ─────────────────────────────────────────────
# Permite usar el modelo en modo distilled sin el checkpoint completo
info "[8/9] Distilled LoRA 384 v1.1 (7.61 GB)"
hf_dl "Lightricks/LTX-2.3" \
      "ltx-2.3-22b-distilled-lora-384-1.1.safetensors" \
      "loras" \
    || warn "Distilled LoRA falló"

# ── Verificación ──────────────────────────────────────────────────────────────
echo ""
echo -e "${W}  MODELOS BASE:${N}"
echo "  ──────────────────────────────────────────────"
check_model "checkpoints/ltx-2.3-22b-dev-fp8.safetensors"                     "Checkpoint fp8 (29.1 GB)"
check_model "text_encoders/ltx-2.3_text_projection_bf16.safetensors"           "Text Projection bf16 (2.31 GB)"
check_model "text_encoders/gemma_3_12B_it_fp4_mixed.safetensors"               "Gemma 12B fp4 mixed (9.45 GB)"
check_model "text_encoders/tokenizer.model"                                    "Gemma tokenizer"
check_model "vae/LTX23_audio_vae_bf16.safetensors"                             "Audio VAE (365 MB)"
check_model "vae/LTX23_video_vae_bf16.safetensors"                             "Video VAE (1.45 GB)"
check_model "vae/taeltx2_3.safetensors"                                        "TAE (23.5 MB)"
check_model "latent_upscale_models/ltx-2.3-spatial-upscaler-x1.5-1.0.safetensors" "Upscaler x1.5 (1.09 GB)"
check_model "latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.0.safetensors"   "Upscaler x2 v1.0 (996 MB)"
check_model "latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.1.safetensors"   "Upscaler x2 v1.1"
check_model "loras/ltx-2.3-22b-distilled-lora-384-1.1.safetensors"            "Distilled LoRA 1.1 (7.61 GB)"

echo ""
log "03_modelos_base.sh COMPLETADO"
