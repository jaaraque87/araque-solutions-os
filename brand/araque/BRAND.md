# Marca — Araque Solutions

Kit de marca + plantillas de post-producción reutilizables en todas las piezas.

## Logos
- `araque-mark.png` — la "A" sola (transparente) = **marca de agua** en reels (arriba-derecha).
- `araque-lockup-transp.png` — lockup "A + ARAQUE SOLUTIONS" (transparente) = tarjeta de cierre.
- `araque-logo-final.png` — logo principal. `araque-profile.jpg` — foto de perfil IG.

## Paleta
- Negro base. Acento: **magenta `#FF2D78` → violeta `#7C4DFF`** (gradiente). Crema `#F6F4F8`.
- En captions, magenta accent = `&H782DFF` (formato ASS/BGR).

## Tipografías (`fonts/`)
Anton 400 (display/hook), Inter 600/800 (texto). Cargar vía `@font-face` local (Google Fonts CDN falla en el sandbox de render).

## Plantillas (HTML → render con `tools/carrusel-ana-lab/render-card.js` o `render-overlay.js`)
- `endcard.html` → tarjeta de cierre de marca (logo + ESCRÍBENOS → + @araquesolutions). **Cierre consistente en TODAS las piezas.**
- `t1.html / t2.html / t3.html` → overlays de texto (captions/hook) transparentes (render-overlay.js → PNG con alpha).
- `profile.html` → render de foto de perfil.

## Look de marca — "Warm Clean" (grade horneado en cada export, FFmpeg)
```
eq=contrast=1.05:saturation=1.1:brightness=0.02,colorbalance=rm=0.05:bm=-0.05
```
Unifica clips de distintas fuentes (LTX/Kling/Seedance/GPT) y da identidad. NO usar filtro de IG/TT (inconsistente). Looks alternos: "Cine" (+contraste, teal-orange) / "Moody" (-saturación). Elegido: **Warm Clean**.

## Reglas de captions (estilo CapCut, `.ass` + libass)
- Bold Arial, borde grueso, **tercio inferior** (NUNCA tapar la cara del talento).
- Chunks de 2-4 palabras, pop con `\t` scale + `\fad`, acento magenta `&H782DFF` en keywords.
- Timing proporcional al texto si no hay ASR; nudgear si algo se desfasa.

## Marca de agua + cierre (firma de toda pieza)
1. `araque-mark.png` arriba-derecha durante el video.
2. xfade al `endcard.html` (logo + CTA) como outro. Audio del cierre en silencio/fade.
