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
