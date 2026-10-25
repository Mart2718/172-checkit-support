"""PR4 figures: polynomial long division layouts (cubic divided by a quadratic), drawn row by row.
Terms sit in columns so like terms line up; a subtraction row gets a minus sign in the gutter, parentheses, and a line under it.
Exponents are written with ^ (x^3); x is set in italics.
Run: python3 tools/figures/make_pr4.py"""
import os, re
TEAL, ORANGE, INK = '#1a6b6b', '#a84d16', '#1a1a2e'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'PR4')
os.makedirs(OUT, exist_ok=True)

FS = 24           # font size
CW = 82           # column width
ROW = 40          # row height
DIVW = 124        # room for the divisor, left of the bracket
GUT = 22          # gutter between the bracket and column 0 (holds the minus sign of a subtraction row)


def rich(t, color=INK):
    """'5x^3 − 15x^2' -> SVG tspans with italic x and raised exponents."""
    out = []
    for tok in re.findall(r'\^\d|x|[^x^]+', t):
        if tok.startswith('^'):
            out.append(f'<tspan baseline-shift="super" font-size="{int(FS*0.68)}">{tok[1]}</tspan>')
        elif tok == 'x':
            out.append('<tspan font-style="italic">x</tspan>')
        else:
            out.append(tok.replace(' ', ' '))
    return ''.join(out)


def layout(name, divisor, dividend, quotient=(), rows=(), ncols=4, mark=None):
    """dividend, quotient: lists of (col, text). rows: list of (kind, [(col, text), ...]) with kind 'sub' or 'line'.
    mark: (row index, text) draws an orange box with text (for a blank to fill)."""
    L, T = 8, 10
    BX = L + DIVW                       # bracket x
    C0 = BX + GUT                       # left edge of column 0
    W = C0 + ncols * CW + 8
    nrows = 2 + len(rows)               # quotient row, dividend row, then the rest
    H = T + nrows * ROW + 14
    colx = lambda c: C0 + (c + 1) * CW - 4          # right edge of a column (text anchored at end)
    base = lambda r: T + (r + 1) * ROW - 10         # text baseline of row r
    o = [f'<svg viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif" font-size="{FS}" fill="{INK}">']
    for c, t in quotient:
        o.append(f'<text x="{colx(c)}" y="{base(0)}" text-anchor="end" fill="{TEAL}" font-weight="bold">{rich(t, TEAL)}</text>')
    # divisor and bracket
    top = T + ROW + 2
    o.append(f'<text x="{BX-10}" y="{base(1)}" text-anchor="end">{rich(divisor)}</text>')
    o.append(f'<path d="M{BX},{top} L{W-10},{top} M{BX},{top} Q{BX+12},{top+ROW/2} {BX},{top+ROW}" fill="none" stroke="{INK}" stroke-width="2"/>')
    for c, t in dividend:
        o.append(f'<text x="{colx(c)}" y="{base(1)}" text-anchor="end">{rich(t)}</text>')
    for i, (kind, items) in enumerate(rows):
        r = i + 2
        if kind == 'sub':
            items = list(items)
            c0, t0 = items[0]; items[0] = (c0, '(' + t0)
            c1, t1 = items[-1]; items[-1] = (c1, t1 + ')')
            o.append(f'<text x="{BX+6}" y="{base(r)}">−</text>')
        for c, t in items:
            o.append(f'<text x="{colx(c)}" y="{base(r)}" text-anchor="end">{rich(t)}</text>')
        if kind == 'sub':
            cs = [c for c, _ in items]
            y = base(r) + 10
            o.append(f'<line x1="{C0 + min(cs)*CW + 2}" y1="{y}" x2="{colx(max(cs))+4}" y2="{y}" stroke="{INK}" stroke-width="1.5"/>')
    if mark:
        r, c, t = mark
        o.append(f'<rect x="{C0 + c*CW + 6}" y="{base(r)-24}" width="{CW*(4-c)-12}" height="30" rx="5" fill="#fff4ec" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="6 4"/>')
        o.append(f'<text x="{C0 + c*CW + CW*(4-c)/2}" y="{base(r)-2}" text-anchor="middle" fill="{ORANGE}" font-weight="bold">{t}</text>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')


M = '−'
# One Step 1: the setup (5x^3 - 15x^2 - 49x + 121) / (x^2 + x - 6)
layout('st1.svg', f'x^2 + x {M} 6', [(0, '5x^3'), (1, f'{M} 15x^2'), (2, f'{M} 49x'), (3, '+ 121')])
# One Step 2: (-6x^3 + 6x^2 + 61x + 45) / (x^2 - 3x - 4) after multiplying by -6x; the next line is blank
layout('st2.svg', f'x^2 {M} 3x {M} 4', [(0, f'{M}6x^3'), (1, '+ 6x^2'), (2, '+ 61x'), (3, '+ 45')],
       quotient=[(2, f'{M}6x')], rows=[('sub', [(0, f'{M}6x^3'), (1, '+ 18x^2'), (2, '+ 24x')]), ('line', [])],
       mark=(3, 1, '?'))
# One Step 3: (4x^3 + 16x^2 - 43x - 121) / (x^2 - x - 6) after the first subtraction
layout('st3.svg', f'x^2 {M} x {M} 6', [(0, '4x^3'), (1, '+ 16x^2'), (2, f'{M} 43x'), (3, f'{M} 121')],
       quotient=[(2, '4x')], rows=[('sub', [(0, '4x^3'), (1, f'{M} 4x^2'), (2, f'{M} 24x')]),
                                          ('line', [(1, '20x^2'), (2, f'{M} 19x'), (3, f'{M} 121')])])
# One Step 4: (3x^3 - 15x^2 + 7x + 19) / (x^2 - 3x - 4), worked to the end
layout('st4.svg', f'x^2 {M} 3x {M} 4', [(0, '3x^3'), (1, f'{M} 15x^2'), (2, '+ 7x'), (3, '+ 19')],
       quotient=[(2, '3x'), (3, f'{M} 6')],
       rows=[('sub', [(0, '3x^3'), (1, f'{M} 9x^2'), (2, f'{M} 12x')]),
             ('line', [(1, f'{M}6x^2'), (2, '+ 19x'), (3, '+ 19')]),
             ('sub', [(1, f'{M}6x^2'), (2, '+ 18x'), (3, '+ 24')]),
             ('line', [(2, 'x'), (3, f'{M} 5')])])
# Divide 3: (2x^3 - 25x + 26) / (x^2 + 3x - 4), set up as written (no x^2 term)
layout('dv3.svg', f'x^2 + 3x {M} 4', [(0, '2x^3'), (1, f'{M} 25x'), (2, '+ 26')], quotient=[(2, '2x')])
# Slip 1: (4x^3 + 16x^2 - 59x - 74) / (x^2 - 2x - 3), a student's first subtraction
layout('sl1.svg', f'x^2 {M} 2x {M} 3', [(0, '4x^3'), (1, '+ 16x^2'), (2, f'{M} 59x'), (3, f'{M} 74')],
       quotient=[(2, '4x')], rows=[('sub', [(0, '4x^3'), (1, f'{M} 8x^2'), (2, f'{M} 12x')]),
                                   ('line', [(1, '24x^2'), (2, f'{M} 71x'), (3, f'{M} 74')])])
# Slip 5: (6x^3 - 41x + 32) / (x^2 + x - 6), a student's first subtraction, columns as the student wrote them
layout('sl5.svg', f'x^2 + x {M} 6', [(0, '6x^3'), (1, f'{M} 41x'), (2, '+ 32')],
       quotient=[(1, '6x')], rows=[('sub', [(0, '6x^3'), (1, '+ 6x^2'), (2, f'{M} 36x')]),
                                   ('line', [(1, f'{M}47x^2'), (2, '+ 68x')])])
print('wrote', sorted(os.listdir(OUT)))
