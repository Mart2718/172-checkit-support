"""TE1 figures: unit-circle angle pictures, reference triangles in a quadrant, and a power-reducing graph.
Same style as the other CheckIt figures. Run: python3 tools/figures/make_te1.py"""
import math, os
TEAL, BLUE, ORANGE, INK, GRAY = '#1a6b6b', '#1f4e9c', '#a84d16', '#1a1a2e', '#5a5a6a'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'TE1')
os.makedirs(OUT, exist_ok=True)
W, H = 560, 320


class Fig:
    def __init__(self, w=W, h=H):
        self.w, self.h = w, h
        self.o = [f'<svg viewBox="0 0 {w} {h}" font-family="Arial, Helvetica, sans-serif" font-size="22">',
                  f'<rect x="0" y="0" width="{w}" height="{h}" fill="#fcfcfc"/>']

    def line(self, P, Q, col=TEAL, w=3, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.o.append(f'<line x1="{P[0]:.1f}" y1="{P[1]:.1f}" x2="{Q[0]:.1f}" y2="{Q[1]:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{d}/>')

    def text(self, x, y, s, col=INK, anc='middle', size=22, italic=False, bold=False):
        st = (' font-style="italic"' if italic else '') + (' font-weight="bold"' if bold else '')
        self.o.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anc}" fill="{col}" font-size="{size}"{st}>{s}</text>')

    def frac(self, x, y, num, den, col=INK, size=20):
        """A stacked fraction label centred at (x, y)."""
        self.text(x, y - 4, num, col, 'middle', size)
        self.line((x - 6 - 5 * max(len(num), len(den)), y + 2), (x + 6 + 5 * max(len(num), len(den)), y + 2), col, 1.5)
        self.text(x, y + 22, den, col, 'middle', size)

    def dot(self, P, r=6, col=INK):
        self.o.append(f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="{r}" fill="{col}"/>')

    def arc(self, C, r, a0, a1, col=BLUE, w=2.5, dash=None):
        """Counterclockwise arc (math angles, degrees) of radius r about C."""
        s = (C[0] + r * math.cos(math.radians(a0)), C[1] - r * math.sin(math.radians(a0)))
        e = (C[0] + r * math.cos(math.radians(a1)), C[1] - r * math.sin(math.radians(a1)))
        big = 1 if (a1 - a0) % 360 > 180 else 0
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.o.append(f'<path d="M {s[0]:.1f} {s[1]:.1f} A {r} {r} 0 {big} 0 {e[0]:.1f} {e[1]:.1f}" fill="none" stroke="{col}" stroke-width="{w}"{d}/>')

    def save(self, name):
        self.o.append('</svg>')
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(self.o) + '\n')


def at(C, r, deg):
    return (C[0] + r * math.cos(math.radians(deg)), C[1] - r * math.sin(math.radians(deg)))


def circle_base(f, C, r, half=False):
    f.o.append(f'<circle cx="{C[0]}" cy="{C[1]}" r="{r}" fill="none" stroke="{TEAL}" stroke-width="2.5"/>')
    f.line((C[0] - r - 24, C[1]), (C[0] + r + 24, C[1]), GRAY, 1.5)
    f.line((C[0], C[1] - r - 24), (C[0], C[1] + (12 if half else r + 24)), GRAY, 1.5)


def twelfths(name):
    """Upper half of the unit circle with a tick every 15 degrees; the standard angles labeled; 7pi/12 highlighted."""
    f = Fig(); C = (280, 270); r = 200
    f.o[1] = f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fcfcfc"/>'
    f.o.append(f'<path d="M {C[0]-r} {C[1]} A {r} {r} 0 0 1 {C[0]+r} {C[1]}" fill="none" stroke="{TEAL}" stroke-width="2.5"/>')
    f.line((C[0] - r - 20, C[1]), (C[0] + r + 20, C[1]), GRAY, 1.5)
    labels = {0: ('0', ''), 30: ('π', '6'), 45: ('π', '4'), 60: ('π', '3'), 90: ('π', '2'), 120: ('2π', '3'), 135: ('3π', '4'), 150: ('5π', '6'), 180: ('π', '')}
    for k in range(13):
        d = 15 * k
        P, Q = at(C, r - 8, d), at(C, r + 8, d)
        f.line(P, Q, INK, 2 if d in labels else 1.5)
        if d in labels and d not in (0, 180):
            num, den = labels[d]; L = at(C, r + 36, d)
            f.frac(L[0], L[1] - 6, num, den, INK, 18)
    f.text(C[0] + r + 14, C[1] + 26, '0', INK, 'middle', 18); f.text(C[0] - r - 14, C[1] + 26, 'π', INK, 'middle', 18)
    P = at(C, r, 105)
    f.line(C, P, ORANGE, 3.5); f.dot(P, 7, ORANGE)
    L = at(C, r * 0.55, 112); f.text(L[0] - 6, L[1], '7π/12', ORANGE, 'end', 22, bold=True)
    f.dot(C, 5)
    f.save(name)


def stacked(name):
    """7pi/12 built as pi/3 followed by pi/4."""
    f = Fig(); C = (280, 250); r = 190
    f.o.append(f'<path d="M {C[0]-r} {C[1]} A {r} {r} 0 0 1 {C[0]+r} {C[1]}" fill="none" stroke="{TEAL}" stroke-width="2.5"/>')
    f.line((C[0] - r - 20, C[1]), (C[0] + r + 20, C[1]), GRAY, 1.5)
    A, B = at(C, r, 60), at(C, r, 105)
    f.line(C, A, BLUE, 3); f.line(C, B, ORANGE, 3.5); f.dot(A, 6, BLUE); f.dot(B, 7, ORANGE)
    f.arc(C, 60, 0, 60, BLUE); f.arc(C, 96, 60, 105, ORANGE)
    L1 = at(C, 92, 30); f.frac(L1[0] + 8, L1[1] - 4, 'π', '3', BLUE, 20)
    L2 = at(C, 128, 84); f.frac(L2[0], L2[1] - 8, 'π', '4', ORANGE, 20)
    f.text(B[0] - 14, B[1] - 10, 'angle ?', ORANGE, 'end', 22, bold=True)
    f.dot(C, 5)
    f.save(name)


def halfangle(name):
    """pi/8 as half of pi/4, first quadrant."""
    f = Fig(); C = (90, 290); r = 250
    f.o.append(f'<path d="M {C[0]+r} {C[1]} A {r} {r} 0 0 0 {C[0]} {C[1]-r}" fill="none" stroke="{TEAL}" stroke-width="2.5"/>')
    f.line((C[0] - 10, C[1]), (C[0] + r + 30, C[1]), GRAY, 1.5); f.line((C[0], C[1] + 10), (C[0], C[1] - r - 20), GRAY, 1.5)
    P4, P8 = at(C, r, 45), at(C, r, 22.5)
    f.line(C, P4, BLUE, 3); f.line(C, P8, ORANGE, 3.5); f.dot(P4, 6, BLUE); f.dot(P8, 7, ORANGE)
    f.arc(C, 170, 0, 45, BLUE); f.arc(C, 80, 0, 22.5, ORANGE)
    L4 = at(C, 196, 36); f.frac(L4[0] + 4, L4[1], 'π', '4', BLUE, 20)
    L8 = at(C, 104, 12); f.frac(L8[0] + 6, L8[1] - 2, 'π', '8', ORANGE, 20)
    f.text(P4[0] + 14, P4[1] - 10, 'cos = √2/2', BLUE, 'start', 20)
    f.text(P8[0] + 14, P8[1] + 6, 'cos = ?', ORANGE, 'start', 20, bold=True)
    f.dot(C, 5)
    f.save(name)


def reftri(name, quad, x, y, hyp, known, ask):
    """Reference triangle in a quadrant. x, y: signed leg values (true ratio). known/ask: 'x' or 'y'."""
    f = Fig(); C = (280, 165); k = 125 / max(abs(x), abs(y))
    P = (C[0] + x * k, C[1] - y * k); F = (P[0], C[1])
    f.line((60, C[1]), (500, C[1]), GRAY, 1.5); f.line((C[0], 20), (C[0], 310), GRAY, 1.5)
    f.text(506, C[1] + 6, 'x', GRAY, 'start', 20, italic=True); f.text(C[0] + 8, 26, 'y', GRAY, 'start', 20, italic=True)
    f.text(548, 30, f'θ in Quadrant {["", "I", "II", "III", "IV"][quad]}', GRAY, 'end', 20)
    f.o.append(f'<polygon points="{C[0]},{C[1]} {F[0]:.1f},{F[1]:.1f} {P[0]:.1f},{P[1]:.1f}" fill="#eef5f5" stroke="{TEAL}" stroke-width="3" stroke-linejoin="round"/>')
    sx = -1 if x > 0 else 1; sy = 1 if y > 0 else -1
    s = 14; f.o.append(f'<polyline points="{F[0]+sx*s:.1f},{F[1]} {F[0]+sx*s:.1f},{F[1]-sy*s:.1f} {F[0]:.1f},{F[1]-sy*s:.1f}" fill="none" stroke="{GRAY}" stroke-width="2"/>')
    f.dot(P, 6); f.line(C, P, BLUE, 3)
    th = math.degrees(math.atan2(y, x)) % 360                     # theta from the positive x-axis to the terminal side
    f.arc(C, 18, 0, th, INK, 1.8)
    m = th / 2; f.text(C[0] + 44 * math.cos(math.radians(m)), C[1] - 44 * math.sin(math.radians(m)) + 8, 'θ', INK, 'middle', 22, italic=True)
    mx, my = P[0] + 0.4 * (C[0] - P[0]), P[1] + 0.4 * (C[1] - P[1])  # r label, on the side away from the right angle
    nx, ny = -(P[1] - C[1]), P[0] - C[0]; L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
    if nx * (F[0] - mx) + ny * (F[1] - my) > 0: nx, ny = -nx, -ny
    f.text(mx + 34 * nx, my + 30 * ny + 8, f'r = {hyp}', BLUE, 'start' if nx > 0.3 else ('end' if nx < -0.3 else 'middle'), 22, italic=True)
    neg = lambda v: str(v).replace('-', '−')
    xl = f'x = {neg(x)}' if known == 'x' else 'x = ?'; yl = f'y = {neg(y)}' if known == 'y' else 'y = ?'
    xm = (C[0] + F[0]) / 2
    if abs(F[0] - C[0]) < 110: xm = C[0] + (1 if x > 0 else -1) * 60
    f.text(xm, C[1] + (30 if y > 0 else -14), xl, ORANGE if ask == 'x' else INK, 'middle', 22, italic=True, bold=(ask == 'x'))
    f.text(F[0] + (-14 if x > 0 else 14) * -1, (C[1] + P[1]) / 2 + 8, yl, ORANGE if ask == 'y' else INK, 'start' if x > 0 else 'end', 22, italic=True, bold=(ask == 'y'))
    f.save(name)


def power_graph(name):
    """y = 3 sin^2(4x) on [0, pi/2], with the midline y = 3/2."""
    f = Fig(); x0, x1, yb, yt = 90, 520, 270, 50
    X = lambda t: x0 + (x1 - x0) * t / (math.pi / 2); Y = lambda v: yb - (yb - yt) * v / 3
    f.line((x0, yb), (x1 + 10, yb), GRAY, 1.5); f.line((x0, yb + 10), (x0, yt - 20), GRAY, 1.5)
    for v, lab in ((3, '3'), (1.5, '3/2')):
        f.line((x0, Y(v)), (x1, Y(v)), GRAY, 1.2, '5 5'); f.text(x0 - 10, Y(v) + 7, lab, INK, 'end', 18)
    f.text(x0 - 10, yb + 7, '0', INK, 'end', 18)
    for i, lab in ((1, 'π/8'), (2, 'π/4'), (3, '3π/8'), (4, 'π/2')):
        t = i * math.pi / 8; f.line((X(t), yb), (X(t), yb + 8), INK, 1.5); f.text(X(t), yb + 30, lab, INK, 'middle', 18)
    pts = ' '.join(f'{X(t):.1f},{Y(3 * math.sin(4 * t) ** 2):.1f}' for t in [i * (math.pi / 2) / 240 for i in range(241)])
    f.o.append(f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="3"/>')
    f.text(x1 + 14, yb + 6, 'x', GRAY, 'start', 20, italic=True)
    f.text(x0 + 8, yt - 24, 'y = 3 sin²(4x)', BLUE, 'start', 20, italic=True)
    f.save(name)


twelfths('bd1.svg')
stacked('ex2.svg')
halfangle('ex3.svg')
reftri('py1.svg', 2, -12, 5, 13, 'y', 'x')
reftri('py2.svg', 4, 8, -15, 17, 'x', 'y')
reftri('py3.svg', 3, -21, -20, 29, 'y', 'x')
reftri('py4.svg', 2, -3, 4, 5, 'x', 'y')
power_graph('pr1.svg')
print('wrote', sorted(os.listdir(OUT)))
