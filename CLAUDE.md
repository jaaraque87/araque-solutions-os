# Claude context

Read `AGENTS.md` first. This file exists so Claude Code lands on the same operating context as Codex.

## Default behavior

- Treat this repo as the shared production brain for Araque Solutions OS.
- Keep portable execution in mind: no machine-specific absolute paths unless documented as examples.
- Use `docs/ejecutar-con-codex-o-claude.md` when setting up a new machine or agent session.
- For ComfyDeploy + HyperFrames work, start in `pipeline/comfydeploy_hyperframes/`.
- For project memory, read `memory/MEMORY.md` and the relevant `memory/project_*.md` file.

## Important boundaries

- Do not commit secrets.
- Do not commit generated videos, rendered outputs, zips, model files, or dependency folders.
- If a local Claude skill exists on another PC, document its purpose and copy only the reusable skill source/instructions into this repo or into a dedicated skills backup folder. Do not copy private credentials or machine-local cache files.

## Useful command

```powershell
git pull
cd .\pipeline\comfydeploy_hyperframes
python .\run.py --brief .\examples\brief.example.json --mock-assets --skip-render
```

