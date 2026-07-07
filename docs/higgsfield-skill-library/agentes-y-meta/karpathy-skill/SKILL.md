---
name: karpathy-skill
title: "Karpathy Skill"
author: kion
category: Content Creation
users: 11
source: https://higgsfield.ai/supercomputer/marketplace/skills/d2d0ccc7-966f-4280-aa76-de6885d00c7c
extracted: modal SKILL.md (via claude-in-chrome) — single file
relevante: guidelines de coding para agentes (mergear con CLAUDE.md del proyecto)
---

# Karpathy Coding Skill (CLAUDE.md behavioral guidelines)
Guidelines de comportamiento para reducir errores comunes de coding de LLMs. Mergear con instrucciones específicas del proyecto. Tradeoff: sesga hacia cautela sobre velocidad (para tareas triviales, usar juicio).

## 1. Think Before Coding
No asumir. No ocultar confusión. Surfacear tradeoffs. Antes de implementar: declarar assumptions explícitas (si hay incertidumbre, preguntar) · si hay múltiples interpretaciones, presentarlas (no elegir en silencio) · si existe un approach más simple, decirlo (push back cuando corresponde) · si algo no está claro, PARAR, nombrar lo confuso, preguntar.

## 2. Simplicity First
Código mínimo que resuelve el problema. Nada especulativo. Sin features más allá de lo pedido · sin abstracciones para código de un solo uso · sin "flexibility"/"configurability" no pedida · sin error handling para escenarios imposibles · si escribís 200 líneas y podrían ser 50, reescribir. Preguntarse: "¿un senior diría que esto está sobre-complicado?" Si sí, simplificar.

## 3. Surgical Changes
Tocar solo lo necesario. Limpiar solo tu propio desorden. Al editar código existente: no "mejorar" código/comentarios/formato adyacente · no refactorizar lo que no está roto · matchear el estilo existente (aunque lo harías distinto) · si notás dead code no relacionado, mencionarlo (no borrarlo). Al crear orphans: remover imports/variables/funciones que TUS cambios dejaron sin uso; no remover dead code preexistente salvo que lo pidan. **Test:** cada línea cambiada debe trazar directo al request del usuario.

## 4. Goal-Driven Execution
Definir criterios de éxito. Loopear hasta verificar. Transformar tasks en goals verificables: "Add validation" → "Write tests for invalid inputs, then make them pass" · "Fix the bug" → "Write a test that reproduces it, then make it pass" · "Refactor X" → "Ensure tests pass before and after". Para multi-step, declarar plan breve (`1. [Step] → verify: [check]`). Criterios fuertes permiten loopear independiente; débiles ("make it work") requieren check-ins constantes.

**Funcionan si:** menos cambios innecesarios en diffs, menos rewrites por sobre-complicación, y preguntas clarificadoras cuando corresponde.
