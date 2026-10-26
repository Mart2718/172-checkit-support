# PR9 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-26. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator and its library code, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key and computation checks out with sympy. It enumerated every parameter combination the generator can produce, about 20,000 times 4 symbols, and compared CheckIt's answers with the true solution sets. It found one important coverage gap and several smaller ones, plus wording issues. All page fixes are made (below).
- Diagrams: a number line with critical points and labeled test points, for the first sign chart, and a number line with mixed open and closed dots, for reading an answer.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Coverage, holes: about 16% of CheckIt problems have a top zero that is also a bottom zero, and about 17% show a side that cancels, like (x − 6)/(x − 6). A Shared Zero, which replaces One Factor Each, solves (x − 6)/(x − 6) ≥ (x − 6)/(x − 5), with answer (5, 6) ∪ (6, ∞). The summary's endpoint rule now says "unless the bottom is also 0 there."
2. Coverage, negative leading coefficient: about 13% of problems combine to a top like −2x. A Negative Out Front, which replaces the notation-to-number-line item, covers this. The summary says a negative number out front counts as one more negative factor.
3. Coverage: the summary notes that CheckIt's numbers can be large, that answers can have one piece or none, and that a top with no x has no zeros.
4. Why Not Multiply? now asks for the sign at x = 3.5 instead of repeating the summary's wording.
5. Slip 1's distractor is a coherent error, and Slip 4's prompt no longer points at the slip. Every distractor's origin is named in Why Not Multiply?, Which Ends Count?, and Slip 3.
6. Test points are triangles labeled with their values, so they no longer look like closed dots. This also updates PR8. Speak lines use one style for numerical tops and read each interval endpoint's inclusion in place.

## Advisory (not changed)
- Several choices differ only by a bracket versus a parenthesis, written as plain text. Some screen readers skip punctuation by default, so those choices can sound alike. A fix needs a template field for a hidden spoken reading (aria-describedby), which would change the shared template.
- Worked-examples document: fractions print flattened, which is heavy for narration, and figure descriptions start with "Plotted data:". This comes from the shared document tool.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning
  - the answer key in each button's onclick

## Source notes (CheckIt, not this page; worth reporting to TBIL)
1. When both sides reduce to the same constant (linear type with e = a·f, about 1.4%), the answer string for < or > is empty, and the number line is blank.
2. In that same family, with ≤ or ≥, the answer splits into unmerged pieces, like (−∞, 4) ∪ (4, 5] ∪ [5, 6) ∪ (6, ∞).
3. The quadratic type rules out c = r1 and c = r2, but the undefined point is −c, so the check does nothing. It probably should be "−c not in (r1, r2)". This causes most of the holes.
4. Numbers can get large: undefined points reach about ±55 and coefficients pass 500. The generated image's alt text is only "Solution to inequality."

## Needs a live screen reader
- How NVDA reads the plain-text interval choices that differ only by a bracket, the long fraction speak lines, and the number-line captions.
