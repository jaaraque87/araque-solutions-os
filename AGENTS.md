# Araque Solutions OS - agent context

This repo is the shared source of truth for Codex, Claude Code, and any other coding agent.

## Mission

Build a portable AI video production system that can run from any PC, RunPod, VPS, Codex session, or Claude Code session.

The repo should contain code, docs, prompts, workflows, templates, and agent instructions. It must not contain secrets, local-only caches, rendered videos, model weights, or generated outputs.

## Main paths

- `README.md`: high-level system map.
- `docs/ejecutar-con-codex-o-claude.md`: how to run this repo from any machine/agent.
- `docs/sincronizacion-pcs.md`: sync workflow between PCs.
- `pipeline/`: Python production pipeline.
- `pipeline/comfydeploy_hyperframes/`: portable ComfyDeploy + HyperFrames pipeline.
- `workflows/`: ComfyUI workflow JSON files.
- `characters/`: character/influencer profiles.
- `memory/`: project memory and operating notes.
- `infrastructure/`: RunPod/ComfyUI setup scripts.

## Agent rules

1. Start every session with `git pull`.
2. Read this file, then read `README.md`, then the task-specific docs.
3. Never commit `.env`, API keys, passwords, tokens, generated videos, model weights, zips, caches, `node_modules`, `.venv`, or run outputs.
4. Use `.env.example` only as a template. Real secrets live in local `.env`, Bitwarden, environment variables, GitHub Secrets, RunPod secrets, or the user's password manager.
5. Prefer small commits with clear messages.
6. Before pushing, run `git status` and check for accidental secrets or large files.
7. If working on HyperFrames, remember HyperFrames 0.7.18 requires Node.js 22+.
8. If working on ComfyDeploy, keep API endpoint details configurable through `COMFYDEPLOY_RUN_URL`.

## Portable pipeline quick test

From repo root:

```powershell
cd .\pipeline\comfydeploy_hyperframes
python .\run.py --brief .\examples\brief.example.json --mock-assets --skip-render
```

This should work without spending credits.

## Real pipeline

Configure local secrets in `pipeline/.env`, then run:

```powershell
cd .\pipeline\comfydeploy_hyperframes
python .\run.py --brief .\examples\brief.example.json
```

## Handoff format

When handing work between Claude and Codex, leave a short note in `memory/` or the relevant docs:

- what changed
- what was tested
- what remains blocked
- which machine/environment was used

