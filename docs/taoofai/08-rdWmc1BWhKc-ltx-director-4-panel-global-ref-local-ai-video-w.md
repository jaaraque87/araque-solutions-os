<!-- generado por yt-analyze 2026-07-07 10:34 | modelo gemini-3.5-flash | tokens in/out: 27653/1821 -->

# LTX Director Unified Workflow: Multi-Prompt & Global Reference - 05:01 - [URL]

## TL;DR
Presentación de una interfaz modificada para **Camera Lab** en **ComfyUI** que unifica storyboards de 4 paneles, prompts por segmento y referencias de identidad global. Permite generar videos consistentes toma a toma con control de movimiento de cámara y expresiones faciales usando **LTX-Video**.

---

## Timeline con timestamps

*   **00:00 - 00:26** Introducción cinematográfica y sketch humorístico sobre la consistencia del personaje de IA.
*   **00:27 - 00:50** Introducción del flujo de trabajo y créditos a los creadores originales (@AIdmxxtd y @WhatDreamsCost).
*   **00:51 - 01:05** Arquitectura lógica del sistema unificado (Storyboard + Tabla de Director + Referencia Global).
*   **01:06 - 01:28** Tour por la interfaz de usuario "Director" dentro de Camera Lab.
*   **01:29 - 01:55** Demostración del cortometraje de ciencia ficción generado ("The Last Organic Rose").
*   **01:56 - 03:14** Tutorial paso a paso para configurar parámetros, subir storyboards y ejecutar la generación.
*   **03:15 - 03:32** Reproducción y análisis del video final de 8 tomas generado en tiempo real.
*   **03:33 - 03:49** Explicación del backend en ComfyUI y el paso de variables mediante API.
*   **03:50 - 03:55** Instrucciones para la instalación local del repositorio.
*   **03:56 - 05:01** Ejemplos adicionales (jardín, movimientos complejos de cámara, expresiones faciales) y cierre.

---

## Configuraciones EXACTAS mostradas en pantalla

### Panel 01: Global Setup [01:07 - 02:14]
*   **Global Setup -> Global prompt** = `consistent subject identity, environment continuity, lighting, color, and visual style`
*   **Global Setup -> Global ref strength** = `0.35`
*   **Global Setup -> Dialogue audio (optional)** = Sin archivo seleccionado (*No audio uploaded*)
*   **Global Setup -> Preset** = `16:9 1280x720`
*   **Global Setup -> Scale** = `1280x720 / 100%`
*   **Global Setup -> Frame size** = `1280x720`

### Diálogo 2x2 Storyboard [02:16 - 02:51]
*   **2x2 image** = `1.png` (primer lote de 4 tomas) y `2.png` (segundo lote de 4 tomas)
*   **Batch prompts (Ejemplo de prompts por línea)**:
    *   Línea 1: `2,woman walks into futuristic greenhouse, approaches glowing white rose inside glass chamber, slow dolly in, blue volumetric lighting, clean environment, cinematic sci-fi`
    *   Línea 2: `2,woman steps in front of glass chamber, looks at white rose, continue dolly in, subtle head movement, soft breathing, clean futuristic greenhouse, cinematic lighting`
    *   Línea 3: `2,woman reaches toward white rose, fingers move close to petals, orbit right, slow hand movement, hair strands moving slightly, shallow depth of field, cosmetic sci-fi`
    *   Línea 4: `2,woman gently removes white rose, holds flower in both hands, looks down at flower, push in, slow motion, clean futuristic greenhouse, cinematic lighting`

### Panel 02: Timeline Segments (Por toma individual) [02:52 - 03:03]
*   **Local prompt** = (Heredado automáticamente del lote de prompts)
*   **Duration** = `2` (segundos por toma)
*   **Strength** = Variable por toma (rango común `0.75` a `1.0`)
*   **Seed** = `Random`

### Nodos del Backend ComfyUI [03:35]
*   **Nodo: Camera Lab multi reference loader**
    *   `width` = `512`
    *   `height` = `512`
    *   `resize_method` = `pad`
    *   `crop_compression` = `10`

---

## Flujo de trabajo paso a paso

1.  **Acceso a la herramienta [01:06]:** Abrir la suite *Camera Lab Test Bench* y hacer clic en la pestaña **Director**.
2.  **Configuración Global [01:56]:** Subir la imagen de referencia facial de la actriz (`ref.png`) en la sección *01 Global Setup*.
3.  **Ajuste de Parámetros Globales [02:04]:** Escribir el prompt de consistencia de estilo y definir el `Global ref strength` en `0.35`. Configurar la resolución de salida a `1280x720`.
4.  **Importación del Storyboard [02:15]:** Hacer clic en **2x2 Storyboard**, cargar la primera imagen de composición de 4 paneles e ingresar los prompts correspondientes separados por saltos de línea (añadiendo el prefijo `2,` para definir la duración de 2 segundos). Presionar **Add to Timeline**.
5.  **Ampliación de tomas [02:38]:** Repetir el proceso con una segunda imagen 2x2 para añadir las tomas 5 a 8 en la línea de tiempo.
6.  **Ajustes finos [02:53]:** Revisar cada segmento en el Timeline y ajustar el parámetro `Strength` individual de cada toma si es necesario para equilibrar la influencia de la imagen guía.
7.  **Renderizado [03:04]:** Hacer clic en **Queue Run** para procesar la cola de generación toma por toma.

---

## Modelos, archivos y links mencionados

*   **Flujo de LTX Director de base:** Creado por **What Dreams Cost** (@WhatDreamsCost).
*   **Concepto de Storyboard de 4 paneles:** Desarrollado por **AI代码侠土豆** (@AIdmxxtd).
*   **Código del proyecto unificado:** Repositorio local `camera-lab-director`.

---

## Requisitos de hardware/software mencionados

*   **Entorno:** Instalación local de ComfyUI.
*   **Dependencias:** Ejecutar el instalador de dependencias del proyecto (`install dependencies` mediante script/docker).
*   **Servicio:** El backend interactúa vía API con un servidor local que corre en el puerto `http://localhost:7860`.

---

## Advertencias, errores y trucos del autor

*   **Limitación de LTX Director [03:33]:** El sistema original de LTX Director no permite conectar directamente una imagen de referencia global debido a su arquitectura enfocada en el control por toma individual.
*   **Solución técnica [03:45]:** Para solucionar esto, el autor pasa la imagen de referencia global directamente a través de la capa de la API hacia el flujo de trabajo de ComfyUI.
*   **Redimensión automática [01:59]:** No es necesario pre-procesar o recortar la imagen de referencia global; el cargador integrado gestiona el padding automáticamente.

---

## Qué NO explica el video (huecos)

*   No se muestra la instalación detallada de los nodos personalizados de ComfyUI requeridos para que funcione el backend.
*   No se especifican los checkpoints de LTX-Video (ej. si utiliza la versión de precisión FP8 o FP16) ni los parámetros de muestreo (Samplers/Schedulers) internos del flujo de ComfyUI.
