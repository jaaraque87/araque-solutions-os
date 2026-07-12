---
name: seedance-fal
description: "Use when the user wants to generate Seedance 2.0 videos through fal.ai using the standard non-fast endpoints, choose between bytedance/seedance-2.0/image-to-video and bytedance/seedance-2.0/reference-to-video, preview payload variables before execution, upload local refs, or run Seedance B-roll from prompts."
---

# Seedance fal

Esta skill ejecuta Seedance 2.0 vía fal.ai.

## Hard Rule: Never Fast

Nunca uses endpoints, modelos, variantes o shortcuts `fast` para Seedance.

Permitidos:

- `bytedance/seedance-2.0/image-to-video`
- `bytedance/seedance-2.0/reference-to-video`

Prohibido:

- cualquier endpoint con `/fast`
- cualquier variante llamada `fast`
- cualquier fallback a fast para ahorrar tiempo/costo

Si el usuario pide `fast`, explica que el contrato del proyecto usa solo endpoints standard/non-fast y propone ejecutar el endpoint standard equivalente.

## Qué leer

1. `references/fal-endpoints.md`
2. Si vas a correr algo, usá `scripts/run_seedance_fal.py --dry-run` primero

## Cuándo usar cada endpoint

- `bytedance/seedance-2.0/image-to-video`
  - una sola imagen inicial
  - opcionalmente una imagen final
  - ideal para animar un frame o una placa ya resuelta

- `bytedance/seedance-2.0/reference-to-video`
  - múltiples referencias
  - hasta 9 imágenes, 3 videos, 3 audios
  - ideal para B-roll más dirigido, mezcla de referencias, o clips con tono / cámara / audio guiado por varias fuentes
  - obligatorio cuando el prompt usa `@Audio1`, `@Audio2` o `@Audio3`

## Regla operativa

Antes de ejecutar:

1. elegí endpoint
2. armá prompt final
3. mostrale al usuario las variables
4. corré `--dry-run`
5. verificá que el endpoint no sea `fast`
6. recién después ejecutá

## Helper

Usá:

```bash
python3 ~/.codex/skills/seedance-fal/scripts/run_seedance_fal.py --help
```

El helper:

- acepta paths locales o URLs
- sube refs locales a fal storage
- imprime payload listo
- puede correr en `--dry-run` o ejecutar
- guarda prompt, payload y resultado en un output dir

## Defaults recomendados para B-roll

- `resolution`: `720p`
- `aspect_ratio`: `9:16`
- `duration`: `5` o `6`
- `generate_audio`: `false` salvo que el sonido sea parte del concepto
- `seed`: fijarlo si querés iteración controlada

## Defaults recomendados para lip sync

- `endpoint`: `reference-to-video`
- `resolution`: `720p` para test, `1080p` para final curado
- `generate_audio`: `true`
- `duration`: igual a la duracion hablada/cantada, entre `4` y `15`
- `audio`: hasta 3 refs MP3/WAV, maximo 15s combinados y 15 MB por archivo
- `image` o `video`: al menos una referencia visual cuando hay audio
- prompt: mapear cada `@AudioN` a un speaker visible y describir emocion, conducta corporal y timing

## Gate de ejecución para lip sync

Antes del `--dry-run`, verificá:

- hay al menos una referencia visual si existen `audio_urls`;
- cada audio del payload aparece en el prompt como `@AudioN`;
- cada `@AudioN` tiene dueño visible por descripción física o posición en cuadro;
- `generate_audio` está en `true`;
- `duration` cubre la duración hablada/cantada y no supera `15`;
- si el audio es solo referencia de tono y el texto pedido es distinto, la respuesta lo marca como riesgo y recomienda audio con frase final;
- el prompt protege la boca: close-up del speaker activo, sin cortes ni objetos tapando labios en sílabas importantes.

## Reglas de prompting para ejecución

- si el prompt viene de `$seedance-anchor-method`, respetalo tal cual
- si el prompt viene de `$seedance-broll`, preferí clips cortos con una sola metáfora visual
- para refs múltiples, nombralas en el prompt como `@Image1`, `@Image2`, `@Video1`, `@Audio1`
- no mandes audio reference sin al menos una imagen o video reference
- si hay varios audios, no ejecutes hasta que el prompt diga explicitamente quien usa cada `@AudioN`

## Entregable esperado

Cuando ejecutes, devolvé:

- endpoint elegido
- variables usadas
- output dir
- archivos resultantes
- cualquier limitación relevante detectada en refs o duración
