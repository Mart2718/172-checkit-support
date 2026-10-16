#!/usr/bin/env python3
"""Build a Canvas quiz import package (QTI 1.2 .zip) from content/CODE.yml.

Usage:  python3 tools/canvas-quiz/make_quiz.py CODE
Needs:  pip install text2qti pyyaml   |  node  |  derived/CODE/*.png (run tools/derive.sh CODE first when the outcome has figures)
Output: derived/CODE/canvas/CODE_canvas_quiz.zip   (import it in Canvas: Settings > Import Course Content > QTI .zip file)
        derived/CODE/canvas/CODE_canvas_quiz.md    (the intermediate text, for checking)
"""
import html, json, os, re, shutil, subprocess, sys, zipfile
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
code = sys.argv[1].upper()
c = yaml.safe_load(open(ROOT / 'content' / f'{code}.yml', encoding='utf-8'))
out = ROOT / 'derived' / code / 'canvas'
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)

def tex_clean(t):
    t = t.strip().replace('\\tfrac', '\\frac').replace('\\dfrac', '\\frac')
    return t

def to_md(s):
    """Our content fields use a little HTML plus \\( \\) and \\[ \\] math. text2qti wants Markdown with $...$ math."""
    s = str(s)
    s = re.sub(r'</?span[^>]*>', '', s)
    s = re.sub(r'<strong>(.*?)</strong>', r'**\1**', s, flags=re.S)
    s = re.sub(r'<em>(.*?)</em>', r'*\1*', s, flags=re.S)
    s = re.sub(r'\\\((.*?)\\\)', lambda m: '$' + tex_clean(m.group(1)) + '$', s, flags=re.S)
    s = re.sub(r'\\\[(.*?)\\\]', lambda m: '$' + tex_clean(m.group(1)) + '$', s, flags=re.S)
    s = re.sub(r'\s*\n\s*', ' ', s).strip()
    assert '<' not in re.sub(r'\$[^$]*\$', '', s), f'unconverted HTML left in: {s}'
    return s

def label_md(v):
    return to_md('Function' if v is True else 'Not a function' if v is False else v)

def table_html(t):
    row_headers_in_first_row = t.get('headers') == 'row'
    rows = []
    for ri, r in enumerate(t['rows']):
        cells = []
        for ci, cell in enumerate(r):
            cell = html.escape(str(cell))
            if row_headers_in_first_row and ri == 0:
                cells.append(f'<th scope="col">{cell}</th>')
            elif not row_headers_in_first_row and ci == 0:
                cells.append(f'<th scope="row">{cell}</th>')
            else:
                cells.append(f'<td>{cell}</td>')
        rows.append('<tr>' + ''.join(cells) + '</tr>')
    return f'<table><caption>{html.escape(t["caption"])}</caption>' + ''.join(rows) + '</table>'

url = f'https://172checkit.netlify.app/{code.lower()}/'
lines = [
    f'Quiz title: {code} Practice with Feedback ({c["h1"].split(": ", 1)[-1]})',
    f'Quiz description: Practice questions for {code}. Pick the answer you think is right, then read the feedback after you submit. You can try as many times as you like. The same ideas, with a guess-first explainer, are at [{url}]({url}).',
    'Shuffle answers: false',
    'Show correct answers: true',
    '',
]
need_images = []
for tab in c['tabs']:
    for it in tab['items']:
        parts = []
        parts.append(to_md(it['prompt']))
        if 'figure' in it:
            f = it['figure']
            png = Path(f['file']).stem + '.png'
            src = ROOT / 'derived' / code / png
            if not src.exists():
                sys.exit(f'Missing {src}. Run: bash tools/derive.sh {code}')
            shutil.copy(src, out / png)
            alt = html.unescape(f['title']).replace('[', '(').replace(']', ')')
            parts.append(f'![{alt}]({png})')
            parts.append(to_md(f['caption']))
        if 'table' in it:
            parts.append(table_html(it['table']))
        if 'math' in it:
            m = it['math']
            if 'display' in m:
                parts.append('$' + tex_clean(m['display']) + '$')
            else:
                parts.append(', '.join('$' + tex_clean(x) + '$' for x in m['inline']))
        lines.append(f'Title: {it["title"]}')
        lines.append('Points: 1')
        lines.append('1. ' + parts[0])
        for p in parts[1:]:
            lines += ['', '   ' + p]
        lines.append('')
        expl = to_md(it['explanation'])
        lines.append("+ That’s right. " + expl)
        lines.append("- Not quite — here’s why: " + expl)
        lines.append('')
        for i, ch in enumerate(it['choices']):
            mark = '*' if ch['value'] == it['correct'] else ''
            lines.append(f'{mark}{"abcdefgh"[i]}) {label_md(ch["label"])}')
        lines.append('')
md = out / f'{code}_canvas_quiz.md'
md.write_text('\n'.join(lines), encoding='utf-8')

subprocess.run(['text2qti', md.name], cwd=out, check=True)
zpath = out / f'{code}_canvas_quiz.zip'

# Post-process: (1) equation images get a plain-words alt text instead of raw LaTeX; (2) unlimited attempts, keep highest.
zin = zipfile.ZipFile(zpath)
files = {n: zin.read(n) for n in zin.namelist()}
zin.close()
# In the QTI XML the HTML is itself entity-escaped (< and > become &lt; and &gt;), and a ">" inside TeX appears as &amp;gt;.
ALT = re.compile(r'alt="LaTeX: (.*?)"')
def raw_tex(escaped):
    return html.unescape(html.unescape(escaped))
texs = set()
for n, b in files.items():
    if n.endswith('.xml'):
        texs |= {raw_tex(x) for x in ALT.findall(b.decode('utf-8'))}
custom = {}   # readings written by hand in the content file take priority over the automatic reading
for tab in c['tabs']:
    for it in tab['items']:
        m = it.get('math') or {}
        if m.get('display') and m.get('speak'):
            custom[tex_clean(m['display'])] = m['speak']
        for ch in it['choices']:
            mm = re.fullmatch(r'\\\(\s*(.*?)\s*\\\)', str(ch['label']), flags=re.S)
            if mm and ch.get('speak'):
                custom[tex_clean(mm.group(1))] = ch['speak']
speech = json.loads(subprocess.run(['node', str(ROOT / 'tools/canvas-quiz/speak.js')], input=json.dumps(sorted(texs)).encode(), capture_output=True, check=True).stdout)
speech.update({t: sp for t, sp in custom.items() if t in speech})
for t, sp in speech.items():
    assert sp and not re.search(r'[&<>"\\\']', sp), f'unsafe or empty spoken text for {t!r}: {sp!r}'
for n in list(files):
    if not n.endswith('.xml'):
        continue
    s = files[n].decode('utf-8')
    s = ALT.sub(lambda m: 'alt="' + speech[raw_tex(m.group(1))] + '"', s)
    if n.endswith('assessment_meta.xml'):
        s = s.replace('<allowed_attempts>1</allowed_attempts>', '<allowed_attempts>-1</allowed_attempts>')
    files[n] = s.encode('utf-8')
with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
    for n, b in files.items():
        z.writestr(n, b)
print('wrote', zpath, f'({sum(len(t["items"]) for t in c["tabs"])} questions)')
