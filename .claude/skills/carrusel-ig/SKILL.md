---
name: carrusel-ig
description: "Carruseles editoriales de Instagram (1080x1350) con fotos IA + tipografía de marca programática (HTML+CSS+Puppeteer, tipografía idéntica en todos los slides). Usar cuando se pida: carrusel, carrusel IG, slides para Instagram, carrusel educativo, o contenido carrusel para un cliente. Sistema Ana Lab validado (piloto Pedro y Mateo 2026-06-10)."
---

# CARRUSEL-IG — sistema Ana Lab

El sistema completo vive en `tools/carrusel-ana-lab/`. **Antes de armar cualquier carrusel, leer `tools/carrusel-ana-lab/SISTEMA.md` entero** — es la fuente de verdad: 13 reglas de diseño lockeadas, tipos de slide, formatos rotativos y patrón de prompts de foto.

## Flujo

1. **Marca**: cada cliente tiene su `brands/<marca>/brand.json` (nombre, handle, 3 colores con roles fijos primary/background/accent, 2 Google Fonts, datos reales). Si el rubro exige leyendas legales, completar `compliance`.
2. **Idea → archivos**: desarrollar hook + beats + copy (usar hook-lab para el hook del slide 1 — un carrusel también compite en el feed) y escribir `inputs.json` + prompts de foto en `manifest.json`.
3. **Fotos**: automático con fal (`node generar-fotos.mjs`, requiere `FAL_KEY`, ~US$0.50 por 5 fotos — GASTA, pedir OK) o manual copiando cada `prompt_base` en el generador que el dueño prefiera.
4. **Render**: `node generar.js` → `preview.html` para revisar + JPGs 1080×1350 en `output/`.
5. **Scorecard (Regla 0)**: hipótesis explícita escrita ANTES de postear + medición (saves, shares, alcance, follows 72h, DMs). Sin scorecard no se postea. Plantilla: `scorecard-template.md`.

## Reglas duras

- La tipografía NUNCA la genera la IA — solo la foto. El texto siempre va por HTML/CSS del renderer.
- Paleta de 3 colores con roles fijos; el renderer rechaza colores fuera de paleta.
- El hook del slide 1 sale de hook-lab (mismo estándar que los reels: claridad en 1.5s, una sola pregunta).
- KPI reina de carruseles: saves. Modo del contenido (ALCANCE vs CONVERSIÓN) declarado en el scorecard.

## Integración con el resto del sistema

Reel (render-batch) + carrusel (este sistema) del mismo tema = un "content drop" completo por cliente: el reel gana alcance, el carrusel gana saves y autoridad. Los hooks salen de la misma batería (`tools/hook-lab/clients/<cliente>/hooks.json`).
