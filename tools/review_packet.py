"""Writes one plain Markdown file per outcome with every item's question, choices, marked answer and explanation,
for a math check by a person or another AI (paste it in and ask it to verify every answer and explanation).
Usage: python3 tools/review_packet.py FN3 [PF3 ...]   ->  review/FN3_math_review.md (not published; review/ is gitignored)"""
import os, re, sys, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'review')
os.makedirs(OUT, exist_ok=True)


def text(t):
    t = re.sub(r'<strong>(.*?)</strong>', r'**\1**', str(t), flags=re.S)
    t = re.sub(r'<em>(.*?)</em>', r'*\1*', t, flags=re.S)
    t = re.sub(r'</?[a-zA-Z][^<>]*>', '', t)   # only real HTML tags; a < in math (like 2<0) stays
    return t.replace('\\(', '$').replace('\\)', '$').replace('\\[', '$$').replace('\\]', '$$').strip()


for code in [a.upper() for a in sys.argv[1:]]:
    c = yaml.safe_load(open(os.path.join(ROOT, 'content', f'{code}.yml'), encoding='utf-8'))
    o = [f"# {code} math review packet", '',
         'Please check the mathematics of every item below: that the marked answer is correct, that each wrong choice',
         'is actually wrong, and that every computation and claim in the explanation is true. Report item ids with problems.',
         'Math is in LaTeX between $ signs. Figures are described in words.', '']
    s = c['summary']
    o += ['## Quick Summary', '', text(s['intro']), '']
    o += ['| ' + ' | '.join(s['columns']) + ' |', '|' + '---|' * len(s['columns'])]
    o += ['| ' + ' | '.join(text(x) for x in r) + ' |' for r in s['rows']]
    o += ['', text(s['note']), '']
    for tab in c['tabs']:
        o += [f"## {tab['label']}", '']
        for it in tab['items']:
            o += [f"### {it['id']}: {it['title']}", '']
            if it.get('figure'):
                o += [f"Figure: {text(it['figure']['caption'])}", '']
            if it.get('table'):
                o += [f"Table ({it['table']['caption']}):", ''] + ['| ' + ' | '.join(r) + ' |' for r in it['table']['rows']] + ['']
            if it.get('math'):
                o += [f"$$ {it['math']['display']} $$", '']
            o += [text(it['prompt']), '']
            for ch in it['choices']:
                mark = '  ← marked correct' if ch['value'] == it['correct'] else ''
                o.append(f"- ({ch['value']}) {text(ch['label'])}{mark}")
            o += ['', f"Explanation: {text(it['explanation'])}", '']
    path = os.path.join(OUT, f'{code}_math_review.md')
    open(path, 'w', encoding='utf-8').write('\n'.join(o) + '\n')
    print('wrote', path)
