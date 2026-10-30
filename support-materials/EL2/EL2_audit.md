# WCAG 2.1 AA Audit — EL2 Support: Graphing Exponential Functions
Date: 2026-10-17 | Standard: WCAG 2.1 AA | Checked via: build guardrails, checkit_lint, axe-core (all tabs, 1000px and 320px embed), sympy check of every answer, spoken-math review, plus an independent agent pass that did not see the first-pass results.

## Summary
2 blocking issues found and fixed, 9 advisory (shared template, same pattern as earlier pages, plus one content item fixed), 4 items for a real screen reader.

## Blocking (fixed)
1. 1.1.1 / 1.3.1 — Hand-written spoken labels such as "f of x equals 2 to the x plus 3" could be heard as 2 to the power (x plus 3), which is a different function in this outcome (Asymptote 3). Every spoken form now puts a comma after a simple exponent that is followed by a plus or minus ("2 to the x, plus 3"), and multi-term exponents say "to the power of the quantity x plus 3, end quantity".
2. 1.3.1 — The shared spoken-math function (template/app.js) did not mark the end of a simple exponent in feedback text, so "2 to the power x minus 1" and "2 to the power of the quantity x minus 1" differed by a few words. It now adds the comma, and also says "the negative of 2 to the x" for a minus sign in front of a power, so a flip is not confused with a negative base. A regression comparison over all 276 math expressions on FN1, EL1, EL2, EL3 and EL4 showed changes only in EL2 content.

## First-pass findings fixed
- Quick Summary example "-2^(x+3)" was identical to the Asymptote 3 question and gave away its answer; replaced with "3^(x-4)".

## Advisory (shared template, not changed, because it would alter earlier pages)
1. Feedback region is hidden, then shown, aria-live polite, and also focused. Works, but may be read twice or not at all.
2. Plain-text answer buttons ("−3", "(−∞, 2)") are read from the symbols, not from words; the ✓ prefix is part of the name and could be hidden from assistive technology.
3. Figure text may be read up to three times (name, description, visible caption).
4. Tab labels differ slightly from their headings; the nav wraps a tablist; table regions are tab stops even when nothing scrolls; the Quick Summary panel has tabindex 0.
5. Main lacks tabindex -1 for the skip link (older Safari); target=_blank links give no warning; the host page needs an iframe title (the LibreTexts code has one).
6. Graph text renders small at 320px wide (about 9.5px). Gridlines are decorative.
7. If the KaTeX CDN fails, explanations show raw LaTeX; display equations and math buttons keep their labels.
8. Click or Enter on a tab moves focus to its heading.
9. Arrow keys move focus to the heading and back to the tab.

## Verified passing
lang and title; heading order; each SVG has role img, a name and a linked caption, and each caption is enough to answer its question without sight; no answer is exposed before a guess; contrast 4.6:1 or better; the curve and dashed line differ by dash pattern, not color alone; no horizontal scroll at 320px or with text spacing overrides; tab roles, roving tabindex and arrow/Home/End keys; visible focus; no traps; embed mode drops the Video tab.

## Needs a real screen reader (NVDA)
- Whether the feedback is spoken once, twice or not at all.
- Whether the SVG children under role img are hidden from the screen reader.
- How "(", "−" and "∞" are read at default punctuation settings.
- Whether "end quantity" is understood by students.

---
This is an AI-assisted audit, not a compliance certification. For DOJ Title II sign-off, route this report through SAC/RSCCD's accessibility or DSPS office, or an outside accessibility specialist who can test with real assistive technology.

## Update 2026-10-17: Spot the Slip tab
- Added a Spot the Slip tab (5 items): a shift inside the exponent, a flipped range, a forgotten vertical shift, a negative exponent vs a flip, and a correct case.
- Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), rendered-math reflow at 320 px with and without the WCAG text-spacing override, a numeric check of every answer, and an independent agent review of the changed parts.
- Result: axe-core 0 violations on every tab; every keyed answer verified twice, independently. Each tab has one item with correct work, in a different position on each page, and every prompt asks "What is the mistake, if any?" No correct choice is the only longest one.
- Fixed after the independent review: spoken readings of -2^x and -e^x now say "the negative of 2 to the x" so they are not heard as (-2)^x.
- Note: some answer buttons put math in a sentence ("…, so the asymptote is y = 1"). axe's best-practice rule on label-in-name can flag these; the visible words come first in each spoken name, so voice-control users can still activate them.

## Update 2026-10-30: graph descriptions that gave answers away
- Graph 2 (range): its text description now sits in a closed "Text description of the graph" disclosure, because it read the range off the graph for the student. Screen readers still get it through aria-describedby. Canvas quiz regenerated.
- Found in a sweep of every graph description after the FN3 audit, with an independent second opinion.
