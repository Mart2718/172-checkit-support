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
    if (window.renderMathInElement) renderMathInElement(b, { delimiters: [{left:"\\(",right:"\\)",display:false}], throwOnError:false });
  });
  fb.setAttribute('tabindex','-1');
  fb.focus();
  if (window.renderMathInElement) {
    renderMathInElement(fb, { delimiters: [{left:"\\[",right:"\\]",display:true},{left:"\\(",right:"\\)",display:false}], throwOnError:false });
  }
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
});
