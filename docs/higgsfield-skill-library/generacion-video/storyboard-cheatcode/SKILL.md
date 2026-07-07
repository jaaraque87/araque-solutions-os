---
name: storyboard-cheatcode
title: "Storyboard Cheatcode"
author: prefabquokka1407
category: Content Creation
users: 540
source: https://higgsfield.ai/supercomputer/marketplace/skills/f28b09f0-3346-448e-bdf4-f3538e223d60
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# storyboard-cheatcode
Pipeline previs-first: de un concepto de una línea → imagen de storyboard multi-panel → opcionalmente preview barato → hero render. Escalada de costos controlada.

## Principio operativo — always ask, never guess
Cada paso empieza preguntando al usuario. No pre-llenar decisiones creativas ni inferir tolerancia de presupuesto. Renders cuestan créditos reales (~7 por storyboard, ~50–70 por clip Seedance 12s 720p). El usuario es el director; vos el operador. Iterar barato en la imagen de storyboard ANTES de cualquier render de video es el mayor ahorro.

## Prerequisito
Higgsfield MCP connector agregado (Settings → Connectors → Add custom MCP → URL `https://mcp.higgsfield.ai/mcp`).

## Step 1 — Collect inputs (un ask batcheado)
Pedir todo en un mensaje: 1) CONCEPT (una oración) · 2) ASPECT (16:9 default / 9:16 / 1:1) · 3) PANELS (4 / 6 default / 9) · 4) ART STYLE (photoreal cinematic default / manga / noir ink / hand-drawn / Pixar) · 5) FACE/CHARACTER REF (URL o upload, o "none") · 6) PRODUCT/OBJECT REF · 7) HARD NEGATIVES. Echo un plan de una línea y preguntar "Ready to generate the storyboard sheet?" — no proceder sin confirmación.

## Step 2 — Generar el storyboard sheet
Prompt que: nombra la grilla explícita ("A {N}-panel storyboard previs sheet, laid out as a {rows}×{cols} grid on a black background...") · describe cada panel en 1–2 oraciones con camera angle (wide/medium/close-up) · lista negatives bajo bloque **HARD RULES:** · termina con "ONE single image — the entire {N}-panel sheet in one composition, {aspect}. Each panel {style}."
```
higgsfield_generate_image(model="gpt_image_2", prompt="<full>", aspect_ratio="<aspect>", resolution="2k", quality="high", reference_images=[<face>, <product>])
```
Devuelve job_id → `higgsfield_wait_for_job`. Mostrar y ofrecer: regenerar con feedback / generar end-frame anchor / saltar a preview barato / done.

## Step 3 — End-frame anchor
Si quiere lockear el shot final (pose triunfante, product reveal), promptear el shot final usando el storyboard como referencia; generar el still; preguntar (1) regenerar / (2) proceder a preview / (3) keep still.

## Step 4 — Cheap preview render (Seedance 2.0 @ 480p)
Solo con confirmación. Default 480p (mitad de créditos, mobile-feed-authentic). Correr `higgsfield_check_cost` antes; si excede 100 créditos, parar y reconfirmar. Prompt Seedance como UN párrafo con timecodes en brackets: `"(0–2s) wide establishing shot of... (2–4s) cut to medium... (4–5s) close-up of..."` (prosa narrativa, no bullets).
```
higgsfield_generate_video(model="seedance_2_0", prompt="<beat-by-beat con timecodes>", aspect_ratio, resolution="480p", duration=<5|8|10|12>, genre="<auto|epic|action|drama|comedy|noir|horror>", start_image=<storyboard-sheet>, end_image=<end-frame si existe>, reference_images=[<product>])
```

## Step 5 — Hero render (1080p)
Solo con confirmación. Misma llamada que Step 4 pero `resolution="1080p"`, honrando la duración ya validada. Si eligió Kling 3.0 Pro: `model="kling3_0"` (Kling solo acepta start_image y end_image, no reference_images array). Correr check_cost, reconfirmar si excede 200 créditos. Al final `higgsfield_get_credits`: reportar saldo restante + total gastado en la sesión.

## Defaults / guardrails
- Pasar la face reference DOS veces cuando hay riesgo de identity drift (en reference_images Y en el prompt body: "use the attached face image as the EXACT identity reference; preserve facial features, beard line...").
- Storyboard sheets en 2k, no más (paneles chicos).
- Nunca recomendar Sora (discontinuado).
- Nunca auto-disparar un render de video — el usuario controla cada render.
- Siempre check_cost antes de calls de video (confirmar si >100 preview / >200 hero).

## Failure modes (avisar proactivo)
Producto genérico en el shot final → falta la product ref o no se generó end-frame anchor · identity drift entre cortes → face ref no pasada o no duplicada en el prompt · shot extra random al final de un clip Seedance largo → duración muy larga para los beats, acortar · watch/logo/garment equivocado → el modelo lo inventó, construir el destino como end_image.
