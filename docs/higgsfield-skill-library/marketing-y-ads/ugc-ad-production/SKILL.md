---
name: ugc-ad-production
title: "UGC Ad Production"
author: imagine_creatiq
category: Marketing And Sales
users: 617
source: https://higgsfield.ai/supercomputer/marketplace/skills/211a9e1b-6c46-49c0-a52f-29a741b61d9c
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# UGC Ad Production Pipeline
Workflow end-to-end para un ad UGC de IA realista de un producto. Formato 15s, 9:16, se ve real. Tools: Nano Banana Pro (visuals), Kling 3.0 (video), Claude 4.6/Gemini (script).

## Required Inputs (pedir TODOS antes de empezar)
Product (nombre/URL/imagen) · Reference UGC video (video real del mismo nicho — Pinterest/TikTok/YouTube, para estilo de script) · Creator face references (2+ imágenes de personas reales atractivas del vibe de la marca — se face-mixean en Nano Banana) · Target audience · Hook type (problem/solution, before/after, testimonial, transformation, o que el agente decida).

## NEVER ask
Editing tool (siempre Canva) · length (siempre 15s) · aspect (siempre 9:16) · video model (siempre Kling 3.0) · image model (siempre Nano Banana Pro).

## Step 1 — Script (Claude 4.6 / Gemini)
Darle MÁXIMO contexto (reference URL, producto, pain points, audiencia). Prompt: "Make a UGC script for a 15-second video like [REF] but for [PRODUCT]. Use [CREATOR desc] as speaker. Include: Hook (first 3-5s: mostrar el problema visual + audio hook), voiceover con palabras exactas, cut descriptions, actions/mannerisms (que el creator se sienta un personaje real — nervous laugh, hair tuck), CTA (últimos 2-3s), timestamps." **Output:** shooting script con columnas Timestamp | Voiceover | Visual/Shot | Action/Mannerism. Virality: pattern interrupt hook, social proof, transformation moment, urgency.

## Step 2 — Creator Face (Nano Banana Pro, 4K)
Prompt: "Mix these two faces to create a new attractive face that does not belong to any real person. Use as face of a UGC beauty/lifestyle creator. Generate at 4K. Hyperrealistic skin texture, natural lighting, creator holding a ring-light..." Usar 2+ refs que matcheen la personalidad de marca. Generar con producto en mano/cerca de cara para el first-frame. Buscar poros/micro-detalle/imperfecciones naturales (eso lo hace no-AI). Generar 3-5 variantes, elegir la más realista. **Output:** portrait 4K del creator con el producto.

## Step 3 — Video (Kling 3.0)
Por qué Kling 3.0: 15s nativo, multi-shot (cortar entre creator hablando → product closeup → transformación → creator), expresivo (mannerisms/gestos), UGC-native.
Setup: creator image (Step 2) = start frame · product image = reference (mid-video) · shooting script = motion/shot prompt.
Prompt structure:
```
[First frame: creator holding product, looking at camera, natural lighting]
Cut 1 (0-3s): Creator speaks to camera with [mannerism], says "[hook line]"
Cut 2 (3-7s): Close-up of product being applied/used on skin
Cut 3 (7-12s): Creator reaction shot — [emotion/mannerism]
Cut 4 (12-15s): Creator faces camera, delivers CTA, [mannerism]
```
Control shots = decirle a Kling exactamente qué muestra cada cut (dirigir, no promptear). ~$4-5 por clip 15s.

## Virality Principles (en cada paso)
Hook = Problem Mirror (mostrar el problema del viewer en primeros 3s) · Before/After = Hope Loop · Audio Hook (whoosh SFX en el cut = pattern interrupt) · Creator Mannerisms = Trust (laughs/hair tuck/sigh) · Reverb = Room Presence (10% reverb quita el "AI feel") · CTA Urgency (últimos 2-3s, directo, low-friction: "link in bio", "tap the link").

## Branding Note (si es para marca real)
La cara del creator debe matchear el persona de la audiencia · estilo/vibe consistente en todos los UGC · no mezclar estéticas entre videos (elegir una y lockearla).

## Platform / Cost
Gemini 2.5 Pro (script, free) · Nano Banana Pro (face+product, Higgsfield creator/Fal.ai) · Kling 3.0 (video ~$4-5/clip) · ElevenLabs (voice cloning, paid) · Play.ht (alt, freemium) · Canva (edit) · Artlist (SFX).
