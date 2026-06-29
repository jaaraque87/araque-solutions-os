# Contexto compartido entre Codex y Claude

Problema: cada PC, Codex y Claude puede tener memoria separada. Eso retrasa el trabajo porque el agente no sabe que ya existe una decision, skill, pipeline o configuracion en otra maquina.

Solucion: usar este repo como centro de mando compartido.

## Capas de sincronizacion

1. `AGENTS.md`: instrucciones comunes para cualquier agente.
2. `CLAUDE.md`: entrada especifica para Claude Code.
3. `docs/`: guias de operacion.
4. `memory/`: memoria viva de decisiones, clientes, personajes y pipelines.
5. `pipeline/`: codigo ejecutable.
6. GitHub: sincronizacion entre PCs.
7. Bitwarden o gestor similar: secretos y claves.

## Como integrar skills de Claude del otro PC

No se debe "conectar el Claude de alla" como si fuera una memoria remota directa. Lo mas robusto es extraer lo reutilizable:

- nombre del skill
- para que sirve
- instrucciones principales
- scripts o plantillas que usa
- variables de entorno necesarias
- ejemplos de uso

Y guardarlo en este repo, idealmente en:

```text
skills-backup/claude/<skill-name>/
```

O, si es parte central del sistema:

```text
docs/skills/<skill-name>.md
pipeline/<feature>/
```

No copiar:

- tokens
- `.env`
- caches
- historiales privados completos
- archivos enormes generados
- rutas absolutas que solo existen en el otro PC

## Flujo recomendado desde el otro PC por AnyDesk

En el otro PC:

```powershell
cd RUTA_DEL_PROYECTO_O_SKILLS
git status
Get-ChildItem -Force
```

Si son skills de Claude, buscar carpetas tipo:

```powershell
Get-ChildItem -Force $env:USERPROFILE\.claude -ErrorAction SilentlyContinue
Get-ChildItem -Force $env:USERPROFILE\.claude\skills -ErrorAction SilentlyContinue
```

Luego copiar solo los skills reutilizables al repo, revisar secretos, hacer commit y push.

## Prompt para cualquier agente nuevo

```text
Estas trabajando en araque-solutions-os. Lee AGENTS.md, CLAUDE.md, README.md y docs/ejecutar-con-codex-o-claude.md. Usa este repo como fuente central de contexto. No subas secretos ni archivos pesados. Antes de cambiar algo, ejecuta git pull. Al terminar, deja commit y una nota corta de handoff.
```

