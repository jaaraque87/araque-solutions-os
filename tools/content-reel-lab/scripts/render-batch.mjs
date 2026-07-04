#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const labRoot = path.resolve(__dirname, "..");
const singleScript = path.join(__dirname, "render-ltx-avatar-original-audio.mjs");
const outputsRoot = path.join(labRoot, "outputs", "ltx-avatar-original-audio");

// Flags que se pasan tal cual al script unitario cuando aparecen en defaults o en el job.
const PASSTHROUGH_KEYS = [
  "hook", "cta", "handle", "name", "out", "quality", "fps",
  "brandPill", "sideWord", "hookKicker", "proof1", "proof2", "proof3",
  "authorityKicker", "authorityTitle", "authorityLine", "ctaKicker", "audioVolume",
];

function usage() {
  console.log(`
Usage:
  node tools/content-reel-lab/scripts/render-batch.mjs --jobs "briefs/batch.example.json"

Options:
  --jobs <path>        Required. JSON con { defaults, jobs: [...] }.
  --dry-run            Lista lo que haria sin renderizar nada.
  --stop-on-error      Aborta el lote al primer fallo (default: continua).

Formato del JSON de jobs:
  {
    "defaults": { "handle": "@araquesolutions", "quality": "standard" },
    "jobs": [
      { "video": "C:\\\\ruta\\\\clip1.mp4", "hook": "...", "cta": "..." },
      { "video": "C:\\\\ruta\\\\clip2.mp4", "hook": "...", "cta": "...", "name": "cliente-x-reel-2" }
    ]
  }

Cada job acepta las mismas opciones que render-ltx-avatar-original-audio.mjs.
Los hooks pueden venir de .claude/skills/hook-lab (hooks.json del cliente).

Environment:
  HYPERFRAMES_CLI                Path a hyperframes/dist/cli.js. Si no esta definido y existe
                                 el node_modules local del lab, se usa automaticamente.
  HYPERFRAMES_EXTRACT_CACHE_DIR  Default "off" en Windows (evita EPERM por symlinks).
`);
}

function parseArgs(argv) {
  const args = { dryRun: false, stopOnError: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") args.help = true;
    else if (arg === "--dry-run") args.dryRun = true;
    else if (arg === "--stop-on-error") args.stopOnError = true;
    else if (arg === "--jobs") {
      const value = argv[i + 1];
      if (!value || value.startsWith("--")) throw new Error("Missing value for --jobs");
      args.jobs = value;
      i += 1;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return args;
}

function buildEnv() {
  const env = { ...process.env };
  if (!env.HYPERFRAMES_CLI) {
    const localCli = path.join(labRoot, "node_modules", "hyperframes", "dist", "cli.js");
    if (fs.existsSync(localCli)) env.HYPERFRAMES_CLI = localCli;
  }
  if (!env.HYPERFRAMES_EXTRACT_CACHE_DIR && process.platform === "win32") {
    env.HYPERFRAMES_EXTRACT_CACHE_DIR = "off";
  }
  return env;
}

function jobArgs(job, defaults) {
  const merged = { ...defaults, ...job };
  if (!merged.video) throw new Error("Job sin campo 'video'");
  const cli = ["--video", merged.video];
  for (const key of PASSTHROUGH_KEYS) {
    if (merged[key] !== undefined && merged[key] !== null && merged[key] !== "") {
      cli.push(`--${key}`, String(merged[key]));
    }
  }
  return cli;
}

function findFinalOutput(job, defaults, startedAt) {
  const merged = { ...defaults, ...job };
  if (merged.out) return path.resolve(merged.out);
  // Sin --out el script unitario crea <slug>-<stamp>/final.mp4; se busca la carpeta mas reciente.
  if (!fs.existsSync(outputsRoot)) return null;
  const candidates = fs.readdirSync(outputsRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => path.join(outputsRoot, entry.name, "final.mp4"))
    .filter((file) => fs.existsSync(file) && fs.statSync(file).mtimeMs >= startedAt);
  candidates.sort((a, b) => fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs);
  return candidates[0] ?? null;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    usage();
    return;
  }
  if (!args.jobs) {
    usage();
    throw new Error("--jobs is required");
  }

  const jobsPath = path.resolve(args.jobs);
  if (!fs.existsSync(jobsPath)) throw new Error(`Jobs file not found: ${jobsPath}`);
  const spec = JSON.parse(fs.readFileSync(jobsPath, "utf8"));
  const defaults = spec.defaults ?? {};
  const jobs = spec.jobs ?? [];
  if (!Array.isArray(jobs) || jobs.length === 0) throw new Error("El JSON no tiene jobs");

  // Validar antes de arrancar: que todos los videos existan.
  const missing = jobs
    .map((job, index) => ({ index, video: job.video ?? defaults.video }))
    .filter(({ video }) => !video || !fs.existsSync(path.resolve(video)));
  if (missing.length > 0) {
    throw new Error(`Videos no encontrados:\n${missing.map((m) => `  job ${m.index + 1}: ${m.video ?? "(sin video)"}`).join("\n")}`);
  }

  const env = buildEnv();
  console.log(`\nBatch: ${jobs.length} job(s) desde ${jobsPath}`);
  if (env.HYPERFRAMES_CLI) console.log(`HyperFrames CLI: ${env.HYPERFRAMES_CLI}`);
  if (env.HYPERFRAMES_EXTRACT_CACHE_DIR) console.log(`Extract cache: ${env.HYPERFRAMES_EXTRACT_CACHE_DIR}`);

  const results = [];
  for (let i = 0; i < jobs.length; i += 1) {
    const job = jobs[i];
    const cli = jobArgs(job, defaults);
    console.log(`\n════════ Job ${i + 1}/${jobs.length} ════════`);
    console.log(`  ${cli.join(" ")}`);
    if (args.dryRun) {
      results.push({ job: i + 1, status: "dry-run" });
      continue;
    }
    const startedAt = Date.now();
    const result = spawnSync(process.execPath, [singleScript, ...cli], {
      stdio: "inherit",
      env,
      cwd: labRoot,
    });
    const elapsed = ((Date.now() - startedAt) / 1000).toFixed(1);
    if (result.status === 0) {
      const output = findFinalOutput(job, defaults, startedAt);
      results.push({ job: i + 1, status: "ok", seconds: Number(elapsed), output });
      console.log(`  ✔ Job ${i + 1} OK en ${elapsed}s`);
    } else {
      results.push({ job: i + 1, status: "failed", seconds: Number(elapsed) });
      console.error(`  ✘ Job ${i + 1} FALLÓ en ${elapsed}s`);
      if (args.stopOnError) break;
    }
  }

  const ok = results.filter((r) => r.status === "ok").length;
  const failed = results.filter((r) => r.status === "failed").length;
  const report = {
    jobsFile: jobsPath,
    finishedAt: new Date().toISOString(),
    total: jobs.length,
    ok,
    failed,
    results,
  };
  fs.mkdirSync(outputsRoot, { recursive: true });
  const reportPath = path.join(outputsRoot, `batch-report-${new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19)}.json`);
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), "utf8");

  console.log(`\n════════ RESUMEN ════════`);
  for (const r of results) {
    const line = r.status === "ok" ? `✔ job ${r.job} → ${r.output ?? "(output no localizado)"}` : `${r.status === "failed" ? "✘" : "·"} job ${r.job} (${r.status})`;
    console.log(`  ${line}`);
  }
  console.log(`\n${ok}/${jobs.length} OK · reporte: ${reportPath}`);
  if (failed > 0) process.exitCode = 1;
}

try {
  main();
} catch (error) {
  console.error(`\nERROR: ${error.message}`);
  process.exit(1);
}
