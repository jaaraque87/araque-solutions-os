---
name: seed-audio-to-video
description: "Pipeline gated de idea â†’ escena audiovisual: storyboard 2x2 fotorrealista con GPT Image 2 (cuadrantes numerados + Action, sin texto sobreimpreso), audio de escena completo con Seed Audio 1.0 (diÃ¡logo + ambiente + SFX en una pasada, prompt canÃ³nico), prompt Seedance en prosa @Image1/@Audio1 con [SHOT | t] sincronizado a los beats medidos del audio, y generaciÃ³n reference-to-video vÃ­a fal por DEFAULT (Higgsfield/Replicate/Runway solo si Paul lo pide explÃ­cito). Valida con Paul al final de CADA paso â€” nunca corre de punta a punta sola. Usar cuando el usuario diga 'seed audio to video', 'armÃ¡ la escena completa', 'convertÃ­ esta idea en un clip con audio', 'idea â†’ storyboard â†’ audio â†’ video', o describa una mini-escena costumbrista/dramÃ¡tica que necesita diÃ¡logo con ambiente sonoro y video corto 9:16."
---

# Seed Audio â†’ Video

Pipeline de 4 pasos (mÃ¡s una etapa opcional de direcciÃ³n) que convierte una idea en un clip corto con audio de escena real (diÃ¡logo + ambiente + SFX). NaciÃ³ del flujo validado el 2026-07-03 (escena "los dÃ³lares del vestidor").

**Regla de oro: es un pipeline GATED.** Al final de cada paso, mostrÃ¡ el artifact, esperÃ¡ el OK explÃ­cito de Paul y reciÃ©n ahÃ­ avanzÃ¡. Si Paul pide cambios, iterÃ¡ dentro del paso. Si al reanudar existe la posibilidad de que haya editado un artifact a mano, re-leelo desde disco antes de seguir.

**Formato default: vertical 9:16 SIEMPRE**, salvo que Paul explicite lo contrario. Esto gobierna el encuadre de los paneles del storyboard, el prompt Seedance y el aspect ratio de generaciÃ³n.

**La duraciÃ³n del audio MANDA.** El video Seedance dura exactamente lo que dura el audio (redondeado hacia arriba), con tope duro de 15s. Por eso el guion/escena sonora se diseÃ±a desde el arranque para entrar en â‰¤15s â€” si el audio sale mÃ¡s largo, se itera el audio, no se estira el video.

## Run setup

- Run dir: `outputs/ugc/<descripcion-kebab>-<YYYYMMDD-HHMMSS>/` (registrado en CONTRACT.md, comparte carpeta con el flow ugc_video).
- Estructura: `storyboard/`, `audio/`, `seedance/`, `run.json` (estado por paso: pending/approved), prompts como `.txt` versionados al lado de cada output.
- Keys: `FAL_API_KEY` y `OPENAI_API_KEY` en `.env` de la raÃ­z del repo. Nunca hardcodear.

## Personaje = Paul (mÃ©todos registrados; el flujo sigue siendo versÃ¡til)

Este pipeline funciona con CUALQUIER personaje. Pero cuando el personaje es Paul, usar estos mÃ©todos canÃ³nicos sin reinventar:

- **Visual (storyboard/imagen)**: Four-Photo Identity Pack + bloque IDENTITY LOCK â€” detalle en `references/storyboard-style.md` Â§ Identidad de Paul. Nunca una sola foto.
- **Voz real (lÃ­nea hablada en mezclas dos-capas)**: el preset de `/avatar-reel` (`identity.json â†’ voice_generation_canon`, "mecha_chameleon_reel_voice") vÃ­a `scripts/generate_gemini_eleven_audio.py`: Gemini TTS voz **Puck** + profile/accent canÃ³nicos de identity.json verbatim + ElevenLabs STS Paul Pro (settings del preset, ya hardcodeados en el script). Adaptar SOLO `--scene/--style/--pacing/--energy` a la escena, sobrio. **NO cambiar la voz Gemini** (Algenib u otras texturas rompen el timbre de Paul a travÃ©s del STS â€” validado 2026-07-03, run chef). Usar `audio_final_normalized.mp3` (el `audio_final.mp3` crudo del STS sale ~-36 LUFS).
- **Sync voz + bed**: medir el crash/evento real del bed (volumedetect fino 0.1s), recortar silencios de borde de la lÃ­nea (`silenceremove`), `adelay` hasta el beat elegido, y mezclar preservando dinÃ¡mica: bed a unity, voz ~-4 dB, master estÃ¡tico `gain = min(target_LUFS - premix_I, -1.5 - premix_TP)` + limiter solo de seguridad. **Ojo con `seed_audio_mix.py` + voz padded**: si el stem de voz estÃ¡ bajo, el master positivo estampa crash Y voz contra el limiter y mata el contraste.

## Paso 0 (opcional) â€” DirecciÃ³n con StillsLab

Cuando la escena tiene ambiciÃ³n cinematogrÃ¡fica (perÃ­odo, gÃ©nero marcado, mood especÃ­fico) o Paul pide "direcciÃ³n", "referencias", "mood": corrÃ© esta etapa ANTES del storyboard. Para escenas costumbristas simples se puede saltear.

1. ArmÃ¡ 2-3 bÃºsquedas semÃ¡nticas en StillsLab que cubran los espacios/momentos clave de la escena, y bajÃ¡ ~6 stills por bÃºsqueda:
   ```bash
   python3 scripts/stills_lab.py --out <run>/references/stills_lab/<tema> \
     --search "<descripciÃ³n de la escena en inglÃ©s plano>" --n 6
   ```
2. Cada still trae ficha tÃ©cnica (director, DP, cÃ¡mara, lente, color, lighting, INT/EXT, hora, frame size, shot type, composiciÃ³n) + paleta HEX extraÃ­da. **La ficha ES el research** â€” leerla y despuÃ©s promediarla en adjetivos genÃ©ricos es desperdiciarla.
3. SintetizÃ¡ en `<run>/direction/direction.md` con un **mapa panelâ†’still ancla**: cada beat del storyboard queda asignado a UN still concreto cuya ficha viaja despuÃ©s al prompt (ver regla en Paso 1). AdemÃ¡s: outfit, locaciÃ³n y paleta global.
4. ArmÃ¡ un contact-sheet de los stills elegidos para mostrar.

**GATE 0:** mostrale a Paul el contact-sheet + el brief de direcciÃ³n. IterÃ¡ hasta OK.

## Paso 0.5 â€” Assets fuente con Krea 2 (canon 2026-07-05)

**NUNCA reusar fotos viejas de personaje/locaciÃ³n** (ni del brand kit ni de runs anteriores) como assets fuente de una escena nueva. Los assets text-to-image nuevos (personaje, locaciÃ³n, moodplates) se generan con **Krea 2 Large** (skill `krea-2-large-api`: API oficial `api.krea.ai`, key en `~/.config/krea/env`, helper `scripts/krea_api.py`; `resolution: "1K"`, `creativity` explÃ­cito).

- **Krea es MUY sensible al prompt**: ser hiper-especÃ­fico con estilo, cÃ¡mara, lente, iluminaciÃ³n, paleta y textura â€” la ficha StillsLab del ancla viaja al prompt de Krea igual que al storyboard (pelÃ­cula+DP, lighting verbatim, lente, HEX).
- **ExploraciÃ³n previa**: generar 2-3 variantes por asset basadas en lo aprendido en la fase de direcciÃ³n (distintos anclas/esquemas de luz), comparar y elegir el ganador antes de seguir. `creativity: "raw"` o `"low"` para direcciÃ³n apretada.
- **GPT Image 2 queda SOLO para**: (a) la lÃ¡mina del storyboard, (b) ediciones que exigen consistencia de producto/personaje/locaciÃ³n vÃ­a `image_urls` (edit multi-ref). El producto real de un brand kit (packshot) NO se regenera: es caso consistencia.
- **Preferencia estÃ©tica validada por Paul (2026-07-05, run asador)**: en la exploraciÃ³n ganaron las variantes **moody/nocturnas** â€” retrato 3/4 con practicable tungsteno + edge light rojo (tipo War Machine/Aaron Morton) y locaciÃ³n low-wide con columna de humo backlit dramÃ¡tica â€” por sobre las frontales doradas tipo catÃ¡logo. Sesgar la exploraciÃ³n hacia ese polo (y NO asumir que "frontal nÃ­tido = mejor ref de identidad": la ref con carÃ¡cter cinematogrÃ¡fico tambiÃ©n sostiene identidad y define mejor el mundo).

## Paso 1 â€” Storyboard (GPT Image 2)

LeÃ© `references/storyboard-style.md` (estilo exacto de la lÃ¡mina + prompt template).

1. ConvertÃ­ la idea en beats narrativos: **4 por default, hasta 6 como mÃ¡ximo absoluto** (grilla 2x2 o 2x3). Si la historia no entra en 6 beats, simplificÃ¡ la historia, no agregues paneles.
2. **DirigÃ­, no decores.** Cada panel especifica: hacia dÃ³nde mira el personaje, orientaciÃ³n del cuerpo, quÃ© acciÃ³n estÃ¡ ejecutando y a quÃ© reacciona. Meter los objetos de la historia en el cuadro no alcanza â€” si un beat es "ve una sombra escapando", el personaje tiene que estar MIRANDO la sombra y la sombra tiene que estar EN MOVIMIENTO de fuga.
3. **La ficha viaja al prompt, panel por panel** (cuando corriÃ³ el Paso 0). Para modelos de imagen esta info es LA clave del estilo: cada frame del prompt lleva el bloque de SU still ancla â€” pelÃ­cula + DP nombrados ("in the exact photographic style of Breaking Bad S4E5, DP Michael Slovis"), frame size + shot type + composiciÃ³n textuales de la ficha ("high angle wide shot, right-heavy composition"), tÃ©rminos de lighting verbatim ("hard top light, high contrast"), lente/cÃ¡mara con carÃ¡cter ("Panavision T-Series glass") y paleta anclada en HEX ("palette anchored on #7C8454 #0F0B06 #B1A697"). PROHIBIDO promediar las fichas en una sola frase de adjetivos globales â€” eso produce "perÃ­odo genÃ©rico" y desperdicia el research. Ver template por panel en `references/storyboard-style.md`.
4. **ActuaciÃ³n con FACS**: cada panel con cara visible lleva una lÃ­nea `Acting:` con direcciÃ³n FACS compacta (skill `facs-acting-direction`: AUs con nombre anatÃ³mico + intensidad + respiraciÃ³n/mandÃ­bula/mirada/postura; intensidades medias 0.25-0.70 salvo shock). Los paneles de manos/objeto se saltean. Bloque validado en `references/storyboard-style.md`.
5. GenerÃ¡ la lÃ¡mina con GPT Image 2 en fal con **`quality: "high"`** y **`image_size: {"width": 1536, "height": 2048}`** (custom WxH es vÃ¡lido; el preset `portrait_4_3` rinde 768x1024 y los paneles quedan borrosos) â€” con identidad de personaje usar `openai/gpt-image-2/edit` vÃ­a `fal_client`; sin identidad, `openai/gpt-image-2`. **Si el personaje es Paul: SIEMPRE el Four-Photo Identity Pack completo como `image_urls` + bloque IDENTITY LOCK en el prompt** (skill `paul-seedance`; detalle y snippet en `references/storyboard-style.md`) â€” una sola foto afloja el parecido en planos medios/wides. UNA sola imagen con todos los cuadrantes + rotulado.
6. **El formato de la lÃ¡mina es fijo** (el de la referencia canÃ³nica, ver `references/storyboard-style.md`): fondo ivory, grilla de paneles fotorrealistas, badge negro numerado + tÃ­tulo MAYÃšSCULAS + "Action:" por panel, footer NOTAS. Los paneles deben leerse como **film stills fotogrÃ¡ficos reales** (35mm, textura de piel, fÃ­sica real) â€” nunca ilustraciÃ³n ni render pictÃ³rico.
7. CrÃ­tico: **cero texto sobreimpreso dentro de las escenas** (nada de quotes ni captions sobre la foto). Texto diegÃ©tico (pantalla de TV, cartel fÃ­sico) solo si la historia lo exige.

**GATE 1:** mostrale la lÃ¡mina a Paul. IterÃ¡ hasta OK.

## Paso 2 â€” Audio (Seed Audio 1.0)

LeÃ© `references/seed-audio-prompting.md` (formato guion intercalado + armadura tÃ©cnica + gotchas + los dos ejemplos canÃ³nicos aprobados). Base de conocimiento completa: `_research/seed-audio/README.md`.

**CANÃ“NICO: el audio se genera COMPLETO en UNA sola pasada de Seed Audio** â€” diÃ¡logo (si hay) + ambiente + SFX + el evento pico, todo incluido en la misma generaciÃ³n. Nada de stems separados, nada de parchear eventos con one-shots mezclados en post. Si un elemento sale dÃ©bil (p. ej. el evento pico sin fuerza), se **itera el prompt de la pasada Ãºnica**, no se arregla mezclando.

1. EscribÃ­ el prompt en formato guion intercalado (el orden del texto ES el timeline): apertura de ambiente en una oraciÃ³n sin voces, diÃ¡logo lÃ­nea por lÃ­nea con descriptor completo en la primera apariciÃ³n y direcciÃ³n emocional que evoluciona por lÃ­nea, SFX como lÃ­neas `Sound effect:` en su beat exacto, cierre con lÃ­nea `Ending sound:`. SumÃ¡ la armadura tÃ©cnica cuando aplica: idioma/acento reforzado 3 veces, perspectiva acÃºstica por voz, style/avoid, "Never repeat any dialogue line".
2. **Si la escena tiene un evento pico** (vidrio que estalla, golpe, portazo): declaralo como EL evento definitorio de la pieza, al principio del prompt ("The scene builds to ONE violent event... BY FAR the loudest moment, like a film jump-scare, dramatically louder than everything around it") y repetilo en su beat del timeline. El contraste de dinÃ¡mica hay que pedirlo explÃ­cito o sale plano.
3. **DuraciÃ³n: pedÃ­ ~20% menos del target** (el modelo se pasa). Guion hablado debe entrar cÃ³modo en la duraciÃ³n pedida.
4. GenerÃ¡: `python3 scripts/seed_audio_gen.py --prompt-file <run>/audio/prompt.txt --out <run>/audio/scene_v1.mp3`
5. QA obligatorio: `ffprobe` (duraciÃ³n vs. mÃ¡ximo) + transcripciÃ³n Whisper API (`whisper-1`, la CLI de anaconda estÃ¡ rota) verificando diÃ¡logo verbatim y SIN lÃ­neas repetidas. Con evento pico: **perfil de niveles segundo a segundo** (`volumedetect` por ventanas de 1s) verificando que el pico estÃ© donde corresponde y â‰¥8 dB sobre el resto. Si falla, iterÃ¡ el prompt (no mezcles).
6. Master liviano sobre la pasada Ãºnica si hace falta nivel (ganancia estÃ¡tica a ~-14/-16 LUFS + limiter TP -1.5): eso no es layering, es normalizaciÃ³n.
7. **MedÃ­ los beats** con `response_format=verbose_json` + `timestamp_granularities[]=segment` â€” los timestamps alimentan los shots del Paso 3. Guardalos en `<run>/audio/beats.json`.

### Caso (b) â€” dos capas separadas (SOLO si Paul lo pide explÃ­cito)

ExcepciÃ³n al canÃ³nico single-pass: Ãºnicamente cuando Paul pide "dos capas", "voz y ambiente separados" o control fino de mezcla, el paso 2 cambia a un flujo de 3 sub-pasos (detalle completo en `references/seed-audio-prompting.md` Â§ Dos capas). Nunca elegir este camino por iniciativa propia:

1. **Capa voz**: generar SOLO las voces (stem seco, sin ambiente/SFX/mÃºsica) y medir sus beats.
2. **Capa SFX/ambiente**: prompt SIN voces con **timeline de timestamps exactos** derivados de los beats de la voz y del storyboard (`0.0 to X seconds: ...`). Pedir nivel de grabaciÃ³n sano ("healthy, clearly audible level like a professional film ambience stem") â€” sin eso sale casi mudo.
3. **Mezcla**: `python3 scripts/seed_audio_mix.py --voice voz.mp3 --bed sfx.mp3 --out mix.wav --bed-offset-db 10` â€” mide LUFS de ambos stems, pone el bed N dB abajo de la voz (default 10), masteriza a -14 LUFS con limiter TP -1.5 y capea a 15s.

**Seedance acepta UN solo audio de referencia de mÃ¡x 15s** â€” nunca mandar los dos stems por separado: siempre entra la mezcla. Conservar los stems en el run para remezclar sin regenerar.

**GATE 2:** mandale a Paul el MP3 (en caso (b): los dos stems + la mezcla, con el mix report). IterÃ¡ hasta OK.

## Paso 3 â€” Prompt Seedance

LeÃ© `references/seedance-prompt-template.md` (estructura prosa @Image1/@Audio1 â€” es la versiÃ³n actualizada del prompter; la skill `seedance-prompter` YAML sigue existiendo para text-to-video puro sin audio).

1. MapeÃ¡: cada shot â†” un rango de beats del audio â†” un panel del storyboard.
2. Estructura fija: pÃ¡rrafo de referencias y reglas acÃºsticas â†’ bloques `[SHOT N | X.X-Y.Ys]` â†’ `Negative prompt:`.
3. GuardÃ¡ en `<run>/seedance/prompt.txt`.

**GATE 3:** mostrale el prompt a Paul (bloque de cÃ³digo completo). IterÃ¡ hasta OK.

## Paso 4 â€” GeneraciÃ³n de video

**Default: fal** (`bytedance/seedance-2.0/reference-to-video`) vÃ­a el helper canÃ³nico:

```bash
export $(grep -E "^FAL_API_KEY=" .env | head -1) && export FAL_KEY="$FAL_API_KEY"
python3 .claude/skills/seedance-fal/scripts/run_seedance_fal.py \
  --endpoint reference-to-video \
  --prompt "$(cat <run>/seedance/prompt.txt)" \
  --image <run>/storyboard/storyboard.png \
  --audio <run>/audio/scene_vN.mp3 \
  --resolution 1080p --duration <ceil(duraciÃ³n_audio), 4-15> --aspect-ratio 9:16 \
  --generate-audio \
  --output-dir <run>/seedance
```

- `--generate-audio` SIEMPRE true cuando pasÃ¡s audio de referencia: en false el clip sale MUDO.
- HacÃ© primero `--dry-run` y verificÃ¡ el payload; despuÃ©s ejecutÃ¡ (en background, tarda minutos).
- Defaults salvo pedido contrario: **1080p, 9:16, duration = duraciÃ³n del audio redondeada hacia arriba**.
- **Plataformas alternativas SOLO si Paul lo pide explÃ­cito** en el momento: Higgsfield (`higgsfield generate create seedance_2_0`, patrÃ³n en `scripts/seedance_submit.py`), Replicate o Runway. No las ofrezcas proactivamente.

QA final: ffprobe (duraciÃ³n/resoluciÃ³n), verificar que tiene stream de audio, y contact-sheet de frames (1 frame/s) antes de entregar.

**GATE 4 (entrega):** mandale el MP4 con el QA. Si pide iteraciÃ³n, volvÃ© al paso que corresponda (cambio de guion â†’ Paso 2; cambio de encuadre â†’ Paso 3; re-roll â†’ Paso 4).

## Errores conocidos

| SÃ­ntoma | Causa | Fix |
|---|---|---|
| Audio mÃ¡s largo que lo pedido, repite Ãºltimas lÃ­neas | DuraciÃ³n pedida no realista para el guion | Undershoot 20% + cierre explÃ­cito + "Never repeat any dialogue line" |
| Evento pico plano, sin contraste | Contraste de dinÃ¡mica no pedido explÃ­cito | Declarar el evento como razÃ³n de ser de la pieza + "at least 10 decibels quieter" para el resto + pre-crash "hushed/restrained" |
| Evento pico ~2s antes de lo pedido | Sesgo sistemÃ¡tico de Seed Audio | Pedirlo 1-2s MÃS TARDE del beat deseado, medir dÃ³nde cayÃ³ (volumedetect 1s) y remapear los shots a los beats reales â€” el audio manda |
| LÃ­nea de diÃ¡logo no se genera | DiÃ¡logo enterrado dentro del timeline | Bloque `Dialogue:` explÃ­cito y separado, con personaje + emociÃ³n + delivery (aunque sea una sola lÃ­nea) |
| 422 al buscar el response (submit OK, COMPLETED rÃ¡pido) | Prompt > 2.048 chars â€” la API acepta el submit y falla reciÃ©n en el response | `seed_audio_gen.py` tiene guard; si aparece, recortar el prompt |

## Run canÃ³nico validado

`outputs/ugc/detective-sherlock-20260703-140402/` â€” primer run end-to-end completo (2026-07-03), usar como ejemplo de CADA artifact:

- `direction/direction.md` + `references/stills_lab/` â€” etapa de direcciÃ³n StillsLab (18 stills, 3 bÃºsquedas) + mapa panelâ†’still ancla
- `storyboard/storyboard_prompt_v3.txt` â†’ `storyboard_v3.png` â€” **el ejemplo canÃ³nico**: lÃ¡mina 2x3 dirigida (miradas/bloqueo) CON ficha por panel (pelÃ­cula+DP+lente+lighting+HEX). `storyboard_prompt_v2.txt` queda como el ANTIPATRÃ“N: mismas escenas con estilo promediado en adjetivos â†’ "perÃ­odo genÃ©rico"; el A/B entre v2 y v3 es la prueba de por quÃ© la ficha viaja al prompt
- `audio/prompt_v6b.txt` â†’ `scene_final.mp3` + `beats.json` â€” single-pass todo incluido: ambiente + crash full-scale + lÃ­nea con bloque Dialogue
- `seedance/prompt.txt` â†’ `seedance_output.mp4` â€” 6 shots a beats reales, 3 referencias (@Image1 storyboard + @Image2 cara + @Audio1), corte ON el crash
| Acento neutro/mexicano | Acento mencionado una sola vez | Reforzar en instrucciÃ³n general + por personaje; anclar con lÃ©xico local |
| Clip de video mudo | `generate_audio: false` con audio ref | `--generate-audio` |
| Whisper CLI crashea (numba/numpy) | Entorno anaconda roto | Whisper API `whisper-1` vÃ­a curl |
| Acento/lÃ©xico cambiado en el render ("laburo"â†’"laboro") | `generate_audio` re-sintetiza la referencia, no la pega | Post: reemplazar la pista entera por el mix real (mux `-c:v copy`) alineado a los beats visuales |
| Mix real reemplazado queda desincronizado | Se alineÃ³ contra el audio EMBEBIDO del render â€” que tambiÃ©n sale corrido vs la imagen | Medir los eventos VISUALES frame a frame (grid fps=6 en la ventana del evento + crop de boca fps=8) y alinear el bed/lÃ­nea a ESOS beats; splice de ambiente del propio bed con acrossfade 60ms para correr el crash sin tocar la campanilla |
| Objetos "levitan" en caÃ­das | FÃ­sica floja de Seedance en drops (caÃ­da ~0.67s vs ~0.45s real) | Prompt: "falls fast with real gravity" + negative "floating/suspended objects"; si ya estÃ¡ horneado: aceptar, micro-retime del segmento, o re-roll |
| Nombre de marca hablado se empasta ("Rub Rojo"â†’"rubro/rabo", 3/3 intentos) | Seed Audio no pronuncia marcas/anglicismos confiablemente; coaching fonÃ©tico puede empeorarlo ("Rab"â†’"rabo") | Default de ad: VO sin marca hablada + marca VISUAL (hero shot del pack durante el VO). Si la marca DEBE decirse, validar de oÃ­do (Whisper tambiÃ©n alucina en nombres) o pedir OK a Paul |
| Boca moviÃ©ndose en silencio tras reemplazar el audio | La boca queda animada al timing del audio ORIGINAL de Seedance; mover la voz no alcanza | Sync V3 (`fal-ai/sync-lipsync/v3`, bounce) SOLO sobre el segmento hablado: cortar el tramo (re-encode), sync con el slice del master, re-encode ambas partes con params idÃ©nticos, concat video-only y muxear el master COMPLETO encima (una pista continua, sin costura). Elegir el punto de corte en un plano estÃ¡tico sin cara |
