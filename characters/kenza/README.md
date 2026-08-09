# Kenza — Influencer Virtual

**Tipo:** Venezuelan-Ukrainian · "Biker de Miami"  
**Descripción:** Bob negro, ojos verdes, piel blanca/olive, estilo UGC lifestyle Miami

---

## Identidad visual

- **Foto ganadora base:** `BANANA_PRO_00006_.png` — Miami waterfront, crochet top blanco + denim, full body, golden hour, iPhone UGC
- **Character sheet oficial:** `projects/kenza-lux-global-reveal/assets/keyframes/kenza-character-sheet-v2-official.png` — Kenza adulta de 23 años, frente, 3/4, perfil y espalda; identidad canónica aprobada por el usuario.
- **Rostro maestro hiperrealista:** `projects/kenza-lux-global-reveal/assets/portraits/kenza-master-face-v1-official.png` — variante B aprobada, camiseta negra básica de tiras finas estilo Naia; referencia principal para rostro y talking head.
- **Validación oficial en estudio de pódcast:** `projects/kenza-lux-global-reveal/assets/keyframes/kenza-podcast-identity-validation-v1.png` — vistas frontal, 3/4, lateral, perfil detallado y cuerpo completo; aprobada por el usuario.
- **Canon corporal estable:** figura reloj de arena, cintura marcada, hombros y caderas equilibrados, busto prominente pero proporcionado, piernas atléticas y anatomía natural. Mantener estos rasgos sin exageración ni deriva entre escenas.

## Prompts base

### Para NanoBanana / ComfyDeploy (kenza-nanababana-fullbody)
```
white skin, black bob hair, green eyes, [outfit], [location], full body, golden hour, iPhone UGC style
```
> CRÍTICO: usar `white skin` en este contexto (no light olive)

### Para FLUX1 general (kenza-prompt-master)
```
kenza, light olive skin, black bob hair, green eyes, [outfit], [location]
```
> Trigger word: `kenza` | LoRA strength: 0.85 | Seed ganador: 52

### Para LTX 2.3 TODOENUNO (ComfyUI)
```
Kenza, Venezuelan-Ukrainian woman, black bob hair, green eyes, white skin,
Miami waterfront, talking to camera, golden hour, iPhone UGC style, natural movement,
lifestyle content creator, authentic, casual
```

## LoRAs

| LoRA | Uso | Strength |
|---|---|---|
| `kenza_lora_v3.safetensors` | FLUX1 imagen fija | 0.85 |
| `comfy_lora_weights_step_00500.safetensors` | LTX-Video 2.3 movimiento | 0.80 |

**Ubicación local:** `C:\Users\SOPORTE2\Downloads\kenza_lora\kenza_lora\checkpoints\`

## Voz

- **TTS base:** Gemini Flash TTS, voz Leda
- **Voice change:** ElevenLabs STS `eleven_multilingual_sts_v2`
- **ID LoRA voz (TODOENUNO):** ltx-2.3-id-lora-celebvhq-3k.safetensors — 5s sample

## Baterías de outfits pendientes

| Batería | Outfit | Locación |
|---|---|---|
| A (ganadora) | Crochet top blanco + denim | Miami waterfront |
| B | Linen blanco + shorts beige | South Beach boardwalk |
| C | Leather jacket roja + denim | Wynwood street |
| D | Gold sequin mini dress | Rooftop Miami noche |
| E | Black bikini top + linen pants | Hotel pool |
| F | Sports set negro | Brickell sunrise |

## Modelo de negocio

- Precio lanzamiento: $497/mes por cliente (60 videos)
- Comparativo: Aitana López (The Clueless, España) — referencia del sector

## Archivos de referencia (guardar en Google Drive / local)

> Los archivos grandes NO se suben a GitHub (ver .gitignore)
> Guardar en: Google Drive → ARAQUE SOLUTIONS → characters → kenza → assets

- `BANANA_PRO_00006_.png` — foto base ganadora
- `turnaround_00001_.png` — character sheet 3 ángulos
- `kenza_lora_v3.safetensors` — LoRA FLUX1
- `comfy_lora_weights_step_00500.safetensors` — LoRA LTX-Video
