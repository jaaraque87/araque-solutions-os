"""State, contracts, approvals, and environment handling for realistic_ugc."""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import FLOW_NAME, FLOW_VERSION


STAGES = ("research", "script", "assets", "video", "qa", "finishing")
APPROVAL_GATES = {
    "script": "research",
    "assets": "script",
    "video": "assets",
    "finishing": "qa",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "realistic-ugc"


def make_run_slug(description: str, now: datetime | None = None) -> str:
    stamp = (now or datetime.now()).strftime("%Y%m%d-%H%M%S")
    return f"{slugify(description)}-{stamp}"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def default_outputs_root() -> Path:
    return repo_root() / "outputs" / "ugc"


def load_env_file(path: Path) -> dict[str, str]:
    """Read one explicit env file. Never walk parent directories."""
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        if name and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            values[name] = value.strip().strip('"').strip("'")
    return values


def resolve_secret(name: str, env_path: Path, aliases: tuple[str, ...] = ()) -> str | None:
    import os

    file_values = load_env_file(env_path)
    for candidate in (name, *aliases):
        value = os.environ.get(candidate) or file_values.get(candidate)
        if value:
            return value
    return None


def event(run_dir: Path, event_type: str, **data: Any) -> None:
    path = run_dir / "logs" / "events.ndjson"
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"ts": utc_now(), "event": event_type, **data}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_run(run_dir: Path) -> dict[str, Any]:
    path = run_dir / "run.json"
    if not path.exists():
        raise FileNotFoundError(f"run.json not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_run(run_dir: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    path = run_dir / "run.json"
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def initialize_run(
    *,
    brand: str,
    campaign: str,
    description: str,
    product_image: Path,
    look_image: Path | None = None,
    brief_file: Path | None = None,
    outputs_root: Path | None = None,
    run_slug: str | None = None,
) -> Path:
    if not product_image.is_file():
        raise FileNotFoundError(f"product image not found: {product_image}")
    if look_image and not look_image.is_file():
        raise FileNotFoundError(f"look image not found: {look_image}")
    if brief_file and not brief_file.is_file():
        raise FileNotFoundError(f"brief file not found: {brief_file}")

    slug = run_slug or make_run_slug(description)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*-\d{8}-\d{6}", slug):
        raise ValueError("run slug must be kebab-case ending in YYYYMMDD-HHMMSS")
    run_dir = (outputs_root or default_outputs_root()) / slug
    if run_dir.exists():
        raise FileExistsError(f"run already exists: {run_dir}")

    for relative in (
        "logs",
        "source_assets",
        "research",
        "script",
        "assets",
        "video",
        "qa",
        "finishing",
        "tmp",
    ):
        (run_dir / relative).mkdir(parents=True, exist_ok=True)

    product_dest = run_dir / "source_assets" / f"product{product_image.suffix.lower()}"
    shutil.copy2(product_image, product_dest)
    copied: dict[str, str] = {"product": product_dest.relative_to(run_dir).as_posix()}
    if look_image:
        look_dest = run_dir / "source_assets" / f"look{look_image.suffix.lower()}"
        shutil.copy2(look_image, look_dest)
        copied["look"] = look_dest.relative_to(run_dir).as_posix()
    if brief_file:
        brief_dest = run_dir / "source_assets" / f"brief{brief_file.suffix.lower()}"
        shutil.copy2(brief_file, brief_dest)
        copied["brief"] = brief_dest.relative_to(run_dir).as_posix()

    created = utc_now()
    state: dict[str, Any] = {
        "schema_version": 1,
        "flow": FLOW_NAME,
        "flow_version": FLOW_VERSION,
        "run_slug": slug,
        "brand": brand,
        "campaign": campaign,
        "description": description,
        "status": "initialized",
        "created_at": created,
        "updated_at": created,
        "final_artifact": None,
        "source_assets": copied,
        "stages": {
            stage: {
                "status": "pending",
                "approved": False,
                "artifacts": [],
                "cost_usd": 0.0,
            }
            for stage in STAGES
        },
        "cost": {"estimated_usd": 0.0, "actual_usd": 0.0, "currency": "USD"},
    }
    save_run(run_dir, state)
    event(run_dir, "run.created", flow=FLOW_NAME, brand=brand, campaign=campaign)
    return run_dir


def require_gate(state: dict[str, Any], target_stage: str) -> None:
    prerequisite = APPROVAL_GATES.get(target_stage)
    if prerequisite and not state["stages"][prerequisite]["approved"]:
        raise PermissionError(
            f"stage '{target_stage}' requires approved stage '{prerequisite}'"
        )


def set_stage(
    run_dir: Path,
    stage: str,
    *,
    status: str,
    artifacts: list[str] | None = None,
    cost_usd: float | None = None,
    detail: str | None = None,
) -> dict[str, Any]:
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage}")
    state = load_run(run_dir)
    entry = state["stages"][stage]
    entry["status"] = status
    entry["updated_at"] = utc_now()
    if artifacts is not None:
        entry["artifacts"] = artifacts
    if cost_usd is not None:
        previous = float(entry.get("cost_usd", 0.0))
        entry["cost_usd"] = round(float(cost_usd), 4)
        state["cost"]["actual_usd"] = round(
            float(state["cost"].get("actual_usd", 0.0)) - previous + float(cost_usd), 4
        )
    if detail:
        entry["detail"] = detail
    save_run(run_dir, state)
    event(run_dir, f"stage.{status}", stage=stage, artifacts=artifacts or [], detail=detail)
    return state


def approve_stage(run_dir: Path, stage: str, approver: str, note: str = "") -> dict[str, Any]:
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage}")
    state = load_run(run_dir)
    entry = state["stages"][stage]
    if entry["status"] not in {"ready_for_review", "complete", "qa_passed"}:
        raise ValueError(
            f"stage '{stage}' cannot be approved while status is '{entry['status']}'"
        )
    entry["approved"] = True
    entry["approved_by"] = approver
    entry["approved_at"] = utc_now()
    entry["approval_note"] = note
    save_run(run_dir, state)
    event(run_dir, "stage.approved", stage=stage, approver=approver, note=note)
    return state


def relative_artifact(run_dir: Path, path: Path) -> str:
    return path.resolve().relative_to(run_dir.resolve()).as_posix()
