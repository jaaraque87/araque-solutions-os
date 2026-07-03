import { createRequire } from "node:module";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const puppeteer = require("C:/Users/SOPORTE2/AppData/Local/npm-cache/_npx/702923228c2ce1e6/node_modules/puppeteer-core");

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const htmlPath = path.join(__dirname, "carousel.html");
const outDir = path.resolve(__dirname, "../outputs/carousel");

await mkdir(outDir, { recursive: true });

const chromePath = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const browser = await puppeteer.launch({
  executablePath: chromePath,
  headless: "new",
  args: ["--disable-gpu", "--no-sandbox"]
});
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "networkidle0" });
await page.evaluate(() => document.fonts.ready);

const slides = await page.$$(".slide");
for (let i = 0; i < slides.length; i += 1) {
  const file = path.join(outDir, `slide-${String(i + 1).padStart(2, "0")}.jpg`);
  await slides[i].screenshot({ path: file, type: "jpeg", quality: 95 });
  console.log(file);
}

await browser.close();
