# Handoff de contenido y automatización — 2026-07-16

Este documento es el punto de entrada portable para continuar el sistema de
producción y marketing desde otro PC. El repositorio contiene procesos, código,
prompts y documentación. Los assets, renders y ZIP de entrega permanecen fuera
de Git por política del repositorio.

## Respaldo local verificado

### Paquete base

- Archivo: `HANDOFF-CONTENIDO-IA-2026-07-15.zip`
- Tamaño: 152,68 MB
- SHA-256: `E31962A67DB51CE61DEB876376D6A3C9CB1CD0071EFE1F3EF2415B67F4DC43C5`

### Delta del 16 de julio

- Archivo: `HANDOFF-DELTA-CONTENIDO-IA-2026-07-16.zip`
- Tamaño: 19,46 MB
- Entradas: 51
- SHA-256: `DFEC924DB235A5C3F5BC04C40885069C64501033E4E817BF0DA960DDD984D862`
- El manifiesto interno SHA-256 fue verificado correctamente.

En el PC de origen ambos paquetes están en `C:\Users\SOPORTE2\Downloads\`.
En otro equipo pueden ubicarse en cualquier carpeta; se debe verificar cada hash
antes de descomprimir.

## ComeSano by Ana

Proyecto final: `comesano-reel-team-yuca-platano`.

- Concepto: “Tu desayuno no tiene que sonar complicado”.
- CTA: “¿TEAM YUCA o TEAM PLÁTANO?”.
- Entrega: 1080×1920, 30 fps, H.264/AAC, 16,0 segundos.
- Los rótulos `YUCA` y `PLÁTANO` fueron corregidos y tienen tiempo de lectura.
- La cadencia conserva motion dinámico, con pausas adicionales en puntos clave.
- SHA-256 del MP4 final:
  `B40D88B04EC6939FAD88758C5AF363FA4F134F831B8B456A40B1330C1A3BA5C6`.
- Ana dispone de aproximadamente USD 3 semanales para Instagram Ads. Con ese
  presupuesto se valida primero en orgánico y solo se impulsa un ganador local;
  no se fragmenta entre varios conjuntos o creatividades.

Las fuentes y el MP4 están en el paquete delta bajo
`projects/comesano-by-ana/videos/comesano-reel-team-yuca-platano/`.

## Automatización preservada en Git

### TAO Director

`tools/tao-director/render_scene.py` convierte una imagen aprobada y su audio
correspondiente en una escena determinista. Usa seed fijo, duración a 24 fps,
modo `--dry-run`, descarga controlada y manifiesto de hashes.

### Builder Orchestrator

`tools/builder-orchestrator/` monta kits y renderiza de forma headless. Evita
heredar outputs, identifica cada escena por contrato y hashes, rechaza clips de
slots equivocados y bloquea rutas duplicadas antes del stitch.

Pruebas verificadas el 2026-07-16:

- Builder Orchestrator: 11/11.
- TAO Director: 3/3.
- Compilación Python: correcta para los tres scripts de producción.

### Arquitectura recomendada

`kit/contrato → TAO por escena → QA automático → HyperFrames → master final`

TAO resuelve actuación y lipsync. HyperFrames ensambla, añade captions, overlays,
CTA, música/SFX y exporta. El orden se determina por `scene_id + hash`, nunca por
el nombre remoto ni por el orden de finalización.

## Nuevo cliente: objetivo siguiente

Crear un proyecto independiente para gestionar Instagram y TikTok con trazabilidad
desde contenido hasta conversaciones, pedidos, margen y recompra. El SOP está en
`docs/marketing/plan-instagram-tiktok-rentable.md`.

Al iniciar:

1. Revisar los assets y sus permisos sin pedir contraseñas por chat.
2. Definir oferta, precios, margen, capacidad, ubicación y conversión principal.
3. Construir inventario y manifiesto SHA-256.
4. Levantar baseline de Instagram, TikTok y ventas.
5. Ejecutar research con competidores directos, performer data, Trend Picker y
   Organic Marketing.
6. Crear hipótesis, hooks y guiones; evaluarlos con el scorecard antes de producir.
7. Aprobar wireframes por lote, producir en HyperFrames, verificar y publicar.
8. Medir con IDs trazables e iterar semanalmente por señales de negocio.

## Inicio en otro PC

1. Clonar este repositorio y leer `AGENTS.md`.
2. Abrir este archivo.
3. Copiar los dos ZIP al equipo nuevo y verificar sus SHA-256.
4. Descomprimir el paquete base y después el delta.
5. Abrir el `HANDOFF.md` del paquete base y `CONTEXTO-PARA-NUEVO-CODEX.md` del
   delta.
6. Instalar dependencias siguiendo los README de cada herramienta; no copiar
   `.env`, caches ni credenciales desde Git.
