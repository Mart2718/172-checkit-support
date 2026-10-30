# FN5 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-30. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key and distractor computation checks out, and the four Spot the Slip rules pass. It simulated the generator 4,000 times to measure coverage. It found three coverage gaps and a worked-examples printing problem that changed the math. All are fixed (below).
- Diagrams: two function-machine diagrams, one input feeding two machines whose outputs are added, and two machines in a row. They scaffold the first exposure to combining and composing; neither gives an answer.
- The Quick Summary table is wider than a 320 px screen by about 50 px, so it scrolls sideways inside its frame (the page itself does not). Data tables are exempt from WCAG 1.4.10 reflow; FN2 and FN3 do the same, less so.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. The worked-examples document printed fractions in ways that changed the math: x + 3/2x (read as (3/2)x) for x + 3/(2x), which made Slip 5's key look like its distractor. The shared document tool now puts any denominator that is more than one symbol in parentheses, and never wraps a single term on top (2x/(x+3), √3/2, f(x)/g(x)). Diagram descriptions are labeled "Diagram:" instead of "Plotted data:".
2. Coverage of the generator's ten function pairs: the Combine tab used only a line with a quadratic.
   - Product now multiplies a line by a square root, and stays unexpanded, as CheckIt writes it.
   - Quotient now divides by a fraction, ax/(x + b), so the flip is practiced.
3. The swap flag: CheckIt lists the two functions in either order. Compose 1, 3 and 4 now list the inside function first, so "the first one listed goes outside" fails.
4. Compose 4 is now a quadratic of a fraction, q(r(x)) = 2(x/(x+2))² − 1, with every choice in a similar form (the old one gave its answer away by being the only choice with parentheses).
5. Evaluate 3 now uses a negative input into a cubic and a fraction function: r(p(−2)) = 21/5.
6. Letters now come only from CheckIt's set f, g, h, p, q, r.
7. Quick Summary: CheckIt leaves products unexpanded (not "may"); dividing by a fraction means flipping it; simplifying a composition is optional; read the letters, not the listing order; inputs can be negative and answers can be large.
8. Speak lines: "end root" on every root; fractions read with "end fraction"; Slip 5's visible "x + 3/2" became "x + 1.5" so a screen reader does not say "3 slash 2".

## Advisory (not changed)
- Slip choices are plain text (with Unicode ², √, −), the same as earlier outcomes, because axe flags label-in-name mismatches on buttons that pair rendered math with a separate spoken label.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; captions both visible and referenced by aria-describedby; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
TBIL's FN5 generator checks out. Notes:
1. The value question uses the opposite order from the formula question: the formula is A(B(x)) and the value is B(A(n)) (generator lines 14 and 21).
2. Products and quotients are left exactly as Sage writes f1*f2 and f1/f2, unexpanded.
3. About 30% of composition values are square roots (some of fractions), 22% are fractions, and 13% are larger than 1000 (cubics). About 37% of inputs are negative.
4. The four functions always have four different types and four different letters.

## Needs a live screen reader
- How NVDA reads the long product and quotient speak lines, and whether feedback is announced once.
