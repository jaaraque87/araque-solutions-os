---
name: performance-optimization
title: "Performance Optimization"
category: Frontend-engineer
users: 14
source: https://higgsfield.ai/supercomputer/marketplace/skills/374fea25-b533-1ae9-8723-c6f23b063ee6
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): performance-checklist.md
---

# Performance Optimization
**Medir antes de optimizar.** Trabajo de performance sin medición = adivinar. NO optimizar antes de tener evidencia (la optimización prematura agrega complejidad).

## Core Web Vitals Targets
| Métrica | Good | Needs Improvement | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | ≤2.5s | ≤4.0s | >4.0s |
| INP (Interaction to Next Paint) | ≤200ms | ≤500ms | >500ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | ≤0.25 | >0.25 |

## Workflow
1. **MEASURE** — baseline con data real. 2. **IDENTIFY** — el bottleneck real (no asumido). 3. **FIX** — el bottleneck específico. 4. **VERIFY** — medir de nuevo, confirmar mejora. 5. **GUARD** — monitoring/tests contra regresión.

## Step 1: Measure (usar ambos)
- **Synthetic** (Lighthouse, DevTools Performance, Chrome DevTools MCP): condiciones controladas, reproducible, bueno para CI.
- **RUM** (web-vitals library `onLCP/onINP/onCLS`, CrUX): data de usuarios reales, requerido para validar que un fix mejoró de verdad.
- Backend: response time logging, APM, DB query log con timing (`console.time`).

## Where to start (por síntoma)
First page load → bundle grande (medir bundle, code splitting) / server lento (TTFB en Network waterfall → DNS: dns-prefetch/preconnect; TCP/TLS: HTTP/2, edge; server waiting: profile backend/queries/cache) / render-blocking resources. Interaction sluggish → UI freeze (main thread, long tasks >50ms) / input lag (re-renders) / animation jank (layout thrashing). Backend → single endpoint (queries, indexes) / all endpoints (pool, memory, CPU) / intermitente (locks, GC, deps externas).

## Step 3: Anti-patterns → Fix
- **N+1 queries:** en vez de un query por item, usar single query con `include`/join.
- **Unbounded fetching:** paginar (`take`, `skip`, `orderBy`) en vez de `findMany()` todo.
- **Image optimization:** `<picture>` con art direction (media) + resolution switching (srcset+sizes), AVIF/WebP, `width`/`height` siempre, `fetchpriority="high"` para LCP/hero, `loading="lazy"` + `decoding="async"` para below-the-fold.
- **Re-renders (React):** referencias estables (constante fuera del componente en vez de objeto inline), `React.memo` para componentes caros, `useMemo` para cómputos caros.
- **Bundle grande:** bundlers modernos tree-shakean named imports (si ESM + `sideEffects:false`); las ganancias reales vienen de `lazy()` + code splitting a nivel de ruta con `<Suspense>`.
- **Missing caching (backend):** cache en memoria con TTL para data frecuente/estable; HTTP `Cache-Control` (`max-age`, `immutable` para assets con content-hash).

## Performance Budget (enforcer en CI)
JS bundle <200KB gzip (initial) · CSS <50KB gzip · imágenes <200KB (above the fold) · fonts <100KB total · API <200ms (p95) · TTI <3.5s en 4G · Lighthouse ≥90. CI: `npx bundlesize`, `npx lhci autorun`.

## Common Rationalizations (realidad)
"optimizamos después" → la deuda compone, arreglar anti-patterns obvios ya · "es rápido en mi máquina" → no es la del usuario, profile en hardware/redes representativos · "esta optimización es obvia" → si no mediste, no sabés · "100ms no se nota" → afecta conversión · "el framework maneja la performance" → no arregla N+1 ni bundles gigantes.

## Red Flags
Optimización sin data de profiling · N+1 · list endpoints sin paginación · imágenes sin dimensiones/lazy/responsive · bundle creciendo sin review · sin monitoring en producción · `React.memo`/`useMemo` en todos lados (sobre-usar es tan malo como sub-usar).

## Verification
Mediciones antes/después (números específicos) · bottleneck identificado y atacado · CWV en "Good" · bundle no creció · sin N+1 nuevos · budget pasa en CI · tests siguen pasando.
