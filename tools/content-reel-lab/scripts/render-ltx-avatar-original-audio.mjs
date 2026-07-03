#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const labRoot = path.resolve(__dirname, "..");
const templateDir = path.join(labRoot, "templates", "ltx-avatar-original-audio");
const outputsRoot = path.join(labRoot, "outputs", "ltx-avatar-original-audio");

const defaults = {
  brandPill: "LTX 2.3 UGC",
  sideWord: "VENTA",
  hookKicker: "Prueba avatar",
  hookTitle: "Rostro real. Audio real. Venta real.",
  proof1: "Avatar LTX",
  proof2: "Audio original",
  proof3: "Overlay de marca",
  authorityKicker: "Araque Solutions",
  authorityTitle: "UGC con IA que parece nativo.",
  authorityLine: "La estrategia encima. La credibilidad en la voz y el gesto.",
  ctaKicker: "Sistema de contenido",
  ctaTitle: "Vender mas, vendas lo que vendas.",
  handle: "@araquesolutions",
  audioVolume: "1",
};

function usage() {
  console.log(`
Usage:
  node tools/content-reel-lab/scripts/render-ltx-avatar-original-audio.mjs --video "C:\\ruta\\avatar.mp4"

Options:
  --video <path>       Required. LTX/Comfy MP4 with the original synced audio.
  --out <path>         Optional final MP4 path. Defaults to the generated output folder.
  --name <slug>        Optional output folder name.
  --skip-render        Build, normalize, lint, validate and inspect, but do not render MP4.
  --skip-inspect       Skip HyperFrames visual inspection.
  --quality <value>    HyperFrames quality: draft, standard, high. Default: standard.
  --fps <value>        Render FPS. Default: 30.
  --hook <text>        Main hook overlay.
  --cta <text>         Final CTA overlay.
  --handle <text>      Handle shown under the CTA.

Environment:
  HYPERFRAMES_CLI              Optional path to hyperframes/dist/cli.js.
  HYPERFRAMES_FFMPEG_PATH      Optional path to ffmpeg.
  HYPERFRAMES_FFPROBE_PATH     Optional path to ffprobe.
`);
}

function parseArgs(argv) {
  const args = { quality: "standard", fps: "30", render: true, inspect: true };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") args.help = true;
    else if (arg === "--skip-render") args.render = false;
    else if (arg === "--skip-inspect") args.inspect = false;
    else if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const value = argv[i + 1];
      if (!value || value.startsWith("--")) throw new Error(`Missing value for ${arg}`);
      args[key] = value;
      i += 1;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return args;
}

function run(command, args, options = {}) {
  const result = spawnSync(command, args, {
    stdio: options.capture ? ["ignore", "pipe", "pipe"] : "inherit",
    encoding: "utf8",
    shell: false,
    cwd: options.cwd ?? process.cwd(),
    env: options.env ?? process.env,
  });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    const detail = options.capture ? `${result.stderr || result.stdout || ""}`.trim() : "";
    throw new Error(`${command} ${args.join(" ")} failed${detail ? `\n${detail}` : ""}`);
  }
  return result.stdout ?? "";
}

function commandName(name) {
  return process.platform === "win32" ? `${name}.cmd` : name;
}

function verifyCommand(command, args, label) {
  try {
    run(command, args, { capture: true });
  } catch (error) {
    throw new Error(`${label} not found or not working. Install it and make sure it is on PATH.\n${error.message}`);
  }
}

function ffmpegPathFromEnvOrCommand(name) {
  const envName = name === "ffmpeg" ? "HYPERFRAMES_FFMPEG_PATH" : "HYPERFRAMES_FFPROBE_PATH";
  const configured = process.env[envName];
  if (configured) return configured;
  return name;
}

function resolveExecutable(command) {
  if (path.isAbsolute(command) || command.includes("/") || command.includes("\\")) {
    return path.resolve(command);
  }
  const candidates = process.platform === "win32" ? [command, `${command}.exe`, `${command}.cmd`] : [command];
  for (const dir of (process.env.PATH ?? "").split(path.delimiter)) {
    if (!dir) continue;
    for (const candidate of candidates) {
      const fullPath = path.join(dir, candidate);
      if (fs.existsSync(fullPath)) return fullPath;
    }
  }
  const finder = process.platform === "win32" ? "where" : "which";
  try {
    const stdout = run(finder, [command], { capture: true });
    const first = stdout.split(/\r?\n/).map((line) => line.trim()).find(Boolean);
    if (first) return first;
  } catch {
    // Fall through to the Windows package search below.
  }
  if (process.platform === "win32" && (command === "ffmpeg" || command === "ffprobe")) {
    const wingetRoot = path.join(process.env.LOCALAPPDATA ?? "", "Microsoft", "WinGet", "Packages");
    const found = findFileByName(wingetRoot, `${command}.exe`, 4);
    if (found) return found;
  }
  throw new Error(`Could not resolve executable path for ${command}`);
}

function findFileByName(root, fileName, maxDepth) {
  if (!root || maxDepth < 0 || !fs.existsSync(root)) return null;
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    const fullPath = path.join(root, entry.name);
    if (entry.isFile() && entry.name.toLowerCase() === fileName.toLowerCase()) return fullPath;
    if (entry.isDirectory()) {
      const found = findFileByName(fullPath, fileName, maxDepth - 1);
      if (found) return found;
    }
  }
  return null;
}

function readDuration(ffprobe, videoPath) {
  const stdout = run(ffprobe, [
    "-v",
    "error",
    "-show_entries",
    "format=duration",
    "-of",
    "default=noprint_wrappers=1:nokey=1",
    videoPath,
  ], { capture: true });
  const duration = Number(stdout.trim());
  if (!Number.isFinite(duration) || duration <= 0) {
    throw new Error(`Could not read video duration from ${videoPath}`);
  }
  return Number(duration.toFixed(2));
}

function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const from = path.join(src, entry.name);
    const to = path.join(dst, entry.name);
    if (entry.isDirectory()) copyDir(from, to);
    else fs.copyFileSync(from, to);
  }
}

function slugify(value) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 54) || "ltx-avatar";
}

function stamp() {
  return new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function seconds(value) {
  return Number(value).toFixed(2).replace(/\.00$/, "");
}

function buildTiming(duration) {
  const beat1Start = 0.35;
  const beat1End = Math.min(duration * 0.25, 4.6);
  const beat2Start = Math.max(beat1End + 0.45, duration * 0.27);
  const beat2End = Math.max(beat2Start + 2.4, duration * 0.53);
  const beat3Start = Math.max(beat2End + 0.45, duration * 0.55);
  const beat3End = Math.max(beat3Start + 2.6, duration * 0.79);
  const beat4Start = Math.max(beat3End + 0.3, duration * 0.8);
  return {
    duration: seconds(duration),
    beat1Start: seconds(beat1Start),
    beat1Duration: seconds(Math.max(1, beat1End - beat1Start)),
    beat2Start: seconds(Math.min(beat2Start, duration - 2)),
    beat2Duration: seconds(Math.max(1, Math.min(beat2End, duration - 1.2) - Math.min(beat2Start, duration - 2))),
    beat3Start: seconds(Math.min(beat3Start, duration - 1.8)),
    beat3Duration: seconds(Math.max(1, Math.min(beat3End, duration - 0.8) - Math.min(beat3Start, duration - 1.8))),
    beat4Start: seconds(Math.min(beat4Start, duration - 1.1)),
    beat4Duration: seconds(Math.max(0.8, duration - Math.min(beat4Start, duration - 1.1))),
    beat1In: seconds(beat1Start + 0.15),
    beat1Out: seconds(Math.max(beat1Start + 0.7, beat1End - 0.35)),
    beat2In: seconds(Math.min(beat2Start + 0.1, duration - 1.4)),
    beat2Out: seconds(Math.max(beat2Start + 0.8, Math.min(beat2End - 0.55, duration - 1.0))),
    beat3In: seconds(Math.min(beat3Start + 0.15, duration - 1.2)),
    beat3Out: seconds(Math.max(beat3Start + 0.8, Math.min(beat3End - 0.35, duration - 0.6))),
    beat4In: seconds(Math.min(beat4Start + 0.12, duration - 0.7)),
  };
}

function renderTemplate(vars, workDir) {
  let html = fs.readFileSync(path.join(templateDir, "index.template.html"), "utf8");
  for (const [key, value] of Object.entries(vars)) {
    html = html.replaceAll(`{{${key}}}`, value);
  }
  fs.writeFileSync(path.join(workDir, "index.html"), html, "utf8");
  fs.copyFileSync(path.join(templateDir, "hyperframes.json"), path.join(workDir, "hyperframes.json"));
}

function hyperframesCommand() {
  if (process.env.HYPERFRAMES_CLI) {
    return {
      command: process.execPath,
      prefix: [process.env.HYPERFRAMES_CLI],
    };
  }
  return {
    command: commandName("npx"),
    prefix: ["hyperframes"],
  };
}

function runHyperframes(args, cwd, env) {
  const hf = hyperframesCommand();
  run(hf.command, [...hf.prefix, ...args], { cwd, env });
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    usage();
    return;
  }
  if (!args.video) {
    usage();
    throw new Error("--video is required");
  }

  const inputVideo = path.resolve(args.video);
  if (!fs.existsSync(inputVideo)) throw new Error(`Video not found: ${inputVideo}`);
  if (!fs.existsSync(templateDir)) throw new Error(`Template not found: ${templateDir}`);

  const major = Number(process.versions.node.split(".")[0]);
  if (major < 22) {
    throw new Error(`Node.js 22+ is required. Current version: ${process.version}`);
  }

  const ffmpeg = resolveExecutable(ffmpegPathFromEnvOrCommand("ffmpeg"));
  const ffprobe = resolveExecutable(ffmpegPathFromEnvOrCommand("ffprobe"));
  verifyCommand(ffmpeg, ["-version"], "FFmpeg");
  verifyCommand(ffprobe, ["-version"], "FFprobe");

  if (!process.env.HYPERFRAMES_CLI) {
    verifyCommand(commandName("npx"), ["hyperframes", "--version"], "npx hyperframes");
  }

  const duration = readDuration(ffprobe, inputVideo);
  const name = slugify(args.name ?? path.basename(inputVideo, path.extname(inputVideo)));
  const workDir = path.join(outputsRoot, `${name}-${stamp()}`);
  const assetsDir = path.join(workDir, "assets");
  fs.mkdirSync(assetsDir, { recursive: true });
  copyDir(path.join(templateDir, "assets"), assetsDir);

  const normalizedVideo = path.join(assetsDir, "ltx-avatar-hf-normalized.mp4");
  console.log(`\n[1/5] Normalizing LTX video for HyperFrames seek safety...`);
  run(ffmpeg, [
    "-y",
    "-i",
    inputVideo,
    "-c:v",
    "libx264",
    "-r",
    "30",
    "-g",
    "30",
    "-keyint_min",
    "30",
    "-pix_fmt",
    "yuv420p",
    "-movflags",
    "+faststart",
    "-c:a",
    "copy",
    normalizedVideo,
  ]);

  const textVars = {
    brandPill: args.brandPill ?? defaults.brandPill,
    sideWord: args.sideWord ?? defaults.sideWord,
    hookKicker: args.hookKicker ?? defaults.hookKicker,
    hookTitle: args.hook ?? args.hookTitle ?? defaults.hookTitle,
    proof1: args.proof1 ?? defaults.proof1,
    proof2: args.proof2 ?? defaults.proof2,
    proof3: args.proof3 ?? defaults.proof3,
    authorityKicker: args.authorityKicker ?? defaults.authorityKicker,
    authorityTitle: args.authorityTitle ?? defaults.authorityTitle,
    authorityLine: args.authorityLine ?? defaults.authorityLine,
    ctaKicker: args.ctaKicker ?? defaults.ctaKicker,
    ctaTitle: args.cta ?? args.ctaTitle ?? defaults.ctaTitle,
    handle: args.handle ?? defaults.handle,
    audioVolume: args.audioVolume ?? defaults.audioVolume,
  };

  const vars = {
    ...Object.fromEntries(Object.entries(textVars).map(([key, value]) => [key, escapeHtml(value)])),
    ...buildTiming(duration),
  };

  renderTemplate(vars, workDir);

  const env = {
    ...process.env,
    HYPERFRAMES_FFMPEG_PATH: ffmpeg,
    HYPERFRAMES_FFPROBE_PATH: ffprobe,
  };

  console.log(`\n[2/5] HyperFrames lint...`);
  runHyperframes(["lint", "."], workDir, env);

  console.log(`\n[3/5] HyperFrames validate...`);
  runHyperframes(["validate", "."], workDir, env);

  if (args.inspect) {
    console.log(`\n[4/5] HyperFrames inspect...`);
    runHyperframes(["inspect", ".", "--samples", "12"], workDir, env);
  } else {
    console.log(`\n[4/5] Skipping inspect.`);
  }

  const outputPath = args.out
    ? path.resolve(args.out)
    : path.join(workDir, "final.mp4");

  if (args.render) {
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    console.log(`\n[5/5] Rendering final MP4...`);
    runHyperframes(["render", ".", "--output", outputPath, "--quality", args.quality, "--fps", args.fps], workDir, env);
    console.log(`\nDone: ${outputPath}`);
  } else {
    console.log(`\n[5/5] Skipping render.`);
    console.log(`Project ready: ${workDir}`);
  }
}

try {
  main();
} catch (error) {
  console.error(`\nERROR: ${error.message}`);
  process.exit(1);
}
