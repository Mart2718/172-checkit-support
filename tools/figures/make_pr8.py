"""PR8 figures: number lines (open or closed dots, shaded pieces with arrows, test points) and one parabola.
Run: python3 tools/figures/make_pr8.py"""
import math, os
TEAL, BLUE, ORANGE, INK, GRAY = '#1a6b6b', '#1f4e9c', '#a84d16', '#1a1a2e', '#6b6b6b'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'PR8')
os.makedirs(OUT, exist_ok=True)
M = '−'


def num(v):
    return str(v).replace('-', M)


def numberline(name, x0, x1, points=(), shade=(), tests=(), step=1):
    """points: (x, label, closed). shade: (a, b) with None for an infinite end. tests: (x, label) small dots below."""
    W, H, L, R = 400, (160 if tests else 110), 24, 24
    y = 62
    sx = lambda x: L + (x - x0) / (x1 - x0) * (W - L - R)
    o = [f'<svg viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif" font-size="20">']
    o.append(f'<line x1="{L-14}" y1="{y}" x2="{W-R+14}" y2="{y}" stroke="{GRAY}" stroke-width="2"/>')
    o.append(f'<path d="M{L-14},{y} l10,-6 v12 z M{W-R+14},{y} l-10,-6 v12 z" fill="{GRAY}"/>')
    i = math.ceil(x0 / step) * step
    while i <= x1 + 1e-9:
        o.append(f'<line x1="{sx(i):.1f}" y1="{y-7}" x2="{sx(i):.1f}" y2="{y+7}" stroke="{GRAY}" stroke-width="1.5"/>')
        o.append(f'<text x="{sx(i):.1f}" y="{y+30}" text-anchor="middle" fill="#333">{num(i)}</text>')
        i += step
    for a, b in shade:
        xa = sx(a) if a is not None else L - 12
        xb = sx(b) if b is not None else W - R + 12
        o.append(f'<line x1="{xa:.1f}" y1="{y}" x2="{xb:.1f}" y2="{y}" stroke="{TEAL}" stroke-width="7" stroke-linecap="butt"/>')
        if a is None: o.append(f'<path d="M{xa-6:.1f},{y} l14,-10 v20 z" fill="{TEAL}"/>')
        if b is None: o.append(f'<path d="M{xb+6:.1f},{y} l-14,-10 v20 z" fill="{TEAL}"/>')
    for x, lab in tests:
        o.append(f'<circle cx="{sx(x):.1f}" cy="{y}" r="4.5" fill="{BLUE}"/>')
        o.append(f'<path d="M{sx(x):.1f},{y+40} l-6,10 h12 z" fill="{BLUE}"/>')
        o.append(f'<text x="{sx(x):.1f}" y="{y+72}" text-anchor="middle" fill="{BLUE}" font-weight="bold">{lab}</text>')
    for x, lab, closed in points:
        o.append(f'<circle cx="{sx(x):.1f}" cy="{y}" r="8" fill="{INK if closed else "#fff"}" stroke="{INK}" stroke-width="3"/>')
        if lab: o.append(f'<text x="{sx(x):.1f}" y="{y-18}" text-anchor="middle" fill="{INK}" font-weight="bold">{lab}</text>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


def parabola(name, f, x0, x1, y0, y1, ystep, dots=()):
    W, H, L, T, R, B = 400, 300, 50, 12, 14, 34
    pw, ph = W - L - R, H - T - B
    sx = lambda x: L + (x - x0) / (x1 - x0) * pw
    sy = lambda y: T + (y1 - y) / (y1 - y0) * ph
    o = [f'<svg viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif" font-size="21">',
         f'<rect x="{L}" y="{T}" width="{pw}" height="{ph}" fill="#fcfcfc"/>', '<g stroke="#e0e0e0" stroke-width="1">']
    for i in range(math.ceil(x0), math.floor(x1) + 1): o.append(f'<line x1="{sx(i):.1f}" y1="{T}" x2="{sx(i):.1f}" y2="{T+ph}"/>')
    j = math.ceil(y0 / ystep) * ystep
    while j <= y1:
        o.append(f'<line x1="{L}" y1="{sy(j):.1f}" x2="{L+pw}" y2="{sy(j):.1f}"/>'); j += ystep
    o.append('</g>')
    o.append(f'<g stroke="{GRAY}" stroke-width="1.5"><line x1="{L}" y1="{sy(0):.1f}" x2="{L+pw}" y2="{sy(0):.1f}"/>'
             f'<line x1="{sx(0):.1f}" y1="{T}" x2="{sx(0):.1f}" y2="{T+ph}"/></g>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(math.ceil(x0), math.floor(x1) + 1):
        if i and i % 2 == 0: o.append(f'<text x="{sx(i):.1f}" y="{T+ph+25}">{num(i)}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    j = math.ceil(y0 / ystep) * ystep
    while j <= y1:
        if j: o.append(f'<text x="{L-6}" y="{sy(j)+7:.1f}">{num(j)}</text>')
        j += ystep
    o.append('</g>')
    o.append(f'<text x="{L+pw-4}" y="{sy(0)-8:.1f}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    o.append(f'<text x="{sx(0)-10:.1f}" y="{T+20}" text-anchor="end" fill="#333" font-style="italic">y</text>')
    xs = [x0 + (x1 - x0) * k / 400 for k in range(401)]
    o.append(f'<clipPath id="c{name[:-4]}"><rect x="{L}" y="{T}" width="{pw}" height="{ph}"/></clipPath>')
    pts = ' '.join(f'{sx(x):.1f},{sy(max(min(f(x), y1 + 30), y0 - 30)):.1f}' for x in xs)
    o.append(f'<polyline clip-path="url(#c{name[:-4]})" points="{pts}" fill="none" stroke="{TEAL}" stroke-width="3.5"/>')
    for (x, y, lab, anc, dx, dy) in dots:
        o.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="6" fill="{INK}" stroke="#fff" stroke-width="1.5"/>')
        o.append(f'<text x="{sx(x)+dx:.1f}" y="{sy(y)+dy:.1f}" text-anchor="{anc}" fill="{INK}" paint-order="stroke" stroke="#fff" stroke-width="5">{lab}</text>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


# Test the Intervals 1: boundary points -2/3 and 1/2 with test points -1, 0, 1 (for 6x^2 + x - 2 <= 0)
numberline('ti1.svg', -2, 2, points=[(-2/3, M + '2/3', True), (1/2, '1/2', True)],
           tests=[(-1, 'test'), (0, 'test'), (1, 'test')])
# Test the Intervals 2: the parabola y = (x - 3)(x + 5)
parabola('ti2.svg', lambda x: (x - 3) * (x + 5), -8, 6, -20, 20, 5,
         dots=[(-5, 0, '(' + M + '5, 0)', 'end', -8, 26), (3, 0, '(3, 0)', 'start', 8, 26)])
# Write the Answer 1: open dots at -4 and 5/2, shaded outward
numberline('wa1.svg', -5, 5, points=[(-4, '', False), (2.5, '5/2', False)], shade=[(None, -4), (2.5, None)])
# Spot the Slip 2: a student's number line for x^2 - x - 12 >= 0: closed dots at -3 and 4, shaded between
numberline('sl2.svg', -5, 6, points=[(-3, '', True), (4, '', True)], shade=[(-3, 4)])
print('wrote', sorted(os.listdir(OUT)))
