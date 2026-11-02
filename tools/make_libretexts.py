"""Writes support-materials/<CODE>/<CODE>_libretexts_page.html from a reference page, swapping in this outcome's
code, outcome text (from TBIL's bank.xml, passed on the command line), hub summary and video intro.
Usage: python3 tools/make_libretexts.py NEW_CODE REF_CODE "Outcome text." """
import sys, os, re, yaml
new, ref, outcome = sys.argv[1].upper(), sys.argv[2].upper(), sys.argv[3]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(root, 'support-materials', ref, f'{ref}_libretexts_page.html'), encoding='utf-8').read()
cr = yaml.safe_load(open(os.path.join(root, 'content', f'{ref}.yml'), encoding='utf-8'))
cn = yaml.safe_load(open(os.path.join(root, 'content', f'{new}.yml'), encoding='utf-8'))
s = re.sub(r'(<p><strong>' + ref + r':</strong> )(.*?)(</p>)', lambda m: m.group(1) + outcome + m.group(3), s, count=1)
assert cr['videoIntro'] in s and cr['hubSummary'] in s
s = s.replace(cr['videoIntro'], cn['videoIntro']).replace(cr['hubSummary'], cn['hubSummary'])
if cr.get('video'):   # the reference has a real video; put the coming-soon note back for the new outcome
    s = re.sub(r'<p><a href="https://youtu\.be/[^"]+"[^>]*>.*?</a></p>\s*<p><iframe[^>]*youtube[^>]*></iframe></p>',
               '<p><em>The video walkthrough is coming soon. In the meantime, the Quick Summary and the Try It tabs cover the same ideas.</em></p>', s, flags=re.S)
s = s.replace(ref, new).replace(ref.lower(), new.lower())
os.makedirs(os.path.join(root, 'support-materials', new), exist_ok=True)
open(os.path.join(root, 'support-materials', new, f'{new}_libretexts_page.html'), 'w', encoding='utf-8').write(s)
print('wrote', new, 'from', ref)
