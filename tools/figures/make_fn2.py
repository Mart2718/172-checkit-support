"""FN2 figures: CheckIt-style graphs of a function g made of straight segments (slopes +/-1 or +/-2) on a closed interval,
with a grid every 1 unit and every corner and end marked. Run: python3 tools/figures/make_fn2.py"""
import os
TEAL, INK, GRAY = '#1a6b6b', '#1a1a2e', '#6b6b6b'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'FN2')
os.makedirs(OUT, exist_ok=True)
M = '−'


def num(v):
    return str(v).replace('-', M)


def segs(name, pts, x0, x1, y0, y1, cell=26):
    L, T, R, B = 40, 12, 14, 34
    W, H = (x1 - x0) * cell, (y1 - y0) * cell
    sx = lambda x: L + (x - x0) * cell
    sy = lambda y: T + (y1 - y) * cell
    o = [f'<svg viewBox="0 0 {W+L+R} {H+T+B}" font-family="Arial, Helvetica, sans-serif" font-size="19">',
         f'<rect x="{L}" y="{T}" width="{W}" height="{H}" fill="#fcfcfc"/>', '<g stroke="#d9d9d9" stroke-width="1">']
    for i in range(x0, x1 + 1): o.append(f'<line x1="{sx(i)}" y1="{T}" x2="{sx(i)}" y2="{T+H}"/>')
    for j in range(y0, y1 + 1): o.append(f'<line x1="{L}" y1="{sy(j)}" x2="{L+W}" y2="{sy(j)}"/>')
    o.append('</g>')
    o.append(f'<g stroke="{GRAY}" stroke-width="1.8"><line x1="{L}" y1="{sy(0)}" x2="{L+W}" y2="{sy(0)}"/><line x1="{sx(0)}" y1="{T}" x2="{sx(0)}" y2="{T+H}"/></g>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(x0, x1 + 1):
        if i: o.append(f'<text x="{sx(i)}" y="{T+H+24}">{num(i)}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    for j in range(y0, y1 + 1):
        if j and j % 2 == 0: o.append(f'<text x="{L-6}" y="{sy(j)+6}">{num(j)}</text>')
    o.append('</g>')
    o.append(f'<text x="{L+W-4}" y="{sy(0)-6}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    o.append(f'<text x="{sx(0)-8}" y="{T+16}" text-anchor="end" fill="#333" font-style="italic">y</text>')
    o.append(f'<polyline points="{" ".join(f"{sx(x)},{sy(y)}" for x, y in pts)}" fill="none" stroke="{TEAL}" stroke-width="4" stroke-linejoin="round"/>')
    for x, y in pts:
        o.append(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="5" fill="{INK}" stroke="#fff" stroke-width="1.5"/>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


# Graph A: corners (-5, -1), (-3, 3), (1, -1), (4, 5) on [-5, 4]
segs('ga.svg', [(-5, -1), (-3, 3), (1, -1), (4, 5)], -6, 5, -3, 6)
# Graph B: corners (-4, 4), (-1, -2), (3, 2), (5, 0) on [-4, 5]
segs('gb.svg', [(-4, 4), (-1, -2), (3, 2), (5, 0)], -5, 6, -3, 5)
print('wrote', sorted(os.listdir(OUT)))
