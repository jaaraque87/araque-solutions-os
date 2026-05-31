#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ARAQUE SOLUTIONS — Instalador Universal v5.0                              ║
# ║  Compatible: RunPod · Vast.ai · TensorDock · Lambda                       ║
# ║  GPUs recomendadas: L40S, RTX 4090, A100                                  ║
# ║                                                                             ║
# ║  USO:                                                                       ║
# ║  export HF_TOKEN="hf_xxx" \                                                ║
# ║    CIVITAI_TOKEN="xxx" \                                                    ║
# ║    GITHUB_TOKEN="ghp_xxx" \                                                 ║
# ║    R2_ACCESS_KEY_ID="xxx" \                                                 ║
# ║    R2_SECRET_ACCESS_KEY="xxx" \                                             ║
# ║    R2_ACCOUNT_ID="xxx" && \                                                 ║
# ║  bash <(curl -fsSL https://raw.githubusercontent.com/jaaraque87/araque-solutions-os/main/infrastructure/install.sh)
# ╚══════════════════════════════════════════════════════════════════════════════╝
 
HF_TOKEN="${HF_TOKEN:-}"
CIVITAI_TOKEN="${CIVITAI_TOKEN:-}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
GITHUB_USER="${GITHUB_USER:-jaaraque87}"
GITHUB_REPO="${GITHUB_REPO:-araque-solutions-os}"
R2_ACCOUNT_ID="${R2_ACCOUNT_ID:-}"
R2_ACCESS_KEY_ID="${R2_ACCESS_KEY_ID:-}"
R2_SECRET_ACCESS_KEY="${R2_SECRET_ACCESS_KEY:-}"
R2_BUCKET="${R2_BUCKET:-kenza-models}"
R2_ENDPOINT="https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
 
export HF_TOKEN CIVITAI_TOKEN GITHUB_TOKEN GITHUB_USER GITHUB_REPO
export R2_ACCOUNT_ID R2_ACCESS_KEY_ID R2_SECRET_ACCESS_KEY R2_BUCKET R2_ENDPOINT
export GIT_TERMINAL_PROMPT=0 PIP_ROOT_USER_ACTION=ignore DEBIAN_FRONTEND=noninteractive
 
R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'; C='\033[0;36m'; W='\033[1;37m'; N='\033[0m'
ok()   { echo -e "${G}[✓]${N} $*"; }
warn() { echo -e "${Y}[⚠]${N} $*"; }
err()  { echo -e "${R}[✗]${N} $*"; }
step() { echo -e "\n${C}━━━━ $* ━━━━${N}"; }
 
echo ""
echo -e "${W}╔══════════════════════════════════════════════════════╗${N}"
echo -e "${W}║   ARAQUE SOLUTIONS — Instalador v5.0                ║${N}"
echo -e "${W}║   ComfyUI + LTX 2.3 + Kenza Stack                  ║${N}"
echo -e "${W}╚══════════════════════════════════════════════════════╝${N}"
 
[ -z "$HF_TOKEN" ]             && { err "HF_TOKEN no definido"; exit 1; }
[ -z "$R2_ACCESS_KEY_ID" ]     && { err "R2_ACCESS_KEY_ID no definido"; exit 1; }
[ -z "$R2_SECRET_ACCESS_KEY" ] && { err "R2_SECRET_ACCESS_KEY no definido"; exit 1; }
[ -z "$R2_ACCOUNT_ID" ]        && { err "R2_ACCOUNT_ID no definido"; exit 1; }
ok "Tokens verificados"
 
START_TOTAL=$(date +%s)
 
# ── PASO 1 — Plataforma ───────────────────────────────────────────────────────
step "PASO 1/8 — Plataforma"
if   [ -d "/workspace" ] && [ -w "/workspace" ]; then BASE_DIR="/workspace"; PLATFORM="RunPod"
elif [ -d "/root"      ] && [ -w "/root"      ]; then BASE_DIR="/root";      PLATFORM="Vast/TensorDock"
elif [ -d "/home/ubuntu"] && [ -w "/home/ubuntu"]; then BASE_DIR="/home/ubuntu"; PLATFORM="Lambda"
else BASE_DIR="/workspace"; PLATFORM="Unknown"; fi
 
COMFY_DIR="$BASE_DIR/ComfyUI"
MODELS_DIR="$COMFY_DIR/models"
NODES_DIR="$COMFY_DIR/custom_nodes"
WORKFLOWS_DIR="$COMFY_DIR/user/default/workflows"
REPO_DIR="$BASE_DIR/araque"
export BASE_DIR COMFY_DIR MODELS_DIR NODES_DIR WORKFLOWS_DIR
ok "Plataforma: $PLATFORM | Base: $BASE_DIR"
 
# ── PASO 2 — Dependencias sistema + R2 ───────────────────────────────────────
step "PASO 2/8 — Dependencias"
apt-get update -qq 2>/dev/null || true
apt-get install -y -qq git wget curl ffmpeg libgl1 libglib2.0-0 unzip 2>/dev/null || true
 
USE_R2=false
if ! command -v rclone &>/dev/null; then
    curl -fsSL https://rclone.org/install.sh | bash -s -- --quiet 2>/dev/null || true
fi
if command -v rclone &>/dev/null; then
    mkdir -p ~/.config/rclone
    printf "[r2]\ntype = s3\nprovider = Cloudflare\naccess_key_id = %s\nsecret_access_key = %s\nendpoint = %s\nacl = private\n" \
        "$R2_ACCESS_KEY_ID" "$R2_SECRET_ACCESS_KEY" "$R2_ENDPOINT" > ~/.config/rclone/rclone.conf
    rclone lsd r2:$R2_BUCKET 2>/dev/null && USE_R2=true && ok "R2 conectado ⚡" || warn "R2 no disponible — usando HF"
fi
ok "Sistema listo"
 
# ── PASO 3 — Repo ─────────────────────────────────────────────────────────────
step "PASO 3/8 — Repositorio"
if [ -n "$GITHUB_TOKEN" ]; then
    CLONE_URL="https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"
else
    CLONE_URL="https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"
fi
if [ -d "$REPO_DIR/.git" ]; then
    cd "$REPO_DIR" && git pull --quiet origin main 2>/dev/null || true && ok "Repo actualizado"
else
    git clone --depth=1 "$CLONE_URL" "$REPO_DIR" 2>/dev/null && ok "Repo clonado" || { err "No se pudo clonar"; exit 1; }
fi
 
# ── PASO 4 — ComfyUI ──────────────────────────────────────────────────────────
step "PASO 4/8 — ComfyUI"
mkdir -p "$MODELS_DIR" "$NODES_DIR" "$WORKFLOWS_DIR"
 
if [ -d "$COMFY_DIR" ] && [ ! -d "$COMFY_DIR/.git" ]; then
    warn "ComfyUI existe sin git — convirtiendo..."
    cd "$COMFY_DIR"
    git init --quiet
    git remote add origin https://github.com/comfyanonymous/ComfyUI.git 2>/dev/null || true
    git fetch --depth=1 --quiet origin master 2>/dev/null || git fetch --depth=1 --quiet origin main 2>/dev/null || true
    git checkout --quiet -f FETCH_HEAD 2>/dev/null || true
    ok "ComfyUI convertido desde template"
elif [ -d "$COMFY_DIR/.git" ]; then
    ok "ComfyUI ya existe"
    cd "$COMFY_DIR" && git pull --quiet 2>/dev/null || true
else
    git clone --depth=1 https://github.com/comfyanonymous/ComfyUI.git "$COMFY_DIR" && ok "ComfyUI clonado" || { err "Falló"; exit 1; }
fi
 
pip install -q -r "$COMFY_DIR/requirements.txt" 2>/dev/null && ok "Requirements ComfyUI OK" || warn "Algunos fallaron"
 
# Detectar versión CUDA del driver y usar PyTorch compatible
CUDA_DRIVER=$(nvidia-smi 2>/dev/null | grep "CUDA Version" | awk '{print $9}' | tr -d '.')
if [ -n "$CUDA_DRIVER" ] && [ "$CUDA_DRIVER" -lt "1240" ] 2>/dev/null; then
    warn "Driver CUDA $CUDA_DRIVER detectado — usando PyTorch cu121"
    pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --force-reinstall 2>/dev/null
else
    pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124 2>/dev/null || true
fi
python3 -c "import torch; assert torch.cuda.is_available()" 2>/dev/null && ok "CUDA OK" || warn "CUDA no disponible"
 
# ── PASO 4b — Dependencias críticas ──────────────────────────────────────────
step "PASO 4b/8 — Dependencias adicionales"
pip install -q \
    gitpython \
    opencv-python \
    gguf \
    watchdog \
    imageio-ffmpeg \
    rotary-embedding-torch \
    toml \
    sqlalchemy \
    alembic \
    tqdm \
    piexif \
    uv \
    scipy \
    einops \
    spandrel \
    "transformers>=4.50.3,<5.0.0" \
    "kornia==0.7.3" \
    "safetensors>=0.4.2" \
    && ok "Dependencias adicionales OK" || warn "Algunas fallaron"
 
# ── PASO 5 — Custom nodes ─────────────────────────────────────────────────────
step "PASO 5/8 — Custom nodes"
inode() {
    local name="$1" url="$2"
    local d="$NODES_DIR/$name"
    [ -d "$d" ] && { cd "$d" && git pull --quiet 2>/dev/null || true; ok "OK: $name"; } || \
        { GIT_TERMINAL_PROMPT=0 git clone --depth=1 --quiet "$url" "$d" 2>/dev/null && ok "Instalado: $name" || warn "Falló: $name"; }
    [ -f "$d/requirements.txt" ] && pip install -q -r "$d/requirements.txt" 2>/dev/null || true
    cd "$BASE_DIR"
}
 
# Core
inode "ComfyUI-Manager"               "https://github.com/ltdrdata/ComfyUI-Manager"
inode "ComfyUI-KJNodes"               "https://github.com/kijai/ComfyUI-KJNodes"
inode "ComfyUI-LTXVideo"              "https://github.com/Lightricks/ComfyUI-LTXVideo"
inode "ComfyUI-VideoHelperSuite"      "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite"
inode "ComfyUI-Advanced-ControlNet"   "https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet"
inode "ComfyUI_IPAdapter_plus"        "https://github.com/cubiq/ComfyUI_IPAdapter_plus"
inode "ComfyUI-AnimateDiff-Evolved"   "https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved"
inode "rgthree-comfy"                 "https://github.com/rgthree/rgthree-comfy"
inode "ComfyUI-GGUF"                  "https://github.com/city96/ComfyUI-GGUF"
inode "ComfyUI_Comfyroll_CustomNodes" "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes"
inode "comfyui-mixlab-nodes"          "https://github.com/shadowcz007/comfyui-mixlab-nodes"
inode "ComfyUI-MelBandRoformer"       "https://github.com/kijai/ComfyUI-MelBandRoformer"
inode "ComfyUI-Impact-Pack"           "https://github.com/ltdrdata/ComfyUI-Impact-Pack"
inode "ComfyUI-Inspire-Pack"          "https://github.com/ltdrdata/ComfyUI-Inspire-Pack"
inode "comfyui_essentials"            "https://github.com/cubiq/ComfyUI_essentials"
inode "ComfyUI-Custom-Scripts"        "https://github.com/pythongosssss/ComfyUI-Custom-Scripts"
inode "comfyui-easy-use"              "https://github.com/yolain/ComfyUI-Easy-Use"
inode "ComfyUI-Frame-Interpolation"   "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation"
inode "RES4LYF"                       "https://github.com/ClownsharkBatwing/RES4LYF"
inode "was-node-suite-comfyui"        "https://github.com/WASasquatch/was-node-suite-comfyui"
inode "cg-use-everywhere"             "https://github.com/chrisgoringe/cg-use-everywhere"
inode "comfyui-vrgamedevgirl"         "https://github.com/vrgamegirl19/comfyui-vrgamedevgirl"
inode "comfyui_controlnet_aux"        "https://github.com/Fannovel16/comfyui_controlnet_aux"
# URLs corregidas
inode "comfyui-unload-model"          "https://github.com/bhaskershivadas/ComfyUI-ModelUnloader"
inode "WhatDreamsCost-ComfyUI"        "https://github.com/WhatDreamsCost/ComfyUI-LTXDirector"
inode "tts_audio_suite"               "https://github.com/ShmuelRonen/ComfyUI-AudioAnalyzer"
inode "crt-nodes"                     "https://github.com/ihmyt/comfyui-crt-nodes"
inode "Comfyui-Resolution-Master"     "https://github.com/Extraltodeus/ComfyUI-ResolutionMaster"
inode "Listhelper"                    "https://github.com/liusida/ComfyUI-ListHelper"
 
# Limpiar duplicados y symlinks basura
rm -rf "$NODES_DIR/ComfyUI-Frame-Interpolation-link" 2>/dev/null || true
rm -rf "$NODES_DIR/comfyui-easy-use-bak" 2>/dev/null || true
rm -rf "$NODES_DIR/ComfyUI_essentials_link" 2>/dev/null || true
 
# ── PASO 6 — Modelos ──────────────────────────────────────────────────────────
step "PASO 6/8 — Modelos ($([ "$USE_R2" = true ] && echo 'R2 ⚡' || echo 'HuggingFace 📥'))"
mkdir -p "$MODELS_DIR"/{checkpoints,diffusion_models,text_encoders,vae,loras,latent_upscale_models,audio_separator,lim,rife}
 
dl() {
    local r2="$1" hf_repo="$2" hf_file="$3" dest="$4"
    local fname; fname=$(basename "$dest")
    [ -f "$dest" ] && [ "$(stat -c%s "$dest" 2>/dev/null || echo 0)" -gt 1048576 ] && { ok "Existe: $fname"; return 0; }
    mkdir -p "$(dirname "$dest")"
    if [ "$USE_R2" = true ] && [ -n "$r2" ]; then
        rclone copy "r2:$R2_BUCKET/models/$r2" "$(dirname "$dest")" --transfers 4 --buffer-size 256M --quiet 2>/dev/null
        [ -f "$dest" ] && [ "$(stat -c%s "$dest" 2>/dev/null || echo 0)" -gt 1048576 ] && { ok "R2: $fname"; return 0; }
        warn "R2 falló $fname — HF..."
    fi
    [ -n "$hf_repo" ] && \
        wget -q --show-progress --header="Authorization: Bearer $HF_TOKEN" --continue \
        -O "${dest}.tmp" "https://huggingface.co/$hf_repo/resolve/main/$hf_file" 2>/dev/null \
        && mv "${dest}.tmp" "$dest" && ok "HF: $fname" \
        || { err "Falló: $fname"; rm -f "${dest}.tmp" 2>/dev/null; }
}
 
# Diffusion models
dl "diffusion_models/LTX-2.3-22B-distilled-1.1-Q4_K_M.gguf" "city96/LTX-Video-gguf" "LTX-2.3-22B-distilled-1.1-Q4_K_M.gguf" "$MODELS_DIR/diffusion_models/LTX-2.3-22B-distilled-1.1-Q4_K_M.gguf"
dl "diffusion_models/LTX-2.3-22B-distilled-1.1-Q6_K.gguf" "city96/LTX-Video-gguf" "LTX-2.3-22B-distilled-1.1-Q6_K.gguf" "$MODELS_DIR/diffusion_models/LTX-2.3-22B-distilled-1.1-Q6_K.gguf"
dl "diffusion_models/ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors" "Kijai/LTX2.3_comfy" "diffusion_models/ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors" "$MODELS_DIR/diffusion_models/ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors"
dl "diffusion_models/MelBandRoformer_fp16.safetensors" "Kijai/MelBandRoFormer_comfy" "MelBandRoformer_fp16.safetensors" "$MODELS_DIR/diffusion_models/MelBandRoformer_fp16.safetensors"
dl "diffusion_models/ltx2310eros_v1.safetensors" "" "" "$MODELS_DIR/diffusion_models/ltx2310eros_v1.safetensors"
# Text encoders
dl "text_encoders/ltx-2.3_text_projection_bf16.safetensors" "Kijai/LTX2.3_comfy" "text_encoders/ltx-2.3_text_projection_bf16.safetensors" "$MODELS_DIR/text_encoders/ltx-2.3_text_projection_bf16.safetensors"
dl "text_encoders/gemma_3_12B_it_fp4_mixed.safetensors" "Comfy-Org/ltx-2" "split_files/text_encoders/gemma_3_12B_it_fp4_mixed.safetensors" "$MODELS_DIR/text_encoders/gemma_3_12B_it_fp4_mixed.safetensors"
dl "text_encoders/gemma_3_12B_it_fp8_scaled.safetensors" "Comfy-Org/ltx-2" "split_files/text_encoders/gemma_3_12B_it_fp8_scaled.safetensors" "$MODELS_DIR/text_encoders/gemma_3_12B_it_fp8_scaled.safetensors"
dl "text_encoders/tokenizer.model" "Kijai/LTX2.3_comfy" "text_encoders/tokenizer.model" "$MODELS_DIR/text_encoders/tokenizer.model"
# VAEs
dl "vae/LTX23_audio_vae_bf16.safetensors" "Kijai/LTX2.3_comfy" "vae/LTX23_audio_vae_bf16.safetensors" "$MODELS_DIR/vae/LTX23_audio_vae_bf16.safetensors"
dl "vae/LTX23_video_vae_bf16.safetensors" "Kijai/LTX2.3_comfy" "vae/LTX23_video_vae_bf16.safetensors" "$MODELS_DIR/vae/LTX23_video_vae_bf16.safetensors"
dl "vae/taeltx2_3.safetensors" "Kijai/LTX2.3_comfy" "vae/taeltx2_3.safetensors" "$MODELS_DIR/vae/taeltx2_3.safetensors"
# Upscalers
dl "latent_upscale_models/ltx-2.3-spatial-upscaler-x1.5-1.0.safetensors" "Lightricks/LTX-2.3" "ltx-2.3-spatial-upscaler-x1.5-1.0.safetensors" "$MODELS_DIR/latent_upscale_models/ltx-2.3-spatial-upscaler-x1.5-1.0.safetensors"
dl "latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.1.safetensors" "Lightricks/LTX-2.3" "ltx-2.3-spatial-upscaler-x2-1.1.safetensors" "$MODELS_DIR/latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.1.safetensors"
# LoRAs
dl "loras/ltx-2.3-id-lora-talkvid-3k.safetensors" "Comfy-Org/ltx-2.3" "split_files/loras/ltx-2.3-id-lora-talkvid-3k.safetensors" "$MODELS_DIR/loras/ltx-2.3-id-lora-talkvid-3k.safetensors"
dl "loras/ltx-2.3-id-lora-celebvhq-3k.safetensors" "Comfy-Org/ltx-2.3" "split_files/loras/ltx-2.3-id-lora-celebvhq-3k.safetensors" "$MODELS_DIR/loras/ltx-2.3-id-lora-celebvhq-3k.safetensors"
dl "loras/ltx-2.3-22b-distilled-lora-384-1.1.safetensors" "Lightricks/LTX-2.3" "ltx-2.3-22b-distilled-lora-384-1.1.safetensors" "$MODELS_DIR/loras/ltx-2.3-22b-distilled-lora-384-1.1.safetensors"
dl "loras/ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors" "Lightricks/LTX-2.3-22b-IC-LoRA-Union-Control" "ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors" "$MODELS_DIR/loras/ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors"
dl "loras/ltx-2-19b-ic-lora-detailer.safetensors" "Lightricks/LTX-2-19b-IC-LoRA-Detailer" "ltx-2-19b-ic-lora-detailer.safetensors" "$MODELS_DIR/loras/ltx-2-19b-ic-lora-detailer.safetensors"
for lora in "AmateurHour_01_rank16.safetensors" "LTX2.3_Crisp_Enhance.safetensors" "LTX2.3_Luxe_Sensual.safetensors" "LTX2.3_Post_Apocalyptic.safetensors" "LTX2.3_Soft_Enhance.safetensors" "LTX2.3_Wild_West.safetensors" "LTX23-GalaxyAce.safetensors" "LTX23_Enhancers_CrispSoft.safetensors"; do
    dl "loras/$lora" "" "" "$MODELS_DIR/loras/$lora"
done
# Nombres exactos que buscan los workflows
cp "$MODELS_DIR/loras/ltx-2.3-id-lora-celebvhq-3k.safetensors" "$MODELS_DIR/loras/LTX-2_3-ID-LoRA-CelebVHQ-3K.safetensors" 2>/dev/null || true
cp "$MODELS_DIR/loras/ltx-2.3-id-lora-celebvhq-3k.safetensors" "$MODELS_DIR/loras/LTX-2.3-ID-LoRA-Celeb.safetensors" 2>/dev/null || true
# RIFE — desde HF
dl "" "Kijai/RIFE_sf" "rife49.pt" "$MODELS_DIR/rife/rife49.pt"
dl "" "Kijai/RIFE_sf" "rife47.pt" "$MODELS_DIR/rife/rife47.pt"
 
# ── PASO 7 — Workflows ────────────────────────────────────────────────────────
step "PASO 7/8 — Workflows"
mkdir -p "$WORKFLOWS_DIR"
[ -d "$REPO_DIR/workflows" ] && cp "$REPO_DIR"/workflows/*.json "$WORKFLOWS_DIR/" 2>/dev/null && ok "Workflows copiados" || warn "Sin workflows en repo"
 
# ── PASO 8 — Arranque ─────────────────────────────────────────────────────────
step "PASO 8/8 — Arranque ComfyUI"
POD_ID="${RUNPOD_POD_ID:-POD_ID}"
[ "$PLATFORM" = "RunPod" ] && \
    ACCESS_URL="https://${POD_ID}-8188.proxy.runpod.net" || \
    ACCESS_URL="http://$(curl -s ifconfig.me 2>/dev/null || echo 'TU_IP'):8188"
 
cat > "$BASE_DIR/start_comfyui.sh" << BOOT
#!/bin/bash
pkill -f 'python.*main.py' 2>/dev/null || true; sleep 2
cd $COMFY_DIR && nohup python main.py --listen 0.0.0.0 --port 8188 > $BASE_DIR/comfyui.log 2>&1 &
echo "ComfyUI arrancando — Acceso: $ACCESS_URL"
sleep 20 && tail -5 $BASE_DIR/comfyui.log
BOOT
chmod +x "$BASE_DIR/start_comfyui.sh"
bash "$BASE_DIR/start_comfyui.sh"
 
END_TOTAL=$(date +%s)
ELAPSED=$(( (END_TOTAL - START_TOTAL) / 60 ))
TOTAL_MODELS=$(find "$MODELS_DIR" -type f \( -name "*.safetensors" -o -name "*.gguf" -o -name "*.pt" \) 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "$MODELS_DIR" 2>/dev/null | cut -f1)
 
echo ""
echo -e "${G}╔══════════════════════════════════════════════════════╗${N}"
echo -e "${G}║   ✅ LISTO en ${ELAPSED} minutos                     ║${N}"
echo -e "${G}╠══════════════════════════════════════════════════════╣${N}"
echo -e "${G}║${N}   Plataforma : $PLATFORM"
echo -e "${G}║${N}   Modelos    : $TOTAL_MODELS archivos · $TOTAL_SIZE"
echo -e "${G}║${N}   Acceso     : $ACCESS_URL"
echo -e "${G}║${N}   Reiniciar  : bash $BASE_DIR/start_comfyui.sh"
echo -e "${G}╚══════════════════════════════════════════════════════╝${N}"
