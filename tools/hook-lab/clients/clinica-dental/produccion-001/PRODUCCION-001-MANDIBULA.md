# Producción 001 — "¿Te truena la mandíbula?" (hook h03, score 9, respaldo 26K @UnDentista)
_Cliente: clínica dental/estética · Presentadora: **Dra. Camila Rey** (vocera propia del nicho — ver characters/dra-camila-rey/PERFIL.md; decisión 2026-07-12: Naia no presta la cara a voces ajenas) · Formato: corto <30s vertical (síntesis del radar: empezar CORTO) · 2026-07-12_

## Guion (método Kallaway: hook auto-diagnóstico + promesa rápida → romper normalización → CTA)
> "¿Te truena la mandíbula cuando abres la boca? Quédate... te lo explico en veinte segundos. Ese clic es tu articulación avisando que el disco no está en su lugar. Y si además se te traba, o te duele al masticar... eso NO es normal. La buena noticia: detectado a tiempo se trata fácil, sin cirugía. Hazte el chequeo... agenda tu valoración gratis, link en la bio."

~66 palabras ≈ 24-26 s. Overlay del hook (post/HyperFrames): **"¿te truena? mira esto"**.

## ⛔ BLOQUEO ACTUAL: audio
ElevenLabs devuelve `payment_issue` (factura fallida en la suscripción starter; créditos congelados: 76.605). **Acción del dueño**: completar el invoice en elevenlabs.io. La key y la voz (ELEVENLABS_VOICE_ID) están bien. Nota: `eleven_v3` por API dio 401 antes del payment_issue — al reactivar usar `eleven_multilingual_v2` por API (v3 solo web en starter).
Alternativa para no frenar: VO placeholder con Gemini Flash TTS (gratis, skill tts-ugc) para timing/prueba y swap a voz Naia después.

## Serie de prompts GPT Images 2 (generar en ChatGPT, retrato; luego Claude recorta TODOS a 1080×1920 EXACTO — regla naiatest1)
Sujeto fijo (pegar al inicio de CADA prompt):
> Ultra-realistic vertical portrait photo, 2:3. Naia Cruz: young woman 25-29, short sleek black bob with straight jaw-length ends, olive green hazel eyes, pale olive skin with warm undertone and realistic skin texture with visible pores, natural full lips, small gold hoop earrings, delicate gold "N" pendant necklace, natural glowy makeup. Wearing a clean white medical-adjacent blouse (smart casual, NOT a doctor coat). Modern bright dental clinic interior, soft daylight, shallow depth of field, shot on 50mm. No text anywhere.

| # | Escena (segmento del guion) | Prompt variable (añadir tras el sujeto) |
|---|---|---|
| S1 | Hook: "¿Te truena la mandíbula...?" | She faces the camera in medium close-up, one hand touching her jaw near the ear, mouth slightly open as if testing the joint, curious raised-eyebrow expression, direct eye contact. |
| S2 | "Quédate... te lo explico en 20 segundos" | Medium close-up, she speaks to the camera with confident warm energy, small inviting hand gesture toward the lens, clinic reception blurred behind. |
| S3 | "Ese clic es tu articulación... el disco no está en su lugar" | Medium shot, she points with two fingers to the jaw joint area in front of her ear, explanatory expression, slight head turn showing profile line of the jaw. |
| S4 | "Se te traba o te duele... eso NO es normal" | Close-up, serious concerned expression, subtle head shake, direct intense eye contact with the camera, darker corner of the clinic behind. |
| S5 | "Se trata fácil... agenda tu valoración gratis" | Medium close-up, big genuine warm smile, relaxed shoulders, welcoming energy at the bright clinic front desk, direct eye contact. |

## Timeline del Builder (cuando exista el audio)
1. Medir el VO con faster-whisper (word timestamps) → cortar las 5 escenas EXACTO en los límites de frase de arriba (~4-6 s c/u).
2. Builder: `Speaking (short film)` / I2V · **1080×1920 Portrait — VERIFICAR altura > ancho** · resize fit/contain · ref strength 1.0 · bypass image=false · LoRA talkvid 0.8 · FPS 24 · una imagen 9:16 recortada por escena · el VO completo (el Builder lo parte por escena con LoadAudioSplit).
3. Prompt base y negativo: los del HANDOFF-BUILDER-DEBUG + añadir al prompt `olive green eyes` y al negativo `duplicated necklace, floating letters, extra jewelry` (defectos de naiatest1).
4. Quick Save + descargar output + apagar L40S (presupuesto ~$15).

## Post (HyperFrames)
Overlay del hook 0.0-2.5s, captions por frase, CTA final con texto "VALORACIÓN GRATIS → link en bio". SFX: click/pop en el "clic" de la articulación (skill sfx-ugc, library-first).
