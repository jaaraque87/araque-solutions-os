"""
Step 09 — Background Music (Suno via Kie.ai)
=============================================
Generates background music tailored to the video mood using Suno V4.5
via the Kie.ai API.

Input:   run_dir/guion.json  (for music_mood)
Output:  run_dir/music.mp3

API: https://kie.ai/api/v1/suno

Cost: ~$0.06 per track

Kie.ai Suno API:
  POST /api/v1/suno/v4
  Headers: Authorization: Bearer {KIE_API_KEY}
  Body: { prompt, make_instrumental, model, wait_audio }
"""

import json
import os
import time
from pathlib import Path

import requests

KIE_BASE_URL    = "https://api.kie.ai"
SUNO_SUBMIT_URL = f"{KIE_BASE_URL}/api/v1/suno/v4"
SUNO_QUERY_URL  = f"{KIE_BASE_URL}/api/v1/suno/record-info"

MAX_WAIT_SECS   = 300   # 5 minutes max
POLL_INTERVAL   = 10    # poll every 10 seconds


def _build_music_prompt(guion: dict, profile: dict) -> str:
    mood    = guion.get("music_mood", "upbeat, positive, lifestyle")
    concept = guion.get("video_concept", "lifestyle content")
    brand   = guion.get("brand", "")
    visual  = profile.get("visual_identity", {})
    locations = visual.get("locations", ["Miami"])
    city = locations[0].split()[0] if locations else "Miami"

    return (
        f"{mood}, {city} vibes, {concept}, "
        f"modern pop, upbeat energy, "
        f"background music for social media video, "
        f"no lyrics, instrumental, "
        f"TikTok/Instagram Reels style, "
        f"professional production, "
        f"30-60 seconds"
    )


def _submit_music(prompt: str, api_key: str) -> str:
    """Submit a Suno music generation job. Returns task_id."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "make_instrumental": True,
        "model": "chirp-v4-5",   # Suno V4.5
        "wait_audio": False,
    }
    r = requests.post(SUNO_SUBMIT_URL, headers=headers, json=payload, timeout=30)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Kie.ai submit error {r.status_code}: {r.text[:200]}")

    data = r.json()
    # Response structure: {"data": {"task_id": "..."}} or {"task_id": "..."}
    task_id = (
        data.get("data", {}).get("taskId")
        or data.get("data", {}).get("task_id")
        or data.get("taskId")
        or data.get("task_id")
        or data.get("data", {}).get("id")
    )
    if not task_id:
        raise RuntimeError(f"No task_id in response: {data}")
    return str(task_id)


def _poll_music(task_id: str, api_key: str, console) -> list[dict]:
    """Poll until music is ready. Returns list of clip dicts with audio_url."""
    headers = {"Authorization": f"Bearer {api_key}"}
    elapsed = 0

    while elapsed < MAX_WAIT_SECS:
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL

        r = requests.get(
            SUNO_QUERY_URL,
            headers=headers,
            params={"taskId": task_id},
            timeout=30,
        )
        if r.status_code != 200:
            console.print(f"  [dim]  → poll {elapsed}s: HTTP {r.status_code}[/dim]")
            continue

        data = r.json()
        clips = (
            data.get("data", {}).get("clips")
            or data.get("clips")
            or []
        )

        if isinstance(clips, dict):
            clips = list(clips.values())

        ready_clips = [c for c in clips if c.get("audio_url") or c.get("stream_audio_url")]
        if ready_clips:
            return ready_clips

        status = data.get("data", {}).get("status") or data.get("status", "pending")
        console.print(f"  [dim]  → {elapsed}s: {status}...[/dim]")

    raise TimeoutError(f"Music generation timed out after {MAX_WAIT_SECS}s")


def _download_mp3(url: str, dest: Path) -> None:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    dest.write_bytes(r.content)


def run(ctx: dict) -> dict:
    brand: str    = ctx["brand"]
    run_dir: Path = ctx["run_dir"]
    console       = ctx["console"]

    # Load guion for mood
    guion_path = run_dir / "guion.json"
    guion = {}
    if guion_path.exists():
        guion = json.loads(guion_path.read_text(encoding="utf-8"))

    # Load profile for visual context
    profile_path = run_dir / "brand_profile.json"
    profile = {}
    if profile_path.exists():
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
    elif (ctx["brands_dir"] / brand / "brand_profile.json").exists():
        profile = json.loads((ctx["brands_dir"] / brand / "brand_profile.json").read_text(encoding="utf-8"))

    api_key = os.getenv("KIE_API_KEY")
    if not api_key:
        raise EnvironmentError("KIE_API_KEY not set")

    prompt = _build_music_prompt(guion, profile)
    console.print(f"  [dim]Music prompt: {prompt[:80]}...[/dim]")
    console.print(f"  Generando música con Suno V4.5...")

    task_id = _submit_music(prompt, api_key)
    console.print(f"  [dim]  → task_id: {task_id} — esperando...[/dim]")

    clips = _poll_music(task_id, api_key, console)

    # Take the first clip
    clip = clips[0]
    audio_url = clip.get("audio_url") or clip.get("stream_audio_url")

    out_path = run_dir / "music.mp3"
    _download_mp3(audio_url, out_path)

    file_size_kb = out_path.stat().st_size // 1024
    console.print(f"  [green]✓[/green] music.mp3 ({file_size_kb} KB) — {clip.get('title', '')}")

    return {
        "status": "ok",
        "cost_usd": 0.06,
        "music_path": str(out_path),
        "music_url": audio_url,
        "title": clip.get("title", ""),
        "prompt": prompt,
    }
