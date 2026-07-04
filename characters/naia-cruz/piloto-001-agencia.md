# PILOTO 001 — Reel agencia (formato DIARIO)

Audio master YA GENERADO (2026-07-04, eleven_multilingual_v2, 23.9s): `naia-piloto-001-audio-master.mp3` (está en Downloads del PC original — copiarlo junto con el .env; regenerable con el body de abajo por ~310 créditos).

## Guion segmentado (el audio contiene TODO seguido)

| SEG | Frase | Tipo | ~dur |
|---|---|---|---|
| 1 | "Este video no lo grabó nadie. Y aun así, vende más que tu último anuncio." | AVATAR lipsync | 6s |
| 2 | "Sin cámara, sin actores, sin estudio... solo inteligencia artificial bien usada." | B-ROLL (voz encima) | 5s |
| 3 | "Tu negocio puede tener treinta videos así cada mes, por menos de lo que cuesta un solo creador de contenido." | AVATAR lipsync | 8s |
| 4 | "Escríbeme UGC al DM, y te muestro cómo." | AVATAR CTA | 4s |

Cortar el audio por frases: `ffprobe`/Whisper local da los timestamps exactos (`node <HYPERFRAMES_CLI> transcribe -m small -l es --json audio.mp3`).

**✅ YA CORTADO (2026-07-04)** — carpeta `Downloads\naia-piloto-001\` (llevar por WhatsApp):
- `seg1-hook-avatar.mp3` 4.20s · `seg2-broll-voz.mp3` 4.38s · `seg3-prueba-avatar.mp3` 5.37s · `seg4-cta-avatar.mp3` 9.92s · `audio-master.mp3` 23.87s
- Cortes exactos usados: 0→4.20 → 8.58 → 13.95 → fin
- seg4 tiene 2 pausas dramáticas (en ~5.7s y ~8.4s internos): el prompt LTX del SEG 4 ya incluye acting beats en esas pausas — Naia sostiene la mirada, NO debe quedar estática
- Duración de cada clip LTX = duración de su mp3 + 0.3s

## Imágenes GPT (generar en ChatGPT Plus con el character sheet adjunto)

⚠ Subir SIEMPRE el character sheet como imagen de referencia + este texto. Specs del sheet: identidad facial exacta, bob negro, ojos verde oliva, piel pale olive textura real, silueta curvy natural, lentes 35/50mm, luz golden hour o soft indoor luxury, evitar piel plástica.

**IMG-A (SEG 1 y 4 — hook y CTA, mismo setup):**
```
UGC-style photo, vertical 9:16 portrait, shot on iPhone, waist-up framing. Use the attached character sheet for exact facial identity: young woman mid-twenties, short sleek black bob, hazel green eyes, pale warm olive skin, curvy hourglass figure, gold "N" initial necklace. Wearing a fitted black tank top and high-waist beige trousers, confident posture, talking to camera mid-gesture with one hand slightly raised. Modern bright home office / creative studio background, laptop and ring light visible but blurred, organic lived-in space, asymmetrical composition. Soft indoor luxury light, bright even exposure, natural skin texture with visible pores, authentic UGC feel, 35mm look. No plastic skin, no text.
```

**IMG-B (SEG 3 — prueba, cambio de toma):**
```
Same woman from the attached character sheet (exact same face, short black bob, hazel green eyes, gold "N" necklace), UGC-style photo, vertical 9:16, medium close-up from chest up. Now sitting on a stool slightly angled to camera, wearing the same fitted black tank top, leaning slightly forward mid-conversation, warm confident half-smile. Same bright creative studio, softly blurred. Golden hour window light from the side, natural skin texture, authentic UGC feel, 50mm look. No plastic skin, no text.
```

**IMG-C (SEG 2 — b-roll, sin Naia):**
```
UGC-style photo, vertical 9:16. A smartphone on a small tripod recording nothing — empty chair in front of it — in a bright modern studio corner, ring light on, laptop open showing a video editing timeline, coffee cup. Nobody in the scene. Soft daylight, shallow depth of field, authentic behind-the-scenes feel. No text, no logos.
```
(La idea visual: "nadie lo grabó" — el set VACÍO. Refuerza el hook.)

## Prompts LTX Director (uno por segmento, con su trozo de audio)

> ⚠ QA 2026-07-04: las imágenes generadas (IMG-A y B) salieron estilo SELFIE con brazo extendido — los prompts de abajo ya están ajustados a "selfie handheld" para que el movimiento coincida con la imagen (un tripod locked-off contradiría el brazo extendido y genera artefactos). IMG-C validada: set vacío perfecto.

**SEG 1 (IMG-A + audio frase 1):**
```
Shot on iPhone 16 Pro Max, 4K Cinematic mode, Apple ProRes LOG. Vertical frame, selfie video, close-up portrait, face in upper third. A young woman in her mid-twenties, short sleek black bob hair, hazel green eyes, pale warm olive skin, curvy hourglass figure, gold "N" initial necklace, wearing a fitted black tank top and beige high-waist trousers. She holds the camera with one extended arm in authentic selfie style, standing in a bright modern creative studio with a ring light and laptop blurred behind. She speaks directly to camera with her free hand gesturing naturally, confident direct energy. Speaking in Latin American Spanish with a confident, slightly playful tone. "Este video no lo grabó nadie. Y aun así, vende más que tu último anuncio." Subtle handheld selfie movement, natural micro-shake, camera stays on her face. 24mm selfie lens equivalent, f/2.2. Smart HDR 4, bright even exposure, natural warm skin tones, skin pores visible. Her lips move clearly matching the audio. She raises one eyebrow slightly at the end with a knowing half-smile. Vertical 9:16 format.
```

**SEG 2 (IMG-C + audio frase 2, SIN lipsync):**
```
Shot on iPhone 16 Pro Max, vertical frame 9:16. An empty creative studio corner: a smartphone on a small tripod, ring light glowing, empty chair, laptop showing a video editing timeline. The camera very slowly pushes in toward the phone on the tripod, subtle handheld feel. Soft daylight, shallow depth of field, authentic behind-the-scenes atmosphere. No people, no text.
```

**SEG 3 (IMG-B + audio frase 3):**
```
Shot on iPhone 16 Pro Max, 4K Cinematic mode. Vertical frame, selfie video, medium close-up from chest up. The same young woman, short sleek black bob hair, hazel green eyes, pale warm olive skin, gold "N" initial necklace, fitted black tank top, holding the camera with one extended arm in selfie style, warm golden hour window light in a bright studio. She speaks directly to camera, leaning slightly forward, warm confident energy, her free hand gesturing subtly. Speaking in Latin American Spanish with a confident tone. "Tu negocio puede tener treinta videos así cada mes, por menos de lo que cuesta un solo creador de contenido." She pauses briefly mid-sentence, nods once, then continues. Subtle handheld selfie movement, camera stays on her face. 24mm selfie lens equivalent, f/2.2. Natural skin tones, pores visible. Her lips move clearly matching the audio. Vertical 9:16.
```

**SEG 4 (IMG-A + audio frase 4):**
```
Shot on iPhone 16 Pro Max, 4K Cinematic mode. Vertical frame, selfie video, close-up portrait, face in upper third. The same young woman, short sleek black bob, hazel green eyes, gold "N" necklace, fitted black tank top, holding the camera with one extended arm in selfie style in the bright creative studio. She looks directly into the lens with calm confidence and says in Latin American Spanish, warm direct tone: "Escríbeme UGC al DM, y te muestro cómo." She points once gently toward the camera lens with her free hand on "DM". After speaking she pauses, holding a warm direct gaze at the lens with a slow confident smile forming, tilts her head very slightly, then finishes the last word with a knowing look. Subtle handheld selfie movement. 24mm selfie lens equivalent, f/2.2. Natural skin texture. Her lips move clearly matching the audio, staying naturally still and expressive during the pauses. Vertical 9:16.
```

**Negativos (todos los segmentos):**
```
no extra limbs, no face warp, no object duplication, no text artifacts, no watermark, no flicker, no camera shake, no multiple people
```

## Paso a paso ComfyDeploy / ComfyUI (LTX Director manual)

1. Cortar el audio master en 4 trozos por frase (timestamps de Whisper): `ffmpeg -i master.mp3 -ss <ini> -to <fin> -c copy segN.mp3`
2. En el workflow **LTX23 AllInOne Director v30**: cargar IMG del segmento como first frame (modo I2V), cargar `segN.mp3` en el input de audio (LTXVAudioVAE), pegar el prompt del segmento, negativos, **CFG 1.2**, 30fps, 576×1024, duración = duración del trozo de audio +0.3s.
3. SEG 2 (b-roll): sin audio input, duración fija 5s.
4. Generar → guardar como `seg1.mp4` ... `seg4.mp4`. Si un seg sale mal: cambiar SOLO el seed.
5. Ensamblar (cualquier PC con el repo):
```bash
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\nfile 'seg3.mp4'\nfile 'seg4.mp4'\n" > lista.txt
ffmpeg -f concat -safe 0 -i lista.txt -c:v libx264 -r 30 -pix_fmt yuv420p -an mudo.mp4
ffmpeg -i mudo.mp4 -i naia-piloto-001-audio-master.mp3 -c:v copy -c:a aac -shortest full.mp4
node tools/content-reel-lab/scripts/render-batch.mjs --jobs <jobs con full.mp4>   # o el unitario
```
Overlay del piloto: hook "nadie grabó este video" · CTA "Escríbeme UGC al DM" · @araquesolutions

## Regenerar el audio (cualquier PC, ~310 créditos)
POST `https://api.elevenlabs.io/v1/text-to-speech/rzpLrJDiI1CBeAvkbjNf` con el guion completo, model `eleven_multilingual_v2`, voice_settings {stability:0.45, similarity_boost:0.8, style:0.35}. Key en `.env`.
