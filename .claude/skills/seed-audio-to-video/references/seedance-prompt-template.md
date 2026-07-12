# Prompt Seedance 2.0 — estructura prosa con @Image1/@Audio1

Versión actualizada del prompter para cuando hay **storyboard + audio pregenerado** (este pipeline). La skill `seedance-prompter` (YAML) sigue vigente para text-to-video puro sin audio de referencia — no la reemplaza.

Prerequisito: los beats medidos del audio (`beats.json` del Paso 2). Los timestamps de los shots se clavan a esos beats, no se inventan.

## Estructura fija (3 bloques)

### 1. Párrafo de referencias y reglas acústicas

Un solo párrafo que define el contrato global:

- `Use @Image1 as the storyboard and composition reference only:` + recap compacto de qué contiene (personaje + vestuario, locación, beats, tono).
- `Use @Audio1 as the exact Spanish spoken performance reference with natural breathing, gasp, and timing.`
- Regla de lip-sync: `The on-camera [personaje] speaks only in Spanish with perfect natural lip-sync; [su] voice must sound full-range, normal, and integrated with the [espacio] ambience, not filtered.`
- Regla de dispositivos: todo sonido que sale de un dispositivo en escena (TV/teléfono/radio) `must feel localized to [el dispositivo]: slightly boxy, band-limited, reduced low-end, embedded in the room.`
- Regla de ambiente exterior (sirenas, perros, calle): `natural exterior ambience heard through the walls, distant and muffled, never overpowering.`

### 2. Bloques `[SHOT N | X.X-Y.Ys]`

Un bloque por shot. Los rangos cubren TODO el clip sin huecos y cada borde coincide con un beat medido del audio. Cada bloque incluye, en prosa corrida:

- **Cámara**: tipo de plano + un movimiento primario (`Handheld wide shot from behind the couch, slow lateral drift right`). Mantener la disciplina de un movimiento por shot.
- **Mapeo a panel**: `matching the first panel of @Image1` / `following panels three and four of @Image1`.
- **Acción coreografiada**: movimientos físicos visibles, no resumen emocional.
- **Diálogo inline** cuando el beat tiene línea: `Dialogue (Spanish, full natural room voice, desperate scream with perfect lip-sync to @Audio1): "..."` — o `TV dialogue (Spanish, localized to TV speakers): "..."`.
- **Texto diegético** si existe: texto exacto entre comillas + `Headline text stays static and perfectly legible.`
- **Luz**: una frase (`Warm floor lamp glow, cool TV flicker`).
- **Continuidad**: recordatorios de identidad/vestuario/layout cuando el shot cambia de ángulo (`Maintain exact identity, clothing, hair, and room layout`).

Reglas de mapeo:
- Diálogo del beat → shot que lo contiene, con el speaker en cámara (o el dispositivo visible).
- Gasps/pausas medidos → transiciones de shot o beats de reacción.
- La cola ambiental del audio (sirenas, SFX final) → último shot, con su traducción visual (p. ej. luces policiales azul/rojo barriendo la pared como reflejos, sin patrulleros visibles).

### 3. `Negative prompt:` (lista separada por comas)

Baseline — adaptar según la escena:

```
subtitles, captions, logos, garbled or morphing on-screen text, unreadable headline,
cinematic lighting, luxury staging, commercial polish, exaggerated acting, fake AI look,
visible camera equipment, crew, extra characters, inconsistent face, inconsistent clothing,
duplicate people, broken continuity, filtered or muffled on-camera voice, music,
wrong language, gibberish, translated dialogue.
```

Agregar los específicos de la escena (p. ej. `police officers or vehicles visible`, `full-range TV anchor voice`).

## Referencias múltiples (validado)

El endpoint acepta varias imágenes: `@Image1` = storyboard (composición), `@Image2` = foto canónica del personaje (identidad de cara) — declarar el rol de cada una en el párrafo inicial ("as the exact face and identity reference"). Con ambas, la identidad se sostiene entre shots mucho mejor que con el storyboard solo.

## Cortes sincronizados a sonido (validado)

Para que un corte caiga sobre un evento del audio: "Matching panel N, cut ON the crash sound at exactly 6.0s: ...". El evento visual y el sonoro quedan atados.

## Ejemplos validados completos

- **Canónico**: `outputs/ugc/detective-sherlock-20260703-140402/seedance/prompt.txt` — 6 shots a beats medidos, 3 referencias (storyboard + cara + audio), corte ON crash, línea final con lip-sync. 1080p 9:16 13s.
- Histórico: `scratch/seed-audio-probes/seedance_prompt_noticiero_dolares.txt` — escena noticiero/grito, 4 shots, primera validación del formato.

## Envío (default fal)

Helper canónico: `~/.codex/skills/seedance-fal/scripts/run_seedance_fal.py` (endpoint `bytedance/seedance-2.0/reference-to-video`, sube archivos locales a fal storage). Duraciones válidas: 4-15 o auto. Resoluciones: 480p/720p/1080p. `--generate-audio` obligatorio con audio de referencia (en false el clip sale mudo). Siempre `--dry-run` primero y revisar `seedance_request_preview.json`.
