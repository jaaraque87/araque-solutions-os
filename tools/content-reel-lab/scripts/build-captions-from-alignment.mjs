import { readFileSync, writeFileSync } from "node:fs";

const A = JSON.parse(readFileSync("C:/Users/usuar/Downloads/naia-piloto-004/alignment.json", "utf8"));
const chars = A.characters, starts = A.character_start_times_seconds, ends = A.character_end_times_seconds;

// Cortes originales del master continuo y arranques nuevos en el timeline ensamblado (dur mp3 + 0.1 gap)
const O = [0, 5.508, 9.422, 14.139, 18.879, 23.096, 27.141, 32.216, 36.764];
const D = [5.51, 3.92, 4.73, 4.73, 4.23, 4.02, 5.09, 4.55, 5.61];
const N = []; let acc = 0;
for (let i = 0; i < 9; i++) { N.push(acc); acc += D[i] + 0.1; }
const segOf = t => { for (let i = 8; i >= 0; i--) if (t >= O[i] - 0.01) return i; return 0; };
const remap = t => { const k = segOf(t); return (t - O[k]) + N[k]; };

// Palabras (excluyendo tags [ ... ])
const words = [];
let cur = null, inTag = false;
for (let i = 0; i < chars.length; i++) {
  const c = chars[i];
  if (c === "[") { inTag = true; if (cur) { words.push(cur); cur = null; } continue; }
  if (c === "]") { inTag = false; continue; }
  if (inTag) continue;
  if (c === " " || c === "\n") { if (cur) { words.push(cur); cur = null; } continue; }
  if (!cur) cur = { text: c, start: starts[i], end: ends[i] };
  else { cur.text += c; cur.end = ends[i]; }
}
if (cur) words.push(cur);

// Chunks canon: max 3 palabras, puntuacion terminal = frontera dura, gap >0.6s = frontera
const chunks = []; let ch = [];
const flush = () => { if (ch.length) { chunks.push(ch); ch = []; } };
for (let i = 0; i < words.length; i++) {
  ch.push(words[i]);
  const t = words[i].text;
  const terminal = /[.?!â€¦]$/.test(t.replace(/["Â»)]+$/, ""));
  const nextGap = i + 1 < words.length ? words[i + 1].start - words[i].end : 0;
  if (terminal || ch.length >= 3 || nextGap > 0.6) flush();
}
flush();

const toAss = t => { const h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60), s = (t % 60); return `${h}:${String(m).padStart(2, "0")}:${s.toFixed(2).padStart(5, "0")}`; };

let ev = "";
for (let i = 0; i < chunks.length; i++) {
  const c = chunks[i];
  const st = remap(c[0].start);
  let en = remap(c[c.length - 1].end) + 0.10;
  if (i + 1 < chunks.length) en = Math.min(en, remap(chunks[i + 1][0].start) - 0.02);
  const text = c.map(w => w.text).join(" ").toUpperCase().replace(/[{}]/g, "");
  const style = st < 5.0 ? "CAPHI" : "CAP"; ev += `Dialogue: 0,${toAss(st)},${toAss(en)},${style},,0,0,0,,{\\fad(50,30)}${text}\n`;
}

const ass = `[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: CAP,Arial,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,1,0,1,3.5,1,2,60,60,742,1
Style: CAPHI,Arial,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,1,0,1,3.5,1,2,60,60,900,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
${ev}`;
writeFileSync("C:/Users/usuar/Downloads/naia-piloto-004/captions_canon.ass", ass, "utf8");
console.log(`chunks: ${chunks.length}, palabras: ${words.length}, ultimo fin: ${remap(words[words.length-1].end).toFixed(2)}s`);

