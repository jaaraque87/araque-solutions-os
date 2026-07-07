---
name: soul-id
title: "Soul Id"
author: Higgsfield (first-party / oficial)
source: https://higgsfield.ai/supercomputer/marketplace/skills/f221a998-4425-45e1-945c-3db21da22973
extracted: NO DISPONIBLE
---

# Soul Id — SKILL.md NO extraíble

⚠️ **Soul ID es una skill OFICIAL de Higgsfield (first-party), no de un usuario.**
A diferencia de las skills de la comunidad, **no tiene botón "Manage" ni vista de `SKILL.md`** — solo "Try Now" y una galería "What you can do with Soul Id". Su lógica interna no está expuesta en el marketplace, por lo que no se puede cosechar como las demás.

## Lo único disponible (descripción pública)
Face identity training and management. Entrena un modelo de identidad persistente (Soul ID) desde 1-100 fotos de cara O lo bootstrapea desde una descripción de texto, y luego genera imágenes que preservan el parecido vía **Soul 2.0**. Se usa cuando la misma persona debe aparecer consistente en múltiples generaciones.

## Cómo usarla igual
Se invoca dentro de Higgsfield con `/soul-id` o el botón "Try Now". No requiere el SKILL.md; es una feature nativa del producto.

## Decisión de proyecto (reel Kumar): NO usar soul-id
Para este reel se **descarta** soul-id — se suple con **fijación de rostro por imagen de referencia**:
- **GPT Image 2:** character consistency entre imágenes secuenciales en la misma conversación.
- **Nano Banana Pro:** edición nativa + multi-referencia.
- **Flux:** hasta 8 imágenes de referencia para identidad (el más fuerte por-referencia).

**Motivo:** soul-id (modelo de identidad entrenado) solo aporta ventaja real con muchos ángulos/luces y decenas de generaciones nuevas. Un reel de ~26s con ~5 encuadres repetidos que se animan desde stills no lo necesita → la fijación por referencia alcanza y sobra. soul-id = overkill acá.
