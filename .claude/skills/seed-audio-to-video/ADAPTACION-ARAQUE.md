# Adaptación a Araque Solutions

Skill de origen: Morfeo Academy (Paul de Lavallaz). Actualizada 2026-07-12 con el pack completo `seed-audio-to-video-skill-20260707.zip`. Cambios para operar aquí:

1. **"Paul" = el dueño (Jhon / Araque Solutions).** Todos los gates (GATE 1-4) validan con él. La regla de oro se mantiene: pipeline GATED, nunca corre de punta a punta sola, y cada generación en fal/OpenAI GASTA — pedir autorización explícita antes de cada paso que consuma créditos.
2. **✅ PACK COMPLETO instalado (2026-07-12)** — ya no está incompleto: `scripts/seed_audio_gen.py`, `scripts/seed_audio_mix.py`, `scripts/stills_lab.py` en `scripts/` de la raíz; `_research/seed-audio/README.md` (base de conocimiento de prompting Seed Audio); y las 4 skills de soporte en `.claude/skills/`: **`seedance-fal`** (runner del Paso 4, path ya corregido en SKILL.md), **`seedance-prompter`** (T2V puro sin audio + master-knowledge de 32KB), **`krea-2-large-api`** (assets fuente t2i, Paso 0.5), **`facs-acting-direction`** (dirección actoral facial anatómica para stills — usable TAMBIÉN fuera de este pipeline, en cualquier prompt de imagen con cara).
3. **Keys** (`.env` raíz, gitignoreado): `FAL_API_KEY` (todo corre por fal: GPT Image 2 + Seed Audio 1.0 + Seedance 2.0) y `OPENAI_API_KEY` (Whisper API para QA de diálogo y beats — ⚠ NO configurada aún). `KREA_API_KEY` solo si se usa el Paso 0.5.
4. **Identidad**: el zip excluye los assets biométricos de Paul a propósito. El MÉTODO (pack de 4 fotos + IDENTITY LOCK + TTS→STS) se replica con **Naia** (character sheet + voz ElevenLabs `rzpLrJDiI1CBeAvkbjNf`) o con el personaje del cliente.
5. **Regla clave del formato: el audio manda** — el video dura lo que dura el audio, tope 15s. La escena sonora se diseña para ≤15s desde el arranque.
6. **Run dirs**: usar `tools/content-reel-lab/outputs/seed-audio-video/` (los outputs no se comitean).
7. **Uso en la agencia (dónde encaja vs las otras vías):**
   - **LTX/ComfyDeploy** = reels seriados baratos de Naia (voz ElevenLabs, multi-escena, ~$0.30-0.80)
   - **Seed-audio-to-video (fal)** = la pieza PREMIUM: mini-escenas dramatizadas con diálogo nativo + ambiente + SFX en una pasada — anuncios narrativos de clientes (normalidad → giro → reacción → clímax), el producto "Clon/vocero alto ticket". Costo ~$0.30/s 720p → escena de 12s ≈ $3.6. Se cobra como pieza hero ($40-80), no como reel de volumen.
   - **facs-acting-direction** = upgrade transversal GRATIS a todos los prompts de imagen con rostro (first frames de Naia, retratos de clientes): anatomía facial en vez de "make her sad".
   - Costos Seedance en memoria: 720p $0.3024/s, 1080p $0.682/s, con video input ×0.6.
