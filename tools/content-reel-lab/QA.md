# QA - Araque Instagram Conversion Pilot

Date: 2026-07-03

## Reel

Source:

- `tools/content-reel-lab/reel/index.html`

Rendered artifact, ignored by Git:

- `tools/content-reel-lab/reel/final.mp4`

Checks run:

```powershell
node hyperframes/dist/cli.js lint .
node hyperframes/dist/cli.js validate .
node hyperframes/dist/cli.js inspect . --samples 12
node hyperframes/dist/cli.js render . --output final.mp4 --quality standard
ffprobe final.mp4
```

Result:

- Lint: 0 errors, 1 non-blocking warning for dense transition track.
- Validate: no console errors.
- Inspect: 0 layout issues across 12 samples.
- Render: 1080x1920, 30 fps, 30.000 seconds, MP4.

## Carousel

Source:

- `tools/content-reel-lab/carousel/carousel.html`
- `tools/content-reel-lab/carousel/render-carousel.mjs`

Rendered artifacts, ignored by Git:

- `tools/content-reel-lab/outputs/carousel/slide-01.jpg` through `slide-06.jpg`

Result:

- 6 JPG slides rendered at 1080x1350.
- Contact sheet reviewed at `tools/content-reel-lab/outputs/qa/contact-sheet.jpg`.

## LTX Avatar Original Audio Template

Source:

- `tools/content-reel-lab/templates/ltx-avatar-original-audio/index.template.html`
- `tools/content-reel-lab/scripts/render-ltx-avatar-original-audio.mjs`

Local test input:

- `C:\Users\SOPORTE2\Downloads\LTX2_3_00002-audio (1).mp4`

Smoke command:

```powershell
node tools/content-reel-lab/scripts/render-ltx-avatar-original-audio.mjs --video "C:\Users\SOPORTE2\Downloads\LTX2_3_00002-audio (1).mp4" --name portable-smoke --skip-render
```

Smoke result:

- LTX video normalized to 30 fps with keyframes every 30 frames.
- HyperFrames lint: 0 errors, 0 warnings.
- HyperFrames validate: no console errors.
- HyperFrames inspect: 0 layout issues across 12 samples.

Full render command:

```powershell
node tools/content-reel-lab/scripts/render-ltx-avatar-original-audio.mjs --video "C:\Users\SOPORTE2\Downloads\LTX2_3_00002-audio (1).mp4" --name portable-render --out "tools/content-reel-lab/outputs/ltx-avatar-original-audio-portable-test.mp4"
```

Full render result:

- Final MP4 rendered successfully.
- Output: `tools/content-reel-lab/outputs/ltx-avatar-original-audio-portable-test.mp4`
- Render metadata: 1080x1920, 30 fps, 18.9 seconds, audio preserved.
