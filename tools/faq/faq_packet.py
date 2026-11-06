"""Turn an FAQ repo's <code>-data.json into a Markdown review packet (for the independent audit and for ChatGPT).
Usage: python3 faq_packet.py /path/to/repo [out.md]"""
import json, re, sys, glob, os
repo = sys.argv[1]
data_file = next(iter(sorted(glob.glob(os.path.join(repo, '*-data.json')) + glob.glob(os.path.join(repo, '*data*.json')))))
d = json.load(open(data_file, encoding='utf-8'))
graphs = {}
for p in d.get('paths', []):
    graphs.update(p.get('graphs', {}))
def svg_labels(html):
    """Every graph's own description (a graph entry can hold several SVGs, e.g. panels (a), (b), (c))."""
    labs = [m.group(1) for m in re.finditer(r'<svg\b[^>]*?\baria-label="([^"]*)"', html)]
    if not labs and '<svg' in html:
        m = re.search(r'aria-label="([^"]*)"', html)
        labs = [m.group(1)] if m else ['NO TEXT DESCRIPTION']
    return labs
def graph_text(gid):
    labs = svg_labels(graphs.get(gid, '')) or ['NO TEXT DESCRIPTION']
    if len(labs) == 1: return f"[Graph {gid}: {labs[0]}]"
    return f"[Graph {gid}: " + ' | '.join(f"panel {i+1}: {l}" for i, l in enumerate(labs)) + ']'
def table_text(m):
    rows = []
    for r in re.findall(r'<tr\b.*?</tr>', m.group(0), flags=re.S):
        cells = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<t[hd]\b[^>]*>(.*?)</t[hd]>', r, flags=re.S)]
        rows.append('| ' + ' | '.join(cells) + ' |')
    return '\n\n' + '\n'.join(rows) + '\n\n' if rows else ' '
def clean(t):
    if not isinstance(t, str): return str(t)
    t = re.sub(r'\[\[graph:([^\]]+)\]\]', lambda m: ' ' + graph_text(m.group(1)), t)
    t = re.sub(r'<svg\b.*?</svg>', lambda m: ' [Graph: ' + svg_labels(m.group(0))[0] + '] ', t, flags=re.S)
    t = re.sub(r'<table\b.*?</table>', table_text, t, flags=re.S)
    t = re.sub(r'</?(div|p|br|li|ul|ol|h[1-6])\b[^<>]*>', ' ', t)
    t = re.sub(r'</?[a-zA-Z][^<>]*>', '', t)
    t = re.sub(r'[ \t]{2,}', ' ', t)
    return t.replace('\\(', '$').replace('\\)', '$').replace('\\[', '$$').replace('\\]', '$$')
o = [f"# {d.get('section','')} FAQ and guided learning: math review packet", '',
     f"Learning objective: {d.get('learningObjective','')}", '',
     'Please check the mathematics: every answer, solution, worked step and graph description. Flag anything wrong, ambiguous or misleading.', '']
o += ['## FAQs', '']
for f in d.get('faqs', []):
    o += [f"### {f['id']} ({f.get('category','')})", f"**Q:** {clean(f['question'])}", '', f"**A:** {clean(f['answer'])}", '']
for p in d.get('paths', []):
    o += [f"## Guided path: {p.get('label','')}", '', clean(p.get('intro', '')), '']
    for st in p.get('stages', []):
        o += [f"### Stage {st.get('stage','')}: {clean(st.get('desc',''))}", '']
        for s in st.get('stops', []):
            o += [f"#### {s['id']}: {s.get('title','')}", f"*Target:* {clean(s.get('target',''))}", '']
            for key, lab in [('cold','Try first'),('coldA','Answer'),('solution','Solution'),('mistake','Common mistake'),('again','Try again'),('againA','Answer'),('stretch','Stretch'),('stretchA','Answer'),('reflect','Reflect'),('note','Student note to AI')]:
                if s.get(key): o += [f"- **{lab}:** {clean(s[key])}"]
            o += ['']
o += ['## Videos', ''] + [f"- {v['id']}: {v['title']} ({v['url']}): {clean(v.get('description',''))}" for v in d.get('videos', [])] + ['']
o += ['## Apps', ''] + [f"- {a['id']}: {a['title']} ({a['url']}): {clean(a.get('description',''))}" for a in d.get('apps', [])] + ['']
o += ['## AI prompts', '']
for kind, lst in (d.get('prompts') or {}).items():
    for pr in lst: o += [f"### {pr['id']} ({kind}): {pr.get('title','')}", clean(pr.get('prompt','')), '']
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(repo, 'review_packet.md')
open(out, 'w', encoding='utf-8').write('\n'.join(o) + '\n')
used = set(re.findall(r'\[\[graph:([^\]]+)\]\]', json.dumps(d)))
print('wrote', out, '| graphs:', len(graphs), '| referenced but missing:', sorted(used - set(graphs)), '| defined but unused:', sorted(set(graphs) - used))
