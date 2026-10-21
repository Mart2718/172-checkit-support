# TE2 accessibility audit (WCAG 2.1 AA)

Date: 2026-10-21. Checked by: build guardrails, lint, axe-core on every tab (standalone at 1000 px and embedded at 320 px), rendered-math reflow at 320 px with and without the WCAG text-spacing override, a numeric check of every identity and every equality in the feedback, and an independent agent that saw only the page, the CheckIt generator, and the checklist.

## Result
- axe-core: 0 violations on every tab at both widths. The only "needs review" items are color-contrast checks, the same as TE1.
- Independent audit: it tested every identity and every equality in the feedback numerically at 7 values. It found one item with two correct choices, plus several wording and speech items. All are fixed (below).
- Diagram: a five-step flowchart of the usual route through a verification appears on the first Build the Proof item. A reference table of tan, cot, sec, and csc in sines and cosines appears on the first item. Neither one gives away an answer.
- This is an AI-assisted audit, not a compliance certification. Route final acceptance through SAC/RSCCD's designated accessibility review and approval process, with testing on real assistive technology.

## Fixed before publishing
1. Simplify 4 had two correct choices: tan²x − cot²x equals sec²x − csc²x. That choice is now tan x − cot x, and the feedback notes the equivalent form.
2. Rewrite 2: a speak line could be heard as a different choice ("1 over sine x times cosine x"). It now says "1 over the quantity sine x times cosine x". Other speak lines got commas or "Next line" breaks where a fraction's extent was unclear.
3. Feedback that pointed to choices by position ("the first choice", "the last one") now names the expression.
4. The "work on one side" rule was overstated. The summary, the flowchart, and the Slip 3 feedback now say: start from either side, usually the more complicated one, or simplify each side separately. The rule is never to do the same operation to both sides. Slip 3 explains why: a chain that starts from the claim proves nothing unless every step reverses.
5. The summary's example of cancelling part of a sum was Slip 1's exact expression. It now uses (sin x + tan x)/sin x.
6. CheckIt fit: the summary now says the product can appear on either side. It adds 1 + tan²x = sec²x and 1 + cot²x = csc²x, which explain answers like sec(x)² that CheckIt can print.
7. Worked-examples document: function names no longer run together. "tan xcsc x" now prints as "tan x csc x". This came from a fix to the shared document tool, which only improves output and affects other outcomes only when they are regenerated. The reference table is now two columns, so no words break mid-word.
8. "There is no mistake" now sits in varied positions in Spot the Slip. Correct choices are never the widest. More distractor origins were added to the feedback.

## Advisory (not changed)
- Worked-examples document: stacked verification lines are centred rather than lined up at the equals signs, and fractions print flattened. Both come from the shared document tool and are the same for every outcome.
- Summary table at 320 px with text spacing scrolls inside its own region (data-table exception), as on TE1.
- Same template items as other outcomes:
  - feedback is both a live region and focused
  - panel tabindex
  - "I think:" prefix
  - captions both visible and referenced by aria-describedby
  - new-tab links without warning

## Source note (CheckIt, not this page)
TBIL's TE2 generator gives two "verify that A = B" tasks with no answer key, so students write the proof. The other side is Sage's simplification, so it can appear in mixed forms such as sec(x) − cos(x)/sin(x), sec(x)·sin(x)², or sec(x)². The two sides are shuffled, so the product may be on either side.

## Needs a live screen reader
- How NVDA reads the stacked verification lines and the "missing step" marker, and whether feedback is announced once.
