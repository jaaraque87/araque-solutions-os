// Helper de secretos para runners Node (fal-jobs, carrusel-ana-lab).
// Detecta var faltante, la pide con entrada oculta, ofrece guardarla en un .env
// local SOLO con autorización. Nunca imprime la clave completa ni commitea .env.
// Compatible con el entorno actual: si process.env[name] existe, lo devuelve.
//
// Uso:
//   import { getSecret } from "../lib/get-secret.mjs";
//   const FAL_KEY = await getSecret("FAL_KEY");

import readline from "node:readline";
import fs from "node:fs";

const LABELS = {
  FAL_KEY: "fal.ai — Kling, Seedance, GPT Image 2",
  OPENAI_API_KEY: "OpenAI — GPT Image 2 (BYOK)",
  ELEVENLABS_API_KEY: "ElevenLabs — voz",
};

function mask(v) {
  if (!v) return "(vacío)";
  return v.length <= 8 ? v[0] + "***" : `${v.slice(0, 4)}…${v.slice(-2)}`;
}

function askHidden(query) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: true });
    rl.question(query, (ans) => { rl.close(); process.stdout.write("\n"); resolve(ans.trim()); });
    // Oculta el eco de lo que se escribe.
    rl._writeToOutput = () => rl.output.write("*");
  });
}

function ask(query) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question(query, (ans) => { rl.close(); resolve(ans.trim()); });
  });
}

export async function getSecret(name, label, { envPath = ".env", interactive = true } = {}) {
  if (process.env[name]) return process.env[name];

  label = label || LABELS[name] || name;
  console.log(`\n⚠️  Falta la variable ${name}.`);
  console.log(`   Para qué sirve: ${label}`);

  if (!interactive) throw new Error(`Falta ${name} y el modo no es interactivo. Define ${name} en el entorno o .env.`);

  const value = await askHidden(`   Pega ${name} (entrada oculta): `);
  if (!value) throw new Error(`No se ingresó ${name}.`);

  const save = (await ask("   ¿Guardar en .env local? [s/N]: ")).toLowerCase();
  if (["s", "si", "sí", "y", "yes"].includes(save)) {
    fs.appendFileSync(envPath, `\n${name}=${value}\n`, "utf8");
    console.log(`   ✅ Guardada en ${envPath} (.env está en .gitignore).`);
  }

  process.env[name] = value;
  console.log(`   Usando ${name}=${mask(value)} en esta sesión.`);
  return value;
}
