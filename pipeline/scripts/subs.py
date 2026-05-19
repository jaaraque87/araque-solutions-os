"""
Step 11 — Subtitles + Finishing
=================================
Burns subtitles into the master video and applies final color/format treatment.

Modes (configurable via SUBS_MODE env var):
  "local"    — Generate SRT from guion.json + burn with FFmpeg (free)
  "submagic" — Upload to Submagic API for styled auto-captions (paid, $0.10/video)

Input:   run_dir/master.mp4
         run_dir/guion.json
Output:  run_dir/final.mp4
         run_dir/subtitles.srt  (always generated)

Cost: $0.00 (local) or ~$0.10 (Submagic)
"""

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

import requests

SUBMAGIC_UPLOAD_URL = "https://api.submagic.co/api/v1/projects/upload"
SUBMAGIC_STATUS_URL = "https://api.submagic.co/api/v1/projects/{project_id}"
SUBMAGIC_EXPORT_URL = "https://api.submagic.co/api/v1/projects/{project_id}/export"

MAX_WAIT_SECS  = 300
POLL_INTERVAL  = 10


# ── SRT generation from guion ─────────────────────────────────────────────────

def _seconds_to_srt_time(seconds: float) -> str:
    """Convert float seconds to SRT timestamp format HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _generate_srt(scenes: list[dict]) -> str:
    """Build an SRT file from guion scenes."""
    lines = []
    cursor = 0.0

    for i, scene in enumerate(scenes, 1):
        caption  = scene.get("caption") or scene.get("dialogue", "")[:60]
        duration = float(scene.get("duration_s", 8))

        # Trim to max 2 lines of ~40 chars each
        words = caption.split()
        if len(caption) > 40:
            mid = len(words) // 2
            caption = " ".join(words[:mid]) + "\n" + " ".join(words[mid:])

        start = _seconds_to_srt_time(cursor + 0.2)
        end   = _seconds_to_srt_time(cursor + duration - 0.3)

        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(caption)
        lines.append("")

        cursor += duration

    return "\n".join(lines)


# ── Local burn-in ─────────────────────────────────────────────────────────────

def _burn_subs_local(video_path: Path, srt_path: Path, out_path: Path) -> None:
    """Burn SRT subtitles into video using FFmpeg."""
    # Escape path for FFmpeg subtitle filter (Windows paths need special handling)
    srt_posix = srt_path.as_posix().replace(":", "\\:")

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(video_path),
        "-vf", (
            f"subtitles='{srt_posix}':"
            f"force_style='FontName=Arial,FontSize=14,PrimaryColour=&Hffffff,"
            f"OutlineColour=&H000000,Outline=2,Shadow=1,"
            f"Alignment=2,MarginV=60,Bold=1'"
        ),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "21",
        "-c:a", "copy",
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg subtitle burn failed:\n{result.stderr}")


# ── Submagic API ──────────────────────────────────────────────────────────────

def _submagic_upload(video_path: Path, api_key: str) -> str:
    """Upload video to Submagic and return project_id."""
    headers = {"Authorization": f"Bearer {api_key}"}
    with video_path.open("rb") as f:
        files = {"file": (video_path.name, f, "video/mp4")}
        r = requests.post(SUBMAGIC_UPLOAD_URL, headers=headers, files=files, timeout=120)

    if r.status_code not in (200, 201):
        raise RuntimeError(f"Submagic upload error {r.status_code}: {r.text[:200]}")

    data = r.json()
    project_id = data.get("project_id") or data.get("id") or data.get("data", {}).get("id")
    if not project_id:
        raise RuntimeError(f"No project_id in Submagic response: {data}")
    return str(project_id)


def _submagic_wait_and_download(project_id: str, out_path: Path,
                                api_key: str, console) -> None:
    """Poll Submagic until ready, then download the final video."""
    headers = {"Authorization": f"Bearer {api_key}"}
    status_url = SUBMAGIC_STATUS_URL.format(project_id=project_id)
    elapsed = 0

    while elapsed < MAX_WAIT_SECS:
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL

        r = requests.get(status_url, headers=headers, timeout=30)
        if r.status_code != 200:
            continue

        data = r.json()
        status = (data.get("status") or data.get("data", {}).get("status", "processing")).lower()
        console.print(f"  [dim]  → Submagic: {elapsed}s — {status}[/dim]")

        if status in ("completed", "done", "finished"):
            # Get download URL
            export_url = SUBMAGIC_EXPORT_URL.format(project_id=project_id)
            r2 = requests.get(export_url, headers=headers, timeout=30)
            if r2.status_code == 200:
                export_data = r2.json()
                download_url = (
                    export_data.get("url")
                    or export_data.get("download_url")
                    or export_data.get("data", {}).get("url")
                )
                if download_url:
                    response = requests.get(download_url, timeout=300, stream=True)
                    with out_path.open("wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    return
            raise RuntimeError(f"Could not get download URL from Submagic: {r2.text[:200]}")

        if status in ("failed", "error"):
            raise RuntimeError(f"Submagic processing failed: {data}")

    raise TimeoutError(f"Submagic timed out after {MAX_WAIT_SECS}s")


# ── Main ──────────────────────────────────────────────────────────────────────

def run(ctx: dict) -> dict:
    run_dir: Path = ctx["run_dir"]
    console       = ctx["console"]

    master_path = run_dir / "master.mp4"
    if not master_path.exists():
        raise FileNotFoundError("master.mp4 not found. Run step 10 first.")

    # Load guion for subtitle text
    guion_path = run_dir / "guion.json"
    scenes = []
    if guion_path.exists():
        guion = json.loads(guion_path.read_text(encoding="utf-8"))
        scenes = guion.get("scenes", [])

    # Always generate SRT
    srt_content = _generate_srt(scenes)
    srt_path = run_dir / "subtitles.srt"
    srt_path.write_text(srt_content, encoding="utf-8")
    console.print(f"  [green]✓[/green] subtitles.srt generado ({len(scenes)} escenas)")

    final_path = run_dir / "final.mp4"
    subs_mode  = os.getenv("SUBS_MODE", "local").lower()

    if subs_mode == "submagic":
        api_key = os.getenv("SUBMAGIC_API_KEY", "")
        if not api_key:
            console.print("[yellow]  ⚠  SUBMAGIC_API_KEY no definida — usando modo local[/yellow]")
            subs_mode = "local"

    if subs_mode == "submagic":
        console.print(f"  Subiendo a Submagic para captions automáticos...")
        project_id = _submagic_upload(master_path, api_key)
        console.print(f"  [dim]  → project_id: {project_id}[/dim]")
        _submagic_wait_and_download(project_id, final_path, api_key, console)
        cost = 0.10
        method = "submagic"
    else:
        # Local burn-in with FFmpeg
        console.print(f"  Quemando subtítulos con FFmpeg (modo local)...")
        try:
            _burn_subs_local(master_path, srt_path, final_path)
            cost = 0.0
            method = "local_ffmpeg"
        except RuntimeError as e:
            # If subtitle burn fails (e.g. libass not available), just copy
            console.print(f"  [yellow]⚠  Subtitle burn falló: {e}[/yellow]")
            console.print(f"  [dim]  → Copiando master.mp4 como final.mp4[/dim]")
            import shutil
            shutil.copy2(master_path, final_path)
            cost = 0.0
            method = "copy_no_subs"

    file_size_mb = final_path.stat().st_size // (1024 * 1024)
    console.print(f"  [green]✓[/green] final.mp4 ({file_size_mb} MB) — método: {method}")
    console.print(f"\n  [bold green]🎬 Video listo:[/bold green] {final_path}")
    console.print(f"  [dim]Siguiente: revisión manual → publicar[/dim]")

    return {
        "status": "ok",
        "cost_usd": cost,
        "final_path": str(final_path),
        "srt_path": str(srt_path),
        "method": method,
        "file_size_mb": file_size_mb,
    }
