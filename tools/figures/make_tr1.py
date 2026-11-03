"""TR1 figures: angles in standard position. Run: python3 tools/figures/make_tr1.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from anglefig import draw
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'TR1')
draw(os.path.join(OUT, 'd1.svg'), 150, label='150°')                    # first exposure: 150 degrees
draw(os.path.join(OUT, 's1.svg'), 240, guides=30)                      # unlabeled 240 degrees, guide rays every 30
draw(os.path.join(OUT, 'sl4.svg'), 240, clockwise=True, label='2π/3')  # student: 2pi/3 turned clockwise
print('wrote', sorted(os.listdir(OUT)))
