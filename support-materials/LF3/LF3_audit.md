# LF3 accessibility audit (WCAG 2.1 AA)

Date: 2026-11-01. Checked by:
- build guardrails and lint, and the rule checks in `tools/rules_check.py`
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key, distractor computation and explanation step recomputed correctly, every figure matched its script, and each Spot the Slip graph shows the mistake its item describes. Its must-fix findings were about giveaways and CheckIt's ranges, not wrong math; all are fixed (below).
- Diagrams: CheckIt's −8 to 8 grid. The student graphs in Spot the Slip mark the student's plotted points. The one graph whose reading is the whole skill (Name the Line) has its text description closed at first.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Convergence giveaways (the key was the only choice with the most common value of every feature): Point and Intercept, Slope and Intercept, both Read the Equation items with points, Standard Form 1 and x = c now mix single and double mistakes.
2. Values CheckIt never produces: slope-intercept and point-slope slopes are whole numbers from −3 to 3, and standard form's C runs from −7 to 7. Slope-Intercept Form is now y = −3x + 2, Slip 1 is y = −2x + 3, Standard Form 2 is 3x + 4y = 4, and Slip 4 is 3x + 2y = 6. Slope 0's distractor y = −5x is now x = −5.
3. The Quick Summary's point-slope example no longer matches Slip 5, and it no longer says "the signs flip", which Slip 5 calls the student's mistake. Slip 5's choices now say "read the signs as written" and name which point was swapped.
4. Coverage of the generator:
   - Slip 2 is now a correct graph of 2x + 3y = 7, where both intercepts are fractions (about 4 in 10 standard-form cases), plotted at whole-number points instead. The Quick Summary says what to do then, and when C = 0.
   - Undefined Slope is now x = 0 (the y-axis); CheckIt's horizontal-or-vertical value can be 0. The Quick Summary mentions it, and a 0 coordinate in point-slope form.
5. The Quick Summary note no longer says CheckIt's slopes run from −4 to 4 (true only for one task).
6. Every distractor names its origin; speak lines use "the fraction 5, over 4, end fraction".
7. Worked examples: "x-intercept" prints with a hyphen, and a fraction before a letter prints as (2/3)x.

## Advisory (not changed)
- The tab heading "Flat and Upright Lines" tells students the tab is about horizontal and vertical lines, which makes the sloped choice in x = c easier to rule out. Kept, because the tab's purpose is to name the special case.
- Text inside math (such as "x-intercept") prints in italics in the worked-examples document.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
1. **Wrong answer graph for some vertical lines.** In about 7% of point-and-intercept problems the point and the intercept share an x-coordinate, so the line is vertical. The generator's `line_from_points` then returns x == c, and the graphics code plots its right-hand side, which draws the horizontal line y = c. CheckIt's answer graph is wrong in that case.
2. The template's comments say task 2 never gives a horizontal line and task 3 is never an axis, but the code allows slope 0 (which, with an x-intercept, is the x-axis itself) and the value 0.
3. Task 1 slopes can reach about ±14 (two points in opposite quadrants), and standard-form slopes up to ±6.
4. How CheckIt prints the held product in point-slope form was not confirmed (Sage is not installed here); check one live problem before recording.

## Needs a live screen reader
- How NVDA reads the student-graph descriptions and the collapsed graph description, and whether feedback is announced once.
