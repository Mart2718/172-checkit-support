"""PR9 figures: number lines for rational inequalities (critical points, test points, shaded answers).
Reuses the number-line drawing from make_pr8.py. Run: python3 tools/figures/make_pr9.py"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'make_pr8.py'), encoding='utf-8').read().split('# Test the Intervals 1')[0]   # functions only
pr8 = {'__file__': os.path.join(HERE, 'make_pr8.py')}
exec(compile(src, 'make_pr8.py', 'exec'), pr8)
OUT = os.path.join(HERE, '..', '..', 'figures', 'PR9')
os.makedirs(OUT, exist_ok=True)
pr8['OUT'] = OUT
numberline, M = pr8['numberline'], pr8['M']

# Sign Chart 1: critical points -4, -3, -2 (all open, since the inequality is strict), test points -5, -3.5, -2.5, 0
numberline('sc1.svg', -6, 1, points=[(-4, '', False), (-3, '', False), (-2, '', False)],
           tests=[(-5, M + '5'), (-3.5, M + '3.5'), (-2.5, M + '2.5'), (0, '0')])
# Write the Answer 1: closed dot at -2, open dot at 1, shaded between; closed dot at 3, shaded right
numberline('wa1.svg', -4, 5, points=[(-2, '', True), (1, '', False), (3, '', True)], shade=[(-2, 1), (3, None)])
print('wrote', sorted(os.listdir(OUT)))
