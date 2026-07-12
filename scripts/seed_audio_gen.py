#!/usr/bin/env python3
"""Generate audio with ByteDance Seed Audio 1.0 via fal queue API.

Usage:
  python3 scripts/seed_audio_gen.py --prompt "..." --out scratch/seed-audio-probes/test.mp3
  python3 scripts/seed_audio_gen.py --prompt-file prompt.txt --out out.mp3
"""
import argparse, json, os, sys, time, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://queue.fal.run/bytedance/seed-audio-1.0"


def load_fal_key():
    key = os.environ.get("FAL_API_KEY") or os.environ.get("FAL_KEY")
    if key:
        return key
    env_path = os.path.join(REPO, ".env")
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("FAL_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"')
    sys.exit("FAL_API_KEY not found in env or .env")


def generate(prompt, out_path, key, max_wait=600):
    if len(prompt) > 2048:
        sys.exit(f"Prompt too long: {len(prompt)} chars (Seed Audio max 2048). "
                 "Note: the API accepts the submit and only 422s on the response fetch.")
    data = json.dumps({"prompt": prompt}).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=data, method="POST")
    req.add_header("Authorization", f"Key {key}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        job = json.loads(resp.read())

    status_url = job["status_url"]
    response_url = job["response_url"]
    waited = 0
    while waited < max_wait:
        time.sleep(5)
        waited += 5
        sreq = urllib.request.Request(status_url)
        sreq.add_header("Authorization", f"Key {key}")
        with urllib.request.urlopen(sreq, timeout=30) as resp:
            status = json.loads(resp.read())
        state = status.get("status")
        print(f"  [{waited}s] {state}")
        if state == "COMPLETED":
            break
        if state in ("FAILED", "ERROR"):
            sys.exit(f"Job failed: {json.dumps(status)}")
    else:
        sys.exit("Timed out waiting for job")

    rreq = urllib.request.Request(response_url)
    rreq.add_header("Authorization", f"Key {key}")
    with urllib.request.urlopen(rreq, timeout=30) as resp:
        result = json.loads(resp.read())

    audio = result.get("audio") or {}
    audio_url = audio.get("url")
    if not audio_url:
        sys.exit(f"No audio url in response: {json.dumps(result)[:500]}")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    dreq = urllib.request.Request(audio_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(dreq, timeout=120) as resp, open(out_path, "wb") as f:
        f.write(resp.read())
    meta_path = os.path.splitext(out_path)[0] + ".json"
    with open(meta_path, "w") as f:
        json.dump({"prompt": prompt, "result": result}, f, indent=2, ensure_ascii=False)
    print(f"Saved {out_path} ({os.path.getsize(out_path)} bytes) + {meta_path}")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt")
    ap.add_argument("--prompt-file")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if args.prompt_file:
        prompt = open(args.prompt_file).read().strip()
    elif args.prompt:
        prompt = args.prompt
    else:
        sys.exit("Pass --prompt or --prompt-file")
    generate(prompt, args.out, load_fal_key())
