"""Deterministic QA and patch preparation for realistic UGC renders."""

from __future__ import annotations

import json
import os
import re
import subprocess
import urllib.request
import uuid
from pathlib import Path
from typing import Any

from .core import relative_artifact, resolve_secret, set_stage


def _run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, capture_output=True, text=True, check=check)
    except FileNotFoundError as exc:
        raise RuntimeError(f"required command not found: {command[0]}") from exc


def probe_video(video: Path) -> dict[str, Any]:
    result = _run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=index,codec_type,width,height,r_frame_rate",
            "-of",
            "json",
            str(video),
        ]
    )
    data = json.loads(result.stdout)
    video_stream = next(
        (stream for stream in data.get("streams", []) if stream.get("codec_type") == "video"),
        {},
    )
    audio_streams = [
        stream for stream in data.get("streams", []) if stream.get("codec_type") == "audio"
    ]
    return {
        "duration_seconds": round(float(data.get("format", {}).get("duration", 0.0)), 3),
        "width": video_stream.get("width"),
        "height": video_stream.get("height"),
        "frame_rate": video_stream.get("r_frame_rate"),
        "has_audio": bool(audio_streams),
    }


def make_contact_sheet(video: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    _run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(video),
            "-vf",
            "fps=1,scale=270:-1,tile=6x5",
            "-frames:v",
            "1",
            str(output),
        ]
    )


def measure_loudness(video: Path) -> dict[str, float | None]:
    result = _run(
        [
            "ffmpeg",
            "-nostats",
            "-i",
            str(video),
            "-af",
            "loudnorm=print_format=json",
            "-f",
            "null",
            os.devnull,
        ],
        check=False,
    )
    combined = result.stderr + "\n" + result.stdout
    matches = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", combined, flags=re.DOTALL)
    if not matches:
        return {"integrated_lufs": None, "true_peak_dbtp": None}
    parsed = json.loads(matches[-1])

    def number(value: Any) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    return {
        "integrated_lufs": number(parsed.get("input_i")),
        "true_peak_dbtp": number(parsed.get("input_tp")),
    }


def transcribe_openai(video: Path, output: Path, env_path: Path) -> Path:
    key = resolve_secret("OPENAI_API_KEY", env_path)
    if not key:
        raise RuntimeError(f"OPENAI_API_KEY is missing from environment or {env_path}")
    wav = output.parent / "transcription-input.wav"
    _run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(video),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            str(wav),
        ]
    )
    boundary = f"----araquetranscribe{uuid.uuid4().hex}"
    audio = wav.read_bytes()
    parts = [
        _multipart_field(boundary, "model", "whisper-1"),
        _multipart_field(boundary, "language", "es"),
        _multipart_field(boundary, "response_format", "verbose_json"),
        (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
            f"filename=\"qa.wav\"\r\nContent-Type: audio/wav\r\n\r\n"
        ).encode("utf-8"),
        audio,
        f"\r\n--{boundary}--\r\n".encode("utf-8"),
    ]
    request = urllib.request.Request(
        "https://api.openai.com/v1/audio/transcriptions",
        data=b"".join(parts),
        method="POST",
    )
    request.add_header("Authorization", f"Bearer {key}")
    request.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    with urllib.request.urlopen(request, timeout=300) as response:
        data = json.loads(response.read())
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    wav.unlink(missing_ok=True)
    return output


def _multipart_field(boundary: str, name: str, value: str) -> bytes:
    return (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n"
        f"{value}\r\n"
    ).encode("utf-8")


def run_qa(
    *,
    run_dir: Path,
    video: Path,
    env_path: Path,
    transcribe: bool = False,
) -> dict[str, Any]:
    qa_dir = run_dir / "qa"
    qa_dir.mkdir(parents=True, exist_ok=True)
    specs = probe_video(video)
    specs.update(measure_loudness(video))
    expected_vertical = specs["width"] == 720 and specs["height"] == 1280
    expected_duration = 29.0 <= specs["duration_seconds"] <= 31.5
    specs["automated_checks"] = {
        "vertical_720p": expected_vertical,
        "duration_near_30s": expected_duration,
        "audio_stream_present": specs["has_audio"],
    }
    specs["automated_pass"] = all(specs["automated_checks"].values())
    report = qa_dir / "report.json"
    report.write_text(json.dumps(specs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    contact_sheet = qa_dir / "contact-sheet.png"
    make_contact_sheet(video, contact_sheet)
    artifacts = [report, contact_sheet]
    if transcribe:
        artifacts.append(transcribe_openai(video, qa_dir / "transcript.json", env_path))
    status = "ready_for_review" if specs["automated_pass"] else "failed"
    set_stage(
        run_dir,
        "qa",
        status=status,
        artifacts=[relative_artifact(run_dir, path) for path in artifacts],
        detail=(
            "Automated checks passed. Human review still required: identity, duplicate people, "
            "object counts, product physics, label integrity, dialogue, and unwanted text."
            if specs["automated_pass"]
            else "One or more automated video checks failed; inspect qa/report.json."
        ),
    )
    return specs


def detect_scene_cuts(video: Path, threshold: float = 0.35) -> list[float]:
    result = _run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(video),
            "-vf",
            f"select=gt(scene\\,{threshold}),showinfo",
            "-an",
            "-f",
            "null",
            os.devnull,
        ],
        check=False,
    )
    return [float(value) for value in re.findall(r"pts_time:([0-9.]+)", result.stderr)]


def prepare_patch(run_dir: Path, video: Path, shot: int, start: float, end: float) -> Path:
    if shot < 1 or start < 0 or end <= start:
        raise ValueError("invalid shot or time range")
    patch_dir = run_dir / "qa" / "patches" / f"shot-{shot:02d}"
    patch_dir.mkdir(parents=True, exist_ok=True)
    for name, timestamp in (("anchor-open.png", start), ("anchor-context.png", min(end, start + 0.5))):
        _run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-ss",
                f"{timestamp:.3f}",
                "-i",
                str(video),
                "-frames:v",
                "1",
                str(patch_dir / name),
            ]
        )
    manifest = {
        "shot": shot,
        "source_video": relative_artifact(run_dir, video),
        "start_seconds": start,
        "end_seconds": end,
        "recommended_generation_seconds": min(30, max(4, int(end - start + 1.99))),
        "warning": "Check transcript timing before replacement; spoken audio may cross the visual cut.",
        "references_in_order": ["anchor-open.png", "anchor-context.png", "product source asset"],
    }
    (patch_dir / "patch.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return patch_dir
