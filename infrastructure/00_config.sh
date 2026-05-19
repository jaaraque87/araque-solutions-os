#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  00_config.sh — Configuración compartida + helpers                         ║
# ║  Todos los demás scripts hacen:  source "$(dirname "$0")/00_config.sh"     ║
# ║                                                                             ║
# ║  TOKENS: copia secrets.example.sh → secrets.sh y pon tus keys              ║
# ║          secrets.sh está en .gitignore — NUNCA se sube a GitHub            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

export GIT_TERMINAL_PROMPT=0
export PIP_ROOT_USER_ACTION=ignore

# ── CARGAR SECRETS (si existe secrets.sh en la misma carpeta) ─────────────────
SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
if [ -f "$SCRIPT_DIR/secrets.sh" ]; then
    source "$SCRIPT_DIR/secrets.sh"
fi

# ── TOKENS (desde env vars — NO hardcodear aquí) ──────────────────────────────
HF_TOKEN="${HF_TOKEN:-}"
CIVITAI_TOKEN="${CIVITAI_TOKEN:-}"

# Validar que existan
if [ -z "$HF_TOKEN" ]; then
    echo -e "\033[0;31m[✗]\033[0m HF_TOKEN no definido."
    echo "    Copia secrets.example.sh → secrets.sh y completa tus tokens."
    echo "    O ejecuta: export HF_TOKEN=hf_xxxxxxxxxxxx"
    exit 1
fi

# ── RUTAS ─────────────────────────────────────────────────────────────────────
COMFY_DIR="/workspace/ComfyUI"
MODELS_DIR="$COMFY_DIR/models"
NODES_DIR="$COMFY_DIR/custom_nodes"
WORKFLOWS_DIR="$COMFY_DIR/user/default/workflows"

# ── COLORES ───────────────────────────────────────────────────────────────────
R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'
B='\033[0;34m'; C='\033[0;36m'; W='\033[1;37m'; N='\033[0m'

log()  { echo -e "${G}[✓]${N} $*"; }
warn() { echo -e "${Y}[⚠]${N} $*"; }
err()  { echo -e "${R}[✗]${N} $*"; }
step() { echo -e "\n${C}━━━━ $* ━━━━${N}"; }
info() { echo -e "${B}[→]${N} $*"; }

# ── HELPER: descargar desde HuggingFace ───────────────────────────────────────
hf_dl() {
    local repo="$1" filepath="$2" dest_dir="$3"
    local dest_name="${4:-$(basename "$filepath")}"
    local full_dest="$MODELS_DIR/$dest_dir/$dest_name"
    mkdir -p "$MODELS_DIR/$dest_dir"
    if [ -f "$full_dest" ]; then log "Ya existe: $dest_name"; return 0; fi
    info "Descargando: $dest_name"
    wget -q --show-progress \
         --header="Authorization: Bearer $HF_TOKEN" \
         --continue -O "${full_dest}.tmp" \
         "https://huggingface.co/${repo}/resolve/main/${filepath}" \
    && mv "${full_dest}.tmp" "$full_dest" && log "OK: $dest_name" \
    || { err "FALLÓ: $dest_name"; rm -f "${full_dest}.tmp"; return 1; }
}

# ── HELPER: descargar desde CivitAI ──────────────────────────────────────────
civitai_dl() {
    local version_id="$1" dest_dir="$2" dest_name="$3"
    local full_dest="$MODELS_DIR/$dest_dir/$dest_name"
    mkdir -p "$MODELS_DIR/$dest_dir"
    if [ -f "$full_dest" ]; then log "Ya existe: $dest_name"; return 0; fi
    [ -z "$CIVITAI_TOKEN" ] && { warn "Sin CIVITAI_TOKEN — omitiendo: $dest_name"; return 0; }
    info "Descargando CivitAI: $dest_name"
    wget -q --show-progress --continue \
         -O "${full_dest}.tmp" \
         "https://civitai.com/api/download/models/${version_id}?token=${CIVITAI_TOKEN}" \
    && mv "${full_dest}.tmp" "$full_dest" && log "OK: $dest_name" \
    || { err "FALLÓ: $dest_name"; rm -f "${full_dest}.tmp"; return 1; }
}

# ── HELPER: clonar o actualizar nodo custom ───────────────────────────────────
install_node() {
    local name="$1" url="$2"
    local node_dir="$NODES_DIR/$name"
    if [ -d "$node_dir" ]; then
        info "Actualizando: $name"
        cd "$node_dir" && git pull --quiet origin HEAD 2>/dev/null || true
        cd /workspace
    else
        info "Instalando: $name"
        git clone --depth=1 --quiet "$url" "$node_dir" \
            && log "Clonado: $name" || { err "FALLÓ clonar: $name"; return 1; }
    fi
    [ -f "$node_dir/requirements.txt" ] && \
        pip install -q -r "$node_dir/requirements.txt" || true
    [ -f "$node_dir/install.py" ] && \
        cd "$node_dir" && python install.py 2>/dev/null || true
    cd /workspace 2>/dev/null || true
}

# ── HELPER: verificar modelo ──────────────────────────────────────────────────
check_model() {
    local path="$MODELS_DIR/$1" name="$2"
    if [ -f "$path" ]; then
        echo -e "  ${G}[✓]${N} $name ($(du -sh "$path" 2>/dev/null | cut -f1))"
    else
        echo -e "  ${R}[✗]${N} $name — FALTA"
    fi
}
