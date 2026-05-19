#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  secrets.example.sh — Template de tokens/credenciales                     ║
# ║                                                                             ║
# ║  USO:                                                                       ║
# ║    cp secrets.example.sh secrets.sh                                        ║
# ║    nano secrets.sh   ← pon tus tokens reales                               ║
# ║                                                                             ║
# ║  IMPORTANTE: secrets.sh está en .gitignore — NUNCA se sube a GitHub       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# HuggingFace — https://huggingface.co/settings/tokens
# Crear token con permisos "Read"
export HF_TOKEN="hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# CivitAI — https://civitai.com/user/account (sección API Keys)
export CIVITAI_TOKEN="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# ── APIs del pipeline UGC (para los scripts Python) ───────────────────────────

# Google Gemini — https://aistudio.google.com/apikey
export GEMINI_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# ElevenLabs — https://elevenlabs.io/app/settings/api-keys
export ELEVENLABS_API_KEY="sk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# fal.ai (Kling, Sync-3, GPT Image 2) — https://fal.ai/dashboard/keys
export FAL_KEY="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX:XXXXXXXX"

# Suno / Kie.ai — https://kie.ai/dashboard
export KIE_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# OpenAI (GPT Image 2) — https://platform.openai.com/api-keys
export OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Supabase — https://app.supabase.com/project/_/settings/api
export SUPABASE_URL="https://XXXXXXXXXXXXXXXX.supabase.co"
export SUPABASE_KEY="eyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
