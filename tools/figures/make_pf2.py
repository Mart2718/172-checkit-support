"""PF2 figures: trig graphs with x ticks in multiples of pi/4 and several dashed vertical asymptotes.
Same visual style as graph_svg.py (which labels integer ticks only). Run: python3 tools/figures/make_pf2.py"""
import math, os
from fractions import Fraction

TEAL, BLUE, ORANGE = '#1a6b6b', '#1f4e9c', '#a84d16'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'PF2')
PI = math.pi

def fmt(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')

def pi_label(q):
    """q = multiple of pi as a Fraction -> label such as −3π/4, π/2, 2π."""
    if q == 0: return '0'
    s = '−' if q < 0 else ''; q = abs(q)
    n, d = q.numerator, q.denominator
    top = 'π' if n == 1 else f'{n}π'
    return s + (top if d == 1 else f'{top}/{d}')

def trig_graph(name, f, xr, yr, asym, pts, step=Fraction(1, 4), label_every=2, cell=30):
    """xr: (min, max) as Fractions of pi; yr: integer (min, max); asym: list of Fractions of pi;
    pts: list of (x_fraction_of_pi, y, anchor, dx, dy) labeled points."""
    x0, x1 = xr; y0, y1 = yr
    nx = int((x1 - x0) / step)
    L, T, R, B = 34, 12, 16, 30
    W = nx * cell; H = (y1 - y0) * cell
    sx = lambda q: L + float((q - x0) / step) * cell
    sy = lambda y: T + (y1 - y) * cell
    o = [f'<svg viewBox="0 0 {W+L+R} {H+T+B}" font-family="Arial, Helvetica, sans-serif" font-size="13">']
    o.append(f'<rect x="{L}" y="{T}" width="{W}" height="{H}" fill="#fcfcfc"/>')
    o.append('<g stroke="#e0e0e0" stroke-width="1">')
    for i in range(nx + 1): o.append(f'<line x1="{fmt(L+i*cell)}" y1="{T}" x2="{fmt(L+i*cell)}" y2="{T+H}"/>')
    for j in range(y0, y1 + 1): o.append(f'<line x1="{L}" y1="{fmt(sy(j))}" x2="{L+W}" y2="{fmt(sy(j))}"/>')
    o.append('</g>')
    ax = '<g stroke="#6b6b6b" stroke-width="1.5">'
    if y0 <= 0 <= y1: ax += f'<line x1="{L}" y1="{fmt(sy(0))}" x2="{L+W}" y2="{fmt(sy(0))}"/>'
    if x0 <= 0 <= x1: ax += f'<line x1="{fmt(sx(Fraction(0)))}" y1="{T}" x2="{fmt(sx(Fraction(0)))}" y2="{T+H}"/>'
    o.append(ax + '</g>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(nx + 1):
        q = x0 + i * step
        if q != 0 and (q / step) % label_every == 0: o.append(f'<text x="{fmt(L+i*cell)}" y="{T+H+16}">{pi_label(q)}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    for j in range(y0, y1 + 1):
        if j != 0: o.append(f'<text x="{L-4}" y="{fmt(sy(j)+4)}">{str(j).replace("-", "−")}</text>')
    o.append('</g>')
    xa = sy(0) if y0 <= 0 <= y1 else T + H
    o.append(f'<text x="{L+W+2}" y="{fmt(xa-5)}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    ya = sx(Fraction(0)) if x0 <= 0 <= x1 else L
    o.append(f'<text x="{fmt(ya+6)}" y="{T+10}" fill="#333" font-style="italic">y</text>')
    for a in asym:
        o.append(f'<line x1="{fmt(sx(a))}" y1="{T}" x2="{fmt(sx(a))}" y2="{T+H}" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="7 5"/>')
    # curve: sample, break at asymptotes and wherever it leaves the window
    n = 2400; runs = []; run = []
    for k in range(n + 1):
        q = x0 + (x1 - x0) * Fraction(k, n)
        x = float(q) * PI
        near = any(abs(float(q - a)) < 1e-4 for a in asym)
        try: y = None if near else f(x)
        except (ZeroDivisionError, ValueError): y = None
        if y is not None and y0 - 0.02 <= y <= y1 + 0.02 and not (run and abs(y - run[-1][2]) > (y1 - y0) / 2):
            run.append((sx(q), sy(y), y))
        else:
            if len(run) > 1: runs.append(run)
            run = [(sx(q), sy(y), y)] if (y is not None and y0 - 0.02 <= y <= y1 + 0.02) else []
    if len(run) > 1: runs.append(run)
    for r in runs:
        o.append('<polyline points="' + ' '.join(f'{fmt(a)},{fmt(b)}' for a, b, _ in r) + f'" fill="none" stroke="{TEAL}" stroke-width="3" stroke-linejoin="round"/>')
    for (q, y, anchor, dx, dy) in pts:
        o.append(f'<circle cx="{fmt(sx(q))}" cy="{fmt(sy(y))}" r="4.5" fill="{BLUE}" stroke="#fff" stroke-width="1.5"/>')
        text = f'({pi_label(q)}, {str(y).replace("-", "−")})'
        o.append(f'<text x="{fmt(sx(q)+dx)}" y="{fmt(sy(y)+dy)}" text-anchor="{anchor}" fill="#1a1a2e" paint-order="stroke" stroke="#fff" stroke-width="3">{text}</text>')
    o.append('</svg>')
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')

F = Fraction
tan = math.tan; sec = lambda t: 1 / math.cos(t); csc = lambda t: 1 / math.sin(t)
# Graph 1: tan(x + pi/4). Asymptotes at pi/4 + k pi; zeros at -pi/4 + k pi; (0, 1), (-pi/2, -1).
trig_graph('graph1.svg', lambda x: tan(x + PI / 4), (F(-5, 4), F(7, 4)), (-4, 4),
           [F(-3, 4), F(1, 4), F(5, 4)], [(F(0), 1, 'start', 8, -6), (F(-1, 2), -1, 'start', 8, 18), (F(-1, 4), 0, 'end', -8, -8), (F(3, 4), 0, 'start', 8, -8)], label_every=1, cell=44)
# Graph 2: csc(2x). Asymptotes at k pi/2; (pi/4, 1), (3pi/4, -1), (-pi/4, -1).
trig_graph('graph2.svg', lambda x: csc(2 * x), (F(-1, 1), F(1, 1)), (-4, 4),
           [F(-1), F(-1, 2), F(0), F(1, 2), F(1)], [(F(1, 4), 1, 'middle', 0, 22), (F(3, 4), -1, 'middle', 0, -12), (F(-1, 4), -1, 'middle', 0, -12), (F(-3, 4), 1, 'middle', 0, 22)], label_every=1, cell=56)
# Graph 3: sec(x + pi/4). Asymptotes at pi/4 + k pi; (-pi/4, 1), (3pi/4, -1).
trig_graph('graph3.svg', lambda x: sec(x + PI / 4), (F(-5, 4), F(7, 4)), (-4, 4),
           [F(-3, 4), F(1, 4), F(5, 4)], [(F(-1, 4), 1, 'end', -8, 16), (F(3, 4), -1, 'start', 8, -6)], label_every=1, cell=44)
# Graph 4: tan(-x/2) = -tan(x/2). Asymptotes at pi + 2k pi; zero at 0; (pi/2, -1), (-pi/2, 1).
trig_graph('graph4.svg', lambda x: tan(-x / 2), (F(-2), F(2)), (-4, 4),
           [F(-1), F(1)], [(F(0), 0, 'start', 8, -8), (F(1, 2), -1, 'start', 8, 16), (F(-1, 2), 1, 'end', -8, -6)], step=F(1, 4), label_every=2, cell=40)
print('wrote', sorted(os.listdir(OUT)))
