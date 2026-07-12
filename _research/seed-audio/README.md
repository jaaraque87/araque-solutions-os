# Seed Audio 1.0 (ByteDance) — Base de conocimiento

Última actualización: 2026-07-07. Fuentes: [model page](https://fal.ai/models/bytedance/seed-audio-1.0), [guía fal](https://fal.ai/learn/tools/how-to-use-seed-audio), probes propios en `scratch/seed-audio-probes/`.

## Specs

| Item | Valor |
|---|---|
| Endpoint fal | `bytedance/seed-audio-1.0` (queue: `https://queue.fal.run/bytedance/seed-audio-1.0`) |
| Precio | $0.1875 / minuto generado (~$0.10 por clip de 30s) |
| Output | MP3, 24 kHz, ~64 kbps |
| Máx. por pasada | 2 minutos de audio |
| Prompt | máx. 2.048 caracteres |
| Referencias de voz | hasta 3 clips de 30s, se citan como `@Audio1`–`@Audio3` en el prompt |
| Velocidad observada | ~25–30s de cola para clips de 20–30s |

Qué hace en una sola pasada: diálogo multi-personaje con emoción, SFX, ambiente y música integrados. También edita: extender clips, inpainting (rellenar huecos), stitching y regenerar secciones conservando la voz.

## Hallazgos propios (validados con probes)

1. **Español rioplatense funciona**, aunque la doc oficial dice "solo inglés y chino" (multilingüe anunciado para julio 2026). Acento porteño natural, "che"/"laburo" bien pronunciados. Validado 2 veces el 2026-07-03.
2. **El diálogo sale verbatim** — las 6 líneas del guion salieron palabra por palabra en ambos probes (verificado con Whisper).
3. **Perspectiva acústica por personaje funciona muy bien**: pedir voz principal full-frequency integrada al ambiente + interlocutor "thin, distant, high-pass filtered like a phone speaker" produce exactamente ese contraste.
4. **La instrucción de duración NO es dura**: pedimos "10 seconds" con un guion que necesita ~20s → generó 31s y **rellenó repitiendo las últimas líneas del diálogo**. Fix validado: pedir duración realista + cierre explícito + "Never repeat any dialogue line" + describir el último sonido antes del final → 23.3s limpio, sin repeticiones.
5. **Capas de fondo con jerarquía explícita** ("very low muffled radio", "dog barks once or twice, noticeable but distant") se respetan; la sección **Avoid** (negative prompt) también.
6. **Compensar el overshoot de duración**: el modelo genera ~10-50% más de lo pedido. Para un máximo duro, pedir menos ("target 12 seconds, total under 15") + arrancar la escena con la primera línea ya hablando (sin intro de ambiente) + limitar la cola final ("for barely one more second, then end immediately"). Validado: pedido 12 → salió 13.1s.
7. **Acento: una mención no alcanza**. Reforzar en tres lugares: instrucción general con negativos explícitos ("strong Rioplatense porteño, never neutral Latin American, never Mexican, never Castilian"), y repetir la nacionalidad en la descripción de CADA personaje ("Argentine news anchor from a Buenos Aires TV channel"). Si un personaje sigue neutro, anclar con léxico local en su diálogo.

## Playbook de prompt (estructura canónica)

> **Refinado 2026-07-07**: el cuerpo del prompt ahora es formato guion intercalado (ver "Hallazgos 3ª sesión" abajo); las partes 1-2 y 5-7 de esta lista quedan como armadura técnica que se suma cuando aplica.

El prompt es un **mini guion de audio**, no un brief abstracto. Orden que funciona:

1. **Idioma + acento + duración realista** — "Generate a realistic audio scene of about 20 seconds in Spanish with a natural Buenos Aires Argentine accent."
2. **Escena + tratamiento acústico por voz** — quién está físicamente en el espacio (full-frequency, integrado al ambiente) vs. quién suena mediado (teléfono/radio → thin, muffled, high-pass). Decir explícitamente "Do not make the main voice sound like phone audio."
3. **Diálogo línea por línea** con etiqueta de personaje y marcadores de pausa ("Short pause, listening.").
4. **Background** — UNA cama sonora continua fuerte (sartén friendo) + 1-2 eventos puntuales con volumen relativo ("very low", "distant").
5. **Style** — el carácter de la grabación ("imperfect smartphone recording, believable daily-life conversation").
6. **Avoid** — negative prompt: qué filtros no aplicar, qué no debe tapar la voz.
7. **Cierre explícito** — cuál es la última línea, qué sonido queda después, y "Never repeat any dialogue line."

Prompt canónico validado: [prompt_cocina_telefono_v2_duration.txt](../../scratch/seed-audio-probes/prompt_cocina_telefono_v2_duration.txt) (escena cocina + llamada telefónica, rioplatense).

Estructura alternativa de la guía fal para escenas sound-design-heavy (formato bracket):

```
[Estilo/género. Lugar. Mood.]
[Cama sonora continua descripta.]
Personaje (voz, emoción, ritmo) dice, acción: "línea"
[SFX puntual o transición.]
...
[Cue final que resuelve o suspende.]
```

## Workflows que ofrece (según guía fal, sin probar aún)

- **T2A**: solo texto (lo que usamos).
- **TA2A**: texto + hasta 3 clips de referencia (`@Audio1`…); sirve para TTS con voz propia consistente.
- **Extend**: "Continue this exact speech seamlessly in the same voice and topic, as if it never stopped, for about X more seconds."
- **Inpainting**: rellenar un hueco en una grabación; poner el diálogo faltante al FINAL del prompt.
- **Stitching / blending / editing**: unir clips, mezclar música+FX, regenerar secciones manteniendo la voz.
- Clips de referencia ideales: 30s, un solo speaker, emoción consistente, sin ruido, 70–85 palabras.

## Cómo generar

```bash
python3 scripts/seed_audio_gen.py --prompt-file prompt.txt --out scratch/seed-audio-probes/test.mp3
```

Lee `FAL_API_KEY` de `.env`, hace submit a la queue, poll y descarga MP3 + JSON con metadata.

QA rápido: `ffprobe` para duración + Whisper API (`whisper-1`, la CLI de anaconda está rota por numba/numpy) para verificar verbatim y detectar repeticiones de relleno.

## Hallazgos 2ª sesión (run detective-sherlock, 2026-07-03)

1. **Escenas sound-design puras funcionan** (sin diálogo): timeline con timestamps + cama + eventos. Pero los descriptores tímidos ("subtle", "understated") producen audio casi mudo (pico -36 dB) — pedir "healthy, clearly audible level like a professional film sound stem".
2. **Evento pico** (vidrio, golpe): necesita declararse como la razón de ser de la pieza + contraste en términos de mezcla ("peaking near full scale; everything else at least 10 decibels quieter"). Con eso: ~30 dB de contraste real.
3. **Sesgo de adelanto**: el evento pico dispara 1-4s ANTES de lo pedido, sistemáticamente. "Never earlier than Xs" no lo frena. Compensar pidiendo más tarde y remapear el video a los beats medidos.
4. **Diálogo dentro del timeline no se genera** — siempre bloque `Dialogue:` separado, aunque sea una línea.
5. **Límite 2.048 chars confirmado y traicionero**: submit 200 → COMPLETED en ~5s → 422 recién en el response con `string_too_long`. Guard agregado a `scripts/seed_audio_gen.py`.
6. Whisper global sobre piezas SFX-heavy desubica los timestamps de la línea hablada (la marca en 0-2s aunque esté en 8-10s); ubicarla transcribiendo segmentos extraídos con ffmpeg.
7. Pipeline completo idea→video canonizado en la skill `seed-audio-to-video`; run canónico: `outputs/ugc/detective-sherlock-20260703-140402/`.

## Hallazgos 3ª sesión (2026-07-07) — formato guion intercalado

Dos prompts de referencia calificados "perfectos" por Paul consolidan el formato del cuerpo del prompt. Verbatim + estructura completa en `.claude/skills/seed-audio-to-video/references/seed-audio-prompting.md` (§ Ejemplos canónicos). Patrones:

1. **El orden del texto ES el timeline**: prosa en párrafos cortos que alternan ambiente, diálogo y SFX en el orden exacto en que suenan; sin secciones etiquetadas (Style/Avoid/Dialogue quedan como armadura opcional para acento español, voces filtradas, evento pico y anti-relleno).
2. **Apertura = una oración de escena sonora sin voces**, con movimiento espacial ("school bell rings from near to far") y cama con comportamiento ("swelling whenever the action peaks").
3. **Diálogo**: `Nombre (demografía, acento, textura, personalidad) verbo-de-delivery: "línea"` — descriptor completo solo en la primera aparición; después tag corto + la emoción de ESA línea, dibujando un arco línea a línea ("coaxing, dragging the words with a grin" → "gentler, more sincere" → "excited and triumphant").
4. **Verbos de delivery específicos** (teases playfully, mutters, shouts rapidly, stretches the word) y **prosodia escrita dentro de la línea** ("What a goooal!", "Uh...", "...Fine").
5. **SFX como líneas `Sound effect:` intercaladas** en su beat, con onomatopeya + distancia de mic ("goes 'zzzip' close to the mic") o gatillo narrativo ("the crowd erupts at the moment of the goal").
6. **Cierre como línea `Ending sound:`** describiendo el último sonido y su decay ("footsteps fade down the hallway as the school ambience softens").

## Preguntas abiertas

- Cómo se adjuntan los clips de referencia (`@Audio1`) vía API fal — ¿parámetro `reference_audio_urls`? Revisar el OpenAPI schema del endpoint.
- Input de imagen (la model page menciona "or an image") — ¿qué hace exactamente?
- Techo real de calidad en español: ¿aguanta 2 minutos sin degradar acento ni repetir?
- Música + diálogo en español en una pasada (probamos solo radio de fondo muy baja).
- Uso en pipeline UGC: ¿reemplaza TTS+SFX+música en escenas ambiente? Candidato obvio: escenas "persona en situación real" donde Gemini TTS suena demasiado limpio.
