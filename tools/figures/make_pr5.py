"""PR5 figures: synthetic division tableaus and one polynomial graph (unlabeled crossings, so students read them).
Run: python3 tools/figures/make_pr5.py"""
import math, os
TEAL, ORANGE, INK = '#1a6b6b', '#a84d16', '#1a1a2e'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'PR5')
os.makedirs(OUT, exist_ok=True)
M = '−'
FS = 28


def num(v):
    return str(v).replace('-', M)


def synth(name, r, top, mid, bot, box=None):
    """top: coefficients; mid: products under columns 1..; bot: bottom row. Entries may be None (blank) or '?' .
    box: (row, col) to draw a dashed answer box with '?'."""
    n = len(top)
    CW, L, T, ROW = 80, 8, 10, 48
    RX = L + 58                         # right edge of the zero box
    C0 = RX + 14
    W = C0 + n * CW + 10
    H = T + 3 * ROW + 16
    cx = lambda c: C0 + (c + 1) * CW - 10
    by = lambda r_: T + (r_ + 1) * ROW - 12
    cls = ' class="map-svg"' if n >= 6 else ''          # wide tableaus may display up to 500 px (template rule)
    o = [f'<svg viewBox="0 0 {W} {H}"{cls} font-family="Arial, Helvetica, sans-serif" font-size="{FS}" fill="{INK}">']
    # the zero being tested, in an L-shaped box
    o.append(f'<path d="M{L},{T+4} L{RX},{T+4} L{RX},{T+ROW+4}" fill="none" stroke="{INK}" stroke-width="2"/>')
    o.append(f'<text x="{(L+RX)/2}" y="{by(0)}" text-anchor="middle" font-weight="bold" fill="{TEAL}">{num(r)}</text>')
    rows = [top, [None] + list(mid), bot]
    for ri, row in enumerate(rows):
        for c, v in enumerate(row):
            if v is None: continue
            if box == (ri, c):
                o.append(f'<rect x="{cx(c)-CW+16}" y="{by(ri)-30}" width="{CW-10}" height="40" rx="5" fill="#fff4ec" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="6 4"/>')
                o.append(f'<text x="{cx(c)-CW/2+10}" y="{by(ri)}" text-anchor="middle" fill="{ORANGE}" font-weight="bold">?</text>')
            else:
                o.append(f'<text x="{cx(c)}" y="{by(ri)}" text-anchor="end"{" font-weight=\"bold\"" if ri == 2 else ""}>{num(v)}</text>')
    ly = T + 2 * ROW + 2
    o.append(f'<line x1="{C0-6}" y1="{ly}" x2="{W-8}" y2="{ly}" stroke="{INK}" stroke-width="2"/>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


def graph(name, f, x0, x1, y0, y1, ystep):
    W, H, L, T, R, B = 400, 300, 58, 12, 14, 34
    pw, ph = W - L - R, H - T - B
    sx = lambda x: L + (x - x0) / (x1 - x0) * pw
    sy = lambda y: T + (y1 - y) / (y1 - y0) * ph
    o = [f'<svg viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif" font-size="21">',
         f'<rect x="{L}" y="{T}" width="{pw}" height="{ph}" fill="#fcfcfc"/>', '<g stroke="#e0e0e0" stroke-width="1">']
    for i in range(math.ceil(x0), math.floor(x1) + 1): o.append(f'<line x1="{sx(i):.1f}" y1="{T}" x2="{sx(i):.1f}" y2="{T+ph}"/>')
    for i in range(2 * math.ceil(x0), 2 * math.floor(x1) + 1):           # half-unit ticks on the x-axis
        if i % 2: o.append(f'<line x1="{sx(i/2):.1f}" y1="{sy(0)-4:.1f}" x2="{sx(i/2):.1f}" y2="{sy(0)+4:.1f}" stroke="#9a9a9a"/>')
    v = y0
    while v <= y1 + 1e-9:
        o.append(f'<line x1="{L}" y1="{sy(v):.1f}" x2="{L+pw}" y2="{sy(v):.1f}"/>'); v += ystep
    o.append('</g>')
    o.append(f'<g stroke="#6b6b6b" stroke-width="1.5"><line x1="{L}" y1="{sy(0):.1f}" x2="{L+pw}" y2="{sy(0):.1f}"/>'
             f'<line x1="{sx(0):.1f}" y1="{T}" x2="{sx(0):.1f}" y2="{T+ph}"/></g>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(math.ceil(x0), math.floor(x1) + 1):
        if i: o.append(f'<text x="{sx(i):.1f}" y="{T+ph+26}">{num(i)}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    v = y0
    while v <= y1 + 1e-9:
        if v: o.append(f'<text x="{L-6}" y="{sy(v)+7:.1f}">{num(int(v))}</text>')
        v += ystep
    o.append('</g>')
    o.append(f'<text x="{L+pw-4}" y="{sy(0)-8:.1f}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    o.append(f'<text x="{sx(0)+8:.1f}" y="{T+20}" fill="#333" font-style="italic">y</text>')
    xs = [x0 + (x1 - x0) * k / 600 for k in range(601)]
    o.append(f'<clipPath id="c{name[:-4]}"><rect x="{L}" y="{T}" width="{pw}" height="{ph}"/></clipPath>')
    pts = ' '.join(f'{sx(x):.1f},{sy(max(min(f(x), y1 * 2), y0 * 2)):.1f}' for x in xs)
    o.append(f'<polyline clip-path="url(#c{name[:-4]})" points="{pts}" fill="none" stroke="{TEAL}" stroke-width="3.5" stroke-linejoin="round"/>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


# Candidates 3: graph of 2x^4 + x^3 - 46x^2 + 28x + 48 = (x-4)(2x-3)(x^2+6x+4)
graph('cz3.svg', lambda x: 2*x**4 + x**3 - 46*x**2 + 28*x + 48, -6, 5, -400, 400, 200)
# Divide 1: x^5 - 3x^4 - 23x^3 + 91x^2 - 6x - 180 divided by x - 3, partway
synth('sd1.svg', 3, [1, -3, -23, 91, -6, -180], [3, 0, -69, '?', None], [1, 0, -23, 22, None, None], box=(1, 4))
# Divide 2: the same division, finished
synth('sd2.svg', 4, [1, 0, -3, -16, -108, -144], [4, 16, 52, 144, 144], [1, 4, 13, 36, 36, 0])
# Divide 3: the quotient x^4 + 4x^3 + 13x^2 + 36x + 36 divided by x + 2
synth('sd3.svg', -2, [1, 4, 13, 36, 36], [-2, -4, -18, -36], [1, 2, 9, 18, 0])
# Divide 4: 3x^3 + 4x^2 - 16x + 8 divided by x - 2/3
synth('sd4.svg', '2/3', [3, 4, -16, 8], [2, 4, -8], [3, 6, -12, 0])
# Slip 2: x^5 - 5x^4 - 6x^3 + 46x^2 - 32x - 24 divided using 3 (testing x + 3)
synth('sl2.svg', 3, [1, -5, -6, 46, -32, -24], [3, -6, -36, 30, -6], [1, -2, -12, 10, -2, -30])
print('wrote', sorted(os.listdir(OUT)))
