"""
Step 02 — Personaje (Character Portrait)
=========================================
Generates a full-body character reference image using fal.ai.

Uses:
  - fal-ai/flux/dev with LoRA (if configured)
  - OR fal-ai/ideogram/v2 as fallback

Input:   run_dir/brand_profile.json
Output:  run_dir/personaje.png

Cost: ~$0.41 per image
"""

import os
import json
from pathlib import Path

import fal_client
import httpx


# fal.ai model endpoints (in order of preference)
FAL_MODEL_FLUX   = "fal-ai/flux-lora"
FAL_MODEL_FLUX_DEV = "fal-ai/flux/dev"


def _build_prompt(profile: dict) -> str:
    persona = profile.get("persona", {})
    visual  = profile.get("visual_identity", {})
    trigger = profile.get("lora_trigger", "")
    locations = visual.get("locations", ["Miami waterfront"])

    name        = persona.get("name", "character")
    appearance  = persona.get("appearance", "black bob hair, green eyes, light olive skin")
    style       = visual.get("style", "iPhone UGC style")
    lighting    = visual.get("lighting", "golden hour")
    location    = locations[0] if locations else "urban setting"

    trigger_prefix = f"{trigger}, " if trigger else ""

    return (
        f"{trigger_prefix}{appearance}, "
        f"full body portrait, standing, "
        f"{location}, {lighting}, "
        f"{style}, "
        f"casual lifestyle fashion, "
        f"looking at camera, natural expression, "
        f"sharp focus, photorealistic"
    )


def _download_image(url: str, dest: Path) -> None:
    with httpx.Client(timeout=120) as client:
        r = client.get(url)
        r.raise_for_status()
    dest.write_bytes(r.content)


def run(ctx: dict) -> dict:
    brand: str    = ctx["brand"]
    run_dir: Path = ctx["run_dir"]
    console       = ctx["console"]

    # Load brand profile
    profile_path = run_dir / "brand_profile.json"
    if not profile_path.exists():
        profile_path = ctx["brands_dir"] / brand / "brand_profile.json"
    if not profile_path.exists():
        raise FileNotFoundError("brand_profile.json not found. Run step 00 first.")

    profile = json.loads(profile_path.read_text(encoding="utf-8"))

    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        raise EnvironmentError("FAL_KEY not set")
    os.environ["FAL_KEY"] = fal_key  # ensure fal_client picks it up

    prompt = _build_prompt(profile)
    console.print(f"  [dim]Prompt: {prompt[:80]}...[/dim]")

    lora_path = profile.get("lora_path_fal", "")  # optional: URL or fal path to LoRA
    lora_strength = profile.get("lora_strength", 0.85)

    console.print(f"  Generando imagen de personaje en fal.ai...")

    if lora_path:
        # Use flux-lora with custom LoRA
        result = fal_client.subscribe(
            FAL_MODEL_FLUX,
            arguments={
                "prompt": prompt,
                "negative_prompt": "deformed, ugly, bad anatomy, blurry, low quality, "
                                   "text, watermark, logo",
                "image_size": "portrait_4_3",
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "num_images": 1,
                "enable_safety_checker": True,
                "loras": [{"path": lora_path, "scale": lora_strength}],
            },
            with_logs=False,
        )
    else:
        # Use flux/dev without LoRA
        result = fal_client.subscribe(
            FAL_MODEL_FLUX_DEV,
            arguments={
                "prompt": prompt,
                "negative_prompt": "deformed, ugly, bad anatomy, blurry, low quality, "
                                   "text, watermark, logo",
                "image_size": "portrait_4_3",
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "num_images": 1,
                "enable_safety_checker": True,
            },
            with_logs=False,
        )

    images = result.get("images", [])
    if not images:
        raise RuntimeError(f"fal.ai returned no images. Response: {result}")

    image_url = images[0]["url"]
    out_path = run_dir / "personaje.png"
    _download_image(image_url, out_path)

    file_size_kb = out_path.stat().st_size // 1024
    console.print(f"  [green]✓[/green] personaje.png ({file_size_kb} KB) → {out_path}")

    return {
        "status": "ok",
        "cost_usd": 0.41,
        "personaje_path": str(out_path),
        "image_url": image_url,
        "prompt": prompt,
    }
