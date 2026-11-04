// Render an FAQ page in Chromium, open every tab, and report KaTeX errors, unrendered math, missing graph descriptions,
// and axe-core (WCAG 2.1 AA) violations at 1000 px and 320 px. Usage: node faq_checks.js /path/to/repo
const path = require('path'), fs = require('fs'), http = require('http');
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
const T = path.join(__dirname, '..', 'node_modules');
const KT = path.join(__dirname, 'node_modules');   // KaTeX at the version the FAQ pages load (0.16.47)
const axeSrc = fs.readFileSync(path.join(T, 'axe-core/axe.min.js'), 'utf8');
const repo = path.resolve(process.argv[2]);
const srv = http.createServer((q, r) => { const f = path.join(repo, decodeURIComponent(q.url.split('?')[0]).replace(/\/$/, '/index.html'));
  fs.readFile(f, (e, b) => { if (e) { r.statusCode = 404; return r.end(); } r.setHeader('Content-Type', f.endsWith('.json') ? 'application/json' : 'text/html'); r.end(b); }); });
(async () => {
  await new Promise(r => srv.listen(8765, r));
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  let bad = 0;
  for (const w of [1000, 320]) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.route(/cdn\.jsdelivr\.net\/npm\/katex@[^/]+\/dist\/(.*)/, (route) => {   // serve the local KaTeX build
      const rel = route.request().url().split('/dist/')[1]; const f = path.join(KT, 'katex/dist', rel);
      fs.existsSync(f) ? route.fulfill({ body: fs.readFileSync(f), headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': rel.endsWith('.css') ? 'text/css' : rel.endsWith('.js') ? 'application/javascript' : 'font/woff2' } }) : route.abort(); });
    await page.route(/fonts\.googleapis|fonts\.gstatic|youtube|unpkg|cdnjs/, r => r.abort());
    const errs = []; page.on('pageerror', e => errs.push(e.message));
    await page.goto('http://localhost:8765/index.html'); await page.waitForTimeout(1500);
    const tabs = await page.$$eval('[role=tab]', els => els.map(e => e.id));
    const res = [];
    for (const t of (tabs.length ? tabs : [null])) {
      if (t) { await page.click('#' + t).catch(() => {}); await page.waitForTimeout(400); }
      // open every collapsed answer so its math renders and is checked
      await page.$$eval('details', ds => ds.forEach(d => d.open = true));
      await page.$$eval('button[aria-expanded="false"]', bs => bs.forEach(b => b.click())).catch(() => {});
      await page.waitForTimeout(500);
      const info = await page.evaluate(() => ({
        katexErr: [...document.querySelectorAll('.katex-error')].map(e => e.title || e.textContent).slice(0, 5),
        raw: [...document.querySelectorAll('body *')].filter(e => e.children.length === 0 && /\\\(|\\\[|\\frac|\\dfrac|\\pi/.test(e.textContent) && !e.closest('script,style,.katex,textarea,pre,code,.gl-prompt-preview,[class*=prompt]')).map(e => e.textContent.slice(0, 80)).slice(0, 5),
        svgNoText: [...document.querySelectorAll('svg')].filter(s => !s.closest('button,a') && s.getAttribute('aria-hidden') !== 'true' && !s.closest('[aria-hidden=true]') && !s.getAttribute('aria-label') && !s.querySelector('title') && s.getBoundingClientRect().width > 40).map(s => (s.parentElement.className || s.parentElement.tagName) + ' ' + s.getBoundingClientRect().width.toFixed(0) + 'px'),
        wide: document.documentElement.scrollWidth > window.innerWidth + 1 }));
      await page.addScriptTag({ content: axeSrc });
      const ax = await page.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] })).violations.map(v => `${v.id} (${v.impact}) x${v.nodes.length}: ${v.nodes.slice(0, 2).map(n => n.target.join(' ')).join(' | ')}`));
      res.push({ tab: t, ...info, ax });
    }
    const seen = new Set();
    for (const r of res) {
      const probs = [...r.katexErr.map(x => 'KaTeX error: ' + x), ...r.raw.map(x => 'unrendered math: ' + x), ...r.svgNoText.slice(0,3).map(x => 'graph without a text description: ' + x), ...(r.wide ? ['page scrolls sideways'] : []), ...r.ax.map(x => 'axe: ' + x)];
      const fresh = probs.filter(p => !seen.has(p)); fresh.forEach(p => seen.add(p)); bad += fresh.length;
      console.log(`[${w}px] ${r.tab || 'page'}: ${fresh.length ? fresh.length + ' new issue(s)' : 'ok'}`); fresh.forEach(p => console.log('   - ' + p));
    }
    errs.forEach(e => { bad++; console.log(`[${w}px] page error: ${e}`); });
    await page.close();
  }
  await browser.close(); srv.close();
  console.log(bad ? `${bad} issue(s)` : 'ALL PASS');
})();
