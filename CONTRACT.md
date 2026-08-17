# OUTPUT CONTRACT

> **Single source of truth** for where files are written. If a `SKILL.md`, `contract.json`, or memory says otherwise, this file wins.

The repository ships with the `avatar` and `realistic_ugc` flows. Extend this contract and the validator when adding another flow.

## The 3 critical rules

1. Every deliverable lives in `outputs/<flow>/<run_slug>/`; never in the repo root or `brands/`.
2. `run_slug` is `<kebab-description>-<YYYYMMDD-HHMMSS>`.
3. Probes and experiments go in `scratch/`; regenerable run intermediates go in `<run>/tmp/`.

## Flow map

```text
outputs/
├── avatar/<run_slug>/     # avatar_reel
└── ugc/<run_slug>/        # realistic_ugc and gated UGC production
```

Every run requires `run.json` and `logs/events.ndjson`. Its canonical deliverable is `final.mp4`.

### Avatar run

```text
outputs/avatar/my-reel-20260101-143000/
├── run.json
├── logs/events.ndjson
├── final.mp4
├── source_assets/
└── tmp/
```

### Realistic UGC run

```text
outputs/ugc/my-product-ugc-20260101-143000/
├── run.json
├── logs/events.ndjson
├── source_assets/
├── research/
├── script/
├── assets/
├── video/
├── qa/
├── finishing/
├── tmp/
└── final.mp4
```

Generated client assets stay inside the run. Promote an approved reusable character to `characters/` only through an explicit separate operation.

## Intermediates and shared resources

- Per-run previews, crops, discarded frames, and temporary audio: `outputs/<flow>/<run_slug>/tmp/`.
- Experiments and comparison batches: `scratch/`.
- Downloaded research references: `_research/`.
- Reusable automation: `scripts/` and `pipeline/`.
- Shared SFX: `sfx/<category>/<slug>.mp3` plus `sfx/library.json`; copy used files into the run.

## Before closing a run

```bash
python scripts/validate_outputs.py
```

Resolve every reported contract violation before delivery.
