"""TE6 figures: schematic diagrams of each CheckIt application (ladder, cliff, airplane, hiker, airport,
fire towers, divers, lighthouses, crown moulding, carpenter's boards, bridge brace).
Same style as the other CheckIt figures. Run: python3 tools/figures/make_te6.py"""
import math, os
TEAL, BLUE, ORANGE, INK, GRAY = '#1a6b6b', '#1f4e9c', '#a84d16', '#1a1a2e', '#5a5a6a'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'TE6')
os.makedirs(OUT, exist_ok=True)
W, H = 560, 320


class Fig:
    def __init__(self):
        self.o = [f'<svg viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif" font-size="24">',
                  f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fcfcfc"/>']

    def line(self, P, Q, col=TEAL, w=3, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.o.append(f'<line x1="{P[0]:.1f}" y1="{P[1]:.1f}" x2="{Q[0]:.1f}" y2="{Q[1]:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{d}/>')

    def poly(self, pts, fill='#eef5f5', col=TEAL, w=3):
        p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        self.o.append(f'<polygon points="{p}" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linejoin="round"/>')

    def rect(self, x, y, w, h, fill=GRAY):
        self.o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"/>')

    def dot(self, P, r=6, col=INK):
        self.o.append(f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="{r}" fill="{col}"/>')

    def text(self, x, y, s, col=INK, anc='middle', size=24, italic=False, bold=False):
        st = (' font-style="italic"' if italic else '') + (' font-weight="bold"' if bold else '')
        self.o.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anc}" fill="{col}" font-size="{size}"{st}>{s}</text>')

    def arc(self, P, Q, R, rad, label, col=BLUE, off=28, dx=0, dy=0, size=22):
        """Angle mark at P between rays P->Q and P->R (the smaller angle), with its label."""
        a1 = math.atan2(Q[1] - P[1], Q[0] - P[0]); a2 = math.atan2(R[1] - P[1], R[0] - P[0])
        d = (a2 - a1) % (2 * math.pi)
        if d > math.pi: a1, a2, d = a2, a1, 2 * math.pi - d
        s = (P[0] + rad * math.cos(a1), P[1] + rad * math.sin(a1)); e = (P[0] + rad * math.cos(a2), P[1] + rad * math.sin(a2))
        self.o.append(f'<path d="M {s[0]:.1f} {s[1]:.1f} A {rad} {rad} 0 0 1 {e[0]:.1f} {e[1]:.1f}" fill="none" stroke="{col}" stroke-width="2.5"/>')
        m = a1 + d / 2
        self.text(P[0] + (rad + off) * math.cos(m) + dx, P[1] + (rad + off) * math.sin(m) + 8 + dy, label, col, size=size)

    def right(self, P, u, v, s=16, col=ORANGE):
        """Right-angle marker at P along unit directions u and v."""
        A = (P[0] + s * u[0], P[1] + s * u[1]); C = (P[0] + s * v[0], P[1] + s * v[1]); B = (A[0] + s * v[0], A[1] + s * v[1])
        self.o.append(f'<polyline points="{A[0]:.1f},{A[1]:.1f} {B[0]:.1f},{B[1]:.1f} {C[0]:.1f},{C[1]:.1f}" fill="none" stroke="{col}" stroke-width="2"/>')

    def save(self, name):
        self.o.append('</svg>')
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(self.o) + '\n')


def pol(P, deg, r):
    """Point r away from P at compass-free screen angle deg (0 = right, 90 = up)."""
    t = math.radians(deg)
    return (P[0] + r * math.cos(t), P[1] - r * math.sin(t))


def side_label(f, P, Q, ref, txt, col=BLUE, off=18, size=22, italic=True, t=0.5):
    """Label segment PQ at its midpoint, pushed off the segment on the side away from point ref."""
    mx, my = P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])
    nx, ny = -(Q[1] - P[1]), Q[0] - P[0]; L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
    if nx * (ref[0] - mx) + ny * (ref[1] - my) > 0: nx, ny = -nx, -ny
    anc = 'middle' if abs(nx) < 0.35 else ('start' if nx > 0 else 'end')
    f.text(mx + off * nx, my + off * ny + 8 + 6 * max(ny, 0), txt, col, anc, size, italic=italic)


# ---------- right-triangle situations ----------
def ladder(name, L, h, ask_angle=True):
    f = Fig(); k = 230 / h
    G = (330, 280); T = (G[0], G[1] - h * k)
    base = math.sqrt(L * L - h * h) * k; F = (G[0] - base, G[1])
    f.line((40, G[1]), (520, G[1]), INK, 3)                          # ground
    f.rect(G[0], T[1] - 10, 22, G[1] - T[1] + 10, '#c9d6d6')         # wall
    f.line(F, T, BLUE, 6)                                              # ladder
    f.right(G, (-1, 0), (0, -1))
    f.text((F[0] + T[0]) / 2 - 16, (F[1] + T[1]) / 2, f'ladder {L} ft', BLUE, 'end', italic=True)
    f.text(G[0] + 34, (G[1] + T[1]) / 2 + 8, f'wall {h} ft', INK, 'start', italic=True)
    f.arc(F, (F[0] + 100, F[1]), T, 46, '?', ORANGE, 26)
    f.save(name)


def cliff_depression(name, h, ang, units, ask='angle'):
    """Observer on a cliff top; boat on the water. ask='angle' marks the angle at the boat; ask='dist' marks the sight line."""
    f = Fig(); P = (120, 70); Bt = (120, 270)
    run = 200 / math.tan(math.radians(ang)); run = min(run, 380); B = (P[0] + run, Bt[1])
    f.poly([(40, 270), (120, 270), (120, 70), (40, 70)], '#d9e3e3', TEAL, 2)   # cliff
    f.line((30, 270), (540, 270), BLUE, 3)                                        # water
    f.line(P, (530, P[1]), INK, 2, '7 6')                                         # horizontal at the top
    f.text(528, P[1] - 10, 'horizontal', GRAY, 'end', 18)
    f.line(P, B, ORANGE if ask == 'dist' else TEAL, 3)                            # line of sight
    f.dot(P, 7); f.dot(B, 8, INK)
    f.text(P[0] - 6, P[1] - 14, 'observer', INK, 'middle', 20)
    f.text(B[0], B[1] + 32, 'boat', INK, 'middle', 20)
    f.right(Bt, (0, -1), (1, 0))
    f.text(Bt[0] - 12, (Bt[1] + P[1]) / 2 + 8, f'{h} {units}', INK, 'end', italic=True)
    f.arc(P, (P[0] + 200, P[1]), B, 70, f'{ang}°', BLUE, 24, dx=14)
    if ask == 'angle':
        f.arc(B, (B[0] - 200, B[1]), P, 56, '?', ORANGE, 24, dx=-8)
    else:
        f.text((P[0] + B[0]) / 2 + 14, (P[1] + B[1]) / 2 - 10, 'distance = ?', ORANGE, 'start', italic=True)
    f.save(name)


def cliff_elevation(name, h, ang, units):
    """Observer on the ground; a person on top of a cliff."""
    f = Fig(); Top = (430, 70); Bt = (430, 270)
    run = min(200 / math.tan(math.radians(ang)), 360); O = (Top[0] - run, 270)
    f.poly([(430, 270), (520, 270), (520, 70), (430, 70)], '#d9e3e3', TEAL, 2)
    f.line((30, 270), (540, 270), INK, 3)
    f.line(O, Top, ORANGE, 3)
    f.dot(O, 7); f.dot(Top, 7)
    f.text(O[0], O[1] + 32, 'observer', INK, 'middle', 20)
    f.text(Top[0] + 8, Top[1] - 14, 'person', INK, 'middle', 20)
    f.right(Bt, (0, -1), (-1, 0))
    f.text(475, (Bt[1] + Top[1]) / 2 + 8, f'{h} {units}', INK, 'middle', italic=True)
    f.arc(O, (O[0] + 200, O[1]), Top, 64, f'{ang}°', BLUE, 26)
    f.text((O[0] + Top[0]) / 2 - 16, (O[1] + Top[1]) / 2 - 10, 'distance = ?', ORANGE, 'end', italic=True)
    f.save(name)


def plane(name, ang, alt):
    f = Fig(); R = (40, 270); run = 360; T = (R[0] + run, R[1] - run * math.tan(math.radians(ang)))
    Gnd = (T[0], R[1])
    f.line((30, 270), (540, 270), INK, 3)
    f.line(R, T, BLUE, 3)
    f.line(T, Gnd, INK, 2, '7 6')
    f.right(Gnd, (-1, 0), (0, -1))
    f.o.append(f'<path d="M {T[0]-14:.1f} {T[1]+6:.1f} l 28 -10 l -6 10 z" fill="{INK}"/>')   # small plane marker
    f.text(T[0] + 14, (T[1] + Gnd[1]) / 2 + 8, 'altitude', INK, 'start', italic=True); f.text(T[0] + 14, (T[1] + Gnd[1]) / 2 + 36, alt, INK, 'start', italic=True)
    f.arc(R, (R[0] + 200, R[1]), T, 90, f'{ang}°', BLUE, 24, dx=10)
    f.text((R[0] + Gnd[0]) / 2, R[1] + 34, 'ground distance = ?', ORANGE, 'middle', italic=True)
    f.save(name)


# ---------- non-right situations ----------
def hiker(name, d1, d2, turn, side, ask='angle', units='mi'):
    """Start S, walk d1 to T, turn `turn` degrees to `side`, walk d2 to E. Dashed return path."""
    f = Fig(); k = 250 / d1
    y0 = 240 if side == 'left' else 80
    S = (50, y0); T = (S[0] + d1 * k, y0)
    h = turn if side == 'left' else -turn
    E = pol(T, h, d2 * k)
    f.line(S, T, BLUE, 3); f.line(T, E, BLUE, 3)
    f.line(T, (T[0] + 130, T[1]), INK, 2, '7 6')                      # straight-ahead extension
    f.text(T[0] + 134, T[1] + 6, 'straight ahead', GRAY, 'start', 16)
    f.line(E, S, ORANGE if ask == 'dist' else INK, 2.5, '9 6')         # path back
    away = 32 if side == 'left' else -18
    f.dot(S, 6); f.text(S[0], S[1] + away, 'start', INK, 'middle', 20)
    f.dot(T, 6); f.text(T[0], T[1] + away, 'turn', INK, 'middle', 20)
    f.dot(E, 6); f.text(E[0] + 12, E[1] + (-12 if side == 'left' else 26), 'end', INK, 'start', 20)
    side_label(f, S, T, E, f'{d1} {units}')
    side_label(f, T, E, S, f'{d2} {units}', t=0.8)
    f.arc(T, (T[0] + 100, T[1]), E, 44, f'{turn}°', BLUE, 20, dx=8)
    if ask == 'angle':
        f.arc(T, S, E, 34, '?', ORANGE, 20)
    else:
        side_label(f, S, E, T, 'back = ?', ORANGE)
    f.save(name)


def airport(name, h1, h2, d1=None, d2=None, labels=('Plane 1', 'Plane 2'), units='mi'):
    """Headings measured clockwise from north. If d1/d2 are given, both planes and the gap between them are drawn."""
    f = Fig(); A = (280, 172); r = 115
    f.line(A, (A[0], A[1] - 135), INK, 2); f.o.append(f'<path d="M {A[0]} {A[1]-145} l -8 16 l 16 0 z" fill="{INK}"/>')
    f.text(A[0], A[1] - 150, 'N', INK, 'middle', 22, bold=True)
    def at(h, rr): t = math.radians(h); return (A[0] + rr * math.sin(t), A[1] - rr * math.cos(t))
    if d1:
        m = max(d1, d2); P1, P2 = at(h1, r * d1 / m), at(h2, r * d2 / m)
    else:
        P1, P2 = at(h1, r), at(h2, r)
    f.line(A, P1, BLUE, 3); f.line(A, P2, BLUE, 3); f.dot(A, 7)
    f.text(A[0] - 14, A[1] + 6, 'airport', INK, 'end', 20)
    for h, P, lab, rad in ((h1, P1, labels[0], 24), (h2, P2, labels[1], 38)):
        s0 = at(0, rad); e = at(h, rad); big = 1 if h > 180 else 0
        f.o.append(f'<path d="M {s0[0]:.1f} {s0[1]:.1f} A {rad} {rad} 0 {big} 1 {e[0]:.1f} {e[1]:.1f}" fill="none" stroke="{GRAY}" stroke-width="2" stroke-dasharray="4 4"/>')
        f.dot(P, 6)
        q = at(h, math.hypot(P[0] - A[0], P[1] - A[1]) + 24)
        anc = 'start' if q[0] > A[0] + 10 else ('end' if q[0] < A[0] - 10 else 'middle')
        f.text(q[0], q[1] + (0 if q[1] < A[1] else 14), f'{lab},', INK, anc, 19); f.text(q[0], q[1] + (24 if q[1] < A[1] else 38), f'heading {h}°', INK, anc, 19)
    if d1:
        side_label(f, A, P1, (A[0], A[1] + 100), f'{d1} {units}', off=14, t=0.7)
        side_label(f, A, P2, P1, f'{d2} {units}')
        f.line(P1, P2, ORANGE, 2.5, '9 6')
        side_label(f, P1, P2, A, 'gap = ?', ORANGE)
    else:
        f.arc(A, P1, P2, 76, '?', ORANGE, 20)
    f.save(name)


def towers(name, dist, a1, a2, n1, n2):
    """Tower 1 at left (angle a1), tower 2 at right (angle a2), fire above."""
    f = Fig(); T1 = (90, 265); T2 = (470, 265)
    # intersection of the two sight lines
    t1, t2 = math.radians(a1), math.radians(a2); L = T2[0] - T1[0]
    x = L * math.tan(t2) / (math.tan(t1) + math.tan(t2)); y = x * math.tan(t1)
    sc = min(1, 200 / y); Fz = (T1[0] + x, T1[1] - y * sc)
    # keep true angles: if scaled, redraw with smaller base instead
    if sc < 1:
        L2 = L * sc; T1 = (280 - L2 / 2, 265); T2 = (280 + L2 / 2, 265); Fz = (T1[0] + x * sc, T1[1] - y * sc)
    f.poly([T1, T2, Fz], '#f7f1ec', TEAL, 2.5)
    for P, lab, anc, dx in ((T1, n1, 'end', -14), (T2, n2, 'start', 14)):
        f.rect(P[0] - 9, P[1] - 4, 18, 30, GRAY); f.text(P[0] + dx, P[1] + 22, f'{lab}', INK, anc, 20)
    f.o.append(f'<path d="M {Fz[0]:.1f} {Fz[1]-26:.1f} q 12 14 0 26 q -12 -12 0 -26 z" fill="{ORANGE}"/>')
    f.text(Fz[0], Fz[1] - 32, 'fire', ORANGE, 'middle', 20)
    f.text(280, 265 + 34, f'{dist} mi', BLUE, 'middle', italic=True)
    f.arc(T1, T2, Fz, 50, f'{a1}°', BLUE, 24)
    f.arc(T2, T1, Fz, 50, f'{a2}°', BLUE, 24)
    f.save(name)


def divers(name, dist, depth, a1, a2, n1, n2, animal):
    f = Fig(); D1 = (120, 120); D2 = (440, 120)
    t1, t2 = math.radians(a1), math.radians(a2); L = D2[0] - D1[0]
    x = L * math.tan(t2) / (math.tan(t1) + math.tan(t2)); y = x * math.tan(t1)
    sc = min(1, 140 / y)
    if sc < 1:
        L2 = L * sc; D1 = (280 - L2 / 2, 120); D2 = (280 + L2 / 2, 120)
    An = (D1[0] + x * sc, D1[1] + y * sc)
    f.rect(0, 0, W, 40, '#dfeaf3'); f.line((0, 40), (W, 40), BLUE, 3)
    f.text(14, 30, 'surface', BLUE, 'start', 18)
    f.line((D1[0] - 50, 40), (D1[0] - 50, D1[1]), GRAY, 1.5, '3 4'); f.line((D1[0] - 58, D1[1]), (D1[0] - 42, D1[1]), GRAY, 1.5)
    f.text(D1[0] - 58, 88, f'{depth} m deep', GRAY, 'end', 18)
    f.line(D1, D2, INK, 2, '7 6')
    f.line(D1, An, ORANGE, 3); f.line(D2, An, TEAL, 3)
    f.dot(D1, 7); f.dot(D2, 7); f.dot(An, 9, BLUE)
    f.text(D1[0], D1[1] - 14, n1, INK, 'middle', 20); f.text(D2[0], D2[1] - 14, n2, INK, 'middle', 20)
    f.text(An[0], An[1] + 34, animal, BLUE, 'middle', 20)
    f.text((D1[0] + D2[0]) / 2, D1[1] - 10, f'{dist} m apart', INK, 'middle', 19, italic=True)
    f.arc(D1, D2, An, 54, f'{a1}°', BLUE, 22)
    f.arc(D2, D1, An, 54, f'{a2}°', BLUE, 22)
    f.text((D1[0] + An[0]) / 2 - 14, (D1[1] + An[1]) / 2 + 10, '?', ORANGE, 'end', 24, italic=True)
    f.save(name)


def lighthouses(name, dist, a_boat, a_red, units):
    """Shore at left: red lighthouse (bottom), other lighthouse (top). Boat out at sea to the right."""
    f = Fig(); R = (110, 270); O = (110, 50)
    L = R[1] - O[1]; tR = math.radians(a_red); tB = math.radians(a_boat)
    aO = math.pi - tR - tB
    RB = L * math.sin(aO) / math.sin(tB)                     # side from red lighthouse to the boat
    B = (R[0] + RB * math.sin(tR), R[1] - RB * math.cos(tR))
    if B[0] > 520:
        s = 410 / (B[0] - R[0]); L *= s; O = (R[0], R[1] - L); RB *= s; B = (R[0] + RB * math.sin(tR), R[1] - RB * math.cos(tR))
    f.rect(0, 0, 70, H, '#e9e2d0'); f.line((70, 0), (70, H), INK, 2)
    f.text(35, 170, 'shore', INK, 'middle', 18)
    f.poly([R, O, B], '#eef5f5', TEAL, 2.5)
    f.line(R, B, ORANGE, 3)
    for P, lab in ((R, 'red'), (O, 'other')):
        f.o.append(f'<path d="M {P[0]-8:.1f} {P[1]+12:.1f} L {P[0]-4:.1f} {P[1]-16:.1f} L {P[0]+4:.1f} {P[1]-16:.1f} L {P[0]+8:.1f} {P[1]+12:.1f} z" fill="{GRAY}"/>')
    f.text(R[0] + 16, R[1] + 30, 'red lighthouse', INK, 'start', 19)
    f.text(O[0] + 4, O[1] - 24, 'other lighthouse', INK, 'start', 19)
    f.o.append(f'<path d="M {B[0]-16:.1f} {B[1]:.1f} L {B[0]+16:.1f} {B[1]:.1f} L {B[0]+10:.1f} {B[1]+10:.1f} L {B[0]-10:.1f} {B[1]+10:.1f} z" fill="{INK}"/>')
    f.text(B[0] + 22, B[1] + 8, 'boat', INK, 'start', 20)
    f.text(R[0] + 12, (R[1] + O[1]) / 2 + 8, f'{dist} {units}', BLUE, 'start', italic=True)
    f.arc(B, R, O, 56, f'{a_boat}°', BLUE, 24)
    f.arc(R, O, B, 46, f'{a_red}°', BLUE, 24)
    f.text((R[0] + B[0]) / 2 + 8, (R[1] + B[1]) / 2 + 30, '?', ORANGE, 'middle', 24, italic=True)
    f.save(name)


def moulding(name, ang, dd, units):
    """Ceiling along the top, wall going down; they meet at `ang` degrees at the corner."""
    f = Fig(); Cn = (400, 50); k = 70
    f.line((40, Cn[1]), Cn, INK, 4)                                         # ceiling
    Wd = pol(Cn, -(180 - ang), 250)                                         # wall direction (angle measured inside)
    Wd = (Cn[0] + 250 * math.cos(math.radians(180 + ang)), Cn[1] - 250 * math.sin(math.radians(180 + ang)))
    f.line(Cn, Wd, INK, 4)
    f.text(60, Cn[1] - 14, 'ceiling', INK, 'start', 20); f.text(Wd[0] + 12, Wd[1] - 6, 'wall', INK, 'start', 20)
    P = (Cn[0] - dd * k, Cn[1]); u = ((Wd[0] - Cn[0]) / 250, (Wd[1] - Cn[1]) / 250); Q = (Cn[0] + u[0] * dd * k, Cn[1] + u[1] * dd * k)
    f.poly([Cn, P, Q], '#f7f1ec', TEAL, 0)
    f.line(P, Q, ORANGE, 7)
    f.text((Cn[0] + P[0]) / 2, Cn[1] + 34, f'{dd} {units}', BLUE, 'middle', italic=True)
    f.text(Cn[0] + 14, (Cn[1] + Q[1]) / 2 + 10, f'{dd} {units}', BLUE, 'start', italic=True)
    f.arc(Cn, P, Q, 40, f'{ang}°', BLUE, 26, dx=-6)
    f.text((P[0] + Q[0]) / 2 - 18, (P[1] + Q[1]) / 2 + 30, 'moulding width = ?', ORANGE, 'end', italic=True)
    f.save(name)


def boards(name, d1, d2, d3, units):
    """Two boards meeting at a corner, with the distance between their far ends."""
    f = Fig(); k = 300 / max(d1, d2, d3)
    c = (d1 * d1 + d2 * d2 - d3 * d3) / (2 * d1 * d2); t = math.acos(c)
    Cn = (90, 270); P = (Cn[0] + d2 * k, Cn[1]); Q = (Cn[0] + d1 * k * math.cos(t), Cn[1] - d1 * k * math.sin(t))
    f.line(Cn, P, '#8a6a3a', 12); f.line(Cn, Q, '#8a6a3a', 12)
    f.line(P, Q, INK, 2.5, '9 6')
    f.text((Cn[0] + P[0]) / 2, Cn[1] + 36, f'{d2} {units}', BLUE, 'middle', italic=True)
    f.text((Cn[0] + Q[0]) / 2 - 14, (Cn[1] + Q[1]) / 2, f'{d1} {units}', BLUE, 'end', italic=True)
    f.text((P[0] + Q[0]) / 2 + 14, (P[1] + Q[1]) / 2, f'{d3} {units}', INK, 'start', italic=True)
    f.arc(Cn, P, Q, 44, '?', ORANGE, 24)
    f.save(name)


def brace(name, s1, s2, s3, units):
    """A triangular brace drawn to scale; sides only, no angle marked (the question names which angle)."""
    f = Fig(); a, b, c = s1, s2, s3                      # c along the bottom
    cx = (b * b + c * c - a * a) / (2 * c); cy = math.sqrt(b * b - cx * cx)
    k = min(420 / c, 210 / cy); A = (70, 270); B = (70 + c * k, 270); C = (70 + cx * k, 270 - cy * k)
    f.poly([A, B, C], '#eef5f5', TEAL, 6)
    f.text((A[0] + B[0]) / 2, 270 + 34, f'{c} {units}', BLUE, 'middle', italic=True)
    f.text((A[0] + C[0]) / 2 - 14, (A[1] + C[1]) / 2, f'{b} {units}', BLUE, 'end', italic=True)
    f.text((B[0] + C[0]) / 2 + 14, (B[1] + C[1]) / 2, f'{a} {units}', BLUE, 'start', italic=True)
    f.save(name)


# Set It Up
hiker('su1.svg', 5, 3, 40, 'left', 'angle')
cliff_depression('su2.svg', 300, 20, 'm', 'angle')
airport('su3.svg', 35, 140)
towers('su4.svg', 20, 50, 65, 'Ana', 'Ben')
# Right-triangle situations
ladder('rt1.svg', 24, 22)
cliff_depression('rt2.svg', 400, 25, 'ft', 'dist')
cliff_elevation('rt3.svg', 150, 35, 'm')
plane('rt4.svg', 15, '10,000 ft')
# Lookouts and landmarks
towers('ls1.svg', 30, 55, 62, 'Carla', 'Dev')
divers('ls2.svg', 20, 10, 45, 60, 'Eva', 'Hani', 'sea turtle')
lighthouses('ls3.svg', 12, 40, 75, 'mi')
moulding('ls4.svg', 92, 3, 'in')
# Paths and frames
hiker('lc1.svg', 6, 4, 35, 'right', 'dist', 'km')
airport('lc2.svg', 70, 200, 45, 30, ('Boeing 737', 'Airbus A320'))
boards('lc3.svg', 12, 16, 20.3, 'in')
brace('lc4.svg', 60, 85, 95, 'ft')
print('wrote', sorted(os.listdir(OUT)))
