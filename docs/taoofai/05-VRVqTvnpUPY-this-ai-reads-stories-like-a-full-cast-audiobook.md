<!-- generado por yt-analyze 2026-07-07 10:31 | modelo gemini-3.5-flash | tokens in/out: 33764/1907 -->

# The Storykeeper - AI-powered Audiobook Generator - 06:08 - [URL del Video]

## TL;DR
* **Storykeeper** es una herramienta local de generación de audiolibros que utiliza LLMs para segmentar texto, identificar personajes y asignar tonos de voz emocionales automáticamente.
* Permite flujos híbridos importando análisis JSON desde LLMs externos (como Claude o ChatGPT) y soporta clonación de voz instantánea.
* Ofrece edición granular de segmentos con regeneración selectiva de filas modificadas ("dirty rows") y exportación final a MP3.

---

## Timeline con timestamps
* **00:00 - 01:03** | Intro cinematográfica generada con LTX 2.3 que presenta la máquina "Storykeeper" y los personajes tipo (Narrator, Young Girl, Warrior, Dragon, Detective).
* **01:03 - 01:21** | Explicación conceptual del autor sobre la automatización del reparto de voces mediante IA basada en emociones del relato.
* **01:21 - 02:15** | Flujo básico de generación de audiolibros en 3 pasos (pegar texto, analizar, generar y combinar).
* **02:15 - 03:02** | Biblioteca de voces y flujo alternativo "Prompt & copy" usando LLMs externos mediante importación de JSON estructurado.
* **03:02 - 03:28** | Clonación de voz (grabación/carga de audio) y demostración de edición de líneas con regeneración de "dirty rows".
* **03:28 - 06:08** | Audiolibro completo de demostración ilustrado en formato steampunk: "The Empty Book".

---

## Configuraciones EXACTAS mostradas en pantalla

### Interfaz WebUI (Storykeeper)

* **Voice Library (Panel izquierdo)**
  * Listado de voces disponibles con botón de reproducción:
    * `Narrator Nick`
    * `Lily`
    * `Raven`
    * `Mai`
    * `Ryle`
    * `Brutus`
    * `Pixie`
    * `Nara Joy`
    * `Casey`
    * `Ember`
    * `Oliver`
    * `Serena`

* **Story Test (Panel central superior)**
  * Caja de texto: `Input de texto del relato`
  * Botones:
    * `Prompt & copy`
    * `Analyze and split` (Botón verde)

* **Cast (Mapeo de Elenco - 01:47)**
  * `Narrator` = `Narrator Nick`
  * `Skill` = `Raven`
  * `Arthur` = `Ryle`
  * `Emily` = `Brutus`
  * `Every` = `Casey`
  * `Neither` = `Oliver`
  * `Then` = `Lily`
  * `Once` = `Mist`
  * Dropdown: `New character` -> Seleccionado: `Narrator Nick`
  * Botón: `Add character`

* **Segment Workbench (Editor de filas - 01:45 / 03:02)**
  * Estructura de fila de edición:
    * **ID fila**: `#01`
    * **Estado**: `Fresh` (verde) / `dirty` (rojo) / `done` (verde oliva)
    * **Texto**: Campo editable con la frase correspondiente.
    * **Character**: `Narrator` (Dropdown)
    * **Voice**: `Narrator Nick` (Dropdown)
    * **Tone**: `Steady & Deep` (Dropdown - también se observa `Default`, `Tense & Hurried`, `Gentle & Warm`)
    * **Speed**: `1.00x` (Deslizador horizontal / Slider)
    * **Controles**: Botones de acción rápida: `Regenerate`, `Preview` (verde), `Delete`, `Insert`

* **Import LLM JSON (Panel derecho superior - 02:53)**
  * Campo de texto con formato JSON de entrada.
  * Botón: `Import segments`

* **Upload Custom Voice (Panel derecho medio - 03:03)**
  * Input text: `Name`
  * Input text: `Reference text`
  * File Input: `Audio file` -> Botón `Choose File`
  * Botones: `Record` (Rojo), `Upload` (Verde)

* **Batch Generation (Panel derecho inferior - 01:50 / 03:15)**
  * Botones:
    * `Generate dirty rows`
    * `Generate all` (Verde)

* **Merge Output (Panel derecho inferior extremo - 02:00)**
  * Botones:
    * `Merge to MP3` (Verde)
    * `Download MP3` (Verde tras renderizar)
  * Reproductor de audio integrado con barra de progreso y volumen.

---

## Flujo de trabajo paso a paso

### Método 1: Procesamiento Local Directo (01:21)
1. Pegue el texto del manuscrito/guion en el área **Story Test**.
2. Presione **Analyze and split**. La herramienta procesará el texto, dividirá los diálogos por oraciones, asignará los personajes al **Cast** y deducirá los tonos y emociones de cada frase.
3. Ajuste los tonos (`Tone`), personajes (`Character`) o la velocidad (`Speed`) de forma manual en la tabla del **Segment Workbench** si es necesario.
4. Haga clic en **Generate all** dentro del panel **Batch Generation**. Espere a que la barra de progreso complete el renderizado de voz de todos los segmentos.
5. Presione **Merge to MP3** en la sección **Merge Output**.
6. Haga clic en **Download MP3** para exportar el audiolibro terminado.

### Método 2: Procesamiento Híbrido (Sin LLM local - 02:40)
1. Pegue su texto en el área **Story Test**.
2. Haga clic en **Prompt & copy**. Esto copiará instrucciones optimizadas de análisis de personajes y formato en su portapapeles.
3. Pegue las instrucciones en un servicio de LLM externo (como Claude o ChatGPT).
4. Copie la respuesta estructurada en formato JSON generada por la IA externa.
5. Pegue dicho JSON en la sección **Import LLM JSON** de Storykeeper y pulse **Import segments**.
6. Proceda con la generación y fusión del audio de la misma forma que en el Método 1.

---

## Modelos, archivos y links mencionados
* **Generación de Vídeo**: LTX 2.3 (utilizado para generar los clips fotorrealistas de la introducción).
* **Inspiración**: Proyecto *Camera Lab* (mencionado por el autor al inicio de la explicación técnica).
* **Código de la Herramienta**: El autor indica que el código fuente de la aplicación ("my workshop") está disponible públicamente (el enlace se encuentra en la descripción del video original).

---

## Requisitos de hardware/software mencionados
* Sistema operativo local capaz de ejecutar la WebUI de Storykeeper.
* Opcional: Un modelo de lenguaje (LLM) configurado localmente para el proceso de análisis de texto nativo. En su defecto, se requiere acceso a un chat de IA externa (ChatGPT/Claude) para el análisis vía JSON.

---

## Advertencias, errores y trucos del autor
* **Evitar explicaciones del LLM (02:46)**: El prompt copiado exige estrictamente que la IA externa responda únicamente con código JSON puro (`Return JSON only. No markdown, no explanation`), ya que cualquier texto adicional romperá la importación en la WebUI.
* **Optimización de tiempos ("Dirty Rows") (03:07)**: Si edita el texto o la voz de un segmento específico, este cambiará automáticamente de estado a `dirty`. Utilice la función **Generate dirty rows** en lugar de generar todo de nuevo para ahorrar tiempo de cómputo y API.

---

## Qué NO explica el video (huecos de información)
* No se detalla qué motor de síntesis de voz (TTS) o modelo de clonación de voz específico (como XTTSv2 o Bark) ejecuta Storykeeper por debajo.
* No se explican los requisitos previos de software (Python, dependencias de CUDA, librerías del sistema) necesarios para desplegar y ejecutar el backend localmente.
