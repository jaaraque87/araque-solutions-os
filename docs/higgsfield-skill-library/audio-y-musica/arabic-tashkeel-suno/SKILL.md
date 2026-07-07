---
name: arabic-tashkeel-suno
title: "Arabic Tashkeel Suno"
author: curatedchaos
category: Writing-suite
version: v2
users: 4
source: https://higgsfield.ai/supercomputer/marketplace/skills/38eb047f-6b6b-443e-ab4a-5a1ab5fc795d
extracted: modal SKILL.md (via claude-in-chrome) — single file
nota: muy nicho (letras en árabe para música IA). Experto en tashkeel (diacritización) dialect-accurate.
---

# Arabic Tashkeel for AI Music (v2: Dual-Track + TTS Verification)
Procesa letras en árabe crudo para herramientas de música IA (Suno, Udio) que son TTS-adjacent. **Tashkeel solo no garantiza** pronunciación correcta → produce TRES outputs paralelos: (1) Tashkeel track (para tools que respetan harakat), (2) Arabizi/Latin track (Suno a veces pronuncia mejor el script latino), (3) Risk audit (flag de cada palabra ambigua).

## Por qué existe
Los generadores predicen pronunciación de patrones de texto; el árabe omite vocales (harakat) → `كتب` puede ser "kutub"/"katab"/"kutiba". Con tashkeel `كَتَبَ` = "katab". Dual-track deja al usuario elegir la mejor toma.

## Dialect Map (identificar/preguntar antes; default música = Egyptian EG)
Egipcio (ج=g, ق=', ث=s, ذ=z, sin tanwin) · Levantino (ق=' o q, consonantes suaves) · Golfo Khaleeji (ج=y/j, ق=g) · Maghrebi (clusters, influencia francesa) · MSA/Fusha (reglas clásicas, tanwin).

## Pipeline (5 layers)
1. **Dialect-aware tashkeel:** harakat completos por reglas del dialecto (ej egipcio: quitar tanwin, ج=g, ق=hamza, sukun en todo consonante sin vocal). Marcas: fatha ـَ (a), damma ـُ (u/o), kasra ـِ (i/e), sukun ـْ, shadda ـّ (doble). Verificar: cada consonante con haraka o sukun.
2. **Arabizi/Latin (co-equal, no fallback):** convención egipcia Suno-tested (ح=H, ع=3, ق=2/q, ص=S, etc.). Mayúscula para enfáticas (H,S,D,T,Z), 3 para ع, 2 para hamza. Testear con y sin numerales.
3. **Per-word risk audit:** 🟢 Low (una pronunciación) · 🟡 Medium (dialecto cambia, tashkeel resuelve) · 🔴 High (múltiples lecturas o falla conocida de Suno → testear en Google Translate TTS antes de generar). High-risk típicos: palabras con ق, ج, shadda que la IA salta, slang, ع (Suno lo dropea).
4. **TTS verification:** por cada línea, generar URL `https://translate.google.com/?sl=ar&tl=en&text={URL_ENCODED_TASHKEEL}&op=translate` — el usuario oye y confirma.
5. **Suno/Udio optimization:** structure tags ([Verse]/[Chorus]/[Bridge]), language lock ("All lyrics in Arabic, no English"), máx 8-10 palabras/línea, coros idénticos, dos bloques Suno-ready (tashkeel + arabizi).

## Output Format v2
Header (Dialect, Tool, Risk summary) · Line-by-line breakdown (Raw / Tashkeel / Arabizi / Risk / TTS test URL) · Flagged words (verificar primero, con alternativas) · SUNO-READY BLOCK A (tashkeel) · BLOCK B (arabizi) · Recommended test protocol.

## Edge Cases
IA aún mispronuncia → phonetic respelling ("ha-BEE-bee"). Mezcla de dialectos → section labels ([Verse - Egyptian]/[Bridge - MSA]). Slang → tashkeel por pronunciación real + flag 🔴. Mahraganat (denso) → líneas cortas + [Break], arabizi más importante. Suno canta phonemes en inglés → forzar "Arabic vocals, no English, native pronunciation" en style; probar bloque arabizi.

## Integración
music-video-director (lyric sync) · album-art-director (text overlay) · seedance-prompt-builder (lip-sync).
