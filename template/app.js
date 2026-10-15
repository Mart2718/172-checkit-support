var TAB_ORDER = /*TAB_ORDER*/;

function switchTab(name) {
  var panels = document.querySelectorAll('.tab-panel');
  var btns = document.querySelectorAll('.tab-btn');
  panels.forEach(function(p){ p.hidden = (p.id !== 'tab-' + name); });
  btns.forEach(function(b){
    var active = (b.id === 'tab-btn-' + name);
    b.setAttribute('aria-selected', active ? 'true' : 'false');
    b.setAttribute('tabindex', active ? '0' : '-1');
  });
  var shown = document.getElementById('tab-' + name);
  var heading = shown.querySelector('h2');
  if (heading) { heading.setAttribute('tabindex','-1'); heading.focus({preventScroll:false}); }
}

function handleTabKey(event) {
  if (['ArrowRight','ArrowLeft','Home','End'].indexOf(event.key) === -1) return;
  var current = TAB_ORDER.indexOf(event.target.id.replace('tab-btn-',''));
  if (current === -1) return;
  var next = event.key === 'Home' ? 0
    : event.key === 'End' ? TAB_ORDER.length - 1
    : event.key === 'ArrowRight' ? (current + 1) % TAB_ORDER.length
    : (current - 1 + TAB_ORDER.length) % TAB_ORDER.length;
  var nextBtn = document.getElementById('tab-btn-' + TAB_ORDER[next]);
  switchTab(TAB_ORDER[next]);
  nextBtn.focus();
  event.preventDefault();
}

function checkGuess(btn, itemId, guess, correct) {
  var isCorrect = (guess === correct);
  var fb = document.getElementById(itemId + '-feedback');
  var explanation = document.getElementById(itemId + '-explanation').innerHTML;
  fb.innerHTML = (isCorrect ? '<strong><span aria-hidden="true">✅</span> That’s right.</strong> ' : '<strong><span aria-hidden="true">❌</span> Not quite — here’s why:</strong> ') + explanation;
  fb.className = 'feedback ' + (isCorrect ? 'feedback-correct' : 'feedback-incorrect');
  fb.hidden = false;
  var row = btn.closest('.guess-row');
  row.querySelectorAll('.guess-btn').forEach(function(b){
    var picked = (b.dataset.guess === guess);
    b.setAttribute('aria-pressed', picked ? 'true' : 'false');
    // data-label holds the raw label (it may contain \( ... \) math), so rebuild the text and re-render the math each time
    b.textContent = (picked ? '✓ ' : '') + b.dataset.label;
    if (window.renderMathInElement) { renderMathInElement(b, { delimiters: [{left:"\\(",right:"\\)",display:false}], throwOnError:false }); makeMathSpeakable(b); }
  });
  if (window.renderMathInElement) {
    renderMathInElement(fb, { delimiters: [{left:"\\[",right:"\\]",display:true},{left:"\\(",right:"\\)",display:false}], throwOnError:false });
    makeMathSpeakable(fb);
  }
  fb.setAttribute('tabindex','-1');
  fb.focus();   // after the math is rendered, so the screen reader reads the finished text
}

// When embedded in LibreTexts with ?embed=1 appended to the iframe src, the video is already on the host page,
// so hide the Video tab here and open on the Quick Summary instead. The standalone link (no ?embed) keeps the Video tab first.
if (/[?&]embed(=|&|$)/.test(window.location.search)) {
  (function() {
    document.documentElement.classList.add('embed');
    var vb = document.getElementById('tab-btn-video'), vp = document.getElementById('tab-video');
    var mb = document.getElementById('tab-btn-method'), mp = document.getElementById('tab-method');
    TAB_ORDER = TAB_ORDER.filter(function(t){ return t !== 'video'; });
    vb.hidden = true; vp.hidden = true;
    vb.setAttribute('aria-selected','false'); vb.setAttribute('tabindex','-1');
    mb.setAttribute('aria-selected','true'); mb.setAttribute('tabindex','0'); mp.hidden = false;
  })();
}

document.addEventListener("DOMContentLoaded", function() {
  if (!window.renderMathInElement) return;   // KaTeX CDN blocked/offline: equations stay readable as plain LaTeX
  renderMathInElement(document.body, {
    delimiters: [
      {left: "\\[", right: "\\]", display: true},
      {left: "\\(", right: "\\)", display: false}
    ],
    throwOnError: false
  });
  makeMathSpeakable(document.body);
});

/*SPEECH-START*/
// Screen-reader support for math. NVDA and several other screen readers do not read the MathML that KaTeX writes,
// so every rendered equation gets a plain-words reading generated from its TeX source (the visible math is unchanged).
function texToSpeech(tex) {
  var FUNCS = {log:'log', ln:'natural log', sin:'sine', cos:'cosine', tan:'tangent', sec:'secant', csc:'cosecant', cot:'cotangent', exp:'e to the'};
  var WORDS = {infty:'infinity', pi:'pi', theta:'theta', alpha:'alpha', beta:'beta', Delta:'delta', delta:'delta', approx:'is approximately equal to',
    le:'is less than or equal to', leq:'is less than or equal to', ge:'is greater than or equal to', geq:'is greater than or equal to', ne:'is not equal to', neq:'is not equal to',
    cdot:'times', times:'times', pm:'plus or minus', to:'approaches', rightarrow:'approaches', in:'is in', cup:'union', ldots:'dot dot dot', dots:'dot dot dot', cdots:'dot dot dot', div:'divided by'};
  var IGNORE = {left:1, right:1, ',':1, ';':1, ':':1, '!':1, ' ':1, quad:1, qquad:1, displaystyle:1, '\\':1};
  var s = String(tex).replace(/−/g, '-');
  var i = 0;
  function peekCmd() { var m = /^\\([a-zA-Z]+|.)/.exec(s.slice(i)); return m ? m[1] : null; }
  function skipWs() { while (i < s.length && /\s/.test(s[i])) i++; }
  function group() {        // reads {...} (or one character) and returns its raw TeX
    skipWs();
    if (s[i] === '{') { var d = 0, st = i + 1; for (; i < s.length; i++) { if (s[i] === '{') d++; else if (s[i] === '}') { d--; if (d === 0) { i++; return s.slice(st, i - 1); } } } return s.slice(st); }
    var m = /^\\[a-zA-Z]+/.exec(s.slice(i)); if (m) { i += m[0].length; return m[0]; }
    return s[i++] || '';
  }
  function parenGroup() {   // at "(", returns raw TeX up to the matching ")"
    var d = 0, st = i + 1;
    for (; i < s.length; i++) { if (s[i] === '(') d++; else if (s[i] === ')') { d--; if (d === 0) { i++; return s.slice(st, i - 1); } } }
    return s.slice(st);
  }
  function ordinal(n) { var t = n % 100, u = n % 10; return n + ((t >= 11 && t <= 13) ? 'th' : u === 1 ? 'st' : u === 2 ? 'nd' : u === 3 ? 'rd' : 'th'); }
  function power(p) {
    p = p.trim();
    if (p === '2') return ' squared';
    if (p === '3') return ' cubed';
    if (/^\d+$/.test(p)) return ' to the ' + ordinal(+p) + ' power';
    var sp = texToSpeech(p);
    return ' to the power ' + sp + (/^(negative )?[\w.]+$/.test(sp) ? '' : ',');
  }
  var out = [];
  var prevOp = true;        // true at the start and after an operator, "(" or ",": a "-" here means "negative"
  var pendingComma = false;
  function push(t, op) { out.push(t); prevOp = !!op; }
  while (i < s.length) {
    var c = s[i];
    if (/\s/.test(c)) { i++; continue; }
    if (c === '\\') {
      var cmd = peekCmd(); i += 1 + (cmd ? cmd.length : 0);
      if (IGNORE[cmd]) continue;
      if (cmd === 'frac' || cmd === 'dfrac' || cmd === 'tfrac') { var a = texToSpeech(group()), b = texToSpeech(group()); push(/^[\w.\- ]{1,6}$/.test(a) && /^[\w.\- ]{1,6}$/.test(b) ? a + ' over ' + b : 'the fraction ' + a + ' over ' + b + ', end fraction', false); continue; }
      if (cmd === 'sqrt') { var r = texToSpeech(group()); push(/^[\w.]+$/.test(r) ? 'the square root of ' + r : 'the square root of the quantity ' + r + ', end root', false); continue; }
      if (cmd === 'text' || cmd === 'mathrm' || cmd === 'textbf' || cmd === 'mathbf') { push(group(), false); continue; }
      if (cmd === 'mathbb') { var g = group(); push(g === 'R' ? 'the real numbers' : g, false); continue; }
      if (FUNCS[cmd]) {
        var name = FUNCS[cmd];
        if (cmd === 'log' && s[i] === '_') { i++; name += ' base ' + texToSpeech(group()); }
        skipWs();
        if (s[i] === '(') {
          var inner = parenGroup(), single = /^\s*-?\s*([A-Za-z]|\d+(\.\d+)?)(\^\{?\w+\}?)?\s*$/.test(inner);
          var sp2 = texToSpeech(inner);
          push(name + ' of ' + (single ? sp2 : 'the quantity ' + sp2), false);
          skipWs(); if (s[i] === '+' || s[i] === '-' || s[i] === '−') out[out.length - 1] += ',';
        } else if (i < s.length && /[A-Za-z0-9\\{]/.test(s[i])) {
          var arg = group(), sp3 = texToSpeech(arg);
          if (s[i] === '^') { i++; sp3 += power(group()); }
          push(name + ' of ' + sp3, false);
        } else push(name, false);
        continue;
      }
      if (WORDS[cmd]) { push(WORDS[cmd], cmd !== 'infty' && cmd !== 'pi' && cmd !== 'theta' && cmd !== 'alpha' && cmd !== 'beta'); continue; }
      push(cmd || '', false); continue;
    }
    if (c === '^') { i++; out.push(power(group())); continue; }
    if (c === '_') { i++; out.push(' sub ' + texToSpeech(group())); continue; }
    if (c === '{' || c === '}') { i++; continue; }
    if (/\d/.test(c)) { var m = /^\d+(\.\d+)?/.exec(s.slice(i)); i += m[0].length; push(m[0], false); continue; }
    if (/[A-Za-z]/.test(c)) {
      var nx = s[i + 1];
      if (/[fgFGhH]/.test(c) && nx === '(' && !/[A-Za-z]/.test(s[i - 1] || '')) { i++; push(c + ' of ' + texToSpeech(parenGroup()), false); skipWs(); if (s[i] === '+' || s[i] === '-') out[out.length - 1] += ','; continue; }
      i++; push(c, false); continue;
    }
    if (c === '=') { i++; push('equals', true); continue; }
    if (c === '<') { i++; push('is less than', true); continue; }
    if (c === '>') { i++; push('is greater than', true); continue; }
    if (c === '+') { i++; push('plus', true); continue; }
    if (c === '-') { i++; push(prevOp ? 'negative' : 'minus', true); continue; }
    if (c === '*') { i++; push('times', true); continue; }
    if (c === '/') { i++; push('divided by', true); continue; }
    if (c === ',') { i++; out.push('comma'); prevOp = true; continue; }
    if (c === '(') { i++; push('open paren', true); continue; }
    if (c === ')') { i++; push('close paren', false); continue; }
    if (c === '[') { i++; push('open bracket', true); continue; }
    if (c === ']') { i++; push('close bracket', false); continue; }
    if (c === '.') { var d3 = s.slice(i, i + 3) === '...'; i += d3 ? 3 : 1; push(d3 ? 'dot dot dot' : 'point', false); continue; }
    if (c === '|') { i++; push('absolute value bars', false); continue; }
    if (c === '%') { i++; push('percent', false); continue; }
    i++;
  }
  return out.join(' ').replace(/\s+,/g, ',').replace(/\s+/g, ' ').trim();
}

// Replaces the hidden MathML that KaTeX writes with a plain-words reading, for every equation under root.
function makeMathSpeakable(root) {
  var nodes = root.querySelectorAll('.katex');
  Array.prototype.forEach.call(nodes, function(k) {
    if (k.getAttribute('data-spoken')) return;
    var ann = k.querySelector('annotation[encoding="application/x-tex"]');
    var holder = k.querySelector('.katex-mathml');
    if (!ann || !holder) return;
    holder.textContent = ' ' + texToSpeech(ann.textContent) + ' ';
    k.setAttribute('data-spoken', '1');
  });
}
/*SPEECH-END*/

if (typeof module !== 'undefined' && module.exports) module.exports = { texToSpeech: texToSpeech };
