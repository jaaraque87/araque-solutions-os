---
name: web-app-building
title: "Web App Building"
author: cherry_blackcloud
category: Content Creation
users: 34
source: https://higgsfield.ai/supercomputer/marketplace/skills/bf2cad76-6e83-482c-baa2-ba71965f229c
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): cdn-editor-quirks.md
nota: convenciones específicas para apps/UIs single-file construidas en chat sobre Higgsfield (varios tips son generales de web).
---

# Web UI Building & Patching
Convenciones y safeguards para construir, deployar y parchear web apps/UIs single-file en chat.

## Authentication & UX flows
- **Frictionless:** nunca pedir al usuario abrir DevTools ni copiar cookies de sesión. Odian los auth flows complejos.
- **Automated token bridges (Chrome extensions):** al integrar herramientas separadas (UIs locales, hosted editors) con plataformas externas, preferir bridges automáticos sobre inputs manuales.
- **Anchor tags vs window.open():** los pop-up blockers bloquean `window.open()` salvo que ocurra síncronamente dentro de un click handler directo. Preferir `<a href target="_blank">` o `<button onclick="window.open('...','_blank')">`.
- **Clipboard fallbacks:** `navigator.clipboard` falla silenciosamente en dominios CloudFront/CDN. Chequear `window.isSecureContext`; proveer un modal visible con `<textarea>` de fallback.
- **Clipboard API vs execCommand:** `navigator.clipboard.writeText()` falla en contexto no-HTTPS o secure-pero-no-reconocido; fallback a `document.execCommand('copy')`.
- **No file checkers for auth:** evitar pickers de API token inline en editores HTML (fricción); usar links con copy manual de URL.

## File Manipulation & Patching
- **Avoid greedy regex:** nunca usar `sed`/`re.sub` con patrones multiline greedy (`.*?` entre líneas) para remover bloques; usar `split()`/`find()`.
- **Exact replacements:** al modificar archivos con Python, `content.replace(old_exact_string, new_exact_string, 1)`.
- **Complete rebuilds:** si un archivo se corrompe o requiere cambio estructural, no parchear repetidamente — reconstruir completo.

## Emoji & Encoding
- **HTML entity JS escaping:** al cambiar texto dinámicamente con `element.textContent = '...'`, recordar que `textContent` parsea string literals directo e IGNORA HTML entities (`&#9654;`); usar el escape unicode `▶`.

## URL Handling & Formats (específico Higgsfield)
- **Editor inputs:** manejar tanto job UUIDs crudos como CDN URLs directas `.mp4`.
- **Resolution logic:** al parsear UUID para armar asset URL (`https://higgsfield.ai/asset/video/UUID`), regex exacto; no agregar `.mp4` accidentalmente a CDN URLs de cloudfront.net que ya lo tienen.
- **Video element references:** modelos de la API usan entidades persistentes; `higgsfield_element(action='get', element_id='<uuid>')` para resolverlas; proveer description rica.
- **CORS & scrubbing:** los scrubbers browser-based requieren que el HTML esté hosteado en el mismo CDN origin que los videos para pasar CORS; usar `higgsfield_upload`.
