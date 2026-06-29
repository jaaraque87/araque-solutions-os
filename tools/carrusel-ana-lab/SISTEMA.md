# Sistema Carrusel Educativo — Ana Lab

Reglas lockeadas del sistema de carruseles IG. Validado con piloto Pedro y Mateo (2026-06-10).
Este documento es la fuente de verdad. Si una regla cambia, se cambia acá primero.

---

## Regla 0 — Scorecard antes que estética

Cada carrusel se postea con **hipótesis explícita escrita ANTES de publicar** y se mide contra ella.

KPIs (marcas sin e-commerce, orgánico):
- Saves (métrica reina de carruseles)
- Shares
- Alcance / cuentas alcanzadas
- Follows atribuibles (delta 72h)
- DMs entrantes (especialmente "¿dónde lo consigo?")
- Visitas al perfil
- Bares/vinotecas nuevas que suman el producto (lag semanas)

Cada carpeta de carrusel lleva su `scorecard.md`. Sin scorecard no se postea.

## Regla 1 — Paleta: 3 colores, roles fijos

- **Primary** — color de marca, domina títulos y fondos plenos
- **Background** — neutro cálido, base de slides claros
- **Accent** — color secundario, números/rules/detalles. NUNCA protagonista

P&M: primary `#6F1D22` tinto · background `#F5EFE0` crema · accent `#6B7A3F` oliva.
Definidos en `brand.json`. El renderer no acepta colores fuera de la paleta.

## Regla 2 — Tipografía: 2 fonts, roles fijos

- **Display** — sans bold pesada, MAYÚSCULA, protagonista (P&M: Inter 900)
- **Personality** — serif italic, minúscula, decorativa/emocional (P&M: Fraunces italic 500)

Títulos mezclan ambas palabra por palabra (italic minúscula + bold MAYÚSCULA), estilo @mobileeditingclub. El italic se dimensiona ~4% más grande para compensar peso visual.

## Regla 3 — Narrativa: 5 beats, desarrollo con formato ROTATIVO

Los beats son fijos; el formato del desarrollo NO:

1. **Hook** (slide 1) — palabra o número hero gigante + opinión/promesa. Para el scroll. NO spoilea
2. **Promise** (slide 2) — completa el hook + beneficios concretos. Pausa visual sin foto
3. **Desarrollo** (slides 3 a N) — elegir UN formato por carrusel:
   - **Lista numerada** (`item` con number) — para tips/maridajes/rankings. Ej: 001
   - **Lista sin número** (`item` sin number) — ítems sueltos sin orden
   - **Narrativa secuencial** (`statement` encadenados: "primero… / después… / al final…") — para procesos/historia. Ej: 002
   - **Statements editoriales** — manifesto, declaraciones, Q&A (statement pregunta → respuesta)
   - **Respiro visual** (`fullphoto`) — foto protagonista + una línea. Intercalable en cualquier formato
4. **Ask/Closer** (último) — cierre suave de marca, sin CTA agresiva. Marca grande

**Rotación obligatoria:** carruseles consecutivos de la misma marca NO repiten formato de desarrollo. Si el 00N fue lista numerada, el 00N+1 usa otro.

## Regla 4 — Voz

Everyman cálido: voseo rioplatense, complicidad, humor seco, sin pretensión, frases cortas.
El body educativo enseña sin sermonear ("y ya estás", "nada más").
No mencionar competidores por nombre. La voz específica vive en `brand.json → voice`.

## Regla 5 — Foto: editorial documental premium cercano

- Estilo: Tyler Mitchell / Tim Walker / Aaron Graubart
- Film stock: Kodak Portra 400 (consistencia dentro del carrusel)
- Luz: golden hour natural, lived-in, never staged
- **Escenas VIVAS**: mesa en uso, manos en gesto, comida real, lugar habitado. Nunca bodegón muerto ni producto solo (lección del 002: las escenas estáticas de depósito rinden peor que la mesa viva del 001)
- **Variedad dentro del carrusel**: distancia focal distinta por slide (macro / medio / amplio), locación variada (interior / exterior / patio), con/sin persona parcial. Rostros parciales OK (nunca <25 años)
- Personas: "neutral mid-adult age, smooth healthy skin, no wrinkles" (sin marcadores de edad)
- Color crítico de producto especificado por hex en el prompt (P&M: vermouth `#5C1A1F` deep wine red, NEVER orange)
- **Cada prompt de foto reserva la zona limpia donde irá el texto** ("negative space upper-left kept clean for typographic overlay") — debe matchear el `anchor` del slide en `inputs.json`
- Calidad: la pasada de **Magnific es manual y opcional** — pisás el archivo generado y re-renderizás. El 001 (con Magnific) > 002 (sin) en textura

## Regla 6 — Layout: identidad consistente + composición variada

**Fijo en todos los slides:** paleta, fonts, footer (logo + handle), tratamiento de gradient.
**Varía por slide:** posición del bloque tipográfico (`anchor`), tamaños, dirección del gradient.
El gradient de legibilidad se deriva del anchor (texto abajo → gradient desde abajo, etc).
Esto pasa el grid test (perfil unificado) sin caer en plantilla monótona.

## Regla 7 — Beat 2 (promesa): pausa visual ROTATIVA

El slide 2 completa el hook, pero su forma rota entre carruseles (no siempre fondo pleno):
- **`promise`** — fondo primary pleno + grano de film + hero crema centrado. Sin foto
- **`statement` sobre foto** — composición editorial sobre imagen
- **`fullphoto`** — foto protagonista + una línea

Si el carrusel anterior usó promise pleno, este usa otra variante.

## Regla 8 — Closer: marca grande, cierre suave

Tipografía grande (la frase de cierre es protagonista), logo al doble de tamaño que en el resto, handle visible. Sin "comprá ya". El carrusel educativo convierte por autoridad, no por presión.

## Regla 9 — Dimensiones y export

1080×1350 (4:5 IG). Render: HTML 540×675 @2x deviceScaleFactor → JPEG quality 95.
Preview HTML antes de renderizar, siempre.

## Regla 10 — Legibilidad mobile

**El body es UNA frase instructiva, máximo ~70 caracteres.** Si la idea necesita más, el resto va al caption del post de IG, no al slide. Cada slide debe leerse en menos de 3 segundos.

Mínimos en píxeles de preview (540×675; multiplicar ×2 para real, ÷2.77 aprox para móvil físico):
- Caption italic: ≥ 20px
- Body: ≥ 19px
- Eyebrow: ≥ 16px
- Hero/título: sin máximo, que respire
- Text-shadow en todo texto sobre foto + gradient de legibilidad en la zona del bloque

## Regla 11 — Manifest de assets (gobierno)

Cada carrusel lleva `manifest.json` con, por foto: prompt usado, modelo, refinamiento (Magnific etc), fecha, quién aprobó, derechos. Si una imagen genera problemas (parecido a referencia, etiqueta alterada), hay trazabilidad. Sin manifest completo no se archiva como "done".

## Regla 12 — Compliance legal (alcohol AR)

**Obligatorio en toda pieza de bebidas alcohólicas** (Ley 24.788 + Decreto 149/2009):
- "PROHIBIDA SU VENTA A MENORES DE 18 AÑOS."
- "BEBER CON MODERACIÓN."

Implementación: leyenda automática en el slide closer (campo `compliance` en `brand.json` — el renderer la mete solo, no depende de acordarse). Repetir en el caption del post de IG.
Slides configurables vía `compliance.slides` (default: `["closer"]`).
Marcas sin alcohol: `compliance: null`.

---

## Estructura de archivos (este paquete)

```
carrusel-ana-lab/
  SISTEMA.md            ← este documento
  generar.js            ← renderer (Puppeteer): inputs.json → JPGs
  generar-fotos.mjs     ← fotos automáticas vía FAL (opcional)
  scorecard-template.md
  brands/<tu-marca>/
    brand.json          ← identidad: paleta, fonts, logo, handle, voz, compliance
    assets/             ← logo-clean.png (+ logo-dark.png, producto.jpg)
    carruseles/<NNN-slug>/
      inputs.json       ← slides de este carrusel (copy, foto, anchor, sizes)
      manifest.json     ← prompts de foto + trazabilidad
      fotos/            ← las fotos generadas
      scorecard.md      ← hipótesis + métricas
      preview.html      ← generado, abrir en browser para revisar
      output/           ← JPGs 1080×1350 finales
      runs.jsonl        ← log de corridas (append automático)
```

## Flujo de uso

**Con Claude como copiloto (recomendado):** abrí Claude Code en esta carpeta y pedile: *"Leé SISTEMA.md y armame un carrusel sobre [idea] para mi marca — escribí inputs.json y los prompts de foto en manifest.json"*. Claude desarrolla hook, copy y prompts respetando estas reglas. Después:

1. Fotos: `node generar-fotos.mjs <carpeta-carrusel>` (FAL automático) — o generálas a mano con los prompts del manifest en tu generador favorito
2. Render: `node generar.js <carpeta-carrusel>` → `preview.html` + JPGs en `output/`
3. Revisar preview → iterar copy/fotos con Claude → re-correr
4. Completar `scorecard.md` con hipótesis ANTES de postear
5. Postear → medir 24h/72h/7d → volcar al scorecard

## Mejoras anotadas (no hacer hasta que duela)

- Fonts locales en vez de Google Fonts CDN (reproducibilidad offline)
- Para Vercel/SaaS: job queue + worker + storage (NO Puppeteer síncrono en serverless)
- text_anchor como parámetro inyectado en prompts de generación de foto (pipeline foto↔layout)
- Grid test automatizado: composición 3×3 de últimos 9 posts

---
## Tipos de slide disponibles (renderer v2.2)

| Tipo | Estructura | Uso |
|---|---|---|
| `hook` | eyebrow + hero (heroSize opcional) + sub + micro + captionBottom | slide 1 |
| `promise` | fondo primary + grano + hero + sub + rule + caption | slide 2 |
| `item` | number (opcional) + titleIt + titleBold + caption + body (opcional) | listas |
| `statement` | lines[] libre (it/bold por línea) + caption opcional | narrativa, Q&A, manifesto |
| `fullphoto` | foto + caption italic (acepta \n) | respiro visual |
| `closer` | eyebrow + titleIt + titleBold + titleIt2 + caption + logo grande + compliance | último |

Todos los tipos con foto aceptan: `anchor` (bottom-left / mid-left), `anchorTop`, `maxWidth`, `gradientStrength`, `sizes{}`.

---
*v1.1 — 2026-06-10. Piloto: P&M 001 (lista numerada) + 002 (narrativa). Review adversarial: Codex (GPT-5.5).*
