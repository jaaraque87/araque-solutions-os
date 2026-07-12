#!/usr/bin/env python3
"""Small Krea API helper for Krea 2 Large workflows.

The script intentionally never contains a real API key. It reads
KREA_API_KEY/KREA_API_TOKEN from the environment or ~/.config/krea/env.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


API_BASE = "https://api.krea.ai"
ENV_FILE = Path.home() / ".config" / "krea" / "env"
TERMINAL_STATUSES = {"completed", "failed", "cancelled"}


def load_env_file() -> None:
    if not ENV_FILE.exists():
        return
    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key in os.environ:
            continue
        try:
            parts = shlex.split(value, posix=True)
            parsed = parts[0] if parts else ""
        except ValueError:
            parsed = value.strip().strip("'\"")
        os.environ[key] = parsed


def api_key() -> str:
    load_env_file()
    key = os.environ.get("KREA_API_KEY") or os.environ.get("KREA_API_TOKEN")
    if not key:
        raise SystemExit(
            "Missing KREA_API_KEY. Run: source ~/.config/krea/env "
            "or set KREA_API_KEY in the environment."
        )
    return key


def request_json(
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
    extra_headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    url = f"{API_BASE}{path}"
    if query:
        clean_query = {k: v for k, v in query.items() if v is not None}
        if clean_query:
            url = f"{url}?{urllib.parse.urlencode(clean_query)}"

    data = None
    headers = {"Authorization": f"Bearer {api_key()}"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if extra_headers:
        headers.update(extra_headers)

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Krea API error {exc.code}: {details}") from exc

    if not payload:
        return {}
    return json.loads(payload)


def parse_weighted(value: str, default_strength: float) -> dict[str, Any]:
    if "=" in value:
        item_id, strength_text = value.rsplit("=", 1)
        return {"id": item_id, "strength": float(strength_text)}
    return {"id": value, "strength": default_strength}


def parse_ref(value: str, default_strength: float) -> dict[str, Any]:
    if "=" in value:
        url, strength_text = value.rsplit("=", 1)
        return {"url": url, "strength": float(strength_text)}
    return {"url": value, "strength": default_strength}


def cmd_generate(args: argparse.Namespace) -> None:
    path_by_model = {
        "large": "/generate/image/krea/krea-2/large",
        "medium": "/generate/image/krea/krea-2/medium",
        "medium-turbo": "/generate/image/krea/krea-2/medium-turbo",
    }
    body: dict[str, Any] = {
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "creativity": args.creativity,
    }
    if args.seed is not None:
        body["seed"] = args.seed
    if args.intensity is not None:
        body["intensity"] = args.intensity
    if args.complexity is not None:
        body["complexity"] = args.complexity
    if args.style:
        body["styles"] = [parse_weighted(item, 0.8) for item in args.style]
    if args.style_ref:
        body["image_style_references"] = [parse_ref(item, 0.5) for item in args.style_ref]
    if args.moodboard:
        moodboard = parse_weighted(args.moodboard, 0.23)
        body["moodboards"] = [moodboard]

    headers = {}
    if args.webhook_url:
        headers["X-Webhook-URL"] = args.webhook_url

    job = request_json("POST", path_by_model[args.model], body, extra_headers=headers)
    print(json.dumps(job, indent=2))

    job_id = job.get("job_id")
    if not job_id or args.no_wait or args.webhook_url:
        return

    while True:
        time.sleep(args.interval)
        current = request_json("GET", f"/jobs/{job_id}")
        print(json.dumps(current, indent=2))
        if current.get("status") in TERMINAL_STATUSES:
            break


def cmd_job(args: argparse.Namespace) -> None:
    print(json.dumps(request_json("GET", f"/jobs/{args.job_id}"), indent=2))


def cmd_styles(args: argparse.Namespace) -> None:
    query = {
        "filter": args.filter,
        "limit": args.limit,
        "cursor": args.cursor,
        "model": args.model,
        "ids": args.ids,
        "liked": args.liked,
        "user": args.user,
    }
    print(json.dumps(request_json("GET", "/styles", query=query), indent=2))


def cmd_style(args: argparse.Namespace) -> None:
    print(json.dumps(request_json("GET", f"/styles/{args.style_id}"), indent=2))


def cmd_share_style(args: argparse.Namespace) -> None:
    print(json.dumps(request_json("POST", f"/styles/{args.style_id}/share/workspace"), indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Krea API helper")
    sub = parser.add_subparsers(dest="command", required=True)

    generate = sub.add_parser("generate", help="Submit a Krea 2 image generation job")
    generate.add_argument("prompt")
    generate.add_argument("--model", choices=["large", "medium", "medium-turbo"], default="large")
    generate.add_argument("--aspect-ratio", default="1:1")
    generate.add_argument("--resolution", default="1K")
    generate.add_argument("--creativity", choices=["raw", "low", "medium", "high"], default="medium")
    generate.add_argument("--seed", type=float)
    generate.add_argument("--style", action="append", help="STYLE_ID or STYLE_ID=strength; repeatable")
    generate.add_argument("--style-ref", action="append", help="URL or URL=strength; repeatable")
    generate.add_argument("--moodboard", help="MOODBOARD_UUID or MOODBOARD_UUID=strength")
    generate.add_argument("--intensity", type=int)
    generate.add_argument("--complexity", type=int)
    generate.add_argument("--webhook-url")
    generate.add_argument("--no-wait", action="store_true")
    generate.add_argument("--interval", type=float, default=3.0)
    generate.set_defaults(func=cmd_generate)

    job = sub.add_parser("job", help="Fetch a job by ID")
    job.add_argument("job_id")
    job.set_defaults(func=cmd_job)

    styles = sub.add_parser("styles", help="List accessible styles")
    styles.add_argument("--filter", default="user")
    styles.add_argument("--limit", type=int, default=50)
    styles.add_argument("--cursor")
    styles.add_argument("--model")
    styles.add_argument("--ids")
    styles.add_argument("--liked", action="store_true")
    styles.add_argument("--user")
    styles.set_defaults(func=cmd_styles)

    style = sub.add_parser("style", help="Fetch one style by ID")
    style.add_argument("style_id")
    style.set_defaults(func=cmd_style)

    share = sub.add_parser("share-style", help="Share an owned style with the workspace")
    share.add_argument("style_id")
    share.set_defaults(func=cmd_share_style)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

