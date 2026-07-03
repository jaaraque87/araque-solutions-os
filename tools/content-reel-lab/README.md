# Content Reel Lab

Pilot production module adapted from the avatar-reel pack for Codex.

This version removes the required avatar provider and keeps the useful production architecture:

```text
source/topic -> brief -> hooks -> script -> visual direction -> HyperFrames reel -> carousel -> QA
```

## Pilot

Brand: Araque Solutions
Source: https://www.instagram.com/araquesolutions/
Objective: sell AI content creation services and position the brand as an authority.
Outputs:

- `reel/final.mp4` from HyperFrames, 30 seconds, 9:16.
- `outputs/carousel/*.jpg`, six 1080x1350 carousel slides.

Generated outputs are intentionally ignored by Git.

## Portable LTX avatar reel

Use this when ComfyUI/LTX 2.3 already generated a vertical avatar video with synced original audio and you want Codex/HyperFrames to add branding, overlays and CTA without replacing the voice.

Requirements on any PC:

- Git.
- Node.js 22 or newer.
- FFmpeg and FFprobe available on PATH. On Windows, `winget install Gyan.FFmpeg` is fine.
- Internet for first `npx hyperframes` install/cache, unless HyperFrames is already cached.

From repo root:

```powershell
git pull
node .\tools\content-reel-lab\scripts\render-ltx-avatar-original-audio.mjs `
  --video "C:\ruta\a\tu-video-ltx.mp4" `
  --hook "Rostro real. Audio real. Venta real." `
  --cta "Vender mas, vendas lo que vendas." `
  --handle "@araquesolutions"
```

The script will:

1. Copy the template into `tools/content-reel-lab/outputs/ltx-avatar-original-audio/`.
2. Normalize the LTX video to 30 fps with safe keyframes for HyperFrames seeking.
3. Keep the original audio for lipsync credibility.
4. Run HyperFrames `lint`, `validate`, `inspect`.
5. Render `final.mp4`.

Fast smoke test without rendering:

```powershell
node .\tools\content-reel-lab\scripts\render-ltx-avatar-original-audio.mjs `
  --video "C:\ruta\a\tu-video-ltx.mp4" `
  --skip-render
```

If a machine has HyperFrames installed in a custom cache, set:

```powershell
$env:HYPERFRAMES_CLI="C:\ruta\a\hyperframes\dist\cli.js"
```

## Run

Use the Node runtime bundled with Codex if the system Node is older than 22.

```powershell
$NODE='C:\Users\SOPORTE2\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
$HF='C:\Users\SOPORTE2\AppData\Local\npm-cache\_npx\702923228c2ce1e6\node_modules\hyperframes\dist\cli.js'

& $NODE $HF lint .\reel
& $NODE $HF validate .\reel
& $NODE $HF inspect .\reel --samples 12
& $NODE $HF render .\reel --output .\reel\final.mp4 --quality standard

$env:NODE_PATH='C:\Users\SOPORTE2\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
& $NODE .\carousel\render-carousel.mjs
```

## Git Rule

Commit only source files, briefs, docs and templates. Do not commit rendered videos, JPG exports, `.env`, caches, `node_modules`, or run outputs.
