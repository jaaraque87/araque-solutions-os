# ARAQUE SOLUTIONS OS

**Sistema completo de producción de video UGC con IA — escalable, reproducible, vendible a otras agencias.**

> Costo real: $3.27/video · Setup en pod nuevo: 4 horas · 60 videos/mes por cliente

---

## Estructura del repositorio

```
araque-solutions-os/
│
├── infrastructure/          → Scripts RunPod (instalar ComfyUI + modelos)
│   ├── secrets.example.sh   → Copia → secrets.sh y pon tus tokens
│   ├── 00_config.sh         → Config compartida (no ejecutar directamente)
│   ├── 01_sistema_comfyui.sh
│   ├── 02_nodos_custom.sh
│   ├── 03_modelos_base.sh   → ~55 GB
│   ├── 04_modelos_mvc.sh    → ~70 GB (Music Video Creator)
│   ├── 05_modelos_todoenuno.sh → ~58 GB (workflow avanzado)
│   ├── 06_loras.sh
│   ├── 07_workflows.sh
│   ├── 08_arranque.sh
│   ├── 09_verificacion.sh
│   └── run_all.sh           → Orquestador principal ← EMPEZAR AQUÍ
│
├── pipeline/                → Scripts Python para producción de videos UGC
│   ├── run.py               → Orchestrator CLI
│   ├── setup.py             → Instalador de dependencias
│   ├── .env.example         → Template de API keys Python
│   └── scripts/             → Los 12 módulos del pipeline (en desarrollo)
│       ├── brand_analyzer.py
│       ├── guion.py
│       ├── personaje.py
│       └── ...
│
├── workflows/               → Archivos JSON de ComfyUI
│   ├── LTX2.3TODOENUNO.json ← RECOMENDADO — all-in-one
│   ├── LTXREALISM.json      ← base LTXREALISM v3
│   └── MVC_V5.1/            ← Music Video Creator V5.1
│       ├── LTX2.3_Music_Video_Creator_Prompt_Creator_V5.json
│       ├── LTX2.3_Music_Video_Creator_T2V_V5.1.json
│       └── LTX2.3_Music_Video_Creator_I2V_V5.1.json
│
├── characters/              → Un folder por personaje/influencer
│   └── kenza/
│       └── README.md        ← prompts, LoRAs, outfits, voz
│
├── docs/                    → Documentos del sistema
│   ├── sistema-araque-solutions.html  ← one-pager para agencias
│   └── guia-araque-solutions.html     ← guía completa del operador
│
└── memory/                  → Notas y contexto del proyecto
    ├── MEMORY.md
    ├── project_kenza.md
    ├── project_araque_solutions.md
    └── project_nora.md
```

---

## Inicio rápido — Pod nuevo (cualquier PC del mundo)

```bash
# 1. Clonar el repo
git clone https://github.com/TU_USUARIO/araque-solutions-os.git
cd araque-solutions-os/infrastructure

# 2. Configurar tokens
cp secrets.example.sh secrets.sh
nano secrets.sh   # ← pon tus tokens reales

# 3. Subir al pod RunPod (desde tu PC)
scp -r ../araque-solutions-os/ root@{pod-ip}:/workspace/

# 4. En el pod
cd /workspace/araque-solutions-os/infrastructure
bash run_all.sh

# 5. Abrir ComfyUI
# https://{POD_ID}-8888.proxy.runpod.net/proxy/8188/
```

**Opciones de run_all.sh:**
```bash
bash run_all.sh              # instalación completa (~200 GB, ~4h)
bash run_all.sh --base       # solo lo mínimo para LTXREALISM (~55 GB)
bash run_all.sh --skip-tod   # sin TODOENUNO (~140 GB)
bash run_all.sh --from=05    # retomar desde script 05
```

---

## Pod recomendado (RunPod)

| GPU | VRAM | Uso recomendado | $/hr |
|---|---|---|---|
| RTX A6000 | 48 GB | Mínimo para TODOENUNO | ~$0.70 |
| A100 SXM | 80 GB | Ideal, máxima velocidad | ~$1.90 |
| RTX 4090 | 24 GB | Solo workflows básicos | ~$0.44 |

- **Template:** RunPod Pytorch 2.x.x (NO el de ComfyUI)
- **Disco:** 300 GB mínimo
- **Acceso:** `https://{POD_ID}-8888.proxy.runpod.net/proxy/8188/`

---

## Workflow recomendado para UGC Kenza

**TODOENUNO — modo Lipsync (⭐ ideal para producción)**
1. Abrir ComfyUI → cargar `workflows/LTX2.3TODOENUNO.json`
2. Presionar `9` → leer instrucciones (están en español)
3. Presionar `0` → click "DISABLE EVERYTHING"
4. Presionar `3` → subir `BANANA_PRO_00006_.png` como imagen de referencia
5. Presionar `4` → subir audio TTS generado con Gemini
6. Presionar `2` → duración 8-10s, resolución 576×1024
7. Queue Prompt → ~5-8 min en A6000

---

## Costos de producción

| Componente | Costo | Herramienta |
|---|---|---|
| Guión | $0.01 | Gemini Pro |
| Imagen personaje + escena | $0.82 | GPT Image 2 / fal.ai |
| Video clip | $1.20 | Kling Pro |
| Voz TTS | $0.02 | Gemini Flash TTS |
| Voice change | $0.06 | ElevenLabs STS |
| Lip sync | $0.60 | Sync-3 / fal.ai |
| Música | $0.06 | Suno V4.5 |
| GPU (RunPod) | ~$0.50 | A6000 por video |
| **TOTAL** | **~$3.27** | |

**Modelo de negocio:** $497/mes por cliente (60 videos) → ~$270/mes margen neto

---

## Modelo white label (para otras agencias)

| Tier | Precio | Qué incluye |
|---|---|---|
| Agency Starter Kit | $2,997 one-time | Todo este repo + onboarding 1h |
| Agency OS | $197/mes | Dashboard white label + soporte continuo |
| Done For You | $4,997 + $297/mes | Operación completa, ellos revenden |

---

## Personajes activos

| Personaje | Estado | Ver |
|---|---|---|
| Kenza | ✅ Activo | `characters/kenza/README.md` |
| Personaje 2 | 🔜 Pendiente | — |

---

## Stack tecnológico completo

| Capa | Tecnología |
|---|---|
| Video gen | LTX-Video 2.3 (22B) en ComfyUI |
| Workflow | TODOENUNO.json + MVC V5.1 |
| GPU cloud | RunPod (A6000/A100) |
| Imagen fija | FLUX1 + LoRA custom |
| Guión | Gemini Pro |
| TTS | Gemini Flash TTS + ElevenLabs STS |
| Lip sync | Sync-3 (fal.ai) |
| Música | Suno V4.5 Plus |
| Montaje | FFmpeg local |
| Dashboard | NORA (Next.js + FastAPI) — en desarrollo |
| Storage | Supabase Storage |

---

*ARAQUE SOLUTIONS — AI-Powered UGC Infrastructure · 2026*
