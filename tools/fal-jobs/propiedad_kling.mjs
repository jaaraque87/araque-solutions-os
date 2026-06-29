import { fal } from "@fal-ai/client";
import fs from "node:fs";

const KEY = process.env.FAL_KEY;
if (!KEY) { console.error("ERROR: falta FAL_KEY"); process.exit(1); }
fal.config({ credentials: KEY });

const imgPath = process.argv[2];
const outPath = process.argv[3] || "propiedad_out.mp4";
if (!imgPath || !fs.existsSync(imgPath)) { console.error("ERROR: imagen no encontrada:", imgPath); process.exit(1); }

const prompt = `Cinematic luxury real estate film, aspirational and elegant. A very slow, smooth dolly push-in toward a modern two-story villa at golden hour; warm interior lights glow softly through the large windows; gentle reflections ripple on the pool water; soft clouds drift slowly in the sky; subtle warm light shift across the architecture. Premium, photorealistic, high-end architectural cinematography, anamorphic, warm elegant color grade, shallow depth of field. The building, architecture and layout stay exactly the same the entire time.`;
const negative = "morphing, warping, deforming building, changing architecture, extra buildings, distorted windows, people walking in, cars appearing, text, watermark, low quality, jitter, flicker, fisheye, lens distortion, camera spinning, orbiting to the back";

const buf = fs.readFileSync(imgPath);
const blob = new Blob([buf], { type: "image/png" });
console.log("[1/3] Subiendo imagen a fal storage...");
const url = await fal.storage.upload(blob);
console.log("    OK:", url);

console.log("[2/3] Lanzando UNA generacion Kling v3 pro (10s, push-in inmobiliario, sin audio)...");
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
