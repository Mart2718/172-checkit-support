"""PF3 figures: inverse trig graphs with x in whole numbers and y in multiples of pi/4.
Same visual style as graph_svg.py and make_pf2.py. Run: python3 tools/figures/make_pf3.py"""
import math, os
from fractions import Fraction

TEAL, BLUE, ORANGE = '#1a6b6b', '#1f4e9c', '#a84d16'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'PF3')
PI = math.pi
F = Fraction

def fmt(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')

def pi_label(q):
    if q == 0: return '0'
    s = '−' if q < 0 else ''; q = abs(q)
    n, d = q.numerator, q.denominator
    top = 'π' if n == 1 else f'{n}π'
    return s + (top if d == 1 else f'{top}/{d}')

def num_label(v):
    return str(v).replace('-', '−')

def inv_graph(name, f, xr, xdomain, hasym, pts, xcell=70, ycell=34):
    """xr: integer (min, max); xdomain: (lo, hi) where the curve exists; hasym: list of Fractions of pi;
    pts: list of (x, y_fraction_of_pi, anchor, dx, dy, closed)."""
    x0, x1 = xr
    y0, y1 = F(-5, 4), F(5, 4)          # y window in multiples of pi
    ystep = F(1, 4)
    ny = int((y1 - y0) / ystep)
    L, T, R, B = 58, 14, 24, 30
    W = (x1 - x0) * xcell; H = ny * ycell
    sx = lambda x: L + (x - x0) * xcell
    sy = lambda q: T + float((y1 - q) / ystep) * ycell
    o = [f'<svg viewBox="0 0 {W+L+R} {H+T+B}" font-family="Arial, Helvetica, sans-serif" font-size="17">']
    o.append(f'<rect x="{L}" y="{T}" width="{W}" height="{H}" fill="#fcfcfc"/>')
    o.append('<g stroke="#e0e0e0" stroke-width="1">')
    for i in range(x0, x1 + 1): o.append(f'<line x1="{fmt(sx(i))}" y1="{T}" x2="{fmt(sx(i))}" y2="{T+H}"/>')
    for j in range(ny + 1): o.append(f'<line x1="{L}" y1="{fmt(T+j*ycell)}" x2="{L+W}" y2="{fmt(T+j*ycell)}"/>')
    o.append('</g>')
    o.append(f'<g stroke="#6b6b6b" stroke-width="1.5"><line x1="{L}" y1="{fmt(sy(F(0)))}" x2="{L+W}" y2="{fmt(sy(F(0)))}"/>'
             f'<line x1="{fmt(sx(0))}" y1="{T}" x2="{fmt(sx(0))}" y2="{T+H}"/></g>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(x0, x1 + 1):
        if i != 0: o.append(f'<text x="{fmt(sx(i))}" y="{T+H+20}">{num_label(i)}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    for j in range(ny + 1):
        q = y1 - j * ystep
        if q != 0 and q.denominator <= 2 or q in (F(1, 4), F(-1, 4)):
            if q != 0: o.append(f'<text x="{L-6}" y="{fmt(sy(q)+6)}">{pi_label(q)}</text>')
    o.append('</g>')
    o.append(f'<text x="{L+W-4}" y="{fmt(sy(F(0))-6)}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    o.append(f'<text x="{fmt(sx(0)+7)}" y="{T+14}" fill="#333" font-style="italic">y</text>')
    for a in hasym:
        o.append(f'<line x1="{L}" y1="{fmt(sy(a))}" x2="{L+W}" y2="{fmt(sy(a))}" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="7 5"/>')
    lo, hi = xdomain
    n = 1200; pts_c = []
    for k in range(n + 1):
        x = lo + (hi - lo) * k / n
        y = f(x) / PI
        pts_c.append((sx(x), T + (float(y1) - y) / float(ystep) * ycell))
    o.append('<polyline points="' + ' '.join(f'{fmt(a)},{fmt(b)}' for a, b in pts_c) + f'" fill="none" stroke="{TEAL}" stroke-width="3" stroke-linejoin="round"/>')
    for (x, q, anchor, dx, dy, closed) in pts:
        o.append(f'<circle cx="{fmt(sx(x))}" cy="{fmt(sy(q))}" r="5" fill="{BLUE if closed else "#fff"}" stroke="{BLUE if not closed else "#fff"}" stroke-width="2"/>')
        o.append(f'<text x="{fmt(sx(x)+dx)}" y="{fmt(sy(q)+dy)}" text-anchor="{anchor}" fill="#1a1a2e" paint-order="stroke" stroke="#fff" stroke-width="3">({num_label(x)}, {pi_label(q)})</text>')
    o.append('</svg>')
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')

# Graph 1: arcsin. Endpoints (-1, -pi/2) and (1, pi/2), through (0, 0).
inv_graph('graph1.svg', math.asin, (-2, 2), (-1, 1), [],
          [(-1, F(-1, 2), 'start', 10, 22, True), (0, F(0), 'start', 10, 20, True), (1, F(1, 2), 'end', -10, -12, True)])
# Graph 2: arccos. Endpoints (-1, pi) and (1, 0), through (0, pi/2).
inv_graph('graph2.svg', math.acos, (-2, 2), (-1, 1), [],
          [(-1, F(1), 'start', 10, -10, True), (0, F(1, 2), 'start', 10, -8, True), (1, F(0), 'start', 10, 22, True)])
# Graph 3: arctan. Dashed lines y = -pi/2 and y = pi/2; through (-1, -pi/4), (0, 0), (1, pi/4).
inv_graph('graph3.svg', math.atan, (-4, 4), (-4, 4), [F(-1, 2), F(1, 2)],
          [(-1, F(-1, 4), 'end', -10, -12, True), (0, F(0), 'start', 10, 22, True), (1, F(1, 4), 'start', 10, 24, True)], xcell=62)
print('wrote', sorted(os.listdir(OUT)))
