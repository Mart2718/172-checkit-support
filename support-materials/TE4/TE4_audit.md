# TE4 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-18. Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), rendered-math reflow at 320 px with and without the WCAG text-spacing override, a numeric check of every answer and distractor, and an independent agent that saw only the page and the checklist.

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: 1 confirmed content issue and 1 confirmed label issue, both fixed, plus several potential and advisory items (below). All 17 keyed answers are correct (checked twice, independently). The triangle figure passes 1.4.11: edges 5.66 to 6.09:1, right-angle marker 5.09:1, labels 7.2:1 or more. Its caption matches the drawing and never says opposite, adjacent, or hypotenuse, so it gives no more than a sighted student sees.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Spot the Slip 1 had a second defensible answer ("use angle B": a = 10 cos 50° gives the same 6.4). That choice now names a wrong value.
2. (2.5.3) Label tab buttons showed "a" while their spoken name said "side a". They now read "Side a" both ways.
3. (2.5.3) Numeric answer buttons showed "a ≈ 9.8" while the spoken name said "a is about 9.8". They now show plain text, "about 9.8", with no separate spoken label.
4. In three Spot the Slip items only the correct choice named a value. Distractors now name the value their mistake would give.
5. Label 4 used the same triangle as Angle and Side 1, so its feedback solved that item. Label 4 now uses A = 50°, c = 8.
6. Label 2's prompt defined "opposite" ("the side across from it"), which turned it into a lookup. The gloss was removed.
7. Triangle labels were small on a phone (about 10 px). They are now larger.
8. Spot the Slip student work put the triangle's given values on the first line, which widened the page to 342 px with text spacing. The givens moved into the prompt.

## Shared tools changed (TE4 is the first outcome with degrees)
- Speech: 35^\circ now reads "35 degrees" instead of "35 to the power circ". Every math expression in every other outcome reads exactly as before.
- Worked-examples document: prints ° and spacing instead of "circ" and "quad". No other outcome uses those commands.
- Canvas quiz: a figure reused by several items is found under each item's id. Outcomes with one figure per item are unchanged.

## Advisory (not changed)
- Feedback speech reads "12 sine of 35 degrees" without "times"; the display math and choices say "times". Fixing it in the shared speech function would also change EL5's log readings, so it was left for a separate decision.
- Feedback reads a single fraction inside a function as "the quantity 8 over 15, end quantity", while display labels say "8 fifteenths".
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; captions both visible and referenced by aria-describedby; new-tab links without warning.

## Source note (CheckIt, not this page)
TBIL's TE4 generator has a bug in its "nice angles" branch: it computes side a as c·cos A and side b as c·cos B, which swaps the two legs. In that branch (about half of all TE4 problems), 93% of answer keys disagree with a correct solution. Example: A = 30°, c = 10 gives a key of a = 8.7, b = 5, but the correct values are a = 5, b = 8.7. This page teaches the standard convention (sin A = a/c, side a across from angle A).

## Needs a live screen reader
- How NVDA reads the triangle caption, degrees, and each equation, and whether feedback is announced once.

## Update 2026-10-18: a triangle for every computation item
- At the instructor's request, each item on the An Angle and a Side and Two Sides tabs now shows its own triangle, labeled with that problem's given values and a question mark on the unknown (drawn by tools/figures/make_te4.py). Each caption says the triangle is not drawn to scale and states the givens and the unknown in words, without "opposite", "adjacent", or "hypotenuse".
- Rechecked: lint, axe-core 0 violations on every tab at both widths, 320 px reflow with and without text spacing. The unknown is marked in orange (#a84d16, 5.48:1 on the background) and also by the question mark, so color is not the only signal.

## Re-audit 2026-10-31 (current rule set, before recording)
An independent agent re-checked every item, the figures, the Quick Summary, the speak lines and the worked-examples PDF against the CheckIt generator. Every key and rounding was correct. Fixed:
1. Answer positions: no tab's keys are a permutation of a, b, c, d; no correct choice is the uniquely widest.
2. Spot the Slip: "There is no mistake." is choice a in every slip. Slip 1 now confuses a leg with the hypotenuse (tangent needed), so its feedback no longer settles Slip 4; Slip 5 now tests B = 180° − A (the acute angles add to 90°), so Slip 3's correct use of inverse tangent no longer gives it away.
3. Every distractor's origin is named in the feedback.
4. Figure: the angle-B arc in Angle and Side 2 bowed the wrong way (SVG sweep flag); it now curves around B.
5. Coverage of the generator, which always says "Solve the triangle":
   - Angle and Side 1 is now a full solve (B, a and b), with a distractor for B = 180° − A.
   - Angle and Side 4 gives an angle to the tenth of a degree and asks for a side to the nearest whole number.
   - Two Sides 1 gives decimal sides and asks for an angle to the nearest degree, with inverse sine.
6. Quick Summary note: CheckIt asks for every missing part; and a heads-up that when CheckIt gives a whole-degree angle, its answer key lists a and b the other way around.
7. Speak lines say "angle C" and "side c" so the capital and small letters are not confused, and fractions use "the fraction …, end fraction".
8. Worked-examples tool: degree signs print on the line (35°), and a triangle's description is labeled "Figure:" instead of "Plotted data:".
Worked examples and the Canvas quiz were regenerated.

## Source note: a labeling issue in CheckIt TE4
In the whole-degree-angle case (generator lines 19-20) CheckIt computes b = c cos B and a = c cos A, which puts side a next to angle A instead of across from it. So for A = 35°, c = 12 its key says a ≈ 9.8, b ≈ 6.9; the standard labels give a ≈ 6.9, b ≈ 9.8. Its whole-number-sides case (line 8) follows the standard convention. Swapping lines 19 and 20 (a = c sin A, b = c cos A) would fix it; worth reporting to the TBIL maintainers.
