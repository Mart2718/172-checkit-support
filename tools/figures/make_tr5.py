"""TR5 figures: angles on the unit circle with the terminal point labeled, as CheckIt shows them.
Run: python3 tools/figures/make_tr5.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from anglefig import draw
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'TR5')
draw(os.path.join(OUT, 'p1.svg'), 150, label='θ', unit_circle=True, point=True, point_label='(−√3/2, 1/2)')
draw(os.path.join(OUT, 'q1.svg'), 180 - math.degrees(math.atan2(4, 3)), label='α', unit_circle=True, point=True, point_label='(−3/5, y)')
print('wrote', sorted(os.listdir(OUT)))
