# LF5 accessibility audit (WCAG 2.1 AA)

Date: 2026-11-01. Checked by:
- build guardrails and lint, and the rule checks in `tools/rules_check.py`
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key, distractor value and explanation step checked out, every story's numbers are inside CheckIt's ranges, and the figure matches its script. Its findings were about printing, giveaways and coverage; all are fixed (below).
- Diagram: the rice model R(d) = 250 − 15d on labeled axes, with two marked points. A Hill Valley population table, with a caption and header cells.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Worked-examples tool: numbers written as 48{,}000 in math now print as 48,000. This applies to any outcome's document when it is next regenerated.
2. Giveaways: A Phone Plan and A Shrinking Town no longer have a key that is the only choice sharing both the most common number and the most common meaning; Population mixes single and double mistakes. Printing Posters showed its model, which gave the slope away; it is now Reading a Table, the slope of a shrinking town from a table of values.
3. How Many Hats: CheckIt's answers are whole numbers, so every distractor is now whole too ($540 fixed costs, a $1,890 budget: 150, 210, 270, 1,350).
4. Coverage of the generator (CheckIt asks for an input and an output in every story):
   - Slip 2 is now the town question CheckIt asks for a year: the student solves for x = 5 and forgets to add 2018.
   - Use the Model now has a water find-the-input item and a phone-plan find-the-input item, and the slope of a shrinking town, which CheckIt prints as negative, is practiced from a table.
5. The Quick Summary says only rice and water stories print the slope as the positive rate; a shrinking town's slope prints as negative.
6. Models are shown in CheckIt's order, mx + b. The figure caption matches the labeled axis.

## Advisory (not changed)
- The (x − 1) and (x − 2015) distractors in Phone Lines, Population and Slip 3 use forms CheckIt does not print, on purpose: they are the real misconceptions about what x counts.
- Rice find-the-output and cost find-the-output with inputs in the hundreds are not practiced separately; the Use the Model items cover the same two moves.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
1. For the rice and water stories, CheckIt's answer key prints the slope as the positive rate (for example 15), though the model it prints, R(d) = −15d + 250, has slope −15. Students who answer −15 are right.
2. The water story's starting amounts are only 50, 55 or 200 ounces (`choice([50,55,200])`), probably meant as a range from 50 to 200 in steps of 5.
3. In the cost story, the first two lines that set m and b are overwritten by the next line, so they have no effect.
4. Both town questions use calendar years: one gives a year, the other asks for one.
5. Template typos: "popuation", a missing period after the phone-plan sentence, and "the year since".

## Needs a live screen reader
- How NVDA reads the population table and the rice graph description, and whether feedback is announced once.
