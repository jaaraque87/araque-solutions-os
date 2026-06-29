import { fal } from "@fal-ai/client";
import fs from "node:fs";

const KEY = process.env.FAL_KEY;
if (!KEY) { console.error("ERROR: falta FAL_KEY"); process.exit(1); }
fal.config({ credentials: KEY });

const startPath = process.argv[2] || "naia-anchor.png";
const endPath   = process.argv[3] || "naia-end.png";
const outPath   = process.argv[4] || "naia_seedance.mp4";
for (const p of [startPath, endPath]) {
  if (!fs.existsSync(p)) { console.error("ERROR: no existe:", p); process.exit(1); }
}

const prompt = `Hyper-real cinematic food-commercial with EXTREME dynamic physics, mixing high-speed and slow-motion, action-movie energy, ending on a charismatic personality beat. Shot on a professional cinema camera with a 35mm lens, shallow depth of field, premium food-commercial color grade, golden-hour warm light; realistic handheld camera energy (not sterile), going fully handheld during the earthquake beat.

The woman is Naia: keep her identity EXACTLY as the start and end frames (oval face, hazel/olive-green eyes, short straight black bob, black-framed glasses, warm pale-olive skin, freckles, real skin texture). She is EXPRESSIVE, warm, confident and charismatic, with lively eyes and natural micro-expressions; she connects with the camera and is never stiff or robotic. The double cheeseburger keeps the exact same ingredients, layers and shape the entire time; it never morphs, melts or deforms. Same loft kitchen, marble counter and city/water view throughout.

[0-3s] Medium shot, locked, with a sudden hard camera jolt at 2.5s. Naia looks into the lens with a confident playful smirk and powerfully launches the double cheeseburger straight up out of her hands. SFX: low rumble building, sharp whoosh on the launch.

[3-6.5s] Sweeping slow-motion tracking shot following the burger as it soars in a dramatic arc across the kitchen, glistening melted cheese and juices, sesame seeds catching the light, weightless and intact. SFX: airy slow whoosh, suspended tension.

[6.5-8.5s] Violent earthquake camera shake, heavy handheld, motion blur. The whole kitchen trembles, cabinets rattle, fine dust falls, the marble counter shakes. SFX: deep earthquake bass rumble, rattling dishes.

[8.5-11s] Low-angle close-up on a white plate, snapping into slow-motion on impact. The burger slams down perfectly onto the plate on the marble counter, sending a shockwave ripple, crumbs and sesame seeds bouncing, settling into a perfect hero food shot. SFX: heavy impact thud with reverb, then a beat of quiet.

[11-15s] Medium shot, slow push-in with slight residual shake, matching the end frame. Naia leans into frame beside the plated burger, full of confident charisma, looks directly into the lens with a playful smirk and gives the camera a single confident charismatic wink as she speaks; glasses stay on; mouth clearly visible and readable for lip-sync. She speaks one line in Spanish with a young woman's voice, neutral Latin-American Spanish accent, warm and confident: "Todo lo que viste... lo hizo Araque Solutions. Escribenos."

Avoid: robotic face, stiff expression, dead eyes, mismatched lip-sync, glasses glitching or melting, morphing or deforming burger, changing ingredients, extra patties, distorted hands, extra fingers, changed face, different person, different eyes, beauty filter, waxy plastic skin, duplicate woman, broken kitchen geometry, on-screen text, watermark, low quality, jitter, flicker.`;

async function up(p) {
  const blob = new Blob([fs.readFileSync(p)], { type: "image/png" });
  return await fal.storage.upload(blob);
}

console.log("[1/3] Subiendo frames a fal storage...");
const startUrl = await up(startPath);
const endUrl   = await up(endPath);
console.log("    start:", startUrl);
console.log("    end:  ", endUrl);

const input = {
  prompt,
  image_url: startUrl,
  end_image_url: endUrl,
  duration: 15,
  resolution: "720p",
  aspect_ratio: "9:16",
  generate_audio: true,
  bitrate_mode: "high",
};

if (process.env.DRY_RUN) {
  console.log("[DRY RUN] payload listo. input:");
  console.log(JSON.stringify({ ...input, prompt: prompt.slice(0, 120) + " ...[truncado]" }, null, 2));
  console.log("[DRY RUN] NO se llamo a fal.subscribe. Sin gasto.");
  process.exit(0);
}

console.log("[2/3] Lanzando UNA generacion Seedance 2.0 image-to-video (15s, start+end, audio nativo)...");
const result = await fal.subscribe("bytedance/seedance-2.0/image-to-video", {
  input,
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
