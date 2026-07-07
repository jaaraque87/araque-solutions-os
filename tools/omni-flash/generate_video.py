#!/usr/bin/env python3
"""
OMNI FLASH — ejecutor de edición generativa de video (Gemini Omni Flash, API directa de Google).
Capa de ejecución Windows para la skill .claude/skills/omni-edit (sin créditos de terceros).

Uso (single):
  py tools\\omni-flash\\generate_video.py --video in.mp4 --prompt "..." --output out.mp4 --aspect-ratio 9:16

Uso (batch, como lo espera la skill):
  py tools\\omni-flash\\generate_video.py --batch jobs.json --concurrency 3

jobs.json = [ { "video": "...", "output": "...", "aspect_ratio": "9:16", "prompt": "...",
                "image": ["styles/<slug>/refs/ref_1.jpg", ...]   # opcional (references-to-video)
              }, ... ]

Cada render guarda <output>.meta.json con interaction_id (SIEMPRE — regla de la skill).
Turn-by-turn: --previous-interaction-id <id> para iterar sobre una generación aprobada.

API key: variable de entorno GOOGLE_API_KEY (o GEMINI_API_KEY), o archivo .env junto a este
script con GOOGLE_API_KEY=... — NUNCA se hardcodea aquí.
"""
import argparse, json, mimetypes, os, sys, time, threading, queue
import urllib.request, urllib.error

# ----------------------------------------------------------------------------- CONFIG
# Si Google cambia nombres de campos/modelo, este bloque es lo único a tocar.
API_BASE   = os.environ.get("OMNI_API_BASE", "https://generativelanguage.googleapis.com")
MODEL      = os.environ.get("OMNI_MODEL", "gemini-omni-flash-preview")  # verificado disponible 2026-07-05
POLL_SECS  = 10
TIMEOUT_S  = 1800  # 30 min por render
# -----------------------------------------------------------------------------

def load_api_key():
    for k in ("GOOGLE_API_KEY", "GEMINI_API_KEY"):
        if os.environ.get(k):
            return os.environ[k]
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [os.path.join(here, ".env"),
                  os.path.join(here, "..", "..", ".env")]  # .env raíz del repo (convención araque-solutions-os)
    for envfile in candidates:
        if os.path.exists(envfile):
            for line in open(envfile, encoding="utf-8"):
                line = line.strip()
                if line.startswith(("GOOGLE_API_KEY=", "GEMINI_API_KEY=")):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    sys.exit("[omni-flash] Falta la API key: completa GEMINI_API_KEY= en el .env raíz del repo "
             "(araque-solutions-os/.env) o define GOOGLE_API_KEY/GEMINI_API_KEY en el entorno.")

KEY = None  # se carga en main()

def _req(url, data=None, headers=None, method=None, raw=False, timeout=120):
    h = {"x-goog-api-key": KEY}
    if headers: h.update(headers)
    body = data if (data is None or isinstance(data, bytes)) else json.dumps(data).encode()
    if body is not None and "Content-Type" not in h:
        h["Content-Type"] = "application/json"
    rq = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(rq, timeout=timeout) as r:
            payload = r.read()
            return payload if raw else (json.loads(payload) if payload else {})
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:800]
        raise RuntimeError(f"HTTP {e.code} en {url.split('?')[0]}: {detail}") from None

def upload_file(path):
    """Files API (subida resumable). Devuelve el file uri para usar en la generación."""
    size = os.path.getsize(path)
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    start = _req(f"{API_BASE}/upload/v1beta/files", data={"file": {"display_name": os.path.basename(path)}},
                 headers={"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start",
                          "X-Goog-Upload-Header-Content-Length": str(size),
                          "X-Goog-Upload-Header-Content-Type": mime}, raw=True)
    # el upload url viene en el header; con urllib hay que repetir con manejo manual:
    rq = urllib.request.Request(f"{API_BASE}/upload/v1beta/files",
        data=json.dumps({"file": {"display_name": os.path.basename(path)}}).encode(),
        headers={"x-goog-api-key": KEY, "Content-Type": "application/json",
                 "X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start",
                 "X-Goog-Upload-Header-Content-Length": str(size),
                 "X-Goog-Upload-Header-Content-Type": mime})
    with urllib.request.urlopen(rq, timeout=60) as r:
        upload_url = r.headers.get("X-Goog-Upload-URL")
    if not upload_url:
        raise RuntimeError("Files API no devolvió X-Goog-Upload-URL")
    with open(path, "rb") as f:
        blob = f.read()
    fin = _req(upload_url, data=blob, headers={"Content-Type": mime, "Content-Length": str(size),
               "X-Goog-Upload-Command": "upload, finalize", "X-Goog-Upload-Offset": "0"}, timeout=600)
    info = fin.get("file", fin)
    uri, name, state = info.get("uri"), info.get("name"), info.get("state", "ACTIVE")
    t0 = time.time()
    while state == "PROCESSING" and time.time() - t0 < 300:
        time.sleep(4)
        info = _req(f"{API_BASE}/v1beta/{name}")
        state = info.get("state", "ACTIVE")
    if state == "FAILED":
        raise RuntimeError(f"Files API: procesamiento del archivo falló ({path})")
    return uri

def generate(job, prev_interaction=None, log=print):
    src, out = job["video"], job["output"]
    prompt = job["prompt"]
    uri = upload_file(src)
    parts = [{"fileData": {"fileUri": uri, "mimeType": "video/mp4"}}]
    for i, img in enumerate(job.get("image") or []):
        parts.append({"fileData": {"fileUri": upload_file(img), "mimeType": "image/jpeg"}})
    parts.append({"text": prompt})
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["VIDEO"]}}
    if prev_interaction:
        body["generationConfig"]["previousResponseId"] = prev_interaction
    log(f"  [{os.path.basename(out)}] generando (generateContent, sincrono)...")
    t0 = time.time()
    resp = _req(f"{API_BASE}/v1beta/models/{MODEL}:generateContent", data=body, timeout=TIMEOUT_S)
    cand = (resp.get("candidates") or [{}])[0]
    fr = cand.get("finishReason", "")
    if fr in ("SAFETY", "PROHIBITED_CONTENT", "BLOCKLIST"):
        raise RuntimeError(f"[FILTRO/BLOQUEO] finishReason={fr}: {json.dumps(cand.get('safetyRatings',''))[:300]}")
    vid_bytes, remote = None, None
    for part in (cand.get("content", {}).get("parts") or []):
        if "inlineData" in part and str(part["inlineData"].get("mimeType","")).startswith("video"):
            import base64; vid_bytes = base64.b64decode(part["inlineData"]["data"]); break
        if "fileData" in part and str(part["fileData"].get("mimeType","")).startswith("video"):
            remote = part["fileData"]["fileUri"]; break
    if remote and not vid_bytes:
        sep = "&" if "?" in remote else "?"
        vid_bytes = _req(remote if "alt=media" in remote else f"{remote}{sep}alt=media", raw=True, timeout=600)
    if not vid_bytes:
        raise RuntimeError(f"[FILTRO/BLOQUEO?] respuesta sin video (finishReason={fr}): {json.dumps(resp)[:400]}")
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    with open(out, "wb") as f:
        f.write(vid_bytes)
    usage = resp.get("usageMetadata", {})
    # costo real: output tokens * $17.50/1M + input tokens * $1.50/1M (pricing 2026-07-05)
    cost = round(usage.get("candidatesTokenCount", 0) * 17.50/1e6
                 + usage.get("promptTokenCount", 0) * 1.50/1e6, 4) if usage else None
    meta = {"interaction_id": resp.get("responseId") or resp.get("responseID") or "",
            "model": MODEL, "source_video": src, "prompt": prompt,
            "previous_interaction_id": prev_interaction, "finish_reason": fr,
            "usage": usage, "cost_usd_est": cost,
            "elapsed_s": round(time.time()-t0, 1), "created": time.strftime("%Y-%m-%dT%H:%M:%S")}
    with open(out + ".meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    log(f"  [{os.path.basename(out)}] OK ({len(vid_bytes)/1e6:.1f} MB, {meta['elapsed_s']}s) - interaction_id: {meta['interaction_id'][:18]}")
    return meta

def run_batch(jobs_path, concurrency, log=print):
    jobs = json.load(open(jobs_path, encoding="utf-8"))
    q, results, errors = queue.Queue(), [], []
    for j in jobs: q.put(j)
    lock = threading.Lock()
    def worker():
        while True:
            try: j = q.get_nowait()
            except queue.Empty: return
            try:
                m = generate(j, j.get("previous_interaction_id"), log)
                with lock: results.append((j["output"], m["interaction_id"]))
            except Exception as e:
                with lock: errors.append((j["output"], str(e)))
                log(f"  [{os.path.basename(j['output'])}] FALLÓ: {e}")
            finally: q.task_done()
    threads = [threading.Thread(target=worker, daemon=True) for _ in range(max(1, concurrency))]
    [t.start() for t in threads]; [t.join() for t in threads]
    log(f"\nBatch: {len(results)} OK, {len(errors)} fallidos.")
    log("[!] Regla de la skill: los interaction_id se loguean por FINALIZACIÓN — para turn-by-turn")
    log("    verificar SIEMPRE el contenido del parent en <output>.meta.json, nunca mapear por posición.")
    if errors:
        log("Fallidos (protocolo anti-filtro de la skill: retry → sonda otro video → sonda control → bisect):")
        for o, e in errors: log(f"  - {o}: {e[:200]}")
        sys.exit(1)

def main():
    global KEY
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch"); ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--video"); ap.add_argument("--prompt"); ap.add_argument("--output")
    ap.add_argument("--aspect-ratio", default="9:16")
    ap.add_argument("--image", action="append", default=None)
    ap.add_argument("--previous-interaction-id")
    a = ap.parse_args()
    KEY = load_api_key()
    if a.batch:
        run_batch(a.batch, a.concurrency)
    else:
        if not (a.video and a.prompt and a.output):
            ap.error("single mode requiere --video --prompt --output")
        generate({"video": a.video, "prompt": a.prompt, "output": a.output,
                  "aspect_ratio": a.aspect_ratio, "image": a.image}, a.previous_interaction_id)

if __name__ == "__main__":
    main()
