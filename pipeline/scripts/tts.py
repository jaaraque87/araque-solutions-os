"""
Step 05 — TTS (Text-to-Speech)
================================
Generates voice audio for each scene using Google Gemini Flash TTS.

Input:   run_dir/guion.json
         run_dir/brand_profile.json
Output:  run_dir/tts_scene_N.wav  (one per scene)

Voice: Leda (default for Kenza) — configurable via brand_profile.json

Cost: ~$0.02 total (Gemini TTS is very cheap)

Gemini TTS API (google-genai >= 1.0):
  Uses gemini-2.5-flash-preview-tts model
  Supported voices: Zephyr, Puck, Charon, Kore, Fenrir, Leda, Orus, Aoede
"""

import json
import os
import struct
import wave
from pathlib import Path

import google.generativeai as genai
from google import genai as genai_new


def _write_wav(pcm_data: bytes, out_path: Path, sample_rate: int = 24000,
               channels: int = 1, sample_width: int = 2) -> None:
    """Write raw PCM bytes to a .wav file."""
    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_data)


def _generate_tts_new_api(text: str, voice: str, api_key: str) -> bytes:
    """
    Use the new google-genai library (v1+) with gemini-2.5-flash-preview-tts.
    Returns raw PCM audio bytes.
    """
    client = genai_new.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=text,
        config=genai_new.types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=genai_new.types.SpeechConfig(
                voice_config=genai_new.types.VoiceConfig(
                    prebuilt_voice_config=genai_new.types.PrebuiltVoiceConfig(
                        voice_name=voice,
                    )
                )
            ),
        ),
    )
    # Extract audio data
    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            return part.inline_data.data
    raise RuntimeError("No audio data in Gemini TTS response")


def _generate_tts_fallback(text: str, voice: str, api_key: str) -> bytes:
    """
    Fallback: older google-generativeai approach.
    Returns raw PCM bytes (may need wrapping).
    """
    genai.configure(api_key=api_key)
    # This model name may vary; use the preview TTS endpoint
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    # Unfortunately older SDK doesn't expose TTS natively — raise to signal use new API
    raise NotImplementedError("Use google-genai >= 1.0 for TTS support")


def run(ctx: dict) -> dict:
    brand: str    = ctx["brand"]
    run_dir: Path = ctx["run_dir"]
    console       = ctx["console"]

    # Load inputs
    guion_path = run_dir / "guion.json"
    if not guion_path.exists():
        raise FileNotFoundError("guion.json not found. Run step 01 first.")

    profile_path = run_dir / "brand_profile.json"
    if not profile_path.exists():
        profile_path = ctx["brands_dir"] / brand / "brand_profile.json"
    if not profile_path.exists():
        raise FileNotFoundError("brand_profile.json not found.")

    guion   = json.loads(guion_path.read_text(encoding="utf-8"))
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    scenes  = guion.get("scenes", [])

    voice = profile.get("tts_voice", "Leda")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set")

    console.print(f"  Voice: [bold]{voice}[/bold] — {len(scenes)} escenas")

    outputs = []
    total_cost = 0.0

    for scene in scenes:
        sid      = scene["scene_id"]
        dialogue = scene.get("dialogue", "").strip()

        if not dialogue:
            console.print(f"  [yellow]⚠  Escena {sid}: sin diálogo — omitiendo[/yellow]")
            continue

        console.print(f"  [dim]Escena {sid}: \"{dialogue[:60]}...\"[/dim]")

        try:
            pcm_bytes = _generate_tts_new_api(dialogue, voice, api_key)
        except Exception as e:
            console.print(f"  [red]✗ TTS falló escena {sid}: {e}[/red]")
            raise

        out_path = run_dir / f"tts_scene_{sid}.wav"
        _write_wav(pcm_bytes, out_path)

        file_size_kb = out_path.stat().st_size // 1024
        console.print(f"  [green]✓[/green] tts_scene_{sid}.wav ({file_size_kb} KB)")

        outputs.append({
            "scene_id": sid,
            "path": str(out_path),
            "duration_chars": len(dialogue),
        })
        total_cost += 0.002

    console.print(f"  [green]✓[/green] {len(outputs)} audios TTS generados — voice: {voice}")

    return {
        "status": "ok",
        "cost_usd": total_cost,
        "tts_files": outputs,
        "voice": voice,
        "num_generated": len(outputs),
    }
