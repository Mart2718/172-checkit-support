# PR4 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-24. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: it redid every long division and brute-forced all 23,040 problems the CheckIt generator can produce. Every key is right and each item has exactly one correct choice. It found wrong arithmetic in three distractor explanations, two Quick Summary lines that answered items, a figure that contradicted its item, unclear spoken math, and a coverage gap. All are fixed (below).
- Diagrams: long division layouts for the first exposure to each step (divide, multiply and subtract, divide again, when to stop), the missing-term setup, and two students' work in Spot the Slip. Each has a caption that reads the layout row by row.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Divide 1, Divide 4: the explanations gave arithmetic for the wrong-sign distractors that did not produce them. They now name the real slip, such as \( 3x^{2}-(-9x^{2})=+12x^{2} \) written as −12, and subtracting in the wrong order, 60 − 62.
2. The Quick Summary no longer gives away Predict (the shape of the quotient and remainder), Write It ("the form CheckIt wants"), or Stop or Go On? (when to stop).
3. Divide 3's figure now leaves a visible gap where the x² term would go and puts 2x above −25x. The caption says so.
4. Coverage: 1 in 6 CheckIt problems has leading coefficient ±1. Divide 2 now divides −x³ + 3x² + 11x − 19, with its hidden −1.
5. Screen readers now hear "end quantity" at the end of each product in Check It and Slip 3.
6. Every distractor's origin is named in the feedback, including the remaining Spot the Slip choices and Predict.
7. Look Ahead: "slant asymptote" is precalculus vocabulary; calculus confirms it with limits.
8. Math in prompts is written as math, so screen readers read x² as "x squared".
9. Correct answers are spread across a, b, c, d, and the correct choice is never the widest.

## Advisory (not changed)
- Spot the Slip choices write their math in plain text (x², 4x³), the same as PR3 and TE2. Writing them as rendered math made axe flag label-in-name mismatches on those buttons.
- Worked-examples document: fractions print flattened, such as (x+2)/(x²−6x+5), and figure descriptions start with "Plotted data:". This comes from the shared document tool. The tool now prints ÷ correctly; it printed "div" before, so the EL1 document was regenerated too.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning
  - each answer button's onclick carries the answer key in the page source

## Source note (CheckIt, not this page)
TBIL's PR4 generator checks out. It builds f = q·g + r with g = (x − a)(x − b), q = k(x − c) with k from ±1 to ±6, and r = x − d, all from distinct values 1 to 6 with random signs. So every answer has a degree 1 quotient and a remainder with leading coefficient 1. About 1 in 13 problems has a 0 coefficient in the cubic, almost always the x² term.

## Needs a live screen reader
- How NVDA reads the long division captions and the plain-text superscripts in the Spot the Slip buttons, and whether feedback is announced once.
