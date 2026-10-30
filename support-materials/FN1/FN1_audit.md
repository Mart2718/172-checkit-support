# FN1 accessibility audit (WCAG 2.1 AA)

The original FN1 page was built before audit notes were kept. This file records later changes.

## Update 2026-10-17: Spot the Slip tab
- Added a Spot the Slip tab (5 items): repeated outputs, an even power on x vs y, the vertical line test, and repeated y-values in ordered pairs.
- Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), rendered-math reflow at 320 px with and without the WCAG text-spacing override, a numeric check of every answer, and an independent agent review of the changed parts.
- Result: axe-core 0 violations on every tab; every keyed answer verified twice, independently. Each tab has one item with correct work, in a different position on each page, and every prompt asks "What is the mistake, if any?" No correct choice is the only longest one.
- Fixed after the independent review: two choices were reworded to state the rule exactly ("an input with two different outputs").
- Note: some answer buttons put math in a sentence ("…, so the asymptote is y = 1"). axe's best-practice rule on label-in-name can flag these; the visible words come first in each spoken name, so voice-control users can still activate them.

## Update 2026-10-30: graph descriptions that gave answers away
- The sideways-parabola description (Graph 2 and Slip 5) no longer lists the points in same-x pairs, which did the vertical line test for the student. It now names the leftmost point and where each branch leaves the grid. Worked examples and Canvas quiz regenerated.
- Found in a sweep of every graph description after the FN3 audit, with an independent second opinion.
