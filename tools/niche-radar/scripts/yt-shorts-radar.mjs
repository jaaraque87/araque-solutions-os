#!/usr/bin/env node
// niche-radar: recolector de datos verificables de YouTube Shorts vía yt-dlp.
// Dump público de un canal → ranking winners/losers → transcripts de winners.
// Todo gratis y reproducible. El análisis de patrones lo hace la skill hook-machine.
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const radarRoot = path.resolve(__dirname, "..");

function usage() {
  console.log(`
Usage:
  node tools/niche-radar/scripts/yt-shorts-radar.mjs --channel "@handle" [options]

Options:
  --channel <@handle|url>  Requerido. Canal de YouTube (se analiza su tab /shorts).
  --max <n>                Máx videos a listar del canal. Default: 60.
  --winners <n>            Cuántos winners detallar+transcribir. Default: 8.
  --client <slug>          Cliente de hook-lab; guarda el run en tools/hook-lab/clients/<slug>/radar/.
  --lang <codes>           Idiomas de subtítulos. Default: "es,es-419,en".
  --skip-transcripts       Solo ranking, sin bajar subtítulos.

Salida: radar.json + report.md + transcripts/*.txt en la carpeta del run.
`);
}

function parseArgs(argv) {
  const args = { max: 60, winners: 8, lang: "es,es-419,en", transcripts: true };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === "--help" || a === "-h") args.help = true;
    else if (a === "--skip-transcripts") args.transcripts = false;
    else if (a.startsWith("--")) {
      const v = argv[i + 1];
      if (!v || v.startsWith("--")) throw new Error(`Falta valor para ${a}`);
      args[a.slice(2)] = v;
      i += 1;
    } else throw new Error(`Argumento desconocido: ${a}`);
  }
  args.max = Number(args.max);
  args.winners = Number(args.winners);
  return args;
}

function findYtDlp() {
  if (process.env.YTDLP_PATH && fs.existsSync(process.env.YTDLP_PATH)) return process.env.YTDLP_PATH;
  const probe = spawnSync(process.platform === "win32" ? "where" : "which", ["yt-dlp"], { encoding: "utf8" });
  const found = (probe.stdout ?? "").split(/\r?\n/).map((l) => l.trim()).find(Boolean);
  if (found) return found;
  if (process.platform === "win32") {
    const root = path.join(process.env.LOCALAPPDATA ?? "", "Microsoft", "WinGet", "Packages");
    if (fs.existsSync(root)) {
      for (const dir of fs.readdirSync(root)) {
        if (dir.startsWith("yt-dlp")) {
          const exe = path.join(root, dir, "yt-dlp.exe");
          if (fs.existsSync(exe)) return exe;
        }
      }
    }
  }
  throw new Error("yt-dlp no encontrado. Instalar: winget install yt-dlp.yt-dlp");
}

function ytdlp(bin, args) {
  // --js-runtimes node: YouTube exige runtime JS para los tabs de canal; usamos el Node ya instalado.
  const r = spawnSync(bin, ["--js-runtimes", "node", ...args], { encoding: "utf8", maxBuffer: 1024 * 1024 * 256 });
  if (r.error) throw r.error;
  if (r.status !== 0) throw new Error(`yt-dlp falló: ${(r.stderr || "").slice(0, 500)}`);
  return r.stdout;
}

function channelUrl(input) {
  if (input.startsWith("http")) return input.replace(/\/$/, "").endsWith("/shorts") ? input : `${input.replace(/\/$/, "")}/shorts`;
  const handle = input.startsWith("@") ? input : `@${input}`;
  return `https://www.youtube.com/${handle}/shorts`;
}

function naturalGap(sorted) {
  // Busca el mayor salto relativo entre videos consecutivos en el tercio superior.
  if (sorted.length < 4) return Math.max(1, Math.floor(sorted.length / 2));
  let bestIdx = -1;
  let bestRatio = 1;
  const scan = Math.max(3, Math.floor(sorted.length / 3));
  for (let i = 1; i <= scan; i += 1) {
    const prev = sorted[i - 1].views;
    const cur = Math.max(1, sorted[i].views);
    const ratio = prev / cur;
    if (ratio > bestRatio) { bestRatio = ratio; bestIdx = i; }
  }
  if (bestIdx > 0 && bestRatio >= 1.8) return bestIdx;
  // Sin gap claro: usar promedio como línea.
  const avg = sorted.reduce((s, v) => s + v.views, 0) / sorted.length;
  const idx = sorted.findIndex((v) => v.views < avg);
  return idx === -1 ? sorted.length : idx;
}

function findWhisper() {
  if (process.env.HYPERFRAMES_WHISPER_PATH && fs.existsSync(process.env.HYPERFRAMES_WHISPER_PATH)) return process.env.HYPERFRAMES_WHISPER_PATH;
  const local = path.join(process.env.LOCALAPPDATA ?? "", "whisper-cpp", "Release", "whisper-cli.exe");
  if (fs.existsSync(local)) return local;
  return null;
}

function findHyperframesCli() {
  if (process.env.HYPERFRAMES_CLI && fs.existsSync(process.env.HYPERFRAMES_CLI)) return process.env.HYPERFRAMES_CLI;
  const local = path.resolve(radarRoot, "..", "content-reel-lab", "node_modules", "hyperframes", "dist", "cli.js");
  if (fs.existsSync(local)) return local;
  return null;
}

// Fallback cuando el canal no publica subtítulos: bajar solo el audio (peor calidad,
// suficiente para voz) y transcribir con Whisper local vía hyperframes. Costo $0.
function whisperFallback(bin, video, base, lang) {
  const hfCli = findHyperframesCli();
  const whisper = findWhisper();
  if (!hfCli || !whisper) return false;
  const mp3 = `${base}.mp3`;
  try {
    ytdlp(bin, ["-f", "worstaudio", "-x", "--audio-format", "mp3", "-o", `${base}.%(ext)s`, video.url]);
    const r = spawnSync(process.execPath, [hfCli, "transcribe", "-m", "small", "-l", lang, "--json", mp3], {
      encoding: "utf8",
      env: { ...process.env, HYPERFRAMES_WHISPER_PATH: whisper },
      cwd: path.dirname(mp3),
      maxBuffer: 1024 * 1024 * 64,
    });
    if (r.status !== 0) return false;
    const meta = JSON.parse(r.stdout.trim().split(/\r?\n/).pop());
    if (!meta.ok || !meta.transcriptPath) return false;
    const words = JSON.parse(fs.readFileSync(meta.transcriptPath, "utf8"));
    const text = (Array.isArray(words) ? words : []).map((w) => w.text ?? "").join(" ").replace(/\s+/g, " ").trim();
    if (!text) return false;
    fs.writeFileSync(`${base}.txt`, `${video.title}\n${video.url}\n[transcript: whisper local, ${meta.wordCount} palabras]\n${"=".repeat(40)}\n${text}\n`, "utf8");
    return true;
  } catch {
    return false;
  } finally {
    if (fs.existsSync(mp3)) fs.unlinkSync(mp3);
  }
}

function cleanVtt(vtt) {
  const seen = new Set();
  const lines = [];
  for (const raw of vtt.split(/\r?\n/)) {
    const line = raw
      .replace(/<[^>]+>/g, "")
      .replaceAll("&gt;", "")
      .replaceAll("&lt;", "")
      .replaceAll("&amp;", "&")
      .replaceAll("&quot;", '"')
      .replaceAll("&#39;", "'")
      .trim();
    if (!line || line === "WEBVTT" || /^\d+$/.test(line) || line.includes("-->") || line.startsWith("Kind:") || line.startsWith("Language:")) continue;
    if (!seen.has(line)) { seen.add(line); lines.push(line); }
  }
  return lines.join("\n");
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { usage(); return; }
  if (!args.channel) { usage(); throw new Error("--channel es requerido"); }

  const bin = findYtDlp();
  const url = channelUrl(args.channel);
  const stamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  const slug = (args.channel.replace(/[^a-zA-Z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "canal").toLowerCase();
  const outDir = args.client
    ? path.resolve(radarRoot, "..", "hook-lab", "clients", args.client, "radar", `${slug}-${stamp}`)
    : path.join(radarRoot, "runs", `${slug}-${stamp}`);
  fs.mkdirSync(path.join(outDir, "transcripts"), { recursive: true });

  console.log(`\n[1/4] Listando shorts de ${url} (máx ${args.max})...`);
  const flat = JSON.parse(ytdlp(bin, ["--flat-playlist", "--playlist-end", String(args.max), "-J", url]));
  const entries = (flat.entries ?? [])
    .filter((e) => e && e.id)
    .map((e) => ({
      id: e.id,
      title: e.title ?? "",
      url: `https://www.youtube.com/shorts/${e.id}`,
      views: Number(e.view_count ?? 0),
    }));
  if (entries.length === 0) throw new Error("No se listaron videos. ¿El canal tiene tab /shorts público?");

  const sorted = [...entries].sort((a, b) => b.views - a.views);
  const cut = naturalGap(sorted);
  const winners = sorted.slice(0, Math.max(cut, Math.min(args.winners, sorted.length)));
  const detailCount = Math.min(args.winners, winners.length);

  console.log(`[2/4] ${entries.length} shorts listados. Línea winner/loser en el puesto ${cut} (${sorted[cut - 1]?.views?.toLocaleString()} views).`);
  console.log(`[3/4] Detallando ${detailCount} winners (likes/comments/duración)...`);

  const detailed = [];
  for (let i = 0; i < detailCount; i += 1) {
    const v = winners[i];
    try {
      const d = JSON.parse(ytdlp(bin, ["--no-download", "-J", v.url]));
      const likes = Number(d.like_count ?? 0);
      const comments = Number(d.comment_count ?? 0);
      detailed.push({
        ...v,
        views: Number(d.view_count ?? v.views),
        likes,
        comments,
        duration_s: Number(d.duration ?? 0),
        uploaded: d.upload_date ?? "",
        engagement_pct: v.views > 0 ? Number((((likes + comments) / Math.max(1, Number(d.view_count ?? v.views))) * 100).toFixed(2)) : 0,
      });
      console.log(`  ${i + 1}/${detailCount} ✓ ${v.title.slice(0, 60)}`);
    } catch {
      detailed.push({ ...v, likes: null, comments: null, duration_s: null, uploaded: "", engagement_pct: null });
      console.log(`  ${i + 1}/${detailCount} ✗ detalle falló: ${v.title.slice(0, 60)}`);
    }
  }

  if (args.transcripts) {
    console.log(`[4/4] Bajando subtítulos de ${detailCount} winners...`);
    for (let i = 0; i < detailCount; i += 1) {
      const v = winners[i];
      const base = path.join(outDir, "transcripts", `${String(i + 1).padStart(2, "0")}-${v.id}`);
      try {
        ytdlp(bin, ["--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", args.lang, "--sub-format", "vtt", "-o", base, v.url]);
        const vtt = fs.readdirSync(path.dirname(base)).find((f) => f.startsWith(path.basename(base)) && f.endsWith(".vtt"));
        if (vtt) {
          const text = cleanVtt(fs.readFileSync(path.join(path.dirname(base), vtt), "utf8"));
          fs.writeFileSync(`${base}.txt`, `${v.title}\n${v.url}\n${"=".repeat(40)}\n${text}\n`, "utf8");
          fs.unlinkSync(path.join(path.dirname(base), vtt));
          console.log(`  ${i + 1}/${detailCount} ✓ transcript`);
        } else {
          const ok = whisperFallback(bin, v, base, args.lang.split(",")[0]);
          console.log(`  ${i + 1}/${detailCount} ${ok ? "✓ transcript (whisper local)" : "· sin subtítulos ni whisper"}`);
        }
      } catch {
        const ok = whisperFallback(bin, v, base, args.lang.split(",")[0]);
        console.log(`  ${i + 1}/${detailCount} ${ok ? "✓ transcript (whisper local)" : "✗ subtítulos y whisper fallaron"}`);
      }
    }
  } else {
    console.log(`[4/4] Transcripts omitidos.`);
  }

  const radar = {
    fuente: "youtube-shorts",
    canal: args.channel,
    url,
    fecha: new Date().toISOString().slice(0, 10),
    total_listados: entries.length,
    linea_winner_loser: { puesto: cut, views: sorted[cut - 1]?.views ?? null },
    winners_detallados: detailed,
    ranking_completo: sorted,
  };
  fs.writeFileSync(path.join(outDir, "radar.json"), JSON.stringify(radar, null, 2), "utf8");

  const fmt = (n) => (n === null || n === undefined ? "—" : Number(n).toLocaleString("es"));
  const report = [
    `# Radar — ${args.channel} (YouTube Shorts)`,
    ``,
    `Fecha: ${radar.fecha} · Videos listados: ${entries.length} · Línea winner/loser: puesto ${cut} (${fmt(sorted[cut - 1]?.views)} views)`,
    ``,
    `| # | Video | Views | Likes | Coments | Eng% | Dur(s) |`,
    `|---|---|---|---|---|---|---|`,
    ...detailed.map((v, i) => `| ${i + 1} | [${v.title.replace(/\|/g, "/").slice(0, 70)}](${v.url}) | ${fmt(v.views)} | ${fmt(v.likes)} | ${fmt(v.comments)} | ${v.engagement_pct ?? "—"} | ${fmt(v.duration_s)} |`),
    ``,
    `Transcripts en \`transcripts/\`. Siguiente paso: analizar con la skill hook-machine (extracción de hooks + patrones + fórmulas) y volcar al swipe.md del cliente.`,
  ].join("\n");
  fs.writeFileSync(path.join(outDir, "report.md"), report, "utf8");

  console.log(`\nListo: ${outDir}`);
  console.log(`  radar.json · report.md · transcripts/`);
}

try {
  main();
} catch (e) {
  console.error(`\nERROR: ${e.message}`);
  process.exit(1);
}
