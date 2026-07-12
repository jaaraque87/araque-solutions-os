<!-- analyze_local 2026-07-11 20:10 | gemini-3.5-flash | fuente: 7-11-26_upates.mp4 -->

# Actualización de V9 Video Builder UI (Lyric & Visual Scene Mapping) - 05:20

## TL;DR
* Presenta la integración de Meta AI (Browser AI) como alternativa gratuita para generación automatizada de imágenes.
* Introduce herramientas de automatización como "Enhance All", importación masiva por carpetas y asignación de personajes vía Codex.
* Añade pistas de superposición (Overlay Tracks) para flujos de trabajo de B-Roll, con copias no destructivas y edición temporal rápida.

## Timeline con timestamps
* **00:00** - Introducción y novedades de Meta AI (Browser AI).
* **01:23** - Demostración en vivo de Browser AI con inicio de sesión y automatización de prompts.
* **02:57** - Manejo de errores de generación de imágenes con Meta AI.
* **03:28** - Modo manual y opción de auto-avance ("Auto advance").
* **04:31** - Herramientas "Enhance All" e importación masiva desde carpeta en proyectos vacíos.
* **06:44** - Mapeo y asignación aleatoria de personajes/escenarios ("Scene Reference Builder").
* **07:41** - Configuración de límites de contexto para el LLM local Gemma ("LLM Runner").
* **08:35** - Función de continuidad de imagen para mantener coherencia visual entre escenas consecutivas.
* **09:12** - Prueba en vivo de continuidad visual en el lienzo de generación.
* **10:24** - Introducción a la nueva funcionalidad de pistas de superposición ("Overlay Tracks") para B-Roll.
* **11:54** - Creación de videos superpuestos, copia no destructiva de clips, bloqueo y recorte ("Trim") en la línea de tiempo.

## Configuraciones EXACTAS mostradas en pantalla
* `[00:19]` **UI -> Pestaña Image -> Model** = `ZImage / Flux Klein / Krea 2`
* `[00:28]` **UI -> Botón Browser AI** = Activo
* `[00:40]` **UI -> Botones de proveedor de Browser AI** = `Flow Nano Banana / GPT Image / Meta AI` (Seleccionado: `Meta AI`)
* `[01:33]` **Browser AI Window** = URL `meta.ai`
* `[03:30]` **Pestaña Image -> Meta AI Settings** = `Manual Mode` (Checkbox), `Auto advance input import` (Checkbox)
* `[03:51]` **Pestaña Image -> Meta AI Settings** = Botones: `Open Manual Browser`, `Export Scene Refs`, `Import Latest Download`
* `[04:02]` **Pestaña Image -> Meta AI Settings -> Prompt edit box** = `using the character and location reference images, create 5 new shots...`
* `[04:36]` **Pestaña Tools** = Botón `Enhance All`, Botón `Fill Timeline Images From Folder`
* `[05:39]` **File Explorer -> Path** = `C:\ComfyUI\ComfyUI_windows_portable\ComfyUI\output`
* `[06:45]` **UI -> Botón Reference Builder -> Pestaña Mapping** = Botón `Assign Scenes`
* `[06:52]` **Character & Location Assignment Modal** = Checkbox `Replace existing mappings`, Checkbox `Avoid consecutive location repeats`, Dropdown `Scene range start`, Dropdown `Character pattern` = `Random character each scene`
* `[07:42]` **LLM Runner Modal** = `Gemma Local`, Input `Context Limit / No. of words` = `8000`
* `[08:48]` **Pestaña Image -> Image Settings** = Checkbox `Ask to send previous scene image`
* `[09:15]` **Alert Dialog** = Texto: `Send the previous scene image as a reference for the Flow/or AI generation? 1. SCENE 1 will be uploaded with the prompt so Flow/or AI can see what happened last.`
* `[10:26]` **Timeline UI -> Botón Overlay Track** = `Display Track: On`
* `[12:17]` **UI Dialog** = Texto: `This scene already has a video. Choose Add To Overlay Track to keep the base clip and create an alternate track above it, or replace the current clip.` -> Botones: `Cancel / Overwrite / Backup and replace / Add to overlay track`
* `[14:27]` **Timeline -> Right-Click Menu on Overlay Clip** = Opciones: `Restore Video...`, `Trim Left at Playhead`, `Trim Right at Playhead`, `Scene options`, `Delete scene`

## Flujo de trabajo paso a paso
1. `[00:40]` Seleccionar `Meta AI` en la configuración de `Browser AI`.
2. `[01:30]` Abrir el navegador manual para autenticar la cuenta de Meta AI en Chrome.
3. `[02:04]` Hacer clic en `Create with Browser AI` para automatizar la inserción de prompts e imágenes de referencia.
4. `[03:28]` Activar `Manual Mode` y `Auto advance` si se desea guiar la generación conversacionalmente paso a paso.
5. `[04:36]` Ejecutar `Enhance All` en la pestaña `Tools` para aplicar un re-escalado por lotes con Lora de consistencia.
6. `[05:22]` Usar `Fill Timeline Images From Folder` para importar un bloque ordenado de imágenes en proyectos limpios.
7. `[06:51]` Configurar asignaciones aleatorias de personajes abriendo `Reference Builder -> Mapping -> Assign Scenes`.
8. `[08:48]` Activar `Ask to send previous scene image` para habilitar el envío del fotograma previo como referencia de contexto.
9. `[12:15]` Activar el canal superior mediante `Overlay Track: On`, generar un video alternativo y presionar `Add to overlay track`.
10. `[13:35]` Desbloquear el clip de B-Roll (`U` / Unlock) y arrastrarlo horizontalmente para sincronizarlo con el compás de audio.
11. `[14:27]` Hacer clic derecho en el clip superpuesto y recortar los extremos sobrantes usando `Trim Left/Right at Playhead`.

## Modelos, archivos y links mencionados
* **Modelos:** Gemma Local LLM, Flux Klein, Krea 2.
* **Sitios/Servicios:** `meta.ai` (Meta AI), Flow (servicios de generación de IA), ComfyUI, CapCut (mencionado para edición final).
* **Directorios:** `C:\ComfyUI\ComfyUI_windows_portable\ComfyUI\output`

## Advertencias, errores y trucos del autor
* `[02:57]` **Advertencia:** "I wasn't able to create that scene for you... and that's because it has to do with her being underwater... Meta AI is a little bit more particular on what you send it."
* `[07:54]` **Truco:** "Keep in mind obviously going higher [with context limit], you can get OOMs, it can stall, it can literally just sit there and get stuck and not do anything... 15,000 for me was like the max I want to do."
* `[12:38]` **Truco:** "If you right-click on the scene, you can choose to copy the track as an overlay track... so that the original doesn't get touched."

## Que NO explica el video (huecos)
* No se detalla cómo configurar localmente Gemma ni la instalación de dependencias necesarias para habilitar el backend de `LLM Runner`.
* No se profundiza en las configuraciones internas de re-escalado o el flujo de trabajo exacto de ComfyUI que procesa la función "Enhance All".
* Se menciona que la asignación automática por Codex fue generada sin conocer totalmente su lógica de programación subyacente.
