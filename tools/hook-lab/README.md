# Hook Lab — research y hooks por cliente

Activo editorial de Araque Solutions. La skill que lo opera vive en `.claude/skills/hook-lab/SKILL.md` (con la librería de 14 patrones en `references/hook-frameworks.md`).

## Estructura

```
tools/hook-lab/
└── clients/
    └── <cliente>/
        ├── intake.md    → quién es, qué vende, a quién, objeción principal
        ├── swipe.md     → research acumulado del nicho (nunca se borra)
        └── hooks.json   → baterías puntuadas; los seleccionados van a producción
```

## Flujo

1. Nuevo cliente → llenar `intake.md` (la skill pregunta lo que falte).
2. Research del nicho → `swipe.md`.
3. Batería de 10+ hooks puntuados → `hooks.json`.
4. Los top se convierten en jobs de `tools/content-reel-lab/scripts/render-batch.mjs`.

Los `hooks.json` y `swipe.md` de clientes SÍ se comitean: son el activo diferencial de la agencia. Lo que nunca se comitea: material privado del cliente (accesos, métricas internas, contratos).
