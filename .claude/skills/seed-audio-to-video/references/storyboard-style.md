# Estilo de lámina de storyboard (referencia canónica)

Referencia visual: lámina "los dólares del vestidor" (2026-07-03). Una sola imagen vertical 1024x1536 generada con GPT Image 2 que contiene los 4 paneles Y el rotulado editorial.

## Anatomía de la lámina

- **Fondo**: ivory/crema cálido (#F2EFE9 aprox), estilo hoja de presentación editorial.
- **Grilla**: 2x2, cuatro paneles fotorrealistas con borde negro fino. Márgenes generosos y consistentes.
- **Paneles**: fotografía realista cinematográfica — luz cálida practicable (lámparas, TV), cámara handheld, tono cotidiano creíble. Los 4 paneles comparten personaje, vestuario, locación y paleta (continuidad estricta).
- **Debajo de cada panel**: badge cuadrado negro con el número en blanco (1-4) + título corto en MAYÚSCULAS bold. En la línea siguiente: `Action:` en bold + descripción breve de lo que sucede, en una o dos líneas, sentence case.
- **Footer**: línea horizontal fina + `NOTAS:` en bold con las notas globales de estilo (luz, cámara, tono).
- **Idioma del rotulado**: español.

## Regla crítica: sin texto sobreimpreso

Dentro de las fotos NO va ningún texto flotante: ni quotes del diálogo, ni captions, ni títulos sobre la escena. Las líneas de diálogo viven solo en el rotulado `Action:` de abajo. Excepción única: texto **diegético** que pertenece físicamente a la escena (titular en una pantalla de TV, cartel en la calle) cuando la historia lo exige — y en ese caso especificá el texto exacto entre comillas para que salga legible.

## Patrón narrativo de 4 beats

1. **NORMALIDAD** — situación cotidiana, plano general que establece locación y personaje.
2. **EL GIRO** — el elemento que rompe la normalidad (frecuentemente un plano del dispositivo/detalle: TV, teléfono, puerta).
3. **REACCIÓN** — primer plano de la emoción (sorpresa, miedo, incredulidad); ojos y boca abiertos.
4. **CLÍMAX** — la acción/grito/decisión; gesto corporal grande.

## Prompt template (GPT Image 2, image_size 1024x1536)

```
A cinematic storyboard presentation sheet on a warm ivory background, portrait orientation.
A 2x2 grid of four photorealistic film frames with thin black borders, all four frames
showing the same [PERSONAJE: descripción física + vestuario exacto] in the same
[LOCACIÓN: descripción + hora/luz], warm practical lighting, handheld realistic tone,
consistent color palette across all frames.

Frame 1 (top left): [beat 1 — plano general de normalidad].
Frame 2 (top right): [beat 2 — el giro].
Frame 3 (bottom left): [beat 3 — primer plano de la reacción].
Frame 4 (bottom right): [beat 4 — clímax con gesto corporal].

Below each frame: a small black square badge with the white number (1, 2, 3, 4), followed
by a short bold uppercase title in Spanish ([TÍTULO 1], [TÍTULO 2], [TÍTULO 3], [TÍTULO 4]),
and underneath, "Action:" in bold followed by one short Spanish sentence describing the beat:
[descripciones]. At the bottom of the sheet, above a thin horizontal rule: "NOTAS:" in bold
followed by "[notas globales de luz/cámara/tono en español]".

No text overlaid inside the photographic frames. No captions, no quotes, no watermarks
inside the scenes. Editorial layout, clean typography, consistent margins.
```

Si un beat exige texto diegético: agregar dentro de la descripción del frame, p. ej. `the TV screen shows a red URGENTE banner with the white headline "LA POLICÍA BUSCA A ESTA MUJER"`.

## Submit (patrón queue fal)

Mismo patrón que `scripts/seed_audio_gen.py` pero contra `https://queue.fal.run/openai/gpt-image-2` con payload `{"prompt": ..., "image_size": "1024x1536", "num_images": 1}`. Guardar como `<run>/storyboard/storyboard.png` + el prompt en `storyboard_prompt.txt`.

## QA antes del gate

- Leé la imagen generada y verificá: 4 paneles, numeración correcta, continuidad de personaje/vestuario entre paneles, rotulado en español sin typos graves, y que NO haya texto flotante dentro de las fotos.
- Typos en el rotulado son el fallo más común de GPT Image 2 → si hay, regenerá o pedile el fix puntual con el mismo prompt + corrección.
