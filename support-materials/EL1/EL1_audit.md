# WCAG 2.1 AA Audit — EL1 Support: Introduction to Exponentials
Date: 2026-10-17 | Standard: WCAG 2.1 AA | Checked via: build guardrails, checkit_lint, axe-core (all tabs, 1000px and 320px embed), spoken-math review, plus an independent agent pass that did not see the first-pass results.

## Summary
2 blocking issues found and fixed, 7 advisory (all in the shared template, same pattern as FN1/EL3/EL4), 4 items for a real screen reader.

## Blocking (fixed in content/EL1.yml)
1. 1.1.1 / 1.3.1 — h(x) = 2^(3x−1) display equation: spoken text "2 to the power 3 x minus 1" could be heard as 2^(3x) − 1, the very misconception behind the distractor 63. Now: "2 to the power of the quantity 3 x minus 1, end quantity".
2. 1.1.1 — Equation 3, option c, "negative 3 times negative 2 to the x" could be heard as −3·(−(2^x)). Now: "negative 3 times the quantity negative 2, to the x".

## First-pass findings fixed before the independent pass
- Duplicate region label on the four data tables (axe landmark-unique): each table now has its own label ("Table 1 of x and y values", …).
- A plain "−6" answer button failed axe label-content-name (as EL3's negative answers do): replaced by "6".

## Advisory (shared template, not changed, because it would alter FN1/EL3/EL4 behavior)
1. Feedback region: hidden→shown, aria-live polite, and also focused. Works, but may be read twice or not at all; choose one approach. Shift+Tab from the feedback lands on the last button, not the one guessed.
2. The ✓ prefix becomes part of the button name and also appears on wrong guesses.
3. Every table-wrap is a tab stop (tabindex=0) even when it does not overflow; Quick Summary has two stops (panel plus region).
4. Arrow-key tab switching briefly focuses the heading before returning focus to the tab.
5. nav wraps a tablist (duplicate label); in embed mode the clipped h1 is a second h1 beside the host page's.
6. aria-pressed on single-choice answers announces "toggle button"; a radio group would fit better.
7. If the KaTeX CDN fails, inline math falls back to raw LaTeX in prompts, explanations and point pairs; button names and display equations survive. Consider bundling KaTeX. The host page's iframe needs a title (the LibreTexts code has one).
Also noted: texToSpeech reads a multi-term exponent such as 2^(3x−1) as "2 to the power 3 x minus 1," in feedback. No EL1 feedback text contains one, but the function should say "of the quantity … end quantity" for the next outcomes.

## Verified passing
lang and title; heading order; table captions and scope headers; contrast (every text pair 5.3:1 or better, UI at least 3.04:1); no color-only meaning; no horizontal scroll at 320px or with text spacing overrides; tab roles, roving tabindex and arrow/Home/End keys; visible focus; no keyboard traps; embed mode drops the Video tab; nothing that reveals an answer is exposed before a guess.

## Needs a real screen reader (NVDA)
- Whether the focused feedback is read once or twice.
- Whether the rewritten math in feedback reads as one clean phrase.
- Whether the role="img" display equations announce as expected.
- Whether arrow-key tab switching announces cleanly.

---
This is an AI-assisted audit, not a compliance certification. For DOJ Title II sign-off, route this report through SAC/RSCCD's accessibility or DSPS office, or an outside accessibility specialist who can test with real assistive technology.
