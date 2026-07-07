---
name: brand-guidelines
title: "Brand Guidelines (Anthropic)"
category: Ui-kit
license: Complete terms in LICENSE.txt
users: 83
source: https://higgsfield.ai/supercomputer/marketplace/skills/8520d3e6-6b20-9b3d-0aa1-9532bfc8a5f2
extracted: modal SKILL.md (via claude-in-chrome) — single file
nota: aplica la identidad de marca OFICIAL de Anthropic (colores + tipografía) a artifacts (slides, etc.). Es el sistema de marca de Anthropic, no genérico.
---

# Anthropic Brand Styling
Aplica la identidad de marca oficial de Anthropic a artifacts. Keywords: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography.

## Colors
**Main:** Dark `#141413` (texto primario/fondos oscuros) · Light `#faf9f5` (fondos claros/texto sobre oscuro) · Mid Gray `#b0aea5` (secundarios) · Light Gray `#e8e6dc` (fondos sutiles).
**Accent:** Orange `#d97757` (accent primario) · Blue `#6a9bcc` (secundario) · Green `#788c5d` (terciario).

## Typography
- **Headings (24pt+):** Poppins (fallback Arial).
- **Body:** Lora (fallback Georgia).
- Para mejores resultados, pre-instalar Poppins y Lora en el entorno.

## Features
- **Smart Font Application:** Poppins a headings (24pt+), Lora a body, fallback automático Arial/Georgia si no están disponibles.
- **Text Styling:** selección de color inteligente según el fondo; preserva jerarquía y formato.
- **Shapes & Accents:** formas no-texto usan accent colors, ciclando orange→blue→green.

## Technical
- Font management: usa fuentes system-installed cuando están, fallback automático, sin requerir instalación.
- Color: valores RGB precisos, aplicados vía `RGBColor` de python-pptx.
