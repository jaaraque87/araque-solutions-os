import { fal } from "@fal-ai/client";
import fs from "node:fs";

const KEY = process.env.FAL_KEY;
if (!KEY) { console.error("ERROR: falta FAL_KEY"); process.exit(1); }
fal.config({ credentials: KEY });

const imgPath = process.argv[2];
const outPath = process.argv[3] || "kling_out.mp4";
if (!imgPath || !fs.existsSync(imgPath)) { console.error("ERROR: imagen no encontrada:", imgPath); process.exit(1); }

const prompt = `Cinematic food commercial shot. Very slow, smooth dolly-in toward a towering gourmet triple-kebab burger on an ornate golden plate, sitting on the grass of a packed night football stadium. Real steam gently rises and curls upward from the burger. Stadium floodlights softly flare and the crowd lights twinkle with shallow depth-of-field bokeh in the background. The glossy white sauce subtly glistens. Gentle, premium, appetizing motion; warm golden cinematic lighting; photorealistic. The burger keeps exactly the same shape, layers and ingredients the entire time.`;
const negative = "morphing, warping, deforming food, melting, ingredients changing, extra patties, hands, biting, a person entering frame, text, logo, watermark, distortion, heavy blur, low quality, shaky camera, flicker";

const buf = fs.readFileSync(imgPath);
const blob = new Blob([buf], { type: "image/jpeg" });
console.log("[1/3] Subiendo imagen a fal storage...");
const url = await fal.storage.upload(blob);
console.log("    OK:", url);

console.log("[2/3] Lanzando UNA generacion Kling v3 pro (10s, 720+/4:5, sin audio)...");
const result = await fal.subscribe("fal-ai/kling-video/v3/pro/image-to-video", {
  input: {
    start_image_url: url,
    prompt,
    duration: "10",
    negative_prompt: negative,
    generate_audio: false,
  },
  logs: true,
  onQueueUpdate: (u) => { if (u.status) console.log("    status:", u.status); },
});

const vurl = result?.data?.video?.url;
console.log("    video url:", vurl);
if (!vurl) { console.error("ERROR: respuesta sin video:", JSON.stringify(result).slice(0, 900)); process.exit(2); }

console.log("[3/3] Descargando MP4...");
const resp = await fetch(vurl);
const ab = await resp.arrayBuffer();
fs.writeFileSync(outPath, Buffer.from(ab));
console.log("LISTO:", outPath, "-", fs.statSync(outPath).size, "bytes");
