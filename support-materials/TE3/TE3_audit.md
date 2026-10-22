# TE3 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-21. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a brute-force check of every solution set
- an independent agent that saw only the page, the CheckIt generator, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: its brute-force solver confirmed every key. Each item has exactly one correct choice, and no distractor is an equivalent set. It found one figure that gave its answer away, a garbled screen-reader reading, and a few wording and coverage items. All are fixed (below).
- Diagrams: unit circles crossed by y = value, x = value, or the line y = mx (for tangent), with the crossing points marked but not named, so the student still identifies the angles. A one-lap and two-lap picture introduces multiple angles.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Unit Circle 2: the figure showed both crossings on the left of the y-axis, and only one choice fit that. Every choice is now an angle or pair on the left side.
2. Spot the Slip 2: "tan of pi over 3" was read as "tangent of the fraction over, end fraction pi 3". It now reads correctly, and the PDF prints tan(π/3).
3. CheckIt coverage:
   - Unit Circle 3 is now 3 sec θ − 2√3 = 0, which needs a flip plus rationalizing. Its distractor "no solution, cosine cannot be more than 1" tests whether students flip before judging.
   - All Solutions 3 is now a cotangent equation.
   - Multiple Angle 3 is sin(2θ) = 0, where θ = 0 counts.
4. The Quick Summary no longer uses the items' own equations or answers as its examples.
5. Squared 1's figure now draws only the + line, so the ± step is the student's.
6. Feedback names choices instead of their positions. It adds missing distractor origins and says cosecant is never strictly between −1 and 1.
7. Spot the Slip prompts now write their equations as math, not plain text.
8. Correct answers are spread across a, b, c, d, and the correct choice is never the widest.

## Advisory (not changed)
- Worked-examples document: fractions print flattened, such as (4π)/3, and figure descriptions start with "Plotted data:". This comes from the shared document tool and is the same for every outcome.
- Spot the Slip 4, sec θ = 1/2, is a no-solution case. CheckIt's generator never gives one, but it is kept as a misconception check.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning

## Source note (CheckIt, not this page)
TBIL's TE3 generator checks out. It gives three tasks:
1. All solutions of f(θ) = a special value, keyed as "θ = a + 2πk, b + 2πk for all integers k". Tangent and cotangent are also written in two 2πk lists rather than +πk.
2. sin²θ or cos²θ = a value on [0, 2π).
3. sin(cθ) or cos(cθ) = a value on [0, 2π), with c = 2, 3, or 4.

Every value is one the function can reach, so CheckIt never gives a no-solution equation.

## Needs a live screen reader
- How NVDA reads the comma-separated angle lists in the answer buttons, and whether feedback is announced once.
