"""
Step 07 — Video Clips (Kling via fal.ai)
==========================================
Generates raw video clips from scene images + voice audio using Kling.

Input:   run_dir/scene_N.png          (from step 04, or locacion_N if no morpheus)
         run_dir/voice_scene_N.mp3    (from step 06, or tts_scene_N if no voice_change)
         run_dir/guion.json
Output:  run_dir/kling_scene_N.mp4   (one per scene)

Kling endpoint: fal-ai/kling-video/v2.1/standard/image-to-video
                fal-ai/kling-video/v2.1/pro/image-to-video  (higher quality)

Cost: ~$1.20 total for 6 scenes (~$0.20/clip at standard quality)
"""

import json
import os
from pathlib import Path

import fal_client
import httpx

# Kling model options
FAL_KLING_STANDARD = "fal-ai/kling-video/v2.1/standard/image-to-video"
FAL_KLING_PRO      = "fal-ai/kling-video/v2.1/pro/image-to-video"

DEFAULT_DURATION   = "5"   # "5" or "10" seconds
DEFAULT_ASPECT     = "9:16"  # vertical for Reels/TikTok
DEFAULT_MODE       = "standard"  # "standard" or "pro"


def _find_scene_image(run_dir: Path, sid: int) -> Path | None:
    """Look for scene frame — prefer morpheus output, fallback to locacion."""
    for name in [f"scene_{sid}.png", f"locacion_{sid}.png", f"personaje.png"]:
        p = run_dir / name
        if p.exists():
            return p
    return None


def _find_voice_audio(run_dir: Path, sid: int) -> Path | None:
    """Look for voice audio — prefer voice_change output, fallback to TTS."""
    for name in [f"voice_scene_{sid}.mp3", f"voice_scene_{sid}.wav",
                 f"tts_scene_{sid}.wav", f"tts_scene_{sid}.mp3"]:
        p = run_dir / name
        if p.exists():
            return p
    return None


def _upload_to_fal(path: Path) -> str:
    """Upload a local file to fal.ai storage and return its URL."""
    url = fal_client.upload_file(path)
    return url


def _download_video(url: str, dest: Path) -> None:
    with httpx.Client(timeout=300) as client:
        r = client.get(url)
        r.raise_for_status()
    dest.write_bytes(r.content)


def _build_motion_prompt(scene: dict) -> str:
    action  = scene.get("action", "talking to camera naturally")
    dialogue_hint = scene.get("dialogue", "")[:40]

    return (
        f"{action}, "
        f"natural movement, authentic UGC style, "
        f"subtle gestures while speaking, "
        f"iPhone handheld feel, "
        f"lifestyle content creator, "
        f"smooth motion, cinematic"
    )


def run(ctx: dict) -> dict:
    brand: str    = ctx["brand"]
    run_dir: Path = ctx["run_dir"]
    console       = ctx["console"]

    # Load guion
    guion_path = run_dir / "guion.json"
    if not guion_path.exists():
        raise FileNotFoundError("guion.json not found. Run step 01 first.")
    guion  = json.loads(guion_path.read_text(encoding="utf-8"))
    scenes = guion.get("scenes", [])

    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        raise EnvironmentError("FAL_KEY not set")
    os.environ["FAL_KEY"] = fal_key

    # Config from env (allow override)
    kling_mode = os.getenv("KLING_MODE", DEFAULT_MODE)
    kling_model = FAL_KLING_PRO if kling_mode == "pro" else FAL_KLING_STANDARD
    kling_duration = os.getenv("KLING_DURATION", DEFAULT_DURATION)

    console.print(f"  Kling mode: [bold]{kling_mode}[/bold]  Duration: {kling_duration}s  "
                  f"Aspect: {DEFAULT_ASPECT}")

    outputs = []
    total_cost = 0.0
    cost_per_clip = 0.28 if kling_mode == "pro" else 0.14

    for scene in scenes:
        sid = scene["scene_id"]

        img_path = _find_scene_image(run_dir, sid)
        if not img_path:
            console.print(f"  [red]✗ No image found for scene {sid} — skipping[/red]")
            continue

        audio_path = _find_voice_audio(run_dir, sid)
        out_path = run_dir / f"kling_scene_{sid}.mp4"

        motion_prompt = _build_motion_prompt(scene)
        console.print(f"  [dim]Escena {sid}: {img_path.name} → kling (uploading...)[/dim]")

        # Upload image to fal storage
        img_url = _upload_to_fal(img_path)

        arguments = {
            "prompt": motion_prompt,
            "image_url": img_url,
            "duration": kling_duration,
            "aspect_ratio": DEFAULT_ASPECT,
        }

        # Note: Kling I2V with audio is supported via a separate endpoint in some versions
        # For now we generate video silently — audio sync happens in step 08
        console.print(f"  [dim]  → generando video (puede tardar 2-4 min)...[/dim]")

        result = fal_client.subscribe(
            kling_model,
            arguments=arguments,
            with_logs=False,
        )

        video = result.get("video", {})
        video_url = video.get("url", "") if isinstance(video, dict) else ""

        if not video_url:
            console.print(f"  [red]✗ No video URL for scene {sid}. Response: {result}[/red]")
            continue

        _download_video(video_url, out_path)
        file_size_mb = out_path.stat().st_size // (1024 * 1024)
        console.print(f"  [green]✓[/green] kling_scene_{sid}.mp4 ({file_size_mb} MB)")

        outputs.append({
            "scene_id": sid,
            "path": str(out_path),
            "url": video_url,
            "image_used": str(img_path),
        })
        total_cost += cost_per_clip

    console.print(f"  [green]✓[/green] {len(outputs)}/{len(scenes)} videos generados")

    return {
        "status": "ok" if len(outputs) == len(scenes) else "partial",
        "cost_usd": total_cost,
        "clips": outputs,
        "kling_mode": kling_mode,
        "num_generated": len(outputs),
    }
