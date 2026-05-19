"""
Step 03 — Locación (Location Frames)
======================================
Generates an empty location/background frame for each scene.
No character in the shot — pure environment to composite later.

Input:   run_dir/guion.json
         run_dir/brand_profile.json
Output:  run_dir/locacion_1.png
         run_dir/locacion_2.png  ... (one per scene)

Cost: ~$0.41 per image × N scenes (estimated as single cost here, actual is per scene)
"""

import json
import os
from pathlib import Path

import fal_client
import httpx

FAL_MODEL = "fal-ai/flux/dev"


def _location_prompt(scene: dict, profile: dict) -> str:
    visual   = profile.get("visual_identity", {})
    style    = visual.get("style", "iPhone UGC style")
    lighting = visual.get("lighting", "golden hour")
    location = scene.get("location", "Miami waterfront")
    brief    = scene.get("brief_visual", "")

    # Extract environment description from brief_visual if possible
    env_hint = ""
    if brief:
        # take first half of brief as environment context
        env_hint = brief.split(",")[0] if "," in brief else brief[:60]

    return (
        f"{location}, empty scene without people, "
        f"{env_hint}, "
        f"{lighting}, "
        f"{style}, "
        f"cinematic background, lifestyle photography, "
        f"sharp focus, photorealistic, high quality"
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

    # Load inputs
    guion_path = run_dir / "guion.json"
    if not guion_path.exists():
        raise FileNotFoundError("guion.json not found. Run step 01 first.")

    profile_path = run_dir / "brand_profile.json"
    if not profile_path.exists():
        profile_path = ctx["brands_dir"] / brand / "brand_profile.json"
    if not profile_path.exists():
        raise FileNotFoundError("brand_profile.json not found. Run step 00 first.")

    guion   = json.loads(guion_path.read_text(encoding="utf-8"))
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    scenes  = guion.get("scenes", [])

    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        raise EnvironmentError("FAL_KEY not set")
    os.environ["FAL_KEY"] = fal_key

    outputs = []
    total_cost = 0.0

    for scene in scenes:
        sid = scene["scene_id"]
        prompt = _location_prompt(scene, profile)
        console.print(f"  [dim]Escena {sid}: {scene.get('location', '')}[/dim]")

        result = fal_client.subscribe(
            FAL_MODEL,
            arguments={
                "prompt": prompt,
                "negative_prompt": "people, person, character, face, body, "
                                   "deformed, blurry, low quality, text, watermark",
                "image_size": "portrait_4_3",
                "num_inference_steps": 25,
                "guidance_scale": 3.5,
                "num_images": 1,
                "enable_safety_checker": True,
            },
            with_logs=False,
        )

        images = result.get("images", [])
        if not images:
            console.print(f"  [red]✗ No image for scene {sid}[/red]")
            continue

        image_url = images[0]["url"]
        out_path = run_dir / f"locacion_{sid}.png"
        _download_image(image_url, out_path)

        file_size_kb = out_path.stat().st_size // 1024
        console.print(f"  [green]✓[/green] locacion_{sid}.png ({file_size_kb} KB)")

        outputs.append({
            "scene_id": sid,
            "path": str(out_path),
            "url": image_url,
        })
        total_cost += 0.07  # ~$0.07 per image on flux/dev

    console.print(f"  [green]✓[/green] {len(outputs)} locaciones generadas")

    return {
        "status": "ok",
        "cost_usd": total_cost,
        "locaciones": outputs,
        "num_generated": len(outputs),
    }
