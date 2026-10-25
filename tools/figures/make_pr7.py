"""PR7 figures: graphs of rational functions with dashed asymptotes, an open circle for the hole, and labeled intercepts.
Run: python3 tools/figures/make_pr7.py"""
import math, os
TEAL, BLUE, ORANGE, INK, GRAY = '#1a6b6b', '#1f4e9c', '#a84d16', '#1a1a2e', '#6b6b6b'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'PR7')
os.makedirs(OUT, exist_ok=True)
M = '−'


def num(v):
    return str(v).replace('-', M)


def plot(name, curves, x0, x1, y0, y1, xstep=1, ystep=2, asym=(), hline=None, holes=(), dots=(), gy=1, hasym=None):
    """curves: list of functions; drawn in pieces split at the vertical asymptotes."""
    W, H, L, T, R, B = 400, 320, 46, 12, 14, 34
    pw, ph = W - L - R, H - T - B
    sx = lambda x: L + (x - x0) / (x1 - x0) * pw
    sy = lambda y: T + (y1 - y) / (y1 - y0) * ph
    o = [f'<svg viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif" font-size="21">',
         f'<rect x="{L}" y="{T}" width="{pw}" height="{ph}" fill="#fcfcfc"/>', '<g stroke="#e0e0e0" stroke-width="1">']
    for i in range(math.ceil(x0), math.floor(x1) + 1): o.append(f'<line x1="{sx(i):.1f}" y1="{T}" x2="{sx(i):.1f}" y2="{T+ph}"/>')
    for j in range(math.ceil(y0 / gy) * gy, math.floor(y1) + 1, gy): o.append(f'<line x1="{L}" y1="{sy(j):.1f}" x2="{L+pw}" y2="{sy(j):.1f}"/>')
    o.append('</g>')
    o.append(f'<g stroke="{GRAY}" stroke-width="1.5"><line x1="{L}" y1="{sy(0):.1f}" x2="{L+pw}" y2="{sy(0):.1f}"/>'
             f'<line x1="{sx(0):.1f}" y1="{T}" x2="{sx(0):.1f}" y2="{T+ph}"/></g>')
    o.append('<g fill="#333" text-anchor="middle">')
    i = math.ceil(x0 / xstep) * xstep
    while i <= x1:
        if i: o.append(f'<text x="{sx(i):.1f}" y="{T+ph+25}">{num(i)}</text>')
        i += xstep
    o.append('</g><g fill="#333" text-anchor="end">')
    j = math.ceil(y0 / ystep) * ystep
    while j <= y1:
        if j: o.append(f'<text x="{L-6}" y="{sy(j)+7:.1f}">{num(j)}</text>')
        j += ystep
    o.append('</g>')
    o.append(f'<text x="{L+pw-4}" y="{sy(0)-8:.1f}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    o.append(f'<text x="{sx(0)+8:.1f}" y="{T+20}" fill="#333" font-style="italic">y</text>')
    for a in asym:
        o.append(f'<line x1="{sx(a):.1f}" y1="{T}" x2="{sx(a):.1f}" y2="{T+ph}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="8 6"/>')
    if hasym is not None:
        o.append(f'<line x1="{L}" y1="{sy(hasym):.1f}" x2="{L+pw}" y2="{sy(hasym):.1f}" stroke="{BLUE}" stroke-width="2" stroke-dasharray="8 6"/>')
    if hline is not None:
        o.append(f'<line x1="{L}" y1="{sy(hline):.1f}" x2="{L+pw}" y2="{sy(hline):.1f}" stroke="{BLUE}" stroke-width="3"/>')
    o.append(f'<clipPath id="c{name[:-4]}"><rect x="{L}" y="{T}" width="{pw}" height="{ph}"/></clipPath>')
    cuts = sorted([x0] + list(asym) + [x1])
    for f in curves:
        for a, b in zip(cuts, cuts[1:]):
            lo, hi = a + 1e-3, b - 1e-3
            xs = [lo + (hi - lo) * k / 500 for k in range(501)]
            pts = ' '.join(f'{sx(x):.1f},{sy(max(min(f(x), y1 + 30), y0 - 30)):.1f}' for x in xs)
            o.append(f'<polyline clip-path="url(#c{name[:-4]})" points="{pts}" fill="none" stroke="{TEAL}" stroke-width="3.5" stroke-linejoin="round"/>')
    for (x, y, lab, anc, dx, dy) in dots:
        o.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="6" fill="{INK}" stroke="#fff" stroke-width="1.5"/>')
        if lab: o.append(f'<text x="{sx(x)+dx:.1f}" y="{sy(y)+dy:.1f}" text-anchor="{anc}" fill="{INK}" paint-order="stroke" stroke="#fff" stroke-width="5">{lab}</text>')
    for (x, y, lab, anc, dx, dy) in holes:
        o.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="7" fill="#fff" stroke="{TEAL}" stroke-width="3"/>')
        if lab: o.append(f'<text x="{sx(x)+dx:.1f}" y="{sy(y)+dy:.1f}" text-anchor="{anc}" fill="{INK}" paint-order="stroke" stroke="#fff" stroke-width="5">{lab}</text>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


# Sketch 1: f(x) = 2(x - 3)(x + 1)/((x + 1)(x - 1)) = 2(x - 3)/(x - 1) with a hole at (-1, 4)
plot('sk1.svg', [lambda x: 2 * (x - 3) / (x - 1)], -6, 8, -8, 10, xstep=2, ystep=2, gy=2, asym=[1], hasym=2,
     holes=[(-1, 4, '(' + M + '1, 4)', 'end', -12, -8)],
     dots=[(3, 0, '(3, 0)', 'start', 8, 24), (0, 6, '(0, 6)', 'start', 10, -6)])
# Sketch 3: f(x) = (x + 2)^2 (x - 1)/(2(x - 1)(x - 3)) = (x + 2)^2/(2(x - 3)) with a hole at (1, -9/4); no horizontal asymptote
plot('sk3.svg', [lambda x: (x + 2) ** 2 / (2 * (x - 3))], -6, 9, -10, 20, xstep=2, ystep=5, gy=5, asym=[3],
     holes=[(1, -2.25, '(1, ' + M + '9/4)', 'start', 12, 28)],
     dots=[(-2, 0, '(' + M + '2, 0)', 'end', -8, -10), (0, -2 / 3, '(0, ' + M + '2/3)', 'end', -10, 28)])
print('wrote', sorted(os.listdir(OUT)))
