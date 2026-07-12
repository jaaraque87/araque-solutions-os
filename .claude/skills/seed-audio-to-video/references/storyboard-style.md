# Estilo de lámina de storyboard (referencia canónica — formato FIJO)

Referencia visual: lámina "los dólares del vestidor" (2026-07-03, `ChatGPT Image Jul 3, 2026, 12_51_19 PM.png`). Una sola imagen vertical generada con GPT Image 2 **vía fal con `quality: "high"`** que contiene todos los paneles Y el rotulado editorial. Este formato se respeta SIEMPRE.

## Anatomía de la lámina

- **Fondo**: ivory/crema cálido (#F2EFE9 aprox), estilo hoja de presentación editorial.
- **Grilla**: 2x2 (4 beats, default) o 2x3 (6 beats, máximo absoluto — nunca más de 6). Paneles fotorrealistas con borde negro fino, márgenes generosos y consistentes.
- **Paneles**: **film stills fotográficos reales** — como fotogramas de una película en 35mm: textura de piel real, física real de lluvia/humo/vidrio, óptica real con profundidad de campo. NUNCA ilustración, render pictórico, concept art ni look CGI. Reforzar en el prompt: "ultra-photorealistic cinematic film stills, real skin texture, natural physics, no illustration, no painterly rendering". Todos los paneles comparten personaje, vestuario, locación y paleta (continuidad estricta).
- **Dirección en cada panel, no decoración**: el prompt de cada panel declara la MIRADA del personaje (hacia qué mira exactamente), la orientación del cuerpo, la acción en curso y a qué está reaccionando. Los elementos narrativos (una sombra que escapa, una piedra que entra) se describen EN MOVIMIENTO y conectados a la reacción del personaje ("his head snaps toward...", "eyes locked on..."). Un panel donde los objetos están presentes pero el personaje no interactúa con ellos es un panel fallido.
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

## La ficha StillsLab viaja al prompt (regla canónica)

Cuando corrió la etapa de dirección, **cada panel se promptea con la ficha completa de su still ancla** — no con un promedio global de adjetivos. Para GPT Image esta especificidad es LA palanca de estilo, en este orden de fuerza:

1. **Película + DP nombrados**: `in the exact photographic style of <Film> (<year>), cinematography by <DP>` — es lo que más mueve la aguja.
2. **Frame size + shot type + composición** textuales de la ficha: `high angle wide shot, right-heavy composition` / `medium close-up, centered composition`.
3. **Lighting verbatim** de la ficha: `hard top light, high contrast` / `soft side light, low contrast` — no parafrasear.
4. **Lente/cámara como carácter de imagen**: `Panavision T-Series glass` / `Zeiss Ultra Prime look` (el nombre lleva textura; no inventar "vintage lens" genérico).
5. **Paleta anclada en HEX**: `palette anchored on #7C8454 #0F0B06 #B1A697` — los 3-4 dominantes del still ancla.

Bloque por panel (validado):

```
Frame 6 (row 3 right): high angle wide shot, right-heavy composition, in the exact
photographic style of Breaking Bad S4E5 (DP Michael Slovis) — hard top light, high
contrast, pools of sodium streetlight on dark wet alley, palette anchored on
#7C8454 #0F0B06 #B1A697: the detective leans out of the shattered window, his gaze
locked DOWN the street where a backlit silhouette sprints away under a gas lamp...
```

Antipatrón (lo que produce "período genérico" y desperdicia el research): una sola frase global tipo "desaturated palette, practical lighting, vintage lens character, 35mm grain" para toda la lámina.

**Validado con A/B** (run detective-sherlock): `storyboard_prompt_v2.txt` (promedio global) vs `storyboard_prompt_v3.txt` (ficha por panel) — la v3 produjo identidad fotográfica distinta por panel: contraste térmico real (el panel American Psycho salió azul-negro frío entre paneles ámbar), composiciones con firma (el picado right-heavy de Breaking Bad para la fuga) y HEX respetados. GPT Image sí diferencia estilos POR PANEL dentro de una misma lámina cuando cada frame lleva su bloque.

**Geometría vs. estilo cuando no coinciden**: si el still ancla tiene una geometría (frame size/shot type) distinta a la que el beat necesita, la geometría la dicta el BEAT (declarada textual igual: "low close shot over wet cobblestones") y de la ficha viajan luz, color, lente y HEX. Elegir anclas cuya geometría coincida con el beat cuando se pueda (Breaking Bad "High angle" para una fuga vista desde arriba = match perfecto).

Nota de alcance: esta regla es para **modelos de imagen** (GPT Image). En el prompt de Seedance (video) viajan película/DP nombrados, lighting y HEX — pero NO specs de cámara/lente como instrucción de movimiento (Seedance responde a ritmo, no a jerga técnica; ver seedance-prompt-template.md).

## Identidad de Paul: pack de 4 fotos + identity lock (canon 2026-07-03, run chef)

Cuando el personaje es Paul, **NO usar una sola foto**: pasar el **Paul Four-Photo Identity Pack** completo como `image_urls` (skill `paul-seedance`, `.claude/skills/paul-seedance/assets/identity-pack-normalized/REF-PAUL-*.jpg`). Con una sola referencia el parecido afloja en los planos medios/wides de la lámina.

Además, el prompt lleva un bloque IDENTITY LOCK explícito (adaptado del canon paul-seedance):

```
IDENTITY LOCK: all four reference photos show THE SAME MAN — Paul. Every frame must show this
exact man: same face shape, hazel-green eyes, heavy dark eyebrows, short natural stubble, light
skin, natural facial asymmetry, dark brown / warm chestnut hair with visible highlights — same
haircut length and volume as the references. No beauty filter, no actor makeover, no generic
handsome face — his ordinary real face, recognizable in every single frame, including the wide
shots. Treat the reference photos as identity anchors only, NOT composition locks: do not copy
their selfie framing, poses, wardrobe or backgrounds.
```

## Actuación: FACS por panel (canon 2026-07-03)

Cada panel con cara visible lleva una línea `Acting:` con dirección FACS en lenguaje compacto (skill `facs-acting-direction`): AUs con nombre anatómico + intensidad, más respiración/mandíbula/mirada/postura. Ejemplo validado (furia contenida del beat final):

```
Acting: repressed fury sliding into resignation — brows lowered and drawn AU4 at 0.7, lids
tightened AU7 at 0.6, lips sealed and compressed AU23+AU24 at 0.6, chin raised AU17 at 0.4,
nostrils flared, jaw rigid, a slow exhale through the nose, shoulders dropped in defeat.
```

Reglas: intensidades medias (0.25-0.70) salvo shock/pánico; paneles de manos/objeto sin cara se saltean; la mirada y el bloqueo corporal siguen siendo obligatorios además del FACS. Esto aplica a la LÁMINA (GPT Image); el prompt de Seedance sigue usando lenguaje de acting simple, no AUs.

## Prompt template (GPT Image 2)

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

## Submit (fal, quality high)

Con identidad de personaje (default cuando hay foto de referencia): `openai/gpt-image-2/edit` vía `fal_client`:

```python
import fal_client
# Paul => SIEMPRE el four-photo identity pack, no una sola foto
pack = ".claude/skills/paul-seedance/assets/identity-pack-normalized"
refs = [fal_client.upload_file(f"{pack}/{n}") for n in [
    "REF-PAUL-IMG_0417-normalized.jpg", "REF-PAUL-IMG_3977-normalized.jpg",
    "REF-PAUL-Yo45-normalized.jpg", "REF-PAUL-IMG_4052-2-normalized.jpg",
]]
result = fal_client.subscribe("openai/gpt-image-2/edit", arguments={
    "image_urls": refs,
    "prompt": open("<run>/storyboard/storyboard_prompt.txt").read(),
    "image_size": {"width": 1536, "height": 2048},  # custom WxH SÍ es válido; portrait_4_3 = 768x1024 (chico, paneles borrosos)
    "quality": "high",
})
```

**Tamaño (validado 2026-07-03)**: el schema fal acepta `image_size` como objeto `{width, height}` custom — el preset `portrait_4_3` rinde solo 768x1024 y cada panel de una 2x3 queda de ~350px (se ve "en mala calidad"). Canon: `{"width": 1536, "height": 2048}` con `quality: "high"`.

Sin identidad: mismo payload contra `openai/gpt-image-2` (sin `image_urls`). Guardar como `<run>/storyboard/storyboard.png` + el prompt en `storyboard_prompt.txt`.

## QA antes del gate

- Leé la imagen generada y verificá: 4 paneles, numeración correcta, continuidad de personaje/vestuario entre paneles, rotulado en español sin typos graves, y que NO haya texto flotante dentro de las fotos.
- Typos en el rotulado son el fallo más común de GPT Image 2 → si hay, regenerá o pedile el fix puntual con el mismo prompt + corrección.
