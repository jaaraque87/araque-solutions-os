# SETUP — Dejar el sistema operativo en cualquier máquina

Clonar y andar. Para tu PC, la de casa, un VPS, RunPod, o un cliente white-label.

## 1. Prerrequisitos (instalar una vez por máquina)
| Herramienta | Mínimo | Para qué |
|---|---|---|
| Git | cualquiera | clonar el repo |
| Node.js | **22+** | HyperFrames (render local) + runners `tools/` |
| Python | **3.10+** | pipeline `comfydeploy_hyperframes` |
| FFmpeg | reciente | audio, grade, captions, montaje |
| Google Chrome | reciente | render headless de HyperFrames / Puppeteer |

Verificar:
```bash
git --version && node --version && python --version && ffmpeg -version | head -1
```
Node debe decir v22 o superior. Si HyperFrames falla por Node, actualizar a 22+.

## 2. Clonar
```bash
git clone https://github.com/jaaraque87/araque-solutions-os.git
cd araque-solutions-os
```

## 3. Secretos (nunca se suben — viven local)
```bash
cp pipeline/.env.example pipeline/.env     # pon tus claves reales
cp tools/fal-jobs/.env.example tools/fal-jobs/.env
```
Si lanzas algo y falta una clave, los scripts **te la piden en la terminal** (entrada oculta) y ofrecen guardarla en `.env` local — nunca la imprimen ni la commitean. Claves que usa el sistema: `FAL_KEY`, `COMFYDEPLOY_API_KEY`/`_DEPLOYMENT_ID`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ELEVENLABS_API_KEY`, `KIE_API_KEY`, `SUBMAGIC_API_KEY`. (Detalle en `pipeline/.env.example`.)

## 4. Instalar dependencias
```bash
# runners Node (fal.ai)
cd tools/fal-jobs && npm install && cd ../..
# render de tarjetas/carruseles (Puppeteer)
cd tools/carrusel-ana-lab && npm install && cd ../..
```
HyperFrames no se instala: se usa vía `npx hyperframes` (baja solo).

## 5. Prueba sin gastar (mock) — confirma que todo está montado
```bash
cd pipeline/comfydeploy_hyperframes
python run.py --brief examples/brief.example.json --mock-assets --skip-render
```
Debe decir `Run created: ...`. Eso valida la forma del pipeline sin tocar APIs.

Render local de HyperFrames (también $0, prueba el motor de video):
```bash
# desde cualquier proyecto con index.html + hyperframes.json
npx hyperframes lint && npx hyperframes render
```

## 6. Corrida real (gasta créditos)
```bash
# con COMFYDEPLOY_API_KEY + COMFYDEPLOY_DEPLOYMENT_ID en pipeline/.env
cd pipeline/comfydeploy_hyperframes
python run.py --brief examples/brief.example.json
```
Para los clips de fal (física/wow), usar los runners de `tools/fal-jobs/` (UNA generación a la vez):
```bash
cd tools/fal-jobs
node seedance_naia.mjs start.png end.png out.mp4      # o DRY_RUN=1 para validar sin gastar
```

## 6b. Producción constante de reels (probado 2026-07-04, Windows)

Un video LTX con audio → reel con marca (unitario):
```bash
node ./tools/content-reel-lab/scripts/render-ltx-avatar-original-audio.mjs --video "clip.mp4" --hook "..." --cta "..." --handle "@araquesolutions"
```
Lote completo (N videos → N reels, ~1.5 min c/u):
```bash
node ./tools/content-reel-lab/scripts/render-batch.mjs --jobs "tools/content-reel-lab/briefs/batch.example.json"
```
Notas Windows (el batch las aplica solo; para el unitario exportarlas):
- Node 24 bloquea `npx.cmd` desde spawn → instalar hyperframes local (`cd tools/content-reel-lab && npm install hyperframes`) y definir `HYPERFRAMES_CLI=<repo>/tools/content-reel-lab/node_modules/hyperframes/dist/cli.js`.
- Symlinks bloqueados sin modo desarrollador → `HYPERFRAMES_EXTRACT_CACHE_DIR=off`.

Los hooks de cada lote salen de la skill `.claude/skills/hook-lab` (research de nicho + batería puntuada por cliente → `tools/hook-lab/clients/<cliente>/hooks.json`). Guion y retención: `.claude/skills/guion-ugc` + `.claude/skills/script-framework`. Voz oficial (Naia Cruz): `brand/araque/voice/VOICE.md` + `characters/naia-cruz/`.

## 7. Arquitectura de producción (qué corre dónde)
- **Generar** → ComfyDeploy/LTX (talking-heads, volumen, $0 por pieza) · fal.ai solo para física/wow imposible en LTX.
- **Componer visual** → HyperFrames (local, $0).
- **Audio + grade + captions + cierre de marca** → FFmpeg (local, $0). Look "Warm Clean" y reglas en `brand/araque/BRAND.md`.
- **Prompts probados** → `docs/recetas/recetas-video-ugc.md`.

## 8. Reglas de oro
- Nunca commitear `.env`, secretos, modelos, renders, videos, `node_modules`, `.venv`.
- `git pull` al empezar; commits chicos; `git status` antes de push.
- Lo pesado (assets, modelos, renders) vive en Drive/S3/RunPod, no en git.
