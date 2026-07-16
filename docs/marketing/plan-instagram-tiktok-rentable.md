# SOP — Instagram y TikTok rentables

## Principio rector

El objetivo no es publicar por volumen. El sistema debe conectar contenido con
conversaciones, pedidos y margen. La rentabilidad no se promete: se define la
economía del negocio, se instrumenta el recorrido y se optimiza semanalmente.

## 0. Definir qué significa ganar

Documentar oferta, precios, ticket promedio, margen bruto, capacidad semanal,
zona de atención, horarios, restricciones y conversión primaria. Fijar objetivos
de 30, 60 y 90 días, CAC máximo y pedido mínimo rentable.

Salida: `00-business/ECONOMIA-DEL-NEGOCIO.md`.

## 1. Ingesta segura de assets

1. Copiar originales sin modificarlos a `04-assets/source/`.
2. Crear inventario, descripciones y manifiesto SHA-256.
3. Clasificar logo, producto, personas, locaciones, testimonios, B-roll y audio.
4. Registrar derechos de uso de rostros, voces, música y testimonios.
5. Mantener contraseñas y tokens fuera del proyecto.

## 2. Accesos y línea base

Solicitar acceso seguro a Instagram Professional/Meta Business Suite y TikTok
Analytics, además de exportes de Insights de 30–90 días y datos agregados de
WhatsApp, CRM o pedidos cuando existan.

Registrar seguidores, alcance, vistas, retención, completados, compartidos,
guardados, comentarios, visitas al perfil, clics, conversaciones, leads, pedidos,
ingresos y margen.

Salida: `01-research/BASELINE.md` y tablero de control.

## 3. Research competitivo y performer

- Seleccionar entre 5 y 10 competidores directos, adyacentes y referentes.
- Revisar Instagram, TikTok, bibliotecas públicas de anuncios y web abierta.
- Usar `niche-radar` para mapear nicho y competidores cuando esté disponible.
- Normalizar performer data por tamaño de cuenta y antigüedad de publicación.
- Registrar hook, primer visual, duración, estructura, edición, sonido, CTA,
  comentarios y señales de intención de compra.
- Aplicar Trend Picker para oportunidades actuales con encaje real de marca.
- Adoptar mecanismos probados sin copiar ideas o ejecuciones.

Salidas: `COMPETIDORES.md`, `PERFORMER-DATA.csv` y `OPORTUNIDADES.md`.

## 4. Posicionamiento y arquitectura

Definir promesa, diferencia defendible, audiencia por necesidad/objeción/ocasión,
voz, lenguaje prohibido y claims que requieren verificación. Construir pilares de
alcance, autoridad, producto, prueba, comunidad y conversión; después una matriz
de seis temas por cinco formatos y su mapa de funnel.

Instagram y TikTok pueden compartir una hipótesis, pero la ejecución debe adaptarse
al comportamiento nativo de cada canal.

## 5. Sistema creativo por sprint

Cadencia inicial orientativa: 12 reels/shorts y 4 carruseles mensuales, más stories
frecuentes. Se ajusta a capacidad y datos, no a una cuota rígida.

Cada pieza debe tener:

- ID único, hipótesis y etapa del funnel.
- Entre 3 y 5 hooks candidatos creados con `hook-lab` o método equivalente.
- Hook verbal, visual y textual alineados.
- Guion UGC y framework de guion cuando el formato lo requiera.
- Storyboard, wireframe, assets, copy, thumbnail, CTA único y métrica primaria.
- Scorecard creativo aprobado antes de pasar a producción.

No repetir concepto, hook y estructura entre reels consecutivos.

## 6. Producción automatizable

`brief → guion → storyboard → assets → wireframe → HyperFrames → check → revisión → render → paquete de publicación`

Reglas:

- Mantener fuentes editables y originales sin sobrescribir.
- Crear manifiesto SHA-256 por lote.
- Dar tiempo de lectura humana aunque el motion sea dinámico.
- Usar gates humanos antes del render final y de la publicación.
- Ejecutar lint, validación y QA visual/técnico de HyperFrames.
- Guardar decisiones, aprendizajes y resultado por ID de contenido.

## 7. Publicación y distribución

Mantener un calendario con fecha, canal, objetivo, ID, copy, CTA y UTM. Publicar
mediante herramientas oficiales o plataformas autorizadas. Adaptar ritmo, caption,
search intent y conversación a cada canal. No automatizar respuestas sensibles,
precios variables o promesas sin reglas aprobadas.

## 8. Conversión en DM o WhatsApp

Preparar respuestas por intención, SLA, responsable y etiquetas de lead. Registrar
fuente y pieza de origen. Realizar follow-up con consentimiento y sin spam.

Estados sugeridos: nuevo, calificado, cotizado, pedido, perdido y recompra.

## 9. Publicidad pagada

1. Validar hooks y piezas orgánicamente.
2. Elegir ganadores por señales de negocio, no solo vistas.
3. Impulsar con segmentación local y CTA coherente.
4. No fragmentar presupuestos mínimos entre demasiadas variables.
5. Escalar solo cuando CAC, margen y capacidad lo permitan.
6. Iterar o retirar al superar umbrales de fatiga o costo.

## 10. Revisión semanal

Métricas de contenido: retención inicial, tiempo promedio, completado, compartidos,
guardados, comentarios con intención y visitas al perfil.

Métricas de negocio: clics, conversaciones, leads calificados, cierre, pedidos,
ingresos, margen atribuible, CAC, ROAS/MER, recompra y tiempo de respuesta.

Árbol de decisiones:

- Buen hook y mala conversión: revisar oferta, CTA y destino.
- Mala retención y buena conversión: conservar oferta y rehacer apertura.
- Buenas vistas y pocos leads: ajustar audiencia y promesa.
- Buenos leads y pocas ventas: mejorar el proceso comercial.
- Buen CAC y capacidad disponible: escalar gradualmente.

## 11. Ciclo 30/60/90

- Días 1–7: ingesta, economía, accesos, baseline y research.
- Días 8–14: posicionamiento, matriz, primer sprint y medición.
- Días 15–30: publicación orgánica, comunidad e iteración.
- Días 31–60: duplicar patrones ganadores y activar ads controlados.
- Días 61–90: escalar lo rentable, automatizar reportes y reforzar recompra.

## Estructura de proyecto

```text
projects/<cliente>/
  00-business/
  01-research/
  02-strategy/
  03-content-system/
  04-assets/source/
  04-assets/derived/
  05-production/
  06-publishing/
  07-analytics/
  08-ads/
  09-sales/
  10-reports/
  automations/
  manifests/
```

Automatizables: inventario, manifiestos, normalización de performer data, backlog,
briefs, render/QA, UTMs, importación de métricas y reporte semanal. Publicación,
inversión, claims y respuestas comerciales sensibles conservan aprobación humana.
