"""
Step 06 — Voice Change (ElevenLabs STS)
=========================================
Applies ElevenLabs Speech-to-Speech to transform the Gemini TTS voice
into a richer, more natural voice that matches the character better.

Input:   run_dir/tts_scene_N.wav
         run_dir/brand_profile.json
Output:  run_dir/voice_scene_N.mp3  (one per scene)

Cost: ~$0.06 total (ElevenLabs STS charges per character)

Optional step — if ElevenLabs key is not set, copies TTS audio directly.
Model: eleven_multilingual_sts_v2
Voice ID: configurable via brand_profile.json → elevenlabs_voice_id
"""

import json
import os
import shutil
from pathlib import Path

import requests


ELEVENLABS_STS_URL = "https://api.elevenlabs.io/v1/speech-to-speech/{voice_id}"
DEFAULT_VOICE_ID   = "EXAVITQu4vr4xnSDxMaL"  # Bella — warm female voice
DEFAULT_MODEL      = "eleven_multilingual_sts_v2"


def _apply_sts(
    audio_path: Path,
    voice_id: str,
    model: str,
    api_key: str,
) -> bytes:
    """Call ElevenLabs STS and return MP3 bytes."""
    url = ELEVENLABS_STS_URL.format(voice_id=voice_id)
    headers = {"xi-api-key": api_key}

    with audio_path.open("rb") as f:
        files = {"audio": (audio_path.name, f, "audio/wav")}
        data = {
            "model_id": model,
            "voice_settings": json.dumps({
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.3,
                "use_speaker_boost": True,
            }),
        }
        response = requests.post(url, headers=headers, files=files, data=data, timeout=120)

    if response.status_code != 200:
        raise RuntimeError(
            f"ElevenLabs STS error {response.status_code}: {response.text[:200]}"
        )

    return response.content  # MP3 bytes


def run(ctx: dict) -> dict:
    brand: str    = ctx["brand"]
    run_dir: Path = ctx["run_dir"]
    console       = ctx["console"]

    # Load brand profile for voice settings
    profile_path = run_dir / "brand_profile.json"
    if not profile_path.exists():
        profile_path = ctx["brands_dir"] / brand / "brand_profile.json"

    profile = {}
    if profile_path.exists():
        profile = json.loads(profile_path.read_text(encoding="utf-8"))

    voice_id = profile.get("elevenlabs_voice_id", DEFAULT_VOICE_ID)
    model    = profile.get("elevenlabs_model", DEFAULT_MODEL)

    api_key = os.getenv("ELEVENLABS_API_KEY")

    # Find TTS input files
    tts_files = sorted(run_dir.glob("tts_scene_*.wav"))
    if not tts_files:
        raise FileNotFoundError("No tts_scene_*.wav files found. Run step 05 first.")

    console.print(f"  Voice ID: [bold]{voice_id}[/bold]  Model: {model}")
    console.print(f"  Procesando {len(tts_files)} archivos de audio...")

    outputs = []
    total_cost = 0.0

    for tts_path in tts_files:
        # Extract scene id from filename: tts_scene_1.wav → 1
        sid = tts_path.stem.replace("tts_scene_", "")
        out_path = run_dir / f"voice_scene_{sid}.mp3"

        if not api_key:
            # No API key → copy TTS directly, rename to voice_scene
            console.print(f"  [yellow]⚠  Sin ELEVENLABS_API_KEY — copiando TTS directo[/yellow]")
            shutil.copy2(tts_path, out_path.with_suffix(".wav"))
            # Rename output expectation to .wav since no conversion
            out_path = run_dir / f"voice_scene_{sid}.wav"
            outputs.append({"scene_id": sid, "path": str(out_path), "skipped": True})
            continue

        console.print(f"  [dim]Escena {sid}: aplicando STS...[/dim]")

        try:
            mp3_bytes = _apply_sts(tts_path, voice_id, model, api_key)
        except Exception as e:
            console.print(f"  [red]✗ STS falló escena {sid}: {e}[/red]")
            # Fallback: use original TTS
            shutil.copy2(tts_path, out_path.with_suffix(".wav"))
            out_path = run_dir / f"voice_scene_{sid}.wav"
            console.print(f"  [yellow]  → usando TTS original como fallback[/yellow]")
            outputs.append({"scene_id": sid, "path": str(out_path), "fallback": True})
            continue

        out_path.write_bytes(mp3_bytes)
        file_size_kb = out_path.stat().st_size // 1024
        console.print(f"  [green]✓[/green] voice_scene_{sid}.mp3 ({file_size_kb} KB)")

        outputs.append({"scene_id": sid, "path": str(out_path)})
        total_cost += 0.01  # ~$0.01 per short clip

    console.print(f"  [green]✓[/green] {len(outputs)} voice files procesados")

    return {
        "status": "ok",
        "cost_usd": total_cost,
        "voice_files": outputs,
        "voice_id": voice_id,
        "num_processed": len(outputs),
    }
