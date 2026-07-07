# LTX Director V2 + Bernini — Simplified — 08:10 — https://www.youtube.com/watch?v=kRNyUOaid7g
_Extracción vía Gemini (video → markdown estructurado), 2026-07-07. Repo: github.com/ai2764/Camera-lab_

## TL;DR
Camera Lab V2 unifica LTX Director V2 y Bernini (edición WAN 2.2) en una UI de timelines sobre ComfyUI: generación continua de películas por storyboard, corrección por trimming/in-betweening, edición localizada de objetos/caras con auto-stitching. Filosofía: workflows dedicados separados en vez de recablear nodos.

## Configuraciones exactas clave
- Global prompt: "A continuous cinematic video with coherent subject identity, consistent lighting, natural motion, and smooth visual continuity across the full timeline. Medium close-up, cinematic kitchen interior."
- Negative: "subtitles, captions, text overlay, watermark, logo, lora card, extra pieces, duplicate person, identity change, face morphing, deformed face, bad hands, extra fingers, missing fingers, camera rot, dutch angle, sudden rot, scene change, flash, sudden movement, bad quality, low resolution, blurry, jittery, choppy"
- Preset 16:9 1280x720 · Seed random (o fijo ej. 7079869016)
- Storyboard 2x2: batch prompts con sintaxis `2.0s <prompt de escena>` por línea (duración explícita por plano)
- Timelines del modo Generate: MAIN · VIDEO AUDIO · DIALOGUE · IC VIDEO. Modo Retake: pista única.
- IC VIDEO: LoRA `wan2.2_lora_ics_anycolor` @ strength 1 → sustitución de objetos por prompt local
- Bernini VR2V (WAN2.2): source clip recortado + reference image + prompt ("she is eating an ice cream") + Preserve audio ✓ + Auto stitch ✓ (16.83s-19.00s del ejemplo)
- WAN VACE Inpaint: reference image (selfy.png) + máscara manual brush 48px + prompt "replace the face" → face swap quirúrgico conservando pelo/luz/estructura
- Casting: análisis de guion por LLM local OpenAI-compatible en `http://127.0.0.1:12345/v1` (si offline → asignación manual); voces con emoción (ej. `xiaomei - angry`)

## Flujo esencial (resumen)
1. Director → Set Storyboard → pegar batch prompts `2.0s ...` → Add to timeline → Queue Run (S1..S8 en paralelo)
2. Error en un tramo → X sobre el clip (queda empty segment) → Edit → in-betweening con **guide image** (truco del autor: mucho más controlable que solo texto)
3. Al importar clips, el audio se separa solo en VIDEO AUDIO → borrar proactivamente si se superpondrán diálogos nuevos
4. Casting → Analyze (LLM) → voz+emoción → colocar en DIALOGUE
5. Retake → recortar rango → Auto stitch ✓ → VR2V (Bernini) o Inpaint (VACE) → Queue Run → se recose solo

## Cita de arquitectura (07:25, aplicable a nuestra app)
"In Bernini, switching between different modes normally means rewiring the workflow and bypassing nodes. In Camera Lab, I split those into separate workflows instead. It's not the most DRY approach, but each one has a clear dedicated job."

## Archivos del repo
- `workflows/app/`: LTX_Director_2_Workflow.json · wan22_bernini_v2v.ui.json · wan_vace_inpainting.ui.json
- `scripts/`: install_workflows.py/.ps1 · start_camera_lab.py · stop_camera_lab.py

## Huecos del video (cubiertos en el repo)
Instalación (docs/wiki/Installation-Guide.md), ubicación de modelos, servidor LLM del Casting (puerto 12345), VRAM mínima, sintaxis estricta del storyboard 2x2.

## RELEVANCIA PARA ARAQUE (análisis Claude)
1. **WAN VACE Inpaint face-replace = arreglo post-hoc del problema "4 hermanas de Naia"**: se puede inyectar la cara EXACTA de Naia (foto de referencia) escena por escena sobre videos ya renderizados, conservando luz/pelo. Complemento o alternativa al LoRA.
2. **Bernini VR2V = "omni local sin API"**: edición localizada de objetos con referencia, corre en GPU propia (o L40S de ComfyDeploy) — sin billing de Google.
3. **LTX Director V2 es de What Dreams Cost** — su custom node YA está en la máquina de ComfyDeploy (workflows LTXDIRECTOR/VideoFlow del usuario). Camera Lab es la UI que le faltaba.
4. **El patrón de app** (server Python liviano + frontend estático + workflows dedicados parcheados por API) es el blueprint para nuestra "app tipo NORA".
5. **Casting LLM local en :12345 (OpenAI-compatible)** → conectable a LM Studio en el PC del usuario.
