# JARVIS HUD — centro de comando oscuro con glow naranja

**Cuándo usarlo:** tech/IA, sistemas y agentes ("mi sistema operativo de contenido",
"mi Jarvis"), features de Claude/Claude Code, pitches Morfeo Labs / Content Engine
(misma paleta obsidian+naranja del logo). Contenido que vende CONTROL y poder de sistema.
**Fuente:** disección del carrusel IG de @ramiro.cubria (post `DaYihscnCY7`, "sistema
operativo de contenido / JARVIS", 2026-07; bajado en `_research/omni-styles/DaYihscnCY7/`)
· **Validado:** BLOQUEADO POR FILTRO (2026-07-05, 5 variantes incluidas
overlay-holograma y data-viz sin texto: el combo dark+charts+data lo dispara hoy).
Reintentar otro día con el protocolo de diagnóstico del SKILL.md

## Bloque de estilo (va literal en el prompt, en inglés)

Cut me out completely from my original background — my original background must never be
visible — and keep my talking face, lip-sync and real clothing exactly as they are,
photographic, with a subtle warm orange rim-light so I sit inside the glow of the scene.
Place my cutout in a dark mission-control command center: a matte near-black canvas with
a faint thin blueprint grid, where dark UI panels with rounded corners and hairline gray
borders float around me — terminal windows, analytics dashboard cards, HUD frames with
corner brackets. Every data element glows warm amber-orange: particle-network clouds of
glowing orange nodes, orange line charts, donut charts, progress bars, tiny orange arrows.
Decorative panels carry charts, bars, nodes and abstract tick-mark lines ONLY — no
readable text inside any panel; the only readable text on screen are the punch words
spelled in this prompt. Dark cinematic mood, high contrast, crisp UI edges — it must read
like a sci-fi JARVIS command center built from real modern dashboard UI, never a flat
illustration.

La capa de motion sobre esto es el canon STICKER PUNCH del SKILL.md (obligatoria, este
bloque solo aporta mundo y paleta).

## Estados de fondo

Constante: negro mate + grilla sutil + glow naranja ámbar. Rotar el motivo dominante por
beat de frase (y reordenar entre clips):

1. **Grid puro** — canvas negro + grilla tenue, el sujeto solo (estado de respiro).
2. **Nube de red** — nube de partículas/nodos naranjas glow (la imagen firma del estilo).
3. **Dashboard** — pared de cards analíticas oscuras con charts naranjas.
4. **Terminal** — ventana de terminal grande y oscura con líneas abstractas corriendo.
5. **HUD** — marco mission-control con corner brackets y micro-ticks.
6. **Graph multicolor** (acento, máx 1 por clip) — mapa de nodos teal/lima/amarillo tipo
   vault de Obsidian; el único estado no-naranja.

## Captions

Punch words ALL-CAPS en **grotesca pesada blanca** (Helvetica bold), con LA keyword de la
frase en naranja ámbar; ≥8% del alto del frame. Acento secundario: 1-2 palabras clave por
clip (nombre de producto, número) en **fuente pixel 8-bit gorda color coral** (como el
"FABLE 5" de la referencia). Flechas "→" naranjas como bullet/acento. Todo deletreado en
el prompt: "spelling exactly: '…'", keyword y color incluidos.

## Doodads

Un prop de UI oscura literal por frase, popeando al beat de la palabra con glow naranja:
se nombra un comando → terminal tipeando; un número/métrica → metric card con ese número
(deletreado); crecimiento → chart naranja spikeando; conexión/contexto → nodo que se
enciende en la nube de red. Si se nombra Claude/Anthropic → sticker cuadrado blanco
redondeado con el starburst coral (el de la referencia, con coronita) popeando junto al
sujeto.

## Refs

`refs/ref_cover.jpg` (tipografía mixta serif+pixel, sticker starburst, nube de red),
`refs/ref_hud.jpg` (HUD mission-control completo), `refs/ref_dashboard.jpg` (cards
analíticas naranjas), `refs/ref_terminal.jpg` (terminal monospace). Default: solo texto.
Adjuntar como IMAGE_REF únicamente si el mundo UI sale "ilustración plana" o el glow
deriva — sabiendo que IMAGE_REF puede teñir la cara del sujeto (regla del SKILL.md):
priorizar reforzar el bloque antes que adjuntar.

## QA específico

- **Identidad primero**: mundo oscuro + glow tiñe caras; confirmar cara fotográfica de la
  fuente y rim light sin cambiar el tono de piel.
- **Separación del fondo**: sujeto sobre negro se funde; verificar que el rim light naranja
  lo despega. Cutout sin halo del fondo original.
- **Paleta**: naranja ámbar cálido consistente — si deriva a rojo, amarillo o charts
  rainbow, falló. El estado multicolor aparece máximo una vez por clip.
- **Grilla sutil**: si se lee como papel milimetrado brillante o wireframe protagonista,
  falló.
- **Cero pseudo-texto**: paneles, terminales y dashboards SIN texto legible (solo ticks
  abstractos/charts); si Omni hornea texto basura en un panel, reemplazar el elemento
  entero (regla del SKILL.md, no editarlo).
- **Pixel words**: verificar letra por letra sobre crop a resolución nativa — la fuente
  pixel comprimida genera falsos positivos de typo.
