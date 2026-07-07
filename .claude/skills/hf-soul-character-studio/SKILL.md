---
name: hf-soul-character-studio
title: "Soul Character Studio"
author: visual_intelligence
category: Personal & Specialized
source: https://higgsfield.ai/supercomputer/marketplace/skills/7786b896-0fb7-4c8f-8b27-62e14265cc3c
extracted: modal SKILL.md (via claude-in-chrome) — single file
description: "Arquitecto de personajes consistentes: auditoria de fotos de referencia (5-30), Character Bible, plantillas por escena y diagnostico de deriva de identidad. Usar para blindar la consistencia de Naia, Kenza o personajes de clientes."
---

# Higgsfield Soul Character Studio
Arquitecto de personajes Soul ID: audita fotos de referencia, construye un Character Bible, da plantillas de prompt por escena, y diagnostica deriva de personaje.

## Guía de fotos de referencia
**Cantidad:** Mínimo viable 5-8 (testear viabilidad) · Standard 10-15 (personaje confiable) · Premium 20-30 (AI influencer / campaña / brand character).
**Diversidad requerida (las tres):**
- **Ángulos:** frontal (ojos a cámara), 3/4 izquierda, 3/4 derecha. Perfil opcional.
- **Expresiones:** neutral/reposo (la más importante — base del personaje), sonrisa natural, focus/serio.
- **Luz:** al menos una en cada: luz día natural, interior suave, direccional más dura.
**Técnico:** mín 1024×1024 (más = mejor) · foco nítido en la cara (nada de motion blur) · la cara ocupa ≥40% del frame · misma persona en todas.
**Excluir:** lentes de sol/oscuros o cara tapada · filtros extremos/retoque/beauty smoothing (el modelo aprende la cara filtrada) · maquillaje pesado no representativo · baja resolución · >2 fotos con misma expresión+luz · fotos grupales sin aislar al sujeto.

## Character Bible (después de entrenar)
```
CHARACTER BIBLE
Character name: [nombre/codename]
Soul training ID: [identificador del modelo entrenado]
Physical anchor: [2-3 frases con features visuales definitorios]
Default aesthetic: [mundo visual: editorial/streetwear/wellness/tech/luxury]
Signature wardrobe: [colores, telas, siluetas]
Default lighting: [la luz que mejor lo hace ver]
Color palette: [2-3 colores ancla]
Tone/mood: [1-2 adjetivos]
Forbidden elements: [lo que nunca aparece — rompe brand]
```

## Librería de prompts por escena (5)
1. **Fashion Editorial** (feed IG, lookbook, campaña): `[Soul ID], [ropa del bible], [entorno: estudio minimal], [luz], [pose]`. Fondo simple (los complejos compiten y aceleran la deriva). Negative: background clutter, different face, inconsistent skin tone, plastic skin, changed hair.
2. **Lifestyle/Product** (e-commerce, ads, UGC-adjacent): `[Soul ID], [acción: holding/using] [producto], [entorno], [luz]`. Describir lo que HACE, no solo cómo se ve. Negative: stock photo energy, stiff pose, product floating, wrong hand anatomy.
3. **UGC/Social** (TikTok/Reels, talking-head): `[Soul ID], selfie-style, [interior casual], [luz natural]`. Reducir complejidad estética = más estable. Negative: studio lighting, professional photography, posed, editorial energy.
4. **Outdoor/Cinematic** (campañas, thumbnails): `[Soul ID], [entorno exterior], [hora del día], [luz]`. Matchear paleta del personaje al entorno. Negative: flat lighting, green screen feel, character floating, mismatched shadows.
5. **Studio/Controlled** (producto, catálogo, brand assets): `[Soul ID], fondo estudio limpio [color], [three-point o single light]`. Las más estables — usarlas para resetear consistencia. Negative: environmental background, harsh shadows, busy background.

## Style Lock (evitar deriva)
- **Siempre llevar una frase de ancla visual** (2-5 palabras) en cada prompt: ej. "warm honey skin, defined jaw, dark wavy hair".
- **Consistency chain** para series: generar la 1ª, notar params que funcionaron, repetirlos.
- **La consistencia de LUZ importa más que la ropa** (distinta ropa = reconocible; distinta luz = no).
- **Testear las 5 escenas antes de lanzar.**

## Errores comunes → fix
| Problema | Causa | Fix |
|---|---|---|
| Cara distinta cada gen | falta ancla visual | agregar descripción física del Bible a cada prompt |
| Skin tone cambia | luz cambia entre prompts | fijar un setup de luz en el Bible y repetirlo |
| Genérico pese a entrenar | fotos de training muy similares | agregar diversidad de ángulo/luz |
| Filtrado/artificial | retoque en fotos de training | reentrenar con piel natural sin retoque |
| Rompe en full-body | training solo de retrato | agregar 3-5 fotos full/half-body |
| Rompe en exteriores | entrenado solo indoor | agregar fotos exteriores / matchear paleta |

## Workflow
1. Auditar fotos de referencia (flag diversidad/calidad antes de entrenar). 2. Construir Character Bible (todos los campos antes de un solo prompt). 3. Test de estabilidad de las 5 escenas. 4. Escribir plantillas por escena. 5. Fijar la frase de ancla. 6. Generar a escala (cambiar solo escena y acción, nunca el ancla).
