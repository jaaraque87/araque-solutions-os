#!/usr/bin/env python3
"""
FASE B — Orquestador headless del V9 Video Builder (v1: montaje perfecto de proyecto).
Corrige/monta un proyecto del Builder por API (túnel de sesión ComfyDeploy) con pairing
garantizado por código. El humano solo hace: Load Project -> Render All -> Build Full Video.

Uso:
  py tools\\builder-orchestrator\\montar_proyecto.py --tunnel https://ta-....modal.host \
     --kit "C:\\Users\\SOPORTE2\\Downloads\\CAMILA-PROD001-KIT" [--project <carpeta_existente>] [--dump]

--dump: solo lista proyectos y vuelca la sesión actual a session_dump.json (descubrimiento).
Sin --project: crea proyecto nuevo con new_project.
"""
import argparse, base64, json, os, re, sys, urllib.request

def post(tunnel, route, payload, timeout=180, ok404=False):
    rq = urllib.request.Request(tunnel + route, data=json.dumps(payload).encode(),
                                headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(rq, timeout=timeout) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:300]
        if ok404: return {"__error__": body}
        raise SystemExit(f"[X] {route} HTTP {e.code}: {body}")

def get(tunnel, route, timeout=60):
    with urllib.request.urlopen(tunnel + route, timeout=timeout) as r:
        return json.loads(r.read() or b"{}")

def data_url(path):
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "mp3": "audio/mpeg", "wav": "audio/wav"}.get(ext, "application/octet-stream")
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()

def kit_scenes(kit):
    """Escenas del kit: escN_*.png + audio-por-escena/escN_*.mp3 + i2v_prompts.txt (I2VN=...)."""
    imgs = sorted(f for f in os.listdir(kit) if re.match(r"esc\d+_.*\.png$", f))
    auds = sorted(f for f in os.listdir(os.path.join(kit, "audio-por-escena"))
                  if re.match(r"esc\d+_.*\.mp3$", f))
    prompts = {}
    for line in open(os.path.join(kit, "i2v_prompts.txt"), encoding="utf-8"):
        m = re.match(r"I2V(\d+)=(.+)", line.strip())
        if m: prompts[int(m.group(1))] = m.group(2)
    scenes = []
    for i, (im, au) in enumerate(zip(imgs, auds), 1):
        n_im = int(re.match(r"esc(\d+)", im).group(1))
        n_au = int(re.match(r"esc(\d+)", au).group(1))
        assert n_im == n_au == i, f"PAIRING ROTO: {im} vs {au} (esperaba esc{i})"
        dur = float(re.search(r"_(\d+\.\d+)s", au).group(1))
        scenes.append({"n": i, "img": os.path.join(kit, im),
                       "aud": os.path.join(kit, "audio-por-escena", au),
                       "dur": dur, "prompt": prompts.get(i, "")})
    return scenes

FACTORY = {"track":"base","label":"New scene","notes":"","timeline_note":"","lyric_text":"","lyric_section":"","story_beat":"","lyric_singers":[],"facial_performance":"","facial_performance_custom":"","no_character_present":False,"i2v_notes":"","t2i_prompt":"","enhance_notes":"","enhance_prompt":"","i2v_prompt":"","ref_image_path":"","use_vision_reference":False,"use_i2v_vision_reference":True,"custom_image_path":"","custom_image_data":"","custom_image_name":"","image":None,"image_history":[],"image_history_index":-1,"preview_mode":"image","video_path":"","video_thumbnail_path":"","video_history":[],"video_thumbnail_history":[],"video_backup_paths":[],"video_backup_thumbnail_paths":[],"video_history_index":-1,"video_output":None,"video_status":"none","custom_audio_path":"","custom_audio_name":"","custom_audio_duration":0,"custom_audio_full_duration":0,"custom_audio_timeline_start":0,"custom_audio_source_start":0,"custom_audio_peaks":[],"custom_audio_beats":[],"overlay_slot_number":0,"flux_image_ingredients":[],"flux_notes":"","flux_prompt":"","nb_notes":"","nb_prompt":"","use_scene_zimage_settings":False,"zimage_settings":None,"use_scene_ernie_image_settings":False,"ernie_image_settings":None,"use_scene_krea2_2pass_settings":False,"krea2_2pass_settings":None,"use_scene_flux_klein_settings":False,"flux_klein_settings":None,"use_scene_i2v_video_settings":False,"i2v_video_settings":None,"source":"manual","approved_image_path":""}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tunnel", required=True)
    ap.add_argument("--kit", required=True)
    ap.add_argument("--project", default="")
    ap.add_argument("--dump", action="store_true")
    a = ap.parse_args()
    T = a.tunnel.rstrip("/")

    projs = get(T, "/vrgdg/music_builder/list_projects")
    print("[1] proyectos en la nube:", json.dumps(projs)[:400])
    if a.dump:
        target = a.project or (projs.get("projects") or [{}])[-1]
        sess = post(T, "/vrgdg/music_builder/load_session",
                    {"project_folder": target if isinstance(target, str) else target.get("path", "")})
        open("session_dump.json", "w", encoding="utf-8").write(json.dumps(sess, indent=1, ensure_ascii=False))
        print("[dump] session_dump.json escrito — inspeccionar esquema de segments"); return

    scenes = kit_scenes(a.kit)
    total = round(sum(s["dur"] for s in scenes), 2)
    print(f"[2] kit OK: {len(scenes)} escenas, {total}s, pairing verificado por código")

    if a.project:
        pf = a.project
    else:
        np_ = post(T, "/vrgdg/music_builder/new_project",
                   {"project_folder": "CAMILA_PROD001_AUTO"})
        pf = np_.get("project_folder", "")
        print("[3] proyecto:", pf)
    if not pf: sys.exit("sin project_folder")

    # cargar sesion existente como plantilla de esquema
    sess = post(T, "/vrgdg/music_builder/load_session", {"project_folder": pf}, ok404=True)
    session = (sess or {}).get("session") or {}
    print("[4] plantilla de sesión cargada; claves:", list(session.keys())[:20])

    # subir assets por escena — pairing por código
    for s in scenes:
        ri = post(T, "/vrgdg/music_builder/save_scene_image",
                  {"source_path": "", "image_data": data_url(s["img"]),
                   "project_folder": pf, "scene_number": s["n"]})
        ra = post(T, "/vrgdg/music_builder/save_scene_audio",
                  {"project_folder": pf, "scene_number": s["n"],
                   "audio_data": data_url(s["aud"]),
                   "audio_name": os.path.basename(s["aud"])}, timeout=300)
        s["img_saved"] = ri.get("saved_path", ""); s["aud_saved"] = ra.get("saved_path", "")
        s["aud_dur_real"] = ra.get("duration", s["dur"])
        print(f"[5] esc{s['n']}: img={bool(s['img_saved'])} aud={bool(s['aud_saved'])} dur={s['aud_dur_real']}")

    # construir segments sobre el esquema real (usa el primero existente como molde si hay)
    molde = (session.get("segments") or [FACTORY])[0] if (session.get("segments")) else FACTORY
    segs, t0 = [], 0.0
    for s in scenes:
        seg = dict(molde)  # hereda todos los campos del esquema real
        seg.update({"id": f"auto-esc{s['n']}", "start": round(t0, 2),
                    "duration": s["dur"], "end": round(t0 + s["dur"], 2),
                    "i2v_prompt": s["prompt"], "prompt": s["prompt"],
                    "approved_image_path": s["img_saved"],
                    "custom_audio_path": s["aud_saved"],
                    "custom_audio_name": os.path.basename(s["aud"]),
                    "custom_audio_duration": s["aud_dur_real"],
                    "custom_audio_full_duration": s["aud_dur_real"],
                    "custom_audio_timeline_start": round(t0, 2),
                    "custom_audio_source_start": 0})
        segs.append(seg); t0 += s["dur"]
    session["segments"] = segs
    # settings críticos (las llaves exactas se validan contra el dump; ajustar si difieren)
    for k, v in (("video_type", "speaking"), ("videoType", "speaking"),
                 ("width", 1080), ("height", 1920), ("fps", 24)):
        if k in session: session[k] = v
    r = post(T, "/vrgdg/music_builder/save_session",
             {"audio_path": "", "project_folder": pf, "session": session}, timeout=120)
    print("[6] save_session:", json.dumps(r)[:300])
    print(f"\nLISTO. En el Builder: Load Project '{pf}' -> verificar 5 escenas pareadas -> Render All -> Build Full Video.")

if __name__ == "__main__":
    main()
