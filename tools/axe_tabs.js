// Usage: node axe_tabs.js page.html   (needs: npm i axe-core ; playwright available)
const path = require('path');
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
const axeSrc = require('fs').readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
(async () => {
  const file = path.resolve(process.argv[2]);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  let bad = 0;
  for (const [label, query, w] of [['standalone @1000', '', 1000], ['embed @320', '?embed=1', 320]]) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.route(/cdnjs|jsdelivr|unpkg/, r => r.abort());   // sandbox: no CDN
    await page.goto('file://' + file + query);
    await page.addScriptTag({ content: axeSrc });
    const tabs = await page.$$eval('[role=tab]', els => els.filter(e => !e.hidden).map(e => e.id.replace('tab-btn-', '')));
    if (!tabs.length) tabs.push(null);   // pages without tabs (hub): audit the page once
    for (const t of tabs) {
      if (t) await page.evaluate(n => switchTab(n), t);
      const res = await page.evaluate(async () => await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'] }));
      const v = res.violations;
      console.log(`[${label}] tab ${t || 'page'}: ${v.length} violation(s), ${res.incomplete.length} needing review`);
      v.forEach(x => { bad++; console.log(`   - ${x.id} (${x.impact}): ${x.help} -> ${x.nodes.slice(0, 3).map(n => n.target.join(' ')).join(' | ')}`); });
      res.incomplete.filter(x => x.id !== 'color-contrast').forEach(x => console.log(`   ? review: ${x.id}`));
    }
    await page.close();
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
