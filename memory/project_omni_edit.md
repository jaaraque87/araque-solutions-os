# OMNI EDIT — restyle generativo de clips (estado 2026-07-05)

Capa de post-producción del pipeline ARAQUE: aplica un estilo consistente (fondos por
frase, reencuadres por beat, cara/voz intactas) a series de clips talking-head, vía
Gemini Omni Flash. Réplica del Shorts Maker de Higgsfield sin sus créditos.

## Componentes (todos en este repo)
- Skill: `.claude/skills/omni-edit/` — v2, 11 estilos (`patterned` = único validado),
  canon "Sticker Punch", + `WINDOWS.md` (adaptador de rutas para este PC).
  Backup v1 en `backups/omni-edit-skill-v1-20260705/`.
- Ejecutor: `tools/omni-flash/generate_video.py` (batch, stdlib puro, Python `py` 3.13).
  Modelo: `gemini-omni-flash-preview` vía **generateContent** (síncrono, responseModalities
  VIDEO). predictLongRunning es solo para Veo. Files API upload VERIFICADO funcionando.
- Post: `tools/omni-flash/remux_voice.py` (retime ~1% + remux voz original — obligatorio).
- Key: `GEMINI_API_KEY` en `.env` raíz — VÁLIDA (formato nuevo `AQ.A...`, 53 chars).

## Bloqueo actual (decisión de plata del dueño)
Free tier de Google = `limit: 0` para omni-flash (video no incluido en gratis).
Desbloqueo: activar billing en el proyecto Google del dueño (aistudio.google.com).

## Piloto listo para disparar (cuando haya billing)
```bat
PYTHONIOENCODING=utf-8 py tools\omni-flash\generate_video.py --batch tools\omni-flash\pilot_smoke.json --concurrency 1
:: luego pilot_rest.json (2 clips más) · después remux_voice.py por clip · QA identidad + lipsync 6 puntos
```
- Jobs: `pilot_smoke.json` (clip "Con Araque Solutions eso se acabó") + `pilot_rest.json`.
- Prompts: canon patterned 2 capas (mundo Omni TEXTLESS + tiritas en post con HyperFrames),
  beat maps dirigidos desde `pilot_words.json` (faster-whisper small, word-level, instalado).
- Clips fuente: Downloads del PC principal (`video_000X_..._audio*.mp4`, 1024×1920, ~3s).

## Integración en el pipeline
ElevenLabs (voz) → MVC ComfyDeploy / LTX Director (clips) → omni-edit (restyle serie)
→ remux_voice → HyperFrames (tiritas captions + ensamble + mix).

## Relacionado
Biblioteca Higgsfield: `docs/higgsfield-skill-library/` (98 skills referencia; 9 activas
con prefijo `hf-` en `.claude/skills/`). Candidatas a estilos omni: flash-reel,
rockstar-agent, pulp-cinema-director.
