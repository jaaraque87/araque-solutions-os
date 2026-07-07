---
name: product-photography-brief
title: "Product Photography Brief"
author: visual_intelligence
category: Creative-marketing
users: 30
source: https://higgsfield.ai/supercomputer/marketplace/skills/0a1e4753-017e-4b50-8565-112e7e6bf0b5
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# Product Photography Brief Workflow
Automatiza el planning de briefs de fotografía de producto e-commerce production-ready. Trigger: "product photography brief", "e-commerce shoot brief", "shot planner for e-commerce".

## Required Inputs
Product Name & Category · Product Details (ingredientes, textura, color, packaging, labels) · Brand Aesthetic (minimalist/clean, rustic/earthy, luxury, vibrant/pop, dark/moody) · Target Platforms / Aspect Ratios.

## Step 1: Input Analysis
Extraer: Hero Ingredient/Material (oats, leather grain, lavender) · Packaging/Labeling Text (¿labels legibles? → routear a `imagegen_2_0` GPT Image 2) · Brand Colors · Lighting Archetype (Soft Studio=beauty/skincare · Hard/Chiaroscuro=luxury/men's grooming · Golden Hour/Natural=wellness/food).

## Step 2: Model Routing Matrix
| Shot Type | Texto legible? | Modelo | Rationale |
|---|---|---|---|
| Hero/Studio Packshot | | nano_banana_pro / nano_banana_2 | studio lighting, texturas crisp |
| Macro/Texture Close-up | | nano_banana_pro | micro-detail (geles, cremas, telas) |
| Packaging/Text Detail | Sí | imagegen_2_0 | mejor control espacial + legibilidad de texto/logos |
| Lifestyle/In-Use | | text2image_soul_v2 / soul_v2 | preserva identidad de caras y contexto hand-holding |
| Creative/Editorial Ad | | cinematic_studio_2_5 | composición artística, luz dramática, luxury |

## Step 3: 4-6 Shot Archetypes (de 8 core)
Hero (limpio en fondo seamless) · Macro/Detail · Lifestyle/Contextual · Flat Lay (top-down con ingredientes/props) · Unboxing/Packaging · Hand/Human Context · Range (variantes juntas) · Creative/Editorial Ad Banner.

## Step 4: Aspect Ratios por plataforma
Shopify/Amazon main 1:1 (fondo blanco puro seamless) · Instagram Feed 4:5 · Pinterest/Blog 2:3 · Reels/TikTok/Shorts 9:16 · Website Banner 16:9 o 21:9.

## Step 5: Production Brief (por shot)
```
### Shot [N]: [Shot Type]
Target Model: [modelo]
Aspect Ratio: [ej. 4:5]
Concept: [1 oración]
Generation Prompt: [prompt production-grade: subject, packaging material, lighting, camera lens...]
Negative Prompt: [banco universal e-commerce + exclusiones del shot]
Shot Priority: [High/Medium/Low]
Production Tip: [composición/props/textura]
```

## Negative Prompt Banks
- **Universal e-commerce:** `low resolution, draft, blurry, out of focus, distorted proportions, low quality, noise, grain, ugly...`
- **Anatomical (hand/lifestyle):** `extra fingers, deformed hands, mutated fingers, fused digits, double hands, backward hand, claw hand...`
- **Amazon main image:** `shadow, text, logo, watermark, accessory, prop, colored background, off-white, reflection...`

## Camera & Lens Specifiers (inyectar en prompts)
- Macro: `100mm macro lens, f/2.8, shallow DOF, sharp focus on [texture]`.
- Studio/Hero: `85mm prime lens, clean studio lighting, f/8, razor-sharp edge definition, commercial`.
- Lifestyle: `35mm lens, natural daylight, organic shadows, f/4, high-end editorial lifestyle`.

## Output Verification Checklist
Strategic Analysis (alineación de marca) · Cohesive Shot List (4-6 numerados) · Exact Model Selections (del routing matrix) · Copy-Pasteable Prompts (lens+lighting+background+negatives) · Multi-Platform Aspect Ratios.
