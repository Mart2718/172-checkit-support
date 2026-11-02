"""PR1 figures: parabolas on a grid, with the vertex and x-intercepts marked as CheckIt's answer graphs do.
Run: python3 tools/figures/make_pr1.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from linegrid import frame, TEAL, ORANGE, BLUE
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'PR1')
os.makedirs(OUT, exist_ok=True)


def parabola(name, q, xa, xb, window, cell=19, vertex=None, roots=(), xstep=1, ystep=2):
    x0, x1, y0, y1 = window
    o, sx, sy, _ = frame(x0, x1, y0, y1, cell, xstep, ystep)
    n = 240
    pts = []
    for i in range(n + 1):
        x = xa + (xb - xa) * i / n
        y = q(x)
        if y0 <= y <= y1: pts.append(f'{sx(x):.1f},{sy(y):.1f}')
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{TEAL}" stroke-width="3.5"/>')
    for r in roots:
        o.append(f'<circle cx="{sx(r):.1f}" cy="{sy(0):.1f}" r="6" fill="{BLUE}" stroke="#fff" stroke-width="1.5"/>')
    if vertex:
        h, k = vertex
        o.append(f'<rect x="{sx(h)-6:.1f}" y="{sy(k)-6:.1f}" width="12" height="12" fill="{ORANGE}" stroke="#fff" stroke-width="1.5"/>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


parabola('b3.svg', lambda x: (x + 4) * (x - 1), -5, 2, (-6, 3, -8, 8), roots=(-4, 1))                 # x-intercepts only
parabola('c1.svg', lambda x: 2 * (x - 1) ** 2 + 1, -2, 4, (-2, 4, -2, 20), vertex=(1, 1))
parabola('c2.svg', lambda x: 2 * (x + 1) ** 2 - 8, -4, 2, (-5, 3, -9, 11), vertex=(-1, -8), roots=(-3, 1))
parabola('c3.svg', lambda x: -(x - 4) ** 2, 1, 7, (-1, 8, -10, 2), vertex=(4, 0))
print('wrote', sorted(os.listdir(OUT)))
