# PR6 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-25. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: it verified every equation, check, and factorization with sympy. It confirmed the four extraneous-solution equations fit CheckIt's own formula and that both graphs match their functions. Every key is right, and each item has exactly one correct choice. It found two distractor explanations with the wrong arithmetic, a coverage gap, and several wording issues. All are fixed (below).
- Diagrams: a graph showing a solution as the x-value where two graphs meet (first exposure). A graph of the left side of an equation shows why an extraneous answer fails: an open circle at x = 4 instead of a crossing.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Solve 3 and Clear the Fractions: two distractor origins named the wrong slip. x = 1 comes from dropping the 1 and cross-multiplying, and 2x comes from dividing 6x by 3 and forgetting the 2.
2. Coverage: CheckIt shuffles the three terms across the two sides. Solve 4 is now 1 = (x − 5)/(x + 2) − (x − 11)/(x + 1): a moved 1, and a minus sign in front of a fraction that applies to its whole product. The Solve It intro says the terms may sit on either side.
3. See It: the caption describes the open circle instead of interpreting it, and the right choice no longer echoes the caption's wording.
4. Spot It: the distractors are realistic (the factor x − 4 equal to 0), and the prompt allows "neither."
5. Clearer feedback in Slip 1, Slip 3 (checked with fractions, not decimals), and Slip 5. Find the LCD stays on the LCD.

## Advisory (not changed)
- Spot the Slip choices write math in plain text, the same as earlier outcomes. Rendered math with a separate spoken label on those buttons triggers axe's label-in-name rule.
- Shared template: the automatic reading of math in prompts and explanations says "5 over 2 x" for \tfrac{5}{2x}, has no comma before "over," and reads parentheses as "open paren … close paren." A fix belongs in the template's texToSpeech and would affect every page, so it is left for a separate decision.
- Worked-examples document: fractions print flattened, and figure descriptions start with "Plotted data:". This comes from the shared document tool.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning
  - the answer key in each button's onclick

## Source note (CheckIt, not this page)
TBIL's PR6 generator mostly checks out. The page covers:
- the one-solution forms p/(x + h) = k and a/(ex) with constant fractions, both with fractional answers
- the shuffled form (x + c)/(x + d) + 1 − (x + f)/(x + g) = 0, which gives two odd-integer solutions
- the "explain why x = a is not a solution" task

One possible generator bug: when p = ±6 with {q, offset} = {2, 3} and p = −q·offset, the numerator is 0. CheckIt then shows an equation like 0 = 2, with the listed answer x = −offset, which is an excluded value. It is rare; worth reporting to TBIL.

## Needs a live screen reader
- How NVDA reads the fraction displays, the two graph captions, and the plain-text math in the Spot the Slip buttons, and whether feedback is announced once.

## Update 2026-10-30: graph descriptions that gave answers away
- The first graph description said the curve passes through (4, 2) "where it meets the line", the same wording as the key; it now says "(4, 2), which is also on the line". Worked examples and Canvas quiz regenerated.
- Found in a sweep of every graph description after the FN3 audit, with an independent second opinion.
