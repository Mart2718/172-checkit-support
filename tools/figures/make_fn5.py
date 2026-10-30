"""FN5 figures: function-machine diagrams. combine.svg shows one input feeding two machines whose outputs are added;
compose.svg shows two machines in a row, the output of the first feeding the second. Run: python3 tools/figures/make_fn5.py"""
import os
TEAL, INK, GRAY, ORANGE = '#1a6b6b', '#1a1a2e', '#6b6b6b', '#a84d16'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'FN5')
os.makedirs(OUT, exist_ok=True)
HEAD = ('<defs><marker id="ah{n}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#444"/></marker></defs>')


def arrow(x1, y1, x2, y2, n):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#444" stroke-width="2.5" marker-end="url(#ah{n})"/>'


def box(x, y, w, h, label):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#e6f2f2" stroke="{TEAL}" stroke-width="3"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + 10}" text-anchor="middle" font-size="30" font-style="italic" fill="{INK}">{label}</text>')


def text(x, y, s, anchor='middle', size=24, color=INK, italic=False):
    st = ' font-style="italic"' if italic else ''
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}"{st}>{s}</text>'


def svg(name, w, h, body, n):
    o = [f'<svg viewBox="0 0 {w} {h}" class="map-svg" font-family="Arial, Helvetica, sans-serif">', HEAD.format(n=n)] + body + ['</svg>']
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


# One input, two machines, outputs added
b = [text(40, 128, 'x', size=30, italic=True),
     arrow(60, 118, 150, 62, 1), arrow(60, 128, 150, 184, 1),
     box(150, 30, 90, 64, 'f'), box(150, 152, 90, 64, 'g'),
     arrow(240, 62, 330, 62, 1), arrow(240, 184, 330, 184, 1),
     text(340, 70, 'f(x)', anchor='start', italic=True), text(340, 192, 'g(x)', anchor='start', italic=True),
     arrow(395, 78, 455, 112, 1), arrow(395, 170, 455, 136, 1),
     f'<circle cx="478" cy="124" r="24" fill="#fff4ec" stroke="{ORANGE}" stroke-width="3"/>', text(478, 134, '+', size=32, color=ORANGE),
     arrow(502, 124, 560, 124, 1), text(568, 132, 'f(x) + g(x)', anchor='start', italic=True)]
svg('combine.svg', 720, 246, b, 1)

# Two machines in a row: 2 -> g -> g(2) -> f -> f(g(2)) = ?
b = [text(30, 92, '2', size=30),
     arrow(50, 82, 110, 82, 2), box(110, 50, 90, 64, 'g'), arrow(200, 82, 290, 82, 2),
     text(245, 66, 'g(2)', italic=True),
     box(290, 50, 90, 64, 'f'), arrow(380, 82, 450, 82, 2),
     text(458, 90, 'f(g(2)) = ?', anchor='start', italic=True),
     text(155, 150, 'first', size=20, color=GRAY), text(335, 150, 'second', size=20, color=GRAY)]
svg('compose.svg', 620, 170, b, 2)
print('wrote', sorted(os.listdir(OUT)))
