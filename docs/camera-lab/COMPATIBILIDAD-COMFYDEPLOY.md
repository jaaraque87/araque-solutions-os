# Camera Lab × ComfyDeploy ARAQUE — matriz de compatibilidad y plan (2026-07-07)

Camera Lab instalado LOCAL en `C:\Users\SOPORTE2\Documents\Camera-lab` (deps ✓, .env creado).
Arquitectura objetivo: **UI local (o en la futura plataforma) → COMFYUI_URL = túnel de sesión
ComfyDeploy (L40S)** → GPU en la nube. `tunnel_url` se obtiene de `GET /api/sessions` del dashboard.

## Matriz (auditoría de nodos de workflows/app/*.json vs máquina v27)

| Módulo | Nodos | Modelos | Estado |
|---|---|---|---|
| LTX Director V2 (`ltx_director_2.json`) | core + WhatDreamsCost ✓ (¡la máquina ya trae hasta el fix CropGuides!) | LTX ✓ volumen | **LISTO** |
| Camera Control (Dolly/Orbit/Roll, I2V/FLF/FML) | core+LTX ✓ | ✓ | **LISTO** |
| Subtitle cleaner extend+crop (`ltx23_*_subtitle_cleaner_nag_extend.json`) | core ✓ (con NAG OFF; nodo `LTX2_NAG` de Shidanyan aún sin fuente — opcional, el método ganador es extend+crop) | ✓ | **LISTO** |
| Bernini (13 modos wan22_bernini_*) | `BerniniConditioning` = CORE 0.23 ✓; GGUF loaders = pack ComfyUI-BerniniR (agregado en v27) | ❌ `neuregex/Bernini-R-GGUF` par high/low Q4_K_M (~19 GB) + `city96/umt5-xxl-encoder-gguf` Q5_K_M + `wan_2.1_vae.safetensors` | Fase 2: subir modelos al volumen |
| WAN VACE Inpaint (face swap con máscara + SAM3) | `SAM3_Detect` + `WanVaceToVideo` = CORE ✓ | ❌ modelo WAN VACE + SAM3 checkpoint | Fase 2 |
| SCAIL2 / Motion 3D | `WanSCAILToVideo` = CORE ✓ | ❌ `wan2.1_14B_SCAIL_2_fp8_scaled.safetensors` + CLIP Vision H (sin GGUF público — honesto del autor) | Fase 3 |
| Casting (voces) | app local: LLM_URL (LM Studio :1234) + CosyVoice vendor | n/a | Fase 2 local |

## Cambios aplicados a la máquina
- v27 (`0aa0d5bb`): + `TTPlanetPig/Comfyui_TTP_Toolset` (requisito base Camera Lab) + `neuregex/ComfyUI-BerniniR` (loaders GGUF Bernini, para fase 2).

## Prueba manual Fase 1 (pendiente de sesión)
1. Esperar v27 ready → iniciar sesión ComfyDeploy (cualquier workflow de la máquina LTX, L40S).
2. Obtener `tunnel_url` de la sesión (GET /api/sessions?machine_id=385499ef-...).
3. En `Camera-lab/.env`: `COMFYUI_URL=<tunnel_url>` (dejar COMFYUI_ROOT placeholder).
4. `py scripts/start_camera_lab.py` → abrir UI local → pestaña Director → storyboard 2x2 de prueba (sintaxis `2.0s <prompt>` por línea) → Queue Run.
5. Validar: cola visible, clips S1..SN, preview, trimming, retake.

## Integración a la plataforma ARAQUE (diseño)
- Patrón del autor (cita 07:25 video 1): un workflow JSON dedicado por modo, parcheado por API — igual que hará nuestra app.
- La plataforma puede: (a) embeber Camera Lab tal cual (server Python detrás de un proxy, COMFYUI_URL dinámico creado vía API de sesiones ComfyDeploy), o (b) canibalizar `server/camera_lab_server.py` (las funciones de parcheo de workflows son reutilizables).
- Videos del canal documentados en `docs/taoofai/` + `docs/camera-lab/video-01-*.md`.
