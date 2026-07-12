#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
import time

import fal_client
import requests


IMAGE_TO_VIDEO = "bytedance/seedance-2.0/image-to-video"
REFERENCE_TO_VIDEO = "bytedance/seedance-2.0/reference-to-video"
URL_SCHEMES = {"http", "https", "data"}
RESOLUTIONS = {"480p", "720p", "1080p"}
DURATIONS = {"auto", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"}
ASPECT_RATIOS = {"auto", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_url(value: str) -> bool:
    scheme = urllib.parse.urlparse(value).scheme.lower()
    return scheme in URL_SCHEMES


def coerce_file(value: str, *, resolve_uploads: bool) -> str:
    if is_url(value):
        return value
    path = Path(value).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    if not resolve_uploads:
        return str(path)
    return fal_client.upload_file(str(path))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Seedance 2.0 on fal with payload preview support.")
    parser.add_argument("--endpoint", choices=("image-to-video", "reference-to-video"), required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--image", action="append", default=[], help="Local path or URL. For image-to-video the first image is required and becomes image_url. For reference-to-video this maps to image_urls.")
    parser.add_argument("--end-image", help="Optional end image path or URL for image-to-video.")
    parser.add_argument("--video", action="append", default=[], help="Reference video path or URL for reference-to-video.")
    parser.add_argument("--audio", action="append", default=[], help="Reference audio path or URL for reference-to-video.")
    parser.add_argument("--resolution", default="720p", choices=sorted(RESOLUTIONS))
    parser.add_argument("--duration", default="auto", choices=sorted(DURATIONS))
    parser.add_argument("--aspect-ratio", default="9:16", choices=sorted(ASPECT_RATIOS))
    parser.add_argument("--seed", type=int)
    parser.add_argument("--generate-audio", dest="generate_audio", action="store_true")
    parser.add_argument("--no-generate-audio", dest="generate_audio", action="store_false")
    parser.set_defaults(generate_audio=False)
    parser.add_argument("--end-user-id")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def endpoint_id(short_name: str) -> str:
    if short_name == "image-to-video":
        return IMAGE_TO_VIDEO
    return REFERENCE_TO_VIDEO


def build_payload(args: argparse.Namespace, *, resolve_uploads: bool) -> dict:
    payload: dict[str, object] = {
        "prompt": args.prompt,
        "resolution": args.resolution,
        "duration": args.duration,
        "aspect_ratio": args.aspect_ratio,
        "generate_audio": bool(args.generate_audio),
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.end_user_id:
        payload["end_user_id"] = args.end_user_id

    image_urls = [coerce_file(item, resolve_uploads=resolve_uploads) for item in args.image]

    if args.endpoint == "image-to-video":
        if not image_urls:
            raise ValueError("image-to-video requires at least one --image")
        payload["image_url"] = image_urls[0]
        if args.end_image:
            payload["end_image_url"] = coerce_file(args.end_image, resolve_uploads=resolve_uploads)
        return payload

    video_urls = [coerce_file(item, resolve_uploads=resolve_uploads) for item in args.video]
    audio_urls = [coerce_file(item, resolve_uploads=resolve_uploads) for item in args.audio]
    if image_urls:
        payload["image_urls"] = image_urls
    if video_urls:
        payload["video_urls"] = video_urls
    if audio_urls:
        if not image_urls and not video_urls:
            raise ValueError("reference-to-video with audio requires at least one image or video reference")
        payload["audio_urls"] = audio_urls
    return payload


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, timeout=900, stream=True) as response:
        response.raise_for_status()
        with dest.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)


def status_name(status: object) -> str:
    return type(status).__name__


def status_logs(status: object) -> list[str]:
    logs = getattr(status, "logs", None) or []
    messages: list[str] = []
    for log in logs:
        message = getattr(log, "message", None)
        if message:
            messages.append(str(message))
    return messages


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    preview_payload = build_payload(args, resolve_uploads=False)
    preview = {
        "generated_at": now_iso(),
        "endpoint": endpoint_id(args.endpoint),
        "mode": args.endpoint,
        "payload": preview_payload,
        "dry_run": bool(args.dry_run),
    }
    save_json(out_dir / "seedance_request_preview.json", preview)
    (out_dir / "seedance_prompt.txt").write_text(args.prompt, encoding="utf-8")

    print(json.dumps(preview, indent=2, ensure_ascii=False))
    if args.dry_run:
        return 0

    fal_key = os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY")
    if not fal_key:
        raise SystemExit("Missing FAL_KEY or FAL_API_KEY")
    os.environ["FAL_KEY"] = fal_key

    payload = build_payload(args, resolve_uploads=True)
    meta = {
        "generated_at": now_iso(),
        "endpoint": endpoint_id(args.endpoint),
        "mode": args.endpoint,
        "payload": payload,
        "dry_run": False,
    }
    save_json(out_dir / "seedance_request.json", meta)

    handle = fal_client.submit(endpoint_id(args.endpoint), arguments=payload)
    print(json.dumps({"event": "submitted", "request_id": handle.request_id}, ensure_ascii=False), flush=True)

    last_status = None
    seen_logs: set[str] = set()
    while True:
        status = handle.status(with_logs=True)
        name = status_name(status)
        if name != last_status:
            print(json.dumps({"event": "queue.update", "status": name}, ensure_ascii=False), flush=True)
            last_status = name

        for message in status_logs(status):
            if message not in seen_logs:
                print(json.dumps({"event": "queue.log", "message": message}, ensure_ascii=False), flush=True)
                seen_logs.add(message)

        if name == "Completed":
            break
        time.sleep(2)

    result = handle.get()
    save_json(out_dir / "seedance_result.json", result)
    video = (result or {}).get("video") or {}
    video_url = video.get("url")
    if not video_url:
        raise RuntimeError("Seedance response did not include video.url")
    download(video_url, out_dir / "seedance_output.mp4")
    print(json.dumps({"event": "done", "video": str(out_dir / 'seedance_output.mp4')}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
