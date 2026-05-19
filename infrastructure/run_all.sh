#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  run_all.sh — Instalador maestro ARAQUE SOLUTIONS v2.3                     ║
# ║  Ejecuta todos los scripts en orden                                        ║
# ║                                                                             ║
# ║  USO:                                                                       ║
# ║    bash run_all.sh              → instalación completa (~200 GB)            ║
# ║    bash run_all.sh --base       → solo base (scripts 01-03)                ║
# ║    bash run_all.sh --skip-tod   → todo excepto TODOENUNO (más rápido)      ║
# ║    bash run_all.sh --from 04    → desde script 04 en adelante              ║
# ║                                                                             ║
# ║  ARCHIVOS A SUBIR AL POD JUNTO A ESTA CARPETA:                             ║
# ║    LTXREALISM.json                                                          ║
# ║    LTX2.3TODOENUNO.json                                                     ║
# ║                                                                             ║
# ║  ESPACIO TOTAL: ~200 GB (recomendado: 300 GB de disco)                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/00_config.sh"

# Tiempo de inicio
START=$(date +%s)

# ── Parsear argumentos ────────────────────────────────────────────────────────
MODE="full"
FROM_SCRIPT=0
for arg in "$@"; do
    case "$arg" in
        --base)     MODE="base" ;;
        --skip-tod) MODE="skip_tod" ;;
        --from)     shift; FROM_SCRIPT="${1:-0}" ;;
        --from=*)   FROM_SCRIPT="${arg#--from=}" ;;
    esac
done

echo -e "${W}"
echo "  ╔══════════════════════════════════════════════════════╗"
echo "  ║  ARAQUE SOLUTIONS — LTX 2.3 Instalador v2.3        ║"
echo "  ║  LTXREALISM + Music Video Creator + TODOENUNO       ║"
echo "  ╚══════════════════════════════════════════════════════╝"
echo -e "${N}"

case "$MODE" in
    base)     echo -e "  Modo: ${C}BASE${N} (solo scripts 01-03)" ;;
    skip_tod) echo -e "  Modo: ${C}SIN TODOENUNO${N} (scripts 01-04, 06-08)" ;;
    *)        echo -e "  Modo: ${C}COMPLETO${N} (~200 GB total)" ;;
esac

FREE_GB=$(df -BG /workspace | tail -1 | awk '{print $4}' | tr -d 'G')
echo -e "  Espacio libre: ${Y}${FREE_GB}GB${N}"
[ "${FREE_GB:-0}" -lt 100 ] && warn "Se recomiendan 200+ GB"
echo ""

# ── Función para ejecutar un script ───────────────────────────────────────────
run_script() {
    local num="$1" name="$2" file="$SCRIPT_DIR/$2"

    [ "$num" -lt "$FROM_SCRIPT" ] && { info "Omitiendo $name (--from $FROM_SCRIPT)"; return; }

    echo ""
    echo -e "${C}════════════════════════════════════════${N}"
    echo -e "${W}  Ejecutando: $name${N}"
    echo -e "${C}════════════════════════════════════════${N}"

    if bash "$file"; then
        log "$name — COMPLETADO"
    else
        err "$name — FALLÓ (código: $?)"
        echo ""
        echo -e "${Y}¿Continuar con el siguiente script? (s/n) [s]${N}"
        read -t 15 -r cont 2>/dev/null || cont="s"
        cont="${cont:-s}"
        [[ "$cont" =~ ^[nN]$ ]] && { err "Instalación abortada por el usuario"; exit 1; }
    fi
}

# ── Ejecutar según modo ───────────────────────────────────────────────────────
run_script 1  "01_sistema_comfyui.sh"

run_script 2  "02_nodos_custom.sh"

run_script 3  "03_modelos_base.sh"

if [ "$MODE" != "base" ]; then
    run_script 4  "04_modelos_mvc.sh"
fi

if [ "$MODE" = "full" ]; then
    run_script 5  "05_modelos_todoenuno.sh"
fi

if [ "$MODE" != "base" ]; then
    run_script 6  "06_loras.sh"
    run_script 7  "07_workflows.sh"
    run_script 8  "08_arranque.sh"
fi

# ── Verificación final ────────────────────────────────────────────────────────
echo ""
echo -e "${C}════════════════════════════════════════${N}"
echo -e "${W}  Verificación final${N}"
echo -e "${C}════════════════════════════════════════${N}"
bash "$SCRIPT_DIR/09_verificacion.sh"

# ── Tiempo total ──────────────────────────────────────────────────────────────
END=$(date +%s)
ELAPSED=$(( (END - START) / 60 ))
echo ""
echo -e "${G}  ✓ Instalación completada en ${ELAPSED} minutos${N}"
echo -e "${G}  ✓ ARAQUE SOLUTIONS — Kenza UGC Pipeline listo${N}"
echo ""
