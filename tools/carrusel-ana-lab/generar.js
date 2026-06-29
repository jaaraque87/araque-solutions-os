// Renderer genérico de carruseles IG — Ana Lab
// Uso: node generar.js <path-carpeta-carrusel>
// La carpeta debe tener inputs.json (que referencia brand.json de la marca).
// Genera: preview.html + output/*.jpg (1080x1350) + append a runs.jsonl
// Reglas del sistema: ver SISTEMA.md

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const TEMPLATE_VERSION = '2.1';

const DEFAULT_CARRUSEL = path.resolve(
  __dirname,
  'brands', 'mi-marca', 'carruseles', '001-ejemplo'
);

const ITEM_DEFAULTS = {
  anchor: 'mid-left',
  anchorTop: '50%',
  maxWidth: '60%',
  gradientStrength: 0.65,
  sizes: { it: 24, bold: 44, number: 88, caption: 18, body: 15, bodyMaxWidth: '90%' },
};

const STATEMENT_DEFAULTS = {
  anchor: 'mid-left',
  anchorTop: '50%',
  maxWidth: '78%',
  gradientStrength: 0.60,
  sizes: { it: 30, bold: 54, caption: 21 },
};

const FULLPHOTO_DEFAULTS = {
  anchor: 'bottom-left',
  maxWidth: '85%',
  gradientStrength: 0.55,
  sizes: { caption: 24 },
};

const GRANO_SVG = "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 220 220' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.92' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.65'/%3E%3C/svg%3E\")";

function fileUrl(absPath) {
  return 'file:///' + absPath.replace(/\\/g, '/');
}

function esc(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function gradientFor(slide) {
  switch (slide.type) {
    case 'hook':
      return 'linear-gradient(180deg, rgba(0,0,0,0.60) 0%, rgba(0,0,0,0) 42%, rgba(0,0,0,0) 65%, rgba(0,0,0,0.50) 100%)';
    case 'closer':
      return 'linear-gradient(180deg, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0) 50%, rgba(0,0,0,0) 70%, rgba(0,0,0,0.45) 100%)';
    case 'item':
    case 'statement':
    case 'fullphoto': {
      const defaults =
        slide.type === 'item' ? ITEM_DEFAULTS : slide.type === 'statement' ? STATEMENT_DEFAULTS : FULLPHOTO_DEFAULTS;
      const s = slide.gradientStrength ?? defaults.gradientStrength;
      const anchor = slide.anchor ?? defaults.anchor;
      if (anchor === 'bottom-left') {
        return `linear-gradient(360deg, rgba(0,0,0,${s}) 0%, rgba(0,0,0,0) 60%)`;
      }
      return `linear-gradient(90deg, rgba(0,0,0,${s}) 0%, rgba(0,0,0,0) 60%)`;
    }
    default:
      return null;
  }
}

function overlayCssFor(slide, n) {
  if (slide.type === 'item' || slide.type === 'statement' || slide.type === 'fullphoto') {
    const defaults =
      slide.type === 'item' ? ITEM_DEFAULTS : slide.type === 'statement' ? STATEMENT_DEFAULTS : FULLPHOTO_DEFAULTS;
    const mw = slide.maxWidth ?? defaults.maxWidth;
    const anchor = slide.anchor ?? defaults.anchor;
    if (anchor === 'bottom-left') {
      return `.s${n} .overlay { bottom: 70px; left: 0; max-width: ${mw}; }`;
    }
    const top = slide.anchorTop ?? defaults.anchorTop ?? '50%';
    return `.s${n} .overlay { top: ${top}; left: 0; transform: translateY(-50%); max-width: ${mw}; }`;
  }
  return '';
}

function slideCss(slide, n) {
  const rules = [];
  if (slide.photoUrl) {
    rules.push(`.s${n} { background-image: url('${slide.photoUrl}'); }`);
  }
  const grad = gradientFor(slide);
  if (grad) {
    rules.push(`.s${n}::before { background: ${grad}; }`);
  } else {
    rules.push(`.s${n}::before { display: none; }`);
  }
  rules.push(overlayCssFor(slide, n));

  if ((slide.type === 'hook' || slide.type === 'promise') && slide.heroSize) {
    const sel = slide.type === 'hook' ? '.hero' : '.hero-promise';
    rules.push(`.s${n} ${sel} { font-size: ${slide.heroSize}px; }`);
  }

  if (slide.type === 'item') {
    const sz = { ...ITEM_DEFAULTS.sizes, ...(slide.sizes || {}) };
    rules.push(
      `.s${n} .it { font-size: ${sz.it}px; line-height: 1; }`,
      `.s${n} .bold { font-size: ${sz.bold}px; line-height: 0.94; }`,
      `.s${n} .number { font-size: ${sz.number}px; }`,
      `.s${n} .caption { font-size: ${sz.caption}px; margin-top: 8px; }`,
      `.s${n} .body { font-size: ${sz.body}px; max-width: ${sz.bodyMaxWidth}; }`
    );
  }

  if (slide.type === 'statement') {
    const sz = { ...STATEMENT_DEFAULTS.sizes, ...(slide.sizes || {}) };
    rules.push(
      `.s${n} .it { font-size: ${sz.it}px; line-height: 1.02; }`,
      `.s${n} .bold { font-size: ${sz.bold}px; line-height: 0.94; }`,
      `.s${n} .caption { font-size: ${sz.caption}px; margin-top: 14px; }`
    );
  }

  if (slide.type === 'fullphoto') {
    const sz = { ...FULLPHOTO_DEFAULTS.sizes, ...(slide.sizes || {}) };
    rules.push(`.s${n} .caption { font-size: ${sz.caption}px; margin-top: 0; line-height: 1.25; }`);
  }
  return rules.filter(Boolean).join('\n  ');
}

function footerHtml(brand, opts = {}) {
  const compliance = opts.compliance
    ? `<div class="compliance">${esc(opts.compliance)}</div>`
    : '';
  return `<div class="footer">
    <img src="${brand.logoUrl}" alt="${esc(brand.name)}">
    <div class="handle">${esc(brand.handle)}</div>
    ${compliance}
  </div>`;
}

function slideHtml(slide, n, brand) {
  const cls = `slide s${n} ${slide.type === 'hook' ? 'hook' : slide.type === 'promise' ? 'promise' : slide.type === 'closer' ? 'closer' : 'item'}`;

  if (slide.type === 'hook') {
    return `<div class="${cls}">
  <div class="overlay">
    <div class="eyebrow">${esc(slide.eyebrow ?? brand.eyebrow)}</div>
    <span class="hero">${esc(slide.hero)}</span>
    <span class="sub">${esc(slide.sub)}</span>
    ${slide.micro ? `<span class="micro">${esc(slide.micro)}</span>` : ''}
  </div>
  ${slide.captionBottom ? `<div class="caption-bottom">${esc(slide.captionBottom)}</div>` : ''}
  ${footerHtml(brand)}
</div>`;
  }

  if (slide.type === 'promise') {
    return `<div class="${cls}">
  <div class="overlay">
    <div class="eyebrow">${esc(slide.eyebrow ?? brand.eyebrow)}</div>
    <span class="hero-promise">${esc(slide.hero)}</span>
    <span class="sub-promise">${esc(slide.sub)}</span>
    <hr class="rule">
    <span class="caption">${esc(slide.caption)}</span>
  </div>
  ${footerHtml(brand)}
</div>`;
  }

  if (slide.type === 'item') {
    return `<div class="${cls}">
  <div class="overlay">
    ${slide.number ? `<div class="number">${esc(slide.number)}</div>` : ''}
    <div>
      <span class="it">${esc(slide.titleIt)}</span>
      <span class="bold">${esc(slide.titleBold)}</span>
    </div>
    <div class="caption">${esc(slide.caption)}</div>
    ${slide.body ? `<div class="body">${esc(slide.body)}</div>` : ''}
  </div>
  ${footerHtml(brand)}
</div>`;
  }

  if (slide.type === 'statement') {
    const lines = (slide.lines || [])
      .map((l) => `<span class="${l.style === 'bold' ? 'bold' : 'it'}">${esc(l.text)}</span>`)
      .join('\n      ');
    return `<div class="${cls}">
  <div class="overlay">
    ${slide.eyebrow ? `<div class="eyebrow">${esc(slide.eyebrow)}</div>` : ''}
    <div>
      ${lines}
    </div>
    ${slide.caption ? `<div class="caption">${esc(slide.caption)}</div>` : ''}
  </div>
  ${footerHtml(brand)}
</div>`;
  }

  if (slide.type === 'fullphoto') {
    const captionHtml = esc(slide.caption).split('\n').join('<br>');
    return `<div class="${cls}">
  <div class="overlay">
    <div class="caption">${captionHtml}</div>
  </div>
  ${footerHtml(brand)}
</div>`;
  }

  if (slide.type === 'closer') {
    return `<div class="${cls}">
  <div class="overlay">
    <div class="eyebrow">${esc(slide.eyebrow ?? brand.eyebrow)}</div>
    <div>
      <span class="it">${esc(slide.titleIt)}</span>
      <span class="bold">${esc(slide.titleBold)}</span>
      ${slide.titleIt2 ? `<span class="it">${esc(slide.titleIt2)}</span>` : ''}
    </div>
    <div class="caption">${esc(slide.caption)}</div>
  </div>
  ${footerHtml(brand, { compliance: brand.complianceText })}
</div>`;
  }

  if (slide.type === 'matches') {
    const rows = (slide.matchesResolved || []).map((m) => `
    <div class="match-row${m.hl ? ' hl' : ''}">
      <img class="flag" src="${m.aUrl}" alt="${esc(m.aName)}">
      <span class="team">${esc(m.aName)}</span>
      <span class="vs">vs</span>
      <span class="team">${esc(m.bName)}</span>
      <img class="flag" src="${m.bUrl}" alt="${esc(m.bName)}">
    </div>`).join('');
    return `<div class="${cls}" style="background: var(--primary);">
  <div class="overlay matches-overlay">
    <div class="eyebrow">${esc(slide.eyebrow)}</div>
    <div class="matches-title">${esc(slide.title)}</div>
    <div class="matches-list">${rows}</div>
    ${slide.caption ? `<div class="caption matches-caption">${esc(slide.caption)}</div>` : ''}
  </div>
  ${footerHtml(brand)}
</div>`;
  }

  throw new Error(`Tipo de slide desconocido: ${slide.type}`);
}

function buildHtml(inputs, brand) {
  const fontSpecs = [brand.fonts.personality.googleFontsSpec, brand.fonts.display.googleFontsSpec]
    .map((s) => 'family=' + s)
    .join('&');

  const perSlideCss = inputs.slides.map((sl, i) => slideCss(sl, i + 1)).join('\n  ');
  const slidesHtml = inputs.slides.map((sl, i) => slideHtml(sl, i + 1, brand)).join('\n\n');

  return `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>${esc(brand.name)} — ${esc(inputs.title)} (generado, no editar a mano)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?${fontSpecs}&display=swap" rel="stylesheet">
<style>
  :root {
    --primary: ${brand.palette.primary};
    --bg: ${brand.palette.background};
    --accent: ${brand.palette.accent};
    --hero: ${brand.palette.heroColor || brand.palette.background};
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #181410;
    padding: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 32px;
    font-family: '${brand.fonts.display.family}', sans-serif;
  }
  .label {
    color: #888;
    font-size: 13px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: -8px;
    margin-top: 16px;
  }
  .label .accent { color: var(--accent); }

  .slide {
    width: 540px;
    height: 675px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    background-size: cover;
    background-position: center;
    color: var(--bg);
  }
  .slide::before {
    content: '';
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
  }

  /* promise: fondo primary pleno + grano de film */
  .slide.promise { background: var(--primary); }
  .slide.promise::after {
    content: '';
    position: absolute;
    inset: 0;
    z-index: 0;
    background-image: ${GRANO_SVG};
    mix-blend-mode: overlay;
    opacity: 0.30;
    pointer-events: none;
  }

  .overlay {
    position: absolute;
    z-index: 2;
    padding: 36px 40px;
  }
  .eyebrow {
    font-family: '${brand.fonts.personality.family}', serif;
    font-style: italic;
    font-weight: 500;
    font-size: 18px;
    letter-spacing: 0.04em;
    opacity: 1;
    text-shadow: 0 1px 5px rgba(0,0,0,0.6);
  }
  .it {
    font-family: '${brand.fonts.personality.family}', serif;
    font-style: italic;
    font-weight: 500;
    text-transform: none;
    letter-spacing: 0;
    display: block;
    text-shadow: 0 1px 6px rgba(0,0,0,0.5);
  }
  .bold {
    font-family: '${brand.fonts.display.family}', sans-serif;
    font-weight: ${brand.fonts.display.weight};
    text-transform: uppercase;
    letter-spacing: -0.02em;
    display: block;
    color: var(--hero);
    text-shadow: 0 2px 12px rgba(0,0,0,0.6);
  }
  .number {
    font-family: '${brand.fonts.display.family}', sans-serif;
    font-weight: ${brand.fonts.display.weight};
    line-height: 0.82;
    color: var(--accent);
    letter-spacing: -0.05em;
    margin-bottom: 8px;
    text-shadow: 0 2px 14px rgba(0,0,0,0.55);
  }
  .caption {
    font-family: '${brand.fonts.personality.family}', serif;
    font-style: italic;
    font-weight: 500;
    font-size: 22px;
    line-height: 1.2;
    opacity: 0.95;
    margin-top: 12px;
    text-shadow: 0 1px 6px rgba(0,0,0,0.55);
  }
  .body {
    font-family: '${brand.fonts.display.family}', sans-serif;
    font-weight: 400;
    line-height: 1.42;
    margin-top: 14px;
    opacity: 0.96;
    text-shadow: 0 1px 6px rgba(0,0,0,0.6);
  }

  .footer {
    position: absolute;
    bottom: 20px;
    left: 0;
    right: 0;
    z-index: 3;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }
  .footer img {
    height: 38px;
    width: auto;
    opacity: 0.95;
    filter: drop-shadow(0 1px 6px rgba(0,0,0,0.55));
  }
  .footer .handle {
    font-family: '${brand.fonts.display.family}', sans-serif;
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    opacity: 0.78;
    text-shadow: 0 1px 4px rgba(0,0,0,0.6);
  }
  .footer .compliance {
    font-family: '${brand.fonts.display.family}', sans-serif;
    font-weight: 500;
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.68;
    margin-top: 6px;
    text-shadow: 0 1px 4px rgba(0,0,0,0.6);
  }

  /* ===== HOOK ===== */
  .slide.hook .overlay { top: 32px; left: 0; max-width: 100%; padding: 0 36px; }
  .slide.hook .eyebrow { margin-bottom: 4px; }

  /* ===== CLOSER ===== */
  .slide.closer .overlay { top: 0; left: 0; right: 0; text-align: center; padding-top: 46px; }
  .slide.closer .eyebrow { margin-bottom: 16px; font-size: 22px; }
  .slide.closer .it { font-size: 42px; line-height: 1; }
  .slide.closer .bold { font-size: 88px; line-height: 0.92; letter-spacing: -0.04em; }
  .slide.closer .caption { font-size: 32px; margin-top: 20px; }
  .slide.closer .footer { bottom: 32px; }
  .slide.closer .footer img { height: 64px; }
  .slide.closer .footer .handle { font-size: 13px; margin-top: 4px; }

  /* ===== PROMISE ===== */
  .slide.promise .overlay {
    top: 50%;
    left: 0;
    right: 0;
    transform: translateY(-50%);
    text-align: center;
    padding: 0 36px;
    z-index: 2;
  }
  .slide.promise .eyebrow {
    display: block;
    margin-bottom: 14px;
    font-size: 16px;
    opacity: 0.78;
    text-shadow: none;
  }
  .slide.promise .hero-promise {
    font-family: '${brand.fonts.display.family}', sans-serif;
    font-weight: ${brand.fonts.display.weight};
    font-size: 170px;
    line-height: 0.85;
    letter-spacing: -0.06em;
    text-transform: uppercase;
    display: block;
    color: var(--hero);
    text-shadow: none;
  }
  .slide.promise .sub-promise {
    font-family: '${brand.fonts.personality.family}', serif;
    font-style: italic;
    font-weight: 500;
    font-size: 38px;
    line-height: 1.05;
    display: block;
    margin-top: 10px;
    opacity: 0.94;
    text-shadow: none;
  }
  .slide.promise .rule {
    display: block;
    width: 60px;
    height: 2px;
    background: var(--accent);
    margin: 26px auto 0;
    border: none;
  }
  .slide.promise .caption {
    display: block;
    margin-top: 16px;
    font-size: 20px;
    line-height: 1.35;
    opacity: 0.80;
    text-shadow: none;
  }

  /* ===== HOOK tipografía ===== */
  .hero {
    font-family: '${brand.fonts.display.family}', sans-serif;
    font-weight: ${brand.fonts.display.weight};
    font-size: 160px;
    line-height: 0.82;
    letter-spacing: -0.05em;
    text-transform: uppercase;
    display: block;
    margin-top: 2px;
    color: var(--hero);
    text-shadow: 0 4px 24px rgba(0,0,0,0.6);
  }
  .sub {
    font-family: '${brand.fonts.personality.family}', serif;
    font-style: italic;
    font-weight: 500;
    font-size: 48px;
    line-height: 1;
    margin-top: 4px;
    display: block;
    text-shadow: 0 2px 12px rgba(0,0,0,0.55);
  }
  .micro {
    font-family: '${brand.fonts.personality.family}', serif;
    font-style: italic;
    font-weight: 500;
    font-size: 22px;
    color: var(--bg);
    margin-top: 14px;
    display: block;
    text-shadow: 0 2px 8px rgba(0,0,0,0.65);
  }
  .caption-bottom {
    position: absolute;
    bottom: 80px;
    left: 36px;
    right: 36px;
    z-index: 2;
    font-family: '${brand.fonts.personality.family}', serif;
    font-style: italic;
    font-weight: 500;
    font-size: 24px;
    line-height: 1.2;
    text-shadow: 0 1px 8px rgba(0,0,0,0.6);
  }

  /* ===== MATCHES (partidos de hoy) ===== */
  .matches-overlay { top: 0; left: 0; right: 0; text-align: center; padding: 64px 40px; }
  .matches-title {
    font-family: '${brand.fonts.display.family}', sans-serif;
    font-weight: ${brand.fonts.display.weight};
    color: var(--hero); font-size: 88px; line-height: 0.9;
    text-transform: uppercase; letter-spacing: -0.02em; margin: 12px 0 22px;
  }
  .match-row { display: flex; align-items: center; justify-content: center; gap: 12px; margin: 14px 0; }
  .match-row .flag { height: 40px; width: auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.5); }
  .match-row .team {
    font-family: '${brand.fonts.display.family}', sans-serif;
    font-weight: ${brand.fonts.display.weight};
    font-size: 24px; text-transform: uppercase; letter-spacing: -0.01em; color: var(--bg);
  }
  .match-row .vs {
    font-family: '${brand.fonts.personality.family}', cursive;
    font-style: italic; font-size: 24px; color: var(--accent);
  }
  .match-row.hl .team { color: var(--accent); }
  .match-row.hl .flag { height: 48px; }
  .matches-caption { display: block; margin-top: 28px; font-size: 26px; opacity: 0.95; }

  /* ===== per-slide (generado desde inputs.json) ===== */
  ${perSlideCss}
</style>
</head>
<body>

<div class="label">${esc(brand.name)} · <span class="accent">${esc(inputs.slug)} · template v${TEMPLATE_VERSION}</span> · preview 50% — generado por generar.js, NO editar a mano</div>

${slidesHtml}

</body>
</html>
`;
}

(async () => {
  const t0 = Date.now();
  const carruselDir = path.resolve(process.argv[2] || DEFAULT_CARRUSEL);
  const inputsPath = path.join(carruselDir, 'inputs.json');

  if (!fs.existsSync(inputsPath)) {
    console.error('No encontré inputs.json en:', carruselDir);
    console.error('Uso: node generar.js <path-carpeta-carrusel>');
    process.exit(1);
  }

  const inputs = JSON.parse(fs.readFileSync(inputsPath, 'utf8'));
  const brandPath = path.resolve(carruselDir, inputs.brand);
  if (!fs.existsSync(brandPath)) {
    console.error('No encontré brand.json en:', brandPath);
    process.exit(1);
  }
  const brandRaw = JSON.parse(fs.readFileSync(brandPath, 'utf8'));
  const brandDir = path.dirname(brandPath);

  // resolver assets a file:// absolutos
  const brand = {
    ...brandRaw,
    logoUrl: fileUrl(path.resolve(brandDir, brandRaw.logo.footer)),
    complianceText:
      brandRaw.compliance && brandRaw.compliance.leyendas
        ? brandRaw.compliance.leyendas.join(' · ').replace(/\.\s*·/g, ' ·').replace(/\.$/, '.')
        : null,
  };
  for (const slide of inputs.slides) {
    if (slide.photo) {
      const p = path.resolve(carruselDir, slide.photo);
      if (!fs.existsSync(p)) {
        console.error(`Foto no encontrada (slide ${slide.file}):`, p);
        process.exit(1);
      }
      slide.photoUrl = fileUrl(p);
    }
    if (slide.matches) {
      slide.matchesResolved = slide.matches.map((pair) => ({
        aName: pair[0].name,
        bName: pair[1].name,
        aUrl: fileUrl(path.resolve(carruselDir, 'flags', pair[0].code + '.png')),
        bUrl: fileUrl(path.resolve(carruselDir, 'flags', pair[1].code + '.png')),
        hl: slide.highlight && (pair[0].code === slide.highlight || pair[1].code === slide.highlight),
      }));
    }
  }

  // compliance solo en los slides configurados (default: closer)
  const complianceSlides = (brandRaw.compliance && brandRaw.compliance.slides) || ['closer'];
  if (brand.complianceText) {
    // el footerHtml del closer ya lo inyecta; otros tipos no implementados aún
    if (!complianceSlides.includes('closer')) brand.complianceText = null;
  }

  // componer + escribir preview
  const html = buildHtml(inputs, brand);
  const previewPath = path.join(carruselDir, 'preview.html');
  fs.writeFileSync(previewPath, html, 'utf8');
  console.log('Preview generado:', previewPath);

  const outputDir = path.join(carruselDir, 'output');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  console.log('Abriendo navegador...');
  const browser = await puppeteer.launch({
    headless: 'new',
    defaultViewport: { width: 700, height: 800, deviceScaleFactor: 2 },
  });

  const page = await browser.newPage();
  await page.goto(fileUrl(previewPath), { waitUntil: 'networkidle0', timeout: 60000 });

  await page.evaluate(async () => {
    await document.fonts.ready;
    const imgs = Array.from(document.images);
    await Promise.all(
      imgs.map((img) => {
        if (img.complete) return Promise.resolve();
        return new Promise((res) => {
          img.onload = img.onerror = () => res();
        });
      })
    );
  });
  await new Promise((r) => setTimeout(r, 800));

  console.log('Renderizando slides 1080x1350...\n');
  const ok = [];
  const skipped = [];
  for (let i = 0; i < inputs.slides.length; i++) {
    const slide = inputs.slides[i];
    const el = await page.$(`.s${i + 1}`);
    if (!el) {
      console.warn('  [skip]', slide.file);
      skipped.push(slide.file);
      continue;
    }
    const out = path.join(outputDir, slide.file + '.jpg');
    await el.screenshot({ path: out, type: 'jpeg', quality: 95 });
    console.log('  [ok]  ', slide.file + '.jpg');
    ok.push(slide.file);
  }

  await browser.close();

  // log estructurado de la corrida
  const run = {
    ts: new Date().toISOString(),
    carrusel: inputs.slug,
    templateVersion: TEMPLATE_VERSION,
    slides: inputs.slides.length,
    ok,
    skipped,
    durationMs: Date.now() - t0,
    outputDir,
  };
  fs.appendFileSync(path.join(carruselDir, 'runs.jsonl'), JSON.stringify(run) + '\n', 'utf8');

  console.log('\nListo. JPGs en:', outputDir);
  console.log('Corrida registrada en runs.jsonl (' + run.durationMs + 'ms)');
})();
