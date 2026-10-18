# EL5 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-17. Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), a spoken-math review, and an independent agent that saw only the page and the checklist.

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: 2 blocking items, 11 advisory. Both blocking items were fixed (below). Every answer and distractor was also checked numerically.
- This is an AI-assisted audit, not a compliance certification. For DOJ Title II sign-off, route it through SAC/RSCCD's accessibility or DSPS office, or a specialist who can test with real assistive technology (NVDA especially, for the spoken math).

## Fixed before publishing
1. Spoken math in the feedback text and Quick Summary was ambiguous ("log base 2 of x plus log base 2 of y" could be heard as log of a sum, and "the quantity …" had no end marker). The shared speech function now says "…, end quantity", puts a comma before a following plus, minus, or times, says "times" between a power and the next factor, and reads a single fraction without a redundant "the quantity". The earlier pages were re-tested on all 433 math expressions: only EL3 and EL4 logarithm readings changed, and only by those added markers.
2. Expand 3 spoken label could be heard as an exponent of negative 2 times z cubed. Reworded with commas.
3. Display math pushed the page 1 pixel wider than a 320 px screen on the Spot the Slip tab. Display math is now slightly smaller at 360 px and under. Rechecked on every tab.
4. "Spot the Slip 3" answer used a minus sign symbol that some screen-reader settings read as "minus". It now says "negative 2".

## Advisory (shared template, not changed; same family as the EL1 and EL2 notes)
- Feedback region: it is hidden then shown, with live-region and focus both used, so a screen reader may announce it twice or not at all. Needs an NVDA check.
- Each answer group is named only by the question, not by the expression above it.
- Tab semantics: the video tab has no focusable content or tabindex, and the tab panel moves focus to the heading on click.
- A tab list sits inside a nav landmark.
- Forced-colors mode: the selected tab and pressed answer rely on color and an inset ring.
- The "✓" prefix after an answer is read as "check mark" for buttons with no aria-label.
- Every answer button starts with "I think:", which makes voice-control targeting by name harder (the criterion is still met).
- Skip-link focus ring is about 3:1 (orange on navy).
- If the KaTeX CDN is blocked, explanations show raw LaTeX with no spoken form.

## Needs a live screen reader
- How NVDA reads each equation and answer button, and whether feedback is announced once.
- Forced-colors and 200%/400% zoom rendering.

## Update 2026-10-17: Spot the Slip tab and feedback fixes
- Feedback no longer refers to choices by letter (Rewrite 2, Rewrite 4, Expand 3, Expand 4); it names the answer instead. The Spot the Slip intro no longer says every line has a mistake, a correct-work item was added, and the choices were rebalanced so the correct one is never the only longest.
- Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), rendered-math reflow at 320 px with and without the WCAG text-spacing override, a numeric check of every answer, and an independent agent review of the changed parts.
- Result: axe-core 0 violations on every tab; every keyed answer verified twice, independently. Each tab has one item with correct work, in a different position on each page, and every prompt asks "What is the mistake, if any?" No correct choice is the only longest one.
- Fixed after the independent review: four prompts said "What is the mistake?" while the correct-work item said "if any", which gave it away; all now say "if any". One "There is no mistake" choice had an extra sentence; it now matches the others. One equation widened the page at 320 px with text spacing; it is now on two lines.
- Note: some answer buttons put math in a sentence ("…, so the asymptote is y = 1"). axe's best-practice rule on label-in-name can flag these; the visible words come first in each spoken name, so voice-control users can still activate them.
