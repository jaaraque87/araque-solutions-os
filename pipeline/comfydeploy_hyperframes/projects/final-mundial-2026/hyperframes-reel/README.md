# Araque Solutions - Final Mundial 2026

Reel vertical de 22 segundos construido con HyperFrames. La composición integra cinco clips LTX, captions dinámicos, voz, ambiente de estadio y un cierre sincronizado con el audio original de `SEG5`.

## Requisitos

- Node.js 22 o superior
- FFmpeg y FFprobe disponibles en `PATH`
- Google Chrome o Chromium

## Restaurar los medios

Por política del repositorio, los videos y audios generados no se guardan en Git. Copia los siete archivos indicados en `assets/README.md` dentro de `assets/`. El logo `araque-watermark.png` sí está versionado.

## Ejecutar

```bash
cd pipeline/comfydeploy_hyperframes/projects/final-mundial-2026/hyperframes-reel
npm run dev
```

HyperFrames Studio se abre normalmente en `http://localhost:3002/#project/hyperframes-reel`.

## Validar y renderizar

```bash
npm run check
npm run render:final
```

HyperFrames está fijado en `0.7.64`. La salida esperada es `renders/araque-final-mundial-synced.mp4`: 1080x1920, 30 fps y 22.000 segundos.

Consulta `HANDOFF.md` para continuar el proyecto desde otra máquina.
