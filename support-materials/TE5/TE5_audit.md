# TE5 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-18. Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), rendered-math reflow at 320 px with and without the WCAG text-spacing override, a numeric check of every answer and of every distractor's stated origin, and an independent agent that saw only the page and the checklist.

## Result
- axe-core: 0 violations on every tab at both widths. The "needs review" items are color contrast over figures, the same as TE4.
- Independent audit: all 21 keyed answers recompute correctly, and each item has exactly one correct choice. It found 5 must-fix items and several should-fix items, all fixed (below).
- Diagrams: every Which Law, Law of Cosines, Law of Sines, and Swing item has its own triangle, labeled with that problem's givens and an orange "?" on the unknown. The question mark means color is never the only signal. The oblique triangles are drawn to scale from their side lengths, so "the longest side is across from the largest angle" matches what students see. The two height diagrams (How Many 1 and 2) are not to scale, and their captions say so.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Swing 1 and 2 used the same givens as How Many 1 and showed both triangles, which answered How Many 1 on the same tab. They now use A = 40°, b = 12, a = 9.
2. The Swing 2 prompt stated Swing 1's answer. It now says "the same two triangles as in Swing 1".
3. In Cosines (Solve) 1, the 50° angle was drawn at about 90°, which looked like a right angle in an item where the Pythagorean Theorem is a distractor. All oblique triangles are now drawn to scale.
4. (1.1.1, 1.3.1) Spoken givens such as "A equals 30 degrees. a equals 6" could not tell an angle from a side. Every speak line now says "angle A" and "side a".
5. The How Many captions now say "Not drawn to scale".
6. Captions for sides shown only as a letter now say "labeled with a letter only" instead of "not marked".
7. Slip 1 distractors now give the values those mistakes produce (15.5 with a plus, 10.0 in radians).
8. Solve 2 feedback names 48.2° as angle B. Figure titles no longer say "wide angle".
9. The Quick Summary now says that if the sine of B comes out greater than 1, no triangle fits.
10. Slip 3 feedback printed a raw "<" that HTML read as a tag, which cut off the rest of the sentence in the worked-examples document. It is now written in words.

## Advisory (not changed)
- Spot the Slip reuses triangles from earlier tabs (Slip 1 and Solve 1, Slip 5 and Solve 2, Slip 3 and How Many 1). It is the last tab, so the earlier answers are already known by then.
- Worked-examples document: fractions print flattened, e.g. "(10 sin 75°)/(sin 40°)", and figure descriptions start with "Plotted data:" (shared document tool, same as TE4).
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; captions both visible and referenced by aria-describedby; new-tab links without warning.

## Source note (CheckIt, not this page)
TBIL's TE5 generator checks out. Three sides or two sides and the angle between them use the law of cosines. Two angles and a side use the law of sines. Two sides and a non-included angle give one or two triangles. Answers are rounded to the tenth. Its text has a typo, "possiblities".

## Needs a live screen reader
- How NVDA reads the figure captions, degrees, and the stacked (aligned) equations in Spot the Slip, and whether feedback is announced once.
