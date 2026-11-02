# LF2 accessibility audit (WCAG 2.1 AA)

Date: 2026-11-01. Checked by:
- build guardrails and lint, and the rule checks in `tools/rules_check.py`
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: one must-fix (Two Points 1, below). Every other key, distractor computation, figure line and caption checks out, and the Spot the Slip rules pass.
- Diagrams: four lines on CheckIt's −10 to 10 grid with no points marked, as on CheckIt. Their text descriptions start closed, since reading the graph is the skill.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Two Points 1 is now (2, −3) and (−4, 4), slope −7/6, intercept −2/3. Each distractor is a named mistake: run over rise (−6/7, with b recomputed), subtracting in opposite orders (7/6), and b found by subtracting 7/3 instead of adding.
2. Convergence giveaways: in several items each distractor changed one feature of the key, so the key was the only choice holding the most common slope and the most common intercept. Standard Form 1, 2 and 4 and Graph 1, 2 and 4 now mix single and double mistakes. Standard Form 3 is now −6x − 4y = 10, where both A and B are negative.
3. Graph 3 is now y = 3(x − 5), a line whose y-intercept (−15) is off the grid, so the point has to come from the x-axis. CheckIt's graphed line passes through a grid point with x and y from −5 to 5, and that point can be on an axis.
4. Slip 4: the two plain-swap choices now give a reason, like the other choices.
5. The Quick Summary says the y-intercept can be between grid lines or off the grid, and its sign example, (4, −1) gives y + 1, no longer matches an item.
6. Speak lines read fractions as "the fraction 3, over 2, end fraction".
7. Worked-examples tool: a fraction followed by a letter or a parenthesis prints in parentheses, (2/3)x and (2/3)(x + 8), and a hyphen inside words in math (y-intercept) prints as a hyphen, not a minus sign. This applies to any outcome's document when it is next regenerated.

## Advisory (not changed)
- Square graph figures print at about a third of the page width in the worked-examples document; zoom in while recording if needed.
- Slip choices and Standard Form choices are plain text (Unicode −), the same as earlier outcomes, because axe flags label-in-name mismatches on buttons that pair rendered math with a separate spoken label.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
1. Standard form: A and B are from −10 to 10 (not 0) and C from −10 to 10 (it can be 0), so the slope and the y-intercept are usually fractions, and the line can go through the origin.
2. The graphed line: a negative slope is −1 to −3 in steps of 1/2; a positive slope is 1/2 to 3 in steps of 1/2. A point on an axis always gets a positive slope. No points are marked.
3. CheckIt accepts slope-intercept or point-slope form.

## Needs a live screen reader
- How NVDA reads the collapsed graph descriptions and the long fraction speak lines, and whether feedback is announced once.
