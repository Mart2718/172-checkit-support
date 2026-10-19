"""TE5 figures: labeled oblique triangles (drawn to scale from their side lengths) and ambiguous-case (SSA) diagrams.
Same style as the other CheckIt figures. Run: python3 tools/figures/make_te5.py"""
import math, os
TEAL, BLUE, ORANGE, INK = '#1a6b6b', '#1f4e9c', '#a84d16', '#1a1a2e'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'TE5')
os.makedirs(OUT, exist_ok=True)

def _arc(P, Q, R, rad):
    """Arc at vertex P between rays P->Q and P->R. Returns (path, label point)."""
    a1 = math.atan2(Q[1] - P[1], Q[0] - P[0]); a2 = math.atan2(R[1] - P[1], R[0] - P[0])
    d = (a2 - a1) % (2 * math.pi)
    if d > math.pi: a1, a2, d = a2, a1, 2 * math.pi - d
    s = (P[0] + rad * math.cos(a1), P[1] + rad * math.sin(a1)); e = (P[0] + rad * math.cos(a2), P[1] + rad * math.sin(a2))
    mid = a1 + d / 2
    lab = (P[0] + (rad + 30) * math.cos(mid), P[1] + (rad + 30) * math.sin(mid) + 9)
    return f'M {s[0]:.1f} {s[1]:.1f} A {rad} {rad} 0 0 1 {e[0]:.1f} {e[1]:.1f}', lab

def _shape(a, b, c):
    """Vertices drawn to scale from the three side lengths: A bottom left, B bottom right, C above."""
    cx = (b * b + c * c - a * a) / (2 * c); cy = math.sqrt(max(b * b - cx * cx, 0))
    xs = [0, c, cx]; x0, x1 = min(xs), max(xs)
    k = min(400 / (x1 - x0), 185 / cy)
    left = 280 - k * (x1 - x0) / 2
    P = lambda x, y: (round(left + k * (x - x0), 1), round(250 - k * y, 1))
    return P(0, 0), P(c, 0), P(cx, cy)

def oblique(name, tri, angles=None, sides=None, ask=None):
    """tri: the full side lengths (a, b, c) used to draw the triangle to scale.
    angles: {'A': '40°', ...}; sides: {'a': '10', ...}; ask: the unknown ('a','b','c','A','B','C'), drawn in orange with '?'."""
    angles = dict(angles or {}); sides = dict(sides or {})
    if ask in ('A', 'B', 'C'): angles[ask] = '?'
    if ask in ('a', 'b', 'c'): sides[ask] = '?'
    A, B, C = _shape(*tri)
    col = lambda k: ORANGE if k == ask else BLUE
    o = ['<svg viewBox="0 0 560 310" font-family="Arial, Helvetica, sans-serif" font-size="28">',
         '<rect x="0" y="0" width="560" height="310" fill="#fcfcfc"/>',
         f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="#eef5f5" stroke="{TEAL}" stroke-width="3" stroke-linejoin="round"/>',
         f'<g fill="{INK}" font-weight="bold"><text x="{A[0]-18}" y="{A[1]+28}" text-anchor="middle">A</text>'
         f'<text x="{B[0]+18}" y="{B[1]+28}" text-anchor="middle">B</text><text x="{C[0]}" y="{C[1]-14}" text-anchor="middle">C</text></g>']
    for k, P, Q, R, rad in (('A', A, B, C, 44), ('B', B, A, C, 44), ('C', C, A, B, 36)):
        if k in angles:
            path, lab = _arc(P, Q, R, rad)
            o.append(f'<path d="{path}" fill="none" stroke="{col(k)}" stroke-width="2.5"/>')
            o.append(f'<text x="{lab[0]:.0f}" y="{lab[1]:.0f}" text-anchor="middle" fill="{col(k)}" font-size="24">{angles[k]}</text>')
    G = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
    for k, P, Q in (('a', B, C), ('b', A, C), ('c', A, B)):
        mx, my = (P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2
        nx, ny = -(Q[1] - P[1]), Q[0] - P[0]; L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
        if nx * (mx - G[0]) + ny * (my - G[1]) < 0: nx, ny = -nx, -ny      # point away from the inside
        x, y = mx + 14 * nx, my + 14 * ny + 9 + 12 * max(ny, 0)
        anc = 'middle' if abs(nx) < 0.3 else ('start' if nx > 0 else 'end')
        txt = f'{k} = {sides[k]}' if k in sides else k
        o.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anc}" fill="{col(k)}" font-style="italic" font-size="26">{txt}</text>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')

def ssa_setup(name, A_deg, b, a):
    """Angle A at the left with side b drawn to C and the height from C to the base line. Side a is NOT placed,
    so the picture does not reveal how many triangles there are."""
    Ap = (60, 260); L = 330; t = math.radians(34)
    C = (Ap[0] + L * math.cos(t), Ap[1] - L * math.sin(t)); foot = (C[0], Ap[1])
    o = ['<svg viewBox="0 0 560 310" font-family="Arial, Helvetica, sans-serif" font-size="28">',
         '<rect x="0" y="0" width="560" height="310" fill="#fcfcfc"/>',
         f'<line x1="{Ap[0]}" y1="{Ap[1]}" x2="530" y2="{Ap[1]}" stroke="{TEAL}" stroke-width="3"/>',
         f'<line x1="{Ap[0]}" y1="{Ap[1]}" x2="{C[0]:.1f}" y2="{C[1]:.1f}" stroke="{TEAL}" stroke-width="3"/>',
         f'<line x1="{C[0]:.1f}" y1="{C[1]:.1f}" x2="{foot[0]:.1f}" y2="{foot[1]}" stroke="{INK}" stroke-width="2" stroke-dasharray="6 5"/>',
         f'<polyline points="{foot[0]-16:.1f},{foot[1]} {foot[0]-16:.1f},{foot[1]-16} {foot[0]:.1f},{foot[1]-16}" fill="none" stroke="{ORANGE}" stroke-width="2"/>']
    path, lab = _arc(Ap, (530, Ap[1]), C, 50)
    o.append(f'<path d="{path}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')
    o.append(f'<text x="{lab[0]+8:.0f}" y="{lab[1]:.0f}" text-anchor="middle" fill="{BLUE}" font-size="24">{A_deg}°</text>')
    o.append(f'<g fill="{INK}" font-weight="bold"><text x="{Ap[0]-18}" y="{Ap[1]+28}" text-anchor="middle">A</text>'
             f'<text x="{C[0]:.0f}" y="{C[1]-14:.0f}" text-anchor="middle">C</text></g>')
    o.append(f'<text x="{(Ap[0]+C[0])/2-12:.0f}" y="{(Ap[1]+C[1])/2-8:.0f}" text-anchor="end" fill="{BLUE}" font-style="italic" font-size="26">b = {b}</text>')
    o.append(f'<text x="{C[0]+10:.0f}" y="{(C[1]+foot[1])/2+8:.0f}" text-anchor="start" fill="{INK}" font-style="italic" font-size="26">h</text>')
    o.append(f'<text x="530" y="{Ap[1]+28}" text-anchor="end" fill="{INK}" font-size="20">a = {a} must reach this line</text>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')

def ssa_two(name, A_deg, b, a, ask=None):
    """The two-triangle picture: side a swings from C and meets the base line at B1 (far) and B2 (near)."""
    Ap = (60, 260); t = math.radians(A_deg)
    k = min(34.0, 200 / (b * math.sin(t)))           # pixels per unit length, so C stays on the canvas
    C = (Ap[0] + b * k * math.cos(t), Ap[1] - b * k * math.sin(t))
    h = b * math.sin(t); dx = math.sqrt(a * a - h * h)
    B1 = (C[0] + dx * k, Ap[1]); B2 = (C[0] - dx * k, Ap[1])
    o = ['<svg viewBox="0 0 560 310" font-family="Arial, Helvetica, sans-serif" font-size="28">',
         '<rect x="0" y="0" width="560" height="310" fill="#fcfcfc"/>',
         f'<line x1="{Ap[0]}" y1="{Ap[1]}" x2="540" y2="{Ap[1]}" stroke="{TEAL}" stroke-width="3"/>',
         f'<line x1="{Ap[0]}" y1="{Ap[1]}" x2="{C[0]:.1f}" y2="{C[1]:.1f}" stroke="{TEAL}" stroke-width="3"/>']
    r = a * k
    ang1 = math.atan2(B2[1] - C[1], B2[0] - C[0]); ang2 = math.atan2(B1[1] - C[1], B1[0] - C[0])
    o.append(f'<path d="M {B2[0]:.1f} {B2[1]:.1f} A {r:.1f} {r:.1f} 0 0 0 {B1[0]:.1f} {B1[1]:.1f}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-dasharray="5 6"/>')
    o.append(f'<line x1="{C[0]:.1f}" y1="{C[1]:.1f}" x2="{B1[0]:.1f}" y2="{B1[1]:.1f}" stroke="{BLUE}" stroke-width="3"/>')
    o.append(f'<line x1="{C[0]:.1f}" y1="{C[1]:.1f}" x2="{B2[0]:.1f}" y2="{B2[1]:.1f}" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="9 5"/>')
    path, lab = _arc(Ap, (540, Ap[1]), C, 46)
    o.append(f'<path d="{path}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')
    o.append(f'<text x="{lab[0]+10:.0f}" y="{lab[1]:.0f}" text-anchor="middle" fill="{BLUE}" font-size="22">{A_deg}°</text>')
    o.append(f'<g fill="{INK}" font-weight="bold"><text x="{Ap[0]-18}" y="{Ap[1]+28}" text-anchor="middle">A</text>'
             f'<text x="{C[0]:.0f}" y="{C[1]-14:.0f}" text-anchor="middle">C</text>'
             f'<text x="{B1[0]:.0f}" y="{B1[1]+30:.0f}" text-anchor="middle">B<tspan font-size="18" dy="6">1</tspan></text>'
             f'<text x="{B2[0]:.0f}" y="{B2[1]+30:.0f}" text-anchor="middle">B<tspan font-size="18" dy="6">2</tspan></text></g>')
    o.append(f'<text x="{(Ap[0]+C[0])/2-12:.0f}" y="{(Ap[1]+C[1])/2-8:.0f}" text-anchor="end" fill="{BLUE}" font-style="italic" font-size="24">b = {b}</text>')
    o.append(f'<text x="{(C[0]+B1[0])/2+12:.0f}" y="{(C[1]+B1[1])/2:.0f}" text-anchor="start" fill="{BLUE}" font-style="italic" font-size="24">a = {a}</text>')
    o.append(f'<text x="{(C[0]+B2[0])/2+12:.0f}" y="{(C[1]+B2[1])/2+30:.0f}" text-anchor="start" fill="{ORANGE}" font-style="italic" font-size="24">a = {a}</text>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')

S = lambda A, B, C, side, val: tuple(val / math.sin(math.radians(X)) * math.sin(math.radians(Y)) for X in [ {'a': A, 'b': B, 'c': C}[side] ] for Y in (A, B, C))
def sas(x, y, ang):  # two sides and the angle between them -> third side
    return math.sqrt(x * x + y * y - 2 * x * y * math.cos(math.radians(ang)))
# Which law? (givens only). Every triangle is drawn to scale from its full set of sides.
oblique('wl1.svg', (7, 9, 12), sides={'a': '7', 'b': '9', 'c': '12'})
oblique('wl2.svg', S(40, 65, 75, 'a', 10), angles={'A': '40°', 'B': '65°'}, sides={'a': '10'})
oblique('wl3.svg', (8, sas(8, 11, 50), 11), angles={'B': '50°'}, sides={'a': '8', 'c': '11'})
oblique('wl4.svg', S(35, 80, 65, 'c', 14), angles={'A': '35°', 'B': '80°'}, sides={'c': '14'})
# Law of Cosines
oblique('lc1.svg', (8, 11, sas(8, 11, 50)), angles={'C': '50°'}, sides={'a': '8', 'b': '11'}, ask='c')
oblique('lc2.svg', (7, 9, 12), sides={'a': '7', 'b': '9', 'c': '12'}, ask='C')
oblique('lc3.svg', (sas(5, 9, 110), 5, 9), angles={'A': '110°'}, sides={'b': '5', 'c': '9'}, ask='a')
oblique('lc4.svg', (5, 8, 10), sides={'a': '5', 'b': '8', 'c': '10'}, ask='A')
# Law of Sines
oblique('ls1.svg', S(40, 65, 75, 'a', 10), angles={'A': '40°', 'B': '65°'}, sides={'a': '10'}, ask='b')
oblique('ls2.svg', S(35, 80, 65, 'c', 14), angles={'A': '35°', 'B': '80°'}, sides={'c': '14'}, ask='a')
oblique('ls3.svg', S(25, 50, 105, 'b', 9), angles={'A': '25°', 'C': '105°'}, sides={'b': '9'}, ask='a')
_B = math.degrees(math.asin(9 * math.sin(math.radians(50)) / 12))
oblique('ls4.svg', S(50, _B, 130 - _B, 'a', 12), angles={'A': '50°'}, sides={'a': '12', 'b': '9'}, ask='B')
# Two sides and an angle not between them
ssa_setup('am1.svg', 30, 10, 6)
ssa_setup('am2.svg', 35, 8, 12)
ssa_two('am3.svg', 40, 12, 9)
print('wrote', sorted(os.listdir(OUT)))
