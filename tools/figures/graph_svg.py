"""Draw a simple labeled graph as an accessible-by-caption SVG in the same style as the other CheckIt pages.
Usage: import and call graph(...); see tools/figures/make_el2.py for an example.
The SVG itself carries no text alternative: the page template adds the title and caption."""
import math

TEAL, BLUE, ORANGE = '#1a6b6b', '#1f4e9c', '#a84d16'

def fmt(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')

def graph(path, f, xr, yr, pts, hasym=None, vasym=None, cell=33, xlab=1, ylab=1, labels=None):
    """f: python function of x; xr/yr: (min, max) integer window; pts: list of (x, y, anchor, dx, dy) labeled points;
    hasym/vasym: y or x value of a dashed asymptote; xlab/ylab: label every n-th tick."""
    x0, x1 = xr; y0, y1 = yr
    L, T, R, B = 34, 12, 16, 28
    W = (x1 - x0) * cell; H = (y1 - y0) * cell
    sx = lambda x: L + (x - x0) * cell
    sy = lambda y: T + (y1 - y) * cell
    o = [f'<svg viewBox="0 0 {W+L+R} {H+T+B}" font-family="Arial, Helvetica, sans-serif" font-size="13">']
    o.append(f'<rect x="{L}" y="{T}" width="{W}" height="{H}" fill="#fcfcfc"/>')
    o.append('<g stroke="#e0e0e0" stroke-width="1">')
    for i in range(x0, x1 + 1): o.append(f'<line x1="{fmt(sx(i))}" y1="{T}" x2="{fmt(sx(i))}" y2="{T+H}"/>')
    for j in range(y0, y1 + 1): o.append(f'<line x1="{L}" y1="{fmt(sy(j))}" x2="{L+W}" y2="{fmt(sy(j))}"/>')
    o.append('</g>')
    ax = '<g stroke="#6b6b6b" stroke-width="1.5">'
    if y0 <= 0 <= y1: ax += f'<line x1="{L}" y1="{fmt(sy(0))}" x2="{L+W}" y2="{fmt(sy(0))}"/>'
    if x0 <= 0 <= x1: ax += f'<line x1="{fmt(sx(0))}" y1="{T}" x2="{fmt(sx(0))}" y2="{T+H}"/>'
    o.append(ax + '</g>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(x0, x1 + 1):
        if i != 0 and (i - x0) % xlab == 0: o.append(f'<text x="{fmt(sx(i))}" y="{T+H+15}">{str(i).replace("-", "−")}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    for j in range(y0, y1 + 1):
        if j != 0 and (j - y0) % ylab == 0: o.append(f'<text x="{L-4}" y="{fmt(sy(j)+4)}">{str(j).replace("-", "−")}</text>')
    o.append('</g>')
    xa = sy(0) if y0 <= 0 <= y1 else T + H
    o.append(f'<text x="{L+W+2}" y="{fmt(xa-5)}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    ya = sx(0) if x0 <= 0 <= x1 else L
    o.append(f'<text x="{fmt(ya+6)}" y="{T+10}" fill="#333" font-style="italic">y</text>')
    if hasym is not None: o.append(f'<line x1="{L}" y1="{fmt(sy(hasym))}" x2="{L+W}" y2="{fmt(sy(hasym))}" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="7 5"/>')
    if vasym is not None: o.append(f'<line x1="{fmt(sx(vasym))}" y1="{T}" x2="{fmt(sx(vasym))}" y2="{T+H}" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="7 5"/>')
    # curve, clipped to the window
    n = 600; run = []; runs = []
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        try: y = f(x)
        except Exception: y = None
        if y is not None and y0 - 0.01 <= y <= y1 + 0.01: run.append((sx(x), sy(y)))
        else:
            if run: runs.append(run); run = []
    if run: runs.append(run)
    for r in runs:
        o.append('<polyline points="' + ' '.join(f'{fmt(a)},{fmt(b)}' for a, b in r) + f'" fill="none" stroke="{TEAL}" stroke-width="3" stroke-linejoin="round"/>')
    for (x, y, anchor, dx, dy), lab in zip(pts, labels or [None] * len(pts)):
        text = lab or f'({fmt(x)}, {fmt(y)})'.replace('-', '−')
        o.append(f'<circle cx="{fmt(sx(x))}" cy="{fmt(sy(y))}" r="4.5" fill="{BLUE}" stroke="#fff" stroke-width="1.5"/>')
        o.append(f'<text x="{fmt(sx(x)+dx)}" y="{fmt(sy(y)+dy)}" text-anchor="{anchor}" fill="#1a1a2e" paint-order="stroke" stroke="#fff" stroke-width="3">{text}</text>')
    o.append('</svg>')
    open(path, 'w', encoding='utf-8').write('\n'.join(o) + '\n')
