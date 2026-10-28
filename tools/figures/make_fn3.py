"""FN3 figures: CheckIt-style graphs (built the way TBIL's FN3 generator builds them: a parabola, a line, two more
parabolas, and a line, joined end to end), with a dot at each end of the domain, filled when the end is included and
open when it is not. No other points are marked, as on CheckIt. Run: python3 tools/figures/make_fn3.py"""
import os
from fractions import Fraction as Fr
TEAL, BLUE, GRAY = '#1a6b6b', '#1f4e9c', '#6b6b6b'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'FN3')
os.makedirs(OUT, exist_ok=True)
M = '−'


def lagrange(pts):
    def f(x):
        s = 0
        for i, (xi, yi) in enumerate(pts):
            t = Fr(yi)
            for j, (xj, _) in enumerate(pts):
                if j != i: t *= Fr(x - xj, xi - xj) if isinstance(x, int) else (x - xj) / (xi - xj)
            s += t
        return s
    return f


def build(a, b, c, yint, ext, flip):
    """ext = (y of first extremum, y of second, y of third) before any flip, as in the generator."""
    L = 3
    e0 = (-2 * a - 2 * b - L, 0); e1 = (2 * c + L, yint + L)
    dom = (e0[0] - b, e1[0])
    X = [(-2 * a - b - L, ext[0]), (-a, ext[1]), (c, ext[2])]
    s = -1 if flip else 1
    yi = s * yint; e1 = (e1[0], s * e1[1]); X = [(x, s * y) for x, y in X]
    cuts = [(-2 * a - L, 0), (-2 * a, yi), (0, yi), (2 * c, yi)]
    pieces = [(dom[0], cuts[0][0], lagrange([e0, X[0], cuts[0]])), (cuts[0][0], cuts[1][0], lagrange([cuts[0], cuts[1]])),
              (cuts[1][0], cuts[2][0], lagrange([cuts[1], X[1], cuts[2]])), (cuts[2][0], cuts[3][0], lagrange([cuts[2], X[2], cuts[3]])),
              (cuts[3][0], dom[1], lagrange([cuts[3], e1]))]
    return dom, pieces, X


def draw(name, dom, pieces, closed, x0, x1, y0, y1, cell=18, ylab=2):
    Lm, T, R, B = 44, 12, 14, 34
    W, H = (x1 - x0) * cell, (y1 - y0) * cell
    sx = lambda x: Lm + (x - x0) * cell
    sy = lambda y: T + (y1 - y) * cell
    o = [f'<svg viewBox="0 0 {W+Lm+R} {H+T+B}" class="map-svg" font-family="Arial, Helvetica, sans-serif" font-size="17">',
         f'<rect x="{Lm}" y="{T}" width="{W}" height="{H}" fill="#fcfcfc"/>', '<g stroke="#e2e2e2" stroke-width="1">']
    for i in range(x0, x1 + 1): o.append(f'<line x1="{sx(i)}" y1="{T}" x2="{sx(i)}" y2="{T+H}"/>')
    for j in range(y0, y1 + 1): o.append(f'<line x1="{Lm}" y1="{sy(j)}" x2="{Lm+W}" y2="{sy(j)}"/>')
    o.append('</g>')
    o.append(f'<g stroke="{GRAY}" stroke-width="1.8"><line x1="{Lm}" y1="{sy(0)}" x2="{Lm+W}" y2="{sy(0)}"/><line x1="{sx(0)}" y1="{T}" x2="{sx(0)}" y2="{T+H}"/></g>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(x0, x1 + 1):
        if i and i % 2 == 0: o.append(f'<text x="{sx(i)}" y="{T+H+22}">{str(i).replace("-", M)}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    for j in range(y0, y1 + 1):
        if j and j % ylab == 0: o.append(f'<text x="{Lm-6}" y="{sy(j)+6}">{str(j).replace("-", M)}</text>')
    o.append('</g>')
    o.append(f'<text x="{Lm+W-4}" y="{sy(0)-6}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    o.append(f'<text x="{sx(0)-8}" y="{T+16}" text-anchor="end" fill="#333" font-style="italic">y</text>')
    pts = []
    for a, b, f in pieces:
        for k in range(61):
            x = a + (b - a) * k / 60
            pts.append(f'{sx(x):.1f},{sy(float(f(x))):.1f}')
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{TEAL}" stroke-width="3.5" stroke-linejoin="round"/>')
    for (x, f), filled in zip([(dom[0], pieces[0][2]), (dom[1], pieces[-1][2])], closed):
        o.append(f'<circle cx="{sx(x)}" cy="{sy(float(f(x)))}" r="6.5" fill="{BLUE if filled else "#fff"}" stroke="{BLUE}" stroke-width="3"/>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')
    return float(pieces[0][2](dom[0])), float(pieces[-1][2](dom[1]))


if __name__ == '__main__':
    # Graph 1: a=1, b=2, c=4, y-intercept 5, extrema (-7,-4), (-1,9), (4,2); domain [-11, 11)
    d, p, X = build(1, 2, 4, 5, (-4, 9, 2), False)
    print('g1', d, X, draw('g1.svg', d, p, (True, False), -12, 12, -5, 13))
    # Graph 2: a=2, b=3, c=3, y-intercept -4 (flipped), extrema (-10,5), (-2,-8), (3,-2); domain (-16, 9]
    d, p, X = build(2, 3, 3, 4, (-5, 8, 2), True)
    print('g2', d, X, draw('g2.svg', d, p, (False, True), -17, 10, -16, 7))
    print('wrote', sorted(os.listdir(OUT)))
