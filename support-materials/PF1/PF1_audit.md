# PF1 accessibility audit (WCAG 2.1 AA)

Date: 2026-11-02. Checked by:
- build guardrails and lint, and the rule checks in `tools/rules_check.py`
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: one item had two choices that were secretly the same function (Graph 3, below). Every other key, distractor and explanation step checked out, and the first two graphs match CheckIt's window and ticks.
- Diagrams: three graphs of two full periods; their descriptions start closed, since reading the graph is the skill.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Graph 3: two of its choices simplified to the same function, one was outside CheckIt's range, and its key drew the same curve as Graph 1. It is now 2cos(4x − 4π/3), a visibly shifted graph, with four different functions as choices (checked numerically), ticks every π/4 as CheckIt draws them, and no marked point.
2. Where a Cycle Starts: the choices no longer point to the key (one distractor now makes two slips).
3. Coverage: about half of CheckIt's phase shifts are π or more, often several periods. Shift 1 is now 4π to the right, Shift 2 is 4π/3 to the left, and Slip 1 is 3π/2 to the right. The Quick Summary says how CheckIt prints the number inside (8/3 π) and how it draws the graph.
4. Displays narrowed so they fit a phone screen with text spacing; wording fixes in two slip explanations.

## Advisory (not changed)
- The worked-examples document prints math in italics, including digits and words.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
1. f prints unfactored, such as 2 sin(4x + 8/3 π). With no shift, the key says "0 to the left".
2. The phase shift is π or more in about half of problems and longer than a period in most; in 69 of 81 cases the shift is a whole number of quarter periods, so the graph looks like an unshifted ±a sin or ±a cos.
3. The graph's window is from min(0, −c/b) to two periods past the shift, with x ticks every π/b and no points marked. Its image has no text description (description="."). The template asks "What is the phase shift f(x)?" (missing "of").

## Needs a live screen reader
- How NVDA reads the long function speak lines and the graph descriptions, and whether feedback is announced once.
