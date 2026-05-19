#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  06_loras.sh — LoRAs de estilo, realism y voice ID                         ║
# ║  Qué hace: TalkVid · vrgamedevgirl84 style LoRAs · CivitAI LoRAs           ║
# ║  Tiempo:   10-20 min                                                        ║
# ║  Espacio:  ~15 GB                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
source "$(dirname "$0")/00_config.sh"
set +e

echo -e "${W}"
echo "  ╔════════════════════════════════════════════╗"
echo "  ║  06 — LoRAs Estilo + Voice ID  v2.3       ║"
echo "  ╚════════════════════════════════════════════╝"
echo -e "${N}"

step "PASO 4 — LoRAs"
mkdir -p "$MODELS_DIR/loras"

# ── [1] TalkVid ID-LoRA (1.13 GB) — lip sync + talking head ──────────────────
# Mantiene identidad facial mientras sincroniza labios con el audio.
# Comfy-Org/ltx-2.3/split_files/loras/
info "[1] TalkVid ID-LoRA (1.13 GB) — lip sync"
hf_dl "Comfy-Org/ltx-2.3" \
      "split_files/loras/ltx-2.3-id-lora-talkvid-3k.safetensors" \
      "loras" \
    || warn "TalkVid LoRA falló"

# ── [2-6] LoRAs vrgamedevgirl84 — estilos cinematográficos para Kenza ─────────
# Luxe Sensual ⭐ = beauty/lifestyle — IDEAL para UGC de productos femeninos
# Crisp Enhance ⭐ = realismo cinematográfico + bordes nítidos
# Soft Enhance  = realismo suave con skin glow
# Post Apocalyptic / Wild West = estilos alternativos para variedad de contenido
info "[2-6] LoRAs vrgamedevgirl84 (Soft, Crisp, Luxe, Post-Apoc, Wild West)"
python3 - << 'PYEOF'
import os, shutil
from huggingface_hub import list_repo_files, hf_hub_download

token = os.environ.get("HF_TOKEN", "")
dest = "/workspace/ComfyUI/models/loras"
os.makedirs(dest, exist_ok=True)

repos = {
    "vrgamedevgirl84/LTX_2.3_Soft_Enhance_Style_LoRa":     "LTX2.3_Soft_Enhance.safetensors",
    "vrgamedevgirl84/LTX_2.3_Crisp_Enhance_Style_LoRa":    "LTX2.3_Crisp_Enhance.safetensors",
    "vrgamedevgirl84/LTX_2.3_Luxe_Sensual_Style_LoRa":     "LTX2.3_Luxe_Sensual.safetensors",
    "vrgamedevgirl84/LTX_2.3_Post_Apocalyptic_Style_LoRa": "LTX2.3_Post_Apocalyptic.safetensors",
    "vrgamedevgirl84/LTX_2.3_Wild_West_Style_LoRa":        "LTX2.3_Wild_West.safetensors",
}
for repo, name in repos.items():
    path = os.path.join(dest, name)
    if os.path.exists(path):
        print(f"[✓] Ya existe: {name}")
        continue
    try:
        files = [f for f in list_repo_files(repo, token=token or None)
                 if f.endswith(".safetensors")]
        if not files:
            print(f"[✗] Sin safetensors: {repo}")
            continue
        src = hf_hub_download(repo_id=repo, filename=files[0], token=token or None)
        shutil.copy2(src, path)
        print(f"[✓] OK: {name}")
    except Exception as e:
        print(f"[✗] Error {name}: {e}")
PYEOF

# ── [7] CivitAI — LTX23 Enhancers Crisp+Soft ─────────────────────────────────
# El "pack doble" de CivitAI — incluye ambas variantes de enhance en un archivo
info "[7] CivitAI: LTX23 Enhancers CrispSoft (v2849716)"
civitai_dl "2849716" "loras" "LTX23_Enhancers_CrispSoft.safetensors" \
    || warn "Enhancers CrispSoft falló"

# ── [8] CivitAI — GalaxyAce LoRA (1.88 GB) ───────────────────────────────────
# Mejora la generación general de personajes femeninos — ideal Kenza
info "[8] CivitAI: GalaxyAce LoRA (v2808759)"
civitai_dl "2808759" "loras" "LTX23-GalaxyAce.safetensors" \
    || warn "GalaxyAce falló"

# ── [9] CivitAI — AmateurHour rank16 ─────────────────────────────────────────
# Estilo footage amateur/handheld — muy auténtico para UGC
info "[9] CivitAI: AmateurHour rank16 (v2844417)"
civitai_dl "2844417" "loras" "AmateurHour_01_rank16.safetensors" \
    || warn "AmateurHour falló"

# ── Verificación ──────────────────────────────────────────────────────────────
echo ""
echo -e "${W}  LoRAs:${N}"
echo "  ──────────────────────────────────────────────"
check_model "loras/ltx-2.3-id-lora-talkvid-3k.safetensors"         "TalkVid ID-LoRA (1.13 GB)"
check_model "loras/LTX2.3_Soft_Enhance.safetensors"                "Soft Enhance LoRA"
check_model "loras/LTX2.3_Crisp_Enhance.safetensors"               "Crisp Enhance LoRA ⭐"
check_model "loras/LTX2.3_Luxe_Sensual.safetensors"                "Luxe Sensual LoRA ⭐ (Kenza beauty)"
check_model "loras/LTX2.3_Post_Apocalyptic.safetensors"            "Post Apocalyptic LoRA"
check_model "loras/LTX2.3_Wild_West.safetensors"                   "Wild West LoRA"
check_model "loras/LTX23_Enhancers_CrispSoft.safetensors"          "Enhancers CrispSoft LoRA (CivitAI)"
check_model "loras/LTX23-GalaxyAce.safetensors"                    "GalaxyAce LoRA (1.88 GB)"
check_model "loras/AmateurHour_01_rank16.safetensors"              "AmateurHour LoRA"
# Nota: CelebVHQ y TalkVid también son ID-LoRAs pero están en script 05

echo ""
log "06_loras.sh COMPLETADO"
