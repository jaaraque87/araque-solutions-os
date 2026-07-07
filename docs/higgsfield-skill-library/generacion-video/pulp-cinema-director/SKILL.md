---
name: pulp-cinema-director
title: "Pulp Cinema Director"
author: teleportingrocket1235
category: Fun-quirky
source: https://higgsfield.ai/supercomputer/marketplace/skills/8756c2fd-c4e4-470c-928b-11f9018bb908
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# Pulp-Cinema Director
Convierte ideas cinematográficas en workflows Higgsfield: shot plan, elección de modelo, cámara/luz. Estilo pulp-cine (crimen no-lineal, standoffs, trunk-level).

## Core Mode (cuando piden "Tarantino/Tarantino-style")
No claim de ser Tarantino; ofrecer un homenaje original con: estructura de capítulos no-lineal · tensión dialogue-first · peligro estilizado sin gore · ángulos trunk-level bajos · standoffs y tableau blocking · snap zooms, slow push-ins, close-ups estáticos · props táctiles (llaves, botas, cigarrillos, tazas de diner, vinilos, teléfonos viejos) · textura de género 70s/90s · rojos/amarillos saturados, sombras duras, neón, halation, film grain · música por género (no títulos con copyright).

## Model Router
- Diálogo con 2-3 personas → Seedance 2.0 o Kling 3.0.
- Wide atmosférico → Veo/Sora (o Seedance 2.0).
- Hero still / poster / title card / texto → GPT Image 2.
- Stills de personaje consistente → Soul 2.0 / Soul Cinema con Soul ID.
- Exploración rápida → Nano Banana Pro / Flux.
- Análisis de video terminado → Virality Predictor.

## Shot Library (patrones de prompt)
- **Trunk-Level Reveal:** cámara baja desde adentro de un baúl/valija/freezer mirando hacia arriba; personajes bien vestidos inclinándose al frame.
- **Standoff Tableau:** blocking triangular, quietud, eye lines, manos cerca de props, tensión antes de la acción; wide estático anamórfico.
- **Extreme Close-Up Chain:** cortar entre ojos, manos, botas, prop, reloj, boca → wide reveal final.
- **Walk-And-Talk:** dos personajes en paralelo, dolly tracking, diálogo implícito por postura/ritmo.
- **Retro Title Card:** fondo negro, texto serif retro mostaza, film gate weave, dust.

## Prompt Formula (mín 6 de estos)
Era/década · Location · Character action · Camera angle · Lens/format feel · Camera motion · Lighting source · Color palette · Texture/film stock · Continuity constraints · Negative constraints.
Template: `[Era] [location]. [Characters and action]. Camera: [shot size, angle, lens, movement]. Lighting: [...]. Palette: [...]. Texture: [...]. Continuity: [...]. Negative: [...]`.

## Longer Scene Workflow (30s-2min)
No pedirle una película entera a un modelo. Capítulos: hero still/storyboard → micro-takes de 5-15s → definir first/last frame de cada take → reusar wardrobe/props como anclas de identidad → menos personajes por shot → violencia implícita (cutaways a props/pies/sombras) → chequear continuidad/manos/caras/prop drift.

## Audio
Música por estilo y fuente ("1960s surf rock guitar from a car radio", "spaghetti-western trumpet and low whistle", "single-note suspense drone"). No nombrar canciones con copyright ni artistas específicos.

## Safety/Style
No claim de ser Tarantino ni recrear el estilo exacto de un artista vivo. No gore explícito (implicar). No likeness de celebridades reales sin permiso. Texto legible → GPT Image 2.

## Checklist
Scene type · genre module · modelo Higgsfield · aspect ratio · prompt con cámara/luz/palette/motion/continuidad/constraints · personajes acotados · first/last frames en multi-shot · costo estimado · aprobación antes de generar · revisar output.
