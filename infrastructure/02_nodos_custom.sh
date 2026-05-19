#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  02_nodos_custom.sh — 15 nodos custom + stack pip vrgamedevgirl            ║
# ║  Qué hace: instala todos los custom nodes de ComfyUI + librería Python     ║
# ║  Tiempo:   ~5-10 min                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
source "$(dirname "$0")/00_config.sh"
set -euo pipefail

echo -e "${W}"
echo "  ╔════════════════════════════════════════════╗"
echo "  ║  02 — Nodos Custom (15 paquetes)  v2.3    ║"
echo "  ╚════════════════════════════════════════════╝"
echo -e "${N}"

step "PASO 2 — Instalando nodos custom"
mkdir -p "$NODES_DIR"

# 1. ComfyUI Manager — gestor de nodos desde la UI
install_node "ComfyUI-Manager" \
    "https://github.com/ltdrdata/ComfyUI-Manager.git"

# 2. RES4LYF — samplers LTX 2.3 (LTXVLoopingSampler, etc.) ← CRÍTICO
install_node "RES4LYF" \
    "https://github.com/ClownsharkBatwing/RES4LYF.git"

# 3. KJNodes — GGUFLoaderKJ, utilidades kijai ← CRÍTICO
install_node "ComfyUI-KJNodes" \
    "https://github.com/kijai/ComfyUI-KJNodes.git"

# 4. Video Helper Suite — concatenar clips, cargar video
install_node "ComfyUI-VideoHelperSuite" \
    "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git"

# 5. Impact Pack — detección de cara, masking
install_node "ComfyUI-Impact-Pack" \
    "https://github.com/ltdrdata/ComfyUI-Impact-Pack.git"

# 6. rgthree — nodos de organización del workflow
install_node "rgthree-comfy" \
    "https://github.com/rgthree/rgthree-comfy.git"

# 7. Custom Scripts (pysssss) — bookmarks, wildcards, presets
install_node "ComfyUI-Custom-Scripts" \
    "https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git"

# 8. Easy Use — wrappers simplificados de nodos complejos
install_node "ComfyUI-Easy-Use" \
    "https://github.com/yolain/ComfyUI-Easy-Use.git"

# 9. Essentials (cubiq) — nodos de utilidad estándar
install_node "ComfyUI_essentials" \
    "https://github.com/cubiq/ComfyUI_essentials.git"

# 10. WAS Node Suite — procesado de imagen, texto, latents
install_node "was-node-suite-comfyui" \
    "https://github.com/WASasquatch/was-node-suite-comfyui.git"

# 11. ComfyUI-GGUF — carga modelos GGUF (UnetLoaderGGUF) ← CRÍTICO
install_node "ComfyUI-GGUF" \
    "https://github.com/city96/ComfyUI-GGUF.git"

# 12. Frame Interpolation — FILM/RIFE para suavizar fps
install_node "ComfyUI-Frame-Interpolation" \
    "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation.git"

# 13. Unload Model — liberar VRAM entre generaciones
install_node "ComfyUI-Unload-Model" \
    "https://github.com/SeanScripts/ComfyUI-Unload-Model.git"

# 14. MelBandRoFormer — separación de stems de audio ← CRÍTICO para TODOENUNO
install_node "ComfyUI-MelBandRoFormer" \
    "https://github.com/kijai/ComfyUI-MelBandRoFormer.git"

# 15. VRGameDevGirl — Music Video Creator, FastFilmGrain, Z-Image ← CRÍTICO
# IMPORTANTE: usar repo correcto vrgamegirl19 (NO vrgamedevgirl84)
install_node "comfyui-vrgamedevgirl" \
    "https://github.com/vrgamegirl19/comfyui-vrgamedevgirl.git"

# 16. ComfyUI-PromptRelay (Kijai) — CRÍTICO para TODOENUNO
# Provee PromptRelayEncodeTimeline: prompts distintos por segmento de tiempo del video
install_node "ComfyUI-PromptRelay" \
    "https://github.com/kijai/ComfyUI-PromptRelay.git"

# ── Stack pip completo vrgamedevgirl (Music Video Creator V5.1) ───────────────
# librosa     — análisis de audio (FastFilmGrain)
# kornia      — visión computacional
# imageio     — lectura/escritura de imágenes
# torchcodec  — decodificación de video con GPU
# av          — PyAV para audio/video
# stable-ts   — transcripción Whisper alineada con timestamps
# demucs      — separación de stems (voz vs instrumental)
# transformers/accelerate — modelos HuggingFace
# google-generativeai — Gemini API (prompts opcionales)
# voxcpm      — síntesis de voz
# llama-cpp-python — inferencia GGUF local (LLaMA, SuperGemma)
step "PASO 2B — Stack pip vrgamedevgirl (Music Video Creator)"
info "Instalando stack completo..."
pip install -q \
    librosa \
    kornia \
    imageio \
    torchcodec \
    av \
    stable-ts \
    demucs \
    transformers \
    accelerate \
    google-generativeai \
    voxcpm \
    llama-cpp-python \
    && log "Stack vrgamedevgirl completo OK" \
    || warn "Algunos paquetes del stack fallaron — revisa manualmente"

# ── Verificación ──────────────────────────────────────────────────────────────
echo ""
echo -e "${W}  NODOS:${N}"
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
    else
        echo -e "  ${R}[✗]${N} $node — FALTA"
    fi
done

echo ""
log "02_nodos_custom.sh COMPLETADO"
