"""
Step 01 — Guión (Script Generator)
====================================
Uses Gemini Pro to generate a full UGC video script.

Input:   run_dir/brand_profile.json
Output:  run_dir/guion.json

Guion schema:
{
  "brand": "Kenza",
  "num_scenes": 6,
  "video_concept": "...",
  "hook": "...",
  "scenes": [
    {
      "scene_id": 1,
      "angle": "problema/solución/testimonial/...",
      "location": "Miami waterfront",
      "outfit": "crochet top blanco + denim",
      "action": "talking to camera, gesturing",
      "dialogue": "Texto que dice Kenza en esta escena...",
      "duration_s": 8,
      "caption": "Subtitle / caption text for this clip",
      "product_mention": false,
      "brief_visual": "Descripción visual para generación de imagen"
    }
  ],
  "cta": "Sigue a @kenza para más contenido!",
  "music_mood": "upbeat, tropical, positive",
  "total_duration_s": 48
}
"""

import json
import os
from pathlib import Path

import google.generativeai as genai


SYSTEM_PROMPT = """Eres un experto en creación de contenido UGC (User Generated Content)
para redes sociales. Creas guiones auténticos, naturales y altamente efectivos para
influencers virtuales de IA. Tu contenido suena humano, empoderado y conversacional —
nunca robótico. Especializas en contenido para Instagram Reels y TikTok."""


def _build_prompt(profile: dict, num_scenes: int) -> str:
    persona = profile.get("persona", {})
    visual = profile.get("visual_identity", {})
    guidelines = profile.get("content_guidelines", {})
    product = profile.get("product", {})

    locations = visual.get("locations", ["Miami waterfront"])
    loc_list = ", ".join(locations)

    return f"""
Crea un guión UGC completo para {num_scenes} escenas para la influencer virtual "{persona.get('name', 'Kenza')}".

PERFIL DE PERSONAJE:
- Arquetiopo: {persona.get('archetype', 'Miami lifestyle creator')}
- Voz: {persona.get('voice', 'casual, empoderada, auténtica')}
- Apariencia: {persona.get('appearance', 'bob negro, ojos verdes, piel blanca/olive')}

IDENTIDAD VISUAL:
- Estilo: {visual.get('style', 'iPhone UGC, golden hour')}
- Locaciones disponibles: {loc_list}
- Iluminación: {visual.get('lighting', 'golden hour, natural')}

PRODUCTO/MARCA:
- Categoría: {product.get('category', 'lifestyle')}
- Nombre: {product.get('name', '')}
- USP: {product.get('usp', '')}

GUÍAS DE CONTENIDO:
- Tono: {guidelines.get('tone', 'auténtico, casual')}
- Evitar: {', '.join(guidelines.get('avoid', []))}

INSTRUCCIONES:
1. El hook debe ser en los primeros 3 segundos, llamativo
2. Cada escena debe tener 7-10 segundos de diálogo natural
3. Los diálogos deben sonar HUMANOS, no robóticos — usa contracciones, pausas naturales
4. Varía los ángulos: puede ser testimonial, lifestyle, tutorial, aspiracional
5. El dialogue es solo el texto hablado (para TTS), sin stage directions
6. El brief_visual es para generar la imagen: describe pose, outfit, locación, acción visual
7. La locación debe ser una de: {loc_list}

Devuelve SOLAMENTE un JSON válido con este esquema exacto:
{{
  "brand": "{profile.get('brand', 'Kenza')}",
  "num_scenes": {num_scenes},
  "video_concept": "concepto del video en 1 oración",
  "hook": "texto del hook (primeras palabras del video)",
  "scenes": [
    {{
      "scene_id": 1,
      "angle": "tipo de ángulo (testimonial/lifestyle/tutorial/aspiracional/cta)",
      "location": "nombre de la locación",
      "outfit": "descripción del outfit",
      "action": "acción visual (ej: talking to camera, walking, gesturing)",
      "dialogue": "Texto hablado completo para esta escena. Natural, conversacional.",
      "duration_s": 8,
      "caption": "Caption/subtítulo corto para esta escena",
      "product_mention": false,
      "brief_visual": "Descripción detallada para generación de imagen: pose, outfit, locación, luz, encuadre"
    }}
  ],
  "cta": "call to action final",
  "music_mood": "descripción del mood musical (ej: upbeat tropical, chill vibes)",
  "total_duration_s": 48
}}

Devuelve SOLO el JSON, sin markdown, sin explicaciones. {num_scenes} escenas exactas.
"""


def run(ctx: dict) -> dict:
    brand: str       = ctx["brand"]
    run_dir: Path    = ctx["run_dir"]
    num_scenes: int  = ctx["num_scenes"]
    console          = ctx["console"]

    # Load brand profile
    profile_path = run_dir / "brand_profile.json"
    if not profile_path.exists():
        # Try canonical brands dir
        profile_path = ctx["brands_dir"] / brand / "brand_profile.json"
    if not profile_path.exists():
        raise FileNotFoundError(f"brand_profile.json not found. Run step 00 first.")

    profile = json.loads(profile_path.read_text(encoding="utf-8"))

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        "gemini-2.0-flash",
        system_instruction=SYSTEM_PROMPT
    )

    console.print(f"  Generando guión para [bold]{brand}[/bold] — {num_scenes} escenas...")

    prompt = _build_prompt(profile, num_scenes)
    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    guion = json.loads(raw)

    # Ensure field consistency
    guion["brand"] = brand
    guion["num_scenes"] = len(guion.get("scenes", []))

    # Renumber scene_ids just in case
    for i, scene in enumerate(guion.get("scenes", []), 1):
        scene["scene_id"] = i
        scene.setdefault("duration_s", 8)

    guion["total_duration_s"] = sum(s.get("duration_s", 8) for s in guion.get("scenes", []))

    # Save
    out_path = run_dir / "guion.json"
    out_path.write_text(json.dumps(guion, indent=2, ensure_ascii=False), encoding="utf-8")

    console.print(f"  [green]✓[/green] guion.json → {guion['num_scenes']} escenas, "
                  f"~{guion['total_duration_s']}s total")
    console.print(f"  [dim]Hook: \"{guion.get('hook', '')}\"[/dim]")

    return {
        "status": "ok",
        "cost_usd": 0.01,
        "guion_path": str(out_path),
        "num_scenes": guion["num_scenes"],
        "total_duration_s": guion["total_duration_s"],
        "hook": guion.get("hook", ""),
    }
