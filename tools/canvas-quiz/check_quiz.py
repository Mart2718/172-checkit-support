#!/usr/bin/env python3
"""Sanity-check a generated Canvas quiz package: usage  python3 tools/canvas-quiz/check_quiz.py CODE"""
import glob, html, re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[2]
code = sys.argv[1].upper()
z = zipfile.ZipFile(ROOT / 'derived' / code / 'canvas' / f'{code}_canvas_quiz.zip')
names = z.namelist()
ok = True
def chk(label, cond):
    global ok
    print(('PASS ' if cond else 'FAIL ') + label); ok &= bool(cond)
for n in names:
    if n.endswith('.xml'):
        ET.fromstring(z.read(n))
chk('all XML files are well-formed', True)
a = [n for n in names if re.search(r'text2qti_assessment_[0-9a-f]+/text2qti_assessment_[0-9a-f]+\.xml$', n)][0]
x = z.read(a).decode('utf-8')
cont = yaml.safe_load(open(ROOT / 'content' / f'{code}.yml', encoding='utf-8'))
items = [it for t in cont['tabs'] for it in t['items']]
root = ET.fromstring(x.encode())
ns = {'q': 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2'}
qitems = root.findall('.//q:item', ns)
chk(f'{len(items)} items in the content file = {len(qitems)} questions in the package', len(items) == len(qitems))
for it, q in zip(items, qitems):
    labels = [r.find('.//q:mattext', ns).text for r in q.findall('.//q:response_label', ns)]
    corr = q.find('.//q:respcondition[@title="correct"]//q:varequal', ns) if q.find('.//q:respcondition[@title="correct"]', ns) is not None else None
    cid = None
    for rc in q.findall('.//q:respcondition', ns):
        v = rc.find('.//q:conditionvar/q:varequal', ns)
        sc = rc.find('.//q:setvar', ns)
        if v is not None and sc is not None and sc.text and float(sc.text) > 0:
            cid = v.text
    rl = [r.get('ident') for r in q.findall('.//q:response_label', ns)]
    right = rl.index(cid) if cid in rl else -1
    exp = [ch['value'] for ch in it['choices']].index(it['correct'])
    chk(f'{it["id"]}: {len(rl)} choices, correct answer is choice {"abcdefgh"[right]} (content file says {"abcdefgh"[exp]})', right == exp and len(rl) == len(it['choices']))
    chk(f'{it["id"]}: has correct and incorrect feedback', 'correct_fb' in ET.tostring(q, encoding='unicode') and 'general_incorrect_fb' in ET.tostring(q, encoding='unicode'))
imgs = set(re.findall(r'%24IMS-CC-FILEBASE%24/([^"&]+)', x))
for i in imgs:
    chk(f'image {i} is inside the zip', i in names)
chk('no equation image left with raw LaTeX alt text', 'alt="LaTeX:' not in x)
chk('every image has alt text', not re.search(r'<img(?![^>]*alt=)', html.unescape(x)))
meta = z.read([n for n in names if n.endswith('assessment_meta.xml')][0]).decode()
chk('unlimited attempts, keep highest', '<allowed_attempts>-1</allowed_attempts>' in meta and 'keep_highest' in meta)
print('ALL PASS' if ok else 'SOME FAILED'); sys.exit(0 if ok else 1)
