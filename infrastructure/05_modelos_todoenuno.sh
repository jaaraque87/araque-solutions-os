#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  05_modelos_todoenuno.sh — Modelos exclusivos del workflow TODOENUNO        ║
# ║  Qué hace: transformer fp8 · Q4_K_M GGUF · Gemma fp8_scaled ·             ║
# ║            MelBandRoformer · mmproj · IC LoRAs · CelebVHQ ID-LoRA          ║
# ║  Tiempo:   40-80 min                                                        ║
# ║  Espacio:  ~58 GB                                                           ║
# ║                                                                             ║
# ║  NOTA: Si TODOENUNO pide Q4_0.gguf → usa Q4_K_M (este script lo descarga) ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
source "$(dirname "$0")/00_config.sh"
set +e

echo -e "${W}"
echo "  ╔═══════════════════════════════════════════════════╗"
echo "  ║  05 — Modelos TODOENUNO (~58 GB)  v2.3           ║"
echo "  ║  IC LoRA · Voice ID · MelBand · Gemma fp8_scaled ║"
echo "  ╚═══════════════════════════════════════════════════╝"
echo -e "${N}"

step "PASO 3.7 — Modelos LTX2.3TODOENUNO"
warn "~58 GB — puede tomar 40-80 min"

mkdir -p "$MODELS_DIR/diffusion_models"
mkdir -p "$MODELS_DIR/text_encoders"
mkdir -p "$MODELS_DIR/audio_separator"
mkdir -p "$MODELS_DIR/llm"
mkdir -p "$MODELS_DIR/loras"

# ── [1] LTX 2.3 transformer_only fp8_scaled (25.2 GB) ────────────────────────
# El transformer del modelo separado de VAE y text encoder.
# Más eficiente en VRAM — carga sólo lo que usa.
# Repo: Kijai/LTX2.3_comfy/diffusion_models/
info "[1/8] Transformer fp8_scaled (25.2 GB) — empieza este primero"
if [ ! -f "$MODELS_DIR/diffusion_models/ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors" ]; then
    wget -q --show-progress \
        --header="Authorization: Bearer $HF_TOKEN" --continue \
        -O "$MODELS_DIR/diffusion_models/ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors" \
        "https://huggingface.co/Kijai/LTX2.3_comfy/resolve/main/diffusion_models/ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors" \
        && log "OK: transformer_only fp8_scaled" \
        || warn "Transformer fp8_scaled falló"
else
    log "Ya existe: transformer_only fp8_scaled"
fi

# ── [2] LTX 2.3 22B Distilled Q4_K_M GGUF (17.8 GB) ─────────────────────────
# TODOENUNO usa Q4_0 pero NO existe públicamente.
# Q4_K_M es el sustituto directo (mismo repo Abiray, mejor calidad incluso).
# El script 07_workflows.sh parchea el JSON para apuntar a este archivo.
info "[2/8] LTX 22B Distilled Q4_K_M (17.8 GB) — sustituto de Q4_0"
if [ ! -f "$MODELS_DIR/diffusion_models/LTX-2.3-22B-distilled-1.1-Q4_K_M.gguf" ]; then
    wget -q --show-progress \
        --header="Authorization: Bearer $HF_TOKEN" --continue \
        -O "$MODELS_DIR/diffusion_models/LTX-2.3-22B-distilled-1.1-Q4_K_M.gguf" \
        "https://huggingface.co/Abiray/LTX-2.3-22B-DISTILLED-1.1-GGUF/resolve/main/LTX-2.3-22B-distilled-1.1-Q4_K_M.gguf" \
        && log "OK: LTX Q4_K_M GGUF" \
        || warn "LTX Q4_K_M falló"
else
    log "Ya existe: LTX Q4_K_M GGUF"
fi

# ── [3] Gemma 3 12B fp8_scaled (13.2 GB) ─────────────────────────────────────
# DIFERENTE del fp4_mixed (script 03).
# TODOENUNO usa la variante fp8_scaled → mayor calidad de prompts.
# Repo: Comfy-Org/ltx-2/split_files/text_encoders/
info "[3/8] Gemma 3 12B fp8_scaled (13.2 GB)"
hf_dl "Comfy-Org/ltx-2" \
      "split_files/text_encoders/gemma_3_12B_it_fp8_scaled.safetensors" \
      "text_encoders" \
    || warn "Gemma fp8_scaled falló — TODOENUNO puede usar fp4_mixed como fallback"

# ── [4] MelBandRoformer fp16 (456 MB) ────────────────────────────────────────
# Separador de stems de audio (voz vs instrumental).
# Requerido por nodo MelBandRoFormerModelLoader en TODOENUNO.
# Va en models/audio_separator/ (ruta específica del nodo kijai)
info "[4/8] MelBandRoformer fp16 (456 MB)"
if [ ! -f "$MODELS_DIR/audio_separator/MelBandRoformer_fp16.safetensors" ]; then
    wget -q --show-progress \
        --header="Authorization: Bearer $HF_TOKEN" --continue \
        -O "$MODELS_DIR/audio_separator/MelBandRoformer_fp16.safetensors" \
        "https://huggingface.co/Kijai/MelBandRoFormer_comfy/resolve/main/MelBandRoformer_fp16.safetensors" \
        && log "OK: MelBandRoformer fp16" \
        || warn "MelBandRoformer falló"
else
    log "Ya existe: MelBandRoformer_fp16"
fi

# ── [5] mmproj-BF16.gguf (1.19 GB) ───────────────────────────────────────────
# Multimodal projector para SuperGemma → habilita visión (análisis de imagen).
# Usado por VRGDG_SuperGemmaGGUFChat cuando recibe imagen de referencia.
# Repo: unsloth/gemma-4-26B-A4B-it-GGUF
info "[5/8] mmproj-BF16.gguf (1.19 GB) — SuperGemma visión multimodal"
if [ ! -f "$MODELS_DIR/llm/mmproj-BF16.gguf" ]; then
    wget -q --show-progress \
        --header="Authorization: Bearer $HF_TOKEN" --continue \
        -O "$MODELS_DIR/llm/mmproj-BF16.gguf" \
        "https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF/resolve/main/mmproj-BF16.gguf" \
        && log "OK: mmproj-BF16.gguf" \
        || warn "mmproj falló"
else
    log "Ya existe: mmproj-BF16.gguf"
fi

# ── [6] IC LoRA Union Control ref0.5 (654 MB) ────────────────────────────────
# Image Conditioning LoRA — permite dar una imagen de referencia visual.
# Con esta LoRA puedes mantener la composición/estilo de una imagen en el video.
# Repo: Lightricks/LTX-2.3-22b-IC-LoRA-Union-Control
info "[6/8] IC LoRA Union Control ref0.5 (654 MB)"
hf_dl "Lightricks/LTX-2.3-22b-IC-LoRA-Union-Control" \
      "ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors" \
      "loras" \
    || warn "IC LoRA Union Control falló"

# ── [7] IC LoRA Detailer 19B ──────────────────────────────────────────────────
# Mejora detalle y sharpness en segunda etapa del pipeline TODOENUNO.
# Lightricks/LTX-2-19b-IC-LoRA-Detailer
info "[7/8] IC LoRA Detailer 19B"
hf_dl "Lightricks/LTX-2-19b-IC-LoRA-Detailer" \
      "ltx-2-19b-ic-lora-detailer.safetensors" \
      "loras" \
    || warn "IC LoRA Detailer falló"

# ── [8] CelebVHQ ID-LoRA (face identity) ─────────────────────────────────────
# Preserva la identidad facial a lo largo del video.
# CRÍTICO para Kenza: mantiene su cara consistente en todos los clips.
# Repo: Comfy-Org/ltx-2.3/split_files/loras/
info "[8/8] CelebVHQ ID-LoRA (face identity — CRÍTICO para Kenza)"
hf_dl "Comfy-Org/ltx-2.3" \
      "split_files/loras/ltx-2.3-id-lora-celebvhq-3k.safetensors" \
      "loras" \
    || warn "CelebVHQ ID-LoRA falló"

# ── [9] Dynamic LoRAs (nuevos — VideoFlow v3.0 + LTX Director v3.0) ──────────
# Mejoran la dinámica de movimiento y fluidez del video.
# Repos: Lightricks/LTX-2.3
info "[9] Dynamic LoRA rank111 bf16"
hf_dl "Lightricks/LTX-2.3" \
      "ltx-2.3-22b-distilled-1.1_lora-dynamic_fro09_avg_rank_111_bf16.safetensors" \
      "loras" \
    || warn "Dynamic LoRA rank111 falló"

info "[9b] Dynamic LoRA rank105 bf16"
hf_dl "Lightricks/LTX-2.3" \
      "ltx-2.3-22b-distilled-lora-dynamic_fro09_avg_rank_105_bf16.safetensors" \
      "loras" \
    || warn "Dynamic LoRA rank105 falló"

# ── [10] MelBandRoformer.ckpt (versión original ckpt) ────────────────────────
# Algunos workflows usan el .ckpt en vez del fp16.safetensors
info "[10] MelBandRoformer.ckpt (original)"
if [ ! -f "$MODELS_DIR/audio_separator/MelBandRoformer.ckpt" ]; then
    wget -q --show-progress \
        --header="Authorization: Bearer $HF_TOKEN" --continue \
        -O "$MODELS_DIR/audio_separator/MelBandRoformer.ckpt" \
        "https://huggingface.co/Kijai/MelBandRoFormer_comfy/resolve/main/MelBandRoformer.ckpt" \
        && log "OK: MelBandRoformer.ckpt" \
        || warn "MelBandRoformer.ckpt falló"
else
    log "Ya existe: MelBandRoformer.ckpt"
fi

# ── [11] DW Preprocessor model ────────────────────────────────────────────────
# Para nodo DWPreprocessor (pose detection) — workflows VideoFlow v3.0
mkdir -p "$COMFY_DIR/custom_nodes/comfyui_controlnet_aux/ckpts/yzd-v/DWPose"
DW_DEST="$COMFY_DIR/custom_nodes/comfyui_controlnet_aux/ckpts/yzd-v/DWPose"
info "[11] DW Preprocessor: dw-ll_ucoco_384 (pose detection)"
if [ ! -f "$DW_DEST/dw-ll_ucoco_384_bs5.torchscript.pt" ]; then
    wget -q --show-progress --continue \
        -O "$DW_DEST/dw-ll_ucoco_384_bs5.torchscript.pt" \
        "https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384_bs5.torchscript.pt" \
        && log "OK: dw-ll_ucoco_384_bs5.torchscript.pt" \
        || warn "DW Preprocessor falló"
else
    log "Ya existe: dw-ll_ucoco_384_bs5.torchscript.pt"
fi

# ── Opcional: gemma abliterated sikaworld ─────────────────────────────────────
warn "MODELO OPCIONAL — descarga manual:"
warn "  gemma-3-12b-it-abliterated-sikaworld-high-fidelity-edition.safetensors"
warn "  → https://huggingface.co/models?search=gemma+abliterated+sikaworld"
warn "  → Destino: $MODELS_DIR/text_encoders/"

# ── Verificación ──────────────────────────────────────────────────────────────
echo ""
echo -e "${W}  MODELOS TODOENUNO:${N}"
echo "  ──────────────────────────────────────────────"
check_model "diffusion_models/ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors" "Transformer fp8_scaled (25.2 GB) ⭐"
check_model "diffusion_models/LTX-2.3-22B-distilled-1.1-Q4_K_M.gguf"       "LTX 22B Q4_K_M GGUF (17.8 GB)"
check_model "text_encoders/gemma_3_12B_it_fp8_scaled.safetensors"            "Gemma 12B fp8_scaled (13.2 GB)"
check_model "audio_separator/MelBandRoformer_fp16.safetensors"               "MelBandRoformer fp16 (456 MB)"
check_model "llm/mmproj-BF16.gguf"                                           "mmproj-BF16 visión (1.19 GB)"
check_model "loras/ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors"    "IC LoRA Union Control (654 MB)"
check_model "loras/ltx-2-19b-ic-lora-detailer.safetensors"                  "IC LoRA Detailer 19B"
check_model "loras/ltx-2.3-id-lora-celebvhq-3k.safetensors"                "CelebVHQ ID-LoRA ⭐ Kenza face"
check_model "loras/ltx-2.3-22b-distilled-1.1_lora-dynamic_fro09_avg_rank_111_bf16.safetensors" "Dynamic LoRA rank111"
check_model "loras/ltx-2.3-22b-distilled-lora-dynamic_fro09_avg_rank_105_bf16.safetensors"     "Dynamic LoRA rank105"
check_model "audio_separator/MelBandRoformer.ckpt"                       "MelBandRoformer.ckpt (original)"

echo ""
log "05_modelos_todoenuno.sh COMPLETADO"
