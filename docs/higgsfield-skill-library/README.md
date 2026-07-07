# Skills de Higgsfield Supercomputer — Repositorio

**Ruta:** `A:\Proyectos Claude\Skill\skill-higgsfield`

Extracción del marketplace de skills de **Higgsfield Supercomputer** (`higgsfield.ai/supercomputer/skills`). Cada skill vive en `<categoría>/<slug>/SKILL.md`.

## Estado

| | Cantidad | Qué es |
|---|---|---|
| ✅ **Completas (descargadas al 100%)** | **68** | Skills de la **comunidad** — tenían botón **Manage** en el marketplace, así que su `SKILL.md` completo es público. El frontmatter incluye `extracted:`. |
| ❌ **No extraíbles (solo descripción)** | **30** | Skills **first-party oficiales de Higgsfield** — solo "Try Now", sin `SKILL.md` público (su lógica corre server-side). Solo quedó un stub con la descripción de la tarjeta. |
| **Total marketplace** | **98** | |

> **Cómo distinguirlas dentro del repo:** si el `SKILL.md` tiene `extracted: modal...` (o `extracted: contenido...`) en el frontmatter → contenido completo. Si dice `source: .../supercomputer/skills` sin `extracted:` (o `extracted: NO DISPONIBLE`) → stub first-party.

Varias skills completas referencian archivos `references/*.md` adicionales que **no** se extrajeron (se anota en el frontmatter de cada una).

---

## ✅ Las 68 skills completas — qué hace cada una

### 🖼️ generacion-imagen (7)
- **higgsfield-prompt-architect** — Guía de selección de modelo, estructuración de prompts y diagnóstico de fallas de generación en Higgsfield.
- **soul-character-studio** — Arquitecto de personajes Soul ID: audita fotos de referencia, arma un Character Bible y da plantillas por escena para consistencia de personaje.
- **gpt-image-2-director** — Director de prompts para GPT Image 2 (imagegen_2_0): retratos, posters, character sheets, UI mockups.
- **asset-extraction** — Genera/extrae elementos UI, cards u objetos con fondos transparentes nítidos.
- **vinyl-print-graphics** — Diseños vector-compatibles para HTV/vinilo/serigrafía/stencil (áreas planas de tinta sólida, sin gradientes).
- **cod-ultimate-thumbnail** — Pipeline de miniaturas de Call of Duty (render 3D Blender + composite + enhancement agresivo). *(nicho, creador "Quix")*
- **ip-carpetman** — IP personal "Carpetman" con reference IDs propios; el **patrón** de identity-locking (face grid + outfit refs + batching) es reusable.

### 🎬 generacion-video (18)
- **seedance-director** — Director maestro y generador de prompts timeline-accurate para Seedance 2.0.
- **cinematic-motion-language** — Vocabulario estructurado de cámara/movimiento/lente para video de alta precisión.
- **kling-3-prompt-director** — Fórmula canónica de **9 campos** para prompts de Kling 3.0.
- **pulp-cinema-director** — Director estilo pulp/Tarantino: shot library, model router, fórmula de prompt.
- **cinematic-scene-generation** — Genera ángulos alternativos e insert shots desde una escena de referencia (Nano Banana Pro).
- **storyboard-generation** — Reglas para slides de presentación y storyboards multi-panel (imagegen_2_0).
- **storyboard-cheatcode** — Previs-first: storyboard → preview barato → hero render, con control de costos.
- **talking-head-director** — Director de talking-head + arquitectura de guión (avatares, hooks, teleprompter, delivery por plataforma). **Muy útil para reels.**
- **b-roll-shot-planner** — Planea 5 B-roll shots (JSON) desde una imagen ancla de estilo (NanoBanana).
- **flash-reel** — Pipeline de reel 9:16 de 30s con estética flash 35mm (GPT Image 2 → Kling 3.0, 8 escenas). **Receta de estética reusable.**
- **seedance-prompting-cinematic-films** — Realismo cinematográfico "grounded" para Seedance 2.0: 5 pilares + estructura de 6 bloques. *(la más popular de la categoría)*
- **cinematic-flow-project-rules** — Overrides de proyecto para cinematic-flow (workaround de continuación de video, combat constraints, audio stitching).
- **ai-short-drama-flow** — Pipeline de micro-drama chino (短剧), wrapper de cinematic-flow (formatos, ganchos/reversiones, consistencia entre episodios).
- **google-flow-composer** — Protocolo de prompt de música para Google Flow / Lyria 3 Pro. **Útil para soundtracks de reels.**
- **higgsfield-veo-3-audio-director** — Veo 3.1 con audio integrado: cuándo usarlo + arquitectura de prompt visual y audio.
- **video-advanced-pipelines** — Bridge/Loop/Extend/Stitch con Seedance 2.0 + FFmpeg + Librosa (reglas de audio scoring, fixes de API).
- **rockstar-agent** — Videos estilo GTA V (Rockstar): visual DNA, workflow, model routing.
- **cherry-blackcloud-guide** — Reglas de prompt-writing para Seedance 2.0 con diálogo (timestamps, accent notes, negativos positivos). *(canon personal del autor)*

### 🌐 web-y-diseno (6)
- **frontend-ui-engineering** — Construir UIs de producción (React/TS): patrones de componentes, **evitar el "AI look"**, accesibilidad WCAG.
- **performance-optimization** — Medir→identificar→fix→verificar→guard: Core Web Vitals, anti-patterns, performance budget.
- **web-app-building** — Convenciones para apps/UIs single-file en chat (auth flows, patching, encoding, CORS).
- **browser-testing-with-devtools** — Chrome DevTools MCP para testing en navegador real (workflows + security boundaries).
- **vercel-composition-patterns** — Patrones de composición React (evitar boolean prop proliferation). *(oficial de Vercel, MIT)*
- **theme-factory** — 10 temas de font+color para estilizar slides/artifacts.

### 📣 marketing-y-ads (19)
- **social-content** — Crear/programar/optimizar contenido para redes (LinkedIn, X, IG, TikTok, FB).
- **ad-creative** — Generar/iterar/escalar ad creatives (headlines, descriptions, variaciones).
- **marketing-psychology** — Aplicar principios de psicología/modelos mentales/ciencia del comportamiento al marketing.
- **copywriting** — Copywriter de conversión (headlines, CTAs, secciones de página).
- **content-strategy** — Estrategia de contenido SEO/social: pilares, keyword research por buyer stage, priorización.
- **marketing-ideas** — 139 ideas de marketing SaaS por categoría/stage/budget.
- **paid-ads** — Campañas pagas (Google/Meta/LinkedIn/TikTok): estructura, copy, targeting, optimización.
- **email-sequence** — Diseño de secuencias de email/drip (tipos, timing, subject lines, copy).
- **seo-auditor** — Auditoría SEO técnica con deliverable TODO estructurado.
- **ab-test-setup** — Diseño de A/B tests + programa de experimentación (ICE).
- **brand-guidelines** — Aplica la identidad de marca oficial de Anthropic (colores + tipografía).
- **marketing-studio-director** — Director de video de marketing: formatos, avatares, hooks, delivery por plataforma.
- **higgsfield-brand-visual-kit** — Sistema de consistencia visual de marca (model routing, color vocabulary, lighting, negatives, templates).
- **product-photography-brief** — Briefs de fotografía de producto e-commerce (model routing, 8 shot types, negatives, lentes).
- **static-ads** — Recrea formatos de ad ganadores con producto/copy propios (workflow zone-based con GPT-image-2).
- **premium-ad-posters** — Posters/ads high-end con typography+hardware precisos (GPT Image 2).
- **ugc-ad-production** — Pipeline UGC completo (Nano Banana Pro + Kling 3.0 + script).
- **ugc-model-swap** — Recrea un UGC con otro personaje (Seedance 2.0).
- **nike-air-force-ad** — Prompt validado de product reveal cinematográfico (Seedance 2.0). *(estructura de 6 shots reusable)*

### ✍️ escritura (5)
- **humanizer** — Quita el "AI look" de textos: **29 patrones** de escritura IA a eliminar (basado en Wikipedia:Signs of AI writing).
- **writing-shape** — Moldea material crudo en un artículo conversacionalmente (openings candidatos → párrafo a párrafo).
- **writing-beats** — Moldea un artículo como journey de beats (choose-your-own-adventure).
- **writing-fragments** — Sesión de grilling que mina fragmentos de escritura a un archivo.
- **edit-article** — Edita artículos por secciones (información como DAG, reescritura por sección).

### 🤖 agentes-y-meta (8)
- **prompt-engineering-expert** — Diseño de prompts/system prompts/instrucciones de agente (workflow, técnicas, anti-patterns, evaluación).
- **context-engineering** — Cómo dar el contexto correcto a agentes de código (jerarquía CLAUDE.md, packing strategies, confusion management).
- **karpathy-skill** — Guidelines de coding para agentes (pensar antes, simplicidad, cambios quirúrgicos, goal-driven).
- **caveman** — Modo de comunicación ultra-comprimido (~75% menos tokens).
- **grill-me** — Interrogar al usuario sobre un plan hasta entendimiento compartido.
- **supercomputer-onboarding** — Mapa completo de capacidades/modelos/workflows de Higgsfield (buena referencia de plataforma).
- **higgsfield-api-quirks** — Comportamiento no documentado y workarounds de error 500 en `higgsfield_generate`.
- **telegram-export-analysis** — Parsear/analizar exports JSON grandes de Telegram (quirks del campo `text`).

### 🎞️ video-edicion (3)
- **video-stitching** — Puentear dos videos con transición AI seamless (quirks de modelos + ffmpeg).
- **video-editor-commands** — Protocolo completo bridge/loop/extend/split/stitch con ffmpeg + SIFT.
- **video-split-stitch** — Split en el cambio de shot de mayor diferencia + transición AI.

### 🎵 audio-y-musica (2)
- **ffmpeg-audio-synthesis** — Síntesis de audio con Python/FFmpeg/pedalboard + librería de instrumentos.
- **arabic-tashkeel-suno** — Diacritización de letras en árabe para música IA (Suno/Udio), dual-track + risk audit. *(nicho)*

---

## ❌ Las 30 skills first-party (NO extraíbles — solo descripción)

Son capacidades oficiales de la plataforma; se usan con "Try Now" y su `SKILL.md` no es público.

- **generacion-imagen:** soul-id
- **generacion-video:** graphic-poster-workflow, seedance-footage-vfx, video-adapt, video-explainer-workflow
- **web-y-diseno:** design-md, excalidraw, game-generation, infographic, landing-page-flow, popular-web-designs, website-builder-flow
- **marketing-y-ads:** organic-marketing
- **escritura:** creative-ideation
- **agentes-y-meta:** create-skill
- **video-edicion:** adobe-connector, edit, montage, reels-studio-flow
- **audio-y-musica:** audio-generation, songwriting-and-ai-music
- **investigacion-y-analisis:** brand-analyzer, content-analyzer, maps, product-analyzer, trend-picker, youtube-content, youtube-research
- **documentos-y-productividad:** pdf, powerpoint

---

## Método de extracción
Vía `claude-in-chrome`: navegar a `/supercomputer/marketplace/skills/<uuid>` → si tiene botón **Manage** (comunidad), abrir el modal y leer el `SKILL.md` completo. Sin Manage = first-party (no extraíble). El contenido se condensó al español conservando fórmulas, prompts y reglas clave.

*Actualizado julio 2026. Estructura consolidada: un `SKILL.md` por skill.*
