---
name: ai-short-drama-flow
title: "AI Short Drama Flow (AI 短剧)"
author: eulerbutterfly1295
category: Content Creation
version: 1.0
source: https://higgsfield.ai/supercomputer/marketplace/skills/7304b0ad-5f4d-498e-ad94-33a23aedb22a
extracted: modal SKILL.md (via claude-in-chrome)
references: hook-and-reversal-library.md (NO extraída — biblioteca de ganchos/reversiones para drama vertical chino)
nota: skill en chino simplificado; nicho (micro-drama chino). Es un wrapper superior de cinematic-flow.
---

# AI 短剧流水线 (Micro-drama pipeline)
Pipeline end-to-end de producción de micro-drama (短剧). El agente actúa como **Productor** orquestador: llama los enhancers de `cinematic-flow` (guionista/director/visual/storyboard/prompt-writer), gestiona pipeline, assets y fixes. Es un **wrapper superior de cinematic-flow** que añade 3 cosas propias del short-drama: routing de formato, ritmo de gancho/reversión, consistencia entre episodios.

## Tres formatos
- **A — Vertical de pago (9:16, 60–90s):** gancho fuerte + reversiones de alta frecuencia (estilo投流 抖音/红果). Densidad alta (1 punto de info cada 2–4s).
- **B — Narrativo horizontal (16:9, 60–180s):** casi = cinematic-flow, orientado a historia.
- **C — Serie multi-episodio (9:16 o 16:9, 60–120s/ep):** la consistencia entre episodios es el núcleo.

## Reglas de hierro del usuario (prioridad sobre defaults — hacen que este skill NO sea full-auto)
1. **Todos los prompts a modelos (Seedance/GPT Image/Soul) en chino simplificado**, no inglés. Placeholders `<<<element_id>>>`, `@Image1`, `@Video1` se preservan.
2. **Parámetros primero:** antes de CADA generación, usar `ask_user_question` para que el usuario elija modelo + todos los parámetros clave. Nunca submitear sin que estén todos elegidos.
3. **Puerta de créditos:** tras elegir params, llamar `higgsfield_balance`, estimar créditos y avisar (estimado + saldo) → esperar confirmación explícita.
4. **Multi-personaje en cuadro:** para 2+ personajes independientes interactuando, primero generar una imagen compuesta estática con `imagegen_2_0` (usuario la llama "ChatGPT2"), que el usuario la apruebe, y recién animarla como frame de referencia único.
5. **Clips de 15s → `seedance_2_0` estándar** (nunca `seedance_2_0_fast`, falla a 15s).

## Pipeline (fases)
0. Routing de formato + recolección de parámetros (ask_user_question una vez: formato A/B/C + duración + episodios + reuso de personajes + estilo). 0.5. Plan de identidad de personaje (Soul ID reusable / Soul Cast único / foto subida / arranque por texto). 1. Guionista (dramaturg). 2. Puerta de scope. 3. Director (FULL; LITE lo salta). 4. Generación de assets (personaje/escena/props; 3 variantes paralelas, aprobación serial; regla④ compuesto). 5. Style Architect → Film Lock + Scene Lock. 6. Shot Planner. **6.5. Confirmación de params + puerta de créditos (★obligatoria en short-drama★).** 7. Prompt-writing (paralelo) → traducir a chino → batch Seedance (≤8 concurrentes). 8. Ensamblaje + entrega (montage → final.mp4). 9. QA opcional. 10. Fixes. 11. Persistencia entre episodios (formato C).

## Gancho de oro (3 seg — clip 1 debe pegar uno)
Suspenso adelantado · brecha de identidad (humillación/malentendido extremo) · personaje de contraste (débil aparente revela pista de identidad oculta) · suspenso letal (cuenta regresiva/amenaza).

## Ritmo de reversión
- 60s (≈6–8 clips): gancho(clip1) → mini-reversión(clip3) → reversión principal(clip5) → cierre-gancho(último).
- 90s (≈9–11 clips): gancho → setup → reversión1 → subir apuesta → reversión2 → clímax → cliffhanger.
- Multi-ep: cada episodio termina en cliffhanger.

## Composición vertical (bloque a Style Architect/Prompt Writer)
9:16 sujeto centrado-arriba, info clave en 2/3 superior (abajo tapado por UI/subs) · close-ups predominan (vertical = cara/emoción) · subtítulos/diálogo son el núcleo (escribir diálogo en beats del prompt Seedance).

## Consistencia entre episodios (formato C — 3 pilares)
1. **Identidad persistente:** un Soul ID entrenado (`reference_id`) + `<<<element_id>>>` derivado por protagonista; persisten cross-session, entrenar una vez, reusar infinitos episodios.
2. **World Bible persistente:** escribir elementos de escena + Film Lock + registro de personajes en project memory (fase 11); cargar al empezar el siguiente episodio.
3. **Continuidad de serie:** cada intro puede retomar el cliffhanger anterior; cada final deja gancho nuevo.
Episodio N>1: cargar memory → reusar soul_id/element (saltar reconstrucción) → solo generar assets nuevos del episodio → arrancar guión desde el cliffhanger previo → mantener Film Lock del ep.1 (no re-elegir estilo).

## Defaults
| | Vertical A | Horizontal B | Multi-ep C |
|---|---|---|---|
| Aspect | 9:16 | 16:9 | a elección |
| Resolución | 1080p | 1080p | 1080p |
| Clip | 5–8s | 8–12s | 5–10s |
| Clip 15s | seedance_2_0 (no fast) | | |
| Pacing | rapid (gancho+reversión) | por brief | rapid |
| Idioma prompt | chino simplificado | | |

Todos los defaults igual pasan por la puerta 6.5 de confirmación del usuario.

## Gates propios (además de G1–G5 de cinematic-flow)
S0 formato · S1 identidad · S-params · S-créditos · S-chino · S-compuesto (multi-personaje) · S-multi-ep (persistencia).

Módulos completos reusados de cinematic-flow (no reescritos): generación de assets, mecanismos de continuidad de secuela, validación de integridad de batch, QA (detect_scene_cuts + video_analyze), fixes (Clip Patch/Regen/Restructure/Full Regen).
