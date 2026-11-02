"""FN6 figure: f(x) = (x - 1)^3 + 2 and its inverse, mirror images across the dashed line y = x, with (2, 3) marked on f.
Run: python3 tools/figures/make_fn6.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from linegrid import frame, TEAL, ORANGE, BLUE, GRAY
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'FN6')
os.makedirs(OUT, exist_ok=True)
x0, x1, y0, y1 = -4, 6, -4, 6
o, sx, sy, _ = frame(x0, x1, y0, y1, 26, 1, 1)
cbrt = lambda v: v ** (1 / 3) if v >= 0 else -((-v) ** (1 / 3))
f = lambda x: (x - 1) ** 3 + 2
g = lambda x: cbrt(x - 2) + 1


def curve(fn, color, dash=''):
    pts = []
    for i in range(1001):
        x = x0 + (x1 - x0) * i / 1000
        y = fn(x)
        if y0 <= y <= y1: pts.append(f'{sx(x):.1f},{sy(y):.1f}')
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="3.5"{dash}/>')


o.append(f'<line x1="{sx(x0):.1f}" y1="{sy(y0):.1f}" x2="{sx(x1):.1f}" y2="{sy(y1):.1f}" stroke="{GRAY}" stroke-width="2" stroke-dasharray="7 6"/>')
curve(f, TEAL)
curve(g, ORANGE, ' stroke-dasharray="12 5"')
o.append(f'<circle cx="{sx(2):.1f}" cy="{sy(3):.1f}" r="6" fill="{BLUE}" stroke="#fff" stroke-width="1.5"/>')
o.append(f'<text x="{sx(1.55):.1f}" y="{sy(5.3):.1f}" fill="{TEAL}" font-weight="bold">f</text>')
o.append(f'<text x="{sx(5.1):.1f}" y="{sy(2.55):.1f}" fill="{ORANGE}" font-weight="bold">f⁻¹</text>')
o.append(f'<text x="{sx(4.6):.1f}" y="{sy(5.3):.1f}" fill="#555">y = x</text>')
o.append('</svg>')
open(os.path.join(OUT, 'mirror.svg'), 'w', encoding='utf-8').write('\n'.join(o) + '\n')
print('wrote mirror.svg')
