# PILOTO 004 — "7 MARAVILLAS" (formato SECUENCIA, ~48s, multi-shot por ejecución)

**Concepto:** Naia "recorre" las 7 maravillas en un día. Cada parada = dato curioso a cámara + toma dron/zoom de la maravilla. Cierre de INTRIGA (no venta): ella nunca salió de casa. Pieza de portafolio/awareness para @araquesolutions.

**Hipótesis del scorecard:** el formato viaje+datos retiene por curiosidad serial (cada maravilla es un re-hook) y el reveal final convierte awareness en DMs sin CTA de venta dura. Métricas: retención >40% al s30, saves/shares (formato coleccionable), DMs espontáneos.

## ⚠ ARQUITECTURA — el límite real del nodo (NO negociable)

**PROHIBIDO intentar los 48s en una sola ejecución:** lipsync degrada >8-10s, la identidad deriva, un seed malo mata todo, y la regla vigente es máx 15s por ejecución.

**El "exprimir" correcto = MULTI-SHOT DENTRO de cada ejecución (~7s):**
```
UNA ejecución LTX Director por parada:
  SHOT 1 (4-4.5s): Naia selfie en la locación, dice el dato (lipsync)
  → transición descrita en el prompt (whip pan / snap zoom)
  SHOT 2 (2.5-3s): toma dron/zoom de la maravilla, la voz REMATA encima (VO)
Audio input = el trozo completo de la parada (lipsync aplica mientras hay cara; el dron absorbe la cola en voiceover)
```
Entre paradas: **corte duro** en el ensamblaje (canon: transiciones LTX solo dentro del mismo entorno). El corte duro ES el ritmo listicle.

**GATE DE VALIDACIÓN:** producir SOLO la ejecución de las pirámides primero. Si el multi-shot interno (cara→dron) sale limpio, se producen las otras 8. Si LTX no aguanta el cambio de escena interno, plan B: 2 ejecuciones por parada (Naia 4s + dron 3s por separado, pipeline estándar piloto-002) = mismo reel, más renders.

## Guion (~130 palabras ≈ 45-48s, eleven_v3 + audio tags, UNA generación master)

| # | Parada | Frase (dato en tuteo) | Estructura |
|---|---|---|---|
| H | HOOK (Naia, look viajera, fondo neutro/aeropuerto) | "[upbeat] Recorrí las siete maravillas del mundo en un solo día... y sin tomar un solo avión. Mira." | solo Naia, 5s |
| 1 | Pirámides de Giza | "[curious] Las pirámides eran blancas. Brillaban tanto que se veían a kilómetros." | Naia→dron 3 pirámides |
| 2 | Gran Muralla | "[amazed] La Muralla mide veintiún mil kilómetros... y aun así no se ve desde el espacio." | Naia→dron muralla serpenteando |
| 3 | Petra | "[hushed] Petra estuvo perdida quinientos años. Una ciudad entera, tallada en la roca." | Naia→zoom out del Tesoro |
| 4 | Coliseo | "[casual] El Coliseo se llenaba en quince minutos. Mejor que muchos estadios de hoy." | Naia→dron orbital lejano |
| 5 | Taj Mahal | "[warm] El Taj Mahal cambia de color tres veces al día. Es una carta de amor." | Naia→zoom in fachada |
| 6 | Machu Picchu | "[impressed] Machu Picchu se construyó sin ruedas y sin cemento. No se ha movido ni un milímetro." | Naia→dron revelando la ciudadela |
| 7 | Chichén Itzá | "[playful] Y en Chichén Itzá, dos veces al año, la pirámide dibuja una serpiente de luz." | Naia→zoom escalinata |
| C | CTA INTRIGA (Naia, mismo fondo del hook) | "[soft laugh] Y aquí el detalle... yo nunca salí de mi casa. Nada de esto lo filmó una cámara. [pause] Piénsalo." | solo Naia, 6s |

Overlays: hook `7 maravillas · 1 día · 0 aviones` · por parada: chip con el nombre (`GIZA, EGIPTO`) · CTA `nada de esto fue filmado` + @araquesolutions. Nunca sobre el rostro.

**Audio:** modelo `eleven_v3` + tags vía `/with-timestamps` (AGENTS.md #9), UNA generación master, cortar por paradas con el alignment. ~700-800 créditos. NO generar sin aprobación del usuario.

## Imágenes GPT (8 first frames, character sheet SIEMPRE adjunto)

**UN solo outfit viajera en TODAS** (consistencia de identidad > variedad): `fitted black athletic top, light utility jacket tied at waist, small crossbody bag, gold "N" necklace`. Solo cambia el fondo.

**Template Naia-en-locación (IMG-1 a IMG-7 + hook):**
```
UGC-style selfie photo, vertical 9:16, waist-up, one extended arm holding the camera. Use the attached character sheet for exact facial identity: young woman mid-twenties, short sleek black bob, hazel green eyes, pale warm olive skin, curvy hourglass figure, gold "N" initial necklace. Wearing a fitted black athletic top with a light utility jacket tied at her waist and a small crossbody bag. Standing at [LOCACIÓN + detalle: "the Giza plateau, the three pyramids clearly visible behind her in warm morning light"]. Golden hour / bright daylight, natural skin texture with visible pores, authentic travel vlog feel, 24mm selfie look. Tourists blurred in the far background. No text, no plastic skin.
```
Variar solo el bloque [LOCACIÓN]: Giza (meseta, 3 pirámides), Gran Muralla (torre vigía, muralla serpenteando), Petra (frente al Tesoro), Coliseo (interior con gradas), Taj Mahal (jardín frontal con reflejo), Machu Picchu (terrazas con Huayna Picchu), Chichén Itzá (explanada de El Castillo). Hook/CTA: fondo neutro cálido (habitación con maleta abierta).

## Prompt LTX Director multi-shot (template por parada)

**PARADA N — IMG-N + `segN.mp3` → duración = mp3 + 0.3s (~7s) · CFG 1.2 · 30fps:**
```
Shot on iPhone 16 Pro Max, 4K Cinematic mode, travel vlog style, vertical 9:16.
SHOT 1: Selfie video, close-up, face in upper third. A young woman in her mid-twenties, short sleek black bob hair, hazel green eyes, pale warm olive skin, gold "N" initial necklace, fitted black athletic top and light utility jacket, holding the camera with one extended arm at [LOCACIÓN, misma descripción de la imagen]. She is talking directly to the camera with excited travel-vlogger energy. Speaking in Latin American Spanish with a [TONO] tone. "[FRASE EXACTA]". Her mouth articulates every word clearly, lips moving in sync with the audio while she is on screen.
Then a fast whip pan transition to
SHOT 2: sweeping aerial drone shot of [MARAVILLA: "the three pyramids of Giza rising from the desert, long morning shadows"], cinematic wide angle, the camera [MOVIMIENTO: slowly pushing forward / orbiting wide / pulling back to reveal]. Natural documentary color, crisp daylight.
Subtle handheld feel in shot 1, smooth stabilized motion in shot 2. Natural skin texture. Vertical 9:16.
```
**Negativos (todas):**
```
no extra limbs, no face warp, no identity change, no multiple people in shot 1, no object duplication, no text artifacts, no watermark, no flicker, no distorted architecture, no melted landmarks, no warped monuments
```
HOOK y CTA: ejecución simple de un solo shot (sin transición), prompt estilo piloto-002 SEG4.

## Ensamblaje

Igual al piloto-002: recortar cada clip a la duración EXACTA de su trozo (trim en filter_complex, lección validada), concat con corte duro, pegar master v3, overlays content-reel-lab (`HYPERFRAMES_CLI` + cache off en Windows). Música: NO en v1 (la voz + ambiente manda; si pide música, `music-ugc` instrumental bajo).

## Costos estimados
8 imágenes GPT (Plus $0) · audio ~700-800 créditos · 9 ejecuciones LTX ~7s (pod) · ensamblaje $0. **Producir 1 (pirámides) → validar → producir 8.**

## Orden de producción
1. Usuario aprueba guion/hook → 2. Audio master v3 (con OK) + cortes → 3. IMG pirámides + IMG hook → 4. **GATE: ejecución pirámides** → 5. QA juntos → 6. Si pasa: 6 imágenes restantes + 6 ejecuciones + hook/CTA → 7. Ensamblaje + overlays → 8. Scorecard + publicar.
