# Prompting Seed Audio 1.0 (estructura canónica)

Modelo: `bytedance/seed-audio-1.0` en fal — genera escenas de audio completas (diálogo multi-personaje verbatim + SFX + ambiente + música) en una pasada. Specs: $0.1875/min, MP3 24kHz, máx 2 min/pasada, prompt máx 2.048 chars. Base de conocimiento completa con hallazgos validados: `_research/seed-audio/README.md`.

Helper: `python3 scripts/seed_audio_gen.py --prompt-file prompt.txt --out out.mp3` (lee `FAL_API_KEY` de `.env`, submit + poll + descarga MP3 y JSON de metadata).

## Estructura canónica del prompt (formato guion intercalado)

El prompt es un **mini guion de audio en prosa**, no un brief con secciones etiquetadas. Patrón validado 2026-07-07 con dos ejemplos calificados "perfectos" por Paul (verbatim en la sección siguiente): párrafos cortos que alternan ambiente, diálogo dirigido y SFX puntuales, **en el orden exacto en que suenan** — el orden del texto ES el timeline. Escribilo en inglés con el diálogo en el idioma target.

### Cuerpo del guion

1. **Apertura = la escena sonora en una oración, sin voces.** Lugar + cama continua + movimiento espacial y dinámica ligada a la acción: `School bell rings from near to far, with after-school hallway ambience: distant footsteps, student chatter, locker clacks, and soft hallway reverb.` La cama no se describe estática — se le da comportamiento (`tens of thousands of fans roar throughout the background, swelling whenever the action peaks`).
2. **Diálogo línea por línea, cada línea en su propio párrafo**, con la fórmula:
   `Nombre (demografía, acento, textura de voz, personalidad) <verbo de delivery + matiz>: "línea"`
   - **Primera aparición** de cada personaje: descriptor completo — edad/género + acento + textura de voz + personalidad (`teenage male, American accent, bright youthful voice, sunny and cocky`).
   - **Líneas siguientes**: tag corto + la emoción de ESA línea. La dirección evoluciona línea a línea y dibuja el arco: `coaxing, dragging the words with a grin` → `gentler, more sincere` → `excited and triumphant`; o en voz única, escalada de intensidad: `extremely exhilarated` → `voice soaring higher, almost hoarse with excitement` → `full-throated and breathless`. Nunca la misma emoción estática en todo el guion.
   - **Verbo de delivery específico**, nunca "says" pelado: teases playfully, mutters, lowers her voice flustered, offers, shouts rapidly, stretches the word.
   - **La prosodia se escribe dentro de la línea**: vocales estiradas (`"What a goooal!"`), dudas con puntos suspensivos (`"Uh... I still haven't finished my homework."`, `"...Fine, just half a day, okay?"`).
3. **SFX como líneas `Sound effect:` intercaladas** en el beat exacto del guion donde suenan (no agrupadas en una sección Background aparte), con onomatopeya + distancia de mic + gatillo narrativo: `Sound effect: a backpack zipper goes "zzzip" close to the mic.` / `Sound effect: the crowd erupts at the moment of the goal, with whistles, applause, and chanting continuing to the end.`
4. **Cierre = línea `Ending sound:`** con el último sonido y cómo decae: `Ending sound: both sets of footsteps fade down the hallway as the school ambience softens.` Es la implementación canónica del cierre explícito anti-relleno.

### Armadura técnica (se suma al guion cuando aplica)

Los ejemplos canónicos son escenas inglesas cortas y no la necesitan; estas capas siguen vigentes y validadas:

- **Idioma + acento reforzado 3 veces** (escenas en español): instrucción general con negativos explícitos (`strong, unmistakable Rioplatense Argentine accent from Buenos Aires (porteño)... Never a neutral Latin American accent, never Mexican, never Castilian`) + nacionalidad/acento repetido en el descriptor de CADA personaje + léxico local en el diálogo si alguno sigue neutro.
- **Duración realista** (pedir ~20% menos del target) + `Never repeat any dialogue line.` al final.
- **Tratamiento acústico por voz** cuando alguien suena mediado por un dispositivo (teléfono/TV/radio → thin, boxy, band-limited, high-pass, con la reverb del cuarto) + decir explícitamente qué voz NO filtrar.
- **Style / Avoid** cuando hacen falta: carácter de la grabación (`imperfect smartphone recording`) y negative prompt (no music, no robotic voices, qué no debe tapar el diálogo).
- **Evento pico**: declararlo al principio como la razón de ser de la pieza + contraste explícito de mezcla (ver sección siguiente).
- **Marcadores no verbales** entre líneas cuando el beat lo pide: `Short pause, listening.` / `A sharp shocked gasp.`

## Ejemplos canónicos (aprobados por Paul, 2026-07-07)

**Diálogo dos personajes + SFX intercalados (pasillo de escuela):**

```
School bell rings from near to far, with after-school hallway ambience: distant footsteps, student chatter, locker clacks, and soft hallway reverb.

Jake (teenage male, American accent, bright youthful voice, sunny and cocky) teases playfully: "Hey, Emma, you free Saturday? My treat, that new amusement park!"

Sound effect: a backpack zipper goes "zzzip" close to the mic.

Emma (teenage female, American accent, sweet soft airy voice, shy) lowers her voice, flustered: "Uh... I still haven't finished my homework."

Jake (teenage male, coaxing, dragging the words with a grin) says: "You can do it Sunday. It's just half a day!"

Emma (teenage female, hesitant but softening) mutters: "But... it's due Monday."

Jake (teenage male, gentler, more sincere) offers: "I'll do it with you, then we head out. Deal?"

Emma (teenage female, unable to hide a laugh, shyly giving in) says: "...Fine, just half a day, okay?"

Jake (teenage male, excited and triumphant) replies: "Deal!"

Ending sound: both sets of footsteps fade down the hallway as the school ambience softens.
```

**Voz única con arco de intensidad + cama reactiva (estadio):**

```
Inside a huge football stadium, tens of thousands of fans roar throughout the background, swelling whenever the action peaks.

Commentator (middle-aged male, British accent, rich penetrating voice, classic sports commentary, extremely exhilarated) shouts rapidly: "Oh, he scores!"

Commentator (middle-aged male, voice soaring higher, almost hoarse with excitement) stretches the word: "What a goooal!"

Commentator (middle-aged male, full-throated and breathless) continues: "He beats two men and buries it in the top corner. Unbelievable! The stadium is on its feet!"

Sound effect: the crowd erupts at the moment of the goal, with whistles, applause, and chanting continuing to the end.
```

## Escenas sound-design con evento pico y/o línea única (run detective)

- **El diálogo enterrado en el timeline NO se genera.** Aunque sea una sola línea al final, va en bloque `Dialogue:` separado con personaje, emoción y delivery. El timeline solo referencia el momento ("then the dialogue line").
- **Evento pico**: declararlo al principio como la razón de ser de la pieza ("The piece exists for ONE violent moment...") + contraste explícito en términos de mezcla ("peaking near full scale; everything else at least 10 decibels quieter") + pre-evento "hushed/restrained". Sin esto sale plano (validado: 4-6 dB de contraste sin el refuerzo, ~30 dB con él).
- **Sesgo de adelanto ~2s**: el evento pico dispara 1-4s antes de lo pedido, e instrucciones tipo "never earlier than 9 seconds" NO lo frenan. Pedirlo 1-2s más tarde del beat deseado, medir dónde cayó realmente (volumedetect por ventanas de 1s) y remapear los shots — el audio manda.
- **Límite de prompt 2.048 chars es duro** y el fallo es traicionero: el submit devuelve 200, el status llega a COMPLETED rápido (~5s) y el 422 aparece recién al buscar el response. `scripts/seed_audio_gen.py` tiene guard preventivo.
- QA de escenas con pico: perfil de niveles segundo a segundo; el pico debe estar ≥8 dB sobre el resto y en el beat esperado. Whisper sobre tramos ayuda a ubicar la línea (los timestamps globales de Whisper en piezas SFX-heavy son poco confiables — transcribir por segmentos extraídos).

## Gotchas validados (2026-07-03)

- **La instrucción de duración NO es dura.** El modelo genera 10-50% más de lo pedido, y si sobra tiempo **rellena repitiendo las últimas líneas del diálogo**. Fix: pedir ~20% menos del máximo real (`target 12 seconds, total under 15`), arrancar la escena con la primera línea ya hablando (sin intro de ambiente), y limitar la cola final (`for barely one more second, then end immediately`).
- **Español rioplatense funciona** aunque la doc oficial diga solo EN/ZH — pero el acento necesita el refuerzo triple (parte 1 + parte 2 por personaje + léxico local en el diálogo si un personaje sigue neutro).
- **El diálogo sale verbatim** si el guion entra cómodo en la duración; verificarlo siempre.
- La sección Avoid y las jerarquías de volumen del background se respetan bien.

## QA obligatorio post-generación

1. `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 out.mp3` — vs. duración máxima acordada.
2. Transcripción para verbatim (la CLI whisper de anaconda está rota — usar la API):
   ```bash
   export $(grep OPENAI_API_KEY .env | head -1)
   curl -s https://api.openai.com/v1/audio/transcriptions -H "Authorization: Bearer $OPENAI_API_KEY" \
     -F file=@out.mp3 -F model=whisper-1 -F language=es -F response_format=text
   ```
   Chequear: diálogo palabra por palabra, sin líneas repetidas al final.
3. **Medir beats** (alimenta los shots del prompt Seedance): mismo curl con `-F response_format=verbose_json -F "timestamp_granularities[]=segment"`. Guardar `[start-end] texto` por segmento en `beats.json`. Los huecos entre segmentos = gasps/pausas/SFX.

## Dos capas: voz + SFX/ambiente por separado (caso b)

Validado 2026-07-03 (escena noticiero). Da control total de la mezcla a costa de una generación extra.

### 1. Capa voz (stem seco)

Mismo prompt canónico pero declarado como stem: `This is a VOICE-ONLY stem for later mixing. Absolutely no background sounds: no ambience, no room tone, no sound effects, no music...` + `Style: Dry, clean recording of the vocal performances only, like isolated dialogue stems, no reverb tails, no environment.` El tratamiento acústico por voz (TV boxy, voz principal full-range) se mantiene — es carácter de la voz, no SFX. Cierre: `The audio ends immediately after the [personaje]'s final word.`

Después de generar: QA verbatim + **medir beats** (verbose_json) — esos timestamps gobiernan la capa 2.

### 2. Capa SFX/ambiente (bed sin voces)

Prompt separado, estructura:

- Apertura: `Generate a sound-effects and ambience audio bed of about X seconds, recorded at a healthy, clearly audible level like a professional film ambience stem. This is an AMBIENCE-ONLY stem for later mixing under dialogue. Absolutely NO voices, no speech, no whispering, no vocalizations, no music.`
- **Timeline con timestamps exactos** derivados de los beats de la voz + storyboard:
  ```
  0.0 to 10.0 seconds: [cama sonora continua + texturas del lugar]
  10.0 to 13.0 seconds: [evento sonoro del clímax, "getting clearly louder second by second"]
  ```
- Style: `Realistic cinematic ambience stem, textured and present, real-room recording quality, well above the noise floor.`
- Avoid: voces + `No near-silence: the ambience must be clearly audible throughout.`

**Gotcha crítico**: sin el pedido explícito de nivel ("healthy, clearly audible", "well above the noise floor", eventos "unmistakably present"), el bed sale casi mudo (probe v1: mean -57.7 dB, pico -36 dB — inservible). Con el refuerzo: mean ~-46 dB, pico ~-27 dB — utilizable. QA del bed: `volumedetect` global y por segmentos (verificar que el evento del clímax realmente sube), y transcript Whisper — texto alucinado (frases random en japonés) sobre ambiente = normal, no es voz real.

### 3. Mezcla (scripts/seed_audio_mix.py)

```bash
python3 scripts/seed_audio_mix.py --voice voz.mp3 --bed sfx.mp3 \
  --out mix.wav --bed-offset-db 10   # bed 10 dB abajo de la voz (default)
```

Mide LUFS integrado de cada stem, calcula la ganancia del bed para que quede `--bed-offset-db` abajo de la voz, mezcla (duración = stem más largo, cap 15s), masteriza con ganancia estática a -14 LUFS + limiter TP -1.5 (NO loudnorm lineal: el TP cap bloquea la ganancia silenciosamente) y verifica midiendo el resultado. Escribe `<out>.mixreport.json` con todos los valores.

**Límite Seedance: UN audio de referencia, máx 15s.** Nunca pasar los dos stems: siempre se mezcla local y entra el mix. Guardar los stems en el run — remezclar (`--bed-offset-db` distinto) es gratis; regenerar no.

## Ejemplo validado (escena cocina + teléfono)

Prompt completo en `scratch/seed-audio-probes/prompt_cocina_telefono_v2_duration.txt` — pedido ~20s → salió 23.3s limpio, verbatim, sin repeticiones. Segundo ejemplo (TV + grito + sirenas): `scratch/seed-audio-probes/prompt_noticiero_dolares_v2.txt` — pedido 12s bajo máximo 15 → salió 13.1s.
