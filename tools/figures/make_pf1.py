"""PF1 figures: two periods of sinusoids, with x ticks in multiples of pi. Reuses trig_graph from make_pf2.py.
Run: python3 tools/figures/make_pf1.py"""
import os, math
from fractions import Fraction as F
src = open(os.path.join(os.path.dirname(__file__), 'make_pf2.py'), encoding='utf-8').read()
src = src[:src.index("\ntrig_graph('graph1.svg'")]          # function definitions only, none of PF2's figures
g = {'__file__': os.path.join(os.path.dirname(__file__), 'make_pf2.py')}
exec(src, g)
g['OUT'] = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'PF1')
tg = g['trig_graph']
sin, cos, PI = math.sin, math.cos, math.pi
tg('g1.svg', lambda x: -2 * sin(3 * x), (F(0), F(4, 3)), (-3, 3), [], [], step=F(1, 6), label_every=2, cell=34)
tg('g2.svg', lambda x: 4 * cos(2 * x + PI), (F(-1, 2), F(3, 2)), (-5, 5), [], [], step=F(1, 4), label_every=2, cell=24)
tg('g4.svg', lambda x: 2 * cos(3 * x - 3 * PI / 2), (F(0), F(11, 6)), (-3, 3), [], [(F(1, 2), 2, 'start', 8, -8)], step=F(1, 6), label_every=3, cell=36)
print('wrote', sorted(os.listdir(g['OUT'])))
