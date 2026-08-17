#!/usr/bin/env python3
"""Validate tracked output folder names and required run artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


RUN_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-\d{8}-\d{6}$")
KNOWN_FLOWS = {"avatar": "avatar_reel", "ugc": "realistic_ugc"}


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    outputs = root / "outputs"
    if not outputs.exists():
        return errors
    for flow_dir in outputs.iterdir():
        if not flow_dir.is_dir():
            errors.append(f"unexpected file in outputs/: {flow_dir.name}")
            continue
        if flow_dir.name not in KNOWN_FLOWS:
            if any(flow_dir.iterdir()):
                errors.append(f"unknown non-empty flow directory: {flow_dir}")
            continue
        for run_dir in flow_dir.iterdir():
            if not run_dir.is_dir():
                errors.append(f"unexpected file in {flow_dir}: {run_dir.name}")
                continue
            if not RUN_SLUG.fullmatch(run_dir.name):
                errors.append(f"invalid run slug: {run_dir}")
            for required in ("run.json", "logs/events.ndjson"):
                if not (run_dir / required).is_file():
                    errors.append(f"missing {required}: {run_dir}")
            state_path = run_dir / "run.json"
            if state_path.is_file():
                try:
                    state = json.loads(state_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as exc:
                    errors.append(f"invalid run.json at {run_dir}: {exc}")
                    continue
                expected = KNOWN_FLOWS[flow_dir.name]
                if state.get("flow") != expected:
                    errors.append(f"flow mismatch at {run_dir}: expected {expected}")
                final = state.get("final_artifact")
                if state.get("status") == "complete" and (not final or not (run_dir / final).is_file()):
                    errors.append(f"complete run lacks final artifact: {run_dir}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print("Output contract violations:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Output contract OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
