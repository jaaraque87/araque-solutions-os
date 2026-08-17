# Realistic UGC premium

`realistic_ugc` is Araque Solutions OS's next-level client production flow: a 30-second vertical ad designed to feel captured by a real creator on a phone. It uses conversion research, seven physically staged shots, a locked character sheet, an empty location reference, and one Seedance 2.5 multimodal generation through Kie.

It complements rather than replaces the modular Kling/TTS/lipsync pipeline. Choose it for premium hero ads where natural behavior, product ritual, and continuous identity matter more than lowest unit cost.

## Operating model

1. Initialize a contracted `outputs/ugc/<run_slug>/` run.
2. Research the niche and approve a scored hook hypothesis.
3. Approve a seven-shot script with verified product physics.
4. Generate and approve portrait, character sheet, and empty location.
5. Dry-run the ordered Seedance reference payload.
6. Approve the provider quote and execute the 30-second generation.
7. Run automated and human QA; patch only a failed shot when practical.
8. Add music, SFX, captions, and finishing in post; promote `final.mp4`.

All provider operations are dry-run unless `--execute` is explicitly supplied. Client images are uploaded to fal.ai and Kie.ai during paid stages; disclose this data boundary before execution.

## Start

```powershell
python -m pipeline.flows.realistic_ugc.run --help
```

The complete agent workflow is in `skills/realistic-ugc/SKILL.md`.
