# Builder Orchestrator

Automatiza el V9 Video Builder sobre el tunnel de una sesion ComfyDeploy.

## 1. Montar un kit

```powershell
py .\tools\builder-orchestrator\montar_proyecto.py `
  --tunnel https://TU-TUNNEL `
  --kit "C:\ruta\CAMILA-PROD001-KIT" `
  --name CAMILA_PROD001_AUTO
```

El montaje fuerza los invariantes de produccion: modo Speaking/I2V, 1080x1920,
24 fps y seed 69 en modo fixed.

## 2. Validar sin GPU

```powershell
py .\tools\builder-orchestrator\render_headless.py `
  --tunnel https://TU-TUNNEL `
  --project /comfyui/output/CAMILA_PROD001_AUTO `
  --dry-run
```

## 3. Primera prueba humeda: una escena

```powershell
py .\tools\builder-orchestrator\render_headless.py `
  --tunnel https://TU-TUNNEL `
  --project /comfyui/output/CAMILA_PROD001_AUTO `
  --scene 5
```

`--scene` deja el clip recolectado en el proyecto remoto y no ejecuta stitch.
Para el lote completo y su descarga local, omita `--scene`:

```powershell
py .\tools\builder-orchestrator\render_headless.py `
  --tunnel https://TU-TUNNEL `
  --project /comfyui/output/CAMILA_PROD001_AUTO `
  --output .\CAMILA_PROD001_FINAL.mp4
```

El proceso es reanudable: recupera clips existentes con
`scan_scene_videos`, guarda la sesion tras cada escena y solo renderiza los
faltantes. `--force` crea versiones nuevas y respalda el clip anterior.

## Cadena API

`build_i2v_prompt -> /prompt -> /history -> find_scene_video_output ->
collect_scene_video -> stitch_scene_videos -> /view`

El POST a `/prompt` incluye metadata de workflow no nula, necesaria para
evitar los crashes ya diagnosticados en VRGDG_ShowText y VHS_VideoCombine.

No iniciar una L40S ni gastar APIs sin autorizacion del dueno. Descargar el
FINAL antes de cerrar la sesion.
