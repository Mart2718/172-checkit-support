# TR5 accessibility audit (WCAG 2.1 AA)

Date: 2026-11-02. Checked by:
- build guardrails and lint, and the rule checks in `tools/rules_check.py`
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key and explanation step checked out except one slip choice's arithmetic (below). It confirmed, and sharpened, the CheckIt bug described in the source notes.
- Diagrams: two angles on the unit circle with the terminal point labeled, as CheckIt shows them (plus a dot marking the point).
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Slip 2: the choice "cos π/2 is 1, so 0/1 = 0" did not follow; it now says sine and cosine were swapped.
2. Convergence giveaways in Secant from a Point and the Quadrant IV item are fixed.
3. Values CheckIt cannot produce: CheckIt's x is always the shorter leg of the triple. The Quadrant IV item is now x = 5/13 (tangent, the case where CheckIt's own key has the wrong sign, which its feedback explains), and the Quadrant I item is now y = 24/25 (the 7, 24, 25 triple).
4. The Quick Summary now says CheckIt's key rationalizes roots (√3/3), spells out exactly which values the CheckIt bug affects, and no longer reuses an item's example.
5. Secant of 270 Degrees: choice labels no longer give away the point (0, −1). Slip 3's distractor no longer contradicts itself.
6. Worked-examples tool: α, β and φ now print as Greek letters (they printed as "alpha"). This applies to any outcome's document when it is next regenerated.

## Advisory (not changed)
- The figures mark the terminal point with a dot, which CheckIt's pictures do not.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
1. **Part 3 bug:** the triple is sorted so x is the shorter leg; for Quadrants I and IV the point is built in Quadrant I, and for II and III in Quadrant III. So in Quadrant IV problems the key's sin, csc, tan and cot are positive (wrong), and in Quadrant II problems they have the wrong sign too; cos and sec are always right. When the given coordinate is y, its sign contradicts the stated quadrant, and CheckIt's picture shows the wrong quadrant. About a third of problems have a wrong key.
2. Half of part 3 draws use 3, 4, 5. Part 2's point can be on an axis, so its keys can be "undefined".
3. CheckIt's own images have no text description (description=".").

## Needs a live screen reader
- How NVDA reads the root speak lines and the unit-circle descriptions, and whether feedback is announced once.

## Dr. Romero's math review (2026-11-03)
An outside AI math check found no wrong keys. Applied, keeping CheckIt's conventions and answer forms: the reference angle is defined as acute, with axis angles handled by their points; the CheckIt note now says to check that a given coordinate fits the stated quadrant and flag the problem if it does not, before using the quadrant for the missing sign.
