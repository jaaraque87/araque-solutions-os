<!-- generado por yt-analyze 2026-07-07 10:24 | modelo gemini-3.5-flash | tokens in/out: 31117/2439 -->

# SCAIL-2 & Bernini: Transformando Counter-Strike en un Set de Cine con IA (Camera Lab) - 05:37

## TL;DR
* Método para transformar gameplay de Counter-Strike 1.6 en metraje cinematográfico fotorrealista controlando la cámara.
* Comparación de consistencia entre los modelos de reemplazo de personajes SCAIL-2 y Bernini (WAN2.2).
* Uso de marionetas 3D en "Camera Lab" y guías de fotograma clave para estabilizar la generación de video a video (V2V).

---

## Timeline con timestamps
* **0:00 - 0:36**: Teaser cinematográfico generado con LTX2.3 y WAN2.2 simulando el mapa de de_dust2.
* **0:37 - 0:51**: Texto explicativo sobre el uso del mapa para pruebas de realización cinematográfica con IA.
* **0:52 - 1:26**: Captura de gameplay de CS 1.6 usada para obtener trayectorias de cámara y movimientos de bots.
* **1:27 - 2:00**: Explicación del problema: mantener la relación espacial cámara-personaje-entorno con control total de movimiento.
* **2:01 - 2:14**: Prueba de reemplazo de personaje usando SCAIL-2.
* **2:15 - 2:28**: Prueba de reemplazo completo (personaje, arma y escena) usando Bernini.
* **2:29 - 2:44**: Justificación del uso de CS 1.6 debido a la falta de espacio en SSD por modelos de IA locales.
* **2:45 - 3:08**: Demostración de la interfaz del software "Camera Lab" (pestañas de Motion, Edit, etc.).
* **3:09 - 3:20**: Grabación de un video guía utilizando el títere 3D en la sección Motion de Camera Lab.
* **3:21 - 3:43**: Detrás de cámaras: uso de un traje de Spandex amarillo ajustado (yin-yang) para mejorar los datos de movimiento.
* **3:44 - 4:09**: Renderizado del personaje desde el títere 3D mediante el modo RV2V de Bernini.
* **4:10 - 4:29**: Intento fallido de generación de fondo/entorno usando el modo V2V directo.
* **4:30 - 4:45**: Solución usando guías de primer y medio fotograma (First/Middle Frame Guides) en Bernini.
* **4:46 - 5:11**: Conclusiones, limitaciones actuales de rigidez y descontrol del entorno.
* **5:12 - 5:37**: Outro con escena humorística del creador en el mapa de Dust2.

---

## Configuraciones EXACTAS mostradas en pantalla

### [2:45] Interfaz "Camera Lab" - Pestaña Motion (SCAIL2 / 3D Motion Stage)
* **Left Panel (Action Library)**: Lista de animaciones predefinidas. Seleccionadas y activas:
  * `ninjajump_start` -> Start: `0.00s` | End: `1.15s` | Multiplier: `0.90` | Speed: `1`
  * `ninjajump_land` -> Start: `1.15s` | End: `2.35s` | Multiplier: `1.20` | Speed: `1`
* **Right Panel (Generate with SCAIL-2)**:
  * Reference image: `Choose` (vacío)
  * Preset dropdown = `9:16 (480x852)`
  * Size = `480x852`
  * Steps = `20`
  * Seed = `Random` (Checkbox: Activado)
  * Keep Background = (Checkbox: Desactivado)
  * Dropdown: `Motion guide used to generate results` -> Valor = `Motion guide`

### [2:51] Interfaz "Camera Lab" - Pestaña Edit (Subpestaña RV2V)
* **Experiment Dropdown** = `WAN2.2 Bernini RV2V`
* **Source video** = `01_prompt_0000_...edit.mp4`
* **Preserve audio** = (Checkbox: Desactivado)
* **Bernini Prompt** = `Replace the girl in the video with a girl dressed in student attire`
* **Reference image** = Imagen cargada de mujer con vestido negro (`ChatGPT image..._20_07.png`)
* **Reference strength** = `0.35`
* **Reference max size** = `840`
* **Long video split** = (Checkbox: Desactivado)
* **Segment duration** = `4`
* **Frame size** = `16:9 1280x720`
* **Preset** = `1280x720`
* **Scale** = `1280x720 / 100%`
* **Steps** = `30`
* **Seed** = `1584100106`
* **Negative prompt** = `bad video`

### [3:51] Interfaz "Camera Lab" - Generación RV2V (Títere 3D a Actor Real)
* **Source video** = `recorded_st.mp4`
* **Bernini Prompt** = `Replace the person in the video with the man in reference image`
* **Reference image** = Imagen de hombre en traje de Spandex amarillo con símbolo Yin-Yang (`test_suit_padding.png`)
* **Reference strength** = `0.35`
* **Reference max size** = `840`

### [4:14] Interfaz "Camera Lab" - Pestaña Edit (Subpestaña V2V - Render de Entorno)
* **Experiment Dropdown** = `WAN2.2 Bernini V2V`
* **Source video** = `01_prompt_0000...` (video previo del actor amarillo generado en el espacio vacío)
* **Bernini Prompt** = `change surrounding to a building top, the man jumped off the building`
* **Frame size** = `9:16 (512x910)`
* **Scale** = `100%`

---

## Flujo de trabajo paso a paso

1. **[0:52] Captura de Movimiento**: Jugar Counter-Strike 1.6 como espectador o "camarógrafo" para registrar movimientos de cámara libre y trayectorias reales.
2. **[2:45] Animación del Títere**: En la pestaña *Motion* de *Camera Lab*, encadenar acciones de la biblioteca (`ninjajump_start` + `ninjajump_land`) aplicadas a una marioneta virtual 3D.
3. **[3:09] Grabación de la Guía**: Pulsar `Record Take` para grabar la secuencia de movimiento del títere y generar un archivo de video guía (`recorded_v2.webm`).
4. **[3:44] Reemplazo de Personaje (RV2V)**: 
   * Transferir el video guía de la marioneta 3D al editor en modo `RV2V`.
   * Cargar la imagen de referencia del actor (en este caso, el creador en traje amarillo).
   * Ejecutar la generación para mapear la apariencia del actor sobre el esqueleto 3D en movimiento.
5. **[4:10] Generación de Escenario (V2V directo)**: Introducir el render del actor en el módulo `V2V` y mediante prompt (`change surrounding to a building top...`) generar el fondo de rascacielos. 
6. **[4:30] Estabilización mediante Keyframes (Alternativo)**: Para evitar el parpadeo y descontrol del entorno en V2V directo, generar por separado el primer y medio fotograma del títere 3D y utilizarlos como guías estáticas en el modelo Bernini.

---

## Modelos, archivos y links mencionados
* **Modelos de video**: LTX 2.3 y WAN 2.2 (usados para los clips cinematográficos del inicio).
* **Modelos de traducción/reemplazo**: 
  * `SCAIL-2` (Character Replacement).
  * `Bernini` (WAN2.2 Bernini RV2V y V2V).
* **Software**: `Camera Lab` (interfaz unificada creada por el autor que se conecta con un backend de ComfyUI).

---

## Requisitos de hardware/software mencionados
* **Hardware**: Se especifica que todos los clips se generaron de forma **local** ("GENERATED LOCALLY"), lo que requiere una GPU de nivel entusiasta con alta VRAM para WAN2.2 y LTX2.3.
* **Almacenamiento**: SSD de gran capacidad dedicado a modelos de IA local (el autor menciona no tener espacio para juegos modernos).

---

## Advertencias, errores y trucos del autor

* **[2:12] Error con SCAIL-2**: Al usar SCAIL-2, la consistencia de la vestimenta del personaje falla y cambia bruscamente a mitad del video.
* **[3:38] Truco de captura**: Vestir un traje de Spandex amarillo brillante ultra ajustado con un logo de Yin-Yang para proporcionar un contraste óptimo y "datos de movimiento más limpios" para el modelo de IA.
* **[4:05] Error de render (RV2V)**: Artefacto extraño donde la pierna derecha del actor generado se vuelve azul sin razón aparente en el render final.
* **[4:22] Advertencia sobre V2V**: El modo Video to Video (V2V) directo tiende a descontrolar por completo la consistencia de los fondos y el entorno. "Everything becomes uncontrollable when it comes to the scene".
* **[4:30] Solución/Truco para Bernini**: Darle una imagen guía estática de inicio o intermedia (First Frame / Middle Frame) para anclar la coherencia espacial del escenario y del personaje.

---

## Qué NO explica el video (huecos de información)
* No detalla cómo exportar exactamente la trayectoria de la cámara del motor GoldSource (CS 1.6) hacia el software *Camera Lab*.
* No muestra el flujo de nodos interno de ComfyUI que corre por detrás de la interfaz simplificada de *Camera Lab*.
* No se provee un enlace directo para descargar la herramienta *Camera Lab* o los pesos exactos del modelo modificado *Bernini*.
