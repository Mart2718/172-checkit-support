# FN3 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-28. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, the Canvas quiz, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key and computation checks out. It evaluated both graphs at 4,000 points per piece to confirm the extrema, intercepts, end values and monotone intervals, and confirmed that both graphs are legal draws from the generator. It found caption and cross-item spoilers and two coverage gaps. All are fixed (below).
- Diagrams: two CheckIt-style graphs built the way the generator builds them, from five pieces that meet at corners, with a filled or open dot at each end. One has a filled end that is the global maximum; the other has an open end at the bottom, so there is no global minimum.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Graph descriptions answered the questions before the guess: they named the intercepts, the high and low points, and the end dots. Each graph's description now sits in a closed "Text description of the graph" disclosure, on the page and in the Canvas quiz. Screen readers still get the full description through aria-describedby. It is worded neutrally ("goes down through (−9, 0) to (−7, −4), where it turns") and names the corners where pieces join. This is a new opt-in figure setting (`collapse: true`); no other outcome uses it, so other pages are unchanged.
2. Cross-item spoilers within a tab, fixed by changing distractors and feedback:
   - Domain's choices and feedback stated the range, and Range's stated the domain.
   - x-Intercepts' choices and feedback stated the y-intercept.
   - Slip 3's choice stated Slip 4's answer, and Slip 4's feedback stated Slip 5's.
3. The Quick Summary note now uses numbers from neither graph.
4. Coverage:
   - Decreasing replaces the first-tab increasing item, on the second graph. Its key ends at a filled dot, (3, 9), and one distractor copies the bracket. CheckIt always writes these intervals with parentheses.
   - The Other Direction replaces the old Between Turns item. Like a CheckIt sketch list, it gives only the decreasing intervals and asks for the increasing ones, including the stretch from the left end of the domain. Its numbers are a legal generator draw.
   - Slip 1 (increasing written with heights) moved to the first graph. Slip 5 now asks about a wrongly claimed "no global minimum" from an open dot partway up the graph.
5. Quick Summary fixes:
   - The domain row no longer mentions arrows; CheckIt FN3 domains always have two ends.
   - The global-extremum rule now covers ties. The generator uses a strict comparison, so when an open end ties a turning point, the turning point is still the global extremum.
   - Increasing and decreasing intervals use parentheses "even at a filled dot".
   - Corners are not turns.
   - CheckIt's bracketed list of intercepts, like [(−9, 0), (−5, 0)], is a list, not an interval.
6. The Ends' feedback explains both wrong dot patterns.
7. Feature lists are in tables with row headers, so the long lists are not packed into choice buttons.

## Advisory (not changed)
- Choices write intervals and points in plain text (−, ∪), the same as earlier outcomes, because axe flags label-in-name mismatches on buttons that pair rendered math with a separate spoken label.
- Worked-examples document: figure descriptions start with "Plotted data:" and print in full. That document is the recording companion, not a student quiz.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - new-tab links without warning
  - the answer key in each button's onclick

## Source notes (CheckIt, not this page)
TBIL's FN3 generator checks out. Notes:
1. The sketch task gives the increasing or the decreasing intervals, not both. Students work out the other, including the stretch from the end of the domain.
2. It lists the sketch's x-intercepts in square brackets, as a list of points.
3. A global extremum is "none" only when an open end is strictly beyond every turning point. Ties go to the turning point.
4. The pieces meet at visible corners, which are not turning points.
5. It also asks students to label and briefly explain how each feature shows on their sketch. No item here practices that; the worked examples can model it on video.

## Needs a live screen reader
- How NVDA and VoiceOver read the closed disclosures and the aria-describedby descriptions, and whether feedback is announced once.
