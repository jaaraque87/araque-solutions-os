# PILOTO 003 - Cola light generica 30s (UGC producto)

Run local preparado: `outputs/avatar/naia-cola-light-ugc-20260704-165008/`  
Cliente Hook Lab: `tools/hook-lab/clients/cola-light-generica/`  
Formato: reel 9:16, 30s aprox, varias escenas LTX de 4-7s. Nunca forzar LTX Director a mas de 15s por ejecucion.

## Concepto

Spec ad de producto realista para una bebida cola light generica, sin marca registrada. Naia no vende salud ni "vida fit"; vende el momento: una pausa fria, burbujeante y con sabor a cola.

**Hipotesis del scorecard:** atacar la objecion "light = sacrificio" deberia vender mejor que abrir con atributos tipo "zero", "sin culpa" o "bajo en calorias". Metrica: retencion en el hook y comentarios/DMs tipo "quiero probarla".

## Hook seleccionado (Hook Lab + Kallaway)

`No queria una cola light. Queria una pausa que supiera bien.`

Overlay: `LIGHT NO ES CASTIGO`

Por que gana:
- Rapid context: se entiende de que va en la primera frase.
- Contraste: light no como sacrificio, sino como pausa deseable.
- Promesa sensorial: "supiera bien" apunta a la objecion real.
- No necesita claims inventados.

## Guion segmentado

| SEG | Frase | Tipo | dur plan |
|---|---|---|---:|
| 1 | "No queria una cola light. Queria una pausa que supiera bien." | AVATAR lipsync | 4.1s |
| 2 | "Porque seamos honestos: muchas bebidas ligeras prometen demasiado... y saben a renuncia." | B-roll VO | 4.2s |
| 3 | "Esta no intenta venderte una vida perfecta. Va directo a lo que importa: fria, burbujeante, cola de verdad." | AVATAR lipsync | 6.1s |
| 4 | "La abri despues de una reunion larga, y ese primer sorbo hizo clic: refresca sin sentirse pesada." | B-roll VO | 5.8s |
| 5 | "Mi prueba es simple: si la termino sin pensar en otra, entra a mi nevera." | AVATAR lipsync | 4.9s |
| 6 | "Pruebala bien fria. Si te gusta la cola, esta pausa te va a sorprender." | AVATAR CTA | 5.2s |

Total estimado: 30.3s. Ajustar al audio real: LTX duration = audio segment +0.3s. Recortar b-roll, nunca avatar hablando.

## Audio ElevenLabs

No gastar API sin aprobacion. Usar voz Naia `rzpLrJDiI1CBeAvkbjNf`, **modelo `eleven_v3` + audio tags via endpoint `/with-timestamps`** (regla AGENTS.md #9 — multilingual_v2 queda prohibido, sonaba a locutora):

```json
{
  "stability": 0.5,
  "similarity_boost": 0.8
}
```

Agregar tags de actuacion al texto (no se hablan): `[casual]`, `[soft laugh]`, `[playful]`, `[warm]` segun la emocion de cada frase. Cortar por frases con los timestamps del alignment que devuelve el endpoint (Whisper no hace falta).

Texto preparado en `outputs/avatar/naia-cola-light-ugc-20260704-165008/elevenlabs_request.json`.

## Imagenes GPT

Adjuntar siempre el character sheet de Naia. Linea fisica canonica:

```text
young woman in her mid-twenties, short sleek black bob hair, hazel green eyes, pale warm olive skin, curvy hourglass figure, gold "N" initial necklace
```

Producto: lata generica matte charcoal, icono abstracto plateado, sin texto legible, sin Coca-Cola, sin Pepsi, sin logos.

Imagenes requeridas:
- `img-a-naia-hook.png` - Naia selfie con lata fria y vaso con hielo.
- `img-b-product-cold-can.png` - lata generica con condensacion, hielo y burbujas.
- `img-c-naia-explain.png` - Naia medium close-up explicando sabor.
- `img-d-pour-first-sip.png` - manos sirviendo cola sobre hielo.
- `img-e-naia-proof.png` - Naia con vaso casi terminado.

Prompts completos: `outputs/avatar/naia-cola-light-ugc-20260704-165008/image_prompts.md`.

## Prompts LTX Director

Prompts completos: `outputs/avatar/naia-cola-light-ugc-20260704-165008/ltx_prompts.md`.

Parametros:

```text
LTX23 AllInOne Director v30
CFG 1.2
30fps
576x1024 o mayor
vertical 9:16
duracion = audio del segmento + 0.3s
clips hablados 4-8s
b-roll sin audio input
```

Negativos:

```text
no extra limbs, no face warp, no object duplication, no text artifacts, no watermark, no flicker, no heavy camera shake, no multiple people, no brand logos, no readable label, no Coca-Cola, no Pepsi, no deformed hands, no melted can
```

## Ensamble

Guardar clips:

```text
clips/seg1-hook-avatar.mp4
clips/seg2-cold-can-broll.mp4
clips/seg3-turn-avatar.mp4
clips/seg4-pour-first-sip-broll.mp4
clips/seg5-proof-avatar.mp4
clips/seg6-cta-avatar.mp4
```

Luego concatenar, pegar audio master y pasar por `tools/content-reel-lab/scripts/render-batch.mjs` con hook `LIGHT NO ES CASTIGO` y CTA `PRUEBALA BIEN FRIA`.

## QA

- Identidad de Naia consistente con character sheet.
- Lata sin logos ni texto raro.
- No captions sobre ojos, boca, rostro, manos ni producto.
- El hook aparece antes de 2.7s.
- Ningun clip LTX pasa de 15s.
- No claims de salud, perdida de peso, energia o nutricion.

