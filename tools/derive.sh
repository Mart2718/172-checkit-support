#!/usr/bin/env bash
# Usage: tools/derive.sh FN1
# Builds the site, then produces derived/FN1/FN1_worked_examples.docx and .pdf (landscape, blank right third)
# from the same content file. Run by Claude in a session; needs Node, Python with beautifulsoup4, Playwright, LibreOffice.
set -e
CODE="$1"; LC=$(echo "$CODE" | tr 'A-Z' 'a-z')
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT="$ROOT/derived/$CODE"; mkdir -p "$OUT"
(cd "$ROOT" && npm run build >/dev/null)
python3 "$ROOT/tools/worked-examples/extract_items.py" "$ROOT/dist/$LC/index.html" "$OUT/items.json"
node -e "const y=require('$ROOT/node_modules/js-yaml'),fs=require('fs');const c=y.load(fs.readFileSync('$ROOT/content/$CODE.yml','utf8'));fs.writeFileSync('$OUT/meta.json',JSON.stringify(Object.assign({code:c.code},c.worked)))"
(cd "$OUT" && node "$ROOT/tools/worked-examples/shots.js" "$ROOT/dist/$LC/index.html" >/dev/null)
cp "$ROOT/tools/worked-examples/build.js" "$OUT/build.js"
(cd "$OUT" && NODE_PATH=/opt/npm-tools/node_modules node build.js && python3 /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf --outdir . "${CODE}_worked_examples.docx" >/dev/null)
echo "wrote $OUT/${CODE}_worked_examples.docx and .pdf"
