# Anatomía de un estilo + cómo crear/copiar uno

## Qué ES un estilo acá

Lo que Higgsfield guarda como "preset" (media de referencia + prompt corto interno),
nosotros lo guardamos destilado y versionado: un `style.md` legible + stills opcionales.
Ventajas: editable, diffeable, no depende de un servicio, y el prompt resultante es
auditable antes de gastar generación.

## Template de `styles/<slug>/style.md`

```markdown
# <Nombre> — <una línea de identidad>

**Cuándo usarlo:** <tipo de contenido al que le queda>
**Fuente:** <de dónde salió: disección de X, creado para Y> · **Validado:** sí/no

## Bloque de estilo (va literal en el prompt, en inglés)
<El párrafo fijo: mundo, material, tratamiento del sujeto, lettering de captions,
textura, grade. NO incluye timecodes ni contenido del clip — eso es variable.>

## Estados de fondo
<Paleta de 3-6 estados (color/motivo) para rotar entre beats de frase y entre clips.>

## Captions
<Formato exacto del lettering del estilo, posición, y regla de keyword si tiene.>

## Doodads
<Regla de props literales: material, tamaño, dónde entran.>

## Refs
<refs/*.jpg si hay; cuándo adjuntarlos como IMAGE_REF.>

## QA específico
<Qué se rompe típicamente en este estilo.>
```

## Copiar un estilo ajeno (el flujo "me gusta ese look")

1. **Conseguir referencia**: URL de video (preview de preset, short de TikTok, reel) →
   bajar (curl/yt-dlp). Si son imágenes, directo.
2. **Strip de frames**: `ffmpeg -vf "fps=1,scale=150:-1,tile=8x1"` → mirar la tira.
3. **Disección — framework de 5 puntos** (responder TODOS mirando frames, no de memoria):
   1. **Sujeto**: ¿keyed real con borde? ¿full-restyle? ¿qué ancla real conserva (desk/laptop)?
   2. **Mundo**: ¿de qué material/tema es el fondo? ¿un universo coherente o collage?
   3. **Estados**: ¿cómo cambia el fondo entre beats? (color, motivo, qué queda constante)
   4. **Captions**: ¿frase o palabra? ¿de qué está hecho el lettering? ¿posición? ¿keyword?
   5. **Doodads**: ¿hay props literales a lo dicho? ¿material? ¿frecuencia?
4. **Escribir el `style.md`** con el template; el bloque de estilo se escribe describiendo
   lo VISTO (material, bordes, texturas, grade), no adjetivos genéricos.
5. **Guardar 2-4 stills** representativos en `refs/` (momentos con caption visible,
   cambio de estado, doodad en pantalla).
6. **Validar con una generación de prueba** en un clip corto real: aplicar el flujo
   normal y correr el QA del estilo. Si el material deriva (clay que se vuelve render 3D,
   marcador que se vuelve vector), reforzar el bloque con la textura ("hand-made,
   imperfect, visible fingerprints/paper grain") o adjuntar refs como IMAGE_REF.
   Recién ahí marcar **Validado: sí**.

## Crear un estilo original

Mismo template, pero el punto de partida es una dirección de arte (de la marca o del
formato): elegir UN material/mundo, definir los 5 puntos a mano, y validar igual. Un
estilo de marca hereda paleta/tipografía del brand kit (`brands/<Brand>/`) traducidas al
material ("captions in torn paper strips in the brand's coral").

## References-to-video (cuándo adjuntar refs)

Default: solo texto (el bloque de estilo destilado suele alcanzar y es más barato de
iterar). Adjuntar `refs/*.jpg` como `IMAGE_REF` cuando: (a) el material derivó en la
prueba, (b) el estilo tiene una textura difícil de nombrar, (c) se copia un look muy
específico. Comando y sintaxis de roles: ver `omni-hook/references/shorts-maker-styles.md`.
