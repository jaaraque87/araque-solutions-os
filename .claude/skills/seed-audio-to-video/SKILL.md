---
name: seed-audio-to-video
description: "Pipeline gated de idea → escena audiovisual: storyboard 2x2 fotorrealista con GPT Image 2 (cuadrantes numerados + Action, sin texto sobreimpreso), audio de escena completo con Seed Audio 1.0 (diálogo + ambiente + SFX en una pasada, prompt canónico), prompt Seedance en prosa @Image1/@Audio1 con [SHOT | t] sincronizado a los beats medidos del audio, y generación reference-to-video vía fal por DEFAULT (Higgsfield/Replicate/Runway solo si Paul lo pide explícito). Valida con Paul al final de CADA paso — nunca corre de punta a punta sola. Usar cuando el usuario diga 'seed audio to video', 'armá la escena completa', 'convertí esta idea en un clip con audio', 'idea → storyboard → audio → video', o describa una mini-escena costumbrista/dramática que necesita diálogo con ambiente sonoro y video corto 9:16."
---

# Seed Audio → Video

Pipeline de 4 pasos que convierte una idea en un clip corto con audio de escena real (diálogo + ambiente + SFX). Nació del flujo validado el 2026-07-03 (escena "los dólares del vestidor").

**Regla de oro: es un pipeline GATED.** Al final de cada paso, mostrá el artifact, esperá el OK explícito de Paul y recién ahí avanzá. Si Paul pide cambios, iterá dentro del paso. Si al reanudar existe la posibilidad de que haya editado un artifact a mano, re-leelo desde disco antes de seguir.

## Run setup

- Run dir: `outputs/seed-audio-video/<descripcion-kebab>-<YYYYMMDD-HHMMSS>/` (registrado en CONTRACT.md).
- Estructura: `storyboard/`, `audio/`, `seedance/`, `run.json` (estado por paso: pending/approved), prompts como `.txt` versionados al lado de cada output.
- Keys: `FAL_API_KEY` y `OPENAI_API_KEY` en `.env` de la raíz del repo. Nunca hardcodear.

## Paso 1 — Storyboard (GPT Image 2)

Leé `references/storyboard-style.md` (estilo exacto de la lámina + prompt template).

1. Convertí la idea en ≤4 beats narrativos (normalidad → giro → reacción → clímax es el patrón que funciona). Cada beat = 1 panel.
2. Generá la lámina con GPT Image 2 en fal (`https://queue.fal.run/openai/gpt-image-2`, `image_size: 1024x1536`, patrón de queue igual a `scripts/seed_audio_gen.py`). UNA sola imagen con los 4 cuadrantes + rotulado, no 4 imágenes.
3. Crítico: **cero texto sobreimpreso dentro de las escenas** (nada de quotes ni captions sobre la foto). Texto diegético (pantalla de TV, cartel físico) solo si la historia lo exige.

**GATE 1:** mostrale la lámina a Paul. Iterá hasta OK.

## Paso 2 — Audio (Seed Audio 1.0)

Leé `references/seed-audio-prompting.md` (estructura canónica de 7 partes + gotchas). Base de conocimiento completa: `_research/seed-audio/README.md`.

1. Escribí el prompt siguiendo la estructura canónica: idioma/acento reforzado 3 veces, perspectiva acústica por voz, diálogo línea por línea, cama sonora + eventos con jerarquía, style, avoid, cierre explícito con "Never repeat any dialogue line".
2. **Duración: pedí ~20% menos del target** (el modelo se pasa). Guion hablado debe entrar cómodo en la duración pedida.
3. Generá: `python3 scripts/seed_audio_gen.py --prompt-file <run>/audio/prompt.txt --out <run>/audio/scene_v1.mp3`
4. QA obligatorio: `ffprobe` (duración vs. máximo) + transcripción Whisper API (`whisper-1`, la CLI de anaconda está rota) verificando diálogo verbatim y SIN líneas repetidas de relleno.
5. **Medí los beats** con `response_format=verbose_json` + `timestamp_granularities[]=segment` — los timestamps alimentan los shots del Paso 3. Guardalos en `<run>/audio/beats.json`.

### Caso (b) — dos capas separadas (a pedido)

Si Paul pide "dos capas", "voz y ambiente separados" o quiere control fino de la mezcla, el paso 2 cambia a un flujo de 3 sub-pasos (detalle completo en `references/seed-audio-prompting.md` § Dos capas):

1. **Capa voz**: generar SOLO las voces (stem seco, sin ambiente/SFX/música) y medir sus beats.
2. **Capa SFX/ambiente**: prompt SIN voces con **timeline de timestamps exactos** derivados de los beats de la voz y del storyboard (`0.0 to X seconds: ...`). Pedir nivel de grabación sano ("healthy, clearly audible level like a professional film ambience stem") — sin eso sale casi mudo.
3. **Mezcla**: `python3 scripts/seed_audio_mix.py --voice voz.mp3 --bed sfx.mp3 --out mix.wav --bed-offset-db 10` — mide LUFS de ambos stems, pone el bed N dB abajo de la voz (default 10), masteriza a -14 LUFS con limiter TP -1.5 y capea a 15s.

**Seedance acepta UN solo audio de referencia de máx 15s** — nunca mandar los dos stems por separado: siempre entra la mezcla. Conservar los stems en el run para remezclar sin regenerar.

**GATE 2:** mandale a Paul el MP3 (en caso (b): los dos stems + la mezcla, con el mix report). Iterá hasta OK.

## Paso 3 — Prompt Seedance

Leé `references/seedance-prompt-template.md` (estructura prosa @Image1/@Audio1 — es la versión actualizada del prompter; la skill `seedance-prompter` YAML sigue existiendo para text-to-video puro sin audio).

1. Mapeá: cada shot ↔ un rango de beats del audio ↔ un panel del storyboard.
2. Estructura fija: párrafo de referencias y reglas acústicas → bloques `[SHOT N | X.X-Y.Ys]` → `Negative prompt:`.
3. Guardá en `<run>/seedance/prompt.txt`.

**GATE 3:** mostrale el prompt a Paul (bloque de código completo). Iterá hasta OK.

## Paso 4 — Generación de video

**Default: fal** (`bytedance/seedance-2.0/reference-to-video`) vía el helper canónico:

```bash
export $(grep -E "^FAL_API_KEY=" .env | head -1) && export FAL_KEY="$FAL_API_KEY"
python3 ~/.codex/skills/seedance-fal/scripts/run_seedance_fal.py \
  --endpoint reference-to-video \
  --prompt "$(cat <run>/seedance/prompt.txt)" \
  --image <run>/storyboard/storyboard.png \
  --audio <run>/audio/scene_vN.mp3 \
  --resolution 1080p --duration <ceil(duración_audio), 4-15> --aspect-ratio 9:16 \
  --generate-audio \
  --output-dir <run>/seedance
```

- `--generate-audio` SIEMPRE true cuando pasás audio de referencia: en false el clip sale MUDO.
- Hacé primero `--dry-run` y verificá el payload; después ejecutá (en background, tarda minutos).
- Defaults salvo pedido contrario: **1080p, 9:16, duration = duración del audio redondeada hacia arriba**.
- **Plataformas alternativas SOLO si Paul lo pide explícito** en el momento: Higgsfield (`higgsfield generate create seedance_2_0`, patrón en `scripts/seedance_submit.py`), Replicate o Runway. No las ofrezcas proactivamente.

QA final: ffprobe (duración/resolución), verificar que tiene stream de audio, y contact-sheet de frames (1 frame/s) antes de entregar.

**GATE 4 (entrega):** mandale el MP4 con el QA. Si pide iteración, volvé al paso que corresponda (cambio de guion → Paso 2; cambio de encuadre → Paso 3; re-roll → Paso 4).

## Errores conocidos

| Síntoma | Causa | Fix |
|---|---|---|
| Audio más largo que lo pedido, repite últimas líneas | Duración pedida no realista para el guion | Undershoot 20% + cierre explícito + "Never repeat any dialogue line" |
| Acento neutro/mexicano | Acento mencionado una sola vez | Reforzar en instrucción general + por personaje; anclar con léxico local |
| Clip de video mudo | `generate_audio: false` con audio ref | `--generate-audio` |
| Whisper CLI crashea (numba/numpy) | Entorno anaconda roto | Whisper API `whisper-1` vía curl |
