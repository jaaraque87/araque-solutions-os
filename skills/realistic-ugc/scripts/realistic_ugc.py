#!/usr/bin/env python3
"""Project-local launcher for the canonical realistic_ugc CLI."""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    start = Path(__file__).resolve()
    root = next(
        (p for p in (start, *start.parents) if (p / "pipeline/flows/realistic_ugc/run.py").is_file()),
        None,
    )
    if root is None:
        raise SystemExit("Araque Solutions OS repository root not found")
    return subprocess.call(
        [sys.executable, "-m", "pipeline.flows.realistic_ugc.run", *sys.argv[1:]], cwd=root
    )


if __name__ == "__main__":
    raise SystemExit(main())
