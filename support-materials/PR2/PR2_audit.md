# PR2 accessibility audit (WCAG 2.1 AA)

Date: 2026-11-01. Checked by:
- build guardrails and lint, and the rule checks in `tools/rules_check.py`
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: all 17 keys are correct, and every model is one CheckIt can produce (the projectile root pairs and the minimum-age and minimum-cost loops were checked). It confirmed from the generator that CheckIt evaluates the least cost and the least age at the rounded input. One explanation had wrong arithmetic (Slip 2, below).
- Diagram: a projectile's height over time on labeled axes; its description starts closed.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Slip 2: the explanation said 1,264 feet came from adding 784; it comes from leaving out the −16t² term, 112(7) + 480.
2. Convergence giveaways: in the When tab and Rounding the Year, every distractor was one change away from the key. Each item now mixes single and double mistakes (for example, −8 seconds drops both the minus and the 2).
3. The projectile graph showed the first item's answer before the guess. It now goes with The Constant Term, where it supports the question without answering it.
4. From the Ground and Greatest Height: the choices no longer form an evenly spaced list with the key second; one distractor in each now comes from forgetting to square.
5. Reading the Vertex no longer states the launch height, which answered The Constant Term in the same tab.
6. CheckIt's printing: the Quick Summary says CheckIt prints 2479.2 for $2,479.20 and 4.0 for 4 seconds, that a vertex at exactly .5 rounds up, and that the rounded-input cost can differ by up to about 20 cents. Coefficients no longer carry trailing zeros (45.1, not 45.10), as on CheckIt.

## Advisory (not changed)
- Some distractors are outside CheckIt's answer range (3,800 widgets, the year 2020); they are kept because they come from real mistakes.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
1. The least age and least cost are computed at the rounded year or number of units, not at the exact vertex. For costs this changes the answer in about 70% of problems, by up to about 20 cents.
2. In three age cases (a = 0.002 with b = −0.35, −0.41 or −0.47) the vertex is exactly x.5 but computes as x.4999…, so CheckIt's key rounds down (1987, 2002, 2017).
3. About a fifth of projectiles start at "an initial height of 0 feet"; about 56% peak at a half second. Whole-second times print as 4.0.
4. The projectile template passes r1 without using it; the cost loop rejects about 30% of draws, so a = 0.1 almost never appears.

## Needs a live screen reader
- How NVDA reads decimal coefficients and the collapsed graph description, and whether feedback is announced once.

## Dr. Romero's math review (2026-11-01)
An outside AI math check found no wrong keys. Applied: the Quick Summary separates whole-number inputs (use the nearest whole number to the vertex) from continuous ones such as time (keep the vertex unrounded); Least Average Age now computes at the unrounded vertex; Slip 4 no longer has a defensible second answer and no longer argues from what an average age "should" be.
