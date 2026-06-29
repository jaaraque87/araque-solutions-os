"""
Helper de secretos para el pipeline.

Detecta variables de entorno faltantes, las pide de forma segura (entrada
oculta), permite guardarlas en un .env local SOLO con autorización del usuario,
nunca imprime la clave completa y nunca commitea el .env.

Mantiene compatibilidad total con el .env actual: si la variable ya existe en
el entorno (cargada por el loader del pipeline), se devuelve tal cual.

Uso:
    from lib.secrets import get_secret
    fal = get_secret("FAL_KEY")
"""

import os
import getpass
from pathlib import Path

# Para qué sirve cada clave (se muestra al usuario si falta).
SECRET_LABELS = {
    "FAL_KEY": "fal.ai — Kling, Seedance, GPT Image 2",
    "FAL_API_KEY": "fal.ai — alias del SDK",
    "OPENAI_API_KEY": "OpenAI — GPT Image 2 (BYOK)",
    "GEMINI_API_KEY": "Google Gemini — guion + TTS",
    "ELEVENLABS_API_KEY": "ElevenLabs — voz (speech-to-speech)",
    "KIE_API_KEY": "Kie.ai / Suno — música",
    "COMFYDEPLOY_API_KEY": "ComfyDeploy — render en la nube",
    "SUBMAGIC_API_KEY": "Submagic — subtítulos / finishing",
    "SUPABASE_URL": "Supabase — URL del proyecto (rama NORA)",
    "SUPABASE_KEY": "Supabase — service key (rama NORA)",
}


def _mask(value: str) -> str:
    """Enmascara la clave para no imprimirla completa nunca."""
    if not value:
        return "(vacío)"
    if len(value) <= 8:
        return value[0] + "***"
    return f"{value[:4]}…{value[-2:]}"


def get_secret(name, label=None, env_path=Path(".env"), interactive=True):
    """Devuelve el valor de `name`. Si falta y hay TTY, lo pide de forma segura."""
    value = os.getenv(name)
    if value:
        return value

    label = label or SECRET_LABELS.get(name, name)
    print(f"\n⚠️  Falta la variable {name}.")
    print(f"   Para qué sirve: {label}")

    if not interactive:
        raise RuntimeError(
            f"Falta {name} y el modo no es interactivo. "
            f"Define {name} en el entorno o en un .env local."
        )

    value = getpass.getpass(f"   Pega {name} (entrada oculta): ").strip()
    if not value:
        raise RuntimeError(f"No se ingresó {name}.")

    answer = input("   ¿Guardar en .env local? [s/N]: ").strip().lower()
    if answer in ("s", "si", "sí", "y", "yes"):
        with env_path.open("a", encoding="utf-8") as f:
            f.write(f"\n{name}={value}\n")
        print(f"   ✅ Guardada en {env_path} (recuerda: .env está en .gitignore).")

    os.environ[name] = value
    print(f"   Usando {name}={_mask(value)} en esta sesión.")
    return value
