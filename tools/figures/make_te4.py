"""TE4 figure: a labeled right triangle (C = 90 degrees) in the same style as the other CheckIt figures.
Run: python3 tools/figures/make_te4.py"""
import os
TEAL, BLUE, ORANGE = '#1a6b6b', '#1f4e9c', '#a84d16'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'TE4')

def triangle(name):
    A, C, B = (60, 250), (380, 250), (380, 50)          # A bottom left, C bottom right (right angle), B top right
    o = ['<svg viewBox="0 0 460 300" font-family="Arial, Helvetica, sans-serif" font-size="22">']
    o.append('<rect x="0" y="0" width="460" height="300" fill="#fcfcfc"/>')
    o.append(f'<polygon points="{A[0]},{A[1]} {C[0]},{C[1]} {B[0]},{B[1]}" fill="#eef5f5" stroke="{TEAL}" stroke-width="3" stroke-linejoin="round"/>')
    s = 22   # right-angle marker at C
    o.append(f'<polyline points="{C[0]-s},{C[1]} {C[0]-s},{C[1]-s} {C[0]},{C[1]-s}" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>')
    o.append('<g fill="#1a1a2e" font-weight="bold">')
    o.append(f'<text x="{A[0]-14}" y="{A[1]+26}" text-anchor="middle">A</text>')
    o.append(f'<text x="{C[0]+16}" y="{C[1]+26}" text-anchor="middle">C</text>')
    o.append(f'<text x="{B[0]+16}" y="{B[1]-8}" text-anchor="middle">B</text>')
    o.append('</g><g fill="' + BLUE + '" font-style="italic" font-size="24">')
    o.append(f'<text x="{C[0]+20}" y="{(B[1]+C[1])//2+8}" text-anchor="start">a</text>')
    o.append(f'<text x="{(A[0]+C[0])//2}" y="{C[1]+30}" text-anchor="middle">b</text>')
    o.append(f'<text x="{(A[0]+B[0])//2-14}" y="{(A[1]+B[1])//2-10}" text-anchor="middle">c</text>')
    o.append('</g></svg>')
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write('\n'.join(o) + '\n')

triangle('triangle.svg')
print('wrote', sorted(os.listdir(OUT)))
