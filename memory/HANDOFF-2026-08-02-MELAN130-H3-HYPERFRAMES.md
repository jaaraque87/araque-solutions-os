# Handoff — melan 130 / MiniMax H3 / HyperFrames

Fecha: 2026-08-02
Equipo de producción: PC SOPORTE2, Windows, zona horaria America/Bogota
Estado: dos MP4 finales renderizados y verificados localmente.

## Objetivo cumplido

Se produjeron dos reels reutilizando un hero hook UGC de producto:

1. **Ana / mesoestetic:** comunicación comercial B2B para médicos, clínicas y profesionales de estética.
2. **Araque Solutions:** caso demostrativo sobre producción de anuncios con IA manteniendo el producto bajo control.

El hook muestra a Johana sosteniendo melan 130, hablando con lipsync y bajando el producto con un movimiento natural del brazo.

## Generación controlada

- Proveedor/modelo: `fal.ai` → `minimax/h3/reference-to-video`.
- Una sola generación autorizada: 5 s, 2K, 9:16.
- Costo estimado autorizado y consumido: **US$1.30**.
- Request ID: `019fc419-612a-71e0-9c5d-07ece62a3cb6`.
- No se hicieron reintentos ni generaciones duplicadas.
- La credencial fal permanece únicamente en `pipeline/.env`; no se incluyó en Git.

Runner local utilizado:

```text
tools/fal-jobs/ana_melan_h3.mjs
```

El runner sigue sin seguimiento porque contiene rutas absolutas de esta PC; debe hacerse portable antes de incorporarlo al repositorio.

## Decisión visual importante

Inicialmente se añadió una imagen recortada sobre la etiqueta para bloquear el texto. En revisión se confirmó que MiniMax ya conservaba suficientemente el envase y que la capa adicional quedaba flotando cuando Johana bajaba la mano.

La superposición se eliminó completamente en ambas composiciones:

- cero referencias a `label-lock`;
- cero referencias a `product-label-lock`;
- el hero visible proviene únicamente del MP4 de MiniMax;
- no se modificó el movimiento natural del brazo.

## Proyectos HyperFrames locales

Ana:

```text
C:\Users\SOPORTE2\Documents\AraqueSolutions\deliveries\mesoestetic-melan130-ana-final
```

Araque:

```text
C:\Users\SOPORTE2\Documents\AraqueSolutions\deliveries\mesoestetic-melan130-araque-final
```

Los proyectos y sus assets son archivos de producción locales y no se subieron a GitHub.

## MP4 finales

Ana:

```text
C:\Users\SOPORTE2\Documents\AraqueSolutions\deliveries\mesoestetic-melan130-ana-final\renders\ANA-MESOESTETIC-MELAN130-FINAL.mp4
```

- 17.90 s
- 1080 × 1920
- 30 fps
- H.264 + AAC
- 14,948,394 bytes
- decodificación completa verificada con FFmpeg

Araque:

```text
C:\Users\SOPORTE2\Documents\AraqueSolutions\deliveries\mesoestetic-melan130-araque-final\renders\ARAQUE-SOLUTIONS-MELAN130-FINAL.mp4
```

- 15.37 s
- 1080 × 1920
- 30 fps
- H.264 + AAC
- 8,618,357 bytes
- decodificación completa verificada con FFmpeg

## Validaciones

Después de retirar la superposición:

- Ana: HyperFrames `check` aprobado con 0 errores y 0 advertencias; 13/13 pruebas de contraste.
- Araque: HyperFrames `check` aprobado con 0 errores y 0 advertencias; 13/13 pruebas de contraste.
- Los servidores de preview en puertos 3011 y 3012 fueron cerrados antes del render para liberar recursos.
- Render final local con HyperFrames 0.7.89, calidad alta, 30 fps y Chrome del sistema.
- Ninguna API externa fue llamada durante el montaje o render final.

## Programación acordada

Reel Araque Solutions:

- Fecha: lunes 2026-08-03.
- Hora: 12:15 p. m. Colombia (`America/Bogota`).
- Equivalente Venezuela: 1:15 p. m.
- Redes: TikTok e Instagram.
- CTA del video y caption: DM `PRODUCTO`.

## Captions aprobables

### Araque — TikTok

```text
Video de producto con IA sin perder la identidad del envase.

El reto no era solo animarlo: era mantener producto, escala y mensaje bajo control mientras construíamos una pieza que pudiera vender.

¿Quieres probar este sistema con tu producto? Escribe PRODUCTO por DM.

#VideoDeProducto #PublicidadConIA #UGCParaMarcas #MarketingDeContenido #AraqueSolutions
```

### Araque — Instagram

```text
Tu producto no debería dejar de parecer tu producto cuando lo animas con IA.

En este caso construimos una pieza completa con:
• UGC realista
• producto reconocible y a escala creíble
• lipsync, motion graphics y subtítulos
• un CTA pensado para convertir

La herramienta genera. El sistema mantiene el control.

¿Quieres uno para tu marca? Envíanos PRODUCTO por DM.

#VideoMarketing #PublicidadConIA #ContenidoUGC #ProductMarketing #AraqueSolutions
```

### Ana / mesoestetic — Instagram

```text
¿Trabajas en medicina estética, dermatología o estética profesional?

Conoce melan 130 pigment control SPF 50+, fotoprotección con color dentro del portafolio mesoestetic.

Si deseas información comercial, disponibilidad y acompañamiento para tu consulta o cabina, escribe MELAN PRO por DM.

Johana te orienta. Ana, tu representante comercial, te atiende directamente.

Información comercial dirigida a profesionales. Uso según ficha técnica y criterio profesional.

#Mesoestetic #MedicinaEstetica #Dermatologia #EsteticaProfesional #Fotoproteccion
```

## Para continuar desde otro PC

1. Ejecutar `git pull` en el repositorio.
2. Los MP4 y assets no viajan por Git. Transferir la carpeta de entregables mediante OneDrive, Google Drive o Syncthing.
3. Confirmar que el reel de Araque esté programado para 12:15 p. m. Colombia en ambas redes.
4. Ana puede programarse después de confirmar fecha, red principal y acceso a `@ana.mesoestetic`.
5. Después de publicar, registrar métricas de 1 h, 24 h y 72 h: retención inicial, tiempo medio, finalización, visitas al perfil, DMs y consultas con las palabras clave.

## Estado Git al iniciar el handoff

- `git pull --ff-only`: **Already up to date**.
- Existían archivos locales sin seguimiento en `scratch/`, `tools/creative-intelligence/` y `tools/fal-jobs/`.
- No se agregaron esos archivos al commit del handoff.
