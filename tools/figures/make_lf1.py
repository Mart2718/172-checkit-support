"""LF1 figures: lines on CheckIt's window (x and y from -10 to 10, grid every 1) with no points marked, as on CheckIt,
and one curve with a secant line for average rate of change. Run: python3 tools/figures/make_lf1.py"""
import os
from fractions import Fraction as Fr
TEAL, ORANGE, GRAY, INK = '#1a6b6b', '#a84d16', '#6b6b6b', '#1a1a2e'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'LF1')
os.makedirs(OUT, exist_ok=True)
M = '−'


def frame(x0, x1, y0, y1, cell, xstep=2, ystep=2, ylab_every=None):
    L, T, R, B = 44, 12, 14, 34
    W, H = (x1 - x0) * cell, (y1 - y0) * cell
    sx = lambda x: L + (x - x0) * cell
    sy = lambda y: T + (y1 - y) * cell
    o = [f'<svg viewBox="0 0 {W+L+R} {H+T+B}" font-family="Arial, Helvetica, sans-serif" font-size="17">',
         f'<rect x="{L}" y="{T}" width="{W}" height="{H}" fill="#fcfcfc"/>', '<g stroke="#e2e2e2" stroke-width="1">']
    for i in range(x0, x1 + 1): o.append(f'<line x1="{sx(i):.1f}" y1="{T}" x2="{sx(i):.1f}" y2="{T+H}"/>')
    for j in range(y0, y1 + 1): o.append(f'<line x1="{L}" y1="{sy(j):.1f}" x2="{L+W}" y2="{sy(j):.1f}"/>')
    o.append('</g>')
    o.append(f'<g stroke="{GRAY}" stroke-width="1.8"><line x1="{L}" y1="{sy(0):.1f}" x2="{L+W}" y2="{sy(0):.1f}"/><line x1="{sx(0):.1f}" y1="{T}" x2="{sx(0):.1f}" y2="{T+H}"/></g>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(x0, x1 + 1):
        if i and i % xstep == 0: o.append(f'<text x="{sx(i):.1f}" y="{T+H+22}">{str(i).replace("-", M)}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    for j in range(y0, y1 + 1):
        if j and j % ystep == 0: o.append(f'<text x="{L-6}" y="{sy(j)+6:.1f}">{str(j).replace("-", M)}</text>')
    o.append('</g>')
    o.append(f'<text x="{L+W-4}" y="{sy(0)-6:.1f}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    o.append(f'<text x="{sx(0)-8:.1f}" y="{T+16}" text-anchor="end" fill="#333" font-style="italic">y</text>')
    return o, sx, sy, (L, T, W, H)


def line(name, m, b):
    o, sx, sy, (L, T, W, H) = frame(-10, 10, -10, 10, 17)
    # clip the line to the window
    pts = []
    for x in [Fr(-10), Fr(10)]:
        pts.append((x, m * x + b))
    if m != 0:
        for y in [Fr(-10), Fr(10)]:
            x = (y - b) / m
            if -10 <= x <= 10: pts.append((x, y))
    pts = sorted({p for p in pts if -10 <= p[1] <= 10})
    (xa, ya), (xb, yb) = pts[0], pts[-1]
    o.append(f'<line x1="{sx(xa):.1f}" y1="{sy(ya):.1f}" x2="{sx(xb):.1f}" y2="{sy(yb):.1f}" stroke="{TEAL}" stroke-width="3.5"/>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


def secant(name):
    f = lambda x: 2 * x * x - 3 * x + 1
    o, sx, sy, (L, T, W, H) = frame(-1, 5, -4, 24, 14, xstep=1, ystep=4)
    sx2 = lambda x: L + (x + 1) * 60
    o[0] = f'<svg viewBox="0 0 {6*60+L+14} {H+T+34}" font-family="Arial, Helvetica, sans-serif" font-size="17">'
    # redraw cleanly with the wider x scale
    o = [o[0], f'<rect x="{L}" y="{T}" width="{6*60}" height="{H}" fill="#fcfcfc"/>', '<g stroke="#e2e2e2" stroke-width="1">']
    for i in range(-1, 6): o.append(f'<line x1="{sx2(i):.1f}" y1="{T}" x2="{sx2(i):.1f}" y2="{T+H}"/>')
    for j in range(-4, 25, 2): o.append(f'<line x1="{L}" y1="{sy(j):.1f}" x2="{L+6*60}" y2="{sy(j):.1f}"/>')
    o.append('</g>')
    o.append(f'<g stroke="{GRAY}" stroke-width="1.8"><line x1="{L}" y1="{sy(0):.1f}" x2="{L+6*60}" y2="{sy(0):.1f}"/><line x1="{sx2(0):.1f}" y1="{T}" x2="{sx2(0):.1f}" y2="{T+H}"/></g>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(-1, 6):
        if i: o.append(f'<text x="{sx2(i):.1f}" y="{T+H+22}">{str(i).replace("-", M)}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    for j in range(-4, 25, 4):
        if j: o.append(f'<text x="{L-6}" y="{sy(j)+6:.1f}">{str(j).replace("-", M)}</text>')
    o.append('</g>')
    o.append(f'<text x="{L+6*60-4}" y="{sy(0)-6:.1f}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    o.append(f'<text x="{sx2(0)-8:.1f}" y="{T+16}" text-anchor="end" fill="#333" font-style="italic">y</text>')
    for xv in (1, 4):
        o.append(f'<line x1="{sx2(xv):.1f}" y1="{T}" x2="{sx2(xv):.1f}" y2="{T+H}" stroke="{GRAY}" stroke-width="2" stroke-dasharray="6 5"/>')
    xs = [-0.6 + k * (4.9 + 0.6) / 200 for k in range(201)]
    pts = [(x, f(x)) for x in xs if -4 <= f(x) <= 24]
    o.append(f'<polyline points="{" ".join(f"{sx2(x):.1f},{sy(y):.1f}" for x, y in pts)}" fill="none" stroke="{TEAL}" stroke-width="3.5"/>')
    o.append(f'<line x1="{sx2(1):.1f}" y1="{sy(f(1)):.1f}" x2="{sx2(4):.1f}" y2="{sy(f(4)):.1f}" stroke="{ORANGE}" stroke-width="3"/>')
    for xv in (1, 4):
        o.append(f'<circle cx="{sx2(xv):.1f}" cy="{sy(f(xv)):.1f}" r="6" fill="{ORANGE}" stroke="#fff" stroke-width="1.5"/>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


line('g1.svg', Fr(-5, 2), Fr(1))
line('g2.svg', Fr(-1, 2), Fr(4))
line('g3.svg', Fr(0), Fr(3))
line('g4.svg', Fr(3, 2), Fr(1))
secant('secant.svg')
print('wrote', sorted(os.listdir(OUT)))
