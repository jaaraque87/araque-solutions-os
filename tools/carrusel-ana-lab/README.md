# Carruseles editoriales de IG — con fotos IA y tipografía de marca

Sistema completo para generar carruseles de Instagram (1080×1350): fotos hechas con IA + tipografía programática idéntica en todos los slides. Lo armó **Ana Paula Cascardo** iterando con Claude (Fable) — compartido con la comunidad para que lo uses con tu marca. Usalo, rompelo, mejoralo.

**La idea central:** la tipografía generada por IA cambia en cada imagen y arruina la marca. Acá el modelo hace SOLO la foto; el texto se superpone con HTML+CSS y se renderiza a JPG con Puppeteer. Fotos espectaculares + tipografía perfecta, siempre.

## Empezar (10 minutos)

1. Instalá [Node.js](https://nodejs.org) (LTS).
2. En esta carpeta:
   ```
   npm install
   ```
3. **Tu marca**: editá `brands/mi-marca/brand.json` (nombre, handle, 3 colores, 2 Google Fonts, datos reales del producto) y poné tu logo según `brands/mi-marca/assets/LEEME.txt`. Si tu rubro exige leyendas legales (alcohol, salud), completá `compliance` — se inyectan solas en el último slide.
4. **Las fotos** — dos caminos:
   - **Automático**: cuenta en [fal.ai](https://fal.ai) (cargá USD 5-10), creá un archivo `.env` acá con `FAL_KEY=tu-key`, y corré:
     ```
     node generar-fotos.mjs
     ```
     Genera las 5 fotos del ejemplo (~USD 0,50) leyendo los prompts del `manifest.json`.
   - **A mano**: abrí `brands/mi-marca/carruseles/001-ejemplo/manifest.json`, copiá cada `prompt_base` en tu generador favorito (GPT Image, Nano Banana, Seedream, Midjourney) y guardá cada foto donde dice `archivo_destino`.
5. **Renderizar**:
   ```
   node generar.js
   ```
   Sale `preview.html` (abrilo en el navegador para revisar) y los JPG finales 1080×1350 en `output/`. Listos para postear.

## El flujo real (con Claude como copiloto)

Lo potente es iterar con Claude Code abierto en esta carpeta:

> "Leé SISTEMA.md. Quiero un carrusel para mi marca sobre [tu idea]. Armame el inputs.json con copy en mi tono y los prompts de foto en el manifest."

Claude desarrolla la idea (hook, beats, copy), escribe los archivos, y vos solo generás fotos + corrés el render. Para iterar: "el título del slide 3 más grande", "ese body más corto" — Claude edita y re-renderiza en segundos.

## Los archivos

```
SISTEMA.md              ← LAS REGLAS. Leelo una vez entero: 13 reglas de diseño,
                          tipos de slide, formatos rotativos, patrón de prompts de foto
generar-fotos.mjs       ← fotos automáticas vía FAL (opcional)
generar.js              ← render final: inputs.json → JPGs 1080×1350
scorecard-template.md   ← medí lo que posteás (saves/shares) — regla 0
brands/mi-marca/        ← ejemplo completo editable (marca ficticia de café)
  brand.json            ← identidad: colores, fonts, logo, voz
  carruseles/001-ejemplo/
    inputs.json         ← el carrusel: 6 slides con copy y layout
    manifest.json       ← los prompts de cada foto
```

## Lo que hace que quede bien (resumen de SISTEMA.md)

- **Hook que para el scroll** sin spoilear: una palabra/número GIGANTE + opinión
- **Títulos mezclados**: serif italic minúscula + sans bold MAYÚSCULA, palabra por palabra
- **Body de UNA frase** (≤70 caracteres) — cada slide se lee en 3 segundos
- **El texto cae donde la foto respira**: cada prompt de foto reserva la zona limpia ("negative space upper-left kept clean for typographic overlay")
- **Fotos editoriales vivas**: escenas en uso, manos, golden hour, Portra 400 — nunca producto solo sobre fondo blanco
- **Formato rotativo**: si este carrusel fue lista numerada, el próximo es narrativa o statements (los 6 tipos de slide están en SISTEMA.md)

Dudas: pegale este README + SISTEMA.md a Claude y preguntale. Está escrito para que Claude lo entienda y lo extienda.
