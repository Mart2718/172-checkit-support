// Usage: node tools/render_checks.js fn3 [pf3 ...]   (run from the repo root after `node build.js`)
// Renders each built page with the same KaTeX version the live site loads (tools/node_modules/katex, pinned to
// KATEX_VERSION in build.js) and checks, on every tab:
//   1. no KaTeX errors and no unrendered \( \) delimiters
//   2. no correct choice is the uniquely widest button (a test-taking giveaway); items with fewer than 4 choices,
//      which are fixed categories like Function / Not a function, are exempt
//   3. reflow at 320 px, embedded, with and without the WCAG 1.4.12 text-spacing override: the page never scrolls
//      sideways and no equation sticks out past the screen (the Quick Summary table may scroll inside its own frame;
//      data tables are exempt from 1.4.10, so equations inside a table are reported as notes, not failures)
// Exit code 1 if anything fails.
const path = require('path');
const fs = require('fs');
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
const ROOT = path.resolve(__dirname, '..');
const K = path.join(__dirname, 'node_modules/katex/dist/');
const want = (fs.readFileSync(path.join(ROOT, 'build.js'), 'utf8').match(/KATEX_VERSION = '([^']+)'/) || [])[1];
const have = require(path.join(__dirname, 'node_modules/katex/package.json')).version;
if (want !== have) { console.error(`tools/node_modules/katex is ${have} but build.js loads ${want}: run "npm i katex@${want}" in tools/`); process.exit(2); }

async function routeKatex(page) {
  const cors = { 'Access-Control-Allow-Origin': '*' };
  await page.route(/(jsdelivr|cdnjs).*\/(katex\.min\.css|katex\.min\.js|contrib\/auto-render\.min\.js|fonts\/[^?]+)/, (r) => {
    const f = r.request().url().split('/dist/')[1];
    const type = f.endsWith('.css') ? 'text/css' : f.endsWith('.js') ? 'application/javascript' : 'font/woff2';
    r.fulfill({ path: K + f, contentType: type, headers: cors });
  });
  await page.route(/youtube/, (r) => r.fulfill({ body: '<html></html>', contentType: 'text/html' }));
}

(async () => {
  const codes = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  let failures = 0;
  for (const code of codes) {
    const file = path.join(ROOT, 'dist', code.toLowerCase(), 'index.html');
    const out = [];
    // 1 and 2: desktop
    const p = await browser.newPage({ viewport: { width: 1000, height: 900 } });
    await routeKatex(p);
    await p.goto('file://' + file); await p.waitForTimeout(700);
    const tabs = await p.$$eval('[role=tab]', (e) => e.map((x) => x.id.replace('tab-btn-', '')));
    let katexCount = 0;
    for (const t of tabs) {
      await p.evaluate((n) => switchTab(n), t);
      const r = await p.evaluate(() => {
        const errs = [...document.querySelectorAll('.katex-error')].map((e) => e.textContent.slice(0, 50));
        const panel = document.querySelector('[role=tabpanel]:not([hidden])') || document.body;
        const raw = /\\\(|\\\)/.test(panel.innerText) ? ['unrendered delimiter on this tab'] : [];
        const btns = [...document.querySelectorAll('.guess-btn')].filter((e) => e.offsetParent).map((e) => {
          const range = document.createRange(); range.selectNodeContents(e);
          const m = e.getAttribute('onclick').match(/'([^']+)','([^']+)','([^']+)'/);
          return { id: m[1], v: m[2], k: m[3], w: Math.round(range.getBoundingClientRect().width) };
        });
        return { errs, raw, btns, k: document.querySelectorAll('.katex').length };
      });
      katexCount = r.k;
      r.errs.forEach((e) => out.push(`FAIL ${t}: KaTeX error near "${e}"`));
      r.raw.forEach((e) => out.push(`FAIL ${t}: ${e}`));
      const by = {};
      r.btns.forEach((o) => (by[o.id] = by[o.id] || []).push(o));
      for (const id in by) {
        const a = by[id], key = a.find((o) => o.v === o.k);
        if (!key || a.length < 4) continue;   // two or three fixed categories (Function / Not a function) are exempt
        const others = Math.max(...a.filter((o) => o.v !== o.k).map((o) => o.w));
        if (key.w > others) out.push(`FAIL ${id}: the correct choice is the uniquely widest (${key.w}px vs ${others}px)`);
      }
    }
    await p.close();
    // 3: reflow
    for (const spacing of [false, true]) {
      const q = await browser.newPage({ viewport: { width: 320, height: 900 } });
      await routeKatex(q);
      if (spacing) await q.addInitScript(() => { document.addEventListener('DOMContentLoaded', () => { const s = document.createElement('style'); s.textContent = '*{line-height:1.5!important;letter-spacing:0.12em!important;word-spacing:0.16em!important}p{margin-bottom:2em!important}'; document.head.appendChild(s); }); });
      await q.goto('file://' + file + '?embed=1'); await q.waitForTimeout(700);
      for (const t of tabs) {
        await q.evaluate((n) => switchTab(n), t);
        const r = await q.evaluate(() => ({
          doc: document.documentElement.scrollWidth,
          wide: [...document.querySelectorAll('.katex-display, .katex')].filter((e) => e.offsetParent && e.getBoundingClientRect().right > 321)
            .map((e) => ({ inTable: !!e.closest('table'), text: e.textContent.slice(0, 30) })),
        }));
        const label = spacing ? '320px + text spacing' : '320px';
        if (r.doc > 321) out.push(`FAIL ${t} @${label}: the page scrolls sideways (${r.doc}px)`);
        r.wide.filter((w) => !w.inTable).forEach((w) => out.push(`FAIL ${t} @${label}: equation sticks out: "${w.text}"`));
        if (r.wide.some((w) => w.inTable) && !spacing) out.push(`note ${t}: the table scrolls inside its frame at 320px (allowed)`);
      }
      await q.close();
    }
    const fails = out.filter((l) => l.startsWith('FAIL'));
    failures += fails.length;
    console.log(`${code.toUpperCase()}: ${fails.length ? fails.length + ' problem(s)' : 'PASS'} (${katexCount} equations rendered)`);
    out.forEach((l) => console.log('  ' + l));
  }
  await browser.close();
  process.exit(failures ? 1 : 0);
})();
