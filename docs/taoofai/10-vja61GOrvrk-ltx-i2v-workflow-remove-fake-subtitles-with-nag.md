<!-- generado por yt-analyze 2026-07-07 10:44 | modelo gemini-3.5-flash | tokens in/out: 24932/2041 -->

# FIX LTX FAKE SUBTITLES | NAG + CROP METHOD - 04:51 - [URL]

## TL;DR (3 líneas)
* El video aborda el problema de los subtítulos falsos generados por LTX en ComfyUI al crear videos de personajes hablando.
* Compara tres soluciones: prompts negativos/positivos modificados, el parche NAG (Anti-Text Guidance) y el método de extensión de imagen inferior con recorte (Crop).
* El método de extensión de imagen inferior combinado con recorte resulta ser el más estable y efectivo para eliminar texto sin perder control de la sincronización labial.

## Timeline con timestamps
* **00:00** - Demostración del problema de subtítulos falsos en LTX.
* **00:16** - Stock Template (LTX I2V Baseline).
* **00:41** - Prueba de Negative Prompt.
* **01:21** - Prueba de eliminación de diálogo en Positive Prompt (No Dialogue Text).
* **02:00** - Implementación de LTX I2V + NAG (Anti-Text Guidance).
* **02:46** - Prueba de control desactivando NAG.
* **03:05** - Prueba del método Black Bar Trap.
* **03:51** - Prueba del método Image Extension (extensión de cuadro inferior).
* **04:22** - Implementación de Toggles lógicos en ComfyUI.
* **04:39** - Demostración final del flujo optimizado.

## Configuraciones EXACTAS mostradas en pantalla
* **00:18** `Load Image` -> image = `小美鱼.png` (Resolución original: 1440x1080)
* **00:23** `Image to Video LTX-2.3` -> width = `512` (cambiado de 1280)
* **00:25** `Image to Video LTX-2.3` -> height = `512` (cambiado de 720)
* **00:25** `Image to Video LTX-2.3` -> duration = `5`
* **00:25** `Image to Video LTX-2.3` -> checkpoint_name = `gamma_3.128_8_fp4_mixed_safetensors` [ILEGIBLE @ 00:25, similar a `gamma_3.128...`]
* **00:25** `Image to Video LTX-2.3` -> latent_up_scale = `ltx-2.3-spatial-upscaler-v2-11.safetensors`
* **00:25** `Image to Video LTX-2.3` -> fps = `25`
* **00:25** `Image to Video LTX-2.3` -> seed = `510825313204` (randomize)
* **00:53** `CLIP Text Encode (Prompt)` (Negative) -> text = `"pc game, console game, video game, cartoon, childish, ugly, subtitles, captions, on-screen text, text overlay, lower-third, title card, watermark, logo, written words, floating text, UI text, Chinese text, English text"`
* **01:34** `Image to Video (LTX-2.3)` (Positive Prompt modificado) -> text = `"A square close-up shot of the young Chinese female presenter from the reference image, speaking directly to the camera... Her eyes look back at the camera and speaks English..."` (Se removieron las líneas de diálogo explícitas).
* **02:16** `LTX2 NAG patch` (Nodo de Shidanyan) -> `nag_scale` = `11.000`
* **02:16** `LTX2 NAG patch` -> `nag_alpha` = `0.250`
* **02:16** `LTX2 NAG patch` -> `nag_tau` = `2.500`
* **02:16** `LTX2 NAG patch` -> `replace` = `True`
* **02:50** `LTX2 NAG patch` -> `nag_scale` = `0.000` (Desactivación de NAG)
* **03:20** `ComfyUI Inputs` -> `OUTPUT HEIGHT` = `512`
* **03:20** `ComfyUI Inputs` -> `DURATION SECONDS` = `4.0`
* **03:20** `ComfyUI Inputs` -> `BLACK BAR HEIGHT` = `160`
* **04:02** `ComfyUI Inputs` -> `BOTTOM EXTEND HEIGHT` = `192`
* **04:24** `ComfyUI Toggles` -> `EXTEND ON` = `True` / `NAG ON` = `False`
* **04:24** `ComfyUI Inputs` -> `EXTEND + CROP BOTTOM` = `192`
* **04:24** `ComfyUI Inputs` -> `NAG SCALE WHEN ON` = `11.0`
* **04:24** `ComfyUI Inputs` -> `CLEAN BOTTOM PX` = `192`

## Flujo de trabajo paso a paso
1. **[00:18]** Carga la imagen de referencia de la mujer asiática (`小美鱼.png`) en el nodo `Load Image`.
2. **[00:22]** Configura la resolución de salida a 512x512 y presiona `Run` usando la plantilla base.
3. **[00:46]** Expande el workflow para localizar el nodo de Prompt Negativo. Agrega etiquetas de exclusión de texto (`subtitles`, `captions`, `text overlay`).
4. **[01:24]** Modifica el Prompt Positivo removiendo la línea de diálogo exacta, dejando solo descripciones de acción hablada.
5. **[02:14]** Integra el nodo de parche `LTX2 NAG patch` (NAG Anti-Text Guidance) conectándolo directamente al pipeline de LTX.
6. **[02:50]** Reduce `nag_scale` a 0 para verificar la reaparición de subtítulos falsos en el video de control.
7. **[03:20]** Configura una trampa física de barra negra inferior (`BLACK BAR HEIGHT` = 160) en la composición de entrada de la imagen.
8. **[04:02]** Configura una extensión de imagen inferior (`BOTTOM EXTEND HEIGHT` = 192) para desplazar el texto generado fuera de la composición final.
9. **[04:24]** Configura interruptores de control (`Toggles` lógicos) para alternar dinámicamente entre el método NAG y la extensión de imagen con auto-recorte (`Crop`).

## Modelos, archivos y links mencionados
* **Nodos personalizados:** `LTX2 NAG patch` (por Shidanyan).
* **Modelos LTX:** `ltx-2.3-22b-dev-fp8.safetensors`, `ltx-2.3-spatial-upscaler-v2-11.safetensors`.
* **Descarga de Workflow:** Disponible en RunningHub y el enlace directo de la descripción.

## Requisitos de hardware/software mencionados
* **Software:** ComfyUI instalado localmente.
* **Dependencias:** Nodos personalizados de Shidanyan (`LTX2 NAG patch` y herramientas de extensión/recorte de imagen).

## Advertencias, errores y trucos del autor
* **[01:17]** *Advertencia:* El uso exclusivo de prompts negativos no resuelve de manera consistente la generación de subtítulos falsos en LTX.
* **[01:54]** *Advertencia:* Remover el diálogo escrito en el prompt positivo evita los subtítulos, pero genera un habla aleatoria en el personaje, inutilizando el lip-sync.
* **[03:40]** *Truco:* El método "Black Bar Trap" atrae los subtítulos hacia la barra negra, pero no es estable. El modelo aún puede generar texto en zonas aleatorias de la imagen original.
* **[04:12]** *Truco:* La extensión de la imagen inferior combinada con recorte (`Crop`) es la solución definitiva. Forza la creación de subtítulos en el área extendida para eliminarlos fácilmente después sin distorsionar el video.

## Qué NO explica el video (huecos)
* No detalla cómo instalar manualmente el nodo personalizado `LTX2 NAG patch` de Shidanyan si no figura directamente en el ComfyUI Manager.
* No muestra las conexiones lógicas ni los nombres exactos de los nodos de recorte (`Crop`) automático que procesan los 192 píxeles agregados en la parte inferior.
