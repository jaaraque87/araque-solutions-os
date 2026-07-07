<!-- generado por yt-analyze 2026-07-07 10:22 | modelo gemini-3.5-flash | tokens in/out: 16187/1720 -->

# Cómo Crear Videos desde un Storyboard de 4 Paneles con LTX 2.3 y Camera Lab - 02:54 - [URL del Video]

## TL;DR
Este tutorial muestra cómo usar ChatGPT (OpenAI Image 2) para generar un storyboard de 4 paneles coherente con un personaje de referencia, extraer prompts de video optimizados y animar la secuencia de forma continua usando la herramienta **Camera Lab** con tecnología LTX 2.3.

---

## Timeline con timestamps

* **00:00** - Introducción a la creación de historias con imágenes de 4 paneles.
* **00:10** - Presentación de OpenAI Image 2 en ChatGPT.
* **00:14** - Generación del guion cinematográfico de 16 segundos en ChatGPT.
* **00:43** - Creación de la plantilla de storyboard de 4 paneles (distribución 2x2).
* **00:59** - Consistencia de personaje mediante imagen de referencia en ChatGPT.
* **01:08** - Generación de prompts y tiempos óptimos de animación para LTX 2.3.
* **01:45** - Importación de storyboard y prompts en la interfaz de Camera Lab.
* **02:00** - Configuración de segmentos, renderizado secuencial y previsualización.
* **02:28** - Método alternativo para subir imágenes individuales sin plantilla 2x2.
* **02:43** - Cierre del video y alternativas de código abierto.

---

## Configuraciones EXACTAS mostradas en pantalla

### 1. Prompts de ChatGPT (00:14 - 01:33)
* **Prompt 1 (Guion - 00:15):** 
  > *"Let's create a simple 16-second story. The main character is a lady. I want a mysterious box that leads to a surprising reveal. The story should have only one location and strong continuity between shots. Break it into 4 shots."*
* **Prompt 2 (Storyboard 2x2 - 00:43):**
  > *"Turn this script into a 4-panel storyboard. Use a 2x2 layout. No borders. Each panel should represent a continuous action. No scene changes. Actions should be continuous."*
* **Prompt 3 (Referencia - 01:01):**
  > *[Imagen de mujer asiática con vestido negro] + "use this reference as the main character"*
* **Prompt 4 (Prompts de Video - 01:12):**
  > *"Provide a prompt for each shot optimized for LTX 2.3 video generation. Use this exact format for every shot: duration, prompt. Also evaluate and suggest the best duration for each shot."*
* **Prompt 5 (Consolidación - 01:33):**
  > *"Put all the prompts together in one clean, copy-pasteable section."*

### 2. Camera Lab - Ventana "2x2 Storyboard" (01:50)
* **2x2 image** = `2x2.png` (Storyboard generado por ChatGPT)
* **Batch prompt** = 
  ```text
  3.5s camera slowly push in, the walk toward the box, slows down, stops beside the table.
  4.0s slowly reach out and places her hand on the lid, studies it briefly, hesitates before opening
  4.0s close up, slowly lifts the lid, beam glow, eyes wider as light shines onto her face
  4.5s over shoulder view, lean forward and looks inside, discovers a miniature version of the room, stares in disbelief, slowly moves closer to inspect it
  ```

### 3. Camera Lab - Parámetros de Timeline Segment 1 (02:00)
* **Local prompt** = `camera slowly push in, the walk toward the box, slows down, stops beside the table.`
* **Timeline image guide** = `2x2_shot_1.png` (Segmentado automáticamente)
* **Start** = `0`
* **Duration** = `3.5`
* **Strength** = `1`
* **Seed** = `1465751015`

### 4. Camera Lab - Parámetros Globales (01:45)
* **Global prompt** = `consistent subject identity, environment continuity, lighting, color, and visual style`
* **Global of strength** = `0.5`
* **Preset** = `Scale 1280x720 / 100%`
* **Frame size** = `1280x720`

---

## Flujo de trabajo paso a paso

1. **[00:14]** Solicita a ChatGPT un guion de 16 segundos estructurado en 4 escenas con alta continuidad en una sola locación.
2. **[00:43]** Pide a ChatGPT convertir el guion en una sola imagen con estructura 2x2 sin bordes.
3. **[00:59]** Sube una imagen de referencia de un personaje a ChatGPT y pídele rehacer la imagen 2x2 aplicándola como protagonista. Guarda la imagen resultante.
4. **[01:11]** Solicita a ChatGPT los prompts optimizados de video para cada escena del storyboard, definiendo tiempos específicos.
5. **[01:45]** Abre **Camera Lab** en el modo "Director".
6. **[01:50]** Haz clic en **2x2 Storyboard**, carga la imagen de 4 paneles e ingresa la lista de prompts por línea en el cuadro de texto. Presiona **Add to timeline**. La herramienta cortará y acomodará los paneles en la línea de tiempo automáticamente.
7. **[02:01]** Presiona **Queue Run** para comenzar la generación secuencial de los fragmentos de video.
8. **[02:10]** Previsualiza el video unificado ("01_director") en el reproductor integrado.

---

## Modelos, archivos y links mencionados
* **OpenAI ChatGPT** (DALL-E 3 / Image 2) para generación de imágenes y textos.
* **Camera Lab** (Interfaz/herramienta web construida sobre ComfyUI). No se especifican URLs de instalación en el video.
* **LTX 2.3** (Modelo de difusión de video base).

---

## Requisitos de hardware/software mencionados
* Servidor local o remoto compatible con flujos de ComfyUI (se observa el botón "ComfyUI online" en la esquina superior derecha de la interfaz).

---

## Advertencias, errores y trucos del autor

* **[01:11]** *"For LTX 2.3, slower camera movement and clear action progression generally produce the best results."* (Los movimientos de cámara lentos y una progresión de acción clara mejoran drásticamente los resultados en LTX 2.3).
* **[01:26]** *"Usually ChatGPT gives very long prompts, and it takes a few rounds to refine them."* (ChatGPT suele generar prompts excesivamente largos. Es crucial refinarlos en varias rondas de chat antes de usarlos).

---

## Qué NO explica el video (huecos)

* No se incluye el enlace de descarga ni instrucciones de instalación de la herramienta **Camera Lab**.
* No detalla cómo conectar la interfaz de Camera Lab con el backend de ComfyUI.
* No explica cómo procesar o combinar el video de salida con audio o música (el video final reproducido cuenta con música pero no se muestra su adición).
