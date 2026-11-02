# FN6 accessibility audit (WCAG 2.1 AA)

Date: 2026-11-01. Checked by:
- build guardrails and lint, and the rule checks in `tools/rules_check.py`
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key, check value and distractor value recomputed correctly, and every function is one CheckIt can produce. Its must-fix findings were giveaways; all are fixed (below).
- Diagram: f(x) = (x − 1)³ + 2 and its inverse, mirror images across y = x, told apart by line style and labels as well as color; the description starts closed.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Convergence giveaways in Fraction 1, Fraction 2, Check with a Point and the root item: each now mixes single and double mistakes.
2. The graph description named the answer to A Point on Each Graph; it no longer does.
3. Distractor origins are named accurately (keeping f's numbers and flipping only the power is not "undoing in the original order").
4. The Quick Summary example no longer matches a student's wrong answer in Slip 2, and feedback in one item no longer answers another in the same tab.
5. Coverage: Fraction 1 now has a negative c, printed the way CheckIt prints it, −(3x − 1)/(2x − 5); the root item is now h(x) = (x − 2)^(1/7) − 3, with both constants negative, r = 1/7, and the name h.
6. Functions are shown in CheckIt's order, power first and constant last, and Fraction 2 is shown with the minus out front, as Sage prints it. Plain-text slip choices use ∛ and superscripts instead of ^, which screen readers read as "caret."

## Advisory (not changed)
- The worked-examples document prints stacked fractions with slashes and centers multi-line work.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
1. a, b, c, d are four different sizes from 1, 2, 3, 5, 7 with random signs, so every fraction is one-to-one.
2. Sage prints a + (x + b)^r as (x + b)^r + a, writes roots as fractional powers, and pulls a leading minus out front: (−2x + 5)/(3x + 1) prints as −(2x − 5)/(3x + 1). Confirm on one live problem before recording.
3. In Sage, a fractional power of a negative number is complex, so (−8)^(1/3) is not −2. Check values should use inputs that keep the base positive.

## Needs a live screen reader
- How NVDA reads the fractional-power speak lines and the ∛ symbol, and whether feedback is announced once.
