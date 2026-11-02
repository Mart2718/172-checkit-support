"""LF5 figure: the rice model R(d) = 250 - 15d on scaled axes (days across, ounces left up).
Run: python3 tools/figures/make_lf5.py"""
import os
TEAL, BLUE, GRAY = '#1a6b6b', '#1f4e9c', '#6b6b6b'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'LF5')
os.makedirs(OUT, exist_ok=True)
L, T, R, B = 62, 14, 16, 52
X1, Y1, CX, CY = 18, 275, 22, 1.2          # d from 0 to 18, R from 0 to 275; pixels per day and per ounce
W, H = X1 * CX, Y1 * CY
sx = lambda d: L + d * CX
sy = lambda r: T + (Y1 - r) * CY
o = [f'<svg viewBox="0 0 {W+L+R:.0f} {H+T+B:.0f}" font-family="Arial, Helvetica, sans-serif" font-size="16">',
     f'<rect x="{L}" y="{T}" width="{W:.0f}" height="{H:.0f}" fill="#fcfcfc"/>', '<g stroke="#e2e2e2" stroke-width="1">']
for d in range(0, X1 + 1, 2): o.append(f'<line x1="{sx(d):.1f}" y1="{T}" x2="{sx(d):.1f}" y2="{T+H:.1f}"/>')
for r in range(0, Y1 + 1, 25): o.append(f'<line x1="{L}" y1="{sy(r):.1f}" x2="{L+W:.1f}" y2="{sy(r):.1f}"/>')
o.append('</g>')
o.append(f'<g stroke="{GRAY}" stroke-width="1.8"><line x1="{L}" y1="{sy(0):.1f}" x2="{L+W:.1f}" y2="{sy(0):.1f}"/><line x1="{L}" y1="{T}" x2="{L}" y2="{T+H:.1f}"/></g>')
o.append('<g fill="#333" text-anchor="middle">')
for d in range(0, X1 + 1, 2): o.append(f'<text x="{sx(d):.1f}" y="{T+H+20:.1f}">{d}</text>')
o.append(f'<text x="{L+W/2:.1f}" y="{T+H+44:.1f}">days, d</text></g><g fill="#333" text-anchor="end">')
for r in range(0, Y1 + 1, 50): o.append(f'<text x="{L-6}" y="{sy(r)+5:.1f}">{r}</text>')
o.append('</g>')
o.append(f'<text x="{L+8}" y="{T+16}" fill="#333">ounces left, R(d)</text>')
dz = 250 / 15
o.append(f'<line x1="{sx(0):.1f}" y1="{sy(250):.1f}" x2="{sx(dz):.1f}" y2="{sy(0):.1f}" stroke="{TEAL}" stroke-width="3.5"/>')
for d, r in [(0, 250), (10, 100)]:
    o.append(f'<circle cx="{sx(d):.1f}" cy="{sy(r):.1f}" r="6" fill="{BLUE}" stroke="#fff" stroke-width="1.5"/>')
o.append('</svg>')
open(os.path.join(OUT, 'rice.svg'), 'w', encoding='utf-8').write('\n'.join(o) + '\n')
print('wrote rice.svg')
