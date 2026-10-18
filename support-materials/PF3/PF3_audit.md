# PF3 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-17. Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), rendered-math reflow at 320 px with and without the WCAG text-spacing override, a numeric check of every answer and distractor, and an independent agent that saw only the page and the checklist.

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: 1 confirmed issue and 4 potential issues, all about spoken math. All fixed (below). Every keyed answer is correct and every distractor is wrong (checked twice, independently). No pre-guess leaks. Graph colors pass 1.4.11: curve 6.09:1, dots 7.79:1, dashed lines 5.48:1.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology (NVDA especially, for the spoken math).

## Fixed before publishing
1. (1.3.1) The shared speech function read sin⁻¹(x) as "sine to the power negative 1, times x", the exact misconception Slip 5 teaches against. It now reads "inverse sine of x" (also cosine, tangent, and the reciprocal functions).
2. The speech function did not know arcsin, arccos, or arctan, so it read "arcsin open paren x close paren". It now reads "arcsine of x".
3. CheckIt's form ½√3 was read "1 over 2 the square root of 3", which could be heard as 1 over 2√3. The speech function now says "1 over 2 times the square root of 3" when a short fraction is followed by a square root.
4. Items 1 to 3 changed the shared template. Every math expression in every outcome (804) was read with the old and new function: only the 37 PF3 expressions changed. FN1 and EL1 through PF2 read exactly as before. axe was rerun on FN1, EL1, EL5, and PF2: still 0 violations.
5. Spot the Slip lines 1 and 2 read "the square root of 3 over 2", which could be heard as the square root of 3/2. They now say "the fraction: the square root of 3, over 2."
6. Spot the Slip choices showed π/2-style text with no spoken reading ("pi slash 2"). They now use math with a written spoken reading, math at the end of the sentence.
7. Feedback now explains every distractor. Graph titles all state the curve's direction. The Quick Summary's sketch points are written as math, so they are read correctly.

## Advisory (shared template, not changed)
- Feedback is both a live region and focused; panel tabindex differs; new-tab links have no warning; "I think:" prefix vs label-in-name, and the pressed "✓" is not in the aria-label; KaTeX CDN fallback; short fractions without "the fraction … end fraction"; captions both visible and referenced by aria-describedby; no link back to the hub.
- Graph captions write coordinates such as (−1, −π/2) as text. Most screen readers say "pi slash 2"; the same is true of PF2's captions.

## Source notes (CheckIt, not this page)
- The figures are drawn by tools/figures/make_pf3.py (x in whole numbers, y in multiples of π/4).
- CheckIt prints special values the way Sage does: √3/2 as ½√3, √2/2 as ½√2, √3/3 as ⅓√3. Since 2026-10-18 the page shows the textbook form, and the Quick Summary note tells students that CheckIt's form is the same number.
- The generator moves the arctan angle away from π/2 and 3π/2, so arctan inputs are always defined.

## Needs a live screen reader
- How NVDA reads each equation, interval, and graph caption, and whether feedback is announced once.
- Forced-colors and 200%/400% zoom rendering of the graphs.

## Update 2026-10-18: textbook form for root values
- At the instructor's request, the Evaluate and More Values items now show values the usual way (√3/2, −√2/2, √3/3) instead of CheckIt's printed form (½√3). The Quick Summary note keeps one line explaining that CheckIt may print ½√3 and that it is the same number.
- The shared speech function now puts a comma after a square-root numerator ("the fraction the square root of 3, over 2"), so it is not heard as the square root of 3/2. Every math expression in every outcome was read with the old and new function: only 13 PF3 expressions changed.
- Rechecked: lint, axe-core 0 violations on every tab at both widths, 320 px reflow with and without text spacing, answer keys unchanged (π/3, 3π/4, π/6, −π/4), quiz checks pass.
