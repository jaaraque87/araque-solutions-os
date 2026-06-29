import { fal } from "@fal-ai/client";
import fs from "node:fs";

const KEY = process.env.FAL_KEY;
if (!KEY) { console.error("ERROR: falta FAL_KEY"); process.exit(1); }
fal.config({ credentials: KEY });

const imgPath = process.argv[2];
const outPath = process.argv[3] || "blacklava_out.mp4";
if (!imgPath || !fs.existsSync(imgPath)) { console.error("ERROR: imagen no encontrada:", imgPath); process.exit(1); }

const prompt = `Premium cinematic food commercial, elegant and dark, conveying exclusivity and a sensory experience. The camera stays IN FRONT of a gourmet double cheeseburger (golden brioche bun, double beef patty, melted cheddar, crispy onions) on a black plate and performs a very slow, gentle dolly push-in with a subtle side-to-side parallax, always keeping the FRONT of the burger facing the camera — it never rotates around to the back. A warm rim light gently shifts across the glossy melted cheese, the juicy texture and gentle rising steam. Low-key chiaroscuro lighting, deep black elegant background with soft bokeh and a refined warm glow, subtle anamorphic light. High-end advertising look, cinematic color grade, photorealistic, appetizing, sensual food detail. The burger keeps exactly the same shape, layers and ingredients the entire time.`;
const negative = "orbiting, 360 rotation, circling to the back, camera revealing the back of the burger, turning around, new toppings appearing, extra food, extra onions, added ingredients, changing ingredients, morphing, warping, deforming food, melting away, extra patties, hands, biting, person entering frame, distortion, heavy blur, low quality, jitter, flicker, harsh flat lighting, watermark";

const buf = fs.readFileSync(imgPath);
const blob = new Blob([buf], { type: "image/png" });
console.log("[1/3] Subiendo imagen a fal storage...");
const url = await fal.storage.upload(blob);
console.log("    OK:", url);

console.log("[2/3] Lanzando UNA generacion Kling v3 pro (10s, orbita premium, sin audio)...");
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
