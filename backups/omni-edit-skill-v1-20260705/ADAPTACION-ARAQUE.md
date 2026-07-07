# Adaptación a Araque Solutions

Skill de origen: Morfeo Academy (Paul de Lavallaz). Librería de 6 estilos visuales para ediciones de imagen (GPT Image vía fal): claymation, marker-scribble, desktop-window, retro-collage, yellow-burst, paper-puzzle.

1. **"Paul" = el dueño (Jhon / Araque Solutions).** La validación de estilos ("Validado: sí/no" en `styles/INDEX.md`) la hace él.
2. Estado heredado: solo 3 estilos traen refs; marker-scribble fue RECHAZADO en origen por falta de dinamismo — no usar sin rehacer.
3. **Uso en la agencia**: editar series de clips con un look unificado (estilo Shorts Maker de Higgsfield pero sin sus créditos) — clientes cuyo feed necesita identidad visual distinta al UGC realista. Cada generación gasta — autorización previa del dueño.
4. Motor: **Gemini Omni Flash vía API directa de Google** → key `GEMINI_API_KEY` en `.env` raíz del repo (aún no configurada 2026-07-04).
