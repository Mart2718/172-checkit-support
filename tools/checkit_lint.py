#!/usr/bin/env python3
"""Static accessibility lint for a CheckIt explainer page.
Usage: python3 checkit_lint.py page.html [--ban "regex of conclusion phrases"]
Exit code 1 if any FAIL."""
import sys, re
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.ids={}; self.dup=[]; self.fails=[]; self.warns=[]
        self.svgs=[]; self.tables=[]; self.cur_table=None; self.headings=[]
        self.cur_text_for={}   # id -> text pieces inside that element
        self.cur_text=[]; self.iframes=[]; self.imgs=[]; self.buttons=[]; self.tabs=[]; self.panels=[]
        self.lang=None; self.title=''; self.in_title=False; self.live=0
        self.cur_svg=None; self.cur_btn=None; self.cur_id_stack=[]; self.cur_cap=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); self.stack.append((tag,a))
        i=a.get('id')
        if i:
            if i in self.ids: self.dup.append(i)
            self.ids[i]=tag
        self.cur_id_stack.append(i)
        if tag=='html': self.lang=a.get('lang')
        if tag=='title': self.in_title=True
        if tag=='svg': self.cur_svg={'a':a,'title':'','id':i}; self.svgs.append(self.cur_svg)
        if tag=='table': self.cur_table={'a':a,'caption':'','ths':[],'id':i}; self.tables.append(self.cur_table)
        if tag=='caption': self.cur_cap=[]
        if tag=='th' and self.cur_table is not None: self.cur_table['ths'].append(a.get('scope'))
        if tag in('h1','h2','h3','h4','h5','h6'): self.headings.append(int(tag[1]))
        if tag=='iframe': self.iframes.append(a)
        if tag=='img': self.imgs.append(a)
        if tag=='button': self.cur_btn={'a':a,'text':''}; self.buttons.append(self.cur_btn)
        if a.get('role')=='tab': self.tabs.append(a)
        if a.get('role')=='tabpanel': self.panels.append(a)
        if 'aria-live' in a: self.live+=1
    def handle_endtag(self,tag):
        if tag=='title': self.in_title=False
        if tag=='caption' and self.cur_table is not None and self.cur_cap is not None:
            self.cur_table['caption']=''.join(self.cur_cap).strip(); self.cur_cap=None
        if tag=='table': self.cur_table=None
        if tag=='svg': self.cur_svg=None
        if tag=='button': self.cur_btn=None
        if self.stack: self.stack.pop()
        if self.cur_id_stack: self.cur_id_stack.pop()
    def handle_data(self,d):
        if self.in_title and not any(t=='svg' for t,_ in self.stack): self.title+=d
        if self.cur_cap is not None: self.cur_cap.append(d)
        if self.cur_btn is not None: self.cur_btn['text']+=d
        for i in self.cur_id_stack:
            if i: self.cur_text_for.setdefault(i,[]).append(d)
        # svg <title>
        if self.cur_svg is not None and self.stack and self.stack[-1][0]=='title': self.cur_svg['title']+=d

def run(path, ban):
    src=open(path,encoding='utf-8').read()
    p=P(); p.feed(src)
    F=[];W=[]
    if not p.lang: F.append('3.1.1 <html> has no lang attribute')
    if not p.title.strip(): F.append('2.4.2 page has no <title>')
    if p.dup: F.append('4.1.1 duplicate ids: '+', '.join(sorted(set(p.dup))))
    for s in p.svgs:
        a=s['a']; sid=s['id'] or '(no id)'
        if a.get('role')!='img': F.append(f'1.1.1 svg {sid}: missing role="img"')
        if not s['title'].strip(): F.append(f'1.1.1 svg {sid}: no <title> text')
        for key in ('aria-labelledby','aria-describedby'):
            for ref in (a.get(key) or '').split():
                if ref not in p.ids: F.append(f'1.1.1 svg {sid}: {key} points to missing id {ref}')
        if not a.get('aria-describedby'): W.append(f'svg {sid}: no aria-describedby caption (text alternative may be too short)')
        else:
            for ref in a['aria-describedby'].split():
                t=''.join(p.cur_text_for.get(ref,[])).strip()
                if len(t)<25: W.append(f'svg {sid}: caption {ref} is very short')
    for im in p.imgs:
        if 'alt' not in im: F.append(f'1.1.1 <img src={im.get("src")}> has no alt attribute')
    for t in p.tables:
        tid=t['id'] or '(table)'
        if not t['caption']: F.append(f'1.3.1 table {tid}: no <caption>')
        if not t['ths']: F.append(f'1.3.1 table {tid}: no <th> header cells')
        if any(s is None for s in t['ths']): F.append(f'1.3.1 table {tid}: <th> without scope attribute')
    for fr in p.iframes:
        if not (fr.get('title') or '').strip(): F.append('4.1.2 <iframe> without title')
    for b in p.buttons:
        if not b['text'].strip() and not b['a'].get('aria-label'): F.append('4.1.2 button with no accessible name')
    last=0
    for h in p.headings:
        if last and h>last+1: F.append(f'1.3.1 heading level skipped (h{last} -> h{h})')
        last=h
    if p.live==0 and any('guess-btn' in (b['a'].get('class') or '') for b in p.buttons): F.append('4.1.3 no aria-live region for feedback')
    for tb in p.tabs:
        if tb.get('aria-controls') not in p.ids: F.append(f'4.1.2 tab {tb.get("id")}: aria-controls target missing')
    for pn in p.panels:
        if pn.get('aria-labelledby') not in p.ids: F.append(f'4.1.2 tabpanel {pn.get("id")}: aria-labelledby target missing')
    if ban:
        rx=re.compile(ban,re.I)
        for s in p.svgs:
            if rx.search(s['title']): F.append(f'ASSESSMENT-VALIDITY svg {s["id"]}: <title> states a conclusion: {s["title"]!r}')
            for ref in (s['a'].get('aria-describedby') or '').split():
                t=''.join(p.cur_text_for.get(ref,[]))
                if rx.search(t): F.append(f'ASSESSMENT-VALIDITY caption {ref} states a conclusion')
        for t in p.tables:
            if rx.search(t['caption']): F.append(f'ASSESSMENT-VALIDITY table {t["id"]} caption states a conclusion')
    print(path)
    print(f'  svgs={len(p.svgs)} tables={len(p.tables)} iframes={len(p.iframes)} buttons={len(p.buttons)} headings={len(p.headings)}')
    for w in W: print('  WARN',w)
    for f in F: print('  FAIL',f)
    if not F: print('  PASS: no static failures')
    return 1 if F else 0

if __name__=='__main__':
    args=sys.argv[1:]
    ban=None
    if '--ban' in args:
        k=args.index('--ban'); ban=args[k+1]; del args[k:k+2]
    sys.exit(run(args[0],ban))
