# LTX Avatar Original Audio Template

HyperFrames template for LTX/ComfyUI avatar videos where the original audio should be preserved for lipsync credibility.

Source flow:

```text
local LTX MP4 -> normalize 30fps/keyframes -> HyperFrames overlays -> final 9:16 MP4
```

Run from the repo root:

```powershell
node .\tools\content-reel-lab\scripts\render-ltx-avatar-original-audio.mjs `
  --video "C:\ruta\a\avatar-ltx.mp4" `
  --hook "Rostro real. Audio real. Venta real." `
  --cta "Vender mas, vendas lo que vendas." `
  --handle "@araquesolutions"
```

Do not commit generated project folders or MP4 outputs. They are created under `tools/content-reel-lab/outputs/` and ignored by Git.
