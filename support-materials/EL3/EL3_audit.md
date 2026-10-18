# WCAG 2.1 AA Audit: EL3 Support (https://172checkit.netlify.app/el3/)
Date: 2026-10-15 | Standard: WCAG 2.1 AA | Checked via: build guardrails, checkit_lint, axe (all tabs, 1000px standalone and 320px embed), math verification, independent agent pass

## Summary
0 blocking issues. 7 advisory items from the independent pass (all in the shared template, so they apply to every outcome page). 1 item fixed on this page. Items needing manual assistive-tech verification are listed at the end.

## Automated results
- Build guardrails: no missing captions, correct answers are among the choices, no unbalanced math delimiters, every choice with math has a spoken reading, every display equation has a spoken reading.
- checkit_lint: PASS. axe: 0 violations on every tab (standalone 1000px, embed 320px).
- Math check (sympy): all 10 items verified, including the distractors, which are each false.
- Independent agent (given only the page and the checklist): 0 violations; contrast measured 6.25:1 to 12:1; reflow at 320px passes; keyboard operation passes; tab pattern and aria-pressed correct.

## Fixed on this page
- The negative-number answer buttons (-2, -9, -100) now announce "negative 2" and so on instead of relying on the screen reader's reading of a minus sign.

## Advisory (shared template; not changed, so FN1 and EL4 stay as they are)
1. 4.1.3 Status messages: the answer feedback region is revealed and focused in one step. Some screen readers may skip the live announcement or read it twice. Suggested fix: an always-present empty role="status" region that is filled, and no focus move, or keep the focus move and drop aria-live.
2. 2.4.3 Focus order: after answering, focus moves to the feedback box, so Shift+Tab lands on the last answer rather than the one pressed.
3. 2.5.3 Label in Name: the visible label of a math answer is symbols, and the accessible name is words. Acceptable for symbolic content; check with Voice Control or Dragon.
4. Tab pattern: activating a tab with the keyboard moves focus to the panel heading instead of staying on the tab.
5. The Video panel has no tabindex="0" and no focusable content, so Tab skips from the tablist to the footer.
6. Landmarks: the tablist sits inside a nav landmark, although tabs are not navigation links.
7. No link back to the hub page from an outcome page (the footer link is hidden in embed mode, which is fine).
Minor: answer buttons use aria-pressed for a single-choice set; a radio group would be more idiomatic.

## Needs manual verification
Screen-reader pass (NVDA/JAWS/VoiceOver) of the spoken math in the feedback region and the Quick Summary table; Voice Control or Dragon with the math answer buttons; the recorded video's human-reviewed captions.

---
This is an AI-assisted audit, not a compliance certification. For DOJ Title II sign-off, route this report through SAC/RSCCD's accessibility or DSPS office, or an outside accessibility specialist who can test with real assistive technology.

## Update 2026-10-17: Spot the Slip tab
- Added a Spot the Slip tab (5 items): swapped base and exponent in both directions, dividing instead of finding the power, a negative log, and a correct base-10 case. The answer buttons showing −2, −9, and −100 (Evaluate and Common & Natural Logs) no longer carry a separate spoken label: axe flagged the mismatch, and screen readers read the minus sign on their own.
- Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), rendered-math reflow at 320 px with and without the WCAG text-spacing override, a numeric check of every answer, and an independent agent review of the changed parts.
- Result: axe-core 0 violations on every tab; every keyed answer verified twice, independently. Each tab has one item with correct work, in a different position on each page, and every prompt asks "What is the mistake, if any?" No correct choice is the only longest one.
- Fixed after the independent review: one feedback line was reworded so it is not read as "the natural log, natural log".
- Note: some answer buttons put math in a sentence ("…, so the asymptote is y = 1"). axe's best-practice rule on label-in-name can flag these; the visible words come first in each spoken name, so voice-control users can still activate them.
