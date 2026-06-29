// Genera las fotos del carrusel vía FAL (automático) leyendo manifest.json
// Uso:  FAL_KEY en .env o variable de entorno →  node generar-fotos.mjs [carpeta-carrusel] [--model=gpt-image-2|nano-banana-2|seedream-v4] [--only=01-cover,03-x] [--force]
// Por cada foto del manifest: genera (t2i, o edit con tu producto como referencia), descarga
// al archivo_destino y registra prompt/seed en el manifest (trazabilidad).

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const QUEUE = "https://queue.fal.run";
const UPLOAD = "https://fal.run/fal-ai/file-storage/upload";

const MODELS = {
  "gpt-image-2": { t2i: "openai/gpt-image-2", edit: "openai/gpt-image-2/edit", payload: (p) => ({ prompt: p, image_size: { width: 1664, height: 2080 }, quality: "high", output_format: "jpeg", num_images: 1 }) },
  "nano-banana-2": { t2i: "fal-ai/nano-banana-2", edit: "fal-ai/nano-banana-2/edit", payload: (p) => ({ prompt: p, aspect_ratio: "4:5", resolution: "2K", output_format: "jpeg", num_images: 1, safety_tolerance: "5" }) },
  "seedream-v4": { t2i: "fal-ai/bytedance/seedream/v4/text-to-image", edit: "fal-ai/bytedance/seedream/v4/edit", payload: (p) => ({ prompt: p, image_size: { width: 1664, height: 2080 }, num_images: 1, enable_safety_checker: false }) },
};

function falKey() {
  if (process.env.FAL_KEY) return process.env.FAL_KEY;
  for (const envPath of [path.join(__dirname, ".env"), path.join(__dirname, "..", ".env")]) {
    if (fs.existsSync(envPath)) {
      const m = fs.readFileSync(envPath, "utf8").match(/^FAL_KEY=(.+)$/m);
      if (m) return m[1].trim();
    }
  }
  console.error("Falta FAL_KEY (en .env o variable de entorno). Conseguila en fal.ai");
  process.exit(1);
}

const H = () => ({ Authorization: `Key ${falKey()}`, "Content-Type": "application/json" });

async function subirReferencia(abs) {
  const data = fs.readFileSync(abs);
  const mime = abs.toLowerCase().endsWith(".png") ? "image/png" : "image/jpeg";
  const form = new FormData();
  form.append("file", new Blob([data], { type: mime }), path.basename(abs));
  const r = await fetch(UPLOAD, { method: "POST", headers: { Authorization: `Key ${falKey()}` }, body: form });
  if (!r.ok) return `data:${mime};base64,${data.toString("base64")}`;
  const j = await r.json();
  return j.url ?? j.file_url;
}

async function generar(modelKey, prompt, refs) {
  const m = MODELS[modelKey];
  const endpoint = refs?.length ? m.edit : m.t2i;
  const payload = m.payload(prompt);
  if (refs?.length) payload.image_urls = refs;
  const sub = await fetch(`${QUEUE}/${endpoint}`, { method: "POST", headers: H(), body: JSON.stringify(payload) });
  if (!sub.ok) throw new Error(`FAL ${sub.status}: ${(await sub.text()).slice(0, 300)}`);
  const { request_id } = await sub.json();
  const base = endpoint.split("/").slice(0, 2).join("/");
  for (let i = 0; i < 120; i++) {
    await new Promise((r) => setTimeout(r, 3000));
    const st = await (await fetch(`${QUEUE}/${base}/requests/${request_id}/status`, { headers: H() })).json();
    if (st.status === "COMPLETED") {
      const res = await (await fetch(`${QUEUE}/${base}/requests/${request_id}`, { headers: H() })).json();
      if (!res.images?.[0]?.url) throw new Error("sin imagen en la respuesta");
      return { url: res.images[0].url, seed: res.seed ?? null };
    }
    if (st.status === "FAILED") throw new Error(`FAL FAILED: ${JSON.stringify(st.error ?? st).slice(0, 300)}`);
  }
  throw new Error("timeout 6min");
}

// ===== main =====
const args = process.argv.slice(2);
const dir = path.resolve(args.find((a) => !a.startsWith("--")) ?? path.join(__dirname, "brands", "mi-marca", "carruseles", "001-ejemplo"));
const model = (args.find((a) => a.startsWith("--model="))?.split("=")[1]) ?? "gpt-image-2";
const only = args.find((a) => a.startsWith("--only="))?.split("=")[1]?.split(",") ?? null;
const force = args.includes("--force");

if (!MODELS[model]) { console.error(`Modelo desconocido: ${model}. Opciones: ${Object.keys(MODELS).join(", ")}`); process.exit(1); }
const manifestPath = path.join(dir, "manifest.json");
if (!fs.existsSync(manifestPath)) { console.error("No encontré manifest.json en:", dir); process.exit(1); }
const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));

console.log(`Generando fotos con ${model} → ${dir}\n`);
const refCache = new Map();
for (const foto of manifest.fotos ?? []) {
  if (only && !only.includes(foto.slide)) continue;
  const dest = path.resolve(dir, foto.archivo_destino);
  if (fs.existsSync(dest) && !force) { console.log(`  [skip] ${foto.slide} (ya existe — usá --force para pisar)`); continue; }
  try {
    let refs = null;
    if (foto.endpoint === "edit" && foto.reference) {
      const refAbs = path.resolve(dir, foto.reference);
      if (!refCache.has(refAbs)) refCache.set(refAbs, await subirReferencia(refAbs));
      refs = [refCache.get(refAbs)];
    }
    process.stdout.write(`  [...] ${foto.slide} `);
    const { url, seed } = await generar(model, foto.prompt_base, refs);
    const img = Buffer.from(await (await fetch(url)).arrayBuffer());
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.writeFileSync(dest, img);
    foto.prompt_final = foto.prompt_base;
    foto.seed = seed;
    foto.modelo_usado = model;
    foto.generated_at = new Date().toISOString();
    fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), "utf8");
    console.log(`✓ (seed ${seed ?? "n/a"})`);
  } catch (e) {
    console.log(`✗ ${e.message}`);
  }
}
console.log("\nListo. Ahora: node generar.js " + (args[0] ?? "") + "  → renderiza los JPGs finales");
