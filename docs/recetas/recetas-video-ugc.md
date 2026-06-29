# Recetas probadas — Video UGC Araque

Prompts y parámetros validados en producción. Ver también `tools/fal-jobs/` y `brand/araque/BRAND.md`.

## División de trabajo (tooling)
- **Generación = setup propio del usuario:** flujo UGC en ComfyDeploy (resolución configurable) + **LTX Director** (multi-frame/escenas) + GPT Image 2. Talking-heads salen de aquí ($0/pieza).
- **fal.ai = solo wow/física imposible** en LTX (ej. hamburguesa volando + terremoto). Pay-per-gen.
- **Post-producción/marca = FFmpeg + HyperFrames:** grade, marca de agua, captions, cierre, montaje multi-clip.

## 1. Realismo iPhone (GPT Image 2) — el game-changer
Positivo: `shot on iPhone 16, handheld selfie/casual snapshot, natural available light, amateur UGC, slightly imperfect framing; HYPERREAL SKIN: visible pores, fine peach fuzz, subtle texture, natural imperfections, faint blemishes, uneven skin tone, light under-eye shadows, natural oil sheen on T-zone, flyaway baby hairs, real human skin, minimal makeup, subtle sensor noise/grain.`
Negativo: `airbrushed, smooth plastic/waxy skin, beauty filter, glossy, porcelain doll skin, perfect symmetry, CGI, 3D render, glamour studio lighting, model-perfect.`
Claves: generar CLOSE-UPS (el poro se ve en plano corto), pedir "real person, not a model", luz plana de teléfono (no rim light). **La IA obvia genera desconfianza** → realismo = argumento de venta. NUNCA gritar "IA" al cliente; vender resultados.

## 2. Seedance 2.0 image-to-video (fal) — física/wow
Endpoint `bytedance/seedance-2.0/image-to-video`. Params: `prompt`, `image_url`, `end_image_url` (opcional, interpola start→end), `duration` (entero 4-15), `resolution` ("720p"...), `aspect_ratio` ("9:16"), `generate_audio` (bool, da SFX+voz nativa), `bitrate_mode` ("high"). **NO existe `negative_prompt`** → negativos como cláusula `Avoid: ...` en el prompt. ~$0.30/s (720p). Estructura: shot-by-shot con timing `[0-3s]`, cámara, acción, física, audio. La voz nativa pronuncia mal marcas en inglés ("Solutions" → "socucions") → cortar antes o tapar con tarjeta de logo.

## 3. Kling image-to-video (fal) — movimiento de cámara sin deformar
`fal-ai/kling-video/v3/pro/image-to-video`. Solo cámara+vapor+luz (nada de manos/mordidas/órbita). Negativos: `orbiting to the back, 360 rotation, revealing the back, morphing, warping, deforming food, changing ingredients, extra patties`. ~$0.112/s.

## 4. Avatar/lip-sync hablado
- **Recomendado: setup LTX propio** (LTX Director one-bullet) — boca/dientes naturales, realista, $0. Subir resolución a 1080.
- **Modelos lip-sync open source** (en Comfy, $0): LatentSync (video+audio→re-sync), Sonic/Hallo2/MultiTalk (image+audio→habla).
- **fal (caro, archivado):** Kling AI Avatar v2 Pro ($0.115/s) — alta res pero boca gomosa; Kling LipSync a2v ($0.014/s).

## 5. Template LTX UGC v4 (talking head, image-to-video)
```
Shot on iPhone 16 Pro Max, 4K Cinematic mode. A [personaje + vestuario], handheld selfie indoors with soft natural window light. Medium close-up, looking into the lens, speaking directly to camera with warm confident energy and small natural hand gestures. Speaking in Latin American Spanish with a [tono] accent. "[1-2 frases del diálogo]". Lips move clearly matching the audio. Static framing, no zoom/push-in. [Realismo iPhone kit]. Background: lived-in interior, asymmetrical, soft bokeh, evenly lit. At the very end she stops speaking and gives a warm genuine smile to camera. Vertical 9:16.
```
Negativos: `no extra limbs, no face warp, no object duplication, no text artifacts, no warped logo, no watermark, no flicker, no rolling shutter wobble, no Dutch angle, no extreme motion blur, no camera shake, no jitter, no beauty filter, no plastic skin.`
Orden que prioriza LTX: Subject → Action → Camera → Lighting → Background → Constraints.

## 6. Color grade "Warm Clean" + captions CapCut
Ver `brand/araque/BRAND.md`. Grade FFmpeg: `eq=contrast=1.05:saturation=1.1:brightness=0.02,colorbalance=rm=0.05:bm=-0.05`. Captions `.ass` libass, tercio inferior, pop, magenta accent.

## 7. Estructura estándar de una pieza terminada
1. Talking-head/clip base (LTX/Kling/Seedance). 2. Grade de marca. 3. Marca de agua "A". 4. Captions CapCut sincronizados (no tapar la cara). 5. Cierre de marca (endcard). 6. Audio maestro mux con FFmpeg. 7. Para redes: audio en tendencia agregado IN-APP (no horneado, para que la plataforma lo atribuya).
