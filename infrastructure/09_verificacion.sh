#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  09_verificacion.sh — Verificar que todo está instalado                    ║
# ║  Qué hace: checkea TODOS los modelos, nodos y workflows                   ║
# ║  Cuándo:   Después de correr todos los scripts (01-08) o cuando quieras   ║
# ║            saber qué falta                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
source "$(dirname "$0")/00_config.sh"

echo -e "${W}"
echo "  ╔════════════════════════════════════════════════════╗"
echo "  ║  09 — Verificación completa ARAQUE SOLUTIONS v2.3 ║"
echo "  ╚════════════════════════════════════════════════════╝"
echo -e "${N}"

MISSING=0
OK=0

check_model_count() {
    local path="$MODELS_DIR/$1" name="$2"
    if [ -f "$path" ]; then
        local size
        size=$(du -sh "$path" 2>/dev/null | cut -f1)
        echo -e "  ${G}[✓]${N} $name ($size)"
        OK=$((OK+1))
    else
        echo -e "  ${R}[✗]${N} $name — FALTA"
        MISSING=$((MISSING+1))
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
# MODELOS BASE (script 03)
# ══════════════════════════════════════════════════════════════════════════════
echo -e "\n${W}  ━━━ MODELOS BASE (~55 GB) ━━━${N}"
check_model_count "checkpoints/ltx-2.3-22b-dev-fp8.safetensors"                     "Checkpoint fp8 (29.1 GB)"
check_model_count "text_encoders/ltx-2.3_text_projection_bf16.safetensors"           "Text Projection bf16 (2.31 GB)"
check_model_count "text_encoders/gemma_3_12B_it_fp4_mixed.safetensors"               "Gemma 12B fp4 mixed (9.45 GB)"
check_model_count "text_encoders/tokenizer.model"                                    "Gemma tokenizer (FIX ValueError)"
check_model_count "vae/LTX23_audio_vae_bf16.safetensors"                             "Audio VAE (365 MB)"
check_model_count "vae/LTX23_video_vae_bf16.safetensors"                             "Video VAE (1.45 GB)"
check_model_count "vae/taeltx2_3.safetensors"                                        "TAE (23.5 MB)"
check_model_count "latent_upscale_models/ltx-2.3-spatial-upscaler-x1.5-1.0.safetensors" "Upscaler x1.5 (1.09 GB)"
check_model_count "latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.0.safetensors"   "Upscaler x2 v1.0 (996 MB)"
check_model_count "latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.1.safetensors"   "Upscaler x2 v1.1"
check_model_count "loras/ltx-2.3-22b-distilled-lora-384-1.1.safetensors"            "Distilled LoRA 1.1 (7.61 GB)"

# ══════════════════════════════════════════════════════════════════════════════
# MUSIC VIDEO CREATOR (script 04)
# ══════════════════════════════════════════════════════════════════════════════
echo -e "\n${W}  ━━━ MUSIC VIDEO CREATOR (~70 GB) ━━━${N}"
check_model_count "checkpoints/z_image_turbo_bf16.safetensors"                      "Z-Image Turbo bf16"
check_model_count "text_encoders/qwen_3_4b.safetensors"                             "Qwen 3 4B CLIP"
check_model_count "llm/Llama-3.2-3B-Instruct-Q4_K_M.gguf"                          "LLaMA 3.2 3B Q4_K_M"
check_model_count "llm/supergemma4-26b-uncensored-fast-v2-Q4_K_M.gguf"             "SuperGemma 4 26B (16.8 GB)"
check_model_count "diffusion_models/LTX-2.3-22B-distilled-1.1-Q6_K.gguf"          "LTX 22B distilled Q6_K (21 GB)"
check_model_count "vae/ae.safetensors"                                               "FLUX VAE ae.safetensors"
check_model_count "vae/ltx-av-step-1751000_vocoder_24K.safetensors"                 "LTX-AV Vocoder 24K"

# ══════════════════════════════════════════════════════════════════════════════
# TODOENUNO (script 05)
# ══════════════════════════════════════════════════════════════════════════════
echo -e "\n${W}  ━━━ TODOENUNO (~58 GB) ━━━${N}"
check_model_count "diffusion_models/ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors" "Transformer fp8_scaled (25.2 GB) ⭐"
check_model_count "diffusion_models/LTX-2.3-22B-distilled-1.1-Q4_K_M.gguf"        "LTX Q4_K_M GGUF (17.8 GB)"
check_model_count "text_encoders/gemma_3_12B_it_fp8_scaled.safetensors"             "Gemma 12B fp8_scaled (13.2 GB)"
check_model_count "audio_separator/MelBandRoformer_fp16.safetensors"                "MelBandRoformer fp16 (456 MB)"
check_model_count "llm/mmproj-BF16.gguf"                                            "mmproj-BF16 visión (1.19 GB)"
check_model_count "loras/ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors"     "IC LoRA Union Control (654 MB)"
check_model_count "loras/ltx-2-19b-ic-lora-detailer.safetensors"                   "IC LoRA Detailer 19B"
check_model_count "loras/ltx-2.3-id-lora-celebvhq-3k.safetensors"                 "CelebVHQ ID-LoRA ⭐ Kenza face"

# ══════════════════════════════════════════════════════════════════════════════
# LoRAs (script 06)
# ══════════════════════════════════════════════════════════════════════════════
echo -e "\n${W}  ━━━ LoRAs ━━━${N}"
check_model_count "loras/ltx-2.3-id-lora-talkvid-3k.safetensors"       "TalkVid ID-LoRA (1.13 GB)"
check_model_count "loras/LTX2.3_Soft_Enhance.safetensors"              "Soft Enhance LoRA"
check_model_count "loras/LTX2.3_Crisp_Enhance.safetensors"             "Crisp Enhance LoRA ⭐"
check_model_count "loras/LTX2.3_Luxe_Sensual.safetensors"              "Luxe Sensual LoRA ⭐ Kenza"
check_model_count "loras/LTX2.3_Post_Apocalyptic.safetensors"          "Post Apocalyptic LoRA"
check_model_count "loras/LTX2.3_Wild_West.safetensors"                 "Wild West LoRA"
check_model_count "loras/LTX23_Enhancers_CrispSoft.safetensors"        "Enhancers CrispSoft (CivitAI)"
check_model_count "loras/LTX23-GalaxyAce.safetensors"                  "GalaxyAce LoRA (1.88 GB)"
check_model_count "loras/AmateurHour_01_rank16.safetensors"            "AmateurHour LoRA"

# ══════════════════════════════════════════════════════════════════════════════
# Workflows
# ══════════════════════════════════════════════════════════════════════════════
echo -e "\n${W}  ━━━ WORKFLOWS ━━━${N}"
for wf in \
    "VideoFlow_LTX23_AllInOne_v3.json" \
    "LTX2.3_Music_Video_Creator_Prompt_Creator_V5.json" \
    "LTX2.3_Music_Video_Creator_T2V_V5.1.json" \
    "LTX2.3_Music_Video_Creator_I2V_V5.1.json" \
    "LTX2.3TODOENUNO.json"; do
    if [ -f "$WORKFLOWS_DIR/$wf" ]; then
        echo -e "  ${G}[✓]${N} $wf"
        OK=$((OK+1))
    else
        echo -e "  ${R}[✗]${N} $wf — FALTA"
        MISSING=$((MISSING+1))
    fi
done

# ══════════════════════════════════════════════════════════════════════════════
# Nodos custom
# ══════════════════════════════════════════════════════════════════════════════
echo -e "\n${W}  ━━━ NODOS CUSTOM ━━━${N}"
for node in \
    "ComfyUI-Manager" "RES4LYF" "ComfyUI-KJNodes" \
    "ComfyUI-VideoHelperSuite" "ComfyUI-Impact-Pack" \
    "rgthree-comfy" "ComfyUI-Custom-Scripts" \
    "ComfyUI-Easy-Use" "ComfyUI_essentials" \
    "was-node-suite-comfyui" "ComfyUI-GGUF" \
    "ComfyUI-Frame-Interpolation" "ComfyUI-Unload-Model" \
    "ComfyUI-MelBandRoFormer" "comfyui-vrgamedevgirl" \
    "ComfyUI-PromptRelay"; do
    if [ -d "$NODES_DIR/$node" ]; then
        echo -e "  ${G}[✓]${N} $node"
        OK=$((OK+1))
    else
        echo -e "  ${R}[✗]${N} $node — FALTA"
        MISSING=$((MISSING+1))
    fi
done

# ══════════════════════════════════════════════════════════════════════════════
# Resumen final
# ══════════════════════════════════════════════════════════════════════════════
echo ""
echo "  ══════════════════════════════════════════════"
TOTAL=$((OK+MISSING))
echo -e "  Total: ${G}$OK/$TOTAL${N} instalados"
if [ "$MISSING" -gt 0 ]; then
    echo -e "  ${R}$MISSING${N} elementos faltantes — revisa los scripts correspondientes"
else
    echo -e "  ${G}✓ Instalación completa — listo para producción Kenza UGC${N}"
fi
echo "  ══════════════════════════════════════════════"
echo ""
echo -e "  Para arrancar: ${C}bash /workspace/start_comfyui.sh${N}"
echo -e "  URL de acceso: ${C}https://{POD_ID}-8888.proxy.runpod.net/proxy/8188/${N}"
echo ""
