#!/usr/bin/env python3
"""Render, stitch y descarga headless para VRGDG V9 Video Builder.

Cadena idéntica a la UI v9:
build_i2v_prompt -> POST /prompt -> /history -> collect_scene_video
-> stitch_scene_videos -> /view.
"""
import argparse
import hashlib
import json
import os
import posixpath
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


DEFAULT_I2V_SETTINGS = {
    "use_gguf_model": True,
    "unet_name": "LTX-2.3-22B-distilled-1.1-Q6_K.gguf",
    "diffusion_model_name": "LTX_8bit\\ltx-2.3-22b-dev_transformer_only_int8_convrot.safetensors",
    "vae_name": "LTX23_video_vae_bf16.safetensors",
    "clip_name1": "gemma-3-12b-it-abliterated-sikaworld-high-fidelity-edition.safetensors",
    "clip_name2": "ltx-2.3_text_projection_bf16.safetensors",
    "upscale_model_name": "ltx-2.3-spatial-upscaler-x2-1.1.safetensors",
    "audio_vae_name": "LTX23_audio_vae_bf16.safetensors",
    "tail_loss_frames": 25,
    "pre_frames": 50,
}

class ApiError(RuntimeError):
    pass


class BuilderApi:
    def __init__(self, tunnel, timeout=180):
        self.tunnel = tunnel.rstrip("/")
        self.timeout = timeout

    def request(self, method, route, payload=None, timeout=None, raw=False):
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.tunnel + route,
            data=body,
            method=method,
            headers={"Content-Type": "application/json"} if body is not None else {},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout or self.timeout) as response:
                result = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ApiError(f"{method} {route} HTTP {exc.code}: {detail[:1200]}") from exc
        except urllib.error.URLError as exc:
            raise ApiError(f"{method} {route}: {exc.reason}") from exc
        if raw:
            return result
        data = json.loads(result or b"{}")
        if data.get("ok") is False or data.get("error"):
            raise ApiError(f"{method} {route}: {data.get('error')}")
        return data

    def get(self, route, **kwargs):
        return self.request("GET", route, **kwargs)

    def post(self, route, payload, **kwargs):
        return self.request("POST", route, payload, **kwargs)


def duration(segment):
    value = float(segment.get("duration") or 0)
    if value <= 0:
        value = float(segment.get("end") or 0) - float(segment.get("start") or 0)
    return max(0.25, value)


def slot_number(segment, index):
    return int(segment.get("overlay_slot_number") or index + 1)


def scene_fingerprint(session, segment, index):
    contract = segment.get("automation_contract") or {}
    stable = {
        "version": 1,
        "scene_id": segment.get("id") or f"scene-{index + 1}",
        "slot": slot_number(segment, index),
        "prompt": str(segment.get("i2v_prompt") or segment.get("prompt") or "").strip(),
        "image_path": str(segment.get("approved_image_path") or "").replace("\\", "/"),
        "audio_path": str(segment.get("custom_audio_path") or "").replace("\\", "/"),
        "duration": round(duration(segment), 4),
        "seed": settings_payload(session, segment)["seed"],
        "source_image_sha256": contract.get("source_image_sha256") or "",
        "source_audio_sha256": contract.get("source_audio_sha256") or "",
    }
    encoded = json.dumps(stable, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def clear_render_state(segment):
    segment.update({
        "video_path": "",
        "video_thumbnail_path": "",
        "video_folder": "",
        "video_status": "none",
        "preview_mode": "image",
    })


def scene_path_matches_slot(path, slot):
    normalized = str(path or "").replace("\\", "/").lower()
    filename = posixpath.basename(normalized)
    tokens = (f"video_{slot:04d}", f"scene_{slot:04d}", f"scene_{slot}")
    return any(token in filename for token in tokens)


def settings_payload(session, segment):
    global_settings = dict(session.get("i2v_video_settings") or {})
    settings = dict(global_settings)
    for key, default in DEFAULT_I2V_SETTINGS.items():
        if key not in settings or settings[key] in ("", None):
            settings[key] = default
    if segment.get("use_scene_i2v_video_settings"):
        settings.update(segment.get("i2v_video_settings") or {})
    loras = settings.get("loras") or []
    settings.update({
        "fps": int(settings.get("fps") or 24),
        "width": int(settings.get("width") or 1080),
        "height": int(settings.get("height") or 1920),
        # El seed global manda incluso si una escena heredó settings antiguos.
        "seed": int(global_settings.get("seed") or 69),
        "seed_mode": "fixed",
        "duration": duration(segment),
        "use_custom_loras": bool(settings.get("use_loras", settings.get("use_custom_loras", False))),
        "lora_count": int(settings.get("lora_count") or 0),
    })
    for index in range(4):
        lora = loras[index] if index < len(loras) else {}
        number = index + 1
        settings.setdefault(f"lora_{number}", lora.get("name", "[none]"))
        settings.setdefault(f"first_pass_strength_{number}", lora.get("first_pass_strength", lora.get("strength", 1)))
        settings.setdefault(f"second_pass_strength_{number}", lora.get("second_pass_strength", lora.get("strength", 1)))
    return settings


def prompt_failure(history, prompt_id):
    item = history.get(prompt_id) or {}
    messages = (item.get("status") or {}).get("messages") or []
    failures = []
    for message in messages:
        if not isinstance(message, list) or len(message) < 2:
            continue
        if message[0] in {"execution_error", "execution_interrupted"}:
            detail = message[1] if isinstance(message[1], dict) else {"message": message[1]}
            failures.append(str(detail.get("exception_message") or detail.get("message") or detail))
    return "\n".join(failures)


def history_finished(history, prompt_id):
    status = ((history.get(prompt_id) or {}).get("status") or {})
    return bool(status.get("completed") or status.get("status_str") in {"success", "error"})


def wait_queue_idle(api, timeout=600):
    started = time.monotonic()
    while time.monotonic() - started < timeout:
        queue = api.get("/queue")
        if not queue.get("queue_running") and not queue.get("queue_pending"):
            return
        time.sleep(2)
    raise ApiError("La cola de ComfyUI no quedó libre a tiempo")


def queue_prompt(api, prompt):
    wait_queue_idle(api)
    queued = api.post("/prompt", {
        "prompt": prompt,
        "client_id": str(uuid.uuid4()),
        # Evita los crashes v31 de VRGDG_ShowText y VHS_VideoCombine.
        "extra_data": {"extra_pnginfo": {"workflow": {"nodes": [], "extra": {}}}},
    })
    if queued.get("node_errors"):
        raise ApiError("Workflow rechazado: " + json.dumps(queued["node_errors"], ensure_ascii=False)[:2400])
    prompt_id = queued.get("prompt_id")
    if not prompt_id:
        raise ApiError("ComfyUI no devolvió prompt_id")
    return prompt_id


def wait_prompt(api, prompt_id, timeout):
    started = time.monotonic()
    while time.monotonic() - started < timeout:
        history = api.get("/history/" + urllib.parse.quote(prompt_id))
        failure = prompt_failure(history, prompt_id)
        if failure:
            raise ApiError(f"Prompt {prompt_id} falló:\n{failure}")
        if history_finished(history, prompt_id):
            return
        time.sleep(3)
    raise ApiError(f"Timeout esperando prompt {prompt_id} después de {timeout}s")


def load_project(api, project):
    loaded = api.post("/vrgdg/music_builder/load_session", {"project_folder": project})
    session = loaded.get("session") or {}
    segments = session.get("segments") or []
    if not segments:
        raise ApiError("El proyecto no tiene escenas")
    return loaded.get("project_folder") or project, session, segments


def validate_scene(segment, index):
    missing = []
    if not str(segment.get("i2v_prompt") or segment.get("prompt") or "").strip():
        missing.append("prompt I2V")
    if not str(segment.get("approved_image_path") or "").strip():
        missing.append("imagen aprobada")
    if not str(segment.get("custom_audio_path") or "").strip():
        missing.append("audio")
    if missing:
        raise ApiError(f"Escena {index + 1}: falta " + ", ".join(missing))


def recover_existing(api, project, session, segments):
    scan = api.post("/vrgdg/music_builder/scan_scene_videos", {"project_folder": project})
    videos = scan.get("videos") or {}
    for index, segment in enumerate(segments):
        slot = slot_number(segment, index)
        found = videos.get(str(slot))
        expected = scene_fingerprint(session, segment, index)
        reusable = (
            found
            and segment.get("render_contract_version") == 1
            and segment.get("render_fingerprint") == expected
            and scene_path_matches_slot(found, slot)
        )
        if reusable:
            segment["video_path"] = found
            segment["video_status"] = "done"
        else:
            clear_render_state(segment)


def render_scene(api, project, session, segment, index, timeout, force):
    slot = slot_number(segment, index)
    scene_duration = duration(segment)
    audio_path = str(segment.get("custom_audio_path") or "").strip()
    source_start = max(0.0, float(segment.get("custom_audio_source_start") or 0))
    trimmed = api.post("/vrgdg/music_builder/trim_scene_audio", {
        "project_folder": project,
        "scene_number": slot,
        "source_path": audio_path,
        "start": source_start,
        "duration": scene_duration,
    }, timeout=120)
    single_srt = api.post("/vrgdg/music_builder/save_single_scene_srt", {
        "project_folder": project,
        "scene_number": slot,
        "start_time": 0,
        "duration": scene_duration,
        "label": segment.get("label") or f"Scene {slot}",
    })
    payload = settings_payload(session, segment)
    payload.update({
        "i2v_prompt": str(segment.get("i2v_prompt") or segment.get("prompt") or "").strip(),
        "audio_path": trimmed.get("audio_path") or audio_path,
        "prompt_number_one_based": 1,
        "srt_path": single_srt.get("srt_path"),
        "project_folder": project,
        "image_folder": posixpath.join(project, "zimage_approved"),
        "image_index_zero_based": slot - 1,
    })
    built = api.post("/vrgdg/workflow_runner/build_i2v_prompt", payload)
    started_at = time.time() - 2
    prompt_id = queue_prompt(api, built.get("prompt") or {})
    print(f"    prompt {prompt_id}; esperando GPU...")
    wait_prompt(api, prompt_id, timeout)
    found = api.post("/vrgdg/workflow_runner/find_scene_video_output", {
        "project_folder": project,
        "video_mode": "i2v",
        "output_folder": built.get("output_folder") or posixpath.join(project, "image_to_video_clips"),
        "scene_number": slot,
        "prompt_number_one_based": 1,
        "min_mtime": started_at,
    })
    source = found.get("video_path")
    if not source:
        raise ApiError(f"Escena {slot}: terminó el prompt pero no apareció el MP4")
    collected = api.post("/vrgdg/workflow_runner/collect_scene_video", {
        "source_path": source,
        "project_folder": project,
        "scene_number": slot,
        "existing_action": "backup" if force else "overwrite",
    }, timeout=120)
    segment["video_path"] = collected.get("video_path") or source
    segment["video_thumbnail_path"] = collected.get("thumbnail_path") or ""
    segment["video_folder"] = collected.get("video_folder") or ""
    segment["video_status"] = "done"
    segment["preview_mode"] = "video"
    segment["render_contract_version"] = 1
    segment["render_fingerprint"] = scene_fingerprint(session, segment, index)
    return segment["video_path"]


def validate_stitch_paths(segments):
    paths = [str(segment.get("video_path") or "").strip() for segment in segments]
    if any(not path for path in paths):
        raise ApiError("No se puede hacer stitch: faltan clips")
    normalized = [path.replace("\\", "/").lower() for path in paths]
    if len(set(normalized)) != len(normalized):
        raise ApiError("No se puede hacer stitch: hay clips duplicados entre escenas")
    for index, path in enumerate(paths):
        slot = slot_number(segments[index], index)
        if not scene_path_matches_slot(path, slot):
            raise ApiError(f"Escena {index + 1}: el MP4 no corresponde al slot {slot}: {path}")
    return paths


def save_session(api, project, session):
    api.post("/vrgdg/music_builder/save_session", {
        "audio_path": "",
        "project_folder": project,
        "session": session,
    }, timeout=120)


def download_final(api, remote_path, destination):
    normalized = remote_path.replace("\\", "/")
    if "/output/" not in normalized:
        raise ApiError(f"FINAL fuera de /comfyui/output: {remote_path}")
    relative_path = normalized.split("/output/", 1)[1]
    subfolder, filename = posixpath.split(relative_path)
    route = "/view?" + urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": "output"})
    content = api.get(route, raw=True, timeout=600)
    destination = os.path.abspath(destination)
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as handle:
        handle.write(content)
    return destination


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tunnel", required=True)
    parser.add_argument("--project", required=True, help="project_folder remoto")
    parser.add_argument("--output", default="", help="MP4 local; por defecto usa el nombre remoto")
    parser.add_argument("--scene", type=int, default=0, help="solo una escena (1-based), sin stitch")
    parser.add_argument("--force", action="store_true", help="regenerar clips existentes")
    parser.add_argument("--dry-run", action="store_true", help="validar sin encolar GPU")
    parser.add_argument("--timeout", type=int, default=45 * 60, help="timeout por escena")
    args = parser.parse_args()

    api = BuilderApi(args.tunnel)
    project, session, segments = load_project(api, args.project)
    recover_existing(api, project, session, segments)
    targets = [(i, s) for i, s in enumerate(segments) if not args.scene or i + 1 == args.scene]
    if args.scene and not targets:
        raise ApiError(f"No existe la escena {args.scene}")
    for index, segment in targets:
        validate_scene(segment, index)
    seed = settings_payload(session, targets[0][1])["seed"]
    print(f"Proyecto: {project}")
    print(f"Plan: {len(targets)} escena(s), seed fijo {seed}")
    if args.dry_run:
        for index, segment in targets:
            action = "skip existente" if segment.get("video_path") and not args.force else "render"
            print(f"  esc{index + 1}: {action}, {duration(segment):.2f}s")
        return 0

    for index, segment in targets:
        if segment.get("video_path") and not args.force:
            print(f"[{index + 1}/{len(segments)}] clip existente; se conserva")
            continue
        print(f"[{index + 1}/{len(segments)}] render {duration(segment):.2f}s")
        path = render_scene(api, project, session, segment, index, args.timeout, args.force)
        save_session(api, project, session)
        print(f"    listo: {path}")

    if args.scene:
        print("Escena lista. Stitch omitido por --scene.")
        return 0
    paths = validate_stitch_paths(segments)
    audio_items = [{
        "path": segment.get("custom_audio_path"),
        "start": max(0.0, float(segment.get("custom_audio_source_start") or 0)),
        "duration": duration(segment),
    } for segment in segments]
    settings = session.get("i2v_video_settings") or {}
    stitched = api.post("/vrgdg/workflow_runner/stitch_scene_videos", {
        "scene_paths": paths,
        "audio_path": "",
        "scene_audio_paths": [item["path"] for item in audio_items],
        "scene_audio_items": audio_items,
        "use_embedded_scene_audio": False,
        "overlay_items": [],
        "project_folder": project,
        "width": int(settings.get("width") or 1080),
        "height": int(settings.get("height") or 1920),
        "audio_start": 0,
        "audio_duration": 0,
        "output_prefix": "FINAL_VIDEO",
    }, timeout=20 * 60)
    remote_final = stitched.get("final_video_path")
    if not remote_final:
        raise ApiError("Stitch terminó sin final_video_path")
    session["final_video_path"] = remote_final
    save_session(api, project, session)
    destination = args.output or os.path.basename(remote_final)
    print(f"FINAL descargado: {download_final(api, remote_final, destination)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ApiError, ValueError) as exc:
        print(f"[X] {exc}", file=sys.stderr)
        raise SystemExit(1)
