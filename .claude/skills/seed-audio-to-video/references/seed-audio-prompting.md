# Prompting Seed Audio 1.0 (estructura canónica)

Modelo: `bytedance/seed-audio-1.0` en fal — genera escenas de audio completas (diálogo multi-personaje verbatim + SFX + ambiente + música) en una pasada. Specs: $0.1875/min, MP3 24kHz, máx 2 min/pasada, prompt máx 2.048 chars. Base de conocimiento completa con hallazgos validados: `_research/seed-audio/README.md`.

Helper: `python3 scripts/seed_audio_gen.py --prompt-file prompt.txt --out out.mp3` (lee `FAL_API_KEY` de `.env`, submit + poll + descarga MP3 y JSON de metadata).

## Estructura canónica del prompt (7 partes, en este orden)

El prompt es un **mini guion de audio**, no un brief. Escribilo en inglés con el diálogo en el idioma target.

1. **Idioma + acento + duración realista.** El acento se refuerza acá con negativos explícitos:
   `Generate a realistic audio scene of about X seconds in Spanish. Both voices must have a strong, unmistakable Rioplatense Argentine accent from Buenos Aires (porteño): Argentine intonation and melody. Never a neutral Latin American accent, never Mexican, never Castilian.`
2. **Escena + tratamiento acústico por voz.** Quién está físicamente en el espacio (full-frequency, integrado al ambiente) vs. quién suena mediado por un dispositivo (teléfono/TV/radio → thin, boxy, band-limited, high-pass, con la reverb del cuarto). Decir explícitamente qué voz NO filtrar. **Repetir la nacionalidad/acento en la descripción de CADA personaje** (tercera capa de refuerzo).
3. **Diálogo línea por línea** con etiqueta de personaje, emoción y delivery, más marcadores de pausa/eventos no verbales (`Short pause, listening.` / `A sharp shocked gasp.`).
4. **Background:** UNA cama sonora continua fuerte + 1-2 eventos puntuales con jerarquía de volumen explícita (`very low`, `distant`, `noticeable but distant`). Si un evento entra en un momento específico, decirlo (`Right after the woman screams, police sirens approach...`).
5. **Style:** el carácter de la grabación (`imperfect smartphone recording`, `realistic domestic night scene, believable daily-life realism`).
6. **Avoid:** negative prompt — qué voces no filtrar, qué no debe tapar el diálogo, no music/no robotic voices.
7. **Duración y cierre explícito:** cuál es la última línea, qué sonido queda después y por cuánto, y `Never repeat any dialogue line.`

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
