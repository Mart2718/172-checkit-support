# TR1 accessibility audit (WCAG 2.1 AA)

Date: 2026-11-02. Checked by:
- build guardrails and lint, and the rule checks in `tools/rules_check.py`
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key, distractor value, explanation step and figure checked out. Its must-fix findings were about distractors outside CheckIt's range, a doubling pattern that pointed to the key, one convergence giveaway, and Quick Summary overlaps; all are fixed (below).
- Diagrams: angles in standard position with a turn arrow; one unlabeled angle with guide lines every 30° (its description starts closed); one student drawing that turns the wrong way.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Distractors are now values CheckIt can produce (special angles), from real mistakes: the reference angle, a mirror image in another quadrant, the same size measured clockwise, or taking π as 90°. Before, most distractors had denominators like 5, 8 or 12 that CheckIt never uses, which left the key as the only plausible value.
2. No item now pairs the key with a choice at exactly twice or half its value as a pattern.
3. Describe the Turn mixes single and multiple mistakes.
4. Coverage: 45° (Quadrant I), π/3 (numerator 1), and π given in radians as CheckIt prints it are now practiced; repeated values across items were removed.
5. The Quick Summary no longer gives away an item, and says CheckIt's answer pictures show a small arc without an arrowhead.
6. Distractor origins are named in every explanation.

## Advisory (not changed)
- The worked-examples document prints fractions in a line (2π/3·180/π) rather than stacked.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
1. CheckIt uses exactly 15 angles: multiples of 30° and 45° strictly between 0° and 360°. The degree question always comes first.
2. Its answer pictures have no text description (description=".") and no arrowhead on the arc.

## Needs a live screen reader
- How NVDA reads the angle descriptions and the π speak lines, and whether feedback is announced once.

## Dr. Romero's math review (2026-11-03)
An outside AI math check found no wrong keys. Applied, keeping CheckIt's conventions and answer forms: Two Thirds of Pi no longer calls 300° the mirror image of 120° across the x-axis (that is 240°); "measured clockwise" is now "coterminal with −45°/−60°"; the summary says the π cancels for multiples of π, and defines radians as θ = s/r.
