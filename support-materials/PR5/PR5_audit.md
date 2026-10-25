# PR5 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-24. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: it redid every synthetic division, expansion, and quadratic formula with sympy and checked the graph against its function. Every key is right, and each item has exactly one correct choice. It found one cross-item spoiler, an overly narrow statement about complex pairs, too little teaching of synthetic division for a first exposure, and several coverage and caption gaps. All are fixed (below).
- Diagrams: synthetic division tableaus for each new step (multiply and add, reading the bottom row, testing a zero again, dividing by a fraction) and one student's work. There is also a graph used to choose which candidates to test. Long expanded polynomials are split over two aligned lines so they reflow at 320 px.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Candidates 3 feedback named the irrational zeros, which are Finish 1's answer. It now says only that they are irrational.
2. Complex zeros: the summary and Count Them now say pairs are a + bi with a − bi. "± pairs" holds only for pure imaginary zeros. The summary example no longer uses Count Them's numbers.
3. Synthetic division: the summary now gives the corner rule (to divide by x − r, put r in the corner; for x + 3, use −3). Divide 1 finishes the division in its feedback, and Divide 3 does its second division in the feedback instead of plugging in.
4. Coverage:
   - The summary example is now a negative fraction, −4/5 → (5x + 4).
   - Slip 3 uses the zero −5/3 → (3x + 5), on its own polynomial, so it no longer shares one with Candidates 2.
   - Slip 4 shows a number staying in front of the root, −2 ± 2√2.
   - Slip 5 shows how CheckIt prints irrational factors: (x − 1 − √5)(x − 1 + √5).
5. Captions say where the middle row of each tableau starts. The graph caption gives both low points as coordinates.
6. Candidates 3 asks which crossings appear to land on candidates, since a graph cannot show "exactly."
7. Function names are no longer reused for different polynomials (r and m added). Distractor origins are spelled out (√52 = 2√13; 16 skips the multiply step). Correct-answer positions differ across tabs.

## Advisory (not changed)
- Spot the Slip choices and two Synthetic Division choices write math in plain text (x⁴, √6), the same as PR3 and PR4. Rendered math with a separate spoken label on those buttons triggers axe's label-in-name rule.
- Worked-examples document: fractions print flattened, such as (−6 ± √20)/2, and figure descriptions start with "Plotted data:". This comes from the shared document tool, which now also drops \big sizing commands.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning
  - the answer key in each button's onclick

## Source note (CheckIt, not this page)
TBIL's PR5 generator checks out. Each problem has two polynomials. Each is (x − a) times either (x − b)² or (nx − m) with n = 2, 3, or 5, times either x² + c² or an x² + bx + c with irrational zeros. The two always use opposite choices, so one has a repeated zero and one a fractional zero, and one has complex zeros and one irrational zeros. Its answer key expands irrational factors, writing x − (−3 + √5) as (x − √5 + 3).

## Needs a live screen reader
- How NVDA reads the synthetic division captions, the plain-text superscripts and roots in the choice buttons, and whether feedback is announced once.
