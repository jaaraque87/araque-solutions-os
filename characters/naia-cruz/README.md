# Naia Cruz — Imagen oficial de Araque Solutions

Avatar creado desde cero. Es la cara y la voz de la agencia en reels, demos comerciales y contenido de autoridad. Para clientes se crean personajes propios; Naia es exclusiva de la marca Araque Solutions.

## Identidad

- Nombre público: **Naia Cruz**
- Rol: imagen oficial de la agencia (IG + TikTok @araquesolutions)
- Tipo: avatar IA original (no basado en persona real)

## Voz

- Proveedor: ElevenLabs (voice cloned)
- Voice ID: `rzpLrJDiI1CBeAvkbjNf` (nombre interno en ElevenLabs: "KENZA VOZ" — pendiente renombrar a Naia Cruz)
- Canon completo de dirección vocal: [`brand/araque/voice/VOICE.md`](../../brand/araque/voice/VOICE.md)
- Sample de referencia: [`brand/araque/voice/samples/naia-cruz-referencia.mp3`](../../brand/araque/voice/samples/naia-cruz-referencia.mp3) (33s)
- API key: variable de entorno `ELEVENLABS_API_KEY` en `.env` local (NUNCA se comitea)

## Animación / video

Naia se anima por cualquiera de estas vías, según la pieza:

| Vía | Cuándo usarla | Dónde |
|---|---|---|
| ComfyDeploy + LTX 2.3 Director | Reels con lipsync nativo (audio ElevenLabs como input) | `pipeline/comfydeploy_hyperframes/` + `workflows/` |
| RunPod ComfyUI directo | Control total, iteración de workflows | `infrastructure/` |
| fal.ai (Kling / Seedance) | Motion rápido sin pod, b-roll del avatar | `tools/fal-jobs/avatar_naia.mjs`, `seedance_naia.mjs` |

Post-producción (overlays de marca, hook, CTA):
`tools/content-reel-lab/scripts/render-ltx-avatar-original-audio.mjs` (unitario) o `render-batch.mjs` (lote).

## Reglas de uso

- Todo reel de agencia lleva la voz oficial — no mezclar voces en contenido de Naia.
- El guion sigue `.claude/skills/guion-ugc` + `.claude/skills/script-framework`; los hooks salen de `.claude/skills/hook-lab`.
- Los créditos ElevenLabs se gastan SOLO con autorización explícita del dueño.
