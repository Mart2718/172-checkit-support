// Build script: content/*.yml + template/ + figures/  ->  dist/<code>/index.html (one page per outcome) + dist/index.html (hub).
// Run locally with:  npm install && npm run build      Netlify runs it for you on every commit.
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const ROOT = __dirname;
const BS = String.fromCharCode(92); // backslash (keeps LaTeX delimiters out of regex/escape trouble)
const CSS = fs.readFileSync(path.join(ROOT, 'template/styles.css'), 'utf8');
const APP_JS = fs.readFileSync(path.join(ROOT, 'template/app.js'), 'utf8');
const KATEX = [
  '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">',
  '<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>',
  '<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>'
].join('\n');

const esc = (s) => String(s).split('&').join('&amp;').split('<').join('&lt;').split('>').join('&gt;').split('"').join('&quot;');
function stripTags(s) { let o = '', t = false; for (const c of String(s)) { if (c === '<') t = true; else if (c === '>') t = false; else if (!t) o += c; } return o; }
const count = (s, sub) => s.split(sub).length - 1;

// ------------------------------------------------------------------ validation (fails the build with a readable message)
function validate(file, c) {
  const errors = [], warnings = [];
  const need = (cond, msg) => { if (!cond) errors.push(`${file}: ${msg}`); };
  ['code', 'h1', 'pageTitle', 'videoIntro'].forEach((k) => need(c[k], `missing "${k}"`));
  need(c.summary && c.summary.intro && c.summary.caption && Array.isArray(c.summary.columns) && Array.isArray(c.summary.rows) && c.summary.note, 'summary needs intro, caption, columns, rows and note');
  need(Array.isArray(c.tabs) && c.tabs.length > 0, 'needs at least one entry under "tabs"');
  const ban = c.banPhrases ? new RegExp(c.banPhrases, 'i') : null;
  if (!ban) warnings.push(`${file}: no "banPhrases" set, so pre-guess text is not checked for leaked answers`);
  const ids = new Set();
  const claim = (id, where) => { if (ids.has(id)) errors.push(`${file}: duplicate id "${id}" (${where})`); ids.add(id); };
  ['video', 'method'].forEach((x) => ids.add(x));
  (c.tabs || []).forEach((tab) => {
    need(tab.id && tab.label && tab.heading && tab.intro && Array.isArray(tab.items), `tab "${tab.id}" needs id, label, heading, intro, items`);
    claim(tab.id, 'tab');
    (tab.items || []).forEach((it) => {
      const w = `item "${it.id}"`;
      need(it.id && it.title && it.prompt && it.explanation, `${w} needs id, title, prompt, explanation`);
      claim(it.id, 'item');
      need(Array.isArray(it.choices) && it.choices.length >= 2, `${w} needs at least 2 choices`);
      need((it.choices || []).some((x) => x.value === it.correct), `${w}: "correct" must equal one of the choice values`);
      (it.choices || []).forEach((x) => need(!/\\\(|\\\[/.test(x.label || '') || x.speak, `${w}: choice "${x.value}" contains math, so it needs a "speak" field (plain-words reading for screen readers)`));
      need(it.figure || it.table || it.math, `${w} needs a figure, table or math block`);
      if (!stripTags(it.explanation || '').trim() || !(it.explanation || '').includes('<strong>')) warnings.push(`${file}: ${w}: explanation should end with the verdict in <strong>...</strong> (the worked-examples tool reads it)`);
      if (it.figure) {
        need(it.figure.file && fs.existsSync(path.join(ROOT, it.figure.file)), `${w}: figure file not found: ${it.figure.file}`);
        need(it.figure.title, `${w}: figure needs a title (the short text alternative)`);
        need(it.figure.caption && stripTags(it.figure.caption).length >= 25, `${w}: figure needs a caption describing the plotted data (at least a sentence)`);
        if (ban) [it.figure.title, stripTags(it.figure.caption || '')].forEach((t) => { if (ban.test(t)) errors.push(`${file}: ${w}: figure text gives away the answer before the guess: "${t}"`); });
      }
      if (it.table) {
        need(it.table.caption, `${w}: table needs a caption`);
        need(Array.isArray(it.table.rows) && it.table.rows.length > 0, `${w}: table needs rows`);
        if (ban) [it.table.caption, it.table.label || ''].forEach((t) => { if (ban.test(t)) errors.push(`${file}: ${w}: table text gives away the answer before the guess: "${t}"`); });
      }
      if (ban && ban.test(it.title)) errors.push(`${file}: ${w}: title gives away the answer: "${it.title}"`);
      [it.prompt, it.explanation, (it.figure || {}).caption].forEach((t) => { if (t && count(t, BS + '(') !== count(t, BS + ')')) errors.push(`${file}: ${w}: unbalanced math delimiters in: ${stripTags(t).slice(0, 60)}`); });
    });
  });
  return { errors, warnings };
}

// ------------------------------------------------------------------ rendering
function renderFigure(it) {
  const f = it.figure;
  let svg = fs.readFileSync(path.join(ROOT, f.file), 'utf8').trim();
  const open = svg.indexOf('<svg') + 4;
  const close = svg.indexOf('>', open);
  const attrs = ` role="img" aria-labelledby="${it.id}-svg-title" aria-describedby="${it.id}-caption"`;
  svg = svg.slice(0, open) + attrs + svg.slice(open, close + 1) + `\n<title id="${it.id}-svg-title">${esc(f.title)}</title>` + svg.slice(close + 1);
  // collapse: true tucks the text description into a closed <details>, for graphs whose description would answer the
  // question before the guess. aria-describedby still gives screen readers the full description.
  const cap = f.collapse ? `<details><summary>Text description of the graph</summary>${f.caption}</details>` : f.caption;
  return `      <figure>\n${svg}\n        <figcaption id="${it.id}-caption">${cap}</figcaption>\n      </figure>`;
}
function renderTable(it) {
  const t = it.table;
  const colHeaders = t.headers === 'row';   // headers: row  => first ROW holds the header cells; default: first COLUMN does
  const rows = t.rows.map((r, ri) => '        <tr>' + r.map((cell, ci) => {
    const c = esc(cell);
    if (colHeaders && ri === 0) return `<th scope="col">${c}</th>`;
    if (!colHeaders && ci === 0) return `<th scope="row">${c}</th>`;
    return `<td>${c}</td>`;
  }).join('') + '</tr>').join('\n');
  return `      <div class="table-wrap" role="region" aria-label="${esc(t.label || t.caption)}" tabindex="0">\n      <table class="data-table">\n        <caption class="tbl-cap">${esc(t.caption)}</caption>\n${rows}\n      </table>\n      </div>`;
}
function renderMath(m) {
  // optional "speak": a plain-words reading. It becomes the accessible name, so screen readers read the equation reliably.
  if (m.display) return m.speak
    ? `      <div role="img" aria-label="${esc(m.speak)}" style="font-size:18px;text-align:center;margin:1em 0;">${BS}[ ${m.display} ${BS}]</div>`
    : `      <p style="font-size:18px;text-align:center;">${BS}[ ${m.display} ${BS}]</p>`;
  return `      <p style="font-size:16px;">${m.inline.map((x) => `${BS}( ${x} ${BS})`).join(', ')}</p>`;
}
function renderItem(it, prefix) {
  const parts = [`    <div class="item" id="${it.id}">`, `      <h3>${esc(it.title)}</h3>`];
  if (it.figure) parts.push(renderFigure(it));
  if (it.table) parts.push(renderTable(it));
  if (it.math) parts.push(renderMath(it.math));
  parts.push(`      <p class="prompt" id="${it.id}-q">${it.prompt}</p>`);
  parts.push(`      <div class="guess-row" role="group" aria-labelledby="${it.id}-q">`);
  it.choices.forEach((ch) => parts.push(`        <button type="button" class="guess-btn" data-guess="${esc(ch.value)}" data-label="${esc(prefix + ch.label)}"${ch.speak ? ` aria-label="${esc(prefix + ch.speak)}"` : ''} aria-pressed="false" onclick="checkGuess(this,'${it.id}','${ch.value}','${it.correct}')">${esc(prefix + ch.label)}</button>`));
  parts.push('      </div>');
  parts.push(`      <div id="${it.id}-feedback" class="feedback" hidden aria-live="polite"></div>`);
  parts.push(`      <div id="${it.id}-explanation" hidden>${it.explanation}</div>`);
  parts.push('    </div>');
  return parts.join('\n');
}
function renderVideo(c) {
  const v = c.video;
  let body;
  if (v && v.embed) {
    body = `    <p><a href="${esc(v.url || v.embed)}" target="_blank" rel="noopener">Open the ${esc(c.code)} video walkthrough in a new tab</a></p>\n` +
      `    <p><iframe width="100%" height="450" loading="lazy" src="${esc(v.embed)}" title="${esc(v.title || c.code + ' video walkthrough')}" style="border:1px solid #d4d4d8;border-radius:8px;" allowfullscreen></iframe></p>` +
      (v.transcript ? `\n    <p><a href="${esc(v.transcript)}" target="_blank" rel="noopener">Read the ${esc(c.code)} video transcript (opens in a new tab)</a></p>` : '');
  } else {
    body = '    <div class="video-wrap">\n      <p style="margin:0;">The video walkthrough is coming soon. In the meantime, the Quick Summary and the Try It tabs cover the same ideas.</p>\n    </div>';
  }
  return `  <section id="tab-video" class="tab-panel" role="tabpanel" aria-labelledby="tab-btn-video">\n    <h2 tabindex="-1">Watch a Video to Learn</h2>\n    <p>${esc(c.videoIntro)}</p>\n${body}\n  </section>`;
}
function renderSummary(c) {
  const s = c.summary;
  const head = s.columns.map((x) => `<th scope="col">${esc(x)}</th>`).join('');
  const rows = s.rows.map((r) => '        <tr>' + r.map((cell, i) => (i === 0 ? `<th scope="row">${cell}</th>` : `<td>${cell}</td>`)).join('') + '</tr>').join('\n');
  return `  <section id="tab-method" class="tab-panel" role="tabpanel" aria-labelledby="tab-btn-method" tabindex="0" hidden>\n    <h2 tabindex="-1">Quick Summary</h2>\n    <p>${s.intro}</p>\n    <div class="table-wrap" role="region" aria-label="Summary table" tabindex="0">\n    <table class="data-table summary-table">\n      <caption class="tbl-cap">${esc(s.caption)}</caption>\n      <thead><tr>${head}</tr></thead>\n      <tbody>\n${rows}\n      </tbody>\n    </table>\n    </div>\n    <div class="note-box">\n      <p style="margin:0;">${s.note}</p>\n    </div>\n  </section>`;
}
function renderCredits(code) {
  return `  <section class="ai-statement" aria-labelledby="ai-statement-heading">
    <h2 id="ai-statement-heading">Sources &amp; Credits</h2>
    <p>Content on this page adapts the ${esc(code)} outcome and exercise types from <a href="https://github.com/TeamBasedInquiryLearning/library" target="_blank" rel="noopener">TBIL Precalculus</a> by Steven Clontz and Drew Lewis, used under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a>.</p>
    <p>AI use statement: The explanations, diagrams, and this page&rsquo;s structure were drafted using Claude (Anthropic) based on TBIL source content, with guidance, review, and editing by Dr. Marty Romero.</p>
    <p>This page is licensed <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a> and freely available for reuse and adaptation under the same terms.</p>
  </section>`;
}
function renderPage(c) {
  const tabIds = ['video', 'method', ...c.tabs.map((t) => t.id)];
  const labels = { video: 'Watch a Video to Learn', method: 'Quick Summary' };
  c.tabs.forEach((t) => { labels[t.id] = t.label; });
  const buttons = tabIds.map((id, i) => `  <button class="tab-btn" id="tab-btn-${id}" role="tab" aria-selected="${i === 0}" aria-controls="tab-${id}" tabindex="${i === 0 ? 0 : -1}" onclick="switchTab('${id}')">${esc(labels[id])}</button>`).join('\n');
  const tryPanels = c.tabs.map((t) => `  <section id="tab-${t.id}" class="tab-panel" role="tabpanel" aria-labelledby="tab-btn-${t.id}" hidden>\n    <h2 tabindex="-1">${esc(t.heading)}</h2>\n    <p>${t.intro}</p>\n\n${t.items.map((it) => renderItem(it, c.choicePrefix || 'I think: ')).join('\n\n')}\n  </section>`).join('\n\n');
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(c.pageTitle)}</title>
${KATEX}
<style>
${CSS}</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>

<header>
  <div>
    <p>Math 172 — Santa Ana College</p>
    <h1>${esc(c.h1)}</h1>
  </div>
  <div style="font-size:12px;opacity:0.75;text-align:right;">CheckIt Practice Companion</div>
</header>

<nav aria-label="Page sections">
<div class="tabs" role="tablist" aria-label="Sections of this page" onkeydown="handleTabKey(event)">
${buttons}
</div>
</nav>

<main id="main">

${renderVideo(c)}

${renderSummary(c)}

${tryPanels}

${renderCredits(c.code)}

</main>

<footer>
  Math 172 &nbsp;|&nbsp; ${esc(c.code)} CheckIt Support &nbsp;|&nbsp; Santa Ana College &nbsp;|&nbsp; Built for SAC
</footer>

<script>
${APP_JS.split('/*TAB_ORDER*/').join(JSON.stringify(tabIds))}</script>
</body>
</html>
`;
}
function renderHub(all) {
  const list = all.map((c) => `      <li><a href="${c.code.toLowerCase()}/"><strong>${esc(c.code)}</strong>: ${esc(c.hubSummary || c.h1)}</a></li>`).join('\n');
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CheckIt Support Pages — Math 172, Santa Ana College</title>
<style>
${CSS}  .hub-list{list-style:none;padding:0;margin:16px 0;}
  .hub-list li{background:#fff;border:1px solid var(--gray-mid);border-radius:8px;margin:10px 0;}
  .hub-list a{display:block;padding:14px 18px;color:var(--teal-dark);font-size:17px;}
  .hub-list a:hover{background:var(--teal-light);}
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <div>
    <p>Math 172 — Santa Ana College</p>
    <h1>CheckIt Support Pages</h1>
  </div>
</header>
<main id="main">
  <section aria-labelledby="pages-heading">
    <h2 id="pages-heading">Choose a learning outcome</h2>
    <p>Each page supports the CheckIt practice for one learning outcome in <em>Building Toward Calculus</em>: a short video, a quick summary, and guess-first practice that explains the reasoning.</p>
    <ul class="hub-list">
${list}
    </ul>
  </section>
${renderCredits('listed')}
</main>
<footer>
  Math 172 &nbsp;|&nbsp; CheckIt Support &nbsp;|&nbsp; Santa Ana College &nbsp;|&nbsp; Built for SAC
</footer>
</body>
</html>
`;
}

// ------------------------------------------------------------------ main
const natural = (a, b) => a.localeCompare(b, undefined, { numeric: true });
const files = fs.readdirSync(path.join(ROOT, 'content')).filter((f) => f.endsWith('.yml')).sort(natural);
const dist = path.join(ROOT, 'dist');
fs.rmSync(dist, { recursive: true, force: true });
fs.mkdirSync(dist, { recursive: true });
const built = []; let failed = false;
for (const f of files) {
  const c = yaml.load(fs.readFileSync(path.join(ROOT, 'content', f), 'utf8'));
  const { errors, warnings } = validate('content/' + f, c || {});
  warnings.forEach((w) => console.warn('WARNING ' + w));
  if (errors.length) { failed = true; errors.forEach((e) => console.error('ERROR ' + e)); continue; }
  const dir = path.join(dist, c.code.toLowerCase());
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), renderPage(c));
  built.push(c);
  console.log(`built ${c.code}  ->  /${c.code.toLowerCase()}/`);
}
if (failed) { console.error('\nBuild stopped: fix the errors above. (Netlify keeps the last good version live.)'); process.exit(1); }
fs.writeFileSync(path.join(dist, 'index.html'), renderHub(built));
console.log(`built hub  ->  /   (${built.length} outcome page${built.length === 1 ? '' : 's'})`);
