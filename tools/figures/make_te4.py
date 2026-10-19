"""TE4 figure: a labeled right triangle (C = 90 degrees) in the same style as the other CheckIt figures.
Run: python3 tools/figures/make_te4.py"""
import os
TEAL, BLUE, ORANGE = '#1a6b6b', '#1f4e9c', '#a84d16'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'TE4')

def triangle(name):
    A, C, B = (60, 250), (380, 250), (380, 50)          # A bottom left, C bottom right (right angle), B top right
    o = ['<svg viewBox="0 0 460 300" font-family="Arial, Helvetica, sans-serif" font-size="30">']
    o.append('<rect x="0" y="0" width="460" height="300" fill="#fcfcfc"/>')
    o.append(f'<polygon points="{A[0]},{A[1]} {C[0]},{C[1]} {B[0]},{B[1]}" fill="#eef5f5" stroke="{TEAL}" stroke-width="3" stroke-linejoin="round"/>')
    s = 22   # right-angle marker at C
    o.append(f'<polyline points="{C[0]-s},{C[1]} {C[0]-s},{C[1]-s} {C[0]},{C[1]-s}" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>')
    o.append('<g fill="#1a1a2e" font-weight="bold">')
    o.append(f'<text x="{A[0]-14}" y="{A[1]+26}" text-anchor="middle">A</text>')
    o.append(f'<text x="{C[0]+16}" y="{C[1]+26}" text-anchor="middle">C</text>')
    o.append(f'<text x="{B[0]+16}" y="{B[1]-8}" text-anchor="middle">B</text>')
    o.append('</g><g fill="' + BLUE + '" font-style="italic" font-size="32">')
    o.append(f'<text x="{C[0]+20}" y="{(B[1]+C[1])//2+8}" text-anchor="start">a</text>')
    o.append(f'<text x="{(A[0]+C[0])//2}" y="{C[1]+30}" text-anchor="middle">b</text>')
    o.append(f'<text x="{(A[0]+B[0])//2-14}" y="{(A[1]+B[1])//2-10}" text-anchor="middle">c</text>')
    o.append('</g></svg>')
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')

triangle('triangle.svg')
print('wrote', sorted(os.listdir(OUT)))

# Per-item triangles: same shape, labeled with that problem's given values and a "?" on the unknown.
def labeled(name, angle=None, sides=None, ask=None):
    """angle: ('A' or 'B', text); sides: {'a': text, ...}; ask: 'a'|'b'|'c'|'A'|'B' (the unknown, drawn in orange)."""
    A, C, B = (60, 250), (380, 250), (380, 50)
    sides = sides or {}
    o = ['<svg viewBox="0 0 510 300" font-family="Arial, Helvetica, sans-serif" font-size="30">']
    o.append('<rect x="0" y="0" width="510" height="300" fill="#fcfcfc"/>')
    o.append(f'<polygon points="{A[0]},{A[1]} {C[0]},{C[1]} {B[0]},{B[1]}" fill="#eef5f5" stroke="{TEAL}" stroke-width="3" stroke-linejoin="round"/>')
    s = 22
    o.append(f'<polyline points="{C[0]-s},{C[1]} {C[0]-s},{C[1]-s} {C[0]},{C[1]-s}" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>')
    o.append('<g fill="#1a1a2e" font-weight="bold">')
    o.append(f'<text x="{A[0]-14}" y="{A[1]+26}" text-anchor="middle">A</text>')
    o.append(f'<text x="{C[0]+16}" y="{C[1]+26}" text-anchor="middle">C</text>')
    o.append(f'<text x="{B[0]+16}" y="{B[1]-8}" text-anchor="middle">B</text></g>')
    def col(k): return ORANGE if k == ask else BLUE
    pos = {'a': (C[0] + 14, (B[1] + C[1]) // 2 + 10, 'start'),
           'b': ((A[0] + C[0]) // 2, C[1] + 32, 'middle'),
           'c': ((A[0] + B[0]) // 2 - 22, (A[1] + B[1]) // 2 - 12, 'end')}
    for k in 'abc':
        x, y, anc = pos[k]
        txt = f'{k} = {sides[k]}' if k in sides else (f'{k} = ?' if ask == k else k)
        o.append(f'<text x="{x}" y="{y}" text-anchor="{anc}" fill="{col(k)}" font-style="italic" font-size="28">{txt}</text>')
    if angle or ask in ('A', 'B'):
        which, txt = angle if angle else (ask, '?')
        if ask in ('A', 'B') and not angle: txt = '?'
        if which == 'A':
            o.append(f'<path d="M {A[0]+46} {A[1]} A 46 46 0 0 0 {A[0]+39} {A[1]-25}" fill="none" stroke="{col("A")}" stroke-width="2.5"/>')
            o.append(f'<text x="{A[0]+56}" y="{A[1]-8}" fill="{col("A")}" font-size="26">{txt}</text>')
        else:
            o.append(f'<path d="M {B[0]} {B[1]+46} A 46 46 0 0 0 {B[0]-39} {B[1]+25}" fill="none" stroke="{col("B")}" stroke-width="2.5"/>')
            o.append(f'<text x="{B[0]-10}" y="{B[1]+80}" text-anchor="end" fill="{col("B")}" font-size="26">{txt}</text>')
    o.append('</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')

labeled('as1.svg', angle=('A', '35°'), sides={'c': '12'}, ask='a')
labeled('as2.svg', angle=('B', '62°'), sides={'a': '7'}, ask='b')
labeled('as3.svg', angle=('A', '20°'), sides={'b': '15'}, ask='c')
labeled('as4.svg', angle=('A', '27°'), sides={'a': '11'}, ask='c')
labeled('ts1.svg', sides={'a': '8', 'b': '15'}, ask='c')
labeled('ts2.svg', sides={'a': '20', 'c': '29'}, ask='b')
labeled('ts3.svg', sides={'a': '8', 'b': '15'}, ask='A')
labeled('ts4.svg', sides={'b': '24', 'c': '25'}, ask='A')
print('wrote', sorted(os.listdir(OUT)))
