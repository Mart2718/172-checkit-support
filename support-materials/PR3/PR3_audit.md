# PR3 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-22. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- an independent agent that saw only the page, the CheckIt generator, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key is correct and each item has exactly one correct choice. It found one explanation that referred to choices by position, graph text that was too small, spoken math that did not say where a square applies, and a coverage gap. All are fixed (below).
- Diagrams: each Match graph labels both zeros and the y-intercept, with its own y-scale, so students read what happens at each zero and at the ends.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Zeros 4 feedback now names the wrong descriptions instead of "the second choice", "the third", and so on.
2. Graph text was about 7–11 px at the page's 340 px figure width. The figures are redrawn at a smaller viewBox with larger type, about 18 px on screen. Match 3's y-intercept label is moved off the curve.
3. Screen readers now hear "the quantity x plus 3, end quantity, squared", so it is clear the square applies to the whole factor.
4. Coverage: CheckIt asks students to sketch from a formula. Match 4 is now a formula-to-sketch item ("Sketch It"): pick the left-to-right description of the graph.
5. Zeros 1 and Intercept 1 put the squared factor second, so students see that factor order does not matter.
6. The Quick Summary example no longer overlaps an item's numbers.

## Advisory (not changed)
- Spot the Slip prompts write the function in plain text, the same as TE2.
- Worked-examples document: figure descriptions start with "Plotted data:". This comes from the shared document tool and is the same for every outcome.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning

## Source note (CheckIt, not this page)
TBIL's PR3 generator gives f(x) = k(x − a)²(x − b)ⁿ and asks for the zeros with their multiplicities, the end behavior, and a sketch. When both zeros have the same sign, the y-intercept can fall outside the graphing window CheckIt shows.

## Needs a live screen reader
- How NVDA reads "end quantity, squared" in the formulas, and whether feedback is announced once.
