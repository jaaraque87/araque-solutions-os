<!-- analyze_local 2026-07-08 21:57 | gemini-3.5-flash | fuente: id lora.mp4 -->

# Demostración de ID-LoRA, Modo Agente FlowGPT y Storyboard Builder en V9 Video Builder UI - 09:49

## TL;DR
Presentación de funciones en desarrollo de V9 Video Builder UI para cortometrajes usando ID-LoRA. Permite clonación de voz y consistencia de identidad en múltiples escenas, integrando flujos con FlowGPT y un Storyboard Builder renovado.

---

## Timeline con timestamps
* **00:00 - 01:30**: Introducción al estado del desarrollo (WIP) enfocado en cortometrajes y consistencia de escenas.
* **01:30 - 02:25**: Configuración de modelos (`Models`) y selección del ID-LoRA adecuado.
* **02:25 - 02:51**: Pestaña `Video Settings` y asignación de muestras de audio para clonación de voz.
* **02:51 - 03:22**: Configuración de diálogos y prompts en la sección `LLM Prompting`.
* **03:22 - 04:32**: Uso del `Reference Builder` (ID-LoRA Ref Builder) para gestionar personajes y audios individuales.
* **04:32 - 05:19**: Asignación de personajes y cálculo automático de duración en `Scene Casting`.
* **05:19 - 06:09**: Pestaña `Storyboard Builder` -> `Image Prep` para configurar la estética y expresiones faciales por defecto.
* **06:09 - 07:31**: Planificación del guion, premisas y beats en `Story Layer`.
* **07:31 - 08:20**: Demostración del ciclo de generación y sincronización de diálogos.
* **08:20 - 08:45**: Integración de generación de imágenes mediante `Flow GPT`.
* **08:45 - 09:49**: Configuración del movimiento de cámara en `Video Prep` y conclusiones.

---

## Configuraciones EXACTAS mostradas en pantalla
* **01:35** `Video` -> `Image to Video` = ID-LoRA (Selected)
* **01:42** `Models` -> `Required ID-LoRA` = `1_740,733_1_433_caldescenes`
* **01:48** `Models` -> `Pass 1` = `1`
* **01:48** `Models` -> `Pass 2` = `1`
* **02:24** `Models` -> `VideoLoRA 1 name` = `NFT`
* **02:26** `Video Settings` -> `FPS` = `24`
* **02:27** `Video Settings` -> `Width` = `1920` (unreadable, default likely 1024)
* **02:27** `Video Settings` -> `Height` = `1024`
* **02:30** `Video Settings` -> `Reference voice sample` = `C:/comfyui/input/dialogues-scenes/so.wav` [ILEGIBLE @ 02:30, posiblemente mp3/wav de voz]
* **02:55** `LLM Prompting` -> `Live / lyric / dialogue` = `Hi there, have you heard of the ID LoRA?`
* **02:57** `LLM Prompting` -> `Performer(s) / speaker(s)` = `be woman`
* **03:28** `ID-LoRA Ref Builder` -> `Character 1 Name` = `the woman`
* **03:35** `ID-LoRA Ref Builder` -> `Reference voice sample` = `C:/comfyui/input/Good morning.mp3`
* **03:36** `ID-LoRA Ref Builder` -> `Speaker style` = `casual`
* **05:25** `Storyboard Builder` -> `Short film prompt` = `Film dialogue coverage`
* **05:32** `Storyboard Builder` -> `Image aesthetic` = `Default thin still`
* **05:47** `Storyboard Builder` -> `Global consistency phrase` = `soft lighting, cinematic film, rich colors, shot on 35mm lens, high quality`
* **05:49** `Storyboard Builder` -> `Global acting style` = `Dialogue naturalism`
* **05:54** `Storyboard Builder` -> `Global screen face` = `Default screen setting`
* **06:07** `Storyboard Builder` -> `Custom facial expression` = `emotional face with context-appropriate expressions, eye movement, micro expression, subtle blinks, looking towards conversation partner`
* **08:50** `Storyboard Builder` -> `Video Prep` -> `Auto-camera pan` = `Balanced cinematic flow`
* **08:53** `Storyboard Builder` -> `Video Prep` -> `Camera pan speed` = `4`
* **08:54** `Storyboard Builder` -> `Video Prep` -> `Character motion speed` = `4`
* **08:55** `Storyboard Builder` -> `Video Prep` -> `Global motion setting` = `Default screen setting`

---

## Flujo de trabajo paso a paso
1. **[00:40]** Cargar las imágenes y composiciones base para cada una de las escenas secuenciales (Escena 1, Escena 2, Escena 3).
2. **[01:34]** Habilitar el pipeline de `ID-LoRA` desde la sección de video y configurar el modelo de pesos en la pestaña `Models`.
3. **[02:26]** Importar el archivo de voz de referencia global (`.mp3` o `.wav`) en `Video Settings` para la clonación de la identidad del hablante.
4. **[02:51]** Escribir los diálogos y asignar los roles de habla a los personajes mediante `LLM Prompting`.
5. **[03:25]** Utilizar el `Reference Builder` (`ID-LoRA Ref Builder`) para asignar muestras de voz únicas por personaje (por ejemplo, voz de hombre y voz de mujer).
6. **[04:32]** Ir a `Scene Casting` y vincular los personajes con sus diálogos respectivos, activando `Auto duration` para ajustar el tiempo del video al audio.
7. **[05:20]** Acceder a `Storyboard Builder` -> `Image Prep` para definir los estilos de acting y consistencia visual general.
8. **[06:10]** Escribir o refinar el guion en la sección `Story Layer`. Generar la premisa (`Create Story Premise`) y el resumen (`Create Short Film Brief`) con el LLM.
9. **[07:44]** Ejecutar `Plan Dialogue Scenes` y `Apply Dialogue Plan` para generar los diálogos estructurados basados en la historia.
10. **[08:20]** Utilizar `Flow GPT` para procesar y renderizar de forma automatizada las prompts de imagen generadas.
11. **[08:46]** Ir a `Video Prep` para definir los valores de movimiento de cámara antes de compilar el video final.

---

## Modelos, archivos y links mencionados
* **ID-LoRA base**: `1_740,733_1_433_caldescenes` (versión recomendada por la autora).
* **ID-LoRA celebridades**: `1_740,733_1_433_celebrities` (mencionado como alternativa menos consistente).
* **Voz de referencia**: `Good morning.mp3` y archivos de audio locales en la ruta `input/dialogues-scenes/`.
* **Enlaces**: La interfaz contiene un botón `Hugging Face Page` para descargar el ID-LoRA.

---

## Advertencias, errores y trucos del autor
* **[01:55]** Evitar usar el LoRA basado en celebridades si se busca alta consistencia de voz entre escenas; el LoRA principal de clonación de voz funciona significativamente mejor.
* **[02:05]** El botón `Hugging Face Page` de la interfaz de usuario está desactualizado y redirige a un LoRA antiguo. El link correcto de descarga será proporcionado en el canal de Discord.
* **[05:13]** No entrar a `Scene Casting` antes de escribir o generar los diálogos en `Story Layer`, ya que el sistema requiere las líneas de texto para calcular las duraciones automáticas de video.
* **[08:05]** Ignorar los botones superiores del encabezado (`Generate Images`, `Stop Prompts`, etc.) en la pestaña `Storyboard Builder`. Están obsoletos y se eliminarán en la versión final de producción.

---

## Qué NO explica el video (huecos)
* No se realiza una renderización final completa en pantalla debido a bugs en el playhead de la interfaz (`[01:15]`).
* No se detallan las especificaciones técnicas requeridas para que los audios de referencia clonen la voz con calidad óptima (duración exacta recomendada, nivel de ruido de fondo).
* No se profundiza en el funcionamiento de la API de FlowGPT ni en los requisitos de hardware locales para correr este pipeline de LTX.
