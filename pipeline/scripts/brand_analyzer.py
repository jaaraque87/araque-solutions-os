"""
Step 00 — Brand Analyzer
========================
Reads or creates a brand_profile.json for the given brand.

Input:   brands/{brand}/brand_profile.json  (if it exists)
         brands/{brand}/brief.txt           (optional raw brief)
Output:  brands/{brand}/brand_profile.json  (canonical)
         run_dir/brand_profile.json         (copy for this run)

Brand profile schema:
{
  "brand": "Kenza",
  "description": "...",
  "persona": { "name": "Kenza", "archetype": "...", "voice": "...", "age": "..." },
  "visual_identity": { "style": "...", "colors": [], "lighting": "..." },
  "audience": { "age_range": "...", "interests": [], "platform": "..." },
  "product": { "category": "...", "name": "...", "usp": "..." },
  "content_guidelines": { "tone": "...", "avoid": [], "hashtags": [] },
  "lora_trigger": "...",
  "reference_image": "BANANA_PRO_00006_.png"
}
"""

import json
import os
import shutil
from pathlib import Path

import google.generativeai as genai


# ── Default profile for Kenza (used if no brief exists) ──────────────────────
KENZA_DEFAULT: dict = {
    "brand": "Kenza",
    "description": "Kenza es una influencer virtual venezolana-ucraniana basada en Miami. "
                   "Crea contenido UGC lifestyle auténtico en español e inglés.",
    "persona": {
        "name": "Kenza",
        "archetype": "Lifestyle creator / Miami girl",
        "voice": "Casual, empoderada, auténtica. Mix español/inglés.",
        "age": "24-27 (aparente)",
        "appearance": "bob negro, ojos verdes, piel blanca/olive"
    },
    "visual_identity": {
        "style": "iPhone UGC, natural, golden hour",
        "colors": ["#F5E6D3", "#2C3E50", "#E8C98C"],
        "lighting": "golden hour, natural soft light",
        "locations": ["Miami waterfront", "South Beach", "Wynwood", "hotel rooftop"]
    },
    "audience": {
        "age_range": "18-35",
        "interests": ["moda", "lifestyle", "miami", "viajes", "belleza"],
        "platform": "Instagram / TikTok"
    },
    "product": {
        "category": "lifestyle / fashion / beauty",
        "name": "Kenza Brand",
        "usp": "Influencer virtual 100% IA, consistencia perfecta, costo $3.27/video"
    },
    "content_guidelines": {
        "tone": "auténtico, casual, empoderado — nunca robótico",
        "avoid": ["lenguaje formal", "tecnicismos", "política"],
        "hashtags": ["#Miami", "#UGC", "#LifestyleMiami", "#Kenza"]
    },
    "lora_trigger": "kenza",
    "lora_strength": 0.85,
    "reference_image": "BANANA_PRO_00006_.png",
    "tts_voice": "Leda",
    "elevenlabs_model": "eleven_multilingual_sts_v2"
}


def _load_or_create_profile(brands_dir: Path, brand: str, console) -> dict:
    """Load brand_profile.json, or generate one via Gemini from a brief, or use default."""
    brand_dir = brands_dir / brand
    brand_dir.mkdir(parents=True, exist_ok=True)
    profile_path = brand_dir / "brand_profile.json"

    # 1. Already exists → load it
    if profile_path.exists():
        console.print(f"[dim]  → Cargando perfil existente: {profile_path}[/dim]")
        return json.loads(profile_path.read_text(encoding="utf-8"))

    # 2. Brief exists → generate with Gemini
    brief_path = brand_dir / "brief.txt"
    if brief_path.exists():
        console.print("[dim]  → Generando brand_profile desde brief.txt con Gemini...[/dim]")
        return _generate_profile_from_brief(brief_path.read_text(encoding="utf-8"), brand, console)

    # 3. Default (Kenza) or empty skeleton
    if brand.lower() == "kenza":
        console.print("[dim]  → Usando perfil default de Kenza.[/dim]")
        return KENZA_DEFAULT.copy()

    # 4. Generic skeleton for new brands
    console.print(f"[yellow]  ⚠  No se encontró brief para '{brand}'. "
                  f"Crea brands/{brand}/brief.txt o brands/{brand}/brand_profile.json[/yellow]")
    return _empty_skeleton(brand)


def _generate_profile_from_brief(brief: str, brand: str, console) -> dict:
    """Call Gemini to parse a free-text brief into a structured brand_profile.json."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
Analiza este brief de marca y devuelve SOLAMENTE un JSON válido con el siguiente esquema:

{{
  "brand": "{brand}",
  "description": "descripción en 2-3 oraciones",
  "persona": {{
    "name": "nombre",
    "archetype": "arquetipo",
    "voice": "tono de voz",
    "age": "rango de edad aparente",
    "appearance": "descripción física"
  }},
  "visual_identity": {{
    "style": "estilo visual",
    "colors": ["#hex1", "#hex2"],
    "lighting": "tipo de iluminación",
    "locations": ["lugar1", "lugar2"]
  }},
  "audience": {{
    "age_range": "18-35",
    "interests": ["interés1", "interés2"],
    "platform": "Instagram / TikTok"
  }},
  "product": {{
    "category": "categoría",
    "name": "nombre del producto/marca",
    "usp": "propuesta de valor única"
  }},
  "content_guidelines": {{
    "tone": "descripción del tono",
    "avoid": ["evitar1", "evitar2"],
    "hashtags": ["#tag1", "#tag2"]
  }},
  "lora_trigger": "trigger word para LoRA",
  "lora_strength": 0.85,
  "reference_image": "",
  "tts_voice": "Leda",
  "elevenlabs_model": "eleven_multilingual_sts_v2"
}}

BRIEF:
{brief}

Devuelve SOLO el JSON, sin markdown, sin explicaciones.
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()
    # Strip ```json fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def _empty_skeleton(brand: str) -> dict:
    return {
        "brand": brand,
        "description": f"Influencer virtual — {brand}",
        "persona": {"name": brand, "archetype": "", "voice": "", "age": "", "appearance": ""},
        "visual_identity": {"style": "iPhone UGC", "colors": [], "lighting": "natural", "locations": []},
        "audience": {"age_range": "18-35", "interests": [], "platform": "Instagram / TikTok"},
        "product": {"category": "", "name": brand, "usp": ""},
        "content_guidelines": {"tone": "auténtico, casual", "avoid": [], "hashtags": []},
        "lora_trigger": brand.lower(),
        "lora_strength": 0.85,
        "reference_image": "",
        "tts_voice": "Leda",
        "elevenlabs_model": "eleven_multilingual_sts_v2"
    }


# ── Main entry point ──────────────────────────────────────────────────────────

def run(ctx: dict) -> dict:
    brand: str       = ctx["brand"]
    run_dir: Path    = ctx["run_dir"]
    brands_dir: Path = ctx["brands_dir"]
    console          = ctx["console"]

    console.print(f"  Brand: [bold]{brand}[/bold]")

    profile = _load_or_create_profile(brands_dir, brand, console)
    profile["brand"] = brand  # ensure field matches arg

    # Save / overwrite canonical profile
    brand_dir = brands_dir / brand
    brand_dir.mkdir(parents=True, exist_ok=True)
    canonical = brand_dir / "brand_profile.json"
    canonical.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"  [green]✓[/green] brand_profile.json → {canonical}")

    # Copy to run dir for traceability
    run_copy = run_dir / "brand_profile.json"
    shutil.copy2(canonical, run_copy)

    return {
        "status": "ok",
        "cost_usd": 0.0,
        "brand_profile_path": str(run_copy),
        "brand": brand,
    }
