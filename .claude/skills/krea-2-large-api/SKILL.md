---
name: krea-2-large-api
description: Use this skill whenever the user asks to use Krea, Krea 2, Krea 2 Large, Krea API, Krea image generation, style references, moodboards, trained Krea styles, or LoRAs via API. This skill covers auth, async job polling, Krea 2 Large request bodies, style/LoRA discovery and sharing, and practical cURL/Python usage. Trigger even when the user says "usar mi LoRA en Krea", "Krea 2 Large via API", "generar imagen con Krea", or "style id / moodboard id".
---

# Krea 2 Large API

Use this skill to integrate or operate Krea 2 Large through the official Krea API.

Last researched: 2026-06-09 against Krea docs and `https://api.krea.ai/openapi.json`.

## Secret handling

Never put the user's Krea API key into generated code, docs, commits, or skill files.

Prefer this lookup order:

1. Existing environment variable `KREA_API_KEY`.
2. Existing environment variable `KREA_API_TOKEN`.
3. Global private env file `~/.config/krea/env`, which may export `KREA_API_KEY`.

To use the key in shell commands:

```bash
source ~/.config/krea/env
```

When showing examples, always use `$KREA_API_KEY` or `<token>`, never the real key.

## Core model facts

- Base URL: `https://api.krea.ai`
- Auth: `Authorization: Bearer $KREA_API_KEY`
- Krea 2 Large endpoint: `POST /generate/image/krea/krea-2/large`
- Full URL: `https://api.krea.ai/generate/image/krea/krea-2/large`
- Krea 2 Large is asynchronous: creation returns a `job_id`; poll `GET /jobs/{job_id}` until terminal state.
- For production or long Krea 2 Large jobs, prefer the optional `X-Webhook-URL` header over tight polling.
- Result image URLs are available at `result.urls` when the job status is `completed`.
- Failed and cancelled jobs are not billed according to Krea docs, but completed jobs are paid.

## Krea 2 Large request body

Required:

```json
{
  "prompt": "a cinematic glass cabin beside a frozen lake at sunrise",
  "aspect_ratio": "16:9",
  "resolution": "1K"
}
```

Optional fields from the current OpenAPI schema:

- `seed`: number or null.
- `creativity`: one of `raw`, `low`, `medium`, `high`.
- `styles`: trained styles / LoRAs, as `[{ "id": "STYLE_ID", "strength": 0.8 }]`.
- `image_style_references`: up to 10 references, as `[{ "url": "https://...", "strength": 0.5 }]`.
- `moodboards`: max 1, as `[{ "id": "MOODBOARD_UUID", "strength": 0.23 }]`.
- `intensity`: integer from `-100` to `100`; use `0` for neutral.
- `complexity`: integer from `-100` to `100`; use `0` for neutral.

Supported `aspect_ratio` values:

```text
1:1, 4:3, 3:2, 16:9, 2.35:1, 4:5, 2:3, 9:16
```

Current `resolution` support is only `1K`.

Set `creativity` explicitly because Krea pages and OpenAPI may disagree on the default. Use:

- `raw` for tightly art-directed prompts.
- `low` when prompt adherence matters.
- `medium` for balanced interpretation.
- `high` for expressive, aesthetic expansion.

## Generate and poll with cURL

Use snake_case fields. Deprecated aliases such as `presetStyles` and `imageStyleRefs` are being sunset on 2026-06-19.

```bash
source ~/.config/krea/env

JOB_ID=$(curl -sS -X POST "https://api.krea.ai/generate/image/krea/krea-2/large" \
  -H "Authorization: Bearer $KREA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a raw photoreal editorial portrait, grainy low dynamic range, morning window light",
    "aspect_ratio": "4:5",
    "resolution": "1K",
    "creativity": "medium"
  }' | jq -r '.job_id')

while :; do
  RESULT=$(curl -sS "https://api.krea.ai/jobs/$JOB_ID" \
    -H "Authorization: Bearer $KREA_API_KEY")
  STATUS=$(printf "%s" "$RESULT" | jq -r '.status')
  printf "%s\n" "$STATUS"
  case "$STATUS" in
    completed)
      printf "%s\n" "$RESULT" | jq -r '.result.urls[]'
      break
      ;;
    failed|cancelled)
      printf "%s\n" "$RESULT" | jq
      break
      ;;
  esac
  sleep 3
done
```

## Helper script

This skill includes `scripts/krea_api.py`. Use it when you want deterministic REST calls without retyping polling logic.

Examples:

```bash
python ~/.codex/skills/krea-2-large-api/scripts/krea_api.py generate \
  "a gritty photoreal campaign image for an outdoor lamp collection" \
  --aspect-ratio 16:9 \
  --creativity high
```

With a trained style / LoRA:

```bash
python ~/.codex/skills/krea-2-large-api/scripts/krea_api.py generate \
  "a fashion editorial portrait in my trained visual style" \
  --aspect-ratio 4:5 \
  --style STYLE_ID=0.85
```

List accessible styles:

```bash
python ~/.codex/skills/krea-2-large-api/scripts/krea_api.py styles --filter user --limit 50
python ~/.codex/skills/krea-2-large-api/scripts/krea_api.py styles --filter shared --limit 50
```

Share an owned style with the workspace:

```bash
python ~/.codex/skills/krea-2-large-api/scripts/krea_api.py share-style STYLE_ID
```

## LoRAs and trained Krea styles

Krea's API calls LoRAs "styles". The current Krea 2 OpenAPI schema exposes `styles` on Krea 2 Large, with items shaped like:

```json
{
  "styles": [
    { "id": "STYLE_ID", "strength": 0.8 }
  ]
}
```

Practical guidance:

- If the user already trained a LoRA/style in Krea, first find its style ID.
- Use `GET /styles?filter=user` for styles owned by the API identity.
- Use `GET /styles?filter=shared` for styles shared into the API workspace.
- Use `GET /styles/{id}` to inspect one style. Check its `models` list when present; incompatible styles may be rejected by generation.
- Krea web app and Krea API can behave as separate user identities. An app-trained style may not be usable by the API until shared with the workspace.
- To share a style the user owns with the workspace, call `POST /styles/{id}/share/workspace`.
- Start LoRA/style strength around `0.8`. Use `0.5-0.7` for subtle influence, `0.8-0.9` for strong style, and `0.95-1.0` for maximum adherence.
- If a trained style fails on Krea 2 Large because it was trained for another base model, use style references or a moodboard as the fallback, or train a Krea-2-compatible style when available in the account.

## Style references

Use `image_style_references` when the user has example images but no trained style, or when a LoRA is not compatible with Krea 2.

Current OpenAPI range is `0..1` per reference, with default around `0.5`.

```json
{
  "prompt": "a portrait of a dancer in a quiet studio",
  "aspect_ratio": "4:3",
  "resolution": "1K",
  "creativity": "medium",
  "image_style_references": [
    { "url": "https://example.com/style-reference.png", "strength": 0.6 }
  ]
}
```

Reference images should be hosted URLs. Upload local files first using `POST /assets` if needed.

## Moodboards

Use `moodboards` when the user wants a broader visual direction: palette, texture, mood, and composition. Moodboards are created in the Krea web app first, then referenced by ID in the API.

Current OpenAPI allows max 1 moodboard per Krea 2 request, with `strength` in `0..1`.

```json
{
  "prompt": "a campaign image for a new outdoor lamp collection",
  "aspect_ratio": "16:9",
  "resolution": "1K",
  "creativity": "high",
  "moodboards": [
    { "id": "1e51738c-7413-469e-93b6-ad50db460a1f", "strength": 0.35 }
  ]
}
```

## Saved style preset: RONALDINHO

Use `RONALDINHO` when the user asks for Paul's favorite caricature style, "mi estilo fav", "estilo Ronaldinho", colored-pencil caricature, pastel caricature, or the rough-paper handmade caricature look.

Reference image:

- Local file: `/Users/pauldelavallaz/Documents/MORFEO/MORFEO IDENTIDAD/YO/CARICATURA/omni-8bdc5120-edea-4554-a5b7-0c3f93ab036a.png`
- Uploaded Krea asset URL: `https://app-uploads.krea.ai/43f7ea83-02fb-4b4e-8c49-2c09c57119f9/1780973203512-omni-8bdc5120-edea-4554-a5b7-0c3f93ab036a.png`
- UI settings observed: Krea 2 Large, Creativity 65, Intensity 10, Complexity 15.
- API mapping: `creativity: "high"`, `intensity: 10`, `complexity: 15`.
- Use `aspect_ratio: "2:3"` when the user wants the same poster/caricature framing as the favorite example.

Core style language:

```text
Colored-pencil caricature of a young man, exaggerated colored-pencil caricature, huge expressive head and small playful body, humorous but flattering likeness, slightly oversized hair mass, amplified eyebrows, nose, cheeks and jaw, visible stubble drawn with pencil strokes, traditional colored-pencil and crayon texture on rough paper, saturated warm colors, hand-drawn sketch lines, layered pencil shading, painterly edges, magazine caricature energy, vibrant but handmade, character dominates the frame, high quality illustration.
```

Default Krea style-reference settings:

```json
{
  "creativity": "high",
  "intensity": 10,
  "complexity": 15,
  "image_style_references": [
    {
      "url": "https://app-uploads.krea.ai/43f7ea83-02fb-4b4e-8c49-2c09c57119f9/1780973203512-omni-8bdc5120-edea-4554-a5b7-0c3f93ab036a.png",
      "strength": 0.72
    }
  ]
}
```

Tuning:

- Use `0.65-0.72` style-reference strength when changing wardrobe/location while preserving the handmade pencil texture.
- Use `0.75-0.85` only when style fidelity matters more than prompt obedience.
- Lower to `0.55-0.62` if Krea copies too much of the original living-room background, hoodie, or facial pose.
- Include `no text, no logo, no signature, no artist signature, no watermark` because Krea may hallucinate a bottom-right signature in this style.

RONALDINHO prompt template:

```text
Colored-pencil caricature of Paul, exaggerated colored-pencil caricature of a young man with thick dark voluminous hair, strong dark eyebrows, hazel-green eyes, light olive skin, short dark stubble beard, huge expressive head and small playful body, cool neutral serious expression, humorous but flattering likeness, slightly oversized hair mass, amplified eyebrows, nose, cheeks and jaw, visible stubble drawn with pencil strokes, traditional colored-pencil and crayon texture on rough paper, saturated warm colors, hand-drawn sketch lines, layered pencil shading, painterly edges, magazine caricature energy, vibrant but handmade.

Change only the setting and wardrobe: [LOCATION]. Wardrobe: [WARDROBE]. Character dominates the frame, high quality illustration, no text, no logo, no signature, no watermark.
```

## Optional Paul identity transfer workflow

Use this optional workflow when the user asks to generate Paul, "a mi", "yo como protagonista", or asks to transfer Paul's identity into a Krea/style image. The default Paul identity reference is:

```text
/Users/pauldelavallaz/Documents/MORFEO/MORFEO IDENTIDAD/YO/Face_living_simple_01_serio_neutral_00001_.png
```

Goal: transfer recognizability without letting identity overpower the target expression, pose, medium, or style. A previous direct identity transfer made the face too perfect and weakened expression/style, so bias toward caricature identity anchors rather than exact face replacement.

Step-by-step:

1. Separate the inputs into three layers: identity, style, and change request.
2. Identity layer: extract only stable anchors from Paul's reference: light olive skin, round-oval face, thick dark voluminous hair swept up/sideways, strong dark eyebrows, hazel-green almond eyes, straight nose with rounded tip, full lips, short dark stubble beard along jaw/chin/mustache.
3. Style layer: lock the target medium before describing identity. For RONALDINHO, say colored-pencil, crayon, rough paper, handmade sketch lines, layered pencil shading, saturated warm colors, painterly edges.
4. Expression layer: explicitly preserve the requested or target expression. Do not inherit the selfie expression unless the user asks. Example: `preserve the cool neutral serious caricature expression from the target style, not a realistic selfie expression`.
5. Caricature layer: ask for `flattering caricature likeness, not a literal photoreal face swap`. Use `identity resemblance around 65-75%, style and expression priority higher than exact anatomy` when using image-editing models that support such wording.
6. Change layer: state only the variables that should change, usually location and wardrobe. Add `do not change the illustration medium, proportions, or expression`.
7. For Krea-only generation, prefer a trained Paul face LoRA in `styles` when accessible. If no LoRA is visible to the API, use prompt descriptors for identity and a style reference/moodboard for look; do not use the selfie as `image_style_references` because Krea style refs are for look transfer, not face identity.
8. For external image-editing models such as GPT-image workflows, provide two references when available: Paul's selfie as identity reference and the target/caricature image as style reference. In the prompt, mark the selfie as `identity only` and the style image as `style, expression, composition, and medium`.
9. Iterate in small moves: if identity is too strong, reduce exact facial detail and add `more caricatured, less literal`; if style is too weak, increase style-reference strength or repeat the medium/style language earlier in the prompt.

Reusable identity-transfer prompt block:

```text
Use Paul's selfie only as identity inspiration, not as a literal face replacement. Preserve the target artwork's expression, pose, proportions, and handmade medium. Transfer only the recognizable anchors: thick dark voluminous hair, strong eyebrows, hazel-green eyes, light olive skin, round-oval face, straight rounded-tip nose, full lips, and short dark stubble. Make it a flattering caricature resemblance, around 70% identity strength, with style fidelity more important than anatomical exactness.
```

## Training a new style

Use `POST /styles/train` for API-trained styles. Required:

- `name`: descriptive style name.
- `urls`: hosted image URLs.

Common optional fields:

- `model`: `flux_dev`, `flux_schnell`, `qwen`, `z-image`, `wan22`, or video `wan` depending on current availability.
- `type`: `Style`, `Object`, `Character`, or `Default`.
- `trigger_word`: unique activation word; underscores are useful.
- `max_train_steps`: 1 to 2000.
- `learning_rate` and `batch_size` only when the defaults are not working.

The training endpoint returns a job. Poll `GET /jobs/{job_id}`; when completed, `result.style_id` is the style ID to use in `styles`.

## Decision pattern

When the user wants to generate:

1. Confirm whether a paid generation is intended if the wording is ambiguous.
2. Pick Krea 2 Large for photorealism, raw texture, motion blur, grain, low dynamic range, and high-ceiling aesthetic work.
3. Use explicit `aspect_ratio`, `resolution: "1K"`, and explicit `creativity`.
4. Add `styles` for trained LoRAs, `image_style_references` for reference-image look transfer, and `moodboards` for broad art direction.
5. Submit the job, then poll every 2-5 seconds or use a webhook.
6. Return the image URLs and relevant job metadata. Do not expose secrets.

When the user asks "can I use my LoRA?":

1. Explain that yes, Krea API uses the `styles` array for trained styles/LoRAs on Krea 2 according to the current OpenAPI.
2. Check whether the style is visible through `GET /styles?filter=user` or `GET /styles?filter=shared`.
3. If it was trained in the web app and not visible to the API, tell the user to share it with the workspace or use `POST /styles/{id}/share/workspace` if the API identity owns it.
4. If it is not compatible with Krea 2, use style references or moodboards as the nearest fallback.
