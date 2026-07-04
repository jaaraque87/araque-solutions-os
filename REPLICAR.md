# REPLICAR — Producir un reel de Naia desde CUALQUIER PC (Claude o Codex)

Validado 2026-07-04 con el piloto 001 (reel 17.9s publicable). Dos niveles: preparar la máquina (una vez) y el loop de producción (cada reel).

## NIVEL 1 — Preparar máquina nueva (una vez, ~15 min)

```powershell
winget install OpenJS.NodeJS.LTS Git.Git Gyan.FFmpeg yt-dlp.yt-dlp
git clone https://github.com/jaaraque87/araque-solutions-os.git
cd araque-solutions-os
notepad .env    # pegar desde WhatsApp: ELEVENLABS_API_KEY=..., ELEVENLABS_VOICE_ID=..., HYPERFRAMES_WHISPER_PATH=...
cd tools\content-reel-lab
npm install
cd ..\..
```
Whisper local (solo para radar/timestamps): bajar `whisper-blas-bin-x64.zip` de github.com/ggml-org/whisper.cpp/releases → extraer en `%LOCALAPPDATA%\whisper-cpp\` → el `.env` apunta a `...\whisper-cpp\Release\whisper-cli.exe`.

Abrir **Claude Code o Codex EN la carpeta del repo**. Las skills cargan solas (Claude: `.claude/skills/`; Codex: lee `AGENTS.md`).

## NIVEL 2 — El loop por reel (~1h, costo ≈ $0.30-0.80)

**Pega este masterprompt al agente y él ejecuta todo su lado:**

```
Lee CLAUDE.md, characters/naia-cruz/produccion-ltx.md y characters/naia-cruz/piloto-001-agencia.md.
Vamos a producir un reel DIARIO nuevo para [CLIENTE/agencia] sobre [TEMA/OFERTA].
1. Elige el mejor hook de tools/hook-lab/clients/[cliente]/hooks.json (o genera batería nueva con la skill hook-lab si no existe).
2. Escribe el guion segmentado (4 segmentos, ~50 palabras, fórmula HOOK→AGITAR→PRUEBA→CTA).
3. Genera el audio master con ElevenLabs (voz Naia, settings del piloto: stability 0.45/similarity 0.8/style 0.35 — y el CTA a speed 1.08 si sale lento), córtalo por frases con Whisper y dame los trozos.
4. Dame los prompts de imagen para ChatGPT (adjuntaré el character sheet) y los prompts LTX por segmento (estilo selfie handheld, canon del piloto).
5. Cuando te pase los MP4 de LTX: ensambla (concat + audio master + overlays con la plantilla cara-libre) y entrégame el reel final.
Regla: nunca cubrir el rostro con captions. Nunca gastar API sin avisarme.
```

**Tu parte manual (lo único que el agente no puede):**
1. Generar las imágenes en ChatGPT Plus (pegar prompts + character sheet adjunto) → guardarlas
2. Correr los segmentos en ComfyDeploy **LTX Director v30**: imagen + su mp3 + su prompt · **CFG 1.2 · 30fps (o 25 si el deployment no deja) · 576×1024+ · duración = audio +0.3s** · b-roll SIN audio
3. Descargar los MP4 y decirle al agente dónde están

## Reglas de oro (no negociables)
- Segmentos de avatar hablando: **5-10s máx** (el lipsync degrada; el b-roll resetea)
- UN audio master para todo el guion; los clips LTX se generan con su trozo; el master se pega al final
- La cara del talento NUNCA se cubre con texto (plantilla ya lo respeta — no revertir)
- Cada post lleva scorecard con hipótesis ANTES de publicar (Regla 0)
- Todo lo aprendido se comitea al repo — el repo es el cerebro, las máquinas son desechables

## Costos por reel (referencia)
2-3 imágenes GPT (Plus: $0) · ElevenLabs ~300-600 créditos · LTX en pod ~$0.15-0.60 · resto local $0.
