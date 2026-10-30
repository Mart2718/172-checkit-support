# FN2 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-28. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key and computation checks out. It ran the generator 20,000 times to measure coverage. It found a cross-item spoiler, two ambiguous speak lines, and three coverage gaps. All are fixed (below).
- Diagrams: three CheckIt-style graphs made of straight segments with slopes ±1 or ±2. Two zigzag, and one has two rising segments in a row.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Slip 5's prompt gave away Input to Output 2's answer. It now asks for g(4), answered with the reverse question.
2. Speech in Slip 2 and Slip 3 now says "the quantity negative 2, end quantity, squared", so it cannot be heard as −(2²).
3. Coverage:
   - Just One is a g(x) = b item with exactly one answer, at a corner. CheckIt has one solution about 40% of the time.
   - Slip 4 uses a third graph with two rising segments in a row and an endpoint answer.
   - Slip 3 now needs a fraction reduced (−6/10 = −3/5), on its own function.
4. The summary says CheckIt's graph has no dots at its ends or corners, that answers can number one or several, and that a root can come out whole. It also says the "exact values" rule is for formula answers.
5. Slip 1's distractor and Output to Inputs 1's wording are clearer. A speak line uses the page's fraction convention.
6. Piecewise displays put "f(x) =" on its own line, so they reflow at 320 px with the text-spacing override. A raw "<x" in the math was being read as an HTML tag; it is now \lt.

## Also fixed (FN4, found while building FN2)
- FN4's Quick Summary wrote "0<a<1" in two rows, and the browser read "<a" as an HTML tag. That cut the vertical and horizontal stretch rows short on the live page. Both now use \lt; FN4's worked examples and quiz were regenerated.

## Advisory (not changed)
- Some text choices write math in plain text, the same as earlier outcomes, because axe flags label-in-name mismatches on buttons that pair rendered math with a separate spoken label.
- Worked-examples document: fractions print flattened, and figure descriptions start with "Plotted data:". This comes from the shared document tool, which now prints a piecewise function as one line per piece.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning
  - the answer key in each button's onclick

## Source notes (CheckIt, not this page)
TBIL's FN2 generator checks out. Notes:
1. The x-values in its answer key come in random order with no spaces, such as "x=2.5,x=-3.5".
2. Non-integer answers are always halves, since slopes are ±1 or ±2.
3. No segment is flat, so the horizontal line always crosses the graph at single points.
4. Graphs are larger than this page's: a median width of 12 units, and heights up to about 28 units, with ticks every 1.
5. The plot draws no dots at the ends or corners. Its alt text is only "Plot".

## Needs a live screen reader
- How NVDA reads the piecewise speak lines and the three graph captions, and whether feedback is announced once.

## Update 2026-10-30: graph descriptions that gave answers away
- All seven graph descriptions now sit in a closed "Text description of the graph" disclosure. Several stated answers outright (the corner (3, 2) for g(3), the end (5, 0), the corner (−1, −2), the end (3, 0)); the rest are collapsed for consistency. Screen readers still get the full descriptions through aria-describedby. Canvas quiz regenerated.
- Found in a sweep of every graph description after the FN3 audit, with an independent second opinion.
