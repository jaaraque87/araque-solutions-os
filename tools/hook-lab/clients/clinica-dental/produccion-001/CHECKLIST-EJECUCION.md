# KIT PRODUCCIÓN 001 — Dra. Camila Rey · "¿Te truena la mandíbula?" (28.52s, 5 escenas)
_Ejecutar en el V9 Video Builder (sesión ComfyDeploy L40S, máquina v34+). Receta validada en naiatest1._

## Timeline (duraciones EXACTAS — el Builder parte el audio con estos números)
| Escena | Imagen (ya en 1080×1920) | Duración | Habla |
|---|---|---|---|
| 1 | esc1_hook_2.68s.png | **2.68** | "¿Te truena la mandíbula cuando abres la boca?" |
| 2 | esc2_explica_9.08s.png | **9.08** | "Quédate... 20 segundos" + "Ese clic es tu articulación..." |
| 3 | esc3_alerta_6.64s.png | **6.64** | "Y si además se te traba... eso NO es normal." |
| 4 | esc4_alivio_5.50s.png | **5.50** | "La buena noticia... se trata fácil, sin cirugía." |
| 5 | esc5_cta_4.62s.png | **4.62** | "Hazte el chequeo... valoración gratis, link en la bio." |
Audio completo: `vo_camila_28.52s.mp3` (suma = 28.52 ✓)

## Ajustes del Builder (NO negociables)
- Video Type: **Speaking (short film)** / I2V
- Resolución **1080×1920 Portrait 9:16 — VERIFICAR altura > ancho ANTES de lanzar**
- Resize: fit/contain (JAMÁS center-crop) · Reference strength **1.0** · bypass image **false**
- LoRA **talkvid 0.8** · FPS **24**
- Quick Save religioso · descargar output ANTES de cerrar · **apagar L40S al terminar** (~$15 de presupuesto)

## Prompt por escena (pegar; la parte fija va en global si el Builder lo permite)
FIJO (directiva del dueño: cámara natural UGC, cero movimientos bruscos, transmitir confianza):
> Vertical 9:16 natural UGC video. Preserve the exact framing and exact identity from the reference image. Her complete face fully visible from first to last frame. She speaks the supplied audio with precise natural lip sync, subtle blinking, minimal natural head movement. STATIC composition: no zoom, no camera tilt, no reframing, no camera movement — only the subtle breathing of a phone on a small tripod. Preserve warm brown eyes, honey-brown low ponytail, teal medical scrubs, natural skin texture. Trustworthy, calm, credible energy.

VARIABLE por escena: 1) curious expression, hand testing the jaw joint · 2) warm explanatory energy, small natural hand gesture · 3) serious concerned expression, subtle head shake on "NO es normal" · 4) relieved reassuring soft smile, calm open palm · 5) genuine warm smile, small downward point suggesting the link below.

NEGATIVO:
> subtitles, captions, text overlay, watermark, logo, necklace, jewelry, duplicated necklace, floating letters, black bob, zoom, camera tilt, reframing, camera movement, scene change, face outside frame, cropped face, partial face, face replacement, different woman, identity change, deformed face, bad hands, extra fingers, blurry, jittery, choppy
