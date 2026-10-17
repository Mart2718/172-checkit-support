# EL7 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-17. Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), rendered-math reflow at 320 px with and without the WCAG text-spacing override, a numeric check of every answer and distractor, and an independent agent that saw only the page and the checklist.

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: 1 confirmed issue and 4 potential issues specific to EL7, all fixed (below). All 17 keyed answers are correct and every distractor is wrong (checked twice, independently).
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology (NVDA especially, for the spoken math).

## Fixed before publishing
1. (1.3.1) Feedback for the compound-interest items read the base aloud as "open paren 1 plus 0.04 over 4 close paren", which can be heard as (1+0.04)/4. That is the exact mistake those items teach. Feedback now writes the base as 1.01 (or 1.015) and says in words that the rate is divided by n. The Quick Summary row says the same thing in a sentence.
2. Find the Time: the correct choice was the only one without "about" in two items. All time choices now use the same wording.
3. Spot the Slip: the correct choice was the longest in four items. Distractors now give a reason, and the correct choices were shortened. One item (Slip 5) is correct work, so "There is no mistake" is a real option.
4. The Amount and Time tabs showed the Set Up answers in their display math. The Set Up intro now says to start there, and the later tabs show the simplified base (1.01, 1.015), not the fraction form being tested.
5. (1.4.12) With the text-spacing override at 320 px, two long equations widened the page to 325 px. Shortening them (item 4) fixed it. Rechecked on every tab.
6. One feedback line was inaccurate ("ignores the compounding"; it compounds yearly instead of quarterly), and one distractor ($39,999.70) could be ruled out by format alone. Both were replaced.

## Advisory (shared template, not changed)
- The speech function drops the "the fraction … end fraction" wrapper for short fractions, so "1 plus r over n" is ambiguous by ear wherever an equation has no written label (EL7: the summary table formula). Proposed fix: always use the long form when a fraction follows a plus, minus, or open parenthesis. This would change readings on other pages, so it needs a decision and a retest of every outcome.
- The speech function reads A(t) and P(t) as "A open paren t close paren"; the written labels say "A of t". The function's "of" rule only covers f, g, and h.
- Spoken forms use "end power" in written labels and "end quantity" in feedback.
- The same letter A is the output and the starting amount in the depreciation and half-life models. This matches TBIL's and CheckIt's notation, so it was kept.
- Same items as earlier outcomes: feedback is both a live region and focused; panel tabindex differs; new-tab links have no warning; "I think:" prefix vs label-in-name; forced colors; KaTeX CDN fallback; the summary table scrolls inside its own region at 320 px.

## Source issue (TBIL generator, not this page)
The TBIL EL7 generator computes "compounded monthly" with n = 6 instead of 12. CheckIt's answer key for monthly problems is therefore off: by about $20 for a typical problem and up to about $496 in its range. Time answers round to the same whole number. This page teaches n = 12, which is correct.

## Needs a live screen reader
- How NVDA reads each equation, answer button, and the stacked student work, and whether feedback is announced once.
- Forced-colors and 200%/400% zoom rendering.
