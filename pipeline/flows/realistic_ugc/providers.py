"""External provider adapters for the realistic UGC flow.

Network calls only happen from explicit execute commands after approval gates.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .core import relative_artifact, resolve_secret, set_stage


KREA_ENDPOINT = "krea/v2/large/text-to-image"
GPT_IMAGE_ENDPOINT = "openai/gpt-image-2/edit"
KIE_UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"
KIE_CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
KIE_RECORD_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"
KIE_MODEL = "bytedance/seedance-2-5"
KIE_CREDIT_USD = 0.005

PORTRAIT_CANON = (
    "Single person, one subject only, centered, waist up, facing camera, neutral relaxed "
    "expression, plain seamless neutral studio background, even soft light, full outfit "
    "clearly visible. Photorealistic. No collage, no grid, no multiple views, no text, "
    "no borders, no props in hand, no other people."
)
LOCATION_CANON = (
    "Empty interior, three-quarter oblique angle so two walls and the depth of the room "
    "read at once, eye level, wide angle. Photorealistic architectural photography, "
    "natural practical light. Absolutely no people, bodies, faces, silhouettes, mannequins, "
    "portraits on walls, or human reflections. No text, logos, or watermarks."
)
SHEET_PROMPT = (
    "Create a photorealistic character sheet. Include one left-aligned close-up portrait "
    "with the outfit visible, plus four full-body views: front, right profile, left profile, "
    "and back. Use a plain white background, no text, borders, gradients, or props. Preserve "
    "the exact identity, face, bone structure, skin tone, hair, age, proportions, and outfit "
    "from the reference. All five views show the same single person. Do not recast, beautify, "
    "slim, change clothing, or change hairstyle."
)


def _fal_key(env_path: Path) -> str:
    key = resolve_secret("FAL_KEY", env_path, aliases=("FAL_API_KEY",))
    if not key:
        raise RuntimeError(f"FAL_KEY or FAL_API_KEY is missing from environment or {env_path}")
    return key


def _kie_key(env_path: Path) -> str:
    key = resolve_secret("KIE_API_KEY", env_path)
    if not key:
        raise RuntimeError(f"KIE_API_KEY is missing from environment or {env_path}")
    return key


def _fal_client(env_path: Path):
    os.environ["FAL_KEY"] = _fal_key(env_path)
    try:
        import fal_client
    except ImportError as exc:
        raise RuntimeError("fal-client is not installed; run pipeline/setup.py") from exc
    return fal_client


def _download(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "AraqueSolutionsOS/1.0"})
    with urllib.request.urlopen(request, timeout=600) as response:
        output.write_bytes(response.read())


def _write_prompt(output: Path, prompt: str) -> Path:
    prompt_path = output.with_suffix(output.suffix + ".prompt.txt")
    prompt_path.write_text(prompt.strip() + "\n", encoding="utf-8")
    return prompt_path


def generate_assets(
    *,
    run_dir: Path,
    env_path: Path,
    character_brief: Path,
    location_brief: Path,
    description: str,
) -> dict[str, Path]:
    """Generate portrait, identity sheet, and empty location through fal.ai."""
    client = _fal_client(env_path)
    character = character_brief.read_text(encoding="utf-8").strip()
    location = location_brief.read_text(encoding="utf-8").strip()
    if not character or not location:
        raise ValueError("character and location briefs must not be empty")

    assets_dir = run_dir / "assets"
    portrait = assets_dir / "character-portrait.png"
    sheet = assets_dir / "character-sheet.png"
    location_out = assets_dir / "location.png"

    portrait_prompt = f"{character}\n\n{PORTRAIT_CANON}"
    portrait_result = client.subscribe(
        KREA_ENDPOINT,
        arguments={"prompt": portrait_prompt, "aspect_ratio": "4:5", "creativity": "high"},
        with_logs=False,
    )
    portrait_images = portrait_result.get("images") or []
    if not portrait_images:
        raise RuntimeError(f"Krea portrait returned no image: {portrait_result}")
    _download(portrait_images[0]["url"], portrait)
    portrait_prompt_path = _write_prompt(portrait, portrait_prompt)

    portrait_url = client.upload_file(str(portrait))
    sheet_prompt = f"{SHEET_PROMPT}\n\nCharacter description: {description or character}"
    sheet_result = client.subscribe(
        GPT_IMAGE_ENDPOINT,
        arguments={
            "prompt": sheet_prompt,
            "image_urls": [portrait_url],
            "image_size": {"width": 3840, "height": 2160},
            "quality": "high",
            "num_images": 1,
        },
        with_logs=False,
    )
    sheet_images = sheet_result.get("images") or []
    if not sheet_images:
        raise RuntimeError(f"GPT Image character sheet returned no image: {sheet_result}")
    _download(sheet_images[0]["url"], sheet)
    sheet_prompt_path = _write_prompt(sheet, sheet_prompt)

    location_prompt = f"{location}\n\n{LOCATION_CANON}"
    location_result = client.subscribe(
        KREA_ENDPOINT,
        arguments={"prompt": location_prompt, "aspect_ratio": "16:9", "creativity": "high"},
        with_logs=False,
    )
    location_images = location_result.get("images") or []
    if not location_images:
        raise RuntimeError(f"Krea location returned no image: {location_result}")
    _download(location_images[0]["url"], location_out)
    location_prompt_path = _write_prompt(location_out, location_prompt)

    artifacts = {
        "portrait": portrait,
        "character_sheet": sheet,
        "location": location_out,
        "portrait_prompt": portrait_prompt_path,
        "sheet_prompt": sheet_prompt_path,
        "location_prompt": location_prompt_path,
    }
    set_stage(
        run_dir,
        "assets",
        status="ready_for_review",
        artifacts=[relative_artifact(run_dir, path) for path in artifacts.values()],
        detail="Review identity consistency across all five views and confirm the location contains no people.",
    )
    return artifacts


def _post_json(url: str, payload: dict[str, Any], key: str, timeout: int = 120) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    last_error: Exception | None = None
    for attempt in range(3):
        request = urllib.request.Request(url, data=body, method="POST")
        request.add_header("Content-Type", "application/json")
        request.add_header("Authorization", f"Bearer {key}")
        request.add_header("User-Agent", "AraqueSolutionsOS/1.0")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read())
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(2**attempt)
    raise RuntimeError(f"provider request failed after retries: {last_error}")


def _upload_kie(path: Path, key: str, upload_path: str) -> str:
    if not path.is_file():
        raise FileNotFoundError(path)
    data = path.read_bytes()
    remote_name = f"{hashlib.sha256(data).hexdigest()[:12]}-{path.name}"
    boundary = f"----araqueugc{int(time.time() * 1000)}"
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"

    def field(name: str, value: str) -> bytes:
        return (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n"
            f"{value}\r\n"
        ).encode("utf-8")

    body = b"".join(
        [
            field("uploadPath", upload_path),
            field("fileName", remote_name),
            (
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
                f"filename=\"{remote_name}\"\r\nContent-Type: {mime}\r\n\r\n"
            ).encode("utf-8"),
            data,
            f"\r\n--{boundary}--\r\n".encode("utf-8"),
        ]
    )
    request = urllib.request.Request(KIE_UPLOAD_URL, data=body, method="POST")
    request.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    request.add_header("Authorization", f"Bearer {key}")
    request.add_header("User-Agent", "curl/8.7.1")
    with urllib.request.urlopen(request, timeout=300) as response:
        result = json.loads(response.read())
    if not result.get("success"):
        raise RuntimeError(f"Kie upload failed for {path.name}: {result}")
    return result["data"]["downloadUrl"]


def generate_video(
    *,
    run_dir: Path,
    env_path: Path,
    prompt_file: Path,
    images: list[Path],
    duration: int = 30,
    aspect_ratio: str = "9:16",
    resolution: str = "720p",
    generate_audio: bool = True,
    poll_interval: float = 10.0,
    timeout: int = 2400,
) -> Path:
    if not 4 <= duration <= 30:
        raise ValueError("duration must be between 4 and 30 seconds")
    if aspect_ratio not in {"9:16", "16:9", "1:1"}:
        raise ValueError("unsupported aspect ratio")
    if resolution not in {"480p", "720p"}:
        raise ValueError("resolution must be 480p or 720p")
    if not 1 <= len(images) <= 30:
        raise ValueError("Seedance requires 1-30 reference images")
    prompt = prompt_file.read_text(encoding="utf-8").strip()
    if not prompt or len(prompt) > 30000:
        raise ValueError("prompt must contain 1-30000 characters")

    key = _kie_key(env_path)
    remote_images = [_upload_kie(path, key, slug_upload_path(run_dir)) for path in images]
    payload = {
        "model": KIE_MODEL,
        "input": {
            "prompt": prompt,
            "reference_image_urls": remote_images,
            "generate_audio": generate_audio,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "output_format": "mp4",
        },
    }
    video_dir = run_dir / "video"
    video_dir.mkdir(parents=True, exist_ok=True)
    manifest = video_dir / "seedance-request.json"
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    created = _post_json(KIE_CREATE_URL, payload, key)
    if created.get("code") != 200:
        raise RuntimeError(f"Kie createTask failed: {created}")
    task_id = created["data"]["taskId"]
    task_path = video_dir / "seedance-task.json"
    task_path.write_text(
        json.dumps({"task_id": task_id, "model": KIE_MODEL}, indent=2) + "\n",
        encoding="utf-8",
    )

    deadline = time.time() + timeout
    record: dict[str, Any] = {}
    while time.time() < deadline:
        request = urllib.request.Request(f"{KIE_RECORD_URL}?taskId={task_id}")
        request.add_header("Authorization", f"Bearer {key}")
        request.add_header("User-Agent", "AraqueSolutionsOS/1.0")
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read())
        record = result.get("data") or {}
        state = record.get("state")
        if state == "success":
            break
        if state == "fail":
            raise RuntimeError(
                f"Seedance failed: {record.get('failCode')} {record.get('failMsg')}"
            )
        time.sleep(poll_interval)
    else:
        raise TimeoutError(f"Seedance timed out after {timeout}s; task_id={task_id}")

    urls = json.loads(record.get("resultJson") or "{}").get("resultUrls") or []
    if not urls:
        raise RuntimeError(f"Seedance returned no result URL: {record}")
    output = video_dir / "seedance-v1.mp4"
    _download(urls[0], output)
    credits = float(record.get("creditsConsumed") or 0.0)
    cost = round(credits * KIE_CREDIT_USD, 4) if credits else 0.0
    set_stage(
        run_dir,
        "video",
        status="ready_for_review",
        artifacts=[
            relative_artifact(run_dir, output),
            relative_artifact(run_dir, manifest),
            relative_artifact(run_dir, task_path),
        ],
        cost_usd=cost,
        detail=f"task_id={task_id}; credits={credits:g}",
    )
    return output


def slug_upload_path(run_dir: Path) -> str:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in run_dir.name)
    return f"araque/realistic-ugc/{safe}"


def dry_run_payload(
    *,
    prompt_file: Path,
    images: list[Path],
    duration: int,
    aspect_ratio: str,
    resolution: str,
) -> dict[str, Any]:
    prompt = prompt_file.read_text(encoding="utf-8").strip()
    if not prompt or len(prompt) > 30000:
        raise ValueError("prompt must contain 1-30000 characters")
    missing = [str(path) for path in images if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing references: {missing}")
    return {
        "provider": "kie.ai",
        "model": KIE_MODEL,
        "prompt_chars": len(prompt),
        "reference_images_in_order": [str(path) for path in images],
        "duration": duration,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "generate_audio": True,
        "estimated_cost_note": "Confirm current provider quote before execute; package benchmark was USD 9.45 for 30s/720p.",
    }
