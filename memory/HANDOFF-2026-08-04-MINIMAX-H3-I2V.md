# Handoff — MiniMax H3 I2V de alta resolución / melan 130

Fecha: 2026-08-04  
Equipo: PC SOPORTE2, Windows, zona horaria `America/Bogota`  
Estado: segunda prueba I2V revisada y aprobada para montaje con recorte estratégico.

## Contexto

Se continuó evaluando MiniMax H3 para generar un hero shot UGC de Johana sosteniendo `mesoprotech melan 130 pigment control 50+`. El objetivo comercial es demostrar que Araque Solutions puede animar un producto real sin que el envase pierda su identidad y reutilizar la misma pieza en la comunicación B2B de Ana.

La nueva prueba fue ejecutada manualmente después de una primera generación de baja resolución. No se hizo ninguna llamada adicional a fal.ai ni se consumieron créditos durante la revisión local.

## Archivos locales evaluados

Primera prueba, baja resolución:

```text
C:\Users\SOPORTE2\Downloads\MiniMax_H3_00001_.mp4
```

Segunda prueba, alta resolución:

```text
C:\Users\SOPORTE2\Downloads\MiniMax_H3_00001_ (1).mp4
```

Imagen fuente del personaje y producto usada en el proceso:

```text
C:\Users\SOPORTE2\Downloads\ANA-MELAN130-LTX-B2B-V3\S01-HOOK-LTX-SOURCE-FULL-720x1280.png
```

Material de revisión generado localmente:

```text
C:\Users\SOPORTE2\Downloads\MiniMax_H3_review_high\contact-sheet.png
C:\Users\SOPORTE2\Downloads\MiniMax_H3_review_high\product-detail.png
```

Estos assets no están en Git. Deben transferirse a la otra PC mediante OneDrive, Google Drive, Syncthing o almacenamiento externo.

## Comparación técnica

### Primera prueba

- Resolución: 416 × 736.
- Fotogramas: 24 fps.
- Duración: 5.167 s.
- Bitrate aproximado: 492 kbps.
- Peso: 318,095 bytes.
- Resultado: movimiento aceptable, pero fidelidad insuficiente para leer y conservar la etiqueta.

### Segunda prueba

- Resolución: 1088 × 1920.
- Fotogramas: 24 fps.
- Duración: 5.167 s.
- Códec de video: H.264.
- Audio: AAC estéreo, 32 kHz.
- Bitrate aproximado: 1.984 Mbps.
- Peso: 1,281,285 bytes.
- Resultado: mejora muy grande en nitidez, estabilidad de la botella y legibilidad principal.

La salida medida tiene aproximadamente 2.09 megapíxeles, aunque la interfaz o preset utilizado se haya descrito de otra manera.

## Evaluación visual de la segunda prueba

Aspectos aprobados:

- Johana conserva rostro, cabello, gafas, vestuario y presencia profesional.
- El envase mantiene forma, escala, orientación y color.
- La mano y el brazo bajan el producto de manera natural.
- No aparece una botella duplicada ni una etiqueta flotante.
- El fondo se mantiene estable.
- `melan 130`, `pigment control`, `50+` y `mesoestetic` son reconocibles durante el hook.
- El parpadeo, la respiración y el gesto final se sienten naturales.

Limitaciones todavía visibles:

- `mesoprotech` y parte de la tipografía pequeña presentan ligeras alteraciones de glifos.
- El texto regulatorio diminuto no es completamente exacto ni legible.
- La etiqueta se suaviza o deforma cuando la botella comienza a bajar, algo aceptable si se corta en ese momento.
- No conviene congelar el envase durante varios segundos ni hacer un zoom extremo sobre la letra pequeña.

Valoración interna aproximada:

- Primera prueba: 3/10 para uso comercial del producto.
- Segunda prueba: 8/10 con edición controlada.

## Decisión de producción

Para este reel no se recomienda gastar otra generación en R2V. La combinación más eficiente es:

1. MiniMax H3 I2V en alta resolución para el movimiento UGC.
2. Exposición breve del producto durante el tramo más estable.
3. Motion graphics para mostrar el nombre exacto y la información comercial.
4. HyperFrames para montaje, subtítulos, SFX, branding y CTA.

R2V solo se justificaría si el cliente exige exactitud de toda la microtipografía durante movimientos prolongados o rotación del envase.

## Montaje recomendado

- `00:00–00:00.90`: hero shot con el producto frente a cámara.
- `00:00.90–00:01.20`: Johana comienza a bajar el producto; realizar transición o corte.
- `00:01.20–00:02.20`: motion graphic limpio con el nombre exacto:

```text
mesoprotech® melan 130 pigment control
```

- Desde aproximadamente `00:02.20`: recuperar a Johana con el gesto natural y continuar el mensaje o CTA.

Para Araque Solutions puede acompañarse con una promesa como:

```text
Producto real. Etiqueta visible. Movimiento generado con IA.
```

No volver a colocar una imagen estática bloqueando la etiqueta sobre la botella animada: en la prueba anterior esa capa quedó flotando cuando la mano se movió.

## Prompt intent recomendado para futuras iteraciones I2V

El prompt exacto introducido manualmente no quedó registrado en el repositorio. La intención que produjo el resultado aprobado debe conservar:

- cámara vertical fija a la altura de los ojos;
- UGC profesional y natural, no comercial cinematográfico;
- Johana sostiene el producto frontal y estable durante menos de un segundo;
- etiqueta orientada directamente a cámara, botella vertical y a escala real;
- luego baja el brazo suavemente hasta sacar el producto del encuadre;
- mirada directa, respiración, un parpadeo y gesto conversacional discreto;
- sin zoom, paneo, dolly, rotación del producto, cambio de mano, duplicación, texto añadido, subtítulos o deformación del envase.

## Próximo paso desde la otra PC

1. Ejecutar `git pull` en `araque-solutions-os`.
2. Transferir la segunda prueba, la imagen fuente y las dos imágenes de revisión fuera de Git.
3. Incorporar la segunda prueba al proyecto HyperFrames correspondiente.
4. Aplicar el corte temporal recomendado; no usar la primera prueba de 416 × 736.
5. Revisar en preview el frame exacto de transición antes del render final.
6. Renderizar versiones Ana e Araque sin volver a generar el video salvo que se detecte un defecto nuevo y material.

## Estado de sincronización

- `git pull --ff-only`: `Already up to date`.
- La rama activa es `main`.
- Se preservaron los archivos locales sin seguimiento preexistentes en `pipeline/workflows/`, `scratch/`, `tools/creative-intelligence/` y `tools/fal-jobs/`.
- Ningún secreto, `.env`, video, audio o render fue agregado a Git.
