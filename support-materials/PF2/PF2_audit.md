# PF2 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-17. Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), rendered-math reflow at 320 px with and without the WCAG text-spacing override, a numeric check of every answer, distractor, and labeled graph point, and an independent agent that saw only the page and the checklist.

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: 1 confirmed issue and 3 potential issues specific to PF2. All PF2-specific ones are fixed (below). Every keyed answer is correct and every distractor is wrong (checked twice, independently). Graph colors pass 1.4.11: curve 6.09:1, dashed lines 5.48:1, points 7.79:1.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology (NVDA especially, for the spoken math and graph captions).

## Fixed before publishing
1. (1.1.1) Graph 2 caption said every piece's ends climb toward the dashed lines. The downward pieces drop. The caption now describes each direction correctly.
2. (1.1.1) Graph 3 caption did not say which partial shape appears at each edge. It now names both.
3. (1.3.3) One feedback line referred to "the first answer". It now names the answer.
4. Two Spot the Slip prompts were read before the guess as "negative pi over 4 plus k pi", which can be heard as one fraction. The prompts now say "plus any multiple of" between separate math pieces.
5. Figure titles now consistently mention the labeled points. Feedback now explains every distractor.
6. Graph labels were small once the graph was scaled into the page (about 6 to 9 pixels). The PF2 figures now use larger text and wider spacing, and Graph 4 uses a narrower window.
7. axe flagged label-in-name on Spot the Slip choices that put math mid-sentence. Those choices were reworded so the math comes last; axe is now clean.

## Advisory (shared template, not changed)
- The standalone page has no link back to the hub (2.4.5 is met by the hub itself, but a footer link would help).
- Each SVG's caption is both visible and referenced by aria-describedby, so a screen reader may read it twice.
- Feedback speech drops "the fraction … end fraction" for short fractions ("pi over 6 plus k pi over 3"). It affects feedback only on this page; pre-guess prompts were reworded around it.
- Spoken readings of (−∞, ∞) add "all real numbers", which is not on screen. Accurate, not a giveaway.
- Same items as earlier outcomes: feedback is both a live region and focused; panel tabindex differs; new-tab links have no warning; "I think:" prefix vs label-in-name; forced colors; KaTeX CDN fallback; the summary table scrolls inside its own region at 320 px.

## Source notes (CheckIt, not this page)
- The figures are drawn by tools/figures/make_pf2.py, which labels x in multiples of π/4.
- Confirmed from a CheckIt screenshot (2026-10-17): CheckIt keeps a negative inside, as in tan(−4x), and writes a shift with the number first, as in sec(−(3/2)π + x). The page now uses those forms, and a new item (Reading the Notation) practices reading the shift-first form.
- The template's speech reads −(3/2)π as "negative 3 over 2 pi", which can be heard as 3 over 2π. The feedback and summary that use this form also say it in plain words ("negative three halves of π, plus x").

## Needs a live screen reader
- How NVDA reads each equation, interval, and graph caption, and whether feedback is announced once.
- Forced-colors and 200%/400% zoom rendering of the graphs.
