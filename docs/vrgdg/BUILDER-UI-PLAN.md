# Plan: probar el Video Builder UI (vrgdg v9) — preparado 2026-07-08

Contexto: video overview analizado en `01-UOsGoqRJPPE-*.md`. Objetivo del usuario: probar el Builder con Nano Banana o GPT Images como motor de imagen "custom", apilado con el LoRA `naiacruz_zimage_v1`.

## Hallazgos del research (rama dev/music-video-builder-ui-test-v9)

1. **La máquina está DESACTUALIZADA para el Builder**: el pack en la máquina v29 está en commit `d6dde1fd` (04-jul). El lanzador del Builder como nodo ComfyUI (`Move node canvas launcher into ComfyUI node`, `ef98208`) y el **template de workflow ID-LoRA para el Builder** (`eeb65c0`) llegaron el **07-jul**. → Hay que actualizar el pack para tener el nodo.
2. **⚠ Lección vigente**: actualizar pack puede desalinear workflows guardados (ver memory/comfydeploy-mvc-vrgdg.md). Tras el update: re-validar que Prompt Creator V5.1 / I2V V5.2 cargan bien; si se rompen, re-importar los JSON frescos de la rama (los tenemos bajados en `Downloads\naia-lora-workflows\`).
3. **Cómo funcionan los motores "custom" (GPT Images / Google Flow)**: `flow_automation/` es un bridge de AUTOMATIZACIÓN DE NAVEGADOR — los nodos `VRGDG ChatGPT Images Browser` y `VRGDG Flow Browser Image Edit` manejan un Chrome REAL con perfil logueado (`chrome-flow-profile/`, login una vez). Setup: nodo `VRGDG Flow Browser Setup` (baja Node.js portable + npm install solo).
4. **⚠ IMPLICACIÓN CRÍTICA para ComfyDeploy**: esos nodos abren Chrome EN LA MÁQUINA donde corre ComfyUI. En una sesión serverless de ComfyDeploy no hay Chrome/GUI → **los motores browser (GPT Images/Flow) probablemente solo funcionan en ComfyUI LOCAL**. En la nube, los motores viables del Builder son: **Z-Image (nuestro LoRA ✓), Flux, Nano Banana (si va por API con key), Krea 2**. Plan B para GPT Images en nube: generar los frames en ChatGPT a mano (como hoy) y cargarlos como referencias del Reference Builder.

## Secuencia propuesta (sesión dedicada)

1. Actualizar el pack vrgdg de la máquina al head de la rama v9 (PATCH dispara rebuild — puede tardar 15 min-3 h; el build_log no se actualiza en vivo, no asumir colgado)
2. Sesión L40S → cargar nodo `VRGDG Music Video Builder UI` → crear proyecto de prueba
3. Reference Builder: personaje = naiacruz (LoRA Z-Image ON) · motor de imagen = Z-Image primero (validar el stack completo), Nano Banana después
4. Proyecto piloto corto (2-3 escenas, audio corto) antes de nada grande
5. Re-validar MVC clásico (Prompt Creator + I2V) post-update
6. Documentar todo aquí

## Pendientes previos (cerrar antes o en paralelo)
- Video "Soy Naia Cruz": el run corrió 100% pero sin MP4 final visible — bajar los 4 chunks de `output/` y ensamblar local (Claude, $0)
- 7 Maravillas: 9 ejecuciones en TAO Director V2 pendientes de crédito/tiempo
