# Canon de producción — Naia Cruz en LTX 2.3 Director

Flujo completo: GPT Image 2 (imagen) → ElevenLabs (audio master) → ComfyDeploy LTX Director (animación+lipsync) → ensamblaje → overlays de marca (content-reel-lab). Formatos: **DIARIO** (15-20s) y **SECUENCIA** (30-60s multi-escena).

---

## 1. La regla de oro del lipsync (arquitectura anti-drift)

El lipsync de LTX 2.3 degrada con la duración. Datos del canon NORA: TodoEnUno óptimo **8-10s**, VideoFlow I2V **6-8s**, CFG 1.2 (1.5 ya causaba slow-motion en videos largos). Por eso NUNCA se genera un clip hablado de 20s — se generan **segmentos de avatar de 5-10s** y el b-roll absorbe el resto:

```
AUDIO MASTER (ElevenLabs, UNA generación para todo el guion — prosodia natural, voz consistente)
   ↓ se corta por frases (ffmpeg, timestamps de Whisper local)
SEG 1: avatar habla (5-8s)  ← LTX Director CON audio del segmento (lipsync fresco)
SEG 2: b-roll producto (3-5s) ← LTX/imagen SIN lipsync (la voz sigue encima = voiceover)
SEG 3: avatar habla (5-8s)  ← lipsync se RESETEA aquí (nuevo clip, cero drift acumulado)
SEG 4: b-roll proceso/resultado (3-5s)
SEG 5: avatar CTA (4-6s)
   ↓ concat ffmpeg + PISTA DE AUDIO = el master completo (se descarta el audio por-segmento para evitar costuras)
   ↓ render-ltx-avatar-original-audio.mjs → overlays hook/CTA/handle
```

**Por qué funciona:** cada corte a b-roll oculta cualquier deriva y cada regreso del avatar arranca lipsync desde cero. Es el truco de los editores UGC humanos — el corte no es una limitación, ES el lenguaje del formato (retención por cambio visual cada 3-5s).

**Transiciones:** formato DIARIO = corte duro (nativo UGC, gratis, cero riesgo). Formato SECUENCIA = transiciones generadas por LTX Director (whip pan, match cut descritos en prompt) solo entre escenas del mismo entorno.

## 2. Formato DIARIO (15-20s) — la fórmula que convierte

Estructura validada contra los datos del radar (swipe.md 2026-07-04):

| Beat | t | Contenido | Fuente |
|---|---|---|---|
| HOOK | 0-2.5s | Avatar, spoken hook patrón "Hace unos días..." o "Voy a [experimento]" + overlay ≤8 palabras + visual hook (styling) | los 2 openers dominantes del nicho (1.8M/815K views) |
| AGITAR | 2.5-7s | B-roll: el problema/producto en pantalla, voz encima | cambio visual = retención |
| PRUEBA | 7-13s | Avatar de vuelta (lipsync fresco) con la cifra/resultado, o b-roll del resultado | especificidad numérica (patrón #4) |
| CTA | 13-18s | Avatar, mirada directa, UNA sola acción ("Escríbeme UGC al DM") | modo CONVERSIÓN: un CTA, cero ambigüedad |

3-4 segmentos LTX por video. Guion total: ~45-55 palabras (3 wps).

## 3. Formato SECUENCIA (30-60s) — especializado/campaña

Mismo principio, 6-10 segmentos, arco completo: hook → contexto → 2-3 pruebas/escenas de producto → objeción muerta → CTA. Aquí sí: cambios de outfit/escenario por escena (cada uno = nueva imagen GPT + nuevo clip LTX de 5s), transiciones LTX descritas, y re-hook a mitad ("y aquí viene lo que nadie te dice...").

## 4. Imágenes GPT Image 2 — Naia + factor "detiene el scroll"

**Línea física canónica (SIEMPRE, textual):** `A young woman in her mid-twenties, short sleek black bob hair, hazel green eyes, pale warm olive skin, curvy hourglass figure, gold "N" initial necklace`

**Factor fit/atractiva SIN vulgar — vocabulario aprobado:**
- Wardrobe: `fitted athletic wear`, `high-waist leggings and fitted crop top`, `elegant bodycon midi dress`, `fitted blazer over silk top`, `activewear set` — ropa que marca la silueta, nunca lencería/explícito en contenido de agencia
- Pose/energía: `confident posture`, `athletic graceful stance`, `soft knowing smile`, `direct eye contact` — magnetismo por seguridad, no por piel
- La vestimenta SE ADAPTA a lo promocionado: gym/wellness → activewear; SaaS/servicios → office siren (blazer fitted); restaurante/lifestyle → bodycon casual elegante
- ⚠ Regla de coherencia comercial: el styling atractivo es el VISUAL HOOK para audiencia masculina — usarlo cuando el comprador del producto es hombre o mixto; si el avatar comprador es mujer, cambiar a styling aspiracional (ella quiere SER Naia, no mirarla)

**Template imagen (image-to-image con character sheet como referencia):**
```
UGC-style photo, vertical 2:3 portrait, shot on iPhone. [LÍNEA FÍSICA NAIA]. Wearing [OUTFIT según campaña]. [POSE: standing confidently / sitting on stool leaning slightly forward / mid-gesture talking to camera]. [ESCENARIO acorde al producto, realistic lived-in space, organic asymmetrical background]. Natural daylight / warm indoor light, bright even exposure, natural skin tones, skin pores visible, authentic UGC feel, no studio look.
```

**Costos GPT Image 2 (API, verificado 2026-07):** portrait quality medium ≈ **$0.041/imagen**, high ≈ $0.165. Con Batch API: -50%. Presupuesto real por video DIARIO (2-3 imágenes medium): **~$0.10-0.15**. Secuencia (5-8 imágenes): ~$0.25-0.50. El character sheet como imagen de input suma centavos (input tokens $8/M). Regla: medium para iterar, high solo para la imagen ganadora.

## 5. Prompts LTX Director por segmento

**Segmento AVATAR (con lipsync)** — usar template TodoEnUno/Director de la skill nora-prompt-ltxvideo con estos anclajes fijos:
- `Shot on iPhone 16 Pro Max, 4K Cinematic mode` + `Vertical frame, close-up portrait, face in upper third`
- Línea física Naia textual + outfit IGUAL al de la imagen de referencia
- `Speaking in Latin American Spanish with a [confident/warm] tone. "[frase exacta del segmento]"` — el fragmento entre comillas mejora el lipsync
- Acting beats entre frases (`She pauses, glances briefly aside, then back at lens`)
- Cámara: `Absolutely static locked-off camera` (diario) o `very slow subtle dolly-in barely one meter` (énfasis)
- Cierre: `Her lips move clearly matching the audio`
- Duración del prompt proporcional: 5s → 3-4 oraciones; 8-10s → 7-8 oraciones

**Segmento B-ROLL producto (sin lipsync):**
```
[Cinematic/UGC] shot of [producto] on [superficie/contexto], vertical frame. [Luz]. The camera slowly [pushes in / orbits] revealing [detalle]. [1 elemento atmosférico]. No text, no logos animados.
```
Física simple solamente: nada de líquidos rápidos, saltos ni multi-objeto (artefactos).

**Negativos universales:** `no extra limbs, no face warp, no object duplication, no text artifacts, no watermark, no flicker, no camera shake, no multiple people`

## 6. Ensamblaje (post-LTX)

```bash
# 1. concat de segmentos (lista en orden)
ffmpeg -f concat -safe 0 -i segmentos.txt -c:v libx264 -r 30 -pix_fmt yuv420p -an video_mudo.mp4
# 2. pegar el audio master completo
ffmpeg -i video_mudo.mp4 -i audio_master.mp3 -c:v copy -c:a aac -shortest video_full.mp4
# 3. overlays de marca
node tools/content-reel-lab/scripts/render-ltx-avatar-original-audio.mjs --video video_full.mp4 --hook "..." --cta "..."
```
Regla de cuadre: la suma de duraciones de segmentos debe igualar el audio master ±0.3s — cortar b-roll, nunca el avatar hablando.

## 7. Costo total por video DIARIO (transparencia)

| Ítem | Costo |
|---|---|
| 2-3 imágenes GPT medium | ~$0.12 |
| Audio ElevenLabs (~55 palabras ≈ 300 chars) | ~300 créditos (~$0.03 equiv.) |
| 3-4 clips LTX (RunPod/ComfyDeploy) | según pod (~$0.15-0.60) |
| Whisper timestamps + ensamblaje + overlays | $0 (local) |
| **Total** | **≈ $0.30-0.80/video** |

Margen vs Servicio B ($497/60 videos = $8.28/video facturado): **>90%**.
