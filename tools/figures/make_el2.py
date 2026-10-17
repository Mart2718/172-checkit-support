import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from graph_svg import graph
out = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'EL2')
os.makedirs(out, exist_ok=True)
# Graph 1: f(x) = 2^x - 1
graph(f'{out}/graph1.svg', lambda x: 2**x - 1, (-4, 4), (-3, 4), [(0, 0, 'start', 8, 16), (1, 1, 'end', -8, -8)], hasym=-1)
# Graph 2: f(x) = -3^x + 2
graph(f'{out}/graph2.svg', lambda x: -3**x + 2, (-3, 3), (-6, 3), [(0, 1, 'start', 8, 16), (1, -1, 'start', 8, 4)], hasym=2)
# Graph 3: f(x) = (1/2)^x - 2
graph(f'{out}/graph3.svg', lambda x: 0.5**x - 2, (-4, 4), (-3, 5), [(-1, 0, 'start', 8, -6), (0, -1, 'end', -8, 18)], hasym=-2)
