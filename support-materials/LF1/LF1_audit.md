# LF1 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-30. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: no must-fix findings. Every key, distractor computation, figure line and caption checks out, and the four Spot the Slip rules pass. It simulated the generator 20,000 times; the coverage gaps it found are fixed (below).
- Diagrams: four lines on CheckIt's −10 to 10 grid with no points marked (their text descriptions start closed, since reading the slope is the skill), and a curve with a secant segment for the first average-rate item.
- The Quick Summary table is about 10 px wider than a 320 px screen, so it scrolls slightly inside its frame. Data tables are exempt from WCAG 1.4.10 reflow.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Coverage of the generator:
   - Average Rate 2 is now degree 4, x⁴ − 2x on [−2, 1], keeping the negative input.
   - Average Rate 3 now has two irrational outputs: (√11 − √5)/2 for √(3x + 2) on [1, 3], the usual CheckIt case.
   - Average Rate 4 now has a fraction answer, 5/18, for (2x − 1)/(x + 2) on [1, 4].
   - Two Points 2 is now a negative improper fraction slope, −7/3; Table 2 is −7/5 (d = 5) in CheckIt's vertical x | y layout.
   - Graph 1 is now a steep negative half-step slope, −5/2.
2. Answer format: the Quick Summary and Average Rate 3 say CheckIt may print an equivalent split form, such as −2/3 + √7/3, and that both are correct.
3. The Quick Summary's examples no longer match any Try It item.
4. Speak lines read points as "the point negative 3 comma 5", and every root ends with "end root". Slip choices no longer use slash forms like √5/9 that read ambiguously aloud.
5. Worked-examples tool: a root on top of a fraction keeps its parentheses, (√6)/2, so it cannot be read as √(6/2). This applies to any outcome's document when it is next regenerated.
6. Smaller feedback wording fixes (Average Rate 1, Slip 1, Slip 3).

## Advisory (not changed)
- Square graph figures print at about a third of the page width in the worked-examples document, to leave room for the choices; zoom in while recording if needed.
- Slip choices are plain text (Unicode √, −), the same as earlier outcomes, because axe flags label-in-name mismatches on buttons that pair rendered math with a separate spoken label.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
TBIL's LF1 generator checks out. Notes:
1. About a third of polynomials are degree 4; 72% of root answers have two irrational outputs; 87% of fraction-function answers have denominators of 10 or more; the numerator of the fraction can be a constant.
2. Fraction slopes are k + j/d with d from 2 to 5, mostly improper; whole-number slopes can be 0.
3. The table's x-values are sampled at random, so they are usually, but not always, unevenly spaced. Its graph's alt text is only "Plot".

## Needs a live screen reader
- How NVDA reads the vertical table and the collapsed graph descriptions, and whether feedback is announced once.
