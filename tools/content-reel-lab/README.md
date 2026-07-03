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
