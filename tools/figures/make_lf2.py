"""LF2 figures: lines on CheckIt's window (x and y from -10 to 10, grid every 1), no points marked, as on CheckIt.
Run: python3 tools/figures/make_lf2.py"""
import os, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
from linegrid import draw
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'LF2')
draw(os.path.join(OUT, 'g1.svg'), lines=[(Fr(3, 2), -2)])        # through (2, 1), slope 3/2
draw(os.path.join(OUT, 'g2.svg'), lines=[(-2, -2)])              # through (-3, 4), slope -2
draw(os.path.join(OUT, 'g3.svg'), lines=[(3, -15)])                 # through (5, 0), slope 3, y-intercept off the grid
draw(os.path.join(OUT, 'g4.svg'), lines=[(Fr(5, 2), Fr(17, 2))])  # through (-5, -4), slope 5/2
print('wrote', sorted(os.listdir(OUT)))
