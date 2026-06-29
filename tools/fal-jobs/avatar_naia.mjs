import { fal } from "@fal-ai/client";
import fs from "node:fs";

const KEY = process.env.FAL_KEY;
if (!KEY) { console.error("ERROR: falta FAL_KEY"); process.exit(1); }
fal.config({ credentials: KEY });

const img = process.argv[2] || "naia-ugc.png";
const aud = process.argv[3] || "naia-voz.mp3";
const out = process.argv[4] || "naia_avatar.mp4";
for (const p of [img, aud]) {
  if (!fs.existsSync(p)) { console.error("ERROR: no existe:", p); process.exit(1); }
}

const prompt = "natural confident hand and head gestures, relaxed charismatic delivery, subtle realistic movement, she connects with the camera";

function mime(p) {
  const e = p.toLowerCase();
  if (e.endsWith(".mp3")) return "audio/mpeg";
  if (e.endsWith(".wav")) return "audio/wav";
  if (e.endsWith(".m4a")) return "audio/mp4";
  if (e.endsWith(".aac")) return "audio/aac";
  if (e.endsWith(".ogg")) return "audio/ogg";
  return "application/octet-stream";
}
async function up(p, t) { return await fal.storage.upload(new Blob([fs.readFileSync(p)], { type: t })); }

console.log("[1/3] Subiendo imagen y audio a fal storage...");
const imgUrl = await up(img, "image/png");
const audUrl = await up(aud, mime(aud));
console.log("    img:", imgUrl);
console.log("    aud:", audUrl);

if (process.env.DRY_RUN) {
  console.log("[DRY RUN] input listo (image_url + audio_url + prompt). NO se llamo a subscribe. Sin gasto.");
  process.exit(0);
}

console.log("[2/3] Lanzando Kling AI Avatar v2 PRO (image + audio -> talking, ~$0.115/s)...");
const r = await fal.subscribe("fal-ai/kling-video/ai-avatar/v2/pro", {
  input: { image_url: imgUrl, audio_url: audUrl, prompt },
  logs: true,
  onQueueUpdate: (u) => { if (u.status) console.log("    status:", u.status); },
});

const vurl = r?.data?.video?.url;
console.log("    video url:", vurl);
if (!vurl) { console.error("ERROR: respuesta sin video:", JSON.stringify(r).slice(0, 900)); process.exit(2); }

console.log("[3/3] Descargando MP4...");
const resp = await fetch(vurl);
fs.writeFileSync(out, Buffer.from(await resp.arrayBuffer()));
console.log("LISTO:", out, "-", fs.statSync(out).size, "bytes");
