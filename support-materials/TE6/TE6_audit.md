# TE6 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-19. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a numeric check of every answer and of every distractor's stated origin
- an independent agent that saw only the page, the CheckIt generator, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: all 21 keyed answers recompute correctly, and each item has exactly one defensible choice. It found 2 errors in the teaching text and several clarity items, all fixed (below).
- Diagrams: all 16 non-slip items have their own sketch, so every CheckIt problem type has a picture on first exposure. Each sketch shows the given numbers and an orange "?" on what is asked. The question mark means color is never the only signal.
  - The bridge brace is drawn to scale.
  - The fire-tower sketches draw both base angles equal on purpose, so the picture does not show which ranger is closer. Their captions say "not drawn to scale".
- Figure text contrast is at least 4.6:1.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Divers feedback gave the wrong source for the 16.3 m distractor. It now says 16.3 comes from 20 sin 45° / sin 60°, and it adds that CheckIt asks for both divers' distances.
2. The Quick Summary called lighthouses "two angles and the side between them". That row now says "two angles and a side".
3. Fire-tower sketches no longer show which ranger is closer (Set Up 4 asks exactly that).
4. Crown moulding feedback now leads with the law of cosines, which matches the summary. It notes that CheckIt's key uses the law of sines and gets the same answer. The Lookouts tab intro no longer says "two people see the same object".
5. The Fire Towers item now uses CheckIt's wording ("55° to the left of the other tower"), and the summary explains what that phrase means.
6. The rounding note now says CheckIt rounds the airplane ground distance to the nearest foot.
7. Distractor origins were added for Set Up 1 to 3.
8. The red lighthouse is drawn red, and the airplane distance label no longer overlaps its line.
9. The Slip 4 speak line says "d is about 26.6", matching the other slips.

## Advisory (not changed)
- At 320 px the summary table scrolls sideways inside its own focusable region, which the data-table exception allows. The page itself does not scroll sideways.
- Worked-examples document: stacked student work in Slips 1 and 5 prints without alignment, and figure descriptions start with "Plotted data:" (shared document tool, same as TE4 and TE5).
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning

## Source note (CheckIt, not this page)
TBIL's TE6 generator checks out: all 12 problem types compute correctly. These conventions are worth knowing, and the page teaches each one:
- In the cliff problems, "how far away" means the straight-line distance along the line of sight, not the distance along the water.
- The scuba problem gives the divers' depth, which is not needed. Its key assumes the animal is between the two divers.
- The hiker's turn angle is measured from straight ahead, so the angle inside the triangle is 180° minus the turn.
- Two airplane headings: the angle between the paths is the difference of the headings. CheckIt does not reduce differences over 180°, but cosine gives the same value either way.
- The crown-moulding prompt is missing a space ("92°angle").

## Needs a live screen reader
- How NVDA reads the longer scenario captions, the stacked equations in Spot the Slip, and whether feedback is announced once.
