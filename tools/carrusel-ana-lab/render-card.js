// Render genérico de una tarjeta 1080x1350 (#card) a JPG.
// Uso: node render-card.js <html-abs-path> <out-jpg>
const puppeteer = require('puppeteer');
const path = require('path');
(async () => {
  const html = path.resolve(process.argv[2]);
  const out = path.resolve(process.argv[3]);
  const browser = await puppeteer.launch({ headless: 'new', defaultViewport: { width: 1200, height: 1500, deviceScaleFactor: 2 } });
  const page = await browser.newPage();
  await page.goto('file:///' + html.replace(/\\/g, '/'), { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(async () => { await document.fonts.ready; });
  await new Promise((r) => setTimeout(r, 600));
  const el = await page.$('#card');
  await el.screenshot({ path: out, type: 'jpeg', quality: 95 });
  await browser.close();
  console.log('OK', out);
})();
