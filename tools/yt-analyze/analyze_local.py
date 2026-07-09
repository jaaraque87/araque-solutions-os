#!/usr/bin/env python3
"""
ANALYZE_LOCAL — sube videos LOCALES (mp4) a Gemini Files API y produce documentacion
markdown estructurada (mismo formato que analyze_channel.py). Para grabaciones de
Discord/pantalla del creador vrgamedevgirl u otros demos.

Uso:
  py tools\\yt-analyze\\analyze_local.py --files "video1.mp4" "video2.mp4" --outdir docs/vrgdg --context "demos del Builder V9"
"""
import argparse, json, mimetypes, os, re, sys, time, urllib.request, urllib.error

API = "https://generativelanguage.googleapis.com"

PROMPT_BASE = """Analiza este video COMPLETO (es una grabacion de pantalla/demo) y produce un documento
markdown estructurado para que otro agente de IA (que no puede ver video) pueda replicar todo sin verlo.
Contexto: {context}

Estructura EXACTA del documento:

# [Titulo descriptivo del contenido] - [duracion]

## TL;DR (3 lineas)

## Timeline con timestamps
Lista de secciones con minuto:segundo y que se muestra en cada una.

## Configuraciones EXACTAS mostradas en pantalla
CRITICO - transcribe literalmente cada valor visible: nombres de nodos, parametros,
numeros, rutas, nombres de modelos, opciones de dropdowns, checkboxes.
Formato: [timestamp] pantalla/nodo -> parametro = valor

## Flujo de trabajo paso a paso
Numerado, cada paso con su timestamp, tal como el autor lo ejecuta.

## Modelos, archivos y links mencionados

## Advertencias, errores y trucos del autor
Cada "ojo con esto", "no hagan X", "esto falla si Y" - cita textual + timestamp.

## Que NO explica el video (huecos)

Reglas: NO resumas las configuraciones, transcribelas literales. Si un valor no se
lee bien, escribe [ILEGIBLE @ timestamp]. Terminos tecnicos en ingles, resto en espanol."""


def load_key():
    for k in ("GOOGLE_API_KEY", "GEMINI_API_KEY"):
        if os.environ.get(k):
            return os.environ[k]
    here = os.path.dirname(os.path.abspath(__file__))
    envfile = os.path.join(here, "..", "..", ".env")
    if os.path.exists(envfile):
        for line in open(envfile, encoding="utf-8-sig"):
            if line.strip().startswith(("GOOGLE_API_KEY=", "GEMINI_API_KEY=")):
                v = line.split("=", 1)[1].strip().strip('"').strip("'")
                if v:
                    return v
    sys.exit("[analyze_local] falta GEMINI_API_KEY (.env raiz del repo)")


def slug(t, n=48):
    s = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return s[:n].rstrip("-") or "video"


def upload_file(key, path):
    size = os.path.getsize(path)
    mime = mimetypes.guess_type(path)[0] or "video/mp4"
    meta = json.dumps({"file": {"display_name": os.path.basename(path)}}).encode()
    rq = urllib.request.Request(
        f"{API}/upload/v1beta/files",
        data=meta,
        headers={
            "x-goog-api-key": key,
            "X-Goog-Upload-Protocol": "resumable",
            "X-Goog-Upload-Command": "start",
            "X-Goog-Upload-Header-Content-Length": str(size),
            "X-Goog-Upload-Header-Content-Type": mime,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(rq, timeout=120) as r:
        upload_url = r.headers.get("X-Goog-Upload-URL")
    if not upload_url:
        raise RuntimeError("no upload URL")
    data = open(path, "rb").read()
    rq2 = urllib.request.Request(
        upload_url,
        data=data,
        headers={
            "X-Goog-Upload-Command": "upload, finalize",
            "X-Goog-Upload-Offset": "0",
            "Content-Length": str(size),
        },
        method="POST",
    )
    with urllib.request.urlopen(rq2, timeout=3600) as r:
        info = json.loads(r.read())["file"]
    # esperar ACTIVE (procesamiento del video)
    name = info["name"]
    for _ in range(120):
        if info.get("state") == "ACTIVE":
            return info["uri"], mime
        if info.get("state") == "FAILED":
            raise RuntimeError("procesamiento FAILED")
        time.sleep(10)
        rq3 = urllib.request.Request(f"{API}/v1beta/{name}", headers={"x-goog-api-key": key})
        with urllib.request.urlopen(rq3, timeout=60) as r:
            info = json.loads(r.read())
    raise RuntimeError("timeout esperando ACTIVE")


def analyze(key, model, file_uri, mime, context):
    body = {"contents": [{"role": "user", "parts": [
        {"fileData": {"fileUri": file_uri, "mimeType": mime}},
        {"text": PROMPT_BASE.format(context=context)}]}]}
    rq = urllib.request.Request(
        f"{API}/v1beta/models/{model}:generateContent",
        data=json.dumps(body).encode(),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(rq, timeout=900) as r:
        resp = json.loads(r.read())
    parts = (resp.get("candidates") or [{}])[0].get("content", {}).get("parts", [])
    return "\n".join(p.get("text", "") for p in parts if "text" in p).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="+", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--model", default="gemini-3.5-flash")
    ap.add_argument("--context", default="demo de herramienta ComfyUI")
    ap.add_argument("--pause", type=int, default=30)
    a = ap.parse_args()
    key = load_key()
    os.makedirs(a.outdir, exist_ok=True)
    ok = fail = 0
    for i, path in enumerate(a.files, 1):
        base = slug(os.path.splitext(os.path.basename(path))[0])
        out = os.path.join(a.outdir, f"local-{base}.md")
        if os.path.exists(out):
            print(f"[{i}] ya existe, salto: {out}"); continue
        print(f"[{i}/{len(a.files)}] subiendo {os.path.basename(path)} ({os.path.getsize(path)//1048576} MB)...", flush=True)
        try:
            uri, mime = upload_file(key, path)
            print(f"       ACTIVE, analizando...", flush=True)
            text = analyze(key, a.model, uri, mime, a.context)
            if not text:
                raise RuntimeError("respuesta vacia")
            header = f"<!-- analyze_local {time.strftime('%Y-%m-%d %H:%M')} | {a.model} | fuente: {os.path.basename(path)} -->\n\n"
            open(out, "w", encoding="utf-8").write(header + text + "\n")
            print(f"       OK -> {out} ({len(text)} chars)"); ok += 1
        except Exception as e:
            print(f"       FALLO: {e}"); fail += 1
        time.sleep(a.pause)
    print(f"\nResumen: {ok} OK, {fail} fallidos. Salida: {a.outdir}")


if __name__ == "__main__":
    main()
