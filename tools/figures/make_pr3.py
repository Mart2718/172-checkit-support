"""PR3 figures: graphs of CheckIt-style polynomials f(x) = k (x - a)^2 (x - b)^n with the zeros and the y-intercept labeled.
The y-axis has its own scale (labeled ticks), since the y-intercept is often much larger than the x-values.
Run: python3 tools/figures/make_pr3.py"""
import math, os
TEAL, BLUE, ORANGE, INK = '#1a6b6b', '#1f4e9c', '#a84d16', '#1a1a2e'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'PR3')
os.makedirs(OUT, exist_ok=True)


def fmt(v):
    return ('%.1f' % v).rstrip('0').rstrip('.').replace('-', '−')


def nice_step(span):
    raw = span / 5
    p = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 5, 10):
        if m * p >= raw: return m * p


def poly(name, k, a, b, n, label_y=True, ydx=10, ydy=None, yanc='start'):
    f = lambda x: k * (x - a) ** 2 * (x - b) ** n
    x0 = min(a, b, 0) - 1.5; x1 = max(a, b, 0) + 1.5
    xs = [x0 + (x1 - x0) * i / 400 for i in range(401)]
    inner = [f(x) for x in xs if min(a, b, 0) - 0.3 <= x <= max(a, b, 0) + 0.3]
    Y = max(abs(v) for v in inner) * 1.25
    step = nice_step(2 * Y); Y = math.ceil(Y / step) * step
    W, H, L, T, R, B = 400, 300, 56, 12, 14, 34
    pw, ph = W - L - R, H - T - B
    sx = lambda x: L + (x - x0) / (x1 - x0) * pw
    sy = lambda y: T + (Y - y) / (2 * Y) * ph
    o = [f'<svg viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif" font-size="21">',
         f'<rect x="{L}" y="{T}" width="{pw}" height="{ph}" fill="#fcfcfc"/>', '<g stroke="#e0e0e0" stroke-width="1">']
    for i in range(math.ceil(x0), math.floor(x1) + 1): o.append(f'<line x1="{sx(i):.1f}" y1="{T}" x2="{sx(i):.1f}" y2="{T+ph}"/>')
    v = -Y
    while v <= Y + 1e-9:
        o.append(f'<line x1="{L}" y1="{sy(v):.1f}" x2="{L+pw}" y2="{sy(v):.1f}"/>'); v += step
    o.append('</g>')
    o.append(f'<g stroke="#6b6b6b" stroke-width="1.5"><line x1="{L}" y1="{sy(0):.1f}" x2="{L+pw}" y2="{sy(0):.1f}"/>'
             f'<line x1="{sx(0):.1f}" y1="{T}" x2="{sx(0):.1f}" y2="{T+ph}"/></g>')
    o.append('<g fill="#333" text-anchor="middle">')
    for i in range(math.ceil(x0), math.floor(x1) + 1):
        if i: o.append(f'<text x="{sx(i):.1f}" y="{T+ph+26}">{fmt(i)}</text>')
    o.append('</g><g fill="#333" text-anchor="end">')
    v = -Y
    while v <= Y + 1e-9:
        if abs(v) > 1e-9: o.append(f'<text x="{L-6}" y="{sy(v)+7:.1f}">{fmt(v)}</text>')
        v += step
    o.append('</g>')
    o.append(f'<text x="{L+pw-4}" y="{sy(0)-8:.1f}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    o.append(f'<text x="{sx(0)+8:.1f}" y="{T+18}" fill="#333" font-style="italic">y</text>')
    o.append(f'<clipPath id="c{name[:-4]}"><rect x="{L}" y="{T}" width="{pw}" height="{ph}"/></clipPath>')
    pts = ' '.join(f'{sx(x):.1f},{sy(max(min(f(x), Y * 1.5), -Y * 1.5)):.1f}' for x in xs)
    o.append(f'<polyline clip-path="url(#c{name[:-4]})" points="{pts}" fill="none" stroke="{TEAL}" stroke-width="3.5" stroke-linejoin="round"/>')
    lab = lambda x, y, t, anc, dx, dy: o.append(f'<text x="{sx(x)+dx:.1f}" y="{sy(y)+dy:.1f}" text-anchor="{anc}" fill="{INK}" font-size="22" paint-order="stroke" stroke="#fff" stroke-width="5">{t}</text>')
    for z in (a, b):
        o.append(f'<circle cx="{sx(z):.1f}" cy="{sy(0):.1f}" r="6" fill="{ORANGE}" stroke="#fff" stroke-width="1.5"/>')
        l, r = f(z - 0.4), f(z + 0.4)
        if l < 0 and r < 0: lab(z, 0, f'({fmt(z)}, 0)', 'middle', 0, -12)         # touches from below: label above
        elif l > 0 and r > 0: lab(z, 0, f'({fmt(z)}, 0)', 'middle', 0, 26)        # touches from above: label below
        elif r > l: lab(z, 0, f'({fmt(z)}, 0)', 'end', -10, -10)                   # crosses going up: label upper left
        else: lab(z, 0, f'({fmt(z)}, 0)', 'start', 10, -10)                        # crosses going down: label upper right
    y0 = f(0)
    o.append(f'<circle cx="{sx(0):.1f}" cy="{sy(y0):.1f}" r="6" fill="{BLUE}" stroke="#fff" stroke-width="1.5"/>')
    if label_y: lab(0, y0, f'(0, {fmt(y0)})', yanc, ydx, ydy if ydy is not None else (-8 if y0 > 0 else 24))
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')
    return y0


print(poly('mg1.svg', 2, -3, 2, 1))      # 2(x+3)^2 (x-2)
print(poly('mg2.svg', -3, 1, -4, 2))     # -3(x-1)^2 (x+4)^2
print(poly('mg3.svg', 4, -2, 4, 1, ydx=-10, ydy=26, yanc='end'))      # 4(x+2)^2 (x-4)

print('wrote', sorted(os.listdir(OUT)))
