import { fal } from "@fal-ai/client";
import fs from "node:fs";

const KEY = process.env.FAL_KEY;
if (!KEY) { console.error("ERROR: falta FAL_KEY"); process.exit(1); }
fal.config({ credentials: KEY });

const imgPath = process.argv[2];
const outPath = process.argv[3] || "grilled_out.mp4";
if (!imgPath || !fs.existsSync(imgPath)) { console.error("ERROR: imagen no encontrada:", imgPath); process.exit(1); }

const prompt = `Cinematic food commercial with dynamic camera motion. The camera performs a smooth cinematic orbiting arc around a tall loaded gourmet burger (sesame brioche bun, beef patty, crispy broaster fried chicken, bacon, melted cheddar, a fried egg, crispy onions) on a dark plate, while slowly pushing in. Cinematic rack focus, dramatic warm side lighting, glowing orange embers and faint smoke drifting in the dark background, gentle steam rising from the burger. Premium, appetizing, high-contrast, moody, photorealistic. The burger keeps exactly the same shape, layers and ingredients the entire time.`;
const negative = "morphing, warping, deforming food, melting, ingredients changing, extra patties, hands, biting, a person entering frame, text, logo, watermark, distortion, heavy blur, low quality, jitter, flicker";

const buf = fs.readFileSync(imgPath);
const blob = new Blob([buf], { type: "image/jpeg" });
console.log("[1/3] Subiendo imagen a fal storage...");
const url = await fal.storage.upload(blob);
console.log("    OK:", url);

console.log("[2/3] Lanzando UNA generacion Kling v3 pro (10s, orbita dinamica, sin audio)...");
const result = await fal.subscribe("fal-ai/kling-video/v3/pro/image-to-video", {
  input: {
    start_image_url: url,
    prompt,
    duration: "10",
    negative_prompt: negative,
    generate_audio: false,
    shot_type: "intelligent",
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
