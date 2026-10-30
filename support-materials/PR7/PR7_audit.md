# PR7 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-25. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: it checked every hole, intercept, asymptote, and behavior near an asymptote with sympy, along with the minimum named in a caption, and it checked both graphs against their functions. Every key is right, and each item has exactly one correct choice. It found four must-fix problems and several smaller ones. All are fixed (below).
- Diagrams: two graphs drawn the way CheckIt's answer key draws them, with dashed asymptotes, an open circle for the hole, and labeled intercepts. One has a horizontal asymptote; one has none.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Hole Height: the correct choice was the widest. A y-intercept distractor, −5/12, replaces it.
2. Slip 3, the "no mistake" item: the student's work wrote f(−3) = 7/6, but f(−3) is undefined at the hole. The work now shows the cancelled form and the value from plugging −3 into it.
3. Match the Formula feedback no longer writes f(−1) = 4, and no longer refers to a choice by its position.
4. Read the Graph: the hole is no longer labeled on the graph, so students compute its height from the formula. Its distractors now name real slips: reading 0/0 as 0, and forgetting the 2. The caption says "no other dashed lines are drawn."
5. Explanations say "away from the hole" when they use the cancelled form, so they agree with the domain item.
6. Speech: every factor is closed with "end quantity" inside fractions.
7. Coverage:
   - Level Off 2 now has a single, unsquared factor on the bottom.
   - The summary says how to read the range from a finished sketch.
   - Cancel or Stay? and Domain name every distractor's origin.
8. Sketch It: the shared part of the four long choices moved into the prompt.

9. After publishing (instructor review): CheckIt asks "Find any vertical asymptotes" directly, but no item did. The Domain item is now Vertical Asymptotes, on the same function. Its distractors: counting the cancelled factor, reading the sign as written, and taking a top factor. The explanation says the squared factor gives one asymptote, with the graph going the same way on both sides, and it states the domain.

## Advisory (not changed)
- Some text choices write math in plain text, the same as earlier outcomes, because axe flags label-in-name mismatches on buttons that pair rendered math with a separate spoken label.
- CheckIt never asks for the range, though the outcome names it. The page covers it in the summary only.
- Worked-examples document: fractions print flattened, and figure descriptions start with "Plotted data:". This comes from the shared document tool.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning
  - the answer key in each button's onclick
  - automatic speech for math inside prompts reads parentheses as "open paren"

## Source note (CheckIt, not this page)
TBIL's PR7 generator checks out. It builds f(x) = c k0 (x − r3)^n1 (x − r1) / (k1 (x − r1)(x − r2)^n2), with n1 = 0, 1, 2 and n2 = 1, 2. Its horizontal asymptote is:
- y = 0 when the bottom has higher degree, including n1 = 0
- c k0/k1 when the degrees match
- "None" when n1 = 2 and n2 = 1

Each function has one hole and one vertical asymptote.

## Needs a live screen reader
- How NVDA reads the long fraction speak lines and the two graph captions, and whether feedback is announced once.

## Update 2026-10-30: graph descriptions that gave answers away
- Read the Graph (the hole-and-asymptote list): its description lined up with the keyed list ("no other dashed lines", the open circle at x = 1). It now sits in a closed "Text description of the graph" disclosure. Canvas quiz regenerated.
- Found in a sweep of every graph description after the FN3 audit, with an independent second opinion.
