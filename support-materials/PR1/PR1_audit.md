# PR1 accessibility audit (WCAG 2.1 AA)

Date: 2026-11-01. Checked by:
- build guardrails and lint, and the rule checks in `tools/rules_check.py`
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a rendered-width check that no correct choice is the uniquely widest
- an independent agent that saw only the page, the CheckIt generator, the figure script, the worked-examples PDF, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: every key, distractor value and explanation step recomputed correctly, all item functions are ones CheckIt can produce, and the four figures match their script and captions. Its must-fix findings were about Quick Summary examples CheckIt cannot produce, how CheckIt prints vertex form with fractions, and one giveaway; all are fixed (below).
- Diagrams: four parabolas on a grid. Three mark the vertex (a square) and x-intercepts (dots), as CheckIt's answer graphs do; their text descriptions start closed, since reading the graph is the skill. One marks only the two x-intercepts, because its question asks for the axis.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Quick Summary examples are now functions CheckIt can produce: −(x + 1)² + 4, 2x² + 5x + 5 (h = −5/4), and 2x² + 3x + 3, whose vertex is (−3/4, 15/8).
2. How CheckIt prints vertex form: Sage clears a fraction inside the square, so 4(x − 1/2)² + 1 prints as (2x − 1)² + 1. The Vertex Form item now uses CheckIt's printed form, and the Quick Summary shows how to read h from it (set 2x − 5 = 0). Please confirm on one live CheckIt problem before recording.
3. Standard Form 3: the choices no longer point to the key (a distractor now shares both its most common coordinates).
4. Coverage of the generator:
   - Standard Form 1 is now 3x² + 5x + 4, with vertex (−5/6, 23/12): denominators other than 2 appear in about a fifth of CheckIt's problems.
   - Graph 1 is now a parabola with no x-intercepts, 2(x − 1)² + 1, where a has to be read from the graph.
   - Which Way is now −5(x + 3)², the one-root vertex form with no + k and a = −5.
   - Graph 2's distractors are all functions CheckIt can produce.
5. Feedback now names which choice each mistake leads to, and Slip 3 explains why leaving out the 2 works only when a = −1.

## Advisory (not changed)
- The worked-examples document prints math in italics and centers multi-line work instead of aligning it.
- The graphs mark the vertex with a square; CheckIt uses colored dots. A square keeps the vertex distinguishable without color.
- Same template items as other outcomes: feedback is both a live region and focused; panel tabindex; "I think:" prefix; new-tab links without warning; the answer key in each button's onclick.

## Source notes (CheckIt, not this page)
1. a runs from −5 to 5 (not 0); a third of problems each have no, one, or two x-intercepts. About 44% of vertices have a fraction for h and 40% for k.
2. In the no-intercept case b runs from −5 to 5 (it is not multiplied by a), and c is just above b²/(4a).
3. Vertex form prints straight from Sage, which writes (x − 7/2)² as 1/4(2x − 7)². Students need to set the inside to 0 to read h.
4. The answer graph's window is h ± 3 (or the intercepts ± 1). It marks the vertex in red and the intercepts in purple; with one intercept, both dots are at the vertex.

## Needs a live screen reader
- How NVDA reads the collapsed graph descriptions and the long fraction speak lines, and whether feedback is announced once.

## Dr. Romero's math review (2026-11-01)
An outside AI math check found no wrong keys. Applied: Axis from the Intercepts no longer states a vertex height the graph cannot show (its last distractor is now y = −3/2); How Many Crossings says a vertex on the axis touches it rather than crosses it.
