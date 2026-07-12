#!/usr/bin/env python3
"""Mix a voice stem with an ambience/SFX bed into one Seedance-ready track.

Measures loudness of both stems, places the bed N dB below the voice, mixes,
masters to a target LUFS with a true-peak limiter, verifies the result and
caps duration (Seedance reference audio max: 15s).

Usage:
  python3 scripts/seed_audio_mix.py --voice voz.mp3 --bed sfx.mp3 --out mix.wav \
      [--bed-offset-db 10] [--target-lufs -14] [--max-duration 15]
"""
import argparse, json, re, subprocess, sys

FFMPEG = "ffmpeg"


def measure(path, extra_filter=None):
    af = "ebur128=peak=true"
    if extra_filter:
        af = extra_filter + "," + af
    proc = subprocess.run(
        [FFMPEG, "-hide_banner", "-i", path, "-af", af, "-f", "null", "-"],
        capture_output=True, text=True)
    tail = proc.stderr[-2000:]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    if not i:
        sys.exit(f"Could not measure loudness of {path}:\n{tail}")
    return float(i.group(1)), (float(tp.group(1)) if tp else None)


def duration_of(path):
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(proc.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", required=True)
    ap.add_argument("--bed", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bed-offset-db", type=float, default=10.0,
                    help="How many dB the bed sits below the voice (default 10)")
    ap.add_argument("--target-lufs", type=float, default=-14.0)
    ap.add_argument("--max-duration", type=float, default=15.0)
    args = ap.parse_args()

    voice_i, voice_tp = measure(args.voice)
    bed_i, bed_tp = measure(args.bed)
    bed_gain = (voice_i - args.bed_offset_db) - bed_i
    total = min(max(duration_of(args.voice), duration_of(args.bed)), args.max_duration)

    # Pre-mix at computed gains, then measure and apply static master gain +
    # true-peak limiter (static gain + verify instead of loudnorm: linear
    # loudnorm silently under-gains when the TP cap kicks in).
    premix_filter = (
        f"[1:a]volume={bed_gain:.2f}dB[bed];"
        f"[0:a][bed]amix=inputs=2:duration=longest:normalize=0[mix];"
        f"[mix]atrim=0:{total:.3f}[outa]"
    )
    tmp = args.out + ".premix.wav"
    subprocess.run(
        [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
         "-i", args.voice, "-i", args.bed,
         "-filter_complex", premix_filter, "-map", "[outa]", tmp],
        check=True)

    mix_i, mix_tp = measure(tmp)
    master_gain = args.target_lufs - mix_i
    subprocess.run(
        [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", tmp,
         "-af", f"volume={master_gain:.2f}dB,alimiter=limit=0.84:level=false",
         args.out],
        check=True)
    final_i, final_tp = measure(args.out)

    report = {
        "voice_lufs": voice_i, "bed_lufs": bed_i,
        "bed_gain_db": round(bed_gain, 2),
        "bed_offset_db": args.bed_offset_db,
        "premix_lufs": mix_i, "master_gain_db": round(master_gain, 2),
        "final_lufs": final_i, "final_true_peak_dbfs": final_tp,
        "duration_s": round(duration_of(args.out), 3),
        "out": args.out,
    }
    with open(args.out + ".mixreport.json", "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))
    subprocess.run(["rm", "-f", tmp])


if __name__ == "__main__":
    main()
