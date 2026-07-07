---
name: cherry-blackcloud-guide
title: "Cherry Blackcloud Guide"
author: cherry_blackcloud
category: Content Creation
users: 6
source: https://higgsfield.ai/supercomputer/marketplace/skills/6d3a5d4e-d6a6-49f3-99fe-4d2ce5344629
extracted: modal SKILL.md (via claude-in-chrome) — single file
nota: canon/IP personal del autor (universo cyber-noir "Cherry Blackcloud", 9 personajes con UUIDs de Seedance @element privados). El worldbuilding NO es reusable; las PROMPT WRITING RULES abajo SÍ son generales y útiles para prompts Seedance 2.0 de 15s con diálogo.
---

# Cherry Blackcloud — Prompt Writing Guide (Seedance 2.0, 15s)
Universo cyber-noir de Neo-Tokyo (canon personal del autor: 9 personajes, historia de replicantes/Yōkai, con @element UUIDs privados). Estilo: nunca CGI, siempre visceral/real, como practical effects en 35mm anamórfico. Inspiraciones: Matrix, Blade Runner, Ghost in the Shell, Tarantino.

## PROMPT WRITING RULES (parte reusable)

### Structure (timestamps)
```
[00:00-00:03] Scene description. Character action.
[00:03-00:06] Camera move. Dialogue.
...
[00:12-00:15] Final beat.
```

### Characters
- Usar SIEMPRE @element codes; nunca describir lo que el element ya define (ropa, pelo, cara).
- Solo describir acción, posición, expresión y qué están haciendo.

### Dialogue
- Anteponer nota de acento/voz a cada línea: `(she speaks English with a very heavy Macedonian accent): "dialogue"` / `(sultry Marilyn Monroe breathy voice): "..."` / `(low hollow whisper, emotionless): "..."` etc.
- El diálogo debe caber en el timestamp (mín 2-3s por línea). Máx 4-5 intercambios en 15s.

### Camera
- Siempre acción, nunca quietud (personajes siempre moviéndose/reaccionando).
- Preferir shots continuos fluidos (minimizar hard cuts).
- Solo escribir lo que se ve o se oye (sin notas internas del personaje).
- **Usar descriptores positivos específicos, nunca frases negativas:** "musicless" (no "no music"), "earringless" (no "no earrings").
- Especificar props en CADA shot (el modelo resetea prop assignments entre shots).

### Technical
- Terminar CADA prompt con: `Cinematic. 35mm film grain. No CGI. Musicless. Earringless characters.`
- Shots continuos: agregar `One continuous uncut flowing shot throughout.`
- UGC/casual: agregar `Casual handheld phone footage. Slightly shaky. Auto-exposure flickering.`
- Default: Seedance 2.0, 1:1, 1080p. Máx 8 character elements por generación (1 slot reservado para start frame).

### Content Filter
- Nunca describir heridas, sangre ni cuerpos perforados; implicar la violencia, nunca mostrarla explícita.
- Ropa: "slightly open, tasteful hint of neckline" — nunca describir piel desnuda.
- Si una generación falla el content filter: remover el último element y reintentar de a uno.

### Sound Design
- Describir sonidos reales específicos, nunca genéricos (ambient: refrigerator hum, street traffic, laptop fan, rain, neon buzz; practical: footsteps en superficies específicas, fabric, weapon sounds).
- El elemento imposible/sobrenatural debe sonar mundano (como un electrodoméstico roto). Nunca SFX cinematográficos dramáticos.

### Tonal range
Drama: lento, deliberado, emocional, dejar respirar el diálogo · Action: rápido, kinético, nunca quieto · Comedy · Existential.

## Nota sobre el canon (privado)
9 personajes (Dr. Shinigami, Queen of Spades, Cherry, Kali, Ms. Yurei, Mr. Tengu/Noppera-bō/Kappa/Oni) con UUIDs @element específicos del autor, referencias visuales a actores, y una secuencia narrativa ("Reset Trilogy", etc.) — todo IP personal, no reusable.
