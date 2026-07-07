---
name: telegram-export-analysis
title: "Telegram Export Analysis"
author: miha4real
category: Creative-marketing
users: 2
source: https://higgsfield.ai/supercomputer/marketplace/skills/b5292fa6-f83f-46bc-b707-cee3b3e89ce6
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# Telegram Chat Export Analysis
Parsear/analizar/extraer insights de exports grandes de chat de Telegram (`result.json`). Los parsers estándar (`parse_file`, `web_extract`) fallan por el tamaño → SIEMPRE usar `execute_code` (Python).

## 1. Download and Load
No cargar el JSON entero al contexto. Descargar a `/tmp/` y parsear en memoria:
```python
import urllib.request, json
req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
```

## 2. Quirk del campo `text`
En exports de Telegram, `text` NO siempre es string — si el mensaje tiene formato (menciones/links), es un ARRAY de strings y objetos `{type, text}`. Lógica de extracción:
```python
messages = data.get('messages', [])
text_msgs = [m for m in messages if m.get('type')=='message']  # ignorar service messages
for m in text_msgs:
    raw_text = m.get('text','')
    if isinstance(raw_text, list):
        text = ''.join([t if isinstance(t,str) else t.get('text','') for t in raw_text])
    else:
        text = raw_text
    if isinstance(text,str) and text.strip():
        processed_msgs.append({'sender':m.get('from','Unknown'),'date':m.get('date',''),'text':text})
```

## 3. Analysis Patterns
Logs masivos (50k+ mensajes) — no imprimir todo al stdout.
- **Sampling:** imprimir los últimos 300 mensajes (contexto reciente, inside jokes actuales).
- **Metrics:** contar mensajes por sender (balance del chat).
- **Personality/Pattern Slicing:** muestrear chunks de distintas épocas (`text_msgs[len//2 : len//2+100]`) en vez de solo el inicio.
