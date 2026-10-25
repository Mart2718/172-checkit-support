# PR8 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-25. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator and its library code, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key checks out with sympy, and each item has exactly one correct choice. It read CheckIt's library code and ran 4,000 simulated problems. That found the biggest issue, a coverage gap, described below. It also found broken math in the worked-examples document and some smaller items. All are fixed.
- Diagrams: number lines for testing intervals, reading a shaded answer, and a student's shading, plus a parabola for the graph view.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Coverage: CheckIt's shuffled_inequality defaults to strict, so every PR8 problem is equivalent to p(x) > 0. The answer is always two outside pieces with open ends, and the x² term shows up negative about half the time.
   - Shuffled now rewrites 2 − x² < x so the x² term is positive.
   - Solve It now solves −2x² < 9x + 4, a real CheckIt-style problem.
   - All the Way is now strict, with an outside answer.
   - The summary says to keep the x² term positive, and that CheckIt's answers use parentheses.
   - The ≤, ≥, and middle-interval items stay, because the textbook and homework use them.
2. Worked-examples document: < and > inside math printed as "&gt;" and "lt;", and one prompt came out garbled. The shared document tool now decodes these characters in displayed math, and it handles < in plain-text prompts. The PR8 document was regenerated and checked.
3. A display with "<x" was read as an HTML tag, which axe flagged as nested-interactive. It now uses \lt.
4. Test Points and One Test name every distractor's origin. One Test no longer does the arithmetic for the student.
5. The summary no longer gives away the "do not divide by x" trap. Line to Notation no longer copies the summary's example. Correct-answer positions no longer cycle through a, b, c, d within each tab.

## Advisory (not changed)
- Some text choices write math in plain text, the same as earlier outcomes, because axe flags label-in-name mismatches on buttons that pair rendered math with a separate spoken label.
- Worked-examples document: figure descriptions start with "Plotted data:", which reads oddly for a number line. This comes from the shared document tool.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning
  - the answer key in each button's onclick

## Source note (CheckIt, not this page)
TBIL's PR8 generator builds d1 d2 (x − r1)(x − r2), with r1 and r2 drawn from −6 to 6 or from ±1/2, ±3/2, ±1/3, ±2/3. It then calls shuffled_inequality without strict=False, so every problem is a strict inequality equivalent to p(x) > 0. The answer is always (−∞, r1) ∪ (r2, ∞). If TBIL means for students to also see ≤, ≥, or middle intervals, the generator would need strict=False, or a random sign on the polynomial. That is worth reporting.

## Needs a live screen reader
- How NVDA reads the interval speak lines and the number-line captions, and whether feedback is announced once.
