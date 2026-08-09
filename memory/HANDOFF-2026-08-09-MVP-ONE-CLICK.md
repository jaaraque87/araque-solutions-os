# Handoff — MVP one-click seguro — 2026-08-09

## Qué cambió

- Nuevo `pipeline/comfydeploy_hyperframes/one_click.py`:
  - recibe una imagen local;
  - descubre o recibe un corpus `tools/hook-lab/clients/*/hooks.json`;
  - selecciona tres hooks por score existente, sin inventar research;
  - genera `hooks.scored.json`, `brief.auto.json`, scorecard, payload y manifest;
  - construye un preview HyperFrames offline alrededor de la imagen.
- La composición generada dejó GSAP/CDN y usa WAAPI finito, pausado y seek-safe.
- `run.py` y `one_click.py` bloquean ejecución real salvo que coincidan:
  `--execute-real`, `--confirm-cost SPEND_COMFYDEPLOY_CREDITS` y
  `ARAQUE_ALLOW_GPU_EXECUTION=1`.
- One-click real exige además `--source-image-url` accesible por ComfyDeploy.

## Qué se probó

- `python -m unittest -v test_one_click.py`: 3/3 OK.
- Smoke con `brand/araque/araque-profile.jpg`: seleccionó h03=10, h01=9, h02=9.
- HyperFrames 0.7.103 `check --json`: OK; 0 errores/warnings en lint,
  runtime, layout y contraste.
- Snapshots locales a 2s, 6s, 10s y 11.64s revisados visualmente.
- Todas las pruebas se ejecutaron con Chrome en modo software, sin render MP4,
  sin ComfyDeploy y sin GPU.

## Qué queda

- Con aprobación de gasto, conectar una URL real de imagen al nombre exacto del
  input del deployment LTX mediante `--image-input-key` y ejecutar un piloto.
- Añadir UI de upload/selección de cliente sobre este contrato CLI.
- El Python del sistema de esta PC falla por una sesión de inicio inválida; las
  pruebas usaron el runtime Python empaquetado de Codex.

## Entorno

- Windows, repo `araque-solutions-os`, rama `main`.
- Node v24.18.0.
- No se tocaron los directorios no rastreados preexistentes.
