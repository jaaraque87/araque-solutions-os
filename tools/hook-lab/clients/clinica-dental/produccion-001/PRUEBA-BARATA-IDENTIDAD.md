# PRUEBA BARATA — Fidelidad de identidad (antes de invertir en LoRA)
_Objetivo: saber si con adherencia alta a la referencia + seed fijo se elimina el drift de identidad entre escenas, SIN entrenar todavía el LoRA de Camila. 1 sesión L40S, 2-3 escenas cortas, ~$1, apagar al terminar._

## Diagnóstico que motiva esta prueba (2026-07-13)
Los 4 clips que rindió el dueño (render VIEJO, anterior a los fixes de `timeline_start` y prompts v2) mostraron:
- ✅ Técnica OK: 1024×1920, 24fps, audio por escena, stitching correcto.
- ✅ Movimiento VIVO (no estatua) — el problema del "robótico" no está aquí.
- ❌ **Drift de identidad**: cada escena parece una mujer distinta y se aleja de su propio still fuente. LTX I2V re-interpreta la cara en cada render. Para una vocera de marca = mata credibilidad.

Causa raíz probable (por orden de sospecha, leído del workflow `LTX2.3_ID_lora_API.json` + UI del Builder):
1. **Seed en `randomize`** → cada escena arranca de un ruido distinto → LTX empuja la cara en dirección distinta cada vez.
2. **Denoise alto en el pass de refinado** (`pass2 sigmas` arranca a 0.909 = 91% de regeneración).
3. **`img_compression=18`** en `LTXVPreprocess` (nodo 940) degrada la referencia antes de condicionar (no expuesto en la UI).

## Escena cobaya
`esc5` (CTA, 4.62s = la más corta = render más barato). Si sobra tiempo, también `esc4` (5.50s) para ver consistencia ENTRE dos escenas.

## Palancas — probar en orden (la más barata primero)

### Lever 1 — Fijar el seed (casi gratis, PRIMERO)
En los ajustes de render de video / I2V del Builder:
- **Seed mode = `fixed`** (NO `randomize`) y un seed constante, p.ej. `69`, para TODAS las escenas.
- Test: renderizar `esc4` + `esc5` con el mismo seed fijo.
- Lectura: si ahora las 2 caras se parecen ENTRE SÍ y al still → el seed aleatorio era el villano #1. Posible fix definitivo casi gratis.

### Lever 2 — Bajar el denoise del pass de refinado (si aún hay drift)
En I2V Video Settings, campo de sigmas del pass 2:
- Default: `0.909375, 0.725, 0.421875, 0.0`
- Cambiar a: `0.6, 0.45, 0.25, 0.0`  ← arranca a 60% en vez de 91% = se pega más al still
- (opcional, pass 1) default `1., 0.99375, 0.9875, 0.98125, 0.975, 0.909375, 0.725, 0.421875, 0.0` → probar recortando el arranque a `0.85, ...` sólo si el pass 2 no bastó.
- Test: re-render `esc5`, comparar contra el still fuente.

### Lever 3 — img_compression (técnico, sólo si 1+2 no bastan)
`LTXVPreprocess` nodo 940 `img_compression: 18 → 4`. NO está en la UI; requiere editar el template del workflow en la máquina (build step o edición del archivo en la sesión). Dejar para después.

## Cómo se evalúa
Mandar los 2-3 clips de prueba a Claude → hace el mosaico **fuente-vs-render** por escena (mismo método del 2026-07-13). Veredicto en ~5 min:
- Identidad ya fiel y consistente → **vendible sin LoRA**, seguimos con el kit corregido (timeline_start + prompts v2) y a producir.
- Sigue drift → **LoRA de Camila confirmado imprescindible** (dataset + ~2h L40S, ~6000 steps) y no gastamos más en tunear I2V.

## Reglas de gasto
Una sola sesión L40S, sólo estas 2-3 escenas cortas, Quick Save, descargar clips, **apagar L40S**. Presupuesto ~$15.

---

## ✅ RESULTADO (2026-07-13, sesión L40S, esc4+esc5 con seed 69 fixed)

**El Lever 1 (seed fijo) FUNCIONÓ — mejora dramática, sin tocar sigmas.**

| Métrica | Render viejo (seed random) | Render nuevo (seed 69 fixed) |
|---|---|---|
| Identidad vs still fuente | ❌ mujer distinta por escena | ✅ ~85-90% fiel (esc5 casi calcada) |
| Consistencia esc4 ↔ esc5 | ❌ dos mujeres diferentes | ✅ misma mujer, reconocible |
| Estabilidad dentro del clip | media | ✅ estable frame a frame |
| Duraciones | rotas (bug timeline_start) | ✅ exactas (5.50 / 4.62) |
| Movimiento | vivo | ✅ vivo + gestos del prompt v2 (palma, señalar) |

Residual (menor): en esc4 la actuación exagera algo la expresión en picos (cara ligeramente más joven/caricaturizada en 1-2 frames). En movimiento a velocidad real es poco perceptible.

**Decisión**: pipeline VENDIBLE sin LoRA para producción normal. Regla nueva de producción: **seed FIJO (69) en todos los renders de una misma vocera/serie** — el orquestador ya lo inyecta en `i2v_video_settings` al montar. El LoRA de personaje queda como upgrade de "premium consistency" (misma cara entre VIDEOS distintos y ángulos extremos), no como bloqueante.

Lever 2 (sigmas pass2 0.909→0.6): NO fue necesario. Guardado como perilla de refinado si algún cliente exige fidelidad extra.
