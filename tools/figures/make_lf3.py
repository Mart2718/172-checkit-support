"""LF3 figures: CheckIt-style graphs on its -8 to 8 window; the Spot the Slip graphs show the student's plotted points.
Run: python3 tools/figures/make_lf3.py"""
import os, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
from linegrid import draw
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'LF3')
W = dict(window=(-8, 8, -8, 8), cell=21)
draw(os.path.join(OUT, 'h2.svg'), lines=[(0, -2)], **W)                                   # y = -2
draw(os.path.join(OUT, 's1.svg'), lines=[(Fr(1, 2), 3)], points=[(0, 3), (2, 4)], **W)     # student: rising instead of falling
draw(os.path.join(OUT, 's2.svg'), lines=[(2, -4)], points=[(2, 0), (0, -4)], **W)          # correct
draw(os.path.join(OUT, 's3.svg'), lines=[(0, 3)], points=[(0, 3)], **W)                    # student: y = 3 for x = 3
draw(os.path.join(OUT, 's4.svg'), lines=[(Fr(-5, 2), 5)], points=[(2, 0), (0, 5)], **W)    # student: intercepts swapped
draw(os.path.join(OUT, 's5.svg'), lines=[(2, 7)], points=[(-3, 1), (-2, 3)], **W)          # student: point (-3, 1)
print('wrote', sorted(os.listdir(OUT)))
draw(os.path.join(OUT, 'g2.svg'), points=[(4, -2), (0, 3)], **W)                           # the two given points, no line yet
print('wrote g2')
