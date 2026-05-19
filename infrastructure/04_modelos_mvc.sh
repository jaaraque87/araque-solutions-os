#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  04_modelos_mvc.sh — Music Video Creator models (~70 GB)                   ║
# ║  Qué hace: Z-Image Turbo · LLaMA 3B · SuperGemma 26B · LTX Q6_K ·        ║
# ║            Qwen 3 4B · FLUX VAE · Vocoder · Upscaler                       ║
# ║  Tiempo:   30-60 min                                                        ║
# ║  Espacio:  ~70 GB                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
source "$(dirname "$0")/00_config.sh"
set +e

echo -e "${W}"
echo "  ╔════════════════════════════════════════════════╗"
echo "  ║  04 — Music Video Creator Models (~70 GB) v2.3║"
echo "  ╚════════════════════════════════════════════════╝"
echo -e "${N}"

step "PASO 3.5 + 3.6 — Modelos Music Video Creator"
warn "~70 GB — puede tomar 30-60 min"

mkdir -p "$MODELS_DIR/checkpoints"
mkdir -p "$MODELS_DIR/diffusion_models"
mkdir -p "$MODELS_DIR/text_encoders"
mkdir -p "$MODELS_DIR/vae"
mkdir -p "$MODELS_DIR/latent_upscale_models"
mkdir -p "$MODELS_DIR/llm"

# ── Z-Image Turbo (~5 GB) — genera frame de referencia para I2V ──────────────
# Tongyi-MAI/Z-Image-Turbo — usado por VRGDG en I2V workflow
info "[1/8] Z-Image Turbo (genera frames I2V reference)"
python3 - << 'PYEOF'
import os, shutil
from huggingface_hub import list_repo_files, hf_hub_download

token = os.environ.get("HF_TOKEN", "")
dest_dir = "/workspace/ComfyUI/models/checkpoints"
os.makedirs(dest_dir, exist_ok=True)

dest = os.path.join(dest_dir, "z_image_turbo_bf16.safetensors")
if os.path.exists(dest):
    print(f"[✓] Ya existe: z_image_turbo_bf16.safetensors")
else:
    candidates = [
        ("Tongyi-MAI/Z-Image-Turbo",           None),
        ("dimitribarbot/Z-Image-Turbo-BF16",   "transformer/diffusion_pytorch_model.safetensors"),
    ]
    for repo, hint_file in candidates:
        try:
            files = [f for f in list_repo_files(repo, token=token or None)
                     if f.endswith(".safetensors") and "onnx" not in f.lower()]
            target = hint_file if hint_file else (files[0] if files else None)
            if not target:
                print(f"[⚠] Sin safetensors en {repo}")
                continue
            print(f"[→] Descargando desde {repo}/{target}...")
            src = hf_hub_download(repo_id=repo, filename=target, token=token or None)
            shutil.copy2(src, dest)
            print(f"[✓] Z-Image Turbo OK")
            break
        except Exception as e:
            print(f"[⚠] {repo}: {e}")
    else:
        print("[✗] Z-Image Turbo no descargado — descarga manual:")
        print("    https://huggingface.co/dimitribarbot/Z-Image-Turbo-BF16")
PYEOF

# ── Qwen 3 4B safetensors (~3 GB) — CLIP para Z-Image Turbo ──────────────────
info "[2/8] Qwen 3 4B safetensors (CLIP de Z-Image Turbo)"
python3 - << 'PYEOF'
import os, shutil
from huggingface_hub import list_repo_files, hf_hub_download

token = os.environ.get("HF_TOKEN", "")
dest_dir = "/workspace/ComfyUI/models/text_encoders"
os.makedirs(dest_dir, exist_ok=True)
dest = os.path.join(dest_dir, "qwen_3_4b.safetensors")

if os.path.exists(dest):
    print("[✓] Ya existe: qwen_3_4b.safetensors")
else:
    candidates = ["Comfy-Org/Qwen3-4B-Instruct", "Comfy-Org/Qwen3-4B", "Qwen/Qwen3-4B"]
    for repo in candidates:
        try:
            files = [f for f in list_repo_files(repo, token=token or None)
                     if f.endswith(".safetensors")]
            if not files:
                continue
            src = hf_hub_download(repo_id=repo, filename=files[0], token=token or None)
            shutil.copy2(src, dest)
            print(f"[✓] Qwen 3 4B OK desde {repo}")
            break
        except Exception as e:
            print(f"[⚠] {repo}: {e}")
    else:
        print("[✗] Qwen 3 4B no descargado")
PYEOF

# ── LLaMA 3.2 3B GGUF Q4_K_M (~2 GB) — prompts locales ──────────────────────
info "[3/8] LLaMA 3.2 3B Instruct Q4_K_M (~2 GB)"
python3 - << 'PYEOF'
import os, shutil
from huggingface_hub import hf_hub_download

token = os.environ.get("HF_TOKEN", "")
dest_dir = "/workspace/ComfyUI/models/llm"
os.makedirs(dest_dir, exist_ok=True)
dest = os.path.join(dest_dir, "Llama-3.2-3B-Instruct-Q4_K_M.gguf")

if os.path.exists(dest):
    print("[✓] Ya existe: Llama-3.2-3B-Instruct-Q4_K_M.gguf")
else:
    try:
        src = hf_hub_download(
            repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",
            filename="Llama-3.2-3B-Instruct-Q4_K_M.gguf",
            token=token or None
        )
        shutil.copy2(src, dest)
        print("[✓] LLaMA 3.2 3B OK")
    except Exception as e:
        print(f"[✗] LLaMA falló: {e}")
PYEOF

# ── SuperGemma 4 26B Q4_K_M (16.8 GB) — LLM principal vrgamedevgirl ─────────
info "[4/8] SuperGemma 4 26B Q4_K_M (16.8 GB) — puede tardar 20 min"
if [ ! -f "$MODELS_DIR/llm/supergemma4-26b-uncensored-fast-v2-Q4_K_M.gguf" ]; then
    wget -q --show-progress --continue \
        -O "$MODELS_DIR/llm/supergemma4-26b-uncensored-fast-v2-Q4_K_M.gguf" \
        "https://huggingface.co/juan1995-dev/supergemma4-26b-uncensored-fast-v2-Q4_K_M_GGUF/resolve/main/supergemma4-26b-uncensored-fast-v2-Q4_K_M.gguf" \
        && log "OK: SuperGemma 4 26B" \
        || warn "SuperGemma falló"
else
    log "Ya existe: SuperGemma 4 26B"
fi

# ── LTX 2.3 22B Distilled Q6_K (21 GB) — GGUF de calidad alta ───────────────
info "[5/8] LTX 2.3 22B Distilled Q6_K (21 GB)"
if [ ! -f "$MODELS_DIR/diffusion_models/LTX-2.3-22B-distilled-1.1-Q6_K.gguf" ]; then
    wget -q --show-progress \
        --header="Authorization: Bearer $HF_TOKEN" --continue \
        -O "$MODELS_DIR/diffusion_models/LTX-2.3-22B-distilled-1.1-Q6_K.gguf" \
        "https://huggingface.co/Abiray/LTX-2.3-22B-DISTILLED-1.1-GGUF/resolve/main/LTX-2.3-22B-distilled-1.1-Q6_K.gguf" \
        && log "OK: LTX distilled Q6_K" \
        || warn "LTX Q6_K falló"
else
    log "Ya existe: LTX-2.3-22B-distilled-1.1-Q6_K.gguf"
fi

# ── FLUX VAE ae.safetensors (335 MB) — subgraph Z-Image Turbo ────────────────
info "[6/8] FLUX VAE ae.safetensors (335 MB)"
hf_dl "black-forest-labs/FLUX.1-schnell" \
      "ae.safetensors" \
      "vae" \
    || warn "FLUX VAE falló"

# ── LTX-AV Vocoder 24K (~500 MB) — generación de audio en video ──────────────
info "[7/8] LTX-AV Vocoder 24K"
hf_dl "Kijai/LTX2.3_comfy" \
      "ltx-av-step-1751000_vocoder_24K.safetensors" \
      "vae" \
    || warn "Vocoder falló"

# ── Upscaler x2 v1.1 — requerido por workflows nuevos ────────────────────────
info "[8/8] Upscaler x2 v1.1 (si no está instalado ya)"
hf_dl "Lightricks/LTX-2.3" \
      "ltx-2.3-spatial-upscaler-x2-1.1.safetensors" \
      "latent_upscale_models" \
    || warn "Upscaler x2 v1.1 falló"

# ── Verificación ──────────────────────────────────────────────────────────────
echo ""
echo -e "${W}  MUSIC VIDEO CREATOR:${N}"
echo "  ──────────────────────────────────────────────"
check_model "checkpoints/z_image_turbo_bf16.safetensors"                    "Z-Image Turbo bf16"
check_model "text_encoders/qwen_3_4b.safetensors"                           "Qwen 3 4B CLIP"
check_model "llm/Llama-3.2-3B-Instruct-Q4_K_M.gguf"                        "LLaMA 3.2 3B Q4_K_M"
check_model "llm/supergemma4-26b-uncensored-fast-v2-Q4_K_M.gguf"           "SuperGemma 4 26B (16.8 GB)"
check_model "diffusion_models/LTX-2.3-22B-distilled-1.1-Q6_K.gguf"        "LTX 22B distilled Q6_K (21 GB)"
check_model "vae/ae.safetensors"                                             "FLUX VAE ae.safetensors"
check_model "vae/ltx-av-step-1751000_vocoder_24K.safetensors"               "LTX-AV Vocoder 24K"
check_model "latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.1.safetensors" "Upscaler x2 v1.1"

echo ""
log "04_modelos_mvc.sh COMPLETADO"
