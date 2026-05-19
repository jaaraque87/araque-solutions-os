#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  01_sistema_comfyui.sh — Sistema + ComfyUI + Patches                       ║
# ║  Qué hace: apt deps · ComfyUI · PyTorch CUDA · Jupyter proxy · Patches     ║
# ║  Tiempo:   ~5 min                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
source "$(dirname "$0")/00_config.sh"
set -euo pipefail

echo -e "${W}"
echo "  ╔════════════════════════════════════════════╗"
echo "  ║  01 — Sistema + ComfyUI + Patches  v2.3   ║"
echo "  ╚════════════════════════════════════════════╝"
echo -e "${N}"

# ══════════════════════════════════════════════════════════════════════════════
# PASO 0 — Dependencias del sistema
# ══════════════════════════════════════════════════════════════════════════════
step "PASO 0 — Dependencias del sistema"

apt-get update -qq 2>/dev/null || true
apt-get install -y -qq git wget curl 2>/dev/null \
    && log "git/wget/curl OK" \
    || { err "No se pudo instalar git/wget/curl"; exit 1; }

apt-get install -y -qq aria2    2>/dev/null || warn "aria2 no disponible"
apt-get install -y -qq ffmpeg   2>/dev/null || warn "ffmpeg no disponible"
apt-get install -y -qq libgl1 libglib2.0-0 2>/dev/null || warn "libgl1 no disponible"

pip install -q huggingface_hub 2>/dev/null && log "huggingface_hub OK"

# ══════════════════════════════════════════════════════════════════════════════
# PASO 1A — Instalar / verificar ComfyUI
# ══════════════════════════════════════════════════════════════════════════════
step "PASO 1A — ComfyUI"
mkdir -p "$COMFY_DIR" "$MODELS_DIR" "$NODES_DIR" "$WORKFLOWS_DIR"

if [ ! -d "$COMFY_DIR/.git" ]; then
    info "Clonando ComfyUI..."
    git clone --depth=1 https://github.com/comfyanonymous/ComfyUI.git "$COMFY_DIR" \
        && log "ComfyUI clonado" \
        || { err "No se pudo clonar ComfyUI"; exit 1; }
    pip install -q -r "$COMFY_DIR/requirements.txt" \
        && log "Requirements ComfyUI OK" \
        || { err "Error en requirements"; exit 1; }
else
    log "ComfyUI encontrado — actualizando..."
    cd "$COMFY_DIR"
    git pull origin master --quiet 2>/dev/null \
        || git pull origin main --quiet 2>/dev/null \
        || warn "No se pudo actualizar — usando versión actual"
    pip install -q -r requirements.txt || warn "Algunos requirements fallaron"
    cd /workspace
fi

# ══════════════════════════════════════════════════════════════════════════════
# PASO 1B — FIX: model_patcher.py (Linear lazy — LTX 2.3 Audio VAE)
# ══════════════════════════════════════════════════════════════════════════════
# Causa: audio VAE tiene text_embedding_projection como Linear inicialización
# lazy → no tiene .weight cuando ModelPatcher intenta estimar memoria → crash.
# Fix: try/except alrededor de check_module_offload_mem(".weight")
step "PASO 1B — Patch model_patcher.py (fix Audio VAE crash)"

python3 - << 'PYEOF'
path = "/workspace/ComfyUI/comfy/model_patcher.py"
try:
    with open(path, 'r') as f:
        content = f.read()
    old = '                module_offload_mem += check_module_offload_mem("{}.weight".format(n))'
    new = ('                try:\n'
           '                    module_offload_mem += check_module_offload_mem("{}.weight".format(n))\n'
           '                except (AttributeError, Exception):\n'
           '                    pass  # LTX2.3 lazy Linear fix v2.1')
    if old in content:
        with open(path, 'w') as f:
            f.write(content.replace(old, new))
        print("[✓] Patch aplicado: model_patcher.py")
    else:
        print("[→] model_patcher.py ya parchado o versión diferente — sin cambios")
except Exception as e:
    print(f"[⚠] No se pudo parchear model_patcher.py: {e}")
PYEOF

# ══════════════════════════════════════════════════════════════════════════════
# PASO 1C — Verificar PyTorch CUDA
# ══════════════════════════════════════════════════════════════════════════════
step "PASO 1C — PyTorch / CUDA"

CUDA_OK=$(python3 -c "import torch; print('ok' if torch.cuda.is_available() else 'fail')" 2>/dev/null || echo "fail")

if [ "$CUDA_OK" = "fail" ]; then
    warn "PyTorch/CUDA incompatible — reinstalando con cu121..."
    pip install -q torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cu121 \
        --force-reinstall \
        && log "PyTorch cu121 instalado" \
        || { err "No se pudo reinstalar PyTorch"; exit 1; }
    CUDA_OK=$(python3 -c "import torch; print('ok' if torch.cuda.is_available() else 'fail')" 2>/dev/null || echo "fail")
fi

if [ "$CUDA_OK" = "ok" ]; then
    GPU=$(python3 -c "import torch; print(torch.cuda.get_device_name(0))" 2>/dev/null || echo "?")
    VRAM=$(python3 -c "import torch; print(f'{torch.cuda.get_device_properties(0).total_memory/1024**3:.1f}GB')" 2>/dev/null || echo "?")
    log "CUDA OK — GPU: $GPU ($VRAM)"
else
    warn "CUDA no disponible — ComfyUI usará CPU (muy lento)"
fi

# ══════════════════════════════════════════════════════════════════════════════
# PASO 1D — Jupyter Server Proxy (acceso browser en RunPod)
# ══════════════════════════════════════════════════════════════════════════════
step "PASO 1D — Jupyter proxy"
pip install -q jupyter-server-proxy && log "jupyter-server-proxy OK"

# ── Espacio libre ─────────────────────────────────────────────────────────────
FREE_GB=$(df -BG /workspace | tail -1 | awk '{print $4}' | tr -d 'G')
if [ "${FREE_GB:-0}" -lt 200 ]; then
    warn "Espacio libre: ${FREE_GB}GB — se recomiendan 200+ GB para todos los modelos"
else
    log "Espacio libre: ${FREE_GB}GB — OK"
fi

echo ""
log "01_sistema_comfyui.sh COMPLETADO"
