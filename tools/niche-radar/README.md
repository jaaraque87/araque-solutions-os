# Niche Radar — research de nicho con datos verificables, $0

Nuestra alternativa propia a Sandcastles ($49-499/mes). Recolecta métricas REALES y públicas del nicho de un cliente y alimenta la metodología hook-machine. Skill que lo opera: `.claude/skills/niche-radar/SKILL.md`.

## Uso rápido (YouTube Shorts)

```bash
node tools/niche-radar/scripts/yt-shorts-radar.mjs --channel "@AlexHormozi" --max 60 --winners 8
# con cliente de hook-lab:
node tools/niche-radar/scripts/yt-shorts-radar.mjs --channel "@canal" --client mi-cliente
```

Salida por run: `radar.json` (datos crudos), `report.md` (tabla con links verificables), `transcripts/*.txt` (subtítulos de los winners, limpios).

Requisitos: Node 22+, yt-dlp (`winget install yt-dlp.yt-dlp`). El script inyecta `--js-runtimes node` (YouTube exige runtime JS para tabs de canal desde 2026).

## Probado

2026-07-04 · @AlexHormozi · 40 shorts · línea winner/loser detectada por gap natural en el puesto 12 · 5 winners con views/likes/comments/eng% · 2 transcripts.

## Instagram / TikTok

Flujo asistido por navegador (Chrome conectado a Claude) — ver SKILL.md. Datos públicos, ritmo humano, sin scraping masivo.

## Mejoras pendientes

- [ ] Fallback de transcript: cuando el short no tiene subtítulos, bajar audio (con OK del dueño) y transcribir con Whisper local (`hyperframes-media`).
- [ ] Detección de idioma del canal para `--lang` automático.
- [ ] Colector IG/TT semiautomático que escriba el mismo esquema `radar.json`.
