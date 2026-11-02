"""Shared drawing code for straight-line figures (LF2, LF3, LF5): a CheckIt-style grid with a line, optional marked
points, and vertical lines. Import it from a make_<code>.py script."""
import os
from fractions import Fraction as Fr
TEAL, ORANGE, BLUE, GRAY, INK = '#1a6b6b', '#a84d16', '#1f4e9c', '#6b6b6b', '#1a1a2e'
M = '−'


def num(v):
    return str(v).replace('-', M)


def frame(x0, x1, y0, y1, cell, xstep=2, ystep=2, xlabel='x', ylabel='y'):
    L, T, R, B = 44, 12, 14, 34
    W, H = (x1 - x0) * cell, (y1 - y0) * cell
    sx = lambda x: L + (x - x0) * cell
    sy = lambda y: T + (y1 - y) * cell
    o = [f'<svg viewBox="0 0 {W+L+R} {H+T+B}" font-family="Arial, Helvetica, sans-serif" font-size="17">',
         f'<rect x="{L}" y="{T}" width="{W}" height="{H}" fill="#fcfcfc"/>', '<g stroke="#e2e2e2" stroke-width="1">']
    for i in range(x0, x1 + 1): o.append(f'<line x1="{sx(i):.1f}" y1="{T}" x2="{sx(i):.1f}" y2="{T+H}"/>')
    for j in range(y0, y1 + 1): o.append(f'<line x1="{L}" y1="{sy(j):.1f}" x2="{L+W}" y2="{sy(j):.1f}"/>')
    o.append('</g>')
    if y0 <= 0 <= y1: o.append(f'<line x1="{L}" y1="{sy(0):.1f}" x2="{L+W}" y2="{sy(0):.1f}" stroke="{GRAY}" stroke-width="1.8"/>')
    if x0 <= 0 <= x1: o.append(f'<line x1="{sx(0):.1f}" y1="{T}" x2="{sx(0):.1f}" y2="{T+H}" stroke="{GRAY}" stroke-width="1.8"/>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(x0, x1 + 1):
        if i and i % xstep == 0: o.append(f'<text x="{sx(i):.1f}" y="{T+H+22}">{num(i)}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    for j in range(y0, y1 + 1):
        if j and j % ystep == 0: o.append(f'<text x="{L-6}" y="{sy(j)+6:.1f}">{num(j)}</text>')
    o.append('</g>')
    ya = sy(0) if y0 <= 0 <= y1 else T + H
    xa = sx(0) if x0 <= 0 <= x1 else L
    o.append(f'<text x="{L+W-4}" y="{ya-6:.1f}" text-anchor="end" fill="#333" font-style="italic">{xlabel}</text>')
    o.append(f'<text x="{xa+8:.1f}" y="{T+16}" text-anchor="start" fill="#333" font-style="italic">{ylabel}</text>')
    return o, sx, sy, (L, T, W, H)


def clip(m, b, x0, x1, y0, y1):
    pts = [(Fr(x), m * Fr(x) + b) for x in (x0, x1)]
    if m != 0:
        pts += [((Fr(y) - b) / m, Fr(y)) for y in (y0, y1)]
    pts = sorted({p for p in pts if x0 <= p[0] <= x1 and y0 <= p[1] <= y1})
    return pts[0], pts[-1]


def draw(path, lines=(), verticals=(), points=(), window=(-10, 10, -10, 10), cell=17, xstep=2, ystep=2, xlabel='x', ylabel='y'):
    """lines: [(m, b)] for y = mx + b; verticals: [c] for x = c; points: [(x, y)] marked with dots."""
    x0, x1, y0, y1 = window
    o, sx, sy, _ = frame(x0, x1, y0, y1, cell, xstep, ystep, xlabel, ylabel)
    for m, b in lines:
        (xa, ya), (xb, yb) = clip(Fr(m), Fr(b), x0, x1, y0, y1)
        o.append(f'<line x1="{sx(xa):.1f}" y1="{sy(ya):.1f}" x2="{sx(xb):.1f}" y2="{sy(yb):.1f}" stroke="{TEAL}" stroke-width="3.5"/>')
    for c in verticals:
        o.append(f'<line x1="{sx(c):.1f}" y1="{sy(y1):.1f}" x2="{sx(c):.1f}" y2="{sy(y0):.1f}" stroke="{TEAL}" stroke-width="3.5"/>')
    for x, y in points:
        o.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="6" fill="{BLUE}" stroke="#fff" stroke-width="1.5"/>')
    o.append('</svg>')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write('\n'.join(o) + '\n')
