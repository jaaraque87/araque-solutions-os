import argparse
import getpass
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PIPELINE_ROOT = ROOT.parent
RUNS_DIR = ROOT / "runs"
REAL_CONFIRMATION = "SPEND_COMFYDEPLOY_CREDITS"
REAL_ENV_GATE = "ARAQUE_ALLOW_GPU_EXECUTION"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


SECRET_LABELS = {
    "COMFYDEPLOY_API_KEY": "ComfyDeploy API key (https://www.comfydeploy.com -> API Keys)",
    "COMFYDEPLOY_DEPLOYMENT_ID": "ComfyDeploy deployment id (el workflow que desplegaste)",
}


def _mask(value: str) -> str:
    if not value:
        return "(vacio)"
    return value[0] + "***" if len(value) <= 8 else f"{value[:4]}...{value[-2:]}"


def require_secret(name: str, env_path: Path = None) -> str:
    """Devuelve `name` del entorno/.env. Si falta y hay terminal, lo pide de
    forma segura, ofrece guardarlo en .env local, y nunca imprime la clave."""
    value = os.getenv(name, "").strip()
    if value:
        return value
    label = SECRET_LABELS.get(name, name)
    if not sys.stdin.isatty():
        raise RuntimeError(
            f"Falta {name} y no hay terminal interactiva. "
            f"Definelo en el entorno o en pipeline/.env. ({label})"
        )
    print(f"\n[!] Falta {name}.\n    Para que sirve: {label}")
    value = getpass.getpass(f"    Pega {name} (entrada oculta): ").strip()
    if not value:
        raise RuntimeError(f"No se ingreso {name}.")
    answer = input("    Guardar en pipeline/.env local? [s/N]: ").strip().lower()
    if answer in ("s", "si", "y", "yes"):
        target = env_path or (PIPELINE_ROOT / ".env")
        with open(target, "a", encoding="utf-8") as fh:
            fh.write(f"\n{name}={value}\n")
        print(f"    OK guardada en {target} (.env esta en .gitignore).")
    os.environ[name] = value
    print(f"    Usando {name}={_mask(value)} en esta sesion.")
    return value


def slugify(value: str) -> str:
    clean = []
    for char in value.lower():
        if char.isalnum():
            clean.append(char)
        elif char in (" ", "-", "_"):
            clean.append("-")
    slug = "".join(clean).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "run"


def make_run_id(brief: dict) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{slugify(brief.get('brand', 'brand'))}-{stamp}"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def resolve_dimensions(fmt: str) -> tuple[int, int]:
    if fmt == "16:9":
        return 1920, 1080
    if fmt == "1:1":
        return 1080, 1080
    return 1080, 1920


def build_comfydeploy_payload(brief: dict) -> dict:
    return {
        "deployment_id": os.getenv("COMFYDEPLOY_DEPLOYMENT_ID", ""),
        "brand": brief.get("brand"),
        "title": brief.get("title"),
        "style": brief.get("style"),
        "duration_seconds": brief.get("duration_seconds"),
        "inputs": brief.get("comfydeploy_inputs", {}),
    }


def comfydeploy_run_url() -> str:
    deployment_id = os.getenv("COMFYDEPLOY_DEPLOYMENT_ID", "")
    explicit = os.getenv("COMFYDEPLOY_RUN_URL", "").strip()
    if explicit:
        return explicit.format(deployment_id=deployment_id)
    base = os.getenv("COMFYDEPLOY_API_BASE", "https://api.comfydeploy.com/api").rstrip("/")
    return f"{base}/deployments/{deployment_id}/runs"


def call_comfydeploy(payload: dict) -> dict:
    api_key = os.getenv("COMFYDEPLOY_API_KEY", "").strip()
    deployment_id = os.getenv("COMFYDEPLOY_DEPLOYMENT_ID", "").strip()
    if not api_key:
        raise RuntimeError("COMFYDEPLOY_API_KEY is missing")
    if not deployment_id:
        raise RuntimeError("COMFYDEPLOY_DEPLOYMENT_ID is missing")

    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        comfydeploy_run_url(),
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def assert_real_execution_allowed(confirm_cost: str = None) -> None:
    if confirm_cost != REAL_CONFIRMATION:
        raise RuntimeError(
            f"Corrida real bloqueada: usa --confirm-cost {REAL_CONFIRMATION}."
        )
    if os.getenv(REAL_ENV_GATE, "").strip() != "1":
        raise RuntimeError(
            f"Corrida real bloqueada: define {REAL_ENV_GATE}=1 sólo durante producción aprobada."
        )


def extract_asset_urls(response: dict) -> list[str]:
    urls = []

    def walk(value):
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            if any(value.lower().split("?")[0].endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp", ".mp4", ".webm", ".mov")):
                urls.append(value)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(response)
    return urls


def extension_from_url(url: str) -> str:
    clean = url.split("?", 1)[0].lower()
    for ext in (".png", ".jpg", ".jpeg", ".webp", ".mp4", ".webm", ".mov"):
        if clean.endswith(ext):
            return ext
    return ".asset"


def download_assets(urls: list[str], assets_dir: Path) -> list[dict]:
    assets = []
    assets_dir.mkdir(parents=True, exist_ok=True)
    for idx, url in enumerate(urls, start=1):
        ext = extension_from_url(url)
        local = assets_dir / f"comfydeploy-{idx:02d}{ext}"
        urllib.request.urlretrieve(url, local)
        assets.append({"kind": "remote", "source_url": url, "path": str(local)})
    return assets


def make_mock_assets(assets_dir: Path, width: int, height: int) -> list[dict]:
    assets_dir.mkdir(parents=True, exist_ok=True)
    svg_path = assets_dir / "mock-background.svg"
    svg_path.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#101114"/>
  <rect x="{width * 0.08}" y="{height * 0.1}" width="{width * 0.84}" height="{height * 0.8}" rx="32" fill="#1b1f28"/>
  <circle cx="{width * 0.75}" cy="{height * 0.25}" r="{min(width, height) * 0.18}" fill="#2dd4bf" opacity="0.35"/>
  <circle cx="{width * 0.25}" cy="{height * 0.72}" r="{min(width, height) * 0.22}" fill="#f97316" opacity="0.28"/>
  <text x="{width * 0.5}" y="{height * 0.48}" text-anchor="middle" fill="#f8fafc" font-size="{max(48, width // 15)}" font-family="Arial" font-weight="700">COMFYDEPLOY</text>
  <text x="{width * 0.5}" y="{height * 0.54}" text-anchor="middle" fill="#cbd5e1" font-size="{max(28, width // 28)}" font-family="Arial">mock asset for portable testing</text>
</svg>
""",
        encoding="utf-8",
    )
    return [{"kind": "mock", "path": str(svg_path)}]


def asset_src_for_html(asset_path: Path, html_dir: Path) -> str:
    return Path(os.path.relpath(asset_path, html_dir)).as_posix()


def generate_hyperframes_project(run_dir: Path, brief: dict, assets: list[dict]) -> Path:
    hf_dir = run_dir / "hyperframes"
    assets_out = hf_dir / "assets"
    assets_out.mkdir(parents=True, exist_ok=True)

    width, height = resolve_dimensions(brief.get("format", "9:16"))
    duration = float(brief.get("duration_seconds", 12))
    copied_assets = []
    for item in assets:
        src = Path(item["path"])
        target = assets_out / src.name
        if src.resolve() != target.resolve():
            shutil.copy2(src, target)
        copied_assets.append(target)

    background = copied_assets[0] if copied_assets else None
    background_src = asset_src_for_html(background, hf_dir) if background else ""
    captions = brief.get("captions") or []
    captions_json = json.dumps(captions, ensure_ascii=False)

    index = hf_dir / "index.html"
    index.write_text(
        f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{brief.get('title', 'Araque video')}</title>
    <style>
      html, body {{
        margin: 0;
        width: 100%;
        height: 100%;
        background: #101114;
        font-family: Inter, sans-serif;
      }}
      #root {{
        width: {width}px;
        height: {height}px;
        overflow: hidden;
        position: relative;
        background: #101114;
        color: #f8fafc;
      }}
      .bg {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: 1;
      }}
      .shade {{
        position: absolute;
        inset: 0;
        background:
          radial-gradient(circle at 72% 18%, rgba(45, 212, 191, 0.34), transparent 28%),
          linear-gradient(180deg, rgba(16,17,20,0.12), rgba(16,17,20,0.68));
        z-index: 2;
      }}
      .content {{
        position: absolute;
        inset: 0;
        z-index: 3;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
        padding: {int(height * 0.07)}px {int(width * 0.07)}px;
      }}
      .brand {{
        font-size: {max(24, int(width * 0.032))}px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 800;
        color: #2dd4bf;
      }}
      .title {{
        max-width: {int(width * 0.86)}px;
        font-size: {max(58, int(width * 0.088))}px;
        line-height: 0.96;
        font-weight: 900;
        letter-spacing: 0;
        text-wrap: balance;
      }}
      .subtitle {{
        margin-top: 20px;
        max-width: {int(width * 0.82)}px;
        font-size: {max(28, int(width * 0.038))}px;
        line-height: 1.18;
        color: #dbeafe;
        font-weight: 650;
      }}
      .caption-layer {{
        position: absolute;
        left: {int(width * 0.06)}px;
        right: {int(width * 0.06)}px;
        bottom: {int(height * 0.055)}px;
        height: {int(height * 0.19)}px;
        z-index: 5;
      }}
      .caption-contrast {{
        position: absolute;
        left: {int(width * 0.06)}px;
        right: {int(width * 0.06)}px;
        bottom: {int(height * 0.055)}px;
        height: {int(height * 0.19)}px;
        border-radius: 28px;
        background: rgba(0, 0, 0, 0.48);
        backdrop-filter: blur(12px);
        z-index: 4;
      }}
      .caption {{
        position: absolute;
        inset: 0;
        width: 100%;
        box-sizing: border-box;
        padding: 0 {int(width * 0.03)}px;
        text-align: center;
        font-size: {max(38, int(width * 0.046))}px;
        line-height: 1.05;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 4px 22px rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transform: translateY(18px) scale(0.98);
      }}
      .footer {{
        align-self: flex-start;
        padding: 12px 18px;
        border: 1px solid rgba(255,255,255,0.18);
        color: #e2e8f0;
        background: rgba(15,23,42,0.42);
        font-size: {max(20, int(width * 0.026))}px;
        font-weight: 700;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-no-timeline data-start="0" data-width="{width}" data-height="{height}" data-duration="{duration}" data-track-index="0">
      <img id="bg" class="bg" src="{background_src}" />
      <div class="shade"></div>
      <div class="content">
        <div class="brand">{brief.get('brand', 'Araque Solutions')}</div>
        <main>
          <div id="title" class="title">{brief.get('title', '')}</div>
          <div id="subtitle" class="subtitle">{brief.get('subtitle', '')}</div>
        </main>
        <div id="footer" class="footer">ComfyDeploy + HyperFrames</div>
      </div>
      <div class="caption-contrast"></div>
      <div id="caption-layer" class="caption-layer"></div>
    </div>
    <script>
      const captions = {captions_json};
      const layer = document.getElementById("caption-layer");
      captions.forEach((group, idx) => {{
        const el = document.createElement("div");
        el.id = "caption-" + idx;
        el.className = "caption";
        el.textContent = group.text;
        layer.appendChild(el);
      }});

      const durationMs = {duration * 1000};
      function animateHeldEntrance(selector, delaySec, enterSec, x, y) {{
        const delay = delaySec / {duration};
        const entered = (delaySec + enterSec) / {duration};
        const exit = Math.max(entered, ({duration} - 0.45) / {duration});
        const transform = `translate3d(${{x}}px, ${{y}}px, 0)`;
        const animation = document.querySelector(selector).animate(
          [
            {{ opacity: 0, transform, offset: 0 }},
            {{ opacity: 0, transform, offset: delay }},
            {{ opacity: 1, transform: "translate3d(0, 0, 0)", offset: entered }},
            {{ opacity: 1, transform: "translate3d(0, 0, 0)", offset: exit }},
            {{ opacity: 0, transform: "translate3d(0, -12px, 0)", offset: 1 }},
          ],
          {{ duration: durationMs, easing: "linear", fill: "both", iterations: 1 }},
        );
        animation.pause();
      }}

      const backgroundAnimation = document.getElementById("bg").animate(
        [
          {{ transform: "scale(1.08)", offset: 0 }},
          {{ transform: "scale(1)", offset: 1 }},
        ],
        {{ duration: durationMs, easing: "linear", fill: "both", iterations: 1 }},
      );
      backgroundAnimation.pause();
      animateHeldEntrance(".brand", 0.2, 0.6, 0, -28);
      animateHeldEntrance("#title", 0.45, 0.7, 0, 42);
      animateHeldEntrance("#subtitle", 0.75, 0.55, 0, 32);
      animateHeldEntrance("#footer", 1.1, 0.5, -28, 0);

      captions.forEach((group, idx) => {{
        const start = Number(group.start || 0);
        const end = Number(group.end || start + 1.8);
        const captionDuration = Math.max(0.3, end - start);
        const animation = document.getElementById("caption-" + idx).animate(
          [
            {{ opacity: 0, transform: "translate3d(0, 18px, 0) scale(0.98)", offset: 0 }},
            {{ opacity: 1, transform: "translate3d(0, 0, 0) scale(1)", offset: Math.min(0.12, 0.16 / captionDuration) }},
            {{ opacity: 1, transform: "translate3d(0, 0, 0) scale(1)", offset: Math.max(0.7, 1 - 0.12 / captionDuration) }},
            {{ opacity: 0, transform: "translate3d(0, -12px, 0) scale(0.98)", offset: 1 }},
          ],
          {{
            duration: captionDuration * 1000,
            delay: start * 1000,
            easing: "linear",
            fill: "both",
            iterations: 1,
          }},
        );
        animation.pause();
      }});
    </script>
  </body>
</html>
""",
        encoding="utf-8",
    )

    package_json = {
        "private": True,
        "scripts": {
            "lint": "hyperframes lint",
            "check": "hyperframes check",
            "preview": "hyperframes preview",
            "render": "hyperframes render --output output.mp4",
        },
        "devDependencies": {"hyperframes": "^0.7.18"},
        "engines": {"node": ">=22"},
    }
    write_json(hf_dir / "package.json", package_json)
    return hf_dir


def render_hyperframes(hf_dir: Path) -> None:
    command = ["npx", "hyperframes", "render", "--output", "output.mp4"]
    subprocess.run(command, cwd=hf_dir, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Portable ComfyDeploy + HyperFrames pipeline")
    parser.add_argument("--brief", required=True, help="Path to brief JSON")
    parser.add_argument("--run-id", default=None, help="Reuse a specific run id")
    parser.add_argument("--mock-assets", action="store_true", help="Use generated placeholder assets instead of ComfyDeploy")
    parser.add_argument("--skip-render", action="store_true", help="Build HyperFrames project but do not render MP4")
    parser.add_argument("--execute-real", action="store_true", help="Allow a real ComfyDeploy POST after safety gates")
    parser.add_argument("--confirm-cost", default=None, help="Required acknowledgement for credit spending")
    args = parser.parse_args()

    load_env_file(PIPELINE_ROOT / ".env")
    brief_path = Path(args.brief).resolve()
    brief = read_json(brief_path)
    run_id = args.run_id or make_run_id(brief)
    run_dir = RUNS_DIR / run_id
    assets_dir = run_dir / "source-assets"
    run_dir.mkdir(parents=True, exist_ok=True)

    width, height = resolve_dimensions(brief.get("format", "9:16"))

    # Para una corrida real necesitamos las claves de ComfyDeploy. Si faltan y
    # hay terminal, se piden de forma segura (no afecta el modo --mock-assets).
    if not args.mock_assets:
        if not args.execute_real:
            raise RuntimeError(
                "Corrida real bloqueada por defecto. Usa --execute-real sólo en producción aprobada."
            )
        assert_real_execution_allowed(args.confirm_cost)
        require_secret("COMFYDEPLOY_API_KEY")
        require_secret("COMFYDEPLOY_DEPLOYMENT_ID")

    payload = build_comfydeploy_payload(brief)
    write_json(run_dir / "comfydeploy_payload.json", payload)

    if args.mock_assets:
        response = {"status": "mock", "created_at": datetime.now(timezone.utc).isoformat()}
        assets = make_mock_assets(assets_dir, width, height)
    else:
        response = call_comfydeploy(payload)
        urls = extract_asset_urls(response)
        if not urls:
            raise RuntimeError("ComfyDeploy response did not include downloadable media URLs")
        assets = download_assets(urls, assets_dir)

    hf_dir = generate_hyperframes_project(run_dir, brief, assets)
    manifest = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "brief": str(brief_path),
        "mock_assets": args.mock_assets,
        "skip_render": args.skip_render,
        "hyperframes_dir": str(hf_dir),
        "assets": assets,
        "comfydeploy_response": response,
    }
    write_json(run_dir / "manifest.json", manifest)

    if not args.skip_render:
        render_hyperframes(hf_dir)

    print(f"Run created: {run_dir}")
    if args.skip_render:
        print(f"HyperFrames project ready: {hf_dir}")
    else:
        print(f"Rendered video: {hf_dir / 'output.mp4'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
