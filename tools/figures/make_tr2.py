"""TR2 figures: an angle in standard position, and a circle with a central angle and its intercepted arc.
Run: python3 tools/figures/make_tr2.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from anglefig import draw, TEAL, ORANGE, GRAY
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'TR2')
draw(os.path.join(OUT, 'c1.svg'), 135, label='135°')

# a1: circle of radius 6 with a central angle of 5pi/6 (150 degrees) and its arc
S, C, R = 360, 180, 130
pt = lambda deg, r=R: (C + r * math.cos(math.radians(deg)), C - r * math.sin(math.radians(deg)))
o = [f'<svg viewBox="0 0 {S} {S}" font-family="Arial, Helvetica, sans-serif" font-size="18">',
     f'<rect width="{S}" height="{S}" fill="#fcfcfc"/>',
     f'<circle cx="{C}" cy="{C}" r="{R}" fill="none" stroke="{GRAY}" stroke-width="1.8"/>']
a0, a1 = 15, 165
for a in (a0, a1):
    x, y = pt(a)
    o.append(f'<line x1="{C}" y1="{C}" x2="{x:.1f}" y2="{y:.1f}" stroke="{TEAL}" stroke-width="3.5"/>')
arc = ' '.join(f'{pt(a0 + (a1 - a0) * i / 60)[0]:.1f},{pt(a0 + (a1 - a0) * i / 60)[1]:.1f}' for i in range(61))
o.append(f'<polyline points="{arc}" fill="none" stroke="{ORANGE}" stroke-width="6"/>')
small = ' '.join(f'{pt(a0 + (a1 - a0) * i / 40, 30)[0]:.1f},{pt(a0 + (a1 - a0) * i / 40, 30)[1]:.1f}' for i in range(41))
o.append(f'<polyline points="{small}" fill="none" stroke="{GRAY}" stroke-width="2"/>')
x, y = pt(90, 52); o.append(f'<text x="{x:.1f}" y="{y+6:.1f}" text-anchor="middle" fill="#333">5π/6</text>')
x, y = pt(90, R + 18); o.append(f'<text x="{x:.1f}" y="{y+6:.1f}" text-anchor="middle" fill="{ORANGE}" font-weight="bold">s</text>')
x, y = pt(a0, R / 2); o.append(f'<text x="{x:.1f}" y="{y+22:.1f}" text-anchor="middle" fill="{TEAL}">6</text>')
o.append(f'<circle cx="{C}" cy="{C}" r="4" fill="#333"/></svg>')
open(os.path.join(OUT, 'a1.svg'), 'w', encoding='utf-8').write('\n'.join(o) + '\n')
print('wrote', sorted(os.listdir(OUT)))
