# ComfyDeploy + HyperFrames portable pipeline

This folder is the portable video assembly layer.

Goal: run the same pipeline from any computer, RunPod, VPS, Codex session, or Claude Code session by cloning the repo and providing secrets through environment variables.

## What it does

1. Reads a campaign brief from JSON.
2. Sends a normalized payload to ComfyDeploy.
3. Stores the returned assets in a run folder.
4. Builds a HyperFrames composition around those assets.
5. Renders the final MP4 with `npx hyperframes render`.

If ComfyDeploy is not configured yet, it can run in `--mock-assets` mode so Codex/Claude can still generate the HyperFrames project structure and test the pipeline shape.

## MVP one-click: una imagen a preview sin créditos

El entrypoint seguro toma una imagen local, la asocia con un corpus ya investigado
en `tools/hook-lab/clients`, selecciona los tres hooks con mejor score, escribe un
brief y un scorecard automáticos, y construye un proyecto HyperFrames alrededor de
la imagen. No hace llamadas de red, no enciende GPU y no renderiza MP4:

```powershell
python .\one_click.py ..\..\brand\araque\araque-profile.jpg
```

Si la ruta de la imagen no permite inferir el cliente, declara el corpus:

```powershell
python .\one_click.py C:\assets\producto.png --client araque-solutions
```

La salida incluye `hooks.scored.json`, `brief.auto.json`, `manifest.json` y el
proyecto `hyperframes/`. Desde esa carpeta se revisa sin créditos:

```powershell
npx hyperframes check
npx hyperframes preview
```

La corrida real está cerrada por defecto. Para habilitarla hacen falta a la vez
`--execute-real`, la confirmación `--confirm-cost SPEND_COMFYDEPLOY_CREDITS`,
`ARAQUE_ALLOW_GPU_EXECUTION=1`, los secretos `COMFYDEPLOY_*` y una URL pública de
la imagen con `--source-image-url`. No habilites esos gates durante desarrollo.

## Requirements

- Git
- Python 3.10+
- Node.js 22+
- HyperFrames via `npx hyperframes`
- A local `.env` file or environment secrets

Do not commit `.env`.

## Environment

Copy the example:

```powershell
Copy-Item ..\.env.example ..\.env
```

Required for real ComfyDeploy calls:

```text
COMFYDEPLOY_API_KEY=
COMFYDEPLOY_DEPLOYMENT_ID=
COMFYDEPLOY_API_BASE=https://api.comfydeploy.com/api
COMFYDEPLOY_RUN_URL=
```

`COMFYDEPLOY_RUN_URL` is intentionally configurable because ComfyDeploy workspaces can expose different API paths. If it is empty, the runner uses:

```text
{COMFYDEPLOY_API_BASE}/deployments/{COMFYDEPLOY_DEPLOYMENT_ID}/runs
```

## Quick test without spending credits

```powershell
python .\run.py --brief .\examples\brief.example.json --mock-assets --skip-render
```

## Real run

```powershell
$env:ARAQUE_ALLOW_GPU_EXECUTION="1"
python .\run.py --brief .\examples\brief.example.json --execute-real --confirm-cost SPEND_COMFYDEPLOY_CREDITS
```

## Continue from another PC

```powershell
git clone https://github.com/jaaraque87/araque-solutions-os.git
cd araque-solutions-os\pipeline\comfydeploy_hyperframes
Copy-Item ..\.env.example ..\.env
# Fill local secrets, then:
python .\run.py --brief .\examples\brief.example.json --mock-assets --skip-render
```

## Output

Every run is written to:

```text
pipeline/comfydeploy_hyperframes/runs/<run_id>/
```

The folder contains:

- `manifest.json`: run metadata and asset list
- `comfydeploy_payload.json`: payload sent to ComfyDeploy
- `hyperframes/index.html`: generated composition
- `hyperframes/package.json`: local Node package metadata
- `hyperframes/assets/`: assets copied or downloaded for the composition
- `hyperframes/output.mp4`: final render when rendering is enabled
