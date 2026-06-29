# tools/fal-jobs

Runners Node (`@fal-ai/client`) para generar clips en fal.ai. Cada script sube imagen(es), lanza UNA generación y descarga el MP4. Todos leen `process.env.FAL_KEY` y soportan `DRY_RUN=1` (no gasta, solo imprime el payload).

## Setup
```bash
cd tools/fal-jobs
npm install            # instala @fal-ai/client
cp .env.example .env   # pon tu FAL_KEY (NO se commitea)
export FAL_KEY=...     # o expórtala en el shell
```

## Scripts
| Script | Modelo / uso |
|---|---|
| `klingjob.mjs` | Kling v3 pro image-to-video (genérico) |
| `medardo_kling.mjs` / `grilled_kling.mjs` / `blacklava_kling.mjs` / `propiedad_kling.mjs` | Kling i2v con prompts por-cliente (ejemplos de comida/inmobiliaria) |
| `seedance_naia.mjs` | Seedance 2.0 image-to-video (start+end frame, audio nativo). **Ojo: este endpoint NO tiene `negative_prompt`** → negativos como cláusula "Avoid:" dentro del prompt |
| `avatar_naia.mjs` | Kling AI Avatar v2 Pro (imagen + audio → talking, lip-sync). Duración = largo del audio |
| `captions.ass` | Plantilla de subtítulos estilo CapCut (libass) |

## Uso
```bash
node seedance_naia.mjs start.png end.png out.mp4
DRY_RUN=1 node avatar_naia.mjs naia.png voz.mp3   # valida sin gastar
```

## Reglas
- **Una generación a la vez** (control de gasto). Nunca endpoints `/fast`.
- Kling i2v: prompts de cámara solamente (push-in/dron frontal). NUNCA órbita 360 ni morph de comida (deforma).
- Seedance se reserva para física/wow imposible en LTX; el volumen va por ComfyDeploy/LTX.
