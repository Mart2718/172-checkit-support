# FN4 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-22. Checked by:
- build guardrails and lint
- axe-core on every tab, standalone at 1000 px and embedded at 320 px
- rendered-math reflow at 320 px, with and without the WCAG text-spacing override
- a recomputation of every answer and of every plotted point
- an independent agent that saw only the page, the CheckIt generator, and the checklist

## Result
- axe-core: 0 violations on every tab at both widths.
- Independent audit: it recomputed all 17 answers and every distractor's stated origin. Each item has exactly one correct choice, and no alternative order of transformations gives the same graph. It checked every plotted curve and labeled point against the formulas and captions. A screen-reader user can answer every graph item from the caption alone. It found two must-fix items and several smaller ones, all fixed (below).
- Diagrams: CheckIt's three parent graphs (semicircle, parabola piece, tent) are shown with labeled key points. The Match items draw f dashed in gray and g solid in teal. The two are told apart by dash pattern and line weight, not color alone.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Speech could not tell f(x + 3) from f(x) + 3: they read "f of x plus 3" and "f of x, plus 3". That difference is the whole point of FN4. The shared speech function now reads a function of a sum as "f of the quantity x plus 3, end quantity". A diff of all 1,730 math expressions on the site showed that only FN4's readings change. The Canvas quiz uses the same function.
2. Two explanations referred to "the third one". They now name the formula.
3. Point moves were written with an arrow that is read as "approaches". They now say "goes to".
4. Read 3 and Match 3 explanations were corrected and clarified. Spot the Slip 1's correct choice is shorter so it no longer wraps to three lines. Two graph labels were moved off the axes and curves, and all graph text is larger.
5. The Quick Summary adds:
   - a model answer in CheckIt's own phrasing ("shifted left by 3, reflected across the x-axis, and then shifted up by 2")
   - a note that only "reflect before the vertical shift" is required, since the sideways shift and the reflection can go in either order
   - an example value no item uses

## Advisory (not changed)
- No item asks students to choose g's graph from a formula. The Track the Points tab practices the sketch task point by point instead.
- Worked-examples document: figure descriptions start with "Plotted data:". This comes from the shared document tool and is the same for every outcome.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning

## Source note (CheckIt, not this page)
TBIL's FN4 generator checks out. It builds g(x) = ±f(x ± b) ± c with b and c from 1 to 5. Its answer states the order correctly: horizontal shift, reflection, then vertical shift. The outcome names stretches, but the generator's stretch factor is commented out, so CheckIt FN4 uses only shifts and reflections.

CheckIt display quirks students may notice:
- The answer graph for right shifts is drawn without gridlines.
- The window stops at y = 8, so a graph shifted up 5 can run off the top.
- The answer text is missing a space ("f(x)is shifted").
- The graphs' alt text is only "Original graph" and "Transformed graph".

## Needs a live screen reader
- How NVDA reads the graph captions and the new "the quantity" readings, and whether feedback is announced once.
