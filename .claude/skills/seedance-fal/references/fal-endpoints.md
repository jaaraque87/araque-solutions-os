# Seedance 2.0 on fal

Fuentes:

- https://fal.ai/models/bytedance/seedance-2.0/image-to-video/api
- https://fal.ai/models/bytedance/seedance-2.0/reference-to-video/api

## Regla Dura

Usar solo endpoints standard/non-fast. Nunca usar endpoints o variantes `fast`, aunque existan en fal.ai o parezcan equivalentes.

Permitidos:

- `bytedance/seedance-2.0/image-to-video`
- `bytedance/seedance-2.0/reference-to-video`

Prohibidos:

- cualquier endpoint con `/fast`
- cualquier variante `fast`
- fallback automatico a fast

## Endpoint 1

`bytedance/seedance-2.0/image-to-video`

### Uso

Animar una imagen inicial con un prompt de movimiento.

### Inputs

- `prompt` requerido
- `image_url` requerido
- `end_image_url` opcional
- `resolution`: `480p | 720p | 1080p`
- `duration`: `auto | 4..15`
- `aspect_ratio`: `auto | 21:9 | 16:9 | 4:3 | 1:1 | 3:4 | 9:16`
- `generate_audio`: boolean
- `seed`: integer
- `end_user_id`: string

### Cuándo elegirlo

- tenés un frame fuerte
- querés transformar still -> motion
- querés controlar start/end frame

## Endpoint 2

`bytedance/seedance-2.0/reference-to-video`

### Uso

Generar video guiado por varias referencias.

### Inputs

- `prompt` requerido
- `image_urls` opcional, hasta 9
- `video_urls` opcional, hasta 3
- `audio_urls` opcional, hasta 3
- `resolution`: `480p | 720p | 1080p`
- `duration`: `auto | 4..15`
- `aspect_ratio`: `auto | 21:9 | 16:9 | 4:3 | 1:1 | 3:4 | 9:16`
- `generate_audio`: boolean, default `true`; debe estar `true` para speech/sfx/lip sync audibles
- `seed`: integer
- `end_user_id`: string

### Límites importantes

- total de archivos entre modalidades: máximo 12
- `video_urls`: duración combinada entre 2 y 15 segundos
- `video_urls`: total size < 50 MB
- `audio_urls`: duración combinada <= 15 segundos
- `audio_urls`: max 15 MB por archivo
- si hay `audio_urls`, tiene que existir al menos una referencia de imagen o video

### Cuándo elegirlo

- necesitás mezclar varias referencias visuales
- querés controlar más el universo visual
- querés usar audio reference
- querés lip sync nativo con `@Audio1`, `@Audio2` o `@Audio3`
- hacés B-roll complejo o dirigido por múltiples inputs

## Output

Ambos devuelven:

- `video.url`
- `seed`

## Queue

fal expone:

- submit request
- status polling
- result fetch
- cancel

El helper de esta skill usa `fal_client.subscribe` para flujo simple y blocking, con opción de `--dry-run` para no ejecutar.
