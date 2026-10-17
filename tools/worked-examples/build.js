// Worked-examples recording document: content on the left ~2/3, blank right margin for ink/notation.
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, Header, Footer, AlignmentType,
  HeadingLevel, BorderStyle, WidthType, ShadingType, TabStopType, SimpleField, LevelFormat, ImageRun, PageOrientation, PageNumber
} = require('docx');

const meta = JSON.parse(fs.readFileSync(__dirname + '/meta.json', 'utf8'));   // {code, title, coreQuestion, coreFollowup}
const CODE = meta.code;
const DOC_TITLE = meta.title;
const TAB = String.fromCharCode(9);
const NAV = '1A1A2E';
// Landscape US Letter = 15840 x 12240 DXA. Left margin 0.5in, right margin 3in => content 7.5in (68%), blank right ~ 30%.
const M_LEFT = 720, M_RIGHT = 4320, M_TB = 720;
const W = 15840 - M_LEFT - M_RIGHT; // 10800

const items = JSON.parse(fs.readFileSync(__dirname + '/items.json', 'utf8'));

// ---------- text helpers: <strong> -> bold, LaTeX math -> plain text with real superscripts (no regex needed) ----------
const BS = String.fromCharCode(92);                       // backslash
const OPEN = [BS + '(', BS + '['], CLOSE = [BS + ')', BS + ']'];
// LaTeX command -> plain Unicode text. Anything not listed keeps its name without the backslash (for example sin, cos).
const CMD = { left: '', right: '', infty: '∞', leq: '≤', le: '≤', geq: '≥', ge: '≥', neq: '≠', approx: '≈', cdot: '·', times: '×', pm: '±', pi: 'π', theta: 'θ', to: '→', cup: '∪', ldots: '…', cdots: '⋯', log: 'log', ln: 'ln' };
const FUNC = ['log', 'ln', 'sin', 'cos', 'tan', 'sec', 'csc', 'cot'];   // written upright, not italic
function braceGroup(s, i) {   // s[i] is '{'. Returns [text inside the braces, index just after the closing brace]
  let d = 0;
  for (let k = i; k < s.length; k++) { if (s[k] === '{') d++; else if (s[k] === '}') { d--; if (d === 0) return [s.slice(i + 1, k), k + 1]; } }
  return [s.slice(i + 1), s.length];
}
function texToText(tex) {   // convert commands, fractions and roots; leave ^ and _ for mathRuns
  let out = '';
  const wrap = (t) => (t.length > 1 && !/^[0-9.]+$/.test(t) && !/^[A-Za-z](\^(\{[^}]*\}|.))?$/.test(t) ? '(' + t + ')' : t);   // no parentheses around a single letter or a letter with an exponent
  for (let i = 0; i < tex.length; i++) {
    if (tex[i] !== BS) { out += tex[i]; continue; }
    const m = /^[a-zA-Z]+/.exec(tex.slice(i + 1));
    if (!m) { const c = tex[i + 1] || ''; out += (c === ',' || c === ';' || c === ' ') ? ' ' : (c === '!' ? '' : c); i += 1; continue; }
    const name = m[0]; i += name.length;
    if (name === 'frac' || name === 'tfrac' || name === 'dfrac') {
      const [a, j] = braceGroup(tex, i + 1); const [b, k] = braceGroup(tex, j);
      out += wrap(texToText(a)) + '/' + wrap(texToText(b)); i = k - 1;
    } else if (name === 'sqrt') {
      const [a, j] = braceGroup(tex, i + 1); out += '√' + wrap(texToText(a)); i = j - 1;
    } else out += (name in CMD) ? CMD[name] : name;
  }
  return out;
}
function mathRuns(tex, base) {
  tex = texToText(tex).split('-').join('−');   // every hyphen inside math is a minus sign
  const out = []; let buf = '';
  const flush = () => { if (buf) { out.push(new TextRun({ ...base, text: buf, italics: true })); buf = ''; } };
  for (let i = 0; i < tex.length; i++) {
    if (tex[i] === '^' || tex[i] === '_') {   // superscript or subscript: a {group} or a single character
      flush();
      const isSup = tex[i] === '^';
      let part;
      if (tex[i + 1] === '{') { const [g, j] = braceGroup(tex, i + 1); part = g; i = j - 1; } else { part = tex[i + 1]; i += 1; }
      out.push(new TextRun({ ...base, text: part, italics: true, ...(isSup ? { superScript: true } : { subScript: true }) }));
      continue;
    }
    const fn = FUNC.find((f) => tex.startsWith(f, i) && !/[a-zA-Z]/.test(tex[i - 1] || '') && !/[a-zA-Z]/.test(tex[i + f.length] || ''));
    if (fn) { flush(); out.push(new TextRun({ ...base, text: fn })); i += fn.length - 1; continue; }
    buf += tex[i];
  }
  flush();
  return out;
}
function plainWithMath(text, base) {
  const out = []; let rest = text;
  for (;;) {
    let i = -1, k = -1;
    OPEN.forEach((o, j) => { const p = rest.indexOf(o); if (p >= 0 && (i < 0 || p < i)) { i = p; k = j; } });
    if (i < 0) { if (rest) out.push(new TextRun({ ...base, text: rest })); break; }
    if (i > 0) out.push(new TextRun({ ...base, text: rest.slice(0, i) }));
    const j = rest.indexOf(CLOSE[k], i + 2);
    out.push(...mathRuns(rest.slice(i + 2, j).trim(), base));
    rest = rest.slice(j + 2);
  }
  return out;
}
function stripTags(s) { let o = '', t = false; for (const c of s) { if (c === '<') t = true; else if (c === '>') t = false; else if (!t) o += c; } return o.split('&nbsp;').join(' ').split('&lt;').join('<').split('&gt;').join('>').split('&quot;').join('"').split('&#39;').join("'").split('&amp;').join('&'); }
function runsFromHtml(h, base = {}) {
  const out = [];
  h.split('<strong>').forEach((p, i) => {
    if (i === 0) { out.push(...plainWithMath(stripTags(p), base)); return; }
    const k = p.indexOf('</strong>');
    out.push(...plainWithMath(stripTags(p.slice(0, k)), { ...base, bold: true }), ...plainWithMath(stripTags(p.slice(k + 9)), base));
  });
  return out;
}
const SZ = 28; // 14 pt body for on-screen narration
const para = (children, opts = {}) => new Paragraph({ spacing: { before: 80, after: 120, line: 300 }, ...opts, children });
const strip = (h) => stripTags(h).split(BS + '(').join('').split(BS + ')').join('').split(BS + '[').join('').split(BS + ']').join('').split(String.fromCharCode(10)).join(' ').trim();

function figure(it) {
  const png = fs.readFileSync(`${__dirname}/${it.id}.png`);
  // Fit the picture inside 500 x 330 px (Word points) keeping its true proportions, whatever the outcome's figures look like.
  const pw = png.readUInt32BE(16), ph = png.readUInt32BE(20);   // width and height stored in the PNG header
  const maxH = (it.choices && it.choices.length >= 3) ? 260 : 330;   // leave room on the page for the list of choices
  const scale = Math.min(500 / pw, maxH / ph);
  const w = Math.round(pw * scale), h = Math.round(ph * scale);
  const cap = stripTags(it.figcaption || '');
  const dataTex = (cap.startsWith('Plotted data') ? cap.slice(cap.indexOf(':') + 1) : cap).trim();
  const data = strip(dataTex);
  return [
    new Paragraph({
      spacing: { before: 60, after: 60 },
      children: [new ImageRun({
        type: 'png', data: png, transformation: { width: w, height: h },
        altText: { title: it.svg_title, name: it.id, description: `${it.svg_title}. Plotted data: ${data}` }
      })]
    }),
    para([new TextRun({ text: 'Plotted data: ', bold: true, size: 22 }), ...runsFromHtml(dataTex, { size: 22 })])
  ];
}

function dataTable(it, n) {
  const rows = it.table_rows;
  const cols = rows[0].length;
  const first = 1100, rest = Math.floor((9000 - first) / (cols - 1));
  const widths = [first, ...Array(cols - 1).fill(rest)];
  const border = { style: BorderStyle.SINGLE, size: 6, color: '555555' };
  const borders = { top: border, bottom: border, left: border, right: border };
  return [
    para([new TextRun({ text: `Table ${n}. `, bold: true }), new TextRun({ text: it.table_caption || 'Values of x and y' })], { keepNext: true }),
    new Table({
      width: { size: widths.reduce((a, b) => a + b), type: WidthType.DXA }, columnWidths: widths,
      rows: rows.map((r, ri) => new TableRow({
        children: r.map((c, ci) => { const head = it.table_headers === 'row' ? ri === 0 : ci === 0;   // shade and bold the header cells
          return new TableCell({
          borders, width: { size: widths[ci], type: WidthType.DXA },
          shading: head ? { fill: 'E6F4F4', type: ShadingType.CLEAR } : undefined,
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: c.trim(), bold: head, size: SZ })] })]
        }); })
      }))
    })
  ];
}

function mathBlock(it) {
  const isDisplay = it.math.startsWith(BS + '[');
  const BEGIN = BS + 'begin{aligned}', END = BS + 'end{aligned}';
  if (isDisplay && it.math.includes(BEGIN)) {   // stacked lines (student work): one centered line per row
    const body = it.math.slice(it.math.indexOf(BEGIN) + BEGIN.length, it.math.indexOf(END)).split('&amp;').join('').split('&').join('');
    const rows = body.split(BS + BS).map((r) => r.trim()).filter(Boolean);
    return rows.map((r, n) => para(mathRuns(r, { size: 40 }), { alignment: AlignmentType.CENTER, spacing: { before: n ? 40 : 200, after: n === rows.length - 1 ? 200 : 40 } }));
  }
  return [para(plainWithMath(it.math, { size: isDisplay ? 40 : SZ }), { alignment: isDisplay ? AlignmentType.CENTER : AlignmentType.LEFT, spacing: { before: 200, after: 200 } })];
}

let tableNo = 0;
const children = [];
// ---- title page content ----
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 0, after: 160 }, children: [new TextRun({ text: DOC_TITLE })] }));
children.push(para([new TextRun({ text: `Recording companion for the ${CODE} CheckIt support video — Math 172, Santa Ana College`, size: 26 })]));
children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun('How to use this document')] }));
['Each worked example is on its own page, in the same order as the Try It tabs in the interactive explainer, with the same numbers.',
 'The right-hand third of every page is intentionally blank. It is space for handwriting or ink notation while you narrate (for example, after inserting this PDF as a printout in OneNote).',
 'Say it at the start of the video: your CheckIt problem will have different numbers than the examples here. The reasoning is what transfers.']
  .forEach((t) => children.push(new Paragraph({ numbering: { reference: 'bullets', level: 0 }, spacing: { before: 60, after: 100, line: 300 }, children: [new TextRun({ text: t })] })));
children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun('The one question behind every example')] }));
children.push(para([new TextRun({ text: meta.coreQuestion + ' ', bold: true }), new TextRun(meta.coreFollowup)]));

// ---- one example per page ----
items.forEach((it, idx) => {
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, pageBreakBefore: true, children: [new TextRun(`Example ${idx + 1}: ${it.title}`)] }));
  if (it.has_svg) children.push(...figure(it));
  if (it.table_rows) { tableNo += 1; children.push(...dataTable(it, tableNo)); }
  if (it.math) children.push(...mathBlock(it));
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, children: [new TextRun('Question')] }));
  children.push(para(runsFromHtml(it.prompt)));
  if (it.choices && it.choices.length >= 3) {   // list the answer choices (A, B, C ...) when there are more than a yes/no pair
    it.choices.forEach((c, k) => children.push(new Paragraph({ spacing: { before: 20, after: 40 }, indent: { left: 360 }, children: [new TextRun({ text: String.fromCharCode(65 + k) + '.  ', bold: true }), ...plainWithMath(c, {})] })));
  }
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, children: [new TextRun('Answer and reasoning')] }));
  children.push(para(runsFromHtml(it.explanation)));
});

const doc = new Document({
  creator: 'Dr. Marty Romero (drafted with Claude, Anthropic)',
  title: DOC_TITLE,
  description: 'Worked-example pages for recording the FN1 CheckIt support video. Right third of each page is blank for annotation.',
  styles: {
    default: { document: { run: { font: 'Arial', size: SZ, color: '1A1A1A', language: { value: 'en-US' } } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 40, bold: true, font: 'Arial', color: NAV },
        paragraph: { spacing: { before: 0, after: 160 }, outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: '1A6B6B', space: 4 } } } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 34, bold: true, font: 'Arial', color: NAV },
        paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 1, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: NAV, space: 1 } } } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 28, bold: true, font: 'Arial', color: '1A6B6B' },
        paragraph: { spacing: { before: 200, after: 60 }, outlineLevel: 2 } }
    ]
  },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE }, margin: { top: M_TB, bottom: M_TB, left: M_LEFT, right: M_RIGHT, header: 360, footer: 360 } } },
    headers: { default: new Header({ children: [new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: W }], border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA', space: 2 } }, children: [new TextRun({ text: `${CODE} Worked Examples`, bold: true, size: 20, color: NAV }), new TextRun({ text: TAB }), new TextRun({ text: 'Math 172 — Santa Ana College', size: 20, color: '444444' })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: W }], children: [new TextRun({ text: 'Adapted from TBIL Precalculus (Clontz & Lewis), CC BY-NC-SA 4.0. Drafted with Claude (Anthropic); reviewed by Dr. Marty Romero.', size: 16, color: '444444' }), new TextRun({ text: TAB + 'Page ', size: 16, color: '444444' }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: '444444' })] })] }) },
    children
  }]
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(`${__dirname}/${CODE}_worked_examples.docx`, b); console.log('wrote docx'); });
