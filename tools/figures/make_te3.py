"""TE3 figures: unit circles crossed by a line (where sine, cosine, or tangent takes a value) and a two-laps picture.
Points where the line meets the circle are drawn but not labeled, so the student still names the angles.
Same style as the other CheckIt figures. Run: python3 tools/figures/make_te3.py"""
import math, os
TEAL, BLUE, ORANGE, INK, GRAY = '#1a6b6b', '#1f4e9c', '#a84d16', '#1a1a2e', '#5a5a6a'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'TE3')
os.makedirs(OUT, exist_ok=True)
W, H = 560, 340
C = (280, 170); R = 130


def head():
    return [f'<svg viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif" font-size="22">',
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fcfcfc"/>',
            f'<line x1="{C[0]-R-40}" y1="{C[1]}" x2="{C[0]+R+40}" y2="{C[1]}" stroke="{GRAY}" stroke-width="1.5"/>',
            f'<line x1="{C[0]}" y1="{C[1]+R+30}" x2="{C[0]}" y2="{C[1]-R-30}" stroke="{GRAY}" stroke-width="1.5"/>',
            f'<text x="{C[0]+R+44}" y="{C[1]+6}" fill="{GRAY}" font-size="20" font-style="italic">x</text>',
            f'<text x="{C[0]+8}" y="{C[1]-R-12}" fill="{GRAY}" font-size="20" font-style="italic">y</text>',
            f'<circle cx="{C[0]}" cy="{C[1]}" r="{R}" fill="none" stroke="{TEAL}" stroke-width="2.5"/>',
            f'<text x="{C[0]+R+6}" y="{C[1]+24}" fill="{INK}" font-size="18">1</text>',
            f'<text x="{C[0]-8}" y="{C[1]-R+40}" text-anchor="end" fill="{INK}" font-size="18">1</text>']


def label(o, x, y, s, col=ORANGE, anc='start', size=22):
    o.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anc}" fill="{col}" font-size="{size}" font-style="italic" stroke="#fcfcfc" stroke-width="6" stroke-linejoin="round" paint-order="stroke">{s}</text>')


def dot(o, deg):
    P = (C[0] + R * math.cos(math.radians(deg)), C[1] - R * math.sin(math.radians(deg)))
    o.append(f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="7" fill="{INK}"/>')


def save(o, name):
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


def horiz(name, values, labels):
    """Horizontal lines y = v (sine values) with their crossing points."""
    o = head()
    for v, lab in zip(values, labels):
        y = C[1] - R * v
        o.append(f'<line x1="{C[0]-R-30}" y1="{y:.1f}" x2="{C[0]+R+30}" y2="{y:.1f}" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="8 6"/>')
        label(o, C[0] + R + 34, y + 8, lab)
        a = math.degrees(math.asin(v)); dot(o, a); dot(o, 180 - a)
    save(o, name)


def vert(name, v, lab):
    """Vertical line x = v (a cosine value) with its crossing points."""
    o = head(); x = C[0] + R * v
    o.append(f'<line x1="{x:.1f}" y1="{C[1]-R-30}" x2="{x:.1f}" y2="{C[1]+R+30}" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="8 6"/>')
    label(o, x - 10, C[1] + R + 26, lab, ORANGE, 'end')
    a = math.degrees(math.acos(v)); dot(o, a); dot(o, -a)
    save(o, name)


def slope(name, m, lab):
    """The line y = m x through the origin: where tangent equals m."""
    o = head(); t = math.atan(m); L = R + 40
    P, Q = (C[0] + L * math.cos(t), C[1] - L * math.sin(t)), (C[0] - L * math.cos(t), C[1] + L * math.sin(t))
    o.append(f'<line x1="{Q[0]:.1f}" y1="{Q[1]:.1f}" x2="{P[0]:.1f}" y2="{P[1]:.1f}" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="8 6"/>')
    label(o, P[0] + 6, P[1] - 4, lab)
    a = math.degrees(t); dot(o, a); dot(o, a + 180)
    save(o, name)


def laps(name):
    """As theta goes once around, 2 theta goes around twice."""
    o = [f'<svg viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif" font-size="22">',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fcfcfc"/>',
         f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>'
         f'<marker id="ah2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ORANGE}"/></marker></defs>']
    # left: one lap
    c1 = (140, 175); r = 90
    o.append(f'<circle cx="{c1[0]}" cy="{c1[1]}" r="{r}" fill="none" stroke="{TEAL}" stroke-width="2"/>')
    one = ' '.join(f'{c1[0] + (r - 16) * math.cos(math.radians(i)):.1f},{c1[1] - (r - 16) * math.sin(math.radians(i)):.1f}' for i in range(0, 349, 6))
    o.append(f'<polyline points="{one}" fill="none" stroke="{BLUE}" stroke-width="3" marker-end="url(#ah)"/>')
    o.append(f'<text x="{c1[0]}" y="{c1[1]+8}" text-anchor="middle" fill="{BLUE}" font-size="26" font-style="italic">θ</text>')
    o.append(f'<text x="{c1[0]}" y="40" text-anchor="middle" fill="{INK}" font-size="26">θ from 0 to 2π:</text>')
    o.append(f'<text x="{c1[0]}" y="{c1[1]+r+40}" text-anchor="middle" fill="{INK}" font-size="26">once around</text>')
    # right: two laps (spiral)
    c2 = (420, 175)
    o.append(f'<circle cx="{c2[0]}" cy="{c2[1]}" r="{r}" fill="none" stroke="{TEAL}" stroke-width="2"/>')
    pts = []
    for i in range(0, 721, 6):
        rr = r - 30 + 22 * i / 720; a = math.radians(i)
        pts.append(f'{c2[0] + rr * math.cos(a):.1f},{c2[1] - rr * math.sin(a):.1f}')
    o.append(f'<polyline points="{" ".join(pts[:-1])}" fill="none" stroke="{ORANGE}" stroke-width="3" marker-end="url(#ah2)"/>')
    o.append(f'<text x="{c2[0]}" y="{c2[1]+8}" text-anchor="middle" fill="{ORANGE}" font-size="26" font-style="italic">2θ</text>')
    o.append(f'<text x="{c2[0]}" y="40" text-anchor="middle" fill="{INK}" font-size="26">2θ from 0 to 4π:</text>')
    o.append(f'<text x="{c2[0]}" y="{c2[1]+r+40}" text-anchor="middle" fill="{INK}" font-size="26">twice around</text>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


horiz('uc1.svg', [math.sqrt(3) / 2], ['y = √3/2'])
vert('uc2.svg', -math.sqrt(2) / 2, 'x = −√2/2')
slope('uc4.svg', math.sqrt(3) / 3, 'y = (√3/3)x')
horiz('sq1.svg', [math.sqrt(3) / 2, -math.sqrt(3) / 2], ['y = √3/2', 'y = −√3/2'])
laps('ma1.svg')
print('wrote', sorted(os.listdir(OUT)))
