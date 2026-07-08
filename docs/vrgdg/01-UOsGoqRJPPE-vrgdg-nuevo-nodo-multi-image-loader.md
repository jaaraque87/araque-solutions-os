<!-- generado por yt-analyze 2026-07-08 16:30 | modelo gemini-3.5-flash | tokens in/out: 20947/2205 -->

# VRodo Music Video Builder UI para ComfyUI - High-Level Overview - 04:03 - [URL_PLACEHOLDER]

## TL;DR (3 lineas)
* Interfaz de usuario integrada en ComfyUI (VRodo Video Builder) para generar videos cinematográficos escena por escena.
* Automatiza la sincronización de audio, letras de canciones (o marcas de tiempo), consistencia de personajes (LoRA MSR) y guion gráfico (storyboard).
* Se ejecuta en segundo plano con soporte para múltiples motores de imagen/video (LTX, Flux, ZImage) y automatización con LLMs locales.

## Timeline con timestamps
* **00:00** - Introducción a VRodo Video Builder en fase beta (evolución de flujos basados en nodos).
* **00:12** - Inicio y administración de proyectos dentro de la interfaz del Video Creator.
* **00:30** - Descripción general de la UI principal: Escenas (izq), Previsualización (centro), Ajustes (der) y Timeline (abajo).
* **00:46** - El Asistente (Wizard) y los pasos guiados del flujo de trabajo general.
* **01:08** - Mapeo de líricas (Lyric Mapping) y sincronización con la línea de tiempo.
* **01:43** - Reference Builder para mantener consistencia de personajes, vestuarios, props y locaciones.
* **02:01** - Storyboard Builder para la dirección creativa (movimiento de cámara, planos y estilo).
* **02:21** - Configuración de generación de imagen (ZImage, Flux, Nano Banana, Ernie, Krea 2).
* **02:47** - Opciones de generación de video (Image to Video, Reference to Video, Ingredients to Video, Text to Video).
* **03:13** - Configuración del LLM Runner para optimizar prompts con modelos locales o APIs.
* **03:33** - Renderizado por lotes (Batch) y compilación del video final ensamblado.

## Configuraciones EXACTAS mostradas en pantalla
* **00:12** UI principal -> `Existing Projects` list: `VRDOO_ConfyUI_win_portable_v_...`
* **00:30** Panel Derecho (Scene Settings) -> `Scene Label` = `Scene 1`
* **00:30** Panel Derecho (Scene Settings) -> `Start` = `0.00`, `End` = `5.95`
* **00:35** Panel Derecho -> Pestaña `Image` -> LLM/Models = `gemma-2-27b-it-Q4_K_M`
* **00:35** Panel Derecho -> Pestaña `Image` -> ZImage Models = `open_z_llm_scale(calibrated)`
* **00:41** Panel Derecho -> Pestaña `Video` -> `Use Video LoRAs?` = Activado [x]
* **00:41** Panel Derecho -> Pestaña `Video` -> Video Model = `ltx-video-2b-1.1...`
* **00:44** Panel Derecho -> Pestaña `Audio` -> Timeline Audio -> Global Audio = `local_1st_ballad`
* **00:47** Panel Wizard -> `Video Model Block` = `LTX-2.1-320p-128f-Alpha`
* **00:47** Panel Wizard -> `Video VAE` = `LTX_Video_vae_F32`
* **00:47** Panel Wizard -> `Gemma/CLIP` = `gemma-2-2b-it-abliterated-silly-to-high-fidelity-edition`
* **00:47** Panel Wizard -> `Voodoo Demosaic Model` = `gemma-2b-it-Q4`
* **00:47** Panel Wizard -> `Render Status` -> `Frames per second` = `24`
* **00:47** Panel Wizard -> `LoRA Settings` -> LoRA 1 = `LTX_Minimal_0.5`, LoRA 2 = `DecisiveWire1stLine` (Strength = 0.8)
* **00:52** Panel Wizard -> `Lyrics + Scenes` -> `Scene minimum seconds` = `2.0`, `Scene maximum seconds` = `8.0`
* **01:24** Lyric Mapping -> `Scene 1` (00:00:00 -> 00:08:00) -> Singer/Character = `The Woman`
* **01:24** Lyric Mapping -> `Scene 1` -> Location = `Abandoned house hallway`
* **01:46** Reference Builder -> `Subject type` = `character | person`
* **01:46** Reference Builder -> `Subject name` = `The Woman`
* **01:46** Reference Builder -> `Ref description` = `high fashion editorial portrait...`
* **02:03** Storyboard Builder -> `Default style` = `Movie video styles`
* **02:03** Storyboard Builder -> `Default performance style` = `Default cinematic`
* **02:13** Edit Scene Card -> `Starting shot format` = `medium shot`
* **02:13** Edit Scene Card -> `Camera motion pattern` = `handheld follow`
* **03:13** LLM Runner -> `Trust LLM runner` = `Ollama Local` (Opciones: `Gemma Local`, `LM Studio`, `LLM API`)
* **03:40** Build Full Video? -> `Scenes to run` = `All scenes`
* **03:40** Build Full Video? -> `Video seed behavior` = `Keep current video seeds`

## Flujo de trabajo paso a paso
1. **00:05** - Cargar el nodo `VRodo Music Video Builder UI` en el espacio de trabajo de ComfyUI.
2. **00:12** - Iniciar o seleccionar un proyecto en la ventana emergente de inicio.
3. **00:15** - Cargar el archivo de audio global en la pestaña "Audio" para definir el timeline.
4. **01:08** - Importar o transcribir las letras (Lyrics) para generar automáticamente bloques de escenas basados en marcas de tiempo.
5. **01:24** - Asignar personajes (singers) y localizaciones a cada escena creada mediante la matriz de Lyric Mapping.
6. **01:46** - Configurar los descriptores e imágenes de referencia de los personajes/entornos en el Reference Builder.
7. **02:13** - Ajustar los parámetros de cámara, encuadre y estilo de movimiento en el Storyboard Builder.
8. **02:22** - Seleccionar el modelo de generación de imagen keyframe (p. ej., ZImage o Flux) para inicializar visualmente la escena.
9. **02:50** - Configurar el modo de renderizado de video en la pestaña "Video" (se recomienda "Image to Video" o "Reference to Video" con LTX-Video).
10. **03:13** - Ejecutar el LLM Runner (Gemma/Ollama) para expandir los prompts de texto con contexto de escena estructurado.
11. **03:40** - Hacer clic en "Build Full Video" para renderizar todos los clips por lotes en ComfyUI y compilarlos en el archivo final de video con audio.

## Modelos, archivos y links mencionados
* **Video LTX Model**: `LTX-2.1-320p-128f-Alpha` o `ltx-video-2b-1.1` (Colocar en la carpeta habitual de checkpoints/LTX de ComfyUI).
* **LLM Local**: `gemma-2-27b-it-Q4_K_M` y `gemma-2-2b-it-abliterated` (Colocar en la carpeta de modelos LLM correspondientes de ComfyUI o servir vía Ollama/LM Studio).
* **Video VAE**: `LTX_Video_vae_F32`
* **Canal/Servidor de soporte**: El autor menciona un servidor de Discord (Tao of AI) en la descripción del video para descargar instaladores y workflows actualizados.

## Requisitos de hardware/software mencionados
* **Software**: ComfyUI (versión portátil o estándar con dependencias de Python instaladas), Ollama o LM Studio para procesamiento de lenguaje natural (LLM) opcional en local.
* **Hardware**: GPU de alta gama (VRAM optimizada) requerida para procesar paralelamente modelos Flux, LTX-Video y Gemma LLM.

## Advertencias, errores y trucos del autor
* **01:36** - **Truco**: Aunque las herramientas tengan nombres relacionados con líricas ("Lyrics", "Singers"), el workflow sirve igual para cortometrajes o visualizadores instrumentales sin vocales utilizando los bloques de tiempo como beats visuales.
* **03:40** - **Ojo con esto**: Durante reconstrucciones o iteraciones de renders específicos, activa "Keep current video seeds" en la ventana de compilación final para evitar que cambie la consistencia visual de las escenas ya aprobadas.

## Que NO explica el video (huecos)
* No detalla el proceso de instalación técnica de las dependencias de ComfyUI necesarias para correr la UI externa (`VRodo`).
* No muestra cómo configurar el puerto de red o la IP para enlazar Ollama local o LM Studio con la pestaña LLM Runner.
