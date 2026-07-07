---
name: frontend-ui-engineering
title: "Frontend UI Engineering"
category: Frontend-engineer
users: 199
source: https://higgsfield.ai/supercomputer/marketplace/skills/8a1bbf41-6bdb-20cb-53f8-618867fac1b7
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): accessibility-checklist.md
relevante: alto — construir UIs de producción (React/TS), evitar el "AI look"
---

# Frontend UI Engineering
Construir UIs de producción: accesibles, performantes, pulidas. Usar al construir/modificar interfaces, layouts responsive, interactividad, o arreglar UX.

## Component Architecture
- **File structure (colocar todo por componente):** `TaskList/{TaskList.tsx, TaskList.test.tsx, TaskList.stories.tsx, use-task-list.ts, types.ts}`.
- **Composición sobre configuración:** `<Card><CardHeader><CardTitle>...</CardTitle></CardHeader><CardBody><TaskList/></CardBody></Card>` en vez de `<Card title=... headerVariant=... content=.../>`.
- **Componentes enfocados:** cada uno hace una cosa.
- **Separar data fetching de presentación:** Container (maneja data: loading/error/empty via hook) vs Presentation (solo render).

## State Management (elegir lo más simple que funcione)
Local (useState) → UI state del componente · Lifted → compartido entre 2-3 hermanos · Context → theme/auth/locale (read-heavy, write-rare) · URL state (searchParams) → filtros/paginación/UI compartible · Server state (React Query/SWR) → data remota con cache · Global store (Zustand/Redux) → client state complejo app-wide. **Evitar prop drilling >3 niveles.**

## Avoid the AI Aesthetic (tabla clave)
| AI Default | Problema | Producción |
|---|---|---|
| Purple/indigo everything | paletas "safe", todo idéntico | paleta real del proyecto |
| Excessive gradients | ruido visual | flat o gradientes sutiles del design system |
| Rounded everything (rounded-2xl) | ignora jerarquía de radios | border-radius consistente del sistema |
| Generic hero sections | template sin conexión al contenido | content-first layouts |
| Lorem ipsum | oculta problemas de layout real | contenido placeholder realista |
| Oversized padding everywhere | destruye jerarquía visual | spacing scale consistente |
| Stock card grids | ignora prioridad de info | purpose-driven layouts |
| Shadow-heavy | compite con contenido, lento | sombras sutiles/none salvo que el sistema lo pida |

## Spacing/Typography/Color
- **Spacing:** usar la escala (incrementos 0.25rem); no inventar valores (`padding:13px` mal).
- **Typography:** respetar jerarquía h1(uno/página)→h2→h3→body→small; no saltar niveles.
- **Color:** tokens semánticos (`text-primary`, `bg-surface`, `border-default`) no hex crudos; contraste 4.5:1 (normal), 3:1 (large); no depender solo del color (usar iconos/texto).

## Accessibility (WCAG 2.1 AA)
- **Keyboard:** todo interactivo accesible por teclado; preferir `<button>` sobre `<div onClick>` (si div, agregar role/tabIndex/onKeyDown Enter+Space).
- **ARIA labels:** `aria-label` en botones sin texto visible; `<label htmlFor>` en inputs.
- **Focus management:** mover foco al cambiar contenido (dialog → focus al close button, trap focus).
- **Empty/error states:** nunca pantallas en blanco (icono + mensaje + CTA con `role="status"`).

## Responsive (mobile-first)
`grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`. Testear en 320px, 768px, 1024px, 1440px.

## Loading & Transitions
Skeletons (no spinners para contenido) con `aria-busy`/`aria-label`. Optimistic updates (React Query onMutate → cancelQueries → setQueryData → rollback onError).

## Common Rationalizations (realidad)
"A11y es nice-to-have" → requisito legal + calidad · "responsive después" → retrofitting es 3x más difícil · "diseño no final, salto el estilo" → usar defaults del sistema · "es solo prototipo" → los prototipos se vuelven producción · "el AI look está bien por ahora" → señala baja calidad.

## Red Flags
Componentes >200 líneas · inline styles/valores px arbitrarios · sin error/loading/empty states · sin test de teclado · color como único indicador de estado · "AI look".

## Verification (checklist)
Renderiza sin errores de consola · todo interactivo por teclado (Tab) · screen reader transmite estructura · responsive 320/768/1024/1440 · loading+error+empty manejados · sigue el design system · sin warnings de axe-core.
