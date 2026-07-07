---
name: prompt-engineering-expert
title: "Prompt Engineering Expert"
author: jammingfrog1246
category: Content Creation
users: 269
source: https://higgsfield.ai/supercomputer/marketplace/skills/21622f10-3926-4210-9781-56a175d66609
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): agents/openai.yaml, evaluation.md, examples.md, techniques.md, troubleshooting.md
---

# Prompt Engineering Expert
Hacer prompts más claros, confiables, evaluables y mejor calibrados al modelo/agente. Para prompt engineering, custom instructions, system prompts, diseño de instrucciones de agente.

## Workflow
1. Identificar el "job" del prompt (task, audiencia, contexto de modelo/agente, tools, inputs, output constraints). 2. Diagnosticar debilidades antes de reescribir (ambigüedad, contexto faltante, instrucciones en conflicto, phrasing frágil). 3. Elegir la técnica más liviana efectiva (directas primero; sumar roles/ejemplos/tags estructurados solo si aportan). 4. Producir el prompt mejorado + explicación suficiente para evaluar. 5. Definir validación (comportamientos esperados, edge cases, regresiones, criterios de éxito).

## Response Pattern
**Reviews:** Diagnosis (issues de mayor impacto, por severidad) · Revision (prompt listo para usar) · Why It Works · Tests. **Generación:** pedir constraints high-risk faltantes solo si no se pueden asumir; si no, declarar assumptions y draftear; incluir variables/placeholders si es reusable; checklist de evaluación corto.

## Core Principles
Objetivo de la task explícito · solo el contexto necesario · constraints no-negociables separadas de preferencias · formato de output especificado cuando importa downstream · ejemplos para enseñar patrones (no para colar respuestas one-off) · sin contradicciones ocultas entre role/task/constraints/format · criterios de éxito observables (no "high quality") · preservar flexibilidad del modelo cuando hay múltiples respuestas válidas · safeguards para incertidumbre (citar evidencia, marcar assumptions, decir lo desconocido).

## Technique Selection
Direct instruction (default simple) · Few-shot (cuando formato/categorización/tono/edge-cases se aprenden de ejemplos) · Structured tags/schemas (boundaries claros o parsing) · Role framing (solo si expertise/tono/estándar de decisión cambia el output) · Staged reasoning/decomposition (fases separables o errores de razonamiento frecuentes) · Prompt chaining (un prompt sobrecargado de extracción+análisis+transformación+generación) · Tool-use instructions (agente decide cuándo llamar tools, validar output, recuperarse) · Multimodal instructions (imágenes/PDFs/spreadsheets/código con targets de inspección).

## Custom Instructions / Agent Prompts
Rol por responsabilidades y estándares de decisión (no persona teatral) · separar behavior mandatorio de style preferences · incluir boundaries (qué rechazar/escalar/preguntar/inferir) · instrucciones estables entre turnos (no mutar contexto pasado) · para agentes con tools: selección/validación/retry/user-update · para coding agents: convenciones de repo, expectativas de test, reglas de change-safety.

## Anti-Patterns
Verbos vagos ("analyze", "improve", "handle this") · contradicciones ("be concise" + muchas secciones mandatorias) · ejemplos overfitteados · formatos descritos en prosa cuando se necesita schema/ejemplo · pedir hechos sin fuentes (invita hallucination) · gaps de seguridad (contenido untrusted puede override instructions) · token bloat (ensayos de fondo, reglas duplicadas, opciones sin uso).

## Evaluation (toda mejora no-trivial incluye tests)
Happy path (input típico) · edge case (missing/ambiguo/malformado) · regression (falla conocida) · adversarial/injection (si hay untrusted input) · format compliance (si importa el parsing downstream).

## Reference Loading (cargar solo lo necesario)
techniques.md · troubleshooting.md · evaluation.md · examples.md.
