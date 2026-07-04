---
name: omni-edit
description: OMNI EDIT — sistema de estilos propios para edición generativa de clips con Gemini Omni Flash vía API directa de Google (réplica del Shorts Maker de Higgsfield, sin sus créditos). Mantiene una librería de estilos preconfigurados en styles/ y aplica UN estilo elegido de forma CONSISTENTE a una serie de clips (batch), o crea/copia estilos nuevos desde videos/imágenes de referencia. Usar SIEMPRE que Paul diga "omni edit", "editá estos clips con estilo X", "aplicale el estilo claymation/scribble/collage", "pasá esta serie a estilo...", "qué estilos tenemos", "creá un estilo desde este video/referencia", "copiate el estilo de este short/preset", o comparta varios clips pidiendo un look unificado. NO para dirigir un hook puntual con decisión de intensidad por contexto (eso es /omni-hook), NO para unir clips ni captions del pipeline (HyperFrames), NO para generar video desde cero.
---

# OMNI EDIT

Shorts Maker propio: una librería de **estilos** versionada en esta skill + Gemini Omni
Flash vía API directa (`/gemini-omni-flash-api`, venv `~/.venvs/omni-flash`, key en env).
Sin créditos de terceros, con Interaction IDs guardados para iterar turn-by-turn.

Dos flujos: **aplicar** un estilo a una serie de clips, y **crear/copiar** un estilo nuevo.

## La librería

`styles/<slug>/style.md` (+ `refs/` con stills opcionales). Índice rápido en
`styles/INDEX.md`; para listar: `ls .claude/skills/omni-edit/styles/`.

Cada `style.md` define: el mundo (material/tema), el **bloque de estilo en inglés** que se
inserta en el prompt, el formato de captions del estilo, la regla de doodads, la paleta de
estados de fondo, y su QA específico. El estilo es la parte FIJA del prompt; los beats,
captions y doodads de cada clip son la parte variable.

## Flujo 1 — Aplicar un estilo a una serie

1. **Elegir estilo.** Si Paul lo nombró, leer su `style.md`. Si no, listar la librería con
   una línea por estilo y recomendar uno según el contenido (educativo → marker-scribble;
   tech/producto → desktop-window; narrativo cálido → claymation; etc.).
2. **Analizar cada clip** — mismas reglas que `/omni-hook` Paso 2 (obligatorio, nunca
   saltear): ffprobe, prep ≤10s (recortar aire/apretar silencios y verificar con Whisper),
   beats word-level (`~/.venvs/fwhisper/bin/python`, faster-whisper `word_timestamps=True`),
   contact sheet visual. Los spans >0.75s traen silencio pegado al inicio.
3. **Escribir el prompt de cada clip**: esqueleto compartido (cara/lip-sync intactos
   mientras esté en cámara, voz original intacta, no music, 9:16, misma duración) +
   bloque de estilo del `style.md` + lo variable del clip.

   **⚠️ Capa de motion obligatoria (canon validado, feedback Paul 2026-07-03):** el
   prompt McDonald's maximalista es LA gramática de movimiento — los estilos aportan
   material y paleta, NO reemplazan el ritmo. Todo prompt lleva: (a) "a new background
   or insert every ~1 second"; (b) "hard cuts and zoom punch-ins on my face synced to
   emphasis"; (c) reframe inicial del sujeto (más chico/abajo) abriendo espacio para
   title cards que explotan; (d) punch words ALL-CAPS en beats de palabra (no un caption
   por frase); (e) "never let the plain talking head sit still for more than ~1 second";
   (f) beat map palabra-preciso con un evento visual por beat (title card, punch word,
   insert card, background flip, punch-in). La versión 'mundo calmo' (un estado de fondo
   por frase + caption fijo) fue rechazada: se lee estática. Cara fotográfica = prompt
   solo texto; los IMAGE_REF tiñen al sujeto.
   - estados de fondo timecodeados a los beats de FRASE medidos;
   - captions por frase **deletreados exactamente** en el prompt ("spelling exactly:
     '…'") — los presets de Higgsfield shipean typos; nuestro QA letra por letra es la
     diferencia;
   - un doodad literal por frase (frase → prop del material).
4. **Consistencia de serie** (la razón de ser de esta skill):
   - mismo mundo/material/lettering en TODOS los clips de la serie;
   - rotar la paleta de estados de fondo entre clips (mismo set de colores del estilo,
     orden distinto) para que la serie sea familia sin ser clones;
   - los doodads cambian por clip (literales a cada guion); el formato de caption no;
   - si la serie es una película (clips encadenados), la dirección de montaje manda:
     leer el DIRECTION.md del proyecto — el estilo NO reemplaza la dirección.
5. **Batch**: `generate_video.py --batch jobs.json --concurrency 3` (jobs con `video`,
   `output`, `aspect_ratio`; sin `--strip-audio`, sin `duration`). Opcional por job:
   `"image": ["styles/<slug>/refs/ref_1.jpg", ...]` con "in the style of <IMAGE_REF_0>"
   en el prompt (references-to-video; útil cuando el material es difícil de describir).
6. **QA por clip** con el checklist de `/omni-hook` (`references/qa-checklist.md` de esa
   skill) + el QA específico del estilo. Regenerar solo los fallados; guardar
   `<output>.meta.json` con interaction_id SIEMPRE. Correcciones puntuales por
   `--previous-interaction-id`.

## Flujo 2 — Crear o copiar un estilo

Input: videos/imágenes de referencia (archivo local, URL, un preset ajeno con preview
público, un short de TikTok). Proceso completo en `references/style-anatomy.md`:
bajar referencia → strip de frames → disección con el framework de 5 puntos (sujeto /
mundo / estados de fondo / captions / doodads) → escribir `styles/<slug>/style.md` +
guardar 2-4 stills en `refs/` → sumar línea a `styles/INDEX.md`. Validar el estilo nuevo
con UNA generación de prueba sobre un clip corto antes de darlo por bueno.

## Reglas heredadas (no repetir errores ya pagados)

- **El fondo de la fuente NUNCA queda visible** en modos de mundo temático: cutout del
  sujeto obligatorio ("cut me out completely — my original background must never be
  visible"). Meter el frame crudo adentro de una ventana/marco arrastra el fondo fuente
  y mata el estilo (error pagado en el demo omni-edit v1).
- **Paleta saturada y punchy por default.** Nunca escribir "muted"/"clean gray" en un
  bloque de estilo salvo pedido explícito: las referencias Shorts Maker son vibrantes
  sin excepción, y el default Morfeo también.
- **Captions GRANDES**: lettering ≥8% del alto del frame, legible en teléfono. "UI label"
  chico no es un caption de short.
- **Dinamismo mínimo**: el fondo cambia de estado por frase, los doodads laten/popean en
  su palabra, y el cutout puede hacer micro punch-in en cada arranque de frase. Un frame
  quieto por más de ~1s en modo mundo = estilo fallido.
- **Conversión de aspecto o reemplazo total del mundo ⇒ Omni REGENERA el audio** (verificado:
  correlación 0.27 vs fuente, sílabas inventadas). En estos modos el flujo es SIEMPRE:
  generar → **remux de la voz original** (`-map 0:v -map 1:a`) → verificar lip-sync contra
  el video (el timing visual suele preservarse; verificar con crops de boca a 2-3 beats).
  La preservación de audio solo es confiable en edits v2v livianos (multicám/bold sin
  cambio de aspecto).
- **Cambios de vestuario/cuerpo NUNCA en el pase inicial de restyle**: pedir "wardrobe
  change" junto con el restyle puede disparar el reemplazo COMPLETO de la persona (pagado
  en el promo: Omni puso a otro tipo). Secuencia validada: pase 1 = restyle canon con
  identidad blindada y ropa original; pase 2 = vestuario/slimming por turn-by-turn sobre
  la generación aprobada (preserva cara frame a frame).
- **Blindaje de texto en todo prompt maximalista**: "the ONLY on-screen text allowed are
  the punch words spelled above; do NOT add word-by-word subtitles; decorative cards and
  thumbnails stay completely TEXTLESS" — sin esto Omni agrega subs con typos y
  pseudo-texto en cards (apareció 'MERDA' en una card decorativa).
- **QA de identidad primero**: antes de cualquier otro check del render, confirmar que
  la persona ES la fuente. Un restyle con energía perfecta y otra cara es basura.
- Omni puede correr el audio ~0.5s en clips cortos → captions del master se miden sobre
  el render, no la fuente.
- Los gags/transiciones con <1s de ventana = cambio de estado, no movimiento lento.
- Texto diegético/captions del estilo: siempre deletreado en el prompt y verificado
  letra por letra en QA.
- Full-restyle del sujeto (ej. claymation total, sujeto de plastilina) rompe "cara
  intacta" a propósito: avisar a Paul ANTES de generar, es decisión de él.
