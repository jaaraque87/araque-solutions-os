#!/usr/bin/env python3
"""Headless, deterministic adapter for one TAO LTX Director scene."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import mimetypes
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path


FPS = 24
DIRECTOR_NODE = "131"
SEED_NODE = "30"
SAVE_NODE = "37"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_request(url: str, data: bytes | None = None, headers: dict | None = None) -> dict:
    request = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def upload(base_url: str, path: Path) -> str:
    boundary = f"----araque-{uuid.uuid4().hex}"
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    fields = [("subfolder", "whatdreamscost"), ("overwrite", "true")]
    chunks = [
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="image"; filename="{path.name}"\r\n'.encode(),
        f"Content-Type: {mime}\r\n\r\n".encode(),
        path.read_bytes(),
        b"\r\n",
    ]
    for key, value in fields:
        chunks.extend([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode(),
            value.encode(),
            b"\r\n",
        ])
    chunks.append(f"--{boundary}--\r\n".encode())
    result = json_request(
        f"{base_url}/upload/image",
        b"".join(chunks),
        {"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    folder = result.get("subfolder", "")
    return f"{folder}/{result['name']}" if folder else result["name"]


def prompt_text(path: Path, key: str) -> str:
    prefix = f"{key}="
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    raise KeyError(f"Missing {key} in {path}")


def build_workflow(template: dict, *, image_file: str, audio_file: str, prompt: str,
                   seconds: float, seed: int, width: int, height: int, scene_id: str) -> tuple[dict, int]:
    workflow = json.loads(json.dumps(template))
    # Never trim the tail of voice whose duration is not frame-exact.
    frames = max(1, math.ceil(seconds * FPS))
    timeline = {
        "mainTrackEnabled": True,
        "audioTrackEnabled": True,
        "motionTrackEnabled": False,
        "showFilenames": True,
        "overrideAudio": False,
        "inpaint_audio": True,
        "global_prompt": prompt,
        "retakeMode": False,
        "normalStartFrame": 0,
        "normalDurationFrames": frames,
        "segments": [{
            "id": f"{scene_id}-visual",
            "start": 0,
            "length": frames,
            "prompt": prompt,
            "type": "image",
            "imageFile": image_file,
            "guideStrength": 1.0,
        }],
        "motionSegments": [],
        "audioSegments": [{
            "id": f"{scene_id}-audio",
            "start": 0,
            "length": frames,
            "trimStart": 0,
            "audioDurationFrames": frames,
            "audioFile": audio_file,
            "fileName": Path(audio_file).name,
        }],
    }
    director = workflow[DIRECTOR_NODE]["inputs"]
    director.update({
        "start_second": 0,
        "end_second": frames / FPS,
        "duration_seconds": frames / FPS,
        "start_frame": 0,
        "end_frame": frames,
        "duration_frames": frames,
        "timeline_data": json.dumps(timeline, ensure_ascii=False, separators=(",", ":")),
        "local_prompts": prompt,
        "segment_lengths": str(frames),
        "guide_strength": "1.00",
        "use_custom_audio": True,
        "inpaint_audio": True,
        "custom_width": width,
        "custom_height": height,
        "resize_method": "maintain aspect ratio",
    })
    workflow[SEED_NODE]["inputs"]["noise_seed"] = seed
    workflow[SAVE_NODE]["inputs"]["filename_prefix"] = f"video/TAO_{scene_id.upper()}"
    return workflow, frames


def output_items(history: dict) -> list[dict]:
    result = []
    for node in history.get("outputs", {}).values():
        for value in node.values():
            if isinstance(value, list):
                result.extend(item for item in value if isinstance(item, dict) and item.get("filename"))
    return result


def wait_for_history(base_url: str, prompt_id: str, timeout: int) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        payload = json_request(f"{base_url}/history/{prompt_id}")
        if prompt_id in payload:
            history = payload[prompt_id]
            if history.get("status", {}).get("status_str") == "error":
                raise RuntimeError(json.dumps(history["status"], ensure_ascii=False))
            if output_items(history):
                return history
        time.sleep(5)
    raise TimeoutError(prompt_id)


def download(base_url: str, item: dict, output: Path) -> None:
    query = urllib.parse.urlencode({
        "filename": item["filename"],
        "subfolder": item.get("subfolder", ""),
        "type": item.get("type", "output"),
    })
    output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(f"{base_url}/view?{query}", timeout=300) as response:
        output.write_bytes(response.read())


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render one TAO talking-head scene")
    parser.add_argument("--tunnel", required=True)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--prompts", required=True, type=Path)
    parser.add_argument("--prompt-key", required=True)
    parser.add_argument("--duration", required=True, type=float)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seed", type=int, default=20260713)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=1152)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = arguments()
    for path in (args.template, args.image, args.audio, args.prompts):
        if not path.is_file():
            raise FileNotFoundError(path)
    base_url = args.tunnel.rstrip("/")
    prompt = prompt_text(args.prompts, args.prompt_key)
    image_file = f"whatdreamscost/{args.image.name}" if args.dry_run else upload(base_url, args.image)
    audio_file = f"whatdreamscost/{args.audio.name}" if args.dry_run else upload(base_url, args.audio)
    workflow, frames = build_workflow(
        read_json(args.template), image_file=image_file, audio_file=audio_file, prompt=prompt,
        seconds=args.duration, seed=args.seed, width=args.width, height=args.height,
        scene_id=args.scene_id,
    )
    run_dir = args.output.parent / f"{args.output.stem}.tao"
    manifest = {
        "contract_version": 1,
        "engine": "tao-ltx-director-v2",
        "scene_id": args.scene_id,
        "seed": args.seed,
        "fps": FPS,
        "frames": frames,
        "resolution": [args.width, args.height],
        "image": {"path": str(args.image.resolve()), "sha256": file_hash(args.image), "remote": image_file},
        "audio": {"path": str(args.audio.resolve()), "sha256": file_hash(args.audio), "remote": audio_file},
        "prompt": prompt,
    }
    write_json(run_dir / "prompt.json", workflow)
    write_json(run_dir / "manifest.json", manifest)
    if args.dry_run:
        print(run_dir / "prompt.json")
        return 0
    queued = json_request(
        f"{base_url}/prompt",
        json.dumps({"prompt": workflow, "client_id": f"araque-{uuid.uuid4().hex}"}).encode(),
        {"Content-Type": "application/json"},
    )
    manifest["prompt_id"] = queued["prompt_id"]
    write_json(run_dir / "manifest.json", manifest)
    history = wait_for_history(base_url, queued["prompt_id"], args.timeout)
    write_json(run_dir / "history.json", history)
    videos = [item for item in output_items(history) if Path(item["filename"]).suffix.lower() in {".mp4", ".webm", ".mov"}]
    if not videos:
        raise RuntimeError("TAO returned no video")
    download(base_url, videos[0], args.output)
    manifest["output"] = {"path": str(args.output.resolve()), "sha256": file_hash(args.output)}
    write_json(run_dir / "manifest.json", manifest)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
