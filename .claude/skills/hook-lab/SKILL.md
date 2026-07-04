---
name: hook-lab
description: "Research de nicho + generación de hooks que detienen el scroll para IG Reels y TikTok. Funciona para cualquier rubro de cliente: investiga el nicho, extrae patrones ganadores, genera baterías de 10+ hooks puntuados y los exporta como jobs listos para render-batch. Usar cuando se pida: hooks, research de nicho, análisis de competencia en short-form, batería de hooks, contenido que convierta, o preparar producción para un cliente nuevo."
---

# HOOK-LAB — Research de nicho + hooks que detienen el scroll

El diferenciador de Araque Solutions: antes de producir un solo video, se investiga el nicho y se generan hooks con método — no con suerte. El objetivo de cada hook es ganar los primeros 1.5 segundos y convertir viewers en leads/ventas para el cliente, sea cual sea su rubro.

Complementa (no reemplaza) a `/script-framework` (lente editorial) y `/guion-ugc` (estructura del guion). Hook-lab decide **QUÉ ángulos atacan el nicho**; las otras dos escriben el resto.

## Flujo completo

```
intake cliente → research nicho → swipe file → batería 10+ hooks → scoring → top 3 → jobs para render-batch
```

## FASE 1 — Intake (obligatorio antes de investigar)

Definir en `tools/hook-lab/clients/<cliente>/intake.md`:

- **cliente** — nombre y rubro concreto (no "salud", sino "clínica dental en Bogotá").
- **oferta** — qué vende exactamente y a qué precio aproximado.
- **avatar_comprador** — quién compra, qué le duele, qué desea, qué ya intentó.
- **objeción_principal** — la razón #1 por la que NO compran hoy.
- **plataformas** — IG Reels, TikTok, o ambas (afecta tono y formato).
- **prueba_disponible** — testimonios, números, antes/después que se puedan mostrar.

Si el usuario no da estos datos, preguntar SOLO los que falten. Sin intake no hay research.

## FASE 2 — Research del nicho

Con acceso a web (WebSearch/WebFetch disponibles):

1. Buscar los formatos short-form que están funcionando en el nicho: `"<rubro> tiktok viral"`, `"<rubro> hooks"`, `"<rubro> before after reel"`, términos del dolor del avatar.
2. Identificar 5-10 piezas de referencia y extraer de cada una: primera línea hablada, qué se ve en el frame 1, el patrón de hook usado, y por qué retiene.
3. Detectar el **ángulo saturado** (lo que todos hacen) — se anota para EVITARLO o invertirlo.

Sin acceso a web: usar la librería de patrones de `references/hook-frameworks.md` + conocimiento del nicho, y marcarlo en el swipe file como `research: offline`.

Guardar todo en `tools/hook-lab/clients/<cliente>/swipe.md`. El swipe file es acumulativo: cada sesión de research agrega, nunca borra. Es un activo del cliente.

## FASE 3 — Batería de hooks

Generar **mínimo 10 hooks** por batería usando `references/hook-frameworks.md`. Reglas duras:

- Cada hook usa un patrón distinto (mínimo 6 patrones diferentes por batería).
- Cada hook declara: línea hablada (≤ 15 palabras), overlay de texto (≤ 8 palabras), visual del frame 1, patrón usado, ángulo.
- La línea debe entenderse SIN contexto y plantar UNA sola pregunta.
- Nada de "Hola, hoy les voy a mostrar" — entrar en movimiento o en tensión.
- Al menos 2 hooks deben invertir el ángulo saturado del nicho.
- Idioma y registro del avatar comprador (no de la marca).

## FASE 4 — Scoring (rúbrica 0-2 por criterio, máx 10)

| Criterio | 0 | 2 |
|---|---|---|
| Claridad en 1.5s | necesita contexto | se entiende al instante |
| Curiosity gap | no abre pregunta | pregunta irresistible |
| Especificidad | genérico | números/detalles concretos |
| Contraste | plano | tensión "pero/en realidad" |
| Nativo | huele a anuncio | parece contenido orgánico |

Los **top 3** pasan a producción. Puntuar honesto: una batería donde todo saca 9-10 es una batería mal puntuada.

## FASE 5 — Export a producción

Escribir `tools/hook-lab/clients/<cliente>/hooks.json`:

```json
{
  "cliente": "nombre",
  "fecha": "YYYY-MM-DD",
  "research": "web | offline",
  "hooks": [
    {
      "id": "h01",
      "linea": "texto hablado del hook",
      "overlay": "texto en pantalla ≤8 palabras",
      "visual_frame1": "qué se ve en el primer frame",
      "patron": "nombre del patrón",
      "angulo": "dolor | deseo | contrarian | prueba | ...",
      "score": 8,
      "seleccionado": true
    }
  ]
}
```

Los hooks seleccionados alimentan directo el batch de render:

```json
{ "video": "clip.mp4", "hook": "<overlay>", "cta": "<cta del cliente>", "handle": "@cliente" }
```

(formato de `tools/content-reel-lab/scripts/render-batch.mjs`)

## Regla de oro

Un hook que no se puede explicar en una frase ("detiene porque ___") no entra a la batería. Y ningún gasto de API de generación (TTS, video) sin autorización explícita del dueño.
