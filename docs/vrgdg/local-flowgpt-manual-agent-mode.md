<!-- analyze_local 2026-07-08 21:58 | gemini-3.5-flash | fuente: FlowGPT Manual agent mode.mp4 -->

# Automatización de Storyboards con FlowGPT en V9 Video Builder - 4:35

## TL;DR (3 líneas)
* Presentación de la integración experimental (no publicada) entre V9 Video Builder UI y FlowGPT local.
* Uso de agentes de FlowGPT para interpretar letras de canciones e imágenes de referencia, generando secuencias de storyboard cohesivas.
* Flujo de trabajo semi-manual optimizado mediante descarga local y un botón de importación rápida al timeline de escenas.

---

## Timeline con timestamps
* **0:00 - 1:10**: Introducción a la pestaña FlowGPT, opciones de modo manual, avance automático y exportación de referencias.
* **1:10 - 2:13**: Configuración de la interfaz del agente FlowGPT en el navegador local y redacción de instrucciones iniciales.
* **2:13 - 3:28**: Envío de letras de canciones al agente de IA para iniciar el proceso de generación iterativo (cámara rápida).
* **3:28 - 4:35**: Resolución de errores de importación automática, demostración del botón "Import Latest Download" y asignación final al timeline.

---

## Configuraciones EXACTAS mostradas en pantalla

* **0:15 pestaña superior derecha** -> Selección de pestaña = `FlowGPT`
* **0:37 panel lateral derecho** -> Checkbox `Manual Mode` = Habilitado (Checked)
* **0:38 panel lateral derecho** -> Checkbox `Auto-advance after import` = Habilitado (Checked)
* **1:11 URL de la interfaz FlowGPT** -> URL local = `http://127.0.0.1:5813/` [Aproximado, basado en puerto local]
* **1:11 Selector de modelo en FlowGPT** -> Model = `Flex SD3.5` (o similar activo en el backend de ComfyUI)
* **1:40 Chat de FlowGPT** -> Prompt de usuario = *"i need a storyboard for this character. i need 5 different images, not a grid or collage"*
* **2:17 Chat de FlowGPT** -> Prompt con estructura de letras = *"I'm making a music video. Here are the lyrics for each scene. Each lyric segment is a scene and I need one image for each scene."*
* **3:34 panel lateral derecho** -> Botón nuevo = `Import Latest Download`
* **3:48 panel lateral derecho** -> Consola de logs = *"Manual Mode: Flow ready for Scene 3"*

---

## Flujo de trabajo paso a paso

1. **[0:15] Activar pestaña FlowGPT**: En la interfaz de Video Builder, cambia de la pestaña estándar de Imagen/Video a `FlowGPT`.
2. **[0:37] Configurar importación manual**: Activa `Manual Mode` y `Auto-advance after import` para controlar la asignación escena por escena.
3. **[1:21] Inicializar navegador**: Haz clic en `Open Manual Browser` para abrir la interfaz del agente de chat FlowGPT en una ventana secundaria.
4. **[1:28] Exportar referencia**: En el constructor de video, selecciona la escena con la imagen de estilo base y haz clic en `Export Scene Refs` para enviarla automáticamente al chat del agente.
5. **[1:40] Instruir al agente**: En FlowGPT, redacta el prompt indicando que requieres un storyboard secuencial basado en el personaje de referencia (especificando evitar collages/grids).
6. **[2:17] Vincular líricas**: Pega los segmentos de letra correspondientes a cada escena para que el agente asocie el contenido visual al texto.
7. **[3:24] Generar**: Ejecuta la generación en FlowGPT y espera a que el agente devuelva las imágenes individuales.
8. **[3:44] Descargar e Importar**:
   * Haz clic derecho sobre la imagen generada en FlowGPT y selecciona "Guardar/Descargar".
   * Regresa a Video Builder y presiona `Import Latest Download`. La UI cargará el archivo descargado más reciente en la escena activa y avanzará automáticamente al siguiente slot del timeline.

---

## Modelos, archivos y links mencionados
* **FlowGPT local**: Ejecutado bajo el puerto de desarrollo local de ComfyUI.
* **Flex SD3.5 / Xlabs**: Modelos de difusión sugeridos en la barra de herramientas del chat para la síntesis de imagen.

---

## Advertencias, errores y trucos del autor
* **[1:53] Error de formato del Agente**: Los agentes de imagen tienden a generar collages o grids de 2x2. Debes forzar la instrucción en el prompt escribiendo explícitamente *"not a grid or collage"*.
* **[3:29] Bug de importación automática**: La monitorización directa de descargas del sistema fallaba en ciertas configuraciones. El autor añadió el botón `Import Latest Download` para solucionar este problema de forma robusta.

---

## Qué NO explica el video (huecos)
* No se detalla la instalación ni la configuración del backend de FlowGPT en el ecosistema ComfyUI.
* No se especifica la plantilla exacta de instrucciones de sistema (*system prompts*) del agente para lograr que mantenga consistencia de personajes de manera nativa.
