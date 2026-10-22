"""FN4 figures: CheckIt's three parent shapes on [-2, 2] (semicircle, parabola piece, tent), alone or with a
transformed copy. The parent is drawn dashed in gray when both appear; key points are dots, labeled where asked.
Run: python3 tools/figures/make_fn4.py"""
import math, os
TEAL, BLUE, ORANGE, GRAY, INK = '#1a6b6b', '#1f4e9c', '#a84d16', '#6b6b6b', '#1a1a2e'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'FN4')
os.makedirs(OUT, exist_ok=True)

SHAPES = {
    'semi': lambda x: math.sqrt(max(4 - x * x, 0)),
    'para': lambda x: 4 - x * x,
    'tent': lambda x: 4 - abs(x),
}
KEY = {'semi': [-2, 0, 2], 'para': [-2, 0, 2], 'tent': [-2, 0, 2]}


def fmt(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def make(shape, sign=1, b=0, c=0, flip=False):
    """g(x) = (+/-) [sign * f(x + b)] + c, as CheckIt builds it: shift, reflect, then vertical shift."""
    f = SHAPES[shape]
    base = lambda x: sign * f(x)
    g = lambda x: (-1 if flip else 1) * base(x + b) + c
    dom = (-2 - b, 2 - b)
    keys = [(k - b, g(k - b)) for k in KEY[shape]]
    return base, g, dom, keys


def draw(name, curves, xr=(-8, 8), yr=(-8, 8), cell=19):
    """curves: list of dicts {f, dom, style ('parent'|'main'|'ghost'), pts: [(x, y, label or None, anchor, dx, dy)]}"""
    x0, x1 = xr; y0, y1 = yr
    L, T, R, B = 34, 12, 14, 30
    W = (x1 - x0) * cell; H = (y1 - y0) * cell
    sx = lambda x: L + (x - x0) * cell
    sy = lambda y: T + (y1 - y) * cell
    o = [f'<svg viewBox="0 0 {W+L+R} {H+T+B}" font-family="Arial, Helvetica, sans-serif" font-size="18">',
         f'<rect x="{L}" y="{T}" width="{W}" height="{H}" fill="#fcfcfc"/>', '<g stroke="#e0e0e0" stroke-width="1">']
    for i in range(x0, x1 + 1): o.append(f'<line x1="{fmt(sx(i))}" y1="{T}" x2="{fmt(sx(i))}" y2="{T+H}"/>')
    for j in range(y0, y1 + 1): o.append(f'<line x1="{L}" y1="{fmt(sy(j))}" x2="{L+W}" y2="{fmt(sy(j))}"/>')
    o.append('</g><g stroke="#6b6b6b" stroke-width="1.5">'
             f'<line x1="{L}" y1="{fmt(sy(0))}" x2="{L+W}" y2="{fmt(sy(0))}"/><line x1="{fmt(sx(0))}" y1="{T}" x2="{fmt(sx(0))}" y2="{T+H}"/></g>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(x0, x1 + 1, 2):
        if i: o.append(f'<text x="{fmt(sx(i))}" y="{T+H+20}">{str(i).replace("-", "−")}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    for j in range(y0, y1 + 1, 2):
        if j: o.append(f'<text x="{L-4}" y="{fmt(sy(j)+6)}">{str(j).replace("-", "−")}</text>')
    o.append('</g>')
    o.append(f'<text x="{L+W-4}" y="{fmt(sy(0)-6)}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    o.append(f'<text x="{fmt(sx(0)+6)}" y="{T+14}" fill="#333" font-style="italic">y</text>')
    for cv in curves:
        a, b = cv['dom']; n = 300
        pts = [(a + (b - a) * k / n) for k in range(n + 1)]
        poly = ' '.join(f'{fmt(sx(x))},{fmt(sy(cv["f"](x)))}' for x in pts)
        if cv['style'] == 'parent':
            o.append(f'<polyline points="{poly}" fill="none" stroke="{GRAY}" stroke-width="2.5" stroke-dasharray="7 5"/>')
        else:
            o.append(f'<polyline points="{poly}" fill="none" stroke="{TEAL}" stroke-width="3.5" stroke-linejoin="round"/>')
        for (x, y, lab, anc, dx, dy) in cv.get('pts', []):
            col = GRAY if cv['style'] == 'parent' else BLUE
            o.append(f'<circle cx="{fmt(sx(x))}" cy="{fmt(sy(y))}" r="5" fill="{col}" stroke="#fff" stroke-width="1.5"/>')
            if lab:
                o.append(f'<text x="{fmt(sx(x)+dx)}" y="{fmt(sy(y)+dy)}" text-anchor="{anc}" fill="{INK}" font-size="19" paint-order="stroke" stroke="#fff" stroke-width="4">{lab}</text>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


def coord(x, y):
    return f'({fmt(x)}, {fmt(y)})'.replace('-', '−')


def parent_only(name, shape, sign=1):
    base, _, _, _ = make(shape, sign)
    k = [(x, base(x)) for x in KEY[shape]]
    lab = [(k[0][0], k[0][1], coord(*k[0]), 'end', -8, 18 if sign > 0 else -8),
           (k[1][0], k[1][1], coord(*k[1]), 'start', 8, -8 if sign > 0 else 18),
           (k[2][0], k[2][1], coord(*k[2]), 'start', 8, 18 if sign > 0 else -8)]
    draw(name, [{'f': base, 'dom': (-2, 2), 'style': 'main', 'pts': lab}])


def overlay(name, shape, sign, b, c, flip, label_g=True, nudge=None):
    base, g, dom, keys = make(shape, sign, b, c, flip)
    parent = {'f': base, 'dom': (-2, 2), 'style': 'parent', 'pts': [(x, base(x), None, 'start', 0, 0) for x in KEY[shape]]}
    up = (g(dom[0] + 2) > keys[0][1])            # is the middle point above the ends?
    lab = []
    for i, (x, y) in enumerate(keys):
        if i == 1: lab.append((x, y, coord(x, y) if label_g else None, 'middle', 0, -12 if up else 24))
        else: lab.append((x, y, coord(x, y) if label_g else None, 'end' if i == 0 else 'start', -8 if i == 0 else 8, 20 if up else -8))
    for i, (x, y, t, anc, dx, dy) in enumerate(lab):            # keep labels inside the frame
        if anc == 'start' and x >= 5.5: lab[i] = (x, y, t, 'end', -10, dy)
        if anc == 'end' and x <= -5.5: lab[i] = (x, y, t, 'start', 10, dy)
    for i, v in (nudge or {}).items(): lab[i] = lab[i][:3] + v
    draw(name, [parent, {'f': g, 'dom': dom, 'style': 'main', 'pts': lab}])


# Track the points: parent graphs with labeled key points
parent_only('tp1.svg', 'para')
parent_only('tp2.svg', 'semi')
parent_only('tp3.svg', 'tent')
parent_only('tp4.svg', 'para', -1)
# Match the graph: parent dashed, g solid with labeled key points
overlay('mg1.svg', 'para', 1, 3, -2, False)
overlay('mg2.svg', 'semi', 1, -2, 1, True, nudge={0: ('end', -10, 6)})
overlay('mg3.svg', 'tent', 1, 1, 2, True)
overlay('mg4.svg', 'para', -1, -5, 3, False)
print('wrote', sorted(os.listdir(OUT)))
