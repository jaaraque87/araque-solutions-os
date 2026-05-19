"""
Kenza UGC Pipeline — Main Orchestrator

Steps (Morfeo Academy pipeline):
  00 brand_analyzer  — Brand kit setup (brand_profile.json)
  01 guion           — Script: ángulos, personaje, escenas, diálogos, briefs (guion.json)
  02 personaje       — Character portrait via GPT Image 2 / fal.ai (character.png)
  03 locacion        — Location frame via GPT Image 2 / fal.ai (location.png)
  04 morpheus        — Scene frames: personaje + producto + locación (scene_N.png)
  05 tts             — TTS audio via Gemini 3.1 Flash (tts_scene_N.mp3)
  06 voice_change    — Voice change via ElevenLabs STS — optional (voice_scene_N.mp3)
  07 kling           — Raw video clips via Kling (kling_scene_N.mp4)
  08 sync            — Lipsync via fal Sync-3 — optional (sync_scene_N.mp4)
  09 music           — Background music via Suno/Kie.ai (music.mp3)
  10 assembly        — Master assembly via FFmpeg (master.mp4)
  11 subs            — Subtitles burn-in + finishing via Submagic (final.mp4)
  12                 — MANUAL: deliver / publish final.mp4

Usage:
    python run.py --brand Kenza --steps all
    python run.py --brand Kenza --steps 01,04,05,07,09,10,11
    python run.py --brand Kenza --steps 05-10
    python run.py --list-steps
"""

import json
import os
import sys
import importlib
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

# ── Bootstrap ─────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

console = Console()

# ── Step Registry ─────────────────────────────────────────────────────────────
# Each entry: (id, module_name, label, required_keys, cost_usd_estimate)
# Mirrors the Morfeo Academy pipeline exactly:
#   00 brand → 01 guion → 02 personaje → 03 locacion → 04 morpheus →
#   05 tts → 06 voice_change → 07 kling → 08 sync → 09 music → 10 assembly →
#   11 subs → 12 publish (manual, no script)
STEPS = [
    ("00", "brand_analyzer",  "Brand Setup",                  ["GEMINI_API_KEY"],           0.00),
    ("01", "guion",           "Script / Guión",               ["GEMINI_API_KEY"],           0.01),
    ("02", "personaje",       "Character (GPT Image 2)",      ["FAL_KEY"],                  0.41),
    ("03", "locacion",        "Location (GPT Image 2)",       ["FAL_KEY"],                  0.41),
    ("04", "morpheus",        "Scene Frames (Morpheus)",      ["FAL_KEY"],                  0.50),
    ("05", "tts",             "TTS Audio (Gemini)",           ["GEMINI_API_KEY"],           0.02),
    ("06", "voice_change",    "Voice Change (ElevenLabs)",    ["ELEVENLABS_API_KEY"],       0.06),
    ("07", "kling",           "Video Clips (Kling)",          ["FAL_KEY"],                  1.20),
    ("08", "sync",            "Lipsync — optional (Sync-3)",  ["FAL_KEY"],                  0.60),
    ("09", "music",           "Background Music (Suno)",      ["KIE_API_KEY"],              0.06),
    ("10", "assembly",        "Final Assembly (FFmpeg)",      [],                           0.00),
    ("11", "subs",            "Subtitles + Finishing",        ["SUBMAGIC_API_KEY"],         0.10),
    # Step 12 is manual publish — no script
]

STEP_BY_ID = {s[0]: s for s in STEPS}


def make_run_id(brand: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    slug = brand.lower().replace(" ", "_")
    return f"{slug}_{ts}"


def parse_steps(steps_arg: str) -> list[str]:
    """Accept: 'all', '01,05,06', '06-11'"""
    if steps_arg == "all":
        return [s[0] for s in STEPS]

    if "-" in steps_arg and "," not in steps_arg:
        start, end = steps_arg.split("-")
        return [s[0] for s in STEPS if int(start) <= int(s[0]) <= int(end)]

    return [x.zfill(2) for x in steps_arg.split(",")]


def validate_keys(step_ids: list[str]) -> list[str]:
    """Return list of missing required keys for the selected steps."""
    needed = set()
    for sid in step_ids:
        if sid in STEP_BY_ID:
            needed.update(STEP_BY_ID[sid][3])
    return [k for k in needed if not os.getenv(k)]


def write_run_json(run_dir: Path, data: dict) -> None:
    path = run_dir / "run.json"
    existing = {}
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
    existing.update(data)
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")


def append_event(run_dir: Path, event: dict) -> None:
    path = run_dir / "logs" / "events.ndjson"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def run_step(step_id: str, run_dir: Path, brand: str, operator: str, num_scenes: int) -> dict:
    """Dynamically import and execute scripts/<module>.py → returns result dict."""
    _, module_name, label, _, cost_est = STEP_BY_ID[step_id]

    console.rule(f"[bold cyan]Step {step_id}: {label}[/bold cyan]")

    script_path = ROOT / "scripts" / f"{module_name}.py"
    if not script_path.exists():
        msg = f"scripts/{module_name}.py not found — skipping."
        console.print(f"[yellow]⚠  {msg}[/yellow]")
        return {"status": "skipped", "reason": "script_not_found"}

    spec = importlib.util.spec_from_file_location(module_name, script_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    ctx = {
        "brand": brand,
        "operator": operator,
        "run_dir": run_dir,
        "brands_dir": ROOT / "brands",
        "num_scenes": num_scenes,
        "run_id": run_dir.name,
        "console": console,
    }

    result = mod.run(ctx)
    return result


# ── CLI ───────────────────────────────────────────────────────────────────────

@click.command()
@click.option("--brand",      required=False, default="Kenza",   help="Brand name (must exist in brands/)")
@click.option("--steps",      default="all",                      help="Steps: 'all', '01,05,06', '06-11'")
@click.option("--operator",   default=None,                       help="Operator name (overrides .env OPERATOR_NAME)")
@click.option("--num-scenes", default=None, type=int,             help="Number of scenes (overrides DEFAULT_NUM_SCENES in .env)")
@click.option("--run-id",     default=None,                       help="Resume an existing run_id instead of creating a new one")
@click.option("--dry-run",    is_flag=True,                       help="Print what would run without executing")
@click.option("--list-steps", is_flag=True,                       help="Print all pipeline steps and exit")
def main(
    brand: str,
    steps: str,
    operator: Optional[str],
    num_scenes: Optional[int],
    run_id: Optional[str],
    dry_run: bool,
    list_steps: bool,
) -> None:

    if list_steps:
        _print_steps_table()
        return

    operator = operator or os.getenv("OPERATOR_NAME", "unknown")
    num_scenes = num_scenes or int(os.getenv("DEFAULT_NUM_SCENES", "6"))

    step_ids = parse_steps(steps)
    invalid = [s for s in step_ids if s not in STEP_BY_ID]
    if invalid:
        console.print(f"[red]Unknown step IDs: {invalid}. Run --list-steps to see valid IDs.[/red]")
        sys.exit(1)

    total_cost = sum(STEP_BY_ID[s][4] for s in step_ids)

    # Run ID (needed for header even in dry-run)
    rid = run_id or make_run_id(brand)

    # Header
    console.print(Panel(
        f"[bold]Brand:[/bold] {brand}   [bold]Run:[/bold] {rid}\n"
        f"[bold]Operator:[/bold] {operator}   [bold]Scenes:[/bold] {num_scenes}\n"
        f"[bold]Steps:[/bold] {', '.join(step_ids)}   [bold]Est. cost:[/bold] ~${total_cost:.2f} USD",
        title="[bold cyan]Kenza UGC Pipeline[/bold cyan]",
        expand=False,
    ))

    if dry_run:
        _print_steps_table()
        console.print(f"\n[yellow]Dry run — nada ejecutado. Costo estimado: ~${total_cost:.2f} USD[/yellow]")
        return

    # Key validation (only for real runs)
    missing_keys = validate_keys(step_ids)
    if missing_keys:
        console.print(f"[red]Missing API keys in .env: {missing_keys}[/red]")
        console.print("[dim]Edit .env and add the missing keys before running.[/dim]")
        sys.exit(1)

    run_dir = ROOT / "outputs" / rid
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(exist_ok=True)

    # Initialise run.json
    write_run_json(run_dir, {
        "run_id": rid,
        "brand": brand,
        "operator": operator,
        "num_scenes": num_scenes,
        "steps_requested": step_ids,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "running",
        "cost_estimate_usd": total_cost,
        "steps": {},
    })

    results: dict[str, dict] = {}
    total_actual_cost = 0.0

    for sid in step_ids:
        label = STEP_BY_ID[sid][2]
        started_at = datetime.now(timezone.utc).isoformat()

        try:
            result = run_step(sid, run_dir, brand, operator, num_scenes)
        except Exception:
            tb = traceback.format_exc()
            console.print(f"[red]Step {sid} failed:[/red]\n{tb}")
            result = {"status": "error", "traceback": tb}

        result.setdefault("status", "ok")
        result["started_at"] = started_at
        result["finished_at"] = datetime.now(timezone.utc).isoformat()

        actual_cost = result.get("cost_usd", STEP_BY_ID[sid][4])
        total_actual_cost += actual_cost
        result["cost_usd"] = actual_cost

        results[sid] = result

        # Persist step result
        write_run_json(run_dir, {"steps": {sid: result}})
        append_event(run_dir, {
            "ts": result["finished_at"],
            "step": sid,
            "label": label,
            "status": result["status"],
            "cost_usd": actual_cost,
        })

        status_color = "green" if result["status"] == "ok" else ("yellow" if result["status"] == "skipped" else "red")
        console.print(f"[{status_color}]Step {sid} → {result['status']}  (${actual_cost:.3f})[/{status_color}]")

        if result["status"] == "error":
            console.print("[red]Stopping pipeline due to error. Fix and re-run with --run-id to resume.[/red]")
            break

    # Final summary
    all_ok = all(r["status"] in ("ok", "skipped") for r in results.values())
    final_status = "complete" if all_ok else "failed"
    write_run_json(run_dir, {
        "status": final_status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "cost_actual_usd": total_actual_cost,
    })

    _print_summary(results, run_dir, total_actual_cost)


def _print_steps_table() -> None:
    t = Table(title="Kenza UGC Pipeline — Steps", box=box.ROUNDED)
    t.add_column("ID", style="cyan", width=4)
    t.add_column("Label", style="white")
    t.add_column("Script", style="dim")
    t.add_column("Required Keys", style="yellow")
    t.add_column("~Cost", style="green", justify="right")
    for sid, mod, label, keys, cost in STEPS:
        t.add_row(sid, label, f"scripts/{mod}.py", ", ".join(keys) or "—", f"${cost:.2f}")
    console.print(t)


def _print_summary(results: dict, run_dir: Path, total_cost: float) -> None:
    t = Table(title=f"Run complete → {run_dir.name}", box=box.SIMPLE)
    t.add_column("Step")
    t.add_column("Status")
    t.add_column("Cost", justify="right")
    for sid, r in results.items():
        label = STEP_BY_ID[sid][2]
        color = "green" if r["status"] == "ok" else ("yellow" if r["status"] == "skipped" else "red")
        t.add_row(f"{sid} {label}", f"[{color}]{r['status']}[/{color}]", f"${r.get('cost_usd', 0):.3f}")
    t.add_row("", "[bold]TOTAL[/bold]", f"[bold]${total_cost:.3f}[/bold]")
    console.print(t)
    console.print(f"\n[dim]Outputs: {run_dir}[/dim]")


if __name__ == "__main__":
    main()
