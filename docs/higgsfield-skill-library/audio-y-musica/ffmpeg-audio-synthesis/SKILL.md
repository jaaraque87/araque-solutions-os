---
name: ffmpeg-audio-synthesis
title: "FFmpeg Audio Synthesis"
author: cherry_blackcloud
category: Content Creation
users: 10
source: https://higgsfield.ai/supercomputer/marketplace/skills/323d4c00-3e5e-4683-92fe-3c24fd7874d0
extracted: modal SKILL.md (via claude-in-chrome) — single file (nota: el original trae el código Python completo de cada instrumento; acá se resume la técnica y se listan)
---

# FFmpeg Audio Synthesis & Scoring
Sintetizar, mezclar y scorear audio computacionalmente con `ffmpeg`, `numpy`, `pedalboard` — sin descargas externas.

## Fast Synthesis (FFmpeg lavfi)
Waveforms y ruido on-the-fly sin Python. Ej textura de viento atmosférica:
`ffmpeg -f lavfi -i "anoisesrc=color=pink:duration=35:amplitude=0.3" -af "highpass=f=80, lowpass=f=800, equalizer=f=200:width_type=o:width=2:g=-6, equalizer=f=500:..." output.mp3`
Lógica: pink noise base + low cut (rumble) + high cut (harshness) + mid-boost ("hollow" tunnel).

## High-Quality Waveform (NumPy + Pedalboard)
Para sonidos punchy/musicales/transientes (kicks, drones, plucks), construir la waveform directo en numpy y masterizar con pedalboard (Compressor, Reverb, LowShelfFilter, PeakFilter).
- **Kick drum:** frequency sweep 150→45Hz (thud) + sub baseline + transient click (randn·exp), normalizar a 0.9, pedalboard con LowShelfFilter + Compressor.
- **Karplus-Strong pluck (koto/guitar):** buffer de ruido de longitud `sr/freq`, loop `out[i]=buf[i%buf_len]`, `buf[i%buf_len]=decay*0.5*(buf[i%buf_len]+buf[(i+1)%buf_len])`.

## Mixing Dynamics
- **amix con `normalize=0`** (evita compresión agresiva de inputs): `ffmpeg -i video.mp4 -i layer.wav -filter_complex "[0:a]volume=1.0[va];[1:a]volume=0.55[vb];[va][vb]amix=inputs=2:duration=first:normalize=0[aout]" -map 0:v -map "[aout]"`.
- **Ducking bajo voiceover** (adelay para precisión ms): `[0:a]volume=1.0:enable='lt(t,15.667)',volume=0.5:enable='gte(t,15.667)'[bg]; [1:a]adelay=15667|15667...`.

## Librería de instrumentos (funciones NumPy — combinar para scorear videos sin descargas)
Shakuhachi breath (fundamental breathy + flutter vibrato) · Erhu string (bowed two-string, detune 1.003) · Biwa pluck (Karplus-Strong + buzz) · Gong strike (parciales inarmónicos 1.41/2.24/3.0, cola larga) · Bowed glass (sine pura, slow attack, etéreo) · Reversed piano (Karplus-Strong `[::-1]` = swell) · Singing bowl (drone armónico) · Guqin harmonic (zither chino) · Waterphone scrape (bowed metal eerie, horror) · Zheng (zither brillante) · Hang drum (metálico cálido) · Crystal singing bowl (overtone alto puro) · Dulcimer tremolo · Wooden slit drum (hollow knock) · Kalimba tine (metálico brillante).
*(Técnica común: parciales sine con envelopes exp + Karplus-Strong para plucks. El código completo de cada función está en el SKILL.md original.)*

## Python Packages
`numpy`, `scipy` (waveform/filtering) · `soundfile` (I/O limpio sin deps pesadas) · `pedalboard` (master bus, efectos studio) · `librosa` (BPM tracking, beat extraction, análisis estructural). **Evitar `fluidsynth`/`pyfluidsynth`** (el binario requiere operaciones sin privilegios que fallan/timeoutean).
