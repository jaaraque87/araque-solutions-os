"""
Step 04 — Morpheus (Scene Frames)
===================================
Composites the character (personaje) into each scene location using
fal-ai image editing (inpainting / IP-Adapter / image-to-image).

Strategy:
  - Uses fal-ai/flux/dev/image-to-image with the location as base
  - Injects character description to place her in the scene
  - Optionally uses personaje.png as IP-Adapter reference

Input:   run_dir/personaje.png
         run_dir/locacion_N.png  (per scene)
         run_dir/guion.json
         run_dir/brand_profile.json
Output:  run_dir/scene_N.png     (per scene) — character in location

Cost: ~$0.08 per scene
"""

import base64
import json
import os
from pathlib import Path

import fal_client
import httpx

FAL_MODEL_I2I    = "fal-ai/flux/dev/image-to-image"
FAL_MODEL_REDUX  = "fal-ai/flux-pro/v1/redux"   # IP-Adapter style transfer


def _encode_image_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def _image_to_data_uri(path: Path) -> str:
    b64 = _encode_image_b64(path)
    return f"data:image/png;base64,{b64}"


def _build_scene_prompt(scene: dict, profile: dict) -> str:
    persona    = profile.get("persona", {})
    visual     = profile.get("visual_identity", {})
    trigger    = profile.get("lora_trigger", "")
    appearance = persona.get("appearance", "black bob hair, green eyes, white skin")
    lighting   = visual.get("lighting", "golden hour")
    style      = visual.get("style", "iPhone UGC style")

    brief   = scene.get("brief_visual", "")
    outfit  = scene.get("outfit", "casual outfit")
    action  = scene.get("action", "talking to camera")
    location = scene.get("location", "")

    trigger_prefix = f"{trigger}, " if trigger else ""

    return (
        f"{trigger_prefix}{appearance}, "
        f"{outfit}, "
        f"{action}, "
        f"{location}, "
        f"{brief}, "
        f"{lighting}, "
        f"{style}, "
        f"full body, looking at camera, natural expression, "
        f"photorealistic, sharp focus"
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
        raise FileNotFoundError("brand_profile.json not found.")

    guion   = json.loads(guion_path.read_text(encoding="utf-8"))
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    scenes  = guion.get("scenes", [])

    personaje_path = run_dir / "personaje.png"
    has_personaje = personaje_path.exists()

    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        raise EnvironmentError("FAL_KEY not set")
    os.environ["FAL_KEY"] = fal_key

    outputs = []
    total_cost = 0.0

    for scene in scenes:
        sid = scene["scene_id"]
        prompt = _build_scene_prompt(scene, profile)
        location_img = run_dir / f"locacion_{sid}.png"

        console.print(f"  [dim]Escena {sid}: {scene.get('action', '')} @ {scene.get('location', '')}[/dim]")

        if location_img.exists():
            # image-to-image: use location as structural base, add character
            image_url_input = _image_to_data_uri(location_img)
            result = fal_client.subscribe(
                FAL_MODEL_I2I,
                arguments={
                    "prompt": prompt,
                    "negative_prompt": "deformed, ugly, bad anatomy, blurry, "
                                       "text, watermark, multiple people",
                    "image_url": image_url_input,
                    "strength": 0.75,           # 0=keep original, 1=ignore original
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                    "num_images": 1,
                    "enable_safety_checker": True,
                },
                with_logs=False,
            )
        else:
            # No location image — generate from scratch
            console.print(f"  [yellow]  locacion_{sid}.png not found, generando desde cero[/yellow]")
            result = fal_client.subscribe(
                "fal-ai/flux/dev",
                arguments={
                    "prompt": prompt,
                    "negative_prompt": "deformed, ugly, bad anatomy, blurry, "
                                       "text, watermark, multiple people",
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
            console.print(f"  [red]✗ No image for scene {sid}[/red]")
            continue

        image_url = images[0]["url"]
        out_path = run_dir / f"scene_{sid}.png"
        _download_image(image_url, out_path)

        file_size_kb = out_path.stat().st_size // 1024
        console.print(f"  [green]✓[/green] scene_{sid}.png ({file_size_kb} KB)")

        outputs.append({
            "scene_id": sid,
            "path": str(out_path),
            "url": image_url,
            "prompt": prompt,
        })
        total_cost += 0.08

    console.print(f"  [green]✓[/green] {len(outputs)}/{len(scenes)} scene frames generados")

    return {
        "status": "ok" if len(outputs) == len(scenes) else "partial",
        "cost_usd": total_cost,
        "scenes": outputs,
        "num_generated": len(outputs),
    }
