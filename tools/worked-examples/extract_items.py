# Usage: python3 extract_items.py explainer.html items.json
import json, sys
from bs4 import BeautifulSoup
soup = BeautifulSoup(open(sys.argv[1], encoding='utf-8'), 'html.parser')
items = []
for it in soup.select('div.item'):
    btn = it.select_one('.guess-btn')
    correct = btn['onclick'].split(',')[-1].strip(" )'")   # last argument of checkGuess(...)
    fig, svg, tbl = it.select_one('figcaption'), it.select_one('svg'), it.select_one('table')
    math = it.select_one('p[style*="font-size"]')
    items.append(dict(
        id=it['id'], title=it.h3.get_text(), prompt=' '.join(it.select_one('.prompt').get_text().split()),
        explanation=it.select_one('[id$=-explanation]').decode_contents().strip(), correct=correct,
        figcaption=fig.decode_contents().strip() if fig else None,
        svg_title=svg.title.get_text() if svg else None, has_svg=bool(svg),
        table_caption=tbl.caption.get_text() if tbl and tbl.caption else None,
        table_rows=[[c.get_text().strip() for c in r.find_all(['th', 'td'])] for r in tbl.find_all('tr')] if tbl else None,
        table_headers=('row' if tbl and tbl.find('th', attrs={'scope': 'col'}) else 'col') if tbl else None,   # 'row' = first ROW holds the header cells
        math=math.decode_contents().strip() if math else None))
json.dump(items, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
print(len(items), 'items')
