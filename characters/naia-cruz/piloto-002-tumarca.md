# PILOTO 002 — "TU MARCA AQUÍ" (formato DIARIO, producto UGC)

**Concepto:** spec ad de una bebida refrescante GENÉRICA en lata que dice "TU MARCA AQUÍ". Naia actúa un anuncio UGC creíble durante 10s → reveal: la marca no existe → CTA a dueños de negocio. La pieza es demo y pitch a la vez: quien la ve entiende "ahí podría ir mi producto". Sin marcas reales.

**Hipótesis del scorecard (ANTES de publicar):** el fake-out anuncio-real + reveal "tu marca aquí" retiene mejor que el pitch directo del piloto 001 — prueba de la fórmula 6 del swipe ("nadie notó que es IA", hipótesis sin dato). Métrica objetivo: retención >50% en el reveal (~s10) y ≥1 DM con palabra "MARCA".

## Hook variants (skill guion-ugc)

| id | Línea hablada | Visual frame 1 | Ángulo | Estado |
|---|---|---|---|---|
| A | "La probé hace una semana y no he vuelto a tomar otra cosa." | Naia selfie con la lata (texto visible), overlay contradice el audio | fake-out + curiosity gap texto-vs-audio | **SELECCIONADO** |
| — | Batería completa de 10 hooks demo-puro (sin reveal) en `tools/hook-lab/clients/cola-light-generica/hooks.json` — h01 "light no es castigo" (score 10) aporta el remate de la frase 1 | | producto/sensorial | fuente |
| B | "Esta bebida no existe. Y este anuncio igual te dio ganas de probarla." | Igual, reveal inmediato | contrarian directo | reserva |
| C | "—¿Y esa bebida? —No existe. Ese es el punto." | in-media-res, alguien pregunta off-camera | diálogo (patrón 700K del radar) | reserva |

**Por qué A:** el overlay "este anuncio no existe" sobre un anuncio que se ve 100% real crea el gap en 0-2s (el que lee para, el que no lee cae en el fake-out). B quema el reveal en el segundo 1; C necesita segunda voz.

## Guion segmentado (~60 palabras, ~20s, 3 wps)

| SEG | Frase | Tipo | ~dur |
|---|---|---|---|
| 1 | "La probé hace una semana y no he vuelto a tomar otra cosa. Refresca... y no sabe a castigo." | AVATAR lipsync (con lata) | 6.3s |
| 2 | "Se ve bien, se antoja... un anuncio como cualquier otro, ¿no?" | B-ROLL lata hero (voz encima) | 3.7s |
| 3 | "Mira la lata otra vez: dice tu marca aquí. Esta bebida no existe. Tu producto sí." | AVATAR lipsync (reveal, lata al lente) | 5.7s |
| 4 | "Escríbeme MARCA al DM y te muestro tu producto en un anuncio así." | AVATAR CTA | 4.3s |

CTA keyword **"MARCA"** (piloto 001 usó "UGC") → atribución por reel en los DMs.

**Overlays:** hook `este anuncio no existe` · CTA `Escríbeme MARCA al DM` · @araquesolutions. Nunca sobre el rostro (plantilla cara-libre).

## Audio master — ✅ GENERADO Y CORTADO (2026-07-04)

**Modelo definitivo: `eleven_v3` + audio tags** (`[upbeat]`, `[soft laugh]`, `[casual]`, `[playful]`, `[warm]` — settings stability 0.5 / similarity 0.8). QA del usuario: multilingual_v2 con los settings del piloto 001 "no suena natural UGC" (locutora leyendo, pausas casi nulas, 3.7 wps). v3 salió 19.6s, 3.2 wps, pausas naturales de ~0.4s en cada corte → sin post-proceso.

Carpeta `Downloads\naia-piloto-002\` (respaldar por WhatsApp): **`audio-master-final.mp3` 19.6s** (= v3 tal cual, ESTE se pega al video final) · `seg1-hook-avatar.mp3` 5.80s · `seg2-broll-voz.mp3` 3.79s · `seg3-reveal-avatar.mp3` 6.14s · `seg4-cta-avatar.mp3` 3.78s · `alignment-v3.json`.
Cortes exactos (alignment): 0→5.793 → 9.571 → 15.702 → fin.
⚠ Lecciones: (1) usar SIEMPRE el endpoint **with-timestamps**: mismo costo, valida completitud (la 1ª generación por stream llegó TRUNCADA con el CTA a medias) y da los cortes por carácter — Whisper ya no hace falta para esto; (2) los tags v3 van en el texto pero NO se hablan — el texto hablado queda idéntico al que citan los prompts LTX.

## Regenerar el audio (si hiciera falta)

POST `https://api.elevenlabs.io/v1/text-to-speech/rzpLrJDiI1CBeAvkbjNf/with-timestamps`, model `eleven_v3`, voice_settings {stability:0.5, similarity_boost:0.8}, con los audio tags del texto de arriba. Guion completo (~400 chars ≈ 400 créditos):

> La probé hace una semana y no he vuelto a tomar otra cosa. Refresca... y no sabe a castigo. Se ve bien, se antoja... un anuncio como cualquier otro, ¿no? Mira la lata otra vez: dice tu marca aquí. Esta bebida no existe. Tu producto sí. Escríbeme MARCA al DM y te muestro tu producto en un anuncio así.

Nota de intención para el tono: SEG 1-2 en registro "anuncio UGC creíble" (entusiasta natural), SEG 3 baja a confidencia (el reveal), SEG 4 directo cálido. Cortar por frases con Whisper → duración clip LTX = mp3 + 0.3s.

## DISEÑO DE LA LATA (consistencia entre las 3 imágenes)

Describir SIEMPRE igual en los 3 prompts: `sleek matte white aluminum can with a soft teal-to-mint gradient band, bold clean dark sans-serif text "TU MARCA AQUÍ" printed large on the front, small generic droplet icon above the text, condensation droplets on the can`. ⚠ El texto en lata es el punto frágil: GPT Image 2 lo escribe bien en texto corto; LTX puede degradarlo al animar → lata quieta en mano (sin sorbos, sin agitarla), y la legibilidad la garantiza el hero del SEG 2. Si en el clip avatar el texto sale ilegible pero la lata se ve bien, ES ACEPTABLE (el hero + overlay hacen el trabajo).

## Imágenes GPT (ChatGPT Plus + character sheet adjunto)

**IMG-A (SEG 1 y 4 — selfie con lata):**
```
UGC-style photo, vertical 9:16 portrait, shot on iPhone, waist-up selfie framing with one extended arm. Use the attached character sheet for exact facial identity: young woman mid-twenties, short sleek black bob, hazel green eyes, pale warm olive skin, curvy hourglass figure, gold "N" initial necklace. Wearing a fitted ribbed white tank top and light denim, fresh casual look. In her free hand she holds up a sleek matte white aluminum can with a soft teal-to-mint gradient band, bold clean dark sans-serif text "TU MARCA AQUÍ" printed large on the front, small droplet icon above the text, condensation droplets on the can, held at chest height with the label facing the camera. Bright modern kitchen / sunny apartment background, softly blurred, organic lived-in space. Natural daylight, bright even exposure, natural skin texture with visible pores, authentic UGC feel, 24mm selfie look. No plastic skin, no extra text anywhere except on the can.
```

**IMG-B (SEG 3 — reveal, lata hacia el lente):**
```
Same woman from the attached character sheet (exact same face, short black bob, hazel green eyes, gold "N" necklace, fitted ribbed white tank top), UGC-style selfie photo, vertical 9:16, medium close-up. Now she tilts the same matte white aluminum can toward the camera lens so the label "TU MARCA AQUÍ" fills the lower third of the frame, sharp and legible, her face above it with a knowing half-smile, eyebrows slightly raised. Same bright kitchen background softly blurred. Natural daylight, natural skin texture, authentic UGC feel. No plastic skin, no extra text except on the can.
```

**IMG-C (SEG 2 — hero de producto, sin Naia):**
```
UGC-style product photo, vertical 9:16. A sleek matte white aluminum can with a soft teal-to-mint gradient band and bold clean dark sans-serif text "TU MARCA AQUÍ" printed large on the front, small droplet icon above the text, standing on a rustic wooden table with ice cubes scattered around, heavy condensation droplets running down the can, a slice of lime beside it. Bright natural window light, shallow depth of field, fresh summery feel, label perfectly sharp and facing camera. Nobody in the scene. No extra text, no logos.
```

## Prompts LTX Director (selfie handheld, canon QA del piloto 001)

**SEG 1 (IMG-A + audio frase 1):**
```
Shot on iPhone 16 Pro Max, 4K Cinematic mode, Apple ProRes LOG. Vertical frame, selfie video, close-up portrait, face in upper third. A young woman in her mid-twenties, short sleek black bob hair, hazel green eyes, pale warm olive skin, curvy hourglass figure, gold "N" initial necklace, wearing a fitted ribbed white tank top. She holds the camera with one extended arm in authentic selfie style, in a bright modern kitchen softly blurred behind. In her free hand she holds up a matte white aluminum can with a teal gradient band and the text "TU MARCA AQUÍ", keeping it steady at chest height, label toward the camera. She speaks directly to camera with fresh enthusiastic energy, like recommending a product she loves. Speaking in Latin American Spanish with a warm, genuine tone. "La probé hace una semana y no he vuelto a tomar otra cosa. Refresca... y no sabe a castigo." She glances at the can once with a small smile, then back to the lens. Subtle handheld selfie movement, natural micro-shake. 24mm selfie lens equivalent, f/2.2. Smart HDR 4, bright even exposure, natural warm skin tones, skin pores visible. Her lips move clearly matching the audio. The can stays steady, its label stable and unchanged. Vertical 9:16 format.
```

**SEG 2 (IMG-C + audio frase 2, SIN lipsync, duración fija 4s):**
```
Shot on iPhone 16 Pro Max, vertical frame 9:16. Product hero shot: a matte white aluminum can with a teal gradient band and the text "TU MARCA AQUÍ" standing on a rustic wooden table with ice cubes and a lime slice, heavy condensation on the can. The camera very slowly pushes in toward the can, subtle handheld feel. A single condensation drop slides slowly down the can. Bright natural window light, shallow depth of field, fresh summery atmosphere. The text on the can stays perfectly legible, static and unchanged. No people, no extra text.
```

**SEG 3 (IMG-B + audio frase 3):**
```
Shot on iPhone 16 Pro Max, 4K Cinematic mode. Vertical frame, selfie video, medium close-up. The same young woman, short sleek black bob hair, hazel green eyes, pale warm olive skin, gold "N" initial necklace, fitted ribbed white tank top, holding the camera with one extended arm in selfie style in the bright kitchen. She holds the can tilted toward the lens in her free hand, label visible, then looks into the camera with a knowing, conspiratorial half-smile, her energy shifting from ad-mode to honest confession. Speaking in Latin American Spanish with a confident, slightly amused tone. "Mira la lata otra vez: dice tu marca aquí. Esta bebida no existe. Tu producto sí." She taps the label once gently with her thumb on "tu marca aquí", then lowers the can slightly. Subtle handheld selfie movement, camera stays on her face. 24mm selfie lens equivalent, f/2.2. Natural skin tones, pores visible. Her lips move clearly matching the audio. The can label stays stable and unchanged. Vertical 9:16.
```

**SEG 4 (IMG-A + audio frase 4):**
```
Shot on iPhone 16 Pro Max, 4K Cinematic mode. Vertical frame, selfie video, close-up portrait, face in upper third. The same young woman, short sleek black bob, hazel green eyes, gold "N" necklace, fitted ribbed white tank top, holding the camera with one extended arm in selfie style in the bright modern kitchen, the can now resting lower near her waist. She looks directly into the lens with calm confidence and says in Latin American Spanish, warm direct tone: "Escríbeme MARCA al DM y te muestro tu producto en un anuncio así." She points once gently toward the camera lens with her free hand on "DM". After speaking she holds a warm direct gaze with a slow confident smile. Subtle handheld selfie movement. 24mm selfie lens equivalent, f/2.2. Natural skin texture. Her lips move clearly matching the audio. Vertical 9:16.
```

**Negativos (todos):**
```
no extra limbs, no face warp, no object duplication, no text artifacts, no warped letters on the can, no watermark, no flicker, no camera shake, no multiple people
```

## Parámetros ComfyDeploy LTX Director v30 (idénticos al piloto)

Imagen del seg como first frame (I2V) + su mp3 en LTXVAudioVAE + prompt + negativos · **CFG 1.2** · 30fps (o 25) · 576×1024+ · duración = mp3 + 0.3s → **SEG1 6.1s · SEG2 4.1s (sin audio input) · SEG3 6.4s · SEG4 4.1s**. Si un seg falla: cambiar SOLO el seed.

## Ensamblaje

```bash
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\nfile 'seg3.mp4'\nfile 'seg4.mp4'\n" > lista.txt
ffmpeg -f concat -safe 0 -i lista.txt -c:v libx264 -r 30 -pix_fmt yuv420p -an mudo.mp4
ffmpeg -i mudo.mp4 -i audio-master-final.mp3 -c:v copy -c:a aac -shortest full.mp4
node tools/content-reel-lab/scripts/render-ltx-avatar-original-audio.mjs --video full.mp4 --hook "este anuncio no existe" --cta "Escríbeme MARCA al DM"
```

## Caption al publicar (framing spec/concepto)

Concepto propio — la marca de la lata no existe (por eso dice lo que dice 😉). Anuncio completo producido por @araquesolutions sin cámara, sin actores, sin estudio. ¿Lo quieres con TU producto? Escríbeme MARCA al DM. #contenidoparanegocios #marketingdigital
