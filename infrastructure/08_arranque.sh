#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  08_arranque.sh — Genera start_comfyui.sh y arranca ComfyUI                ║
# ║  Qué hace: crea /workspace/start_comfyui.sh y lo ejecuta                  ║
# ║  Tiempo:   <1 min                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
source "$(dirname "$0")/00_config.sh"
set -euo pipefail

echo -e "${W}"
echo "  ╔════════════════════════════════════════════╗"
echo "  ║  08 — Generar + Arrancar ComfyUI  v2.3    ║"
echo "  ╚════════════════════════════════════════════╝"
echo -e "${N}"

step "PASO 6 — Script de arranque"

# Genera /workspace/start_comfyui.sh
cat > /workspace/start_comfyui.sh << 'STARTSCRIPT'
#!/bin/bash
# ── start_comfyui.sh — Arrancar ComfyUI + Jupyter Proxy ──────────────────────
# Acceso: https://{POD_ID}-8888.proxy.runpod.net/proxy/8188/
#
# POD_ID = el ID numérico de tu pod en RunPod (aparece en la URL del pod)

export PIP_ROOT_USER_ACTION=ignore

pkill -f 'python.*main.py' 2>/dev/null || true
pkill -f jupyter            2>/dev/null || true
sleep 2

# Jupyter Lab (proxy para acceso externo)
nohup jupyter lab \
    --ip=0.0.0.0 --port=8888 --no-browser --allow-root \
    --ServerApp.token='' --ServerApp.password='' \
    --ServerApp.allow_origin='*' \
    > /workspace/jupyter.log 2>&1 &

# ComfyUI en puerto 8188
cd /workspace/ComfyUI
nohup python main.py --listen 0.0.0.0 --port 8188 \
    > /workspace/comfyui.log 2>&1 &

echo ""
echo "══════════════════════════════════════════════════════"
echo "  ComfyUI iniciando..."
echo ""
echo "  Accede desde tu browser:"
echo "  → https://{POD_ID}-8888.proxy.runpod.net/proxy/8188/"
echo ""
echo "  Reemplaza {POD_ID} con el ID de tu pod RunPod"
echo "══════════════════════════════════════════════════════"
echo ""
echo "Esperando 15s para que ComfyUI cargue..."
sleep 15
echo ""
echo "═══ Últimas líneas de log ComfyUI ═══"
tail -10 /workspace/comfyui.log
STARTSCRIPT

chmod +x /workspace/start_comfyui.sh
log "Script de arranque creado: /workspace/start_comfyui.sh"

# ── Preguntar si arrancar ahora ───────────────────────────────────────────────
echo ""
echo -e "${Y}¿Arrancar ComfyUI ahora? (s/n)${N}"
read -t 10 -r respuesta 2>/dev/null || respuesta="s"
respuesta="${respuesta:-s}"

if [[ "$respuesta" =~ ^[sS]$ ]]; then
    log "Arrancando ComfyUI..."
    bash /workspace/start_comfyui.sh
else
    info "Para arrancar más tarde:"
    echo -e "  ${C}bash /workspace/start_comfyui.sh${N}"
fi

echo ""
log "08_arranque.sh COMPLETADO"
