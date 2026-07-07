---
name: ip-carpetman
title: "IP Carpetman"
author: bauhauswater_pico
category: Creative-marketing
users: 14
source: https://higgsfield.ai/supercomputer/marketplace/skills/0dd75674-afb5-431c-ae19-df75901a743b
extracted: modal SKILL.md (via claude-in-chrome) — single file
nota: IP/personaje personal del autor ("Carpetman"/Карпетмен) con media reference IDs privados. El PATRÓN de identity-locking (face grid + outfit refs + batching) es reusable; los IDs específicos no.
---

# IP / Character: Carpetman (Карпетмен / Карпет)
Reglas de manejo y referencias de media persistentes para el personaje custom "Carpetman". Cuando piden una imagen de "Carpetman", NUNCA usar solo el nombre en texto — usar `nano_banana_2`/`nano_banana_pro` con las reference images (`medias`/`images`).

## 1. Technical & Chat Protocol
- **Resolution & Aspect:** siempre 9:16 vertical.
- **Batching:** siempre 2 variantes por request en una llamada paralela — una con `nano_banana_2` y otra con `nano_banana_pro`.
- **Chat Response:** responder SOLO el número de tarea (ej. `**21/30**`) arriba, seguido del tool call. Sin filler text/explicaciones/confirmaciones.

## 2. Text Prompt Replacement
- Empezar CADA prompt con: `Vertical 9:16 candid iPhone photo, real uneven lighting, slight grain.`
- Reemplazar el nombre del personaje por UNA de las descripciones según outfit.
- Expresiones neutras (boca cerrada o subtle closed-lip smile) — nunca dientes ni sonrisas amplias.
- **Hat (default):** "Carpetman (Hat outfit) — a real living person wearing a fabric carpet-pattern costume, wide-brimmed [hat]..."
- **Hood:** "Carpetman (Hood outfit) — a real living person wearing a fabric carpet-pattern costume, ornate carpet [hood]..."

## 3. Styling & Clothing Rules
- Ropa civil no-estándar: oversized y muy estilosa (heavy cotton, dropped shoulders, streetwear).
- Uniformes (doctor/policía/deporte/Wendy's): auténticos, no estilizados.
- Nunca se desviste — en agua/baños/piletas/duchas queda completamente vestido en su outfit.
- Prompt length ~250-400 palabras (rico en escena/textura, tight en constraints).

## 4. Mandatory Reference IDs (privados del autor)
Siempre incluir Face Grid + el Outfit/Body correspondiente en `params.images`/`params.medias` (`type:"media_input"`):
- Face/Identity Grid (index 0): `a16310e8-18ed-4723-8a71-8d413252693c`
- Outfit Hat (default, index 1): `f521a04d-3fe6-4c1b-83d3-f682b064e503`
- Outfit Hood (index 1): `29298b2a-9b7e-4eb4-ae03-5e0dfa8a6239`

## 5. Optional Context References (index 2+, solo si la escena lo demanda)
- Carpet Print (entornos/props/fondo): `0e3a927b-1b1c-4fad-a4c7-d0543d4d47ba`
- Close-up Hands (gestos/sostener objetos): `546d0a5a-1898-4efc-be27-da0868beab54` + `ff9159a4-0feb-4ed5-a72b-b4337468f4a9`

## Patrón reusable (para otros personajes IP)
Face grid persistente (index 0) + outfit refs por variante (index 1) + context refs opcionales (index 2+); prefix de estética consistente ("candid iPhone photo..."); batching de 2 modelos por request; expresiones/reglas de vestuario locked para consistencia de personaje.
