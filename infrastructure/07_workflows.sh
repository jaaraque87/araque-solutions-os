#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  07_workflows.sh — Instalar todos los workflows + patches JSON             ║
# ║  Qué hace: LTXREALISM · MVC V5.1 (3wf) · TODOENUNO · patches automáticos  ║
# ║  Tiempo:   <2 min                                                           ║
# ║                                                                             ║
# ║  ARCHIVOS QUE DEBES SUBIR AL POD (junto a los scripts):                    ║
# ║    LTXREALISM.json         → workflow base LTXREALISM v3                   ║
# ║    LTX2.3TODOENUNO.json    → workflow all-in-one (el más completo)         ║
# ║                                                                             ║
# ║  Los workflows MVC V5.1 se descargan automáticamente desde GitHub          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
source "$(dirname "$0")/00_config.sh"
set -euo pipefail

echo -e "${W}"
echo "  ╔════════════════════════════════════════════╗"
echo "  ║  07 — Workflows + JSON Patches  v2.3      ║"
echo "  ╚════════════════════════════════════════════╝"
echo -e "${N}"

step "PASO 5 — Instalando workflows"
mkdir -p "$WORKFLOWS_DIR"

# ══════════════════════════════════════════════════════════════════════════════
# LTXREALISM.json — workflow base (subido manualmente)
# ══════════════════════════════════════════════════════════════════════════════
LTXREALISM_SRC=""
for loc in \
    "/workspace/LTXREALISM.json" \
    "/root/LTXREALISM.json" \
    "$(dirname "$0")/LTXREALISM.json" \
    "/tmp/LTXREALISM.json"; do
    if [ -f "$loc" ]; then LTXREALISM_SRC="$loc"; break; fi
done

if [ -n "$LTXREALISM_SRC" ]; then
    cp "$LTXREALISM_SRC" "$WORKFLOWS_DIR/VideoFlow_LTX23_AllInOne_v3.json"
    log "Copiado: VideoFlow_LTX23_AllInOne_v3.json"

    # Patch: bypass nodos UNETLoader vacíos (fix "null model" TypeError)
    info "Parchando nodos UNETLoader vacíos en LTXREALISM..."
    python3 - << 'PYEOF'
import json
wf_path = "/workspace/ComfyUI/user/default/workflows/VideoFlow_LTX23_AllInOne_v3.json"
try:
    with open(wf_path) as f:
        wf = json.load(f)
    nodes = wf if isinstance(wf, list) else wf.get("nodes", [])
    patched = 0
    for node in nodes:
        if node.get("type") in ("UNETLoader", "UnetLoaderGGUF"):
            node["mode"] = 4   # 4 = Bypass en ComfyUI
            patched += 1
    with open(wf_path, 'w') as f:
        json.dump(wf, f, indent=2)
    print(f"[✓] {patched} nodo(s) UNETLoader bypasseados" if patched else "[→] Sin nodos UNETLoader que parchear")
except Exception as e:
    print(f"[⚠] Patch LTXREALISM: {e}")
PYEOF
else
    warn "LTXREALISM.json no encontrado — sube el archivo a /workspace/"
    warn "  scp LTXREALISM.json root@{pod-ip}:/workspace/"
fi

# ══════════════════════════════════════════════════════════════════════════════
# LTX2.3TODOENUNO.json — workflow all-in-one (subido manualmente)
# ══════════════════════════════════════════════════════════════════════════════
TODOENUNO_SRC=""
for loc in \
    "/workspace/LTX2.3TODOENUNO.json" \
    "/root/LTX2.3TODOENUNO.json" \
    "$(dirname "$0")/LTX2.3TODOENUNO.json" \
    "/tmp/LTX2.3TODOENUNO.json"; do
    if [ -f "$loc" ]; then TODOENUNO_SRC="$loc"; break; fi
done

if [ -n "$TODOENUNO_SRC" ]; then
    cp "$TODOENUNO_SRC" "$WORKFLOWS_DIR/LTX2.3TODOENUNO.json"
    log "Copiado: LTX2.3TODOENUNO.json"

    # Patch 1: Q4_0 → Q4_K_M (Q4_0 no existe públicamente)
    # Patch 2: Bypass UNETLoader vacíos
    info "Parchando TODOENUNO (Q4_0→Q4_K_M + bypass nulos)..."
    python3 - << 'PYEOF'
import json
wf_path = "/workspace/ComfyUI/user/default/workflows/LTX2.3TODOENUNO.json"
try:
    with open(wf_path) as f:
        wf = json.load(f)
    nodes = wf if isinstance(wf, list) else wf.get("nodes", [])
    q4_patched = 0
    bypass_patched = 0
    for node in nodes:
        # Sustituir Q4_0 por Q4_K_M en todos los campos de texto
        widgets = node.get("widgets_values", [])
        for i, v in enumerate(widgets):
            if isinstance(v, str) and "Q4_0" in v:
                widgets[i] = v.replace("Q4_0", "Q4_K_M")
                q4_patched += 1
        # Bypass UNETLoader vacíos
        inputs = node.get("inputs", [])
        for inp in inputs:
            if inp.get("name") == "unet_name" and inp.get("widget", {}).get("value") is None:
                node["mode"] = 4
                bypass_patched += 1
    with open(wf_path, 'w') as f:
        json.dump(wf, f, indent=2)
    print(f"[✓] Q4_0→Q4_K_M: {q4_patched} ref(s) | bypass nulos: {bypass_patched}")
except Exception as e:
    print(f"[⚠] Patch TODOENUNO: {e}")
PYEOF
else
    warn "LTX2.3TODOENUNO.json no encontrado — sube el archivo a /workspace/"
    warn "  Está en: C:\\Users\\SOPORTE2\\Downloads\\LTX2.3TODOENUNO.json"
    warn "  scp LTX2.3TODOENUNO.json root@{pod-ip}:/workspace/"
fi

# ══════════════════════════════════════════════════════════════════════════════
# Music Video Creator V5.1 — 3 workflows (descarga automática desde GitHub)
# ══════════════════════════════════════════════════════════════════════════════
set +e
info "Descargando Music Video Creator V5.1 (3 workflows)..."
MVC_BASE="https://raw.githubusercontent.com/vrgamegirl19/comfyui-vrgamedevgirl/main/Workflows/LTX-2_Workflows/LTX%202.3%20Music%20Video%20Creator%20V5.1"

for wf_file in \
    "LTX2.3_Music_Video_Creator_Prompt_Creator_V5.json" \
    "LTX2.3_Music_Video_Creator_T2V_V5.1.json" \
    "LTX2.3_Music_Video_Creator_I2V_V5.1.json"; do

    dest_file="$WORKFLOWS_DIR/$wf_file"
    if [ -f "$dest_file" ]; then
        log "Ya existe: $wf_file"
    else
        wget -q --show-progress -O "$dest_file" "$MVC_BASE/$wf_file" \
            && log "OK: $wf_file" \
            || { err "FALLÓ: $wf_file"; rm -f "$dest_file"; }
    fi
done
set -e

# ── Verificación ──────────────────────────────────────────────────────────────
echo ""
echo -e "${W}  WORKFLOWS:${N}"
echo "  ──────────────────────────────────────────────"
for wf in \
    "VideoFlow_LTX23_AllInOne_v3.json" \
    "LTX2.3_Music_Video_Creator_Prompt_Creator_V5.json" \
    "LTX2.3_Music_Video_Creator_T2V_V5.1.json" \
    "LTX2.3_Music_Video_Creator_I2V_V5.1.json" \
    "LTX2.3TODOENUNO.json"; do
    if [ -f "$WORKFLOWS_DIR/$wf" ]; then
        echo -e "  ${G}[✓]${N} $wf"
    else
        echo -e "  ${R}[✗]${N} $wf — FALTA (subir manualmente)"
    fi
done

echo ""
log "07_workflows.sh COMPLETADO"
