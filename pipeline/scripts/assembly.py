"""
Step 10 — Final Assembly (FFmpeg)
===================================
Assembles all video clips and background music into a single master video.

Pipeline:
  1. Collect clips in order: sync_scene_N > kling_scene_N (prefer synced)
  2. Collect per-scene audio: voice_scene_N > tts_scene_N
  3. If clips already have audio (sync), keep it; otherwise mux voice audio
  4. Concatenate all clips
  5. Mix background music at low volume (-20dB) under voice
  6. Add fade in/out transitions
  7. Output 9:16 vertical video (1080x1920 or 576x1024)

Input:   run_dir/sync_scene_N.mp4   OR  run_dir/kling_scene_N.mp4
         run_dir/voice_scene_N.*    OR  run_dir/tts_scene_N.*
         run_dir/music.mp3          (optional)
         run_dir/guion.json
Output:  run_dir/master.mp4

Cost: $0.00 (local FFmpeg)
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path


def _find_clips_in_order(run_dir: Path, num_scenes: int) -> list[Path]:
    """Return ordered list of best available clips."""
    clips = []
    for sid in range(1, num_scenes + 1):
        for pattern in [f"sync_scene_{sid}.mp4", f"kling_scene_{sid}.mp4"]:
            p = run_dir / pattern
            if p.exists():
                clips.append(p)
                break
    return clips


def _find_audio_for_scene(run_dir: Path, sid: int) -> Path | None:
    for name in [f"voice_scene_{sid}.mp3", f"voice_scene_{sid}.wav",
                 f"tts_scene_{sid}.wav", f"tts_scene_{sid}.mp3"]:
        p = run_dir / name
        if p.exists():
            return p
    return None


def _ffmpeg(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + list(args)
    return subprocess.run(cmd, capture_output=True, check=check)


def _has_audio_stream(video_path: Path) -> bool:
    """Check if a video file has an audio track."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(video_path)],
        capture_output=True, text=True,
    )
    return "audio" in r.stdout


def _mux_audio_to_clip(video_path: Path, audio_path: Path, out_path: Path) -> None:
    """Replace/add audio track from audio_path to video_path."""
    _ffmpeg(
        "-i", str(video_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "128k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        str(out_path),
    )


def _concat_clips(clip_paths: list[Path], out_path: Path) -> None:
    """Concatenate clips using FFmpeg concat demuxer."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                    delete=False, encoding="utf-8") as f:
        for p in clip_paths:
            f.write(f"file '{p.as_posix()}'\n")
        list_file = f.name

    try:
        _ffmpeg(
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            str(out_path),
        )
    finally:
        os.unlink(list_file)


def _mix_music(video_path: Path, music_path: Path, out_path: Path,
               music_volume: float = 0.12) -> None:
    """
    Mix background music under the voice track.
    music_volume: 0.0-1.0 (0.12 = -18dB approx)
    """
    _ffmpeg(
        "-i", str(video_path),
        "-stream_loop", "-1",    # loop music if shorter than video
        "-i", str(music_path),
        "-filter_complex",
        f"[0:a]volume=1.0[voice];"
        f"[1:a]volume={music_volume}[music];"
        f"[voice][music]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(out_path),
    )


def _add_fade(video_path: Path, out_path: Path,
              fade_in: float = 0.3, fade_out: float = 0.5) -> None:
    """Add fade in/out to both video and audio."""
    # Get duration
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)],
        capture_output=True, text=True,
    )
    try:
        duration = float(r.stdout.strip())
    except (ValueError, AttributeError):
        duration = 30.0  # fallback

    fade_out_start = max(0, duration - fade_out)

    _ffmpeg(
        "-i", str(video_path),
        "-vf", f"fade=t=in:st=0:d={fade_in},fade=t=out:st={fade_out_start:.2f}:d={fade_out}",
        "-af", f"afade=t=in:st=0:d={fade_in},afade=t=out:st={fade_out_start:.2f}:d={fade_out}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        str(out_path),
    )


def run(ctx: dict) -> dict:
    run_dir: Path = ctx["run_dir"]
    console       = ctx["console"]

    # Check ffmpeg available
    check = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    if check.returncode != 0:
        raise EnvironmentError("ffmpeg not found in PATH. Install: winget install Gyan.FFmpeg")

    # Load guion
    guion_path = run_dir / "guion.json"
    num_scenes = 6
    if guion_path.exists():
        guion = json.loads(guion_path.read_text(encoding="utf-8"))
        num_scenes = guion.get("num_scenes", 6)

    clips = _find_clips_in_order(run_dir, num_scenes)
    if not clips:
        raise FileNotFoundError("No video clips found. Run step 07 (or 08) first.")

    console.print(f"  {len(clips)} clips encontrados")
    music_path = run_dir / "music.mp3"
    has_music = music_path.exists()

    # Step 1: Ensure each clip has audio (mux if needed)
    clips_with_audio: list[Path] = []
    tmp_dir = run_dir / "_tmp_assembly"
    tmp_dir.mkdir(exist_ok=True)

    for clip in clips:
        # Detect scene id from filename
        stem = clip.stem  # e.g. "sync_scene_2" or "kling_scene_3"
        sid_str = stem.split("_")[-1]
        try:
            sid = int(sid_str)
        except ValueError:
            sid = 0

        if _has_audio_stream(clip):
            clips_with_audio.append(clip)
            console.print(f"  [dim]  {clip.name} — audio ✓[/dim]")
        else:
            audio_path = _find_audio_for_scene(run_dir, sid)
            if audio_path:
                muxed = tmp_dir / f"muxed_{clip.name}"
                _mux_audio_to_clip(clip, audio_path, muxed)
                clips_with_audio.append(muxed)
                console.print(f"  [dim]  {clip.name} + {audio_path.name} → muxed[/dim]")
            else:
                clips_with_audio.append(clip)
                console.print(f"  [yellow]  {clip.name} — sin audio[/yellow]")

    # Step 2: Concatenate all clips
    concat_path = tmp_dir / "concat.mp4"
    console.print(f"  Concatenando {len(clips_with_audio)} clips...")
    _concat_clips(clips_with_audio, concat_path)

    # Step 3: Mix music (if available)
    if has_music:
        mixed_path = tmp_dir / "mixed.mp4"
        music_vol = float(os.getenv("MUSIC_VOLUME", "0.12"))
        console.print(f"  Mezclando música (vol {music_vol})...")
        _mix_music(concat_path, music_path, mixed_path, music_volume=music_vol)
        pre_fade = mixed_path
    else:
        pre_fade = concat_path
        console.print(f"  [yellow]  Sin music.mp3 — omitiendo mezcla de música[/yellow]")

    # Step 4: Add fade in/out → final master
    master_path = run_dir / "master.mp4"
    console.print(f"  Añadiendo fade in/out → master.mp4...")
    _add_fade(pre_fade, master_path)

    file_size_mb = master_path.stat().st_size // (1024 * 1024)
    console.print(f"  [green]✓[/green] master.mp4 ({file_size_mb} MB) → {master_path}")

    # Cleanup temp files
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)

    return {
        "status": "ok",
        "cost_usd": 0.0,
        "master_path": str(master_path),
        "num_clips": len(clips_with_audio),
        "has_music": has_music,
    }
