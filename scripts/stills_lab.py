#!/usr/bin/env python3
"""
stills_lab.py — Cinematographic reference harvester for the art-direction layer.

Drives StillsLab (https://stillslab.com) headless with Playwright and extracts,
per still, the full technical ficha that maps 1:1 onto the CDD:
director, cinematographer, camera, lens, color, lighting, time of day, INT/EXT,
aspect ratio, frame size, shot type, composition + extracted palette HEX + the
full-res frame.

StillsLab has no public JSON API (Next.js Server Actions render data client-side),
but it publishes /llms.txt inviting agent use and documents its query syntax:
  - Semantic search:  /filter?search=<scene description in plain language>
  - Structured facets: ?camera=Arri+Alexa  ?lighting=...  ?aspect_ratio=2.39
                       ?interior_exterior=Interior&time_of_day=Night
This scraper reads the rendered detail panel for each result. It is the PRIMARY
cinematography source; Are.na (mood) is complementary; Film-Grab is plan-B fallback.

Be a good citizen: light pulls only (default 6 stills), reference use, not bulk
redistribution. Respects robots (never touches /admin, /settings, /data/).

Usage:
  python3 scripts/stills_lab.py \
      --out outputs/ugc/<run>/references/stills_lab \
      --search "tired person at a home office desk, warm window light" \
      --n 6
  # or with facets appended:
  python3 scripts/stills_lab.py --out <dir> \
      --search "home office" --facets "interior_exterior=Interior&time_of_day=Day&lighting=Soft+light" --n 6
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote_plus

import requests
from playwright.sync_api import sync_playwright

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124 Safari/537.36")

FIELD_LABELS = ["Director", "Cinematographer", "Actors", "Color", "INT/EXT",
                "Time of Day", "Aspect Ratio", "Frame Size", "Shot Type",
                "Composition", "Lighting", "Ethnicity", "Camera", "Lenses", "Country"]

EXTRACT_JS = r"""() => {
  const overlays = [...document.querySelectorAll('div.fixed.inset-0')];
  const overlay = overlays.find(o => /ASPECT RATIO|DIRECTOR/i.test(o.innerText)) || overlays[0];
  if(!overlay) return {err:'no overlay'};
  const txt = overlay.innerText;
  const pairs = {};
  const labels = %LABELS%;
  for(const lab of labels){
    const el = [...overlay.querySelectorAll('*')].find(e =>
       e.children.length===0 && e.textContent.trim().toLowerCase()===lab.toLowerCase());
    if(el){
      let v = el.nextElementSibling && el.nextElementSibling.textContent.trim();
      if(!v && el.parentElement) v = el.parentElement.textContent.replace(el.textContent,'').trim();
      pairs[lab] = (v||'').replace(/\s*…$/,'').trim();
    }
  }
  const img = [...overlay.querySelectorAll('img')]
      .sort((a,b)=>(b.naturalWidth||0)-(a.naturalWidth||0))[0];
  return {overlayText: txt, pairs, image_url: img ? (img.currentSrc||img.src) : null};
}""".replace("%LABELS%", json.dumps(FIELD_LABELS))


def parse_header(overlay_text):
    """Palette HEX (leading #lines), then 'Title(Year)', then tags line."""
    lines = [l.strip() for l in overlay_text.splitlines()]
    palette, i = [], 0
    while i < len(lines) and re.fullmatch(r"#[0-9A-Fa-f]{6}", lines[i]):
        palette.append(lines[i].upper()); i += 1
    title, year, tags = "", "", []
    rest = [l for l in lines[i:] if l]
    if rest:
        m = re.match(r"(.*?)\((\d{4})\)\s*$", rest[0])
        if m:
            title, year = m.group(1).strip(), m.group(2)
        else:
            title = rest[0]
        if len(rest) > 1 and "," in rest[1] and rest[1] not in FIELD_LABELS:
            tags = [t.strip() for t in rest[1].split(",") if t.strip()]
    return palette, title, year, tags


def clean(item):
    p = item.pop("pairs", {})
    palette, title, year, tags = parse_header(item.pop("overlayText", ""))
    return {
        "source": "stills_lab",
        "title": title, "year": year, "tags": tags,
        "director": p.get("Director", ""),
        "cinematographer": p.get("Cinematographer", ""),
        "actors": p.get("Actors", ""),
        "color": p.get("Color", ""),
        "int_ext": p.get("INT/EXT", ""),
        "time_of_day": p.get("Time of Day", ""),
        "aspect_ratio": p.get("Aspect Ratio", ""),
        "frame_size": p.get("Frame Size", ""),
        "shot_type": p.get("Shot Type", ""),
        "composition": p.get("Composition", ""),
        "lighting": p.get("Lighting", ""),
        "camera": p.get("Camera", ""),
        "lens": p.get("Lenses", ""),
        "country": p.get("Country", ""),
        "palette": palette,
        "image_url": item.get("image_url"),
    }


def download(url, dest):
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=25)
        r.raise_for_status()
        dest.write_bytes(r.content)
        return True
    except Exception:
        return False


def slug(s, n=40):
    return (re.sub(r"[^a-z0-9]+", "-", (s or "still").lower()).strip("-")[:n]) or "still"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--search", required=True, help="natural-language scene description")
    ap.add_argument("--facets", default="", help="raw extra query string, e.g. 'time_of_day=Day'")
    ap.add_argument("--n", type=int, default=6)
    args = ap.parse_args()

    out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)
    url = f"https://stillslab.com/filter?search={quote_plus(args.search)}"
    if args.facets:
        url += "&" + args.facets

    results = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(user_agent=UA, viewport={"width": 1440, "height": 900}, locale="en-US")
        pg = ctx.new_page()
        print(f"[stills_lab] {url}")
        pg.goto(url, wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_function(
            "() => [...document.querySelectorAll('img')].filter(i=>(i.naturalWidth||0)>200).length >= 3",
            timeout=30000)
        pg.wait_for_timeout(1800)
        cards = pg.locator("button.group.relative")
        total = cards.count()
        n = min(args.n, total)
        print(f"[stills_lab] {total} results, capturing {n}")
        for i in range(n):
            try:
                cards.nth(i).click()
                pg.wait_for_function(
                    "() => [...document.querySelectorAll('div.fixed.inset-0')]"
                    ".some(o=>/ASPECT RATIO|DIRECTOR/i.test(o.innerText))", timeout=12000)
                pg.wait_for_timeout(500)
                raw = pg.evaluate(EXTRACT_JS)
                if raw.get("err"):
                    print(f"  [{i}] {raw['err']}"); pg.keyboard.press("Escape"); pg.wait_for_timeout(600); continue
                item = clean(raw)
                results.append(item)
                print(f"  [{i}] {item['title']} ({item['year']}) — DP {item['cinematographer'] or '—'} | "
                      f"{item['lighting'] or '—'} | {item['color'] or '—'}")
            except Exception as e:
                print(f"  [{i}] FAILED: {str(e)[:80]}")
            finally:
                pg.keyboard.press("Escape")
                pg.wait_for_timeout(700)
        b.close()

    ok = 0
    for idx, it in enumerate(results, 1):
        if it.get("image_url"):
            ext = ".webp" if ".webp" in it["image_url"] else ".jpg"
            fname = f"{idx:02d}_{slug(it['title'])}{ext}"
            if download(it["image_url"], out_dir / fname):
                it["file"] = fname; ok += 1
    (out_dir / "metadata.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\n[stills_lab] {len(results)} fichas, {ok} images -> {out_dir}")
    print(f"[stills_lab] manifest: {out_dir / 'metadata.json'}")


if __name__ == "__main__":
    main()
