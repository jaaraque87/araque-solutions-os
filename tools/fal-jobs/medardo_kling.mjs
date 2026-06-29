import { fal } from "@fal-ai/client";
import fs from "node:fs";

const KEY = process.env.FAL_KEY;
if (!KEY) { console.error("ERROR: falta FAL_KEY"); process.exit(1); }
fal.config({ credentials: KEY });

const imgPath = process.argv[2];
const outPath = process.argv[3] || "medardo_out.mp4";
if (!imgPath || !fs.existsSync(imgPath)) { console.error("ERROR: imagen no encontrada:", imgPath); process.exit(1); }

const prompt = `Cinematic drone-style food commercial. The camera slowly descends and pushes in toward a gourmet double cheeseburger on a wooden board, with a gentle lateral drift, always staying IN FRONT of the burger — it never rotates around to the back. Warm retro American diner lighting; a classic deep-red vintage pickup truck and a Route 66 mural glow softly out of focus in the background; gentle steam rising; glossy melted cheese; premium, appetizing, photorealistic, warm nostalgic color grade. The burger, the truck and the whole scene stay exactly the same the entire time.`;
const negative = "orbiting to the back, 360 rotation, revealing the back of the burger, camera spinning around, morphing, warping, deforming food, changing ingredients, extra patties, distorted truck, people entering frame, text, watermark, low quality, jitter, flicker";

const buf = fs.readFileSync(imgPath);
const blob = new Blob([buf], { type: "image/png" });
console.log("[1/3] Subiendo imagen a fal storage...");
const url = await fal.storage.upload(blob);
console.log("    OK:", url);

console.log("[2/3] Lanzando UNA generacion Kling v3 pro (10s, dron dolly-in frontal, sin audio)...");
const result = await fal.subscribe("fal-ai/kling-video/v3/pro/image-to-video", {
  input: { start_image_url: url, prompt, duration: "10", negative_prompt: negative, generate_audio: false },
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
