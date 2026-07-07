#!/usr/bin/env python3
"""
YT-ANALYZE — convierte videos de YouTube en documentación markdown estructurada vía Gemini
(video understanding, tier GRATUITO). Un .md por video, listo para que un agente lo procese.

Uso:
  py tools\\yt-analyze\\analyze_channel.py --list videos.txt --outdir docs/taoofai
  (videos.txt: lineas "VIDEO_ID|DURACION|TITULO", como salen de:
   yt-dlp --flat-playlist --print "%(id)s|%(duration)s|%(title)s" <URL_CANAL>/videos)

Opciones: --model gemini-3.5-flash · --skip ID1,ID2 · --only ID1,ID2
Reintenta 429 respetando el retry-after. Salta videos ya procesados (archivo existente).
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error

API = "https://generativelanguage.googleapis.com"

PROMPT = """Analiza este video de YouTube COMPLETO y produce un documento markdown estructurado
para que otro agente de IA (que no puede ver video) pueda replicar todo sin verlo.
Canal: Tao of AI (herramientas Camera Lab, ComfyUI, LTX, WAN, SCAIL).

Estructura EXACTA del documento:

# [Titulo del video] - [duracion] - [URL]

## TL;DR (3 lineas)

## Timeline con timestamps
Lista de secciones del video con minuto:segundo y que se muestra en cada una.

## Configuraciones EXACTAS mostradas en pantalla
CRITICO - transcribe literalmente cada valor visible: nombres de nodos, parametros,
numeros, rutas de archivos, nombres de modelos, opciones de dropdowns, checkboxes.
Formato: [timestamp] pantalla/nodo -> parametro = valor

## Flujo de trabajo paso a paso
Numerado, cada paso con su timestamp, tal como el autor lo ejecuta.

## Modelos, archivos y links mencionados
Todo lo que el autor dice descargar o instalar, con la URL/fuente exacta si la menciona
y la carpeta destino donde lo coloca.

## Requisitos de hardware/software mencionados

## Advertencias, errores y trucos del autor
Cada "ojo con esto", "no hagan X", "esto falla si Y" - cita textual + timestamp.

## Que NO explica el video (huecos)

Reglas: NO resumas las configuraciones, transcribelas literales. Si un valor no se
lee bien en pantalla, escribe [ILEGIBLE @ timestamp]. Si el autor habla en ingles,
manten los terminos tecnicos en ingles y el resto en espanol."""

def load_key():
    for k in ("GOOGLE_API_KEY", "GEMINI_API_KEY"):
        if os.environ.get(k): return os.environ[k]
    here = os.path.dirname(os.path.abspath(__file__))
    for envfile in (os.path.join(here, "..", "..", ".env"),):
        if os.path.exists(envfile):
            for line in open(envfile, encoding="utf-8-sig"):
                if line.strip().startswith(("GOOGLE_API_KEY=", "GEMINI_API_KEY=")):
                    v = line.split("=",1)[1].strip().strip('"').strip("'")
                    if v: return v
    sys.exit("[yt-analyze] falta GEMINI_API_KEY (.env raiz del repo)")

def slug(t, n=48):
    s = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return s[:n].rstrip("-") or "video"

def analyze(key, model, vid, title):
    url = f"https://www.youtube.com/watch?v={vid}"
    body = {"contents": [{"role": "user", "parts": [
        {"fileData": {"fileUri": url}},
        {"text": PROMPT}]}]}
    rq = urllib.request.Request(f"{API}/v1beta/models/{model}:generateContent",
        data=json.dumps(body).encode(),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(rq, timeout=600) as r:
        resp = json.loads(r.read())
    parts = (resp.get("candidates") or [{}])[0].get("content", {}).get("parts", [])
    text = "\n".join(p.get("text", "") for p in parts if "text" in p).strip()
    usage = resp.get("usageMetadata", {})
    return text, usage

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--model", default="gemini-3.5-flash")
    ap.add_argument("--skip", default="")
    ap.add_argument("--only", default="")
    ap.add_argument("--pause", type=int, default=25, help="segundos entre videos (respetar TPM free tier)")
    a = ap.parse_args()
    key = load_key()
    skip = set(x for x in a.skip.split(",") if x)
    only = set(x for x in a.only.split(",") if x)
    os.makedirs(a.outdir, exist_ok=True)
    rows = []
    for line in open(a.list, encoding="utf-8-sig", errors="replace"):
        line = line.strip()
        if not line: continue
        p = line.split("|", 2)
        rows.append((p[0], p[1] if len(p) > 1 else "?", p[2] if len(p) > 2 else p[0]))
    ok = fail = skipped = 0
    for i, (vid, dur, title) in enumerate(rows, 1):
        if vid in skip or (only and vid not in only):
            skipped += 1; continue
        out = os.path.join(a.outdir, f"{i:02d}-{vid}-{slug(title)}.md")
        if os.path.exists(out):
            print(f"[{i:02d}] ya existe, salto: {os.path.basename(out)}"); skipped += 1; continue
        print(f"[{i:02d}/{len(rows)}] {title[:60]} ({dur}s)...", flush=True)
        for attempt in range(4):
            try:
                text, usage = analyze(key, a.model, vid, title)
                if not text: raise RuntimeError("respuesta vacia")
                header = (f"<!-- generado por yt-analyze {time.strftime('%Y-%m-%d %H:%M')} | modelo {a.model} | "
                          f"tokens in/out: {usage.get('promptTokenCount','?')}/{usage.get('candidatesTokenCount','?')} -->\n\n")
                open(out, "w", encoding="utf-8").write(header + text + "\n")
                print(f"       OK -> {os.path.basename(out)} ({len(text)} chars)")
                ok += 1
                break
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors="replace")
                if e.code == 429 and attempt < 3:
                    m = re.search(r"retry in ([0-9.]+)s", detail, re.I)
                    wait = float(m.group(1)) + 5 if m else 60
                    print(f"       429 rate limit, espero {wait:.0f}s...", flush=True)
                    time.sleep(wait)
                else:
                    print(f"       FALLO HTTP {e.code}: {detail[:200]}"); fail += 1; break
            except Exception as e:
                print(f"       FALLO: {e}"); fail += 1; break
        time.sleep(a.pause)
    print(f"\nResumen: {ok} OK, {fail} fallidos, {skipped} saltados. Salida: {a.outdir}")

if __name__ == "__main__":
    main()
