#!/usr/bin/env python3
"""
Retime exacto + remux de voz original — pipeline FIJO de la skill omni-edit.

Regla pagada: Omni devuelve el video ~1% más largo que la fuente y REGENERA el audio
(sílabas inventadas) en conversiones de aspecto / reemplazo total de mundo. Este script:
  1. Mide duraciones con ffprobe (fuente vs render).
  2. Retima el render: setpts=PTS*(dur_fuente/dur_render), fps=25, sin audio.
  3. Remuxea la VOZ ORIGINAL de la fuente (-map 0:v -map 1:a).

Uso:  py tools\\omni-flash\\remux_voice.py render.mp4 fuente.mp4 final.mp4
Luego: QA de lip-sync en 6 timestamps distribuidos (regla de la skill).
"""
import subprocess, sys, os

def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    return float(out.stdout.strip())

def main():
    if len(sys.argv) != 4:
        sys.exit("uso: remux_voice.py <render_omni.mp4> <fuente_con_voz.mp4|.wav|.mp3> <salida.mp4>")
    render, fuente, salida = sys.argv[1:4]
    d_src, d_ren = dur(fuente), dur(render)
    factor = d_src / d_ren
    print(f"fuente={d_src:.3f}s  render={d_ren:.3f}s  factor setpts={factor:.5f}")
    tmp = salida + ".retimed.tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", render, "-vf", f"setpts=PTS*{factor:.6f},fps=25",
                    "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium", tmp], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", tmp, "-i", fuente, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", salida], check=True)
    os.remove(tmp)
    print(f"OK → {salida}")
    print("Siguiente (regla skill): QA lip-sync en 6 timestamps distribuidos, post-retime.")

if __name__ == "__main__":
    main()
