"""PR2 figure: the projectile height h(t) = -16t^2 + 128t + 144 on scaled axes (seconds across, feet up).
Run: python3 tools/figures/make_pr2.py"""
import os
TEAL, ORANGE, GRAY = '#1a6b6b', '#a84d16', '#6b6b6b'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'PR2')
os.makedirs(OUT, exist_ok=True)
L, T, R, B = 62, 14, 16, 52
X1, Y1, CX, CY = 10, 450, 36, 0.72        # t from 0 to 10 s, h from 0 to 450 ft
W, H = X1 * CX, Y1 * CY
sx = lambda t: L + t * CX
sy = lambda h: T + (Y1 - h) * CY
q = lambda t: -16 * t * t + 128 * t + 144
o = [f'<svg viewBox="0 0 {W+L+R:.0f} {H+T+B:.0f}" font-family="Arial, Helvetica, sans-serif" font-size="16">',
     f'<rect x="{L}" y="{T}" width="{W:.0f}" height="{H:.0f}" fill="#fcfcfc"/>', '<g stroke="#e2e2e2" stroke-width="1">']
for t in range(0, X1 + 1): o.append(f'<line x1="{sx(t):.1f}" y1="{T}" x2="{sx(t):.1f}" y2="{T+H:.1f}"/>')
for h in range(0, Y1 + 1, 50): o.append(f'<line x1="{L}" y1="{sy(h):.1f}" x2="{L+W:.1f}" y2="{sy(h):.1f}"/>')
o.append('</g>')
o.append(f'<g stroke="{GRAY}" stroke-width="1.8"><line x1="{L}" y1="{sy(0):.1f}" x2="{L+W:.1f}" y2="{sy(0):.1f}"/><line x1="{L}" y1="{T}" x2="{L}" y2="{T+H:.1f}"/></g>')
o.append('<g fill="#333" text-anchor="middle">')
for t in range(0, X1 + 1): o.append(f'<text x="{sx(t):.1f}" y="{T+H+20:.1f}">{t}</text>')
o.append(f'<text x="{L+W/2:.1f}" y="{T+H+44:.1f}">seconds, t</text></g><g fill="#333" text-anchor="end">')
for h in range(0, Y1 + 1, 100): o.append(f'<text x="{L-6}" y="{sy(h)+5:.1f}">{h}</text>')
o.append('</g>')
o.append(f'<text x="{L+W-8:.1f}" y="{T+16}" fill="#333" text-anchor="end">height in feet, h(t)</text>')
pts = ' '.join(f'{sx(9*i/180):.1f},{sy(q(9*i/180)):.1f}' for i in range(181))
o.append(f'<polyline points="{pts}" fill="none" stroke="{TEAL}" stroke-width="3.5"/>')
o.append('</svg>')
open(os.path.join(OUT, 'proj.svg'), 'w', encoding='utf-8').write('\n'.join(o) + '\n')
print('wrote proj.svg')
