# Handoff — Inventario PC (Downloads) → araque-solutions-os

**Fecha:** 2026-06-29 · **Máquina:** PC Windows del usuario (`C:\Users\usuar\Downloads`) · **Agente:** Claude Code

## 1. Qué encontré

### Repo (ya clonado, bien estructurado)
`infrastructure/` (scripts RunPod), `pipeline/` (Python, módulos en desarrollo + `comfydeploy_hyperframes/` portable), `workflows/` (LTX JSONs), `characters/kenza/`, `memory/`, `docs/`. `.gitignore` sólido (ya ignora secretos, modelos, *.mp4/png/wav, outputs, node_modules, .venv). `.env.example` y `secrets.example.sh` ya cubren TODAS las variables.

### Fábrica local (`C:\Users\usuar\Downloads\fabrica`)
**Tooling REUTILIZABLE (candidato a integrar):**
- `carrusel-ana-lab/` → Node+Puppeteer: `render-card.js`, `render-overlay.js`, `generar-fotos.mjs` (carruseles 1080×1350 + tarjetas/overlays). Limpio (usa `process.env.FAL_KEY`).
- `fal-jobs/` → runners Node: `klingjob.mjs`, `seedance_naia.mjs`, `avatar_naia.mjs`, `medardo_kling.mjs`, `grilled_kling.mjs`, `blacklava_kling.mjs`, `propiedad_kling.mjs` + `captions.ass`. Todos leen `process.env.FAL_KEY` + soportan `DRY_RUN=1`.
- `araque-brand/` → kit de marca: logos (`araque-mark.png`, `araque-lockup-transp.png`, `endcard.jpg/html`), plantillas overlay (`t1/t2/t3.html`, `endcard.html`), fonts. Look "Warm Clean" + captions CapCut (ver `reference_seedance_ugc_clon`).
- `onepager/` → one-pager de venta + fonts.

**OUTPUTS / trabajo de cliente (NO integrar):**
- `alma-*-reel/`, `araque-reel/`, `grilled-bicampeon-reel/`, `medardo-reel/`, `volcano-reel/`, `real-estate-reel/` → cada uno con `assets/ frames/ renders/` + mp4/png generados. Son entregables/outputs pesados → quedan locales o en Drive.
- `hyperframes/` → CLON del monorepo externo de HeyGen (tiene su propio `.git`, node_modules, releases). NO subir; se usa vía `npx hyperframes`.

## 2. Escaneo de secretos — RESULTADO: LIMPIO ✅
- **No hay archivos `.env`** en la fábrica.
- **Ningún secreto hardcodeado** en mi código (grep del valor real FAL_KEY = 0 resultados). Todos los scripts usan `process.env`.
- Los matches de `sk-`/`AIza`/`API_KEY` fueron **falsos positivos**: dentro de `hyperframes/` (código/docs del repo externo) y `package-lock.json` (hashes). No son secretos del usuario.
- ⚠️ **ACCIÓN: rotar la `FAL_KEY`** — se compartió en texto plano en chat durante el desarrollo (aunque NO quedó en ningún archivo).

## 3. Qué claves necesita el pipeline (todas ya en `.env.example`)
`FAL_KEY` (Kling/Seedance/GPT Image 2 vía fal — lo que más uso), `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ELEVENLABS_API_KEY`+`ELEVENLABS_VOICE_ID`, `KIE_API_KEY` (Suno), `COMFYDEPLOY_API_KEY`/`_DEPLOYMENT_ID`/`_RUN_URL`, `SUBMAGIC_API_KEY`, `SUPABASE_URL`/`_KEY` (rama NORA). Node tooling (`carrusel-ana-lab`, `fal-jobs`) solo necesita `FAL_KEY` (+ `PUPPETEER_EXECUTABLE_PATH` para Puppeteer/Chrome local).

## 4. Plan de integración propuesto (PENDIENTE de OK del usuario)
Copiar SOLO código/plantillas reusables al repo, en carpetas limpias:
- `tools/carrusel-ana-lab/` → scripts .js/.mjs + `package.json` + 1 `inputs.example.json` + README. (sin `node_modules`, sin `brands/` con data real).
- `tools/fal-jobs/` → los `.mjs` + `captions.ass` + `package.json` + README + `.env.example` (FAL_KEY=). Parametrizar prompts por-cliente en `examples/` (los actuales tienen prompts hardcodeados de Medardo/Grilled/etc — OK como ejemplos).
- `brand/araque/` → logos + plantillas `endcard.html`/`t1-3.html` + fonts + `BRAND.md` (paleta, look Warm Clean, reglas de captions/marca de agua).
- `docs/recetas/` → prompts probados (Seedance física, Kling i2v, realismo kit iPhone, template LTX v4, params de color grade, reglas de caption CapCut).

**NO subir:** renders/frames/assets, *.mp4/png/wav, clon `hyperframes/`, node_modules, .venv, los proyectos-reel de cliente.

## 5. Sistema de "missing secrets" (PROPUESTO, sin tocar producción)
Agregar helper NUEVO (no cambia comportamiento actual, mantiene compatibilidad con `.env`):
- Python: `pipeline/scripts/lib/secrets.py` con `get_secret(name, label, save=False)` → usa `os.getenv`, si falta pide con `getpass` (entrada oculta), pregunta "¿Guardar en .env local? [s/N]", nunca imprime la clave completa, nunca commitea.
- Node: `tools/lib/get-secret.mjs` equivalente (readline sin eco).
Cablear a los scripts SOLO tras aprobación; primero correr el mock `--mock-assets --skip-render`.

## 6. Estado
- ✅ Repo clonado, docs leídas, inventario hecho, secret scan limpio.
- ⏳ PENDIENTE OK del usuario para: (a) copiar los 3 toolkits + docs, (b) implementar helper de secrets, (c) commit + push.
- ⚠️ Bloqueos: ninguno técnico. Solo falta decisión humana sobre qué integrar. Rotar FAL_KEY.
