---
name: facs-acting-direction
description: "Create anatomically precise emotional acting direction for Morfeo UGC / GPT Image 2 image prompts, portraits, cinematic close-ups, UGC scene frames, character references, and expressive still frames. Do not use for Seedance Lipsync, Seedance Storyboards, or Seedance video prompts."
---

# FACS Acting Direction

Use this skill to turn generic emotion requests into controlled facial performance maps for image generation, especially Morfeo UGC / GPT Image 2 scene frames.

Do not apply this skill to Seedance Lipsync, Seedance Storyboards, Seedance Prompt Packs, or any Seedance video prompt. Seedance uses simple acting/delivery language instead.

Core principle: FACS describes visible facial muscle movement; it does not diagnose emotion by itself. The final emotional read comes from combining Action Units, intensity, valence/arousal/dominance, gaze, breath, jaw, posture, context, and delivery.

## Workflow

1. Decide whether FACS is useful.
   - Use it for visible faces, portraits, close-ups, cinematic frames, character acting, Morfeo UGC scenes, and expressive image prompts.
   - Skip it for product-only shots, hands-only scenes, tiny faces, masked faces, off-camera speakers, or when expression should remain neutral.
   - Always skip it for Seedance Lipsync, Seedance Storyboards, and Seedance video prompts.

2. Translate the intent into an emotional state.
   - `valence`: negative to positive emotion, from `-1` to `+1`.
   - `arousal`: activation/energy, from `-1` to `+1`.
   - `dominance`: control/power, from `-1` to `+1`.

3. Select or compose FACS Action Units.
   - Read [facs-reference.md](references/facs-reference.md) when you need the AU combinations, the 50 ready-to-use expression recipes, or the prompt templates.
   - Prefer medium intensities (`0.25-0.70`) for believable cinematic/UGC images.
   - Use high intensities only for shock, panic, screaming, physical comedy, or stylized performance.

4. Add performance direction.
   - Include breath, jaw, gaze, eyelids, posture, shoulders, hands, voice/delivery if dialogue matters, and micro-expression timing.
   - Do not rely on AU codes alone. Models respond better to anatomical names plus visible performance notes.

5. Write the prompt.
   - For image prompts, include the full map when expression is central.
   - For Morfeo scene-frame prompts, keep the map concise enough to fit inside the scene brief when useful.
   - Avoid generic commands like `make her sad`; write the anatomical/performance result instead.

## Output Shape

Default structure:

```text
EMOTIONAL STATE:
valence:
arousal:
dominance:

FACS:
AU code + muscle/action name + intensity.

PERFORMANCE:
breath, tension, posture, gaze, jaw, mouth, micro-expressions, delivery.

VISUAL RESULT:
what the face must communicate, with restraint/intensity guidance.
```

Compact inline version:

```text
restrained anxiety: AU4 brow lowerer 0.55, AU7 lid tightener 0.45, AU23 lip tightener 0.35, AU25 lips slightly parted 0.30, shallow breath, tense jaw, wet focused eyes.
```

## Guardrails

- Never say FACS proves an emotion. Say it builds a probable emotional read.
- Do not stack too many AUs without a clear performance goal.
- Do not use this for lipsync/video prompts; for still frames, avoid facial directions that fight the intended visible expression.
- Do not make every scene emotionally extreme; controlled tension often looks more real.
- Pair the face with body acting. Shoulders, neck, hands, breath, and eye line carry emotion too.
- For UGC realism, prioritize believable restraint over theatrical facial distortion.

## Reference

Use [facs-reference.md](references/facs-reference.md) for:

- FACS/EMFACS concept summary;
- valence/arousal/dominance formula;
- the full 50-combination expression library;
- ready-to-use prompt templates;
- compact prompt patterns for image and still-frame use.
