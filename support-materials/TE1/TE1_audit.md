# TE1 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-20. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a numeric check of every answer and distractor
- an independent agent that saw only the page, the CheckIt generator, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: all 21 keyed answers recompute correctly. Each item has exactly one correct choice, and no two choices are equal. The correct choice is never the widest, measured as rendered width. One wrong claim in an explanation and one PDF flattening bug were found, and both are fixed (below).
- Diagrams: one is shown the first time each problem type appears.
  - a unit circle marked in twelfths
  - an angle built as π/3 + π/4
  - π/8 as half of π/4
  - a reference triangle for every Pythagorean identity item
  - a graph for the first power-reducing item, which students can use to check the answer
  
  Unknowns are marked with an orange "?", so color is never the only signal. Labels that cross a line have a light halo so they stay readable.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Identity 1 feedback called −12/5 the tangent. It is the cotangent, and the feedback now says so.
2. Worked-examples PDF: "\sin\tfrac{5\pi}{4}" flattened to "sin(5π)/4", which reads as sin(5π) divided by 4. Every sine or cosine of a fraction now has parentheses around its argument, so it prints as "sin((5π)/4)".
3. Spot the Slip reused the triangles and angles from earlier items, so it answered them. The slips now use new values: sin(5π/12), cos θ = 20/29, sin θ = 7/25, and cos(3π/8). One distractor whose own arithmetic was wrong was rewritten.
4. Build 4 now uses a negative angle, sin(−5π/8), because CheckIt gives negative angles. The summary adds three facts about how CheckIt writes things:
   - sin(−θ) = −sin θ.
   - "Quadrant 2" means Quadrant II.
   - 3 sin(4x)^2 means 3 sin²(4x).
5. The Build intro defines "unit-circle angles" as multiples of π/6 and π/4. Build 1 feedback no longer sounds as if a distractor were correct.
6. Fractions inside answer buttons now render full size.
7. Distractor origins were added to the feedback for Exact 2, Exact 4, Identity 3, and Reduce 4. One speak line was clarified ("end root").

## Advisory (not changed)
- Worked-examples document: radicals and fractions print in flattened form, for example "(√6+√2)/4", and figure descriptions start with "Plotted data:". This comes from the shared document tool and is the same for every outcome.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning

## Source note (CheckIt, not this page)
TBIL's TE1 generator checks out:
- Exact values: angles are ±π/12 or ±π/8 plus a multiple of π/2. Their exact values come from the sum, difference, or half-angle formulas.
- Pythagorean identity: the quadrant signs are applied correctly.
- Power reducing: the outputs are correct.

Sage may print equivalent forms that look different from a textbook's. For example, a power-reducing answer can come out as −3/2·cos(8x) + 3/2, and a radical can be arranged differently. The page tells students to check their form with a calculator. The outcome names the double-angle and tangent formulas, but the generator does not test them.

## Needs a live screen reader
- How NVDA reads the nested radicals in the answer buttons, such as "the square root of the quantity 2 plus the square root of 2", and whether feedback is announced once.

## Update 2026-10-21: reflow fix
- Slip 4 work now wraps onto three lines. With the WCAG 1.4.12 text-spacing override at 320 px, it had been 332 px wide (1.4.10). The worked-examples document was regenerated, and function names no longer run together.
