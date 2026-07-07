---
name: vercel-composition-patterns
title: "Vercel Composition Patterns"
author: vercel
license: MIT
version: 1.0.0
category: Frontend-engineer
users: 7
source: https://higgsfield.ai/supercomputer/marketplace/skills/c0e090d5-ef25-39b6-68e4-3a25fb009a02
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): rules/*.md (por regla) + AGENTS.md (guía compilada completa)
---

# React Composition Patterns
Patrones de composición para componentes React flexibles y mantenibles. Evitar boolean prop proliferation, favorecer composición sobre configuración.

## When to Apply
Refactorizar componentes con muchos boolean props · construir librerías de componentes reusables · diseñar APIs de componentes flexibles · revisar arquitectura de componentes · trabajar con compound components o context providers.

## Rule Categories by Priority
| Prioridad | Categoría | Prefijo |
|---|---|---|
| HIGH | Component Architecture | `architecture-` |
| MEDIUM | State Management | `state-` |
| MEDIUM | Implementation Patterns | `patterns-` |
| MEDIUM | React 19 APIs | `react19-` |

## Quick Reference
**1. Component Architecture (HIGH)**
- `architecture-avoid-boolean-props` — no agregar boolean props para customizar comportamiento; usar composición.
- `architecture-compound-components` — estructurar componentes complejos con shared context.

**2. State Management (MEDIUM)**
- `state-decouple-implementation` — el Provider es el único que sabe cómo se maneja el estado.
- `state-context-interface` — definir interfaz genérica con state, actions, meta (dependency injection).
- `state-lift-state` — mover estado a provider components para acceso entre hermanos.

**3. Implementation Patterns (MEDIUM)**
- `patterns-explicit-variants` — crear componentes de variante explícitos en vez de boolean modes.
- `patterns-children-over-render-props` — usar children para composición en vez de props `renderX`.

**4. React 19 APIs (MEDIUM, solo React 19+)**
- `react19-no-forwardref` — no usar `forwardRef`; usar `use()` en vez de `useContext()`.

## How to Use
Cada `rules/<name>.md` contiene: por qué importa · ejemplo incorrecto con explicación · ejemplo correcto con explicación · contexto/referencias. La guía compilada completa está en `AGENTS.md`.
