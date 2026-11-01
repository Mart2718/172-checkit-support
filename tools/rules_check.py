"""Checks the item-writing rules in BUILD_RULES.md that can be checked from the content file alone.
Usage: python3 tools/rules_check.py FN3 [PF3 ...]   or   python3 tools/rules_check.py --all
FAIL lines break a rule outright; WARN lines are heuristics a person should look at. Exit code 1 on any FAIL."""
import re, sys, glob, os, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NO_MISTAKE = 'There is no mistake.'
SLIP_PROMPT = 'What is the mistake, if any?'
POSITION = re.compile(r'\b(choice|option|answer)\s*\(?[a-d]\)?(?![\w-])|\b(first|second|third|fourth|last|top|bottom) (choice|option|answer|one)\b', re.I)


def plain(t):
    """Text with HTML tags, math delimiters and spacing removed, so a choice can be looked for inside the feedback."""
    t = re.sub(r'<[^>]+>', ' ', str(t))
    t = t.replace('\\(', ' ').replace('\\)', ' ').replace('−', '-').replace('\\,', '')
    t = re.sub(r'\\[dt]frac', r'\\frac', t)
    t = re.sub(r'\b(about|Side|side)\b|≈|°|\^\\circ|\.$', '', t.strip())
    return re.sub(r'\s+', '', t)


NUM = re.compile(r'-?\d+(?:\.\d+)?')


def named(label, expl_raw):
    """True if the feedback mentions this distractor: every number in it, or else its whole math form."""
    nums = NUM.findall(str(label).replace('−', '-'))
    expl_nums = set(NUM.findall(str(expl_raw).replace('−', '-')))
    expl_nums |= {n.lstrip('-') for n in expl_nums}
    if nums:
        return all(n in expl_nums or n.lstrip('-') in expl_nums for n in nums)
    return plain(label) in plain(expl_raw)


def check(code):
    c = yaml.safe_load(open(os.path.join(ROOT, 'content', f'{code}.yml'), encoding='utf-8'))
    out = []
    F = lambda m: out.append('FAIL ' + m)
    W = lambda m: out.append('WARN ' + m)
    for tab in c['tabs']:
        items = tab['items']
        keys = [it['correct'] for it in items]
        # 1. positions: a 4-item tab must not use a, b, c, d once each
        if len(items) == 4 and all(len(it['choices']) == 4 for it in items) and sorted(keys) == ['a', 'b', 'c', 'd']:
            F(f"tab '{tab['id']}': the correct answers are a, b, c, d once each ({''.join(keys)})")
        is_slip = tab['id'] == 'slip'
        nm_keys = 0
        for it in items:
            iid = it['id']
            labels = {ch['value']: ch['label'] for ch in it['choices']}
            # 2. Spot the Slip format
            if is_slip:
                first = it['choices'][0]
                if first['label'] != NO_MISTAKE:
                    F(f"{iid}: '{NO_MISTAKE}' must be choice a")
                if any(ch['label'] == NO_MISTAKE for ch in it['choices'][1:]):
                    F(f"{iid}: '{NO_MISTAKE}' appears in a position other than a")
                if not str(it['prompt']).strip().endswith(SLIP_PROMPT):
                    F(f"{iid}: the prompt must end with '{SLIP_PROMPT}'")
                if labels.get(it['correct']) == NO_MISTAKE:
                    nm_keys += 1
            # 3. feedback never refers to choices by position
            if POSITION.search(str(it['explanation'])):
                F(f"{iid}: the feedback refers to a choice by position: '{POSITION.search(str(it['explanation'])).group(0)}'")
            # 4. every distractor's origin is named: short (math or number) distractors should appear in the feedback
            for ch in it['choices']:
                if ch['value'] == it['correct'] or ch['label'] == NO_MISTAKE:
                    continue
                lab = plain(ch['label'])
                if len(lab) <= 30 and lab and not named(ch['label'], it['explanation']):
                    W(f"{iid}: distractor '{ch['label']}' does not appear in the feedback; check its origin is named")
            # 5. speak-line conventions
            for where, sp in [('math', (it.get('math') or {}).get('speak'))] + [(f"choice {ch['value']}", ch.get('speak')) for ch in it['choices']]:
                if not sp:
                    continue
                if 'the fraction' in sp and sp.count('the fraction') > sp.count('end fraction'):
                    F(f"{iid} {where}: a fraction is read without 'end fraction'")
                if re.search(r'\bover\b', sp) and 'fraction' not in sp and not re.search(r'\b(pi|π)\s+over\s+\d', sp):
                    W(f"{iid} {where}: '… over …' without the fraction convention: \"{sp[:60]}\"")
                if re.search(r'square root of [^,]*?\b(plus|minus|times)\b', sp) and sp.count('square root') > sp.count('end root'):
                    F(f"{iid} {where}: a root of a sum or difference is read without 'end root'")
        if is_slip and nm_keys != 1:
            F(f"tab 'slip': exactly one item must have '{NO_MISTAKE}' as its answer (found {nm_keys})")
    return out


codes = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, 'content', '*.yml'))) if '--all' in sys.argv else [a.upper() for a in sys.argv[1:]]
bad = 0
for code in codes:
    res = check(code)
    fails = sum(1 for r in res if r.startswith('FAIL'))
    warns = len(res) - fails
    bad += fails
    print(f"{code}: {'PASS' if not fails else str(fails) + ' rule break(s)'}{f', {warns} warning(s)' if warns else ''}")
    for r in res:
        print('  ' + r)
sys.exit(1 if bad else 0)
