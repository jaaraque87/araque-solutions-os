"""
Kenza UGC Pipeline — Dependency installer
Run once: python setup.py
"""

import subprocess
import sys
from pathlib import Path

PACKAGES = [
    # fal.ai — Morpheus (GPT Image 2 Edit), Kling, Sync
    "fal-client>=0.5.0",
    # Google Gemini — Brand Analyzer + TTS
    "google-generativeai>=0.8.0",
    # HTTP — Kie.ai (Suno), ElevenLabs, general
    "requests>=2.32.0",
    # FFmpeg wrapper — Assembly step
    "ffmpeg-python>=0.2.0",
    # .env loading
    "python-dotenv>=1.0.0",
    # Terminal UI — progress bars, tables, status
    "rich>=13.7.0",
    # CLI argument parsing helper
    "click>=8.1.0",
    # JSON schema validation for run.json / brand_profile.json
    "jsonschema>=4.23.0",
    # Async HTTP (used by fal polling and Kling)
    "httpx>=0.27.0",
    # Image utils — resize refs before uploading to fal
    "Pillow>=10.4.0",
    # Dashboard API server
    "fastapi>=0.111.0",
    "uvicorn[standard]>=0.30.0",
    "python-multipart>=0.0.9",
]

DEV_PACKAGES = [
    "pytest>=8.0.0",
    "black>=24.0.0",
]


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, check=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main() -> None:
    from rich.console import Console
    from rich.panel import Panel

    console = Console()
    console.print(Panel("[bold cyan]Kenza UGC Pipeline — Setup[/bold cyan]", expand=False))

    console.print("\n[yellow]Installing dependencies...[/yellow]")
    run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    run([sys.executable, "-m", "pip", "install"] + PACKAGES)

    # Check for ffmpeg binary (required by assembly step)
    console.print("\n[yellow]Checking ffmpeg binary...[/yellow]")
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    if result.returncode == 0:
        console.print("[green]✓ ffmpeg found[/green]")
    else:
        console.print(
            "[red]✗ ffmpeg not found in PATH.[/red]\n"
            "  Install it: https://ffmpeg.org/download.html  (or: winget install Gyan.FFmpeg)"
        )

    # Create .env from .env.example if it doesn't exist
    env_file = Path(__file__).parent / ".env"
    env_example = Path(__file__).parent / ".env.example"
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text(encoding="utf-8"), encoding="utf-8")
        console.print(f"\n[green]✓ .env created from .env.example — fill in your API keys.[/green]")
    elif env_file.exists():
        console.print(f"\n[dim].env already exists — skipped[/dim]")

    console.print("\n[bold green]Setup complete.[/bold green]")
    console.print("Next: edit [cyan].env[/cyan] with your API keys, then run [cyan]python run.py --brand Kenza --steps all[/cyan]\n")


if __name__ == "__main__":
    # Rich may not be installed yet on first run — install core deps quietly first
    try:
        from rich.console import Console  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "rich", "click"], check=True)

    main()
