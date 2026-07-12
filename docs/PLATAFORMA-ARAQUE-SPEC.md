# PLATAFORMA ARAQUE — Especificación fundacional (dictada por el dueño, 2026-07-12)

## Principio rector: RESEARCH-FIRST, 0 ejecuciones sin sentido
El research es el paso MÁS importante y MEDIBLE. Ninguna campaña ni generación de contenido
por cliente se ejecuta sin hechos sólidos comprobados. El flujo lo IMPONE la plataforma:
**radar del nicho (niche-radar, datos verificables) → swipe file → hooks generados y
puntuados (hook-machine/Kallaway) → selección basada en score+respaldo → SOLO ENTONCES producción.**
Caso validado de referencia: clinica-dental (radar 2 canales → 10 hooks puntuados → h03 → Producción 001).

## Qué es
App estilo NORA (Supabase como cerebro de estado + motores detrás) donde un cliente o un
operador SIN conocimientos técnicos produce videos UGC completos:
1. **Elige personaje** (Naia, Kenza, Dra. Camila Rey, o vocera nueva por nicho — regla: cada
   nicho su vocera con VOZ ANCLADA; Naia no presta la cara)
2. **Elige voz** (anclada al personaje: Gemini TTS voces / ElevenLabs clones)
3. **Elige estilo/formato** (UGC natural estático de confianza · Director cinemático · restyle omni)
4. **Aporta assets o pide pipeline completo** (guion desde research → TTS → imágenes por
   escena → render → post)
5. La plataforma ejecuta y entrega + métricas de conversión por pieza

## Motores ya probados que envuelve (estado real)
- **V9 Video Builder** (vrgamedevgirl, máquina v34+: parches propios null-workflow + metadata) —
  multi-escena i2v con audio nativo/lipsync. Receta validada: naiatest1 + kit Producción 001.
- **MVC** (Prompt Creator + I2V V5.2) — talking-heads con lipsync desde un VO (probado 5-jul).
- **TAO Director V2 / Camera Lab** — tomas cinemáticas sin diálogo (bug staging remoto audio pendiente).
- **HyperFrames** — post: captions, overlays, SFX, mix.
- **Research**: niche-radar (gratis, yt-dlp) + hook-machine (Kallaway) + swipe files por cliente.
- **TTS**: tts-ugc (Gemini, gratis) + ElevenLabs (Naia/Kenza; hoy con payment_issue).
- **Sesiones ComfyDeploy por API** (tunnel_url de GET /api/session/<id>) — GPU bajo demanda.

## Reglas operativas heredadas (pagadas con errores)
- Referencias SIEMPRE 9:16 exacto pre-recortado · altura > ancho verificado antes de lanzar
- Escenas ≤ ~9-10s · cortes de audio SOLO en límites de palabra (whisper word-timestamps)
- Voz≠cara jamás (credibilidad) · sin joyas en voceras clínicas (artefactos)
- Presupuesto: sesiones GPU solo al ejecutar, apagar al terminar, gasto con OK del dueño
- Todo hallazgo se commitea al repo (cerebro compartido Claude/Codex)

## Ruta MVP
1. **Fase A (manual asistida — HOY)**: kits de producción por cliente (como CAMILA-PROD001-KIT) +
   checklists; el operador ejecuta el Builder en sesión.
2. **Fase B**: orquestador headless del Builder (replicar su submission por API contra el túnel;
   los parches v34 ya garantizan metadata válida) + fix staging remoto Camera Lab.
3. **Fase C**: UI web (patrón NORA/Camera Lab server: Python liviano + frontend + Supabase) con
   los 5 pasos del cliente, gate de research obligatorio y dashboard de métricas/conversión.
