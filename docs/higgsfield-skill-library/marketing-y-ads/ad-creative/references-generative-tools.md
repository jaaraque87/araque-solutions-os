---
source: ad-creative / references/generative-tools.md
extracted: modal (via claude-in-chrome)
---

# Generative AI Tools for Ad Creative

## Cuándo usar cada tipo
| Necesidad | Categoría | Mejor opción |
|---|---|---|
| Imágenes estáticas (banners, social) | Image gen | Nano Banana Pro, Flux, Ideogram |
| Imágenes con texto overlay | Image gen (text-capable) | Ideogram, Nano Banana Pro |
| Video corto (6-30s) | Video gen | Veo, Kling, Runway, Sora, Seedance |
| Video con voiceover | Video + voz | Veo/Sora (nativo) o Runway + ElevenLabs |
| Voiceover | Voice gen | ElevenLabs, OpenAI TTS, Cartesia |
| Multi-idioma | Voice gen | ElevenLabs, PlayHT |
| Clonar voz de marca | Voice gen | ElevenLabs, Resemble AI |
| Mockups/variaciones producto | Image + refs | Flux (multi-image reference) |
| Video templated a escala | Code-based | Remotion |

## Imagen
- **Nano Banana Pro (Gemini):** fuerte render de texto en imagen, edición nativa. API Gemini. `gemini-2.5-flash-image`.
- **Flux (BFL):** fotorrealismo, multi-image reference (hasta 8) para identidad consistente. Variantes: Flux 2 Pro (~6s, $0.015/MP, producción) · Flex (~22s, $0.06/MP, edición) · Dev (~2.5s, $0.012/MP, prototipado) · Klein (más rápido/barato, batch).
- **Ideogram:** el mejor en **tipografía/texto** (~90% precisión vs ~30% otros), style reference (3 imgs), presets de marca.
- Otras: DALL-E 3 (OpenAI), Midjourney (sin API oficial), Stable Diffusion (open source, self-host).

## Video
| Tool | Max | Audio | Res | API | Mejor para |
|---|---|---|---|---|---|
| Veo 3.1 | 60s | nativo | 1080p/4K | Gemini | Social vertical |
| Kling 2.6 | 3 min | nativo | 1080p | terceros | Cinemático largo |
| Runway Gen-4 | 10s | — | 1080p | oficial | Consistencia controlada |
| Sora 2 | 60s | nativo | 1080p | oficial | Diálogo |
| Seedance 2.0 | 20s | nativo | 2K | oficial+terceros | Alto volumen barato, hasta 12 refs |
| Higgsfield | varía | sí | 1080p | web | Social, 50+ movimientos de cámara |

## Voz
- **ElevenLabs:** líder, 29+ idiomas, clonación (instant/pro), control emoción, streaming. ~$0.12-0.30/1K chars.
- **OpenAI TTS:** simple/barato, 13 voces, sin clonación. ~$0.015-0.030/1K.
- **Cartesia Sonic:** ultra baja latencia (40ms), expresividad (risas, respiración). ~$0.03/min.
- **Voicebox (open source, local, gratis):** clonación con Qwen3-TTS, on-device, REST local.
- Otras: PlayHT (900+ voces, 140+ idiomas), Resemble AI (enterprise/on-prem), WellSaid (comercial-safe), Fish Audio (barato), Murf, Google Cloud TTS, Amazon Polly.
- **Workflow voz+video:** guion (ad-creative) → VO (ElevenLabs/OpenAI) → video (Runway/Remotion silencioso + track, o Veo/Sora/Seedance con audio nativo) → combinar con ffmpeg → variaciones.

## Remotion (video por código)
Determinista, pixel-perfect, control total de marca, batch de cientos desde datos, personalización (nombres/precios/stats). React+TypeScript. Casos: ads dinámicos de producto (JSON→video c/u), A/B de variaciones, outreach personalizado, batch multi-aspect (1:1 feed, 9:16 stories, 16:9 YouTube).

## Costo para 100 variaciones
100 imágenes: Nano Banana ~$4-24 · Flux Dev ~$1-2 · Ideogram ~$6. 100 videos 15s: Veo 3.1 Fast ~$225 · Remotion templated ~$0 (self-host). Híbrido Veo+Remotion ~$22 + render.

## Workflow recomendado (escala)
1. Hero creative con IA (Nano Banana/Flux/Veo). 2. Templates Remotion sobre patrones ganadores. 3. Batch de variaciones con data. 4. Iterar (IA para ángulos nuevos, Remotion para escala).

## Specs de imagen por plataforma
Meta feed 1:1 1080x1080 · Meta Stories/Reels 9:16 1080x1920 · Google Display 1.91:1 1200x628 / 1:1 1200x1200 · LinkedIn 1.91:1 1200x627 · TikTok 9:16 1080x1920 · Twitter 16:9 1200x675. (Incluir dimensiones en el prompt para no recortar.)
