# HANDOFF — Debug del V9 Video Builder (Claude → Codex, 2026-07-10)

**Objetivo:** hacer que el Music Video Builder UI (pack `comfyui-vrgamedevgirl`) renderice escenas en ComfyDeploy. Hoy TODO el pipeline previo funciona (proyecto, escenas, audios, imágenes, prompts) pero **Render All crashea siempre en el mismo nodo**. Este doc contiene todo lo diagnosticado para no repetir trabajo.

## 1. Contexto de infraestructura

- **Máquina:** "LTX TODO EN UNO's Machine", id `385499ef-14be-4a75-9ab5-4617913e9e4d`, org `araquesolutions` (app.comfydeploy.com)
- **Versión activa: v30** (`68939b19`, ready 2026-07-09 ~05:30 UTC) = pack vrgamedevgirl en commit **`4cfc7883ac8146d5f8a3f8f861c4b8400ace80c9`** (head de `dev/music-video-builder-ui-test-v9`)
- ⚠ El banner de arranque dice `v9-dev-2026-07-04` EN AMBOS commits — está **hardcodeado en `__init__.py`** (`__version__`), NO sirve para saber qué versión corre
- ComfyUI **0.23.0**, torch 2.12+cu130, sesiones L40S
- Proyecto del Builder ya montado: `/comfyui/output/MARAVILLAS7/` (9 escenas, audios por escena, imágenes, i2v_prompts, ConceptPrompts/I2VMotionNotes/subject/theme/story rellenos)
- El Builder se abre agregando su nodo en un workflow y lanzando su UI (el usuario lo ha usado desde el workspace de ComfyDeploy)

## 2. EL BUG (reproducible al 100%)

Al dar **Render All** (o render de una escena), el scene-video workflow corre hasta ~35% (VRAMCleanup→VAELoader→LoadAudioSplit ✓ con splits perfectos) y muere en:

```
Node 755 VRGDG_ShowText — AttributeError: 'NoneType' object has no attribute 'get'
File "custom_nodes/comfyui-vrgamedevgirl/VRGDG_GeneralNodes2.py", line 1451, in notify
    (x for x in workflow.get("nodes", []) if str(x.get("id")) == str(unique_id[0])),
```

**Código exacto (idéntico en d6dde1fd y 4cfc788 — verificado contra raw.githubusercontent):**
```python
if unique_id is not None and extra_pnginfo is not None:
    if not isinstance(extra_pnginfo, list):
        print(...)
    elif not isinstance(extra_pnginfo[0], dict) or "workflow" not in extra_pnginfo[0]:
        print(...)
    else:
        workflow = extra_pnginfo[0]["workflow"]   # <-- la clave EXISTE pero su VALOR es None
        node = next((x for x in workflow.get("nodes", []) ...
```
El guard revisa que la clave "workflow" exista pero NO que su valor no sea null → `None.get` crashea. Es un nodo de puro display: mata el render por una cosmética.

**Evidencia adicional decisiva:** el propio core de ComfyUI 0.23 crashea igual en cada poll de `/api/jobs`:
```
File "/comfyui/comfy_execution/jobs.py", line 104, in _extract_job_metadata
    workflow_id = extra_pnginfo.get('workflow', {}).get('id')
AttributeError: 'NoneType' object has no attribute 'get'
```
→ los prompts que el Builder somete llegan con `extra_data.extra_pnginfo` roto/null. El problema es **cómo se somete el prompt**, no el proyecto del usuario.

## 3. Qué se probó y queda DESCARTADO (no repetir)

| Intento | Resultado |
|---|---|
| Desmarcar "Use VRGDG text context files" | Crash idéntico |
| Rellenar ConceptPrompts.txt, I2VMotionNotes.txt, subject/theme/story text files | Crash idéntico (igual déjenlos rellenos: otros pasos los usan) |
| Actualizar pack d6dde1fd → 4cfc788 (rebuild v30, hecho vía PATCH API) | Crash idéntico — el código de `notify` no cambió entre commits |
| Revisar proyecto (escenas/audios/timing) | Perfecto — los logs de LoadAudioSplit muestran cortes exactos |

## 4. Hipótesis principal (SIN confirmar aún)

El **workspace de ComfyDeploy** (iframe que envuelve ComfyUI) no serializa el grafo del canvas → cuando el JS del Builder llama queuePrompt, `extra_pnginfo.workflow` va como `null`. El creador desarrolla sobre ComfyUI vanilla, donde `app.graph` siempre serializa bien → por eso a ella nunca le pasa.

## 5. PLAN DE ATAQUE (en orden — ejecutar y documentar resultado aquí)

**Test A — Tunnel URL (NO ejecutado todavía, 5 min, $0):**
1. Con sesión corriendo: `GET https://app.comfydeploy.com/api/sessions` (fetch same-origin desde cualquier página liviana de la app, con cookies) → campo `tunnel_url`
2. Abrir el tunnel_url en una pestaña → ComfyUI VANILLA de la misma sesión
3. Doble clic en canvas → agregar nodo del Builder → abrir UI → Load Project `MARAVILLAS7` → verificar Video Type "Speaking (short film)" y escenas → Quick Save → Render All
4. **Si renderiza:** workaround permanente = "Builder SIEMPRE por tunnel, nunca por workspace". Documentar y cerrar.

**Test B — si A falla igual:** el null lo produce el propio JS del Builder. Inspeccionar en el repo del pack (rama v9) cómo arma la submission: buscar `queuePrompt`, `extra_pnginfo`, `api.queuePrompt` en los .js del pack (carpeta `web/` o similar). Confirmar si manda `workflow: null` por diseño cuando somete workflows internos (los JSON de escena que no están en el canvas).

**Test C — Parche quirúrgico (FUNCIONA CON A O B; pendiente del "sí" del dueño):**
Agregar un step tipo `commands` en el build de la máquina, inmediatamente DESPUÉS del step del pack (índice ~51 de 60):
```
find /comfyui/custom_nodes/comfyui-vrgamedevgirl -name "*.py" -exec sed -i 's/workflow = extra_pnginfo\[0\]\["workflow"\]/workflow = extra_pnginfo[0].get("workflow") or {"nodes": []}/g' {} + && echo PATCH-755-APPLIED
```
- Se hace vía `PATCH /api/machine/serverless/385499ef-...` con `docker_command_steps` completo modificado (el endpoint acepta parcial y dispara rebuild)
- ⚠ La página de detalle de máquina CONGELA Chrome — usar fetch same-origin desde página liviana (receta completa en `memory/comfydeploy-mvc-vrgdg.md`)
- Reversible (quitar el step). El `echo` permite verificar en el build log
- NOTA: el core `jobs.py` seguiría tirando errores en el endpoint /api/jobs (solo ruido de API de historial, no mata renders)

**Test D — reporte al creador (paralelo, cualquiera puede postearlo en su Discord):**
> Found a crash in VRGDG_ShowText (VRGDG_GeneralNodes2.py ~line 1451, both d6dde1fd and 4cfc788): when the prompt is submitted with `extra_pnginfo[0]["workflow"] = null` (happens when the Builder runs inside ComfyDeploy's wrapped workspace), the guard passes because the key exists, but `workflow.get("nodes")` crashes on None and kills the whole scene render. Suggested fix: `workflow = extra_pnginfo[0].get("workflow") or {"nodes": []}`. Same null also breaks ComfyUI 0.23's /api/jobs (`jobs.py _extract_job_metadata`).

## 6. Reglas operativas (no romper)

- Presupuesto: ~$15 restantes en ComfyDeploy — sesiones L40S solo cuando haya algo que ejecutar; apagar al terminar
- Quick Save religioso + **descargar/respaldar `/comfyui/output/MARAVILLAS7` antes de cerrar sesión** (persistencia entre sesiones aún no confirmada)
- NO gastar API/créditos sin OK explícito del dueño
- Todo hallazgo se documenta AQUÍ y se commitea (repo = cerebro compartido)

## 7. Referencias en este repo

- `docs/vrgdg/BUILDER-UI-GUIA.md` — mapa completo de la UI + SOP + historia del bug
- `docs/vrgdg/local-*.md` — 5 demos del creador analizados (receta MSR, ID-LoRA/voz, Beat Mode, LLM instructions, FlowGPT)
- `docs/vrgdg/BUILDER-UI-PLAN.md` — plan original
- `memory/comfydeploy-mvc-vrgdg.md` — máquina, API interna, trucos, lecciones de pack updates
- Contexto de negocio: el reel "7 Maravillas" YA se entregó por la vía TAO Director V2 manual — el Builder es para AUTOMATIZAR los siguientes, no urgencia de hoy
