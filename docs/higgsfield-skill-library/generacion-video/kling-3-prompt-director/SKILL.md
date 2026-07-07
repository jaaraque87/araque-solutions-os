---
name: kling-3-prompt-director
title: "Kling 3 Prompt Director"
author: crococopter
category: Content Creation
source: https://higgsfield.ai/supercomputer/marketplace/skills/09a74d13-70b3-42a6-a56c-889e25065f8e
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# Kling 3.0 Prompt Director
Produce prompts de video Kling 3.0 con la **fórmula canónica de 9 campos**.

## Cuándo dispara
Cualquier request de prompt Kling 3.0 (en cualquier idioma). NO para Seedance (usar seedance-director), Sora, MidJourney.

## La fórmula de 9 campos (orden obligatorio)
Todo prompt Kling 3.0 debe tener estos campos EN ESTE ORDEN, sin saltear ninguno:
1. **Subject** — personaje/objeto principal en una frase nominal corta.
2. **SubjectDescription** — apariencia ultra-detallada: build, cara, ropa, props, texturas.
3. **Movement** — qué hace el sujeto; verbos de acción fuertes, UN arco de acción claro.
4. **Scene** — dónde pasa, una frase corta.
5. **SceneDescription** — entorno ultra-detallado: arquitectura, objetos, materiales, capas de profundidad ("minimal context" solo si es realmente vacío).
6. **Camera** — tipo de plano + movimiento + lente (ej. "medium wide, slow dolly-in, 50mm").
7. **Lighting** — fuente, dirección, calidad, temperatura de color.
8. **Atmosphere** — mood, clima, partículas, feel de post ("neutral" si no hay mood específico).
9. **Negative** — qué excluir; NUNCA vacío.

## Output format
```
**Kling 3.0 prompt — [shot title]**
Subject: [...]
SubjectDescription: [...]
Movement: [...]
Scene: [...]
SceneDescription: [...]
Camera: [...]
Lighting: [...]
Atmosphere: [...]
Negative: [...]

Suggested settings:
- aspect_ratio: [16:9 | 9:16 | 1:1]
- duration: [3–10 seconds]
- start_image: [if applicable]
```

## Hard rules
- **Un solo start_image** — Kling 3.0 acepta UNA imagen de referencia.
- **Aspect ratios:** solo 16:9, 9:16, 1:1. Default 16:9 cinematográfico, 9:16 social.
- **Una acción clara por shot** (la consistencia de movimiento degrada con muchas acciones simultáneas).
- **Verbos de acción fuertes** en Movement.
- **Negative nunca vacío.** Baseline default: "distorted faces, extra limbs, warped hands, low resolution, blurry, watermark, text overlay".
- **Repetir la descripción completa del personaje siempre** — nunca "(as above)".
- **Entornos locked = detalles recurrentes consistentes** (repetir verbatim).
- **Ultra foto-realista por default** salvo que pidan stylized.

## Workflow
1. Leer el request (personajes, entorno, acción, mood, formato). 2. Detectar universo/locks. 3. Decidir aspect ratio y duración. 4. Chequear multi-beat (si hay muchas acciones, proponer split en varios prompts). 5. Llenar los 9 campos en orden. 6. Validar hard rules. 7. Output estructurado (+ variante MCP/CLI si la piden).

## Nota
El SKILL trae "Project Universes" con locks personales del autor (personajes "Gideon/Crococopter", "Swa & Danny" en neerlandés) — específicos de sus proyectos, no reusables. La parte valiosa/general es la fórmula de 9 campos + hard rules de arriba.
