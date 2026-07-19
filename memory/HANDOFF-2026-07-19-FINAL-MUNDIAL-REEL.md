# Handoff - Reel Final Mundial 2026

Fecha: 2026-07-19  
Proyecto: Araque Solutions / Naia Cruz  
Estado: composición aprobada y render final validado en el PC de producción.

## Continuar desde otro PC

```bash
git clone https://github.com/jaaraque87/araque-solutions-os.git
cd araque-solutions-os
git switch feat/final-mundial-2026-reel
cd pipeline/comfydeploy_hyperframes/projects/final-mundial-2026/hyperframes-reel
```

Restaura los archivos descritos en `assets/README.md`, instala Node.js 22+, FFmpeg y Chrome/Chromium, y ejecuta:

```bash
npm run dev
npm run check
npm run render:final
```

No hay secretos ni API keys dentro de este proyecto. `npx` descargará HyperFrames `0.7.64` la primera vez que se ejecute.

## Estado técnico validado

- Formato: 1080x1920 vertical.
- Duración: 22.000 s.
- Frecuencia: 30 fps / 660 frames.
- Video final: H.264 con audio AAC.
- `hyperframes check`: 0 errores y 0 advertencias.
- Sincronía del cierre: retraso medido de 0 ms.
- El último clip comienza a 19.645 s usando offset interno 3.874 s.
- La voz principal termina a 19.645 s; desde allí se usa el audio incorporado de `ltx-05-cierre.mp4`.

## Timeline

| Tiempo | Segmento |
| --- | --- |
| 0.000-4.620 | Hook LTX |
| 4.620-9.900 | Mesa táctica |
| 9.900-15.585 | Naia / sistema |
| 15.585-19.645 | Estadio / final |
| 19.645-22.000 | Cierre LTX, offset 3.874 s |

## Archivos fuente importantes

- `index.html`: composición, captions, transiciones y mezcla de audio.
- `frame.md`: dirección visual.
- `BRIEF.md`: objetivo y estructura creativa.
- `hyperframes.json`: configuración del render.
- `.media/manifest.jsonl`: inventario de medios.

## Pendiente fuera de Git

- Copiar o descargar los siete medios privados indicados en `assets/README.md`.
- Publicar el MP4 aprobado en Instagram si aún no se ha publicado.
- Si se desea portabilidad total sin transferencia manual, subir los medios a almacenamiento privado y documentar sus URLs en un gestor de secretos; no incorporarlos al historial Git.
