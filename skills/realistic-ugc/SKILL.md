---
name: realistic-ugc
description: Produce premium 30-second vertical UGC ads that look phone-shot and physically credible, using conversion research, a seven-shot script, Krea 2/GPT Image identity assets, one multimodal Seedance 2.5 generation through Kie, gated approvals, QA, and optional shot patches. Use when a client asks for realistic influencer-style product UGC, an iPhone-looking TikTok/Reel, a creator naturally using a product in a real location, or Araque's next-level/premium UGC production. Do not use for HeyGen avatars, editorial avatar reels, modular lipsync-by-clip production, or simple B-roll.
---

# Realistic UGC

Produce one premium 30-second, 9:16 UGC ad as a contracted `realistic_ugc` run. Treat every provider call as paid production: never add `--execute` without explicit approval for that stage.

## Contract

- Write runs to `outputs/ugc/<description>-<YYYYMMDD-HHMMSS>/`.
- Keep generated assets, prompts, QA, and patches inside the run.
- Maintain `run.json` and `logs/events.ndjson` through the flow CLI.
- Promote an approved character to `characters/` only by explicit request.
- Read [references/shot-design.md](references/shot-design.md) before scripting, [references/seedance-prompt.md](references/seedance-prompt.md) before prompting, and [references/qa-and-patches.md](references/qa-and-patches.md) before QA or repair.

Run `python -m pipeline.flows.realistic_ugc.run --help` from the repository root. The wrapper at `scripts/realistic_ugc.py` invokes the same CLI.

## Workflow

### 1. Initialize

Require brand, campaign, product image, product facts, audience, and brief. Recommend a look reference.

```powershell
python -m pipeline.flows.realistic_ugc.run init `
  --brand "<brand>" --campaign "<campaign>" --description "<description>" `
  --product-image "<product>" --look-image "<look>" --brief-file "<brief>"
```

### 2. Research conversion

Use `niche-radar`, `hook-lab`, `script-framework`, and client evidence. Write `research/niche.md`, scored `research/hooks.json`, and `research/strategy.md`. Register them with `mark-ready --stage research`, present the selected hypothesis, then record explicit approval with `approve --stage research`.

### 3. Write and approve the script

Use `guion-ugc` plus the shot-design reference. Produce `script/script.json`, `script/script.md`, `script/character-brief.txt`, and `script/location-brief.txt`. Keep dialogue near 68 words and each on-camera line at 13 words or fewer. Verify real product use from authoritative material. Register and approve the script before assets.

### 4. Generate and approve assets

Dry-run first:

```powershell
python -m pipeline.flows.realistic_ugc.run assets --run-dir "<run>" `
  --character-brief "<run>/script/character-brief.txt" `
  --location-brief "<run>/script/location-brief.txt"
```

After spend approval, repeat with `--execute`. Review one identity across five views and confirm the location has no humans, silhouettes, portraits, mannequins, or reflections. Approve assets to unlock video.

### 5. Prompt and generate video

Write `script/seedance-prompt.txt`. Map references in this order: character sheet, empty location, official product, look reference. The `@Image N` mapping must match. Include continuity, seven hard-cut shots, phone camera behavior, room audio, and consistency. Request no music, captions, titles, UI, or animated logos.

Run `video --run-dir "<run>" --prompt-file "<prompt>"` to preview. Show the payload and current quote. Add `--execute` only after approval.

### 6. QA and finish

Run `qa --run-dir "<run>" --transcribe`. Automated QA does not replace human review. Check identity, duplicates, counts, label, product physics, dialogue, background, unwanted text, and audio. Approve QA, finish with `music-ugc`, `sfx-ugc`, and HyperFrames/finishing tools as appropriate, then register it with `mark-ready --stage finishing`, record client approval with `approve --stage finishing`, and promote the canonical `final.mp4` with `finish`.

## Repair rule

Do not regenerate merely for deviation. Diagnose first. For one failed shot, detect cuts, prepare anchors, and propose a patch using the QA reference. Obtain approval before patch generation.

## Hard rules

- Require approval before paid assets, video, patches, and delivery.
- Use no music or burned captions in Seedance.
- Every object enters through a visible hand; keep exactly one protagonist.
- Explain before paid calls that client media is uploaded to fal.ai/Kie.ai.
- Never commit secrets, signed URLs, generated media, or `.env` contents.
