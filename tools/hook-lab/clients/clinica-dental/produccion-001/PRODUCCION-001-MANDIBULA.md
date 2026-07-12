# Producción 001 — "¿Te truena la mandíbula?" (hook h03, score 9, respaldo 26K @UnDentista)
_Cliente: clínica dental/estética · Presentadora: **Dra. Camila Rey** (vocera propia del nicho — ver characters/dra-camila-rey/PERFIL.md; decisión 2026-07-12: Naia no presta la cara a voces ajenas) · Formato: corto <30s vertical (síntesis del radar: empezar CORTO) · 2026-07-12_

## Guion (método Kallaway: hook auto-diagnóstico + promesa rápida → romper normalización → CTA)
> "¿Te truena la mandíbula cuando abres la boca? Quédate... te lo explico en veinte segundos. Ese clic es tu articulación avisando que el disco no está en su lugar. Y si además se te traba, o te duele al masticar... eso NO es normal. La buena noticia: detectado a tiempo se trata fácil, sin cirugía. Hazte el chequeo... agenda tu valoración gratis, link en la bio."

~66 palabras ≈ 24-26 s. Overlay del hook (post/HyperFrames): **"¿te truena? mira esto"**.

## ✅ AUDIO RESUELTO — voz ANCLADA de la Dra. Camila Rey
`vo_mandibula_gemini.mp3` (28.52s, Gemini TTS "Leda", 6 segmentos, loudnorm -16). Duraciones por escena: S1 2.68 · S2 3.28 · S3 5.80 · S4 6.64 · S5a+S5b 10.12 (partido en ~5.06+5.06 — regla >10s). La voz Leda ES la voz canónica del personaje (ver characters/dra-camila-rey/PERFIL.md) — NO se cambia a ElevenLabs.
(Nota histórica: ElevenLabs quedó con payment_issue — invoice pendiente del dueño; solo afecta a las voces de Naia/Kenza.)

## Serie de prompts GPT Images 2 (generar en ChatGPT, retrato; luego Claude recorta TODOS a 1080×1920 EXACTO — regla naiatest1)
Sujeto fijo (pegar al inicio de CADA prompt):
> Ultra-realistic vertical portrait photo, 2:3 aspect ratio. Dra. Camila Rey: professional Latina dentist, woman 31-34 years old, honey-brown hair in a sleek low ponytail with a clean middle part, warm brown eyes, light tan skin with realistic texture and visible pores, natural minimal makeup, small stud earrings, NO necklace. Wearing modern fitted teal medical scrubs with a small name tag. Modern bright dental clinic interior, soft daylight, shallow depth of field, shot on 50mm lens. Credible, warm but clinical presence. No text anywhere in the image.
>
> TRUCO: generar primero la IMG neutra (S2) y adjuntarla como referencia para las otras 5 (misma cara garantizada). 6 imágenes: S1-S5 de la tabla + IMG6 CTA (front desk, sonrisa, gesto hacia abajo señalando el link).

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
3. Prompt base y negativo: los del HANDOFF-BUILDER-DEBUG + añadir al prompt `warm brown eyes, honey-brown low ponytail, teal scrubs` y al negativo `necklace, jewelry, duplicated necklace, floating letters, black bob` (identidad Camila + defectos de naiatest1).
4. Quick Save + descargar output + apagar L40S (presupuesto ~$15).

## Post (HyperFrames)
Overlay del hook 0.0-2.5s, captions por frase, CTA final con texto "VALORACIÓN GRATIS → link en bio". SFX: click/pop en el "clic" de la articulación (skill sfx-ugc, library-first).
