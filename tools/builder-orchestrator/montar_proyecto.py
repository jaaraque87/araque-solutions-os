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
import argparse, base64, copy, hashlib, json, os, re, sys, urllib.request

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

def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

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
        image_path = os.path.join(kit, im)
        audio_path = os.path.join(kit, "audio-por-escena", au)
        scenes.append({"n": i, "img": image_path,
                       "aud": audio_path,
                       "image_sha256": sha256_file(image_path),
                       "audio_sha256": sha256_file(audio_path),
                       "dur": dur, "prompt": prompts.get(i, "")})
    return scenes

FACTORY = {"track":"base","label":"New scene","notes":"","timeline_note":"","lyric_text":"","lyric_section":"","story_beat":"","lyric_singers":[],"facial_performance":"","facial_performance_custom":"","no_character_present":False,"i2v_notes":"","t2i_prompt":"","enhance_notes":"","enhance_prompt":"","i2v_prompt":"","ref_image_path":"","use_vision_reference":False,"use_i2v_vision_reference":True,"custom_image_path":"","custom_image_data":"","custom_image_name":"","image":None,"image_history":[],"image_history_index":-1,"preview_mode":"image","video_path":"","video_thumbnail_path":"","video_history":[],"video_thumbnail_history":[],"video_backup_paths":[],"video_backup_thumbnail_paths":[],"video_history_index":-1,"video_output":None,"video_status":"none","custom_audio_path":"","custom_audio_name":"","custom_audio_duration":0,"custom_audio_full_duration":0,"custom_audio_timeline_start":0,"custom_audio_source_start":0,"custom_audio_peaks":[],"custom_audio_beats":[],"overlay_slot_number":0,"flux_image_ingredients":[],"flux_notes":"","flux_prompt":"","nb_notes":"","nb_prompt":"","use_scene_zimage_settings":False,"zimage_settings":None,"use_scene_ernie_image_settings":False,"ernie_image_settings":None,"use_scene_krea2_2pass_settings":False,"krea2_2pass_settings":None,"use_scene_flux_klein_settings":False,"flux_klein_settings":None,"use_scene_i2v_video_settings":False,"i2v_video_settings":None,"source":"manual","approved_image_path":""}

VOLATILE_SEGMENT_DEFAULTS = {
    "preview_mode": "image",
    "video_path": "",
    "video_thumbnail_path": "",
    "video_history": [],
    "video_thumbnail_history": [],
    "video_backup_paths": [],
    "video_backup_thumbnail_paths": [],
    "video_history_index": -1,
    "video_output": None,
    "video_status": "none",
    "render_fingerprint": "",
    "render_contract_version": 0,
}

def fresh_segment(mold, scene, start):
    """Crea una escena sin heredar resultados ni listas mutables del molde."""
    segment = copy.deepcopy(mold or FACTORY)
    for key, value in VOLATILE_SEGMENT_DEFAULTS.items():
        segment[key] = copy.deepcopy(value)
    segment.update({
        "id": f"auto-esc{scene['n']}",
        "label": f"Scene {scene['n']}",
        "overlay_slot_number": scene["n"],
        "start": round(start, 2),
        "duration": scene["dur"],
        "end": round(start + scene["dur"], 2),
        "i2v_prompt": scene["prompt"],
        "prompt": scene["prompt"],
        "approved_image_path": scene["img_saved"],
        "image_history": [scene["preview_saved"]] if scene.get("preview_saved") else [],
        "image_history_index": 0 if scene.get("preview_saved") else -1,
        "custom_image_path": "",
        "custom_image_name": "",
        "custom_audio_path": scene["aud_saved"],
        "custom_audio_name": os.path.basename(scene["aud"]),
        "custom_audio_duration": scene["aud_dur_real"],
        "custom_audio_full_duration": scene["aud_dur_real"],
        "custom_audio_timeline_start": 0,
        "custom_audio_source_start": 0,
        "automation_contract": {
            "version": 1,
            "scene_number": scene["n"],
            "source_image_sha256": scene["image_sha256"],
            "source_audio_sha256": scene["audio_sha256"],
        },
    })
    return segment

def apply_production_settings(session, seed=69):
    """Aplica los invariantes validados de producción sin borrar ajustes del Builder."""
    session["video_type"] = "speaking"
    session["videoType"] = "speaking"
    session["video_model_mode"] = "i2v"
    settings = dict(session.get("i2v_video_settings") or {})
    settings.update({
        "seed": int(seed),
        "seed_mode": "fixed",
        "seedMode": "fixed",
        "seed_behavior": "fixed",
        "width": 1080,
        "height": 1920,
        "fps": 24,
    })
    session["i2v_video_settings"] = settings
    session["width"] = 1080
    session["height"] = 1920
    session["fps"] = 24
    return session

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tunnel", required=True)
    ap.add_argument("--kit", required=True)
    ap.add_argument("--project", default="")
    ap.add_argument("--name", default="CAMILA_PROD001_AUTO",
                    help="nombre del proyecto nuevo (si no se pasa --project)")
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
                   {"project_folder": a.name})
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
        # CRITICO (lección SameFileError): subir TAMBIEN como preview de escena.
        # Render All copia "imagen seleccionada" -> zimage_approved; si la seleccionada
        # ES la approved (custom vacío o reescrito por el rehydrate del load_session),
        # shutil.copy2 revienta con "are the same file". La preview vive en
        # scene_image_previews/ y el Builder la re-inyecta al image_history en cada
        # load -> fuente de render distinta del destino, a prueba de guardados.
        rp = post(T, "/vrgdg/music_builder/archive_scene_image",
                  {"project_folder": pf, "scene_number": s["n"],
                   "image_data": data_url(s["img"])}, timeout=300)
        s["preview_saved"] = rp.get("saved_path", "")
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
        seg = fresh_segment(molde, s, t0)
        segs.append(seg); t0 += s["dur"]
    session["segments"] = segs
    # settings críticos (las llaves exactas se validan contra el dump; ajustar si difieren)
    for k, v in (("video_type", "speaking"), ("videoType", "speaking"),
                 ("width", 1080), ("height", 1920), ("fps", 24)):
        if k in session: session[k] = v
    apply_production_settings(session)
    r = post(T, "/vrgdg/music_builder/save_session",
             {"audio_path": "", "project_folder": pf, "session": session}, timeout=120)
    print("[6] save_session:", json.dumps(r)[:300])
    print(f"\nLISTO. En el Builder: Load Project '{pf}' -> verificar 5 escenas pareadas -> Render All -> Build Full Video.")

if __name__ == "__main__":
    main()
