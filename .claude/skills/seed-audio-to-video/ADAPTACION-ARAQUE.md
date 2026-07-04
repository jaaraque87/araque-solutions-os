# Adaptación a Araque Solutions

Skill de origen: Morfeo Academy (Paul de Lavallaz). Cambios para operar aquí:

1. **"Paul" = el dueño (Jhon / Araque Solutions).** Todos los gates (GATE 1-4) validan con él. La regla de oro se mantiene: pipeline GATED, nunca corre de punta a punta sola, y cada generación en fal/OpenAI GASTA — pedir autorización explícita antes de cada paso que consuma créditos.
2. **Keys**: `FAL_API_KEY` y `OPENAI_API_KEY` en el `.env` de la raíz de este repo (gitignoreado). Aún NO configuradas (2026-07-04).
3. **⚠ INCOMPLETO**: el SKILL.md referencia `scripts/seed_audio_gen.py` y `scripts/seed_audio_mix.py` y `_research/seed-audio/README.md` que NO venían en el zip. Fuente probable: classroom Morfeo (Skool). Hasta conseguirlos o reescribirlos, los pasos 2 y 4 no son ejecutables tal cual (el patrón de queue de fal está descrito y se puede reimplementar).
4. **Run dirs**: usar `tools/content-reel-lab/outputs/seed-audio-video/` (los outputs no se comitean).
5. **Uso en la agencia**: escenas costumbristas/dramáticas con diálogo — ideal para anuncios narrativos de clientes (patrón normalidad → giro → reacción → clímax), complementa el talking-head de Naia.
