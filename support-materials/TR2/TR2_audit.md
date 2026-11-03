# TR2 accessibility audit (WCAG 2.1 AA)

Date: 2026-11-02. Checked by:
- build guardrails and lint, and the rule checks in `tools/rules_check.py`
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: one wrong distractor value (Two Fifths of Pi, below); every other key, distractor, explanation step and figure checked out. It confirmed the CheckIt answer-key bug described in the source notes.
- Diagrams: an angle in standard position, and a circle with a central angle and its highlighted arc.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Two Fifths of Pi: the distractor from multiplying by π/180 is about 0.02°, not 0.07°.
2. Angles CheckIt never uses (5π/6, π/5, 7π/9) were replaced with ones it does: CheckIt's angles are all multiples of 40°, 45°, 60° or 72°. Radius 6 is now 3π/4, and the slips use 14π/9, 4π/9 and 16π/9.
3. The Quick Summary's example no longer matches an item.
4. Convergence: both arc items with a degree slip are now balanced 2 × 2 sets (radius or diameter, radians or degrees).
5. A Negative One is now 3π/2 with four negative choices, so the word "negative" no longer rules out half of them.
6. Coterminal feedback no longer states the rule another item in the same tab tests. Radius 14 notes that CheckIt prints 56π/5 as 56/5 π.

## Advisory (not changed)
- The worked-examples document prints fractions in a line rather than stacked.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
1. **Answer-key bug:** when the coterminal question is in degrees, the key's negative angle is the arc-length angle minus 360°, not the coterminal angle minus 360°, so it is usually wrong. The radian branch is correct. Any correct coterminal pair should be accepted.
2. CheckIt's angles are a/b of a full turn with b = 2, 3, 4, 5, 6, 8 or 9: 21 distinct values, all multiples of 40°, 45°, 60° or 72°. The two questions always use opposite units.
3. Arc lengths print as a fraction times π, such as 56/5 π.

## Needs a live screen reader
- How NVDA reads the arc figure description and the π speak lines, and whether feedback is announced once.
