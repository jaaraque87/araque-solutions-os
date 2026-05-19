"""
Step 08 — Lipsync (Sync-3 via fal.ai)  [OPTIONAL]
====================================================
Applies lip sync to Kling video clips using the Sync-3 model on fal.ai.
This makes the character's mouth movements match the voice audio.

Input:   run_dir/kling_scene_N.mp4    (from step 07)
         run_dir/voice_scene_N.mp3    (from step 06, or tts fallback)
Output:  run_dir/sync_scene_N.mp4    (one per scene)

fal.ai endpoint: fal-ai/sync-lipsync

Cost: ~$0.10 per clip × 6 scenes = ~$0.60

SKIP THIS STEP if using ComfyUI TODOENUNO which does lipsync natively.
"""

import json
import os
from pathlib import Path

import fal_client
import httpx

FAL_SYNC_MODEL = "fal-ai/sync-lipsync"


def _find_voice_audio(run_dir: Path, sid: int) -> Path | None:
    for name in [f"voice_scene_{sid}.mp3", f"voice_scene_{sid}.wav",
                 f"tts_scene_{sid}.wav", f"tts_scene_{sid}.mp3"]:
        p = run_dir / name
        if p.exists():
            return p
    return None


def _upload_to_fal(path: Path) -> str:
    return fal_client.upload_file(path)


def _download_video(url: str, dest: Path) -> None:
    with httpx.Client(timeout=300) as client:
        r = client.get(url)
        r.raise_for_status()
    dest.write_bytes(r.content)


def run(ctx: dict) -> dict:
    run_dir: Path = ctx["run_dir"]
    console       = ctx["console"]

    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        raise EnvironmentError("FAL_KEY not set")
    os.environ["FAL_KEY"] = fal_key

    # Find Kling clips
    kling_clips = sorted(run_dir.glob("kling_scene_*.mp4"))
    if not kling_clips:
        raise FileNotFoundError("No kling_scene_*.mp4 found. Run step 07 first.")

    console.print(f"  Sync-3 lipsync — {len(kling_clips)} clips")

    outputs = []
    total_cost = 0.0

    for clip_path in kling_clips:
        # Extract scene id: kling_scene_1.mp4 → 1
        sid_str = clip_path.stem.replace("kling_scene_", "")
        try:
            sid = int(sid_str)
        except ValueError:
            continue

        audio_path = _find_voice_audio(run_dir, sid)
        if not audio_path:
            console.print(f"  [yellow]⚠  No audio for scene {sid} — skipping sync[/yellow]")
            continue

        out_path = run_dir / f"sync_scene_{sid}.mp4"
        console.print(f"  [dim]Escena {sid}: {clip_path.name} + {audio_path.name}[/dim]")

        # Upload both files to fal storage
        console.print(f"  [dim]  → subiendo archivos...[/dim]")
        video_url = _upload_to_fal(clip_path)
        audio_url = _upload_to_fal(audio_path)

        console.print(f"  [dim]  → aplicando lipsync...[/dim]")

        result = fal_client.subscribe(
            FAL_SYNC_MODEL,
            arguments={
                "video_url": video_url,
                "audio_url": audio_url,
                "model": "sync-1.9.0-beta",  # or "wav2lip", depends on fal version
                "sync_mode": "bounce",        # "cut_off" or "bounce"
                "fps": 25,
                "output_format": "mp4",
            },
            with_logs=False,
        )

        output = result.get("video", {})
        output_url = output.get("url", "") if isinstance(output, dict) else result.get("url", "")

        if not output_url:
            console.print(f"  [red]✗ No sync output for scene {sid}[/red]")
            continue

        _download_video(output_url, out_path)
        file_size_mb = out_path.stat().st_size // (1024 * 1024)
        console.print(f"  [green]✓[/green] sync_scene_{sid}.mp4 ({file_size_mb} MB)")

        outputs.append({
            "scene_id": sid,
            "path": str(out_path),
            "url": output_url,
        })
        total_cost += 0.10

    console.print(f"  [green]✓[/green] {len(outputs)} clips con lipsync")

    return {
        "status": "ok",
        "cost_usd": total_cost,
        "synced_clips": outputs,
        "num_synced": len(outputs),
    }
