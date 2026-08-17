"""CLI for the gated realistic_ugc production flow.

Run from the repository root:
    python -m pipeline.flows.realistic_ugc.run --help
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from .core import (
    STAGES,
    approve_stage,
    default_outputs_root,
    initialize_run,
    load_run,
    relative_artifact,
    repo_root,
    require_gate,
    save_run,
    set_stage,
)
from .providers import dry_run_payload, generate_assets, generate_video
from .qa import detect_scene_cuts, prepare_patch, run_qa


DEFAULT_ENV = repo_root() / "pipeline" / ".env"


def path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def add_common_run(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--run-dir", required=True, type=path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Premium 30-second realistic UGC flow with approval gates and auditable runs."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a contracted outputs/ugc run")
    init.add_argument("--brand", required=True)
    init.add_argument("--campaign", required=True)
    init.add_argument("--description", required=True)
    init.add_argument("--product-image", required=True, type=path)
    init.add_argument("--look-image", type=path)
    init.add_argument("--brief-file", type=path)
    init.add_argument("--outputs-root", type=path, default=default_outputs_root())
    init.add_argument("--run-slug")

    status = sub.add_parser("status", help="Print run state")
    add_common_run(status)

    ready = sub.add_parser("mark-ready", help="Register agent-produced artifacts for review")
    add_common_run(ready)
    ready.add_argument("--stage", choices=("research", "script", "finishing"), required=True)
    ready.add_argument("--artifact", action="append", type=path, required=True)
    ready.add_argument("--detail", default="")

    approve = sub.add_parser("approve", help="Record explicit human approval")
    add_common_run(approve)
    approve.add_argument("--stage", choices=STAGES, required=True)
    approve.add_argument("--approver", required=True)
    approve.add_argument("--note", default="")

    assets = sub.add_parser("assets", help="Generate portrait, character sheet, and location")
    add_common_run(assets)
    assets.add_argument("--character-brief", required=True, type=path)
    assets.add_argument("--location-brief", required=True, type=path)
    assets.add_argument("--description", default="")
    assets.add_argument("--env-file", type=path, default=DEFAULT_ENV)
    assets.add_argument("--execute", action="store_true", help="Spend provider credits")

    video = sub.add_parser("video", help="Dry-run or execute Seedance 2.5 via Kie")
    add_common_run(video)
    video.add_argument("--prompt-file", required=True, type=path)
    video.add_argument("--image", action="append", type=path)
    video.add_argument("--duration", type=int, default=30)
    video.add_argument("--aspect-ratio", default="9:16")
    video.add_argument("--resolution", default="720p")
    video.add_argument("--env-file", type=path, default=DEFAULT_ENV)
    video.add_argument("--execute", action="store_true", help="Spend provider credits")

    qa = sub.add_parser("qa", help="Run ffprobe, contact sheet, loudness, and optional transcript")
    add_common_run(qa)
    qa.add_argument("--video", type=path)
    qa.add_argument("--env-file", type=path, default=DEFAULT_ENV)
    qa.add_argument("--transcribe", action="store_true", help="Use OpenAI Whisper API")

    cuts = sub.add_parser("cuts", help="Detect probable hard cuts")
    add_common_run(cuts)
    cuts.add_argument("--video", type=path)
    cuts.add_argument("--threshold", type=float, default=0.35)

    patch = sub.add_parser("prepare-patch", help="Extract anchors for one failed shot")
    add_common_run(patch)
    patch.add_argument("--video", type=path)
    patch.add_argument("--shot", type=int, required=True)
    patch.add_argument("--start", type=float, required=True)
    patch.add_argument("--end", type=float, required=True)

    finish = sub.add_parser("finish", help="Promote an approved final master")
    add_common_run(finish)
    finish.add_argument("--final-video", required=True, type=path)

    return parser


def default_images(run_dir: Path) -> list[Path]:
    state = load_run(run_dir)
    images = [run_dir / "assets" / "character-sheet.png", run_dir / "assets" / "location.png"]
    images.append(run_dir / state["source_assets"]["product"])
    look = state.get("source_assets", {}).get("look")
    if look:
        images.append(run_dir / look)
    return images


def default_video(run_dir: Path) -> Path:
    return run_dir / "video" / "seedance-v1.mp4"


def command_main(args: argparse.Namespace) -> int:
    if args.command == "init":
        run_dir = initialize_run(
            brand=args.brand,
            campaign=args.campaign,
            description=args.description,
            product_image=args.product_image,
            look_image=args.look_image,
            brief_file=args.brief_file,
            outputs_root=args.outputs_root,
            run_slug=args.run_slug,
        )
        print(run_dir)
        return 0

    run_dir: Path = args.run_dir
    state = load_run(run_dir)
    if state.get("flow") != "realistic_ugc":
        raise ValueError(f"not a realistic_ugc run: {run_dir}")

    if args.command == "status":
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0

    if args.command == "mark-ready":
        if args.stage != "research":
            require_gate(state, args.stage)
        artifacts: list[str] = []
        for artifact in args.artifact:
            if not artifact.is_file():
                raise FileNotFoundError(artifact)
            artifacts.append(relative_artifact(run_dir, artifact))
        set_stage(
            run_dir,
            args.stage,
            status="ready_for_review",
            artifacts=artifacts,
            detail=args.detail,
        )
        print(f"{args.stage}: ready_for_review")
        return 0

    if args.command == "approve":
        approve_stage(run_dir, args.stage, args.approver, args.note)
        print(f"{args.stage}: approved by {args.approver}")
        return 0

    if args.command == "assets":
        require_gate(state, "assets")
        for brief in (args.character_brief, args.location_brief):
            if not brief.is_file():
                raise FileNotFoundError(brief)
        if not args.execute:
            preview = {
                "mode": "dry-run",
                "stage": "assets",
                "providers": ["fal.ai Krea 2 Large", "fal.ai GPT Image 2 Edit"],
                "outputs": [
                    "assets/character-portrait.png",
                    "assets/character-sheet.png",
                    "assets/location.png",
                ],
                "credit_spend": False,
            }
            print(json.dumps(preview, indent=2))
            return 0
        generated = generate_assets(
            run_dir=run_dir,
            env_path=args.env_file,
            character_brief=args.character_brief,
            location_brief=args.location_brief,
            description=args.description,
        )
        print(json.dumps({name: str(value) for name, value in generated.items()}, indent=2))
        return 0

    if args.command == "video":
        require_gate(state, "video")
        images = args.image or default_images(run_dir)
        preview = dry_run_payload(
            prompt_file=args.prompt_file,
            images=images,
            duration=args.duration,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
        )
        if not args.execute:
            preview["mode"] = "dry-run"
            preview["credit_spend"] = False
            print(json.dumps(preview, ensure_ascii=False, indent=2))
            return 0
        output = generate_video(
            run_dir=run_dir,
            env_path=args.env_file,
            prompt_file=args.prompt_file,
            images=images,
            duration=args.duration,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
        )
        print(output)
        return 0

    if args.command == "qa":
        video = args.video or default_video(run_dir)
        result = run_qa(
            run_dir=run_dir,
            video=video,
            env_path=args.env_file,
            transcribe=args.transcribe,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["automated_pass"] else 2

    if args.command == "cuts":
        video = args.video or default_video(run_dir)
        print(json.dumps({"cuts_seconds": detect_scene_cuts(video, args.threshold)}, indent=2))
        return 0

    if args.command == "prepare-patch":
        video = args.video or default_video(run_dir)
        print(prepare_patch(run_dir, video, args.shot, args.start, args.end))
        return 0

    if args.command == "finish":
        require_gate(state, "finishing")
        if not state["stages"]["finishing"]["approved"]:
            raise PermissionError("finishing stage requires explicit approval before promotion")
        if not args.final_video.is_file():
            raise FileNotFoundError(args.final_video)
        destination = run_dir / "final.mp4"
        if args.final_video.resolve() != destination.resolve():
            shutil.copy2(args.final_video, destination)
        set_stage(
            run_dir,
            "finishing",
            status="complete",
            artifacts=["final.mp4"],
            detail="Approved master promoted to canonical final.mp4.",
        )
        final_state = load_run(run_dir)
        final_state["status"] = "complete"
        final_state["final_artifact"] = "final.mp4"
        save_run(run_dir, final_state)
        print(destination)
        return 0

    raise ValueError(f"unsupported command: {args.command}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return command_main(args)
    except (FileNotFoundError, FileExistsError, PermissionError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
