# EL6 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-17. Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), rendered-math reflow at 320 px, a numeric check of every answer and distractor, and an independent agent that saw only the page and the checklist.

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: 0 confirmed failures, 3 potential (all shared-template or host-page items, below), several advisory. All 16 keyed answers are correct and all 48 distractors are wrong (checked twice, independently).
- This is an AI-assisted audit, not a compliance certification. For DOJ Title II sign-off, route it through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology (NVDA especially, for the spoken math).

## Fixed before publishing
1. Spot the Slip student work was written on one line ("… so … so …") and pushed the page to 420 px wide on a phone. Each student's work is now stacked as separate lines, and the spoken label reads "Next line:" between them. The worked-examples generator was taught to print stacked lines (one centered line per row). No earlier outcome uses stacked lines, so their documents are unchanged.
2. Feedback referred to "Choice b" and similar, but the page shows no letters on the answer buttons. Feedback now names the answer itself (for example "The answer \( \tfrac{512}{5} \) …"), which reads correctly on the page, in the Word/PDF document, and in the Canvas quiz.
3. Spot the Slip intro said every line has a mistake, which ruled out the "There is no mistake" choice before guessing. It now asks students to decide whether the work is right. Two correct choices were also much longer than their distractors (and one stated the fix). Lengths are now balanced.
4. Logarithmic 1 feedback included "5 times 8 over 5", which can be heard as (5·8)/5. That check was removed; the remaining check is unambiguous.

## Potential (needs testing; not changed)
- 2.5.3 Label in Name: math answer buttons have a spoken name ("x equals log base 3 of 7, minus 4") that differs from the visible symbols. Every name starts with the visible "I think:", which likely passes. Shared template; test with Voice Control or Dragon.
- 4.1.3 Status messages: feedback is both a live region and receives focus while going from hidden to shown. Same as the EL1, EL2, and EL5 notes. Shared template; needs an NVDA check.
- The embedding iframe needs a title. The LibreTexts code in this folder already includes one.

## Advisory (shared template, not changed)
- The feedback speech function reads exponents without an "end power" marker, and turns an aligned block into letters. Display math is unaffected (it uses the written spoken label), and no EL6 feedback uses aligned.
- Earlier outcomes (at least EL5) also refer to "Choice b" in feedback and say "each one has a mistake" in Spot the Slip. Worth the same fix when convenient.
- Answer groups behave like radio buttons but use toggle buttons; tab panels differ in tabindex; links that open a new tab don't say so; plus the items already listed in the EL5 notes (forced colors, "I think:" prefix, skip-link ring, KaTeX CDN fallback).
- The summary table scrolls sideways inside its own labeled, focusable region at 320 px. Data tables are allowed to do this; the page itself does not scroll sideways.

## Needs a live screen reader
- How NVDA reads each equation, answer button, and the stacked student work, and whether feedback is announced once.
- Forced-colors and 200%/400% zoom rendering.
