import argparse
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from run import (
    PIPELINE_ROOT,
    RUNS_DIR,
    build_comfydeploy_payload,
    call_comfydeploy,
    download_assets,
    extract_asset_urls,
    generate_hyperframes_project,
    load_env_file,
    make_run_id,
    require_secret,
    write_json,
)


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
HOOKS_ROOT = REPO_ROOT / "tools" / "hook-lab" / "clients"
REAL_CONFIRMATION = "SPEND_COMFYDEPLOY_CREDITS"
REAL_ENV_GATE = "ARAQUE_ALLOW_GPU_EXECUTION"
SUPPORTED_IMAGES = {".jpg", ".jpeg", ".png", ".webp"}


def normalized_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.sub(r"[^a-z0-9]+", " ", value.lower()).split()
        if len(token) >= 3
    }


def discover_hooks_file(image_path: Path, client: str | None, hooks_file: Path | None) -> Path:
    if hooks_file:
        resolved = hooks_file.resolve()
        if not resolved.is_file():
            raise RuntimeError(f"No existe el corpus de hooks: {resolved}")
        return resolved

    if client:
        candidate = HOOKS_ROOT / client / "hooks.json"
        if not candidate.is_file():
            raise RuntimeError(
                f"No hay research puntuado para '{client}'. Esperado: {candidate}"
            )
        return candidate

    image_tokens = normalized_tokens(str(image_path.resolve()))
    matches: list[tuple[int, Path]] = []
    for candidate in HOOKS_ROOT.glob("*/hooks.json"):
        client_tokens = normalized_tokens(candidate.parent.name)
        overlap = len(image_tokens & client_tokens)
        if overlap:
            matches.append((overlap, candidate))
    if not matches:
        raise RuntimeError(
            "No pude asociar la imagen con un cliente que tenga research. "
            "Usa --client <carpeta-en-tools/hook-lab/clients> o --hooks-file <hooks.json>."
        )
    matches.sort(key=lambda item: (-item[0], str(item[1])))
    return matches[0][1]


def load_scored_hooks(path: Path) -> dict:
    corpus = json.loads(path.read_text(encoding="utf-8"))
    hooks = corpus.get("hooks")
    if not isinstance(hooks, list) or len(hooks) < 3:
        raise RuntimeError("El corpus debe contener al menos tres hooks.")
    if not corpus.get("research"):
        raise RuntimeError("El corpus no declara su research; producción bloqueada.")
    for hook in hooks:
        if not hook.get("linea") or not isinstance(hook.get("score"), (int, float)):
            raise RuntimeError("Cada hook necesita linea y score numérico.")
    return corpus


def select_top_hooks(corpus: dict, limit: int = 3) -> list[dict]:
    ranked = sorted(
        enumerate(corpus["hooks"]),
        key=lambda item: (
            -float(item[1]["score"]),
            -int(bool(item[1].get("seleccionado"))),
            item[0],
        ),
    )
    return [dict(hook, rank=index + 1) for index, (_, hook) in enumerate(ranked[:limit])]


def build_automatic_brief(image_path: Path, corpus: dict, hooks: list[dict]) -> dict:
    winner = hooks[0]
    client = corpus.get("cliente", "cliente")
    duration = 12
    captions = []
    for index, hook in enumerate(hooks):
        start = index * 4 + 0.25
        captions.append(
            {
                "start": start,
                "end": min(duration - 0.2, start + 3.45),
                "text": f"{hook['rank']}. {hook['linea']} · {hook['score']}/10",
            }
        )
    return {
        "schema_version": "araque-one-click-v1",
        "brand": client,
        "client": client,
        "title": "3 hooks listos para probar",
        "subtitle": f"Ganador actual: {winner.get('id', 'hook')} · {winner['score']}/10",
        "format": "9:16",
        "duration_seconds": duration,
        "style": "preview editorial vertical; imagen ancla completa; tres hooks puntuados",
        "source_image": str(image_path.resolve()),
        "research": {
            "source": corpus.get("research"),
            "date": corpus.get("fecha"),
            "note": corpus.get("nota"),
        },
        "hook_candidates": hooks,
        "selected_hook_id": winner.get("id"),
        "captions": captions,
        "scorecard_hypothesis": {
            "variable": "hook",
            "hypothesis": (
                f"El patrón '{winner.get('patron', 'probado')}' con score "
                f"{winner['score']}/10 elevará la retención inicial frente a los otros candidatos."
            ),
            "primary_metric": "retencion_3s",
            "secondary_metrics": ["completion_rate", "shares", "conversations"],
            "status": "ready_for_preview_not_publishing",
        },
        "comfydeploy_inputs": {
            "prompt": winner.get("visual_frame1", winner["linea"]),
            "negative_prompt": "watermark, distorted face, illegible text, horizontal framing",
            "width": 1080,
            "height": 1920,
            "num_outputs": 1,
        },
    }


def assert_real_execution_allowed(confirm_cost: str | None, source_image_url: str | None) -> None:
    if confirm_cost != REAL_CONFIRMATION:
        raise RuntimeError(
            f"Corrida real bloqueada: usa --confirm-cost {REAL_CONFIRMATION}."
        )
    if os.getenv(REAL_ENV_GATE, "").strip() != "1":
        raise RuntimeError(
            f"Corrida real bloqueada: define {REAL_ENV_GATE}=1 sólo durante producción aprobada."
        )
    if not source_image_url or not source_image_url.startswith(("https://", "http://")):
        raise RuntimeError(
            "Corrida real bloqueada: --source-image-url debe ser una URL accesible por ComfyDeploy."
        )


def create_preview_run(
    image_path: Path,
    client: str | None = None,
    hooks_file: Path | None = None,
    run_id: str | None = None,
    runs_dir: Path = RUNS_DIR,
) -> tuple[Path, dict, list[dict], Path]:
    image_path = image_path.resolve()
    if not image_path.is_file() or image_path.suffix.lower() not in SUPPORTED_IMAGES:
        raise RuntimeError("La entrada debe ser una imagen JPG, PNG o WebP existente.")

    resolved_hooks = discover_hooks_file(image_path, client, hooks_file)
    corpus = load_scored_hooks(resolved_hooks)
    hooks = select_top_hooks(corpus)
    brief = build_automatic_brief(image_path, corpus, hooks)
    actual_run_id = run_id or make_run_id(brief)
    run_dir = runs_dir / actual_run_id
    source_assets = run_dir / "source-assets"
    source_assets.mkdir(parents=True, exist_ok=True)
    local_image = source_assets / image_path.name
    if image_path != local_image.resolve():
        shutil.copy2(image_path, local_image)

    write_json(run_dir / "hooks.scored.json", {"source": str(resolved_hooks), "hooks": hooks})
    write_json(run_dir / "brief.auto.json", brief)
    payload = build_comfydeploy_payload(brief)
    write_json(run_dir / "comfydeploy_payload.json", payload)
    hf_dir = generate_hyperframes_project(
        run_dir,
        brief,
        [{"kind": "source-image", "path": str(local_image)}],
    )
    manifest = {
        "run_id": actual_run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "preview-no-credits",
        "network_calls": 0,
        "gpu_started": False,
        "source_image": str(image_path),
        "hooks_source": str(resolved_hooks),
        "selected_hook_id": brief["selected_hook_id"],
        "brief": str(run_dir / "brief.auto.json"),
        "hyperframes_dir": str(hf_dir),
        "next_commands": {
            "check": "npx hyperframes check",
            "preview": "npx hyperframes preview",
        },
        "real_execution_gate": {
            "required_flag": "--execute-real",
            "required_confirmation": REAL_CONFIRMATION,
            "required_environment": f"{REAL_ENV_GATE}=1",
            "requires_public_source_image_url": True,
        },
    }
    write_json(run_dir / "manifest.json", manifest)
    return run_dir, brief, hooks, hf_dir


def execute_real_run(
    run_dir: Path,
    brief: dict,
    source_image_url: str,
    image_input_key: str,
) -> Path:
    brief["comfydeploy_inputs"][image_input_key] = source_image_url
    payload = build_comfydeploy_payload(brief)
    write_json(run_dir / "comfydeploy_payload.json", payload)
    response = call_comfydeploy(payload)
    write_json(run_dir / "comfydeploy_response.json", response)
    urls = extract_asset_urls(response)
    if not urls:
        raise RuntimeError("ComfyDeploy no devolvió assets descargables.")
    assets = download_assets(urls, run_dir / "source-assets" / "comfydeploy")
    hf_dir = generate_hyperframes_project(run_dir, brief, assets)
    manifest_path = run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update(
        {
            "mode": "real-comfydeploy",
            "network_calls": 1,
            "gpu_started": True,
            "hyperframes_dir": str(hf_dir),
            "comfydeploy_response": str(run_dir / "comfydeploy_response.json"),
        }
    )
    write_json(manifest_path, manifest)
    return hf_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Una imagen -> 3 hooks puntuados -> brief -> preview HyperFrames seguro"
    )
    parser.add_argument("image", help="Imagen ancla local")
    parser.add_argument("--client", help="Carpeta dentro de tools/hook-lab/clients")
    parser.add_argument("--hooks-file", type=Path, help="Corpus hooks.json explícito")
    parser.add_argument("--run-id", help="ID reproducible para la corrida")
    parser.add_argument("--execute-real", action="store_true", help="Permitir POST real tras los gates")
    parser.add_argument("--confirm-cost", help="Frase de aceptación de créditos")
    parser.add_argument("--source-image-url", help="URL pública de la misma imagen para ComfyDeploy")
    parser.add_argument("--image-input-key", default="source_image", help="Input del deployment LTX")
    args = parser.parse_args()

    load_env_file(PIPELINE_ROOT / ".env")
    run_dir, brief, hooks, hf_dir = create_preview_run(
        Path(args.image), args.client, args.hooks_file, args.run_id
    )
    mode = "preview-no-credits"
    if args.execute_real:
        assert_real_execution_allowed(args.confirm_cost, args.source_image_url)
        require_secret("COMFYDEPLOY_API_KEY")
        require_secret("COMFYDEPLOY_DEPLOYMENT_ID")
        hf_dir = execute_real_run(
            run_dir,
            brief,
            args.source_image_url,
            args.image_input_key,
        )
        mode = "real-comfydeploy"

    print(f"Mode: {mode}")
    print("Hooks: " + ", ".join(f"{item.get('id')}={item['score']}/10" for item in hooks))
    print(f"Brief: {run_dir / 'brief.auto.json'}")
    print(f"HyperFrames: {hf_dir}")
    print("No se renderizó MP4. Revisa con: npx hyperframes check; npx hyperframes preview")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
