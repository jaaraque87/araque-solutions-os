<!-- generado por yt-analyze 2026-07-07 10:33 | modelo gemini-3.5-flash | tokens in/out: 31939/1733 -->

# ¡Consistencia de Voz Realista en Videos de IA! - Camera Lab Casting System - 05:47 - https://www.youtube.com/watch?v=dQw4w9WgXcQ

## TL;DR (3 lineas)
* Presentación del nuevo módulo **Casting** en la herramienta de código abierto **Camera Lab** para lograr consistencia de voz en videos de IA.
* Utiliza un LLM local para analizar guiones, extraer diálogos y detectar emociones de forma automática.
* Integra **CosyVoice** para la generación de voces y **LTX 2.3** para la creación y sincronización del video final.

---

## Timeline con timestamps
* **00:00 - 00:07** Intro con actores reales y texto indicando que el video fue generado localmente usando LTX 2.3.
* **00:07 - 01:00** Demostración del problema de la inconsistencia de voz en personajes generados por IA.
* **01:00 - 01:24** Introducción de los presentadores y explicación de la necesidad de un sistema de "casting" de voz.
* **01:24 - 02:07** Presentación del módulo *Casting* en Camera Lab.
* **02:07 - 03:20** Demo de la interfaz de *Casting*: análisis de guion, asignación de voces/emociones y edición de audio.
* **03:20 - 03:48** Uso de los audios generados en la pestaña *Camera Lab* para crear videos sincronizados.
* **03:48 - 04:41** Integración de los clips en la pestaña *Director* usando una línea de tiempo multicanal.
* **04:41 - 05:12** Resumen técnico de la arquitectura (LLM local + CosyVoice).
* **05:12 - 05:47** Cierre, petición de suscripción y tomas falsas del personaje de IA.

---

## Configuraciones EXACTAS mostradas en pantalla

* **01:37** pestaña -> `Casting`
* **02:08** `Dialogue - Voices` -> `Script / prompt` = [Texto del guion con acotaciones]
* **02:14** `Line 01` -> `Emotion` = `angry`
* **02:14** `Line 01` -> `Speed` = `1.00x`
* **02:16** `Line 02` -> `Emotion` = `excited`
* **02:17** `Line 03` -> `Emotion` = `angry`
* **02:22** `Line 01` -> `Select voice...` = `Xiaomei (female)`
* **02:27** `Line 02` -> `Select voice...` = `Landao (male)`
* **02:30** Ventana `Add Voice` -> `Voice name` = [Campo vacío]
* **02:30** Ventana `Add Voice` -> `Reference audio` = `Choose File`
* **02:30** Ventana `Add Voice` -> `Reference text` = [Texto leído en el audio de referencia]
* **03:21** pestaña `Camera Lab` -> `Workflow` = `I2V LTX Video Cleaner`
* **03:21** pestaña `Camera Lab` -> `Resolution` = `1028x1028`
* **03:23** pestaña `Camera Lab` -> `Dialogue audio (optional for Director)` = `master_we_need_to_talk_...` (desde casting library)
* **03:48** pestaña `Director` -> Botón `2x2 Storyboard` = `ChatGPT Image...`
* **03:54** pestaña `Director` -> Ventana `Add audio clip` -> `Casting library` = `master_we_need_to_talk_4747 - xiaomei`
* **03:54** pestaña `Director` -> Ventana `Add audio clip` -> `Start` = `0` segundos

---

## Flujo de trabajo paso a paso

1. **[02:08]** Ve a la pestaña **Casting** e introduce el guion del video en el cuadro de texto de la izquierda.
2. **[02:13]** Haz clic en **Analyze** para que el LLM local procese el texto, separe los diálogos y asigne emociones automáticamente.
3. **[02:22]** Selecciona el personaje/voz correspondiente para cada línea del diálogo mediante los menús desplegables.
4. **[02:30]** (Opcional) Agrega voces personalizadas en **Add Voice** subiendo un archivo de audio de referencia y su transcripción.
5. **[02:37]** Haz clic en **Generate all** para crear los archivos de voz sintética consistentes usando CosyVoice.
6. **[03:11]** (Opcional) Ajusta los audios generados recortando silencios o ruido directamente sobre su forma de onda en la librería.
7. **[03:21]** Pasa a la pestaña **Camera Lab**, carga la imagen de origen, selecciona el audio de diálogo creado y ejecuta la cola de generación para el video (I2V).
8. **[03:48]** En la pestaña **Director**, importa tu storyboard, coloca los videos generados en la línea de tiempo y arrastra los clips de audio correspondientes debajo de cada escena para sincronizarlos.

---

## Modelos, archivos y links mencionados

* **Camera Lab**: Herramienta de automatización y control de video basada en ComfyUI (Open-source).
* **CosyVoice**: Modelo empleado para la generación y clonación de voz realista.
* **gpt-oss-20b**: LLM local ligero utilizado para el análisis y etiquetado de los guiones.
* **LTX 2.3 / WAN**: Modelos de generación de video de código abierto soportados en el ecosistema.

---

## Requisitos de hardware/software mencionados

* Servidor o PC local con soporte para **ComfyUI**.
* Entorno de ejecución para **CosyVoice** (requiere una instalación compleja de dependencias de Python).
* **Docker** (mencionado como opción recomendada si el autor publica el contenedor empaquetado).

---

## Advertencias, errores y trucos del autor

* **[01:16]** *"La consistencia de voz es algo que no notas cuando funciona, pero en cuanto falla, la ilusión se rompe por completo."*
* **[03:11]** Truco: Puedes recortar los silencios incómodos y el ruido de fondo directamente en el editor de ondas de la librería de voces para evitar problemas de sincronización en el video final.
* **[04:57]** Advertencia: La configuración del entorno de CosyVoice es bastante compleja. El autor se ofrece a crear un contenedor Docker si la comunidad muestra suficiente interés en los comentarios.

---

## Qué NO explica el video (huecos)

* No se muestra detalladamente el proceso de instalación manual de CosyVoice ni sus requisitos de VRAM específicos.
* No detalla las instrucciones de instalación del LLM local ni la configuración del API link en Camera Lab.
* Se omiten los parámetros finos de generación de LTX 2.3 (como pasos de muestreo o CFG scale) utilizados para lograr el fotorrealismo de las escenas de los presentadores.
