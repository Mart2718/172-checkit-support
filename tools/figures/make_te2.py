"""TE2 figure: the shape of a verification (start on one side, rewrite, simplify, arrive at the other side).
Same style as the other CheckIt figures. Run: python3 tools/figures/make_te2.py"""
import os
TEAL, BLUE, ORANGE, INK, GRAY = '#1a6b6b', '#1f4e9c', '#a84d16', '#1a1a2e', '#5a5a6a'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'TE2')
os.makedirs(OUT, exist_ok=True)


def flow(name):
    W, H = 560, 440
    o = [f'<svg viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif" font-size="24">',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fcfcfc"/>',
         f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>']
    steps = [('1. Start with one side', BLUE), ('2. Rewrite in sin and cos', TEAL), ('3. Distribute, combine, simplify', TEAL),
             ('4. Use sin² + cos² = 1 if needed', TEAL), ('5. Rename to reach the other side', BLUE)]
    y = 10; bh = 54; gap = 16
    for i, (t, col) in enumerate(steps):
        o.append(f'<rect x="20" y="{y}" width="520" height="{bh}" rx="10" fill="#ffffff" stroke="{col}" stroke-width="3"/>')
        o.append(f'<text x="280" y="{y+35}" text-anchor="middle" fill="{INK}" font-weight="bold" font-size="25">{t}</text>')
        if i < len(steps) - 1:
            o.append(f'<line x1="280" y1="{y+bh}" x2="280" y2="{y+bh+gap-1}" stroke="{INK}" stroke-width="2.5" marker-end="url(#ah)"/>')
        y += bh + gap
    o.append(f'<rect x="20" y="{y+4}" width="520" height="72" rx="10" fill="#f7f1ec" stroke="{ORANGE}" stroke-width="3"/>')
    o.append(f'<text x="280" y="{y+34}" text-anchor="middle" fill="{INK}" font-size="22">Work on one side only. Never move terms</text>')
    o.append(f'<text x="280" y="{y+62}" text-anchor="middle" fill="{INK}" font-size="22">across the equals sign.</text>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


flow('pf1.svg')
print('wrote', sorted(os.listdir(OUT)))
