# How a CheckIt support page is built and checked

This is the checklist for every outcome page in this repository. Whoever builds a page (Dr. Romero, or Claude
working with him) and whoever audits it work from the same list. Rules marked **(checked)** are enforced by a
script; the rest need a person or an independent reviewer.

## 1. Build order

1. **Read the CheckIt generator first.** Open `generator.sage` and `template.xml` for the outcome in TBIL
   (`lib/source/precalculus/exercises/outcomes/<group>/<code>/`) and the outcome text in `bank.xml`.
2. **Map the generator before writing items.** List every case CheckIt can produce: function types, which values
   are given, answer forms (fractions, roots, "none", unexpanded products), rounding instructions, letters used,
   negative inputs, and edge cases. Simulate it (a short Python script) when the cases are not obvious. Note any
   bug in CheckIt itself (example: TE4 swaps sides a and b when it gives a whole-degree angle).
3. **Write `content/<CODE>.yml`.** Three Try It tabs of 4 items and a Spot the Slip tab of 5 (17 items), unless
   the outcome needs a Beyond CheckIt tab. Design the items to cover the map from step 2, not just the easy cases.
4. **Draw figures** with `tools/figures/make_<code>.py`, at least at the first exposure to each problem type.
   Graphs follow CheckIt's look (its window, no points marked if CheckIt marks none). Angle sides are rays with arrowheads, as in CheckIt's answer pictures; on a unit circle with a marked point they are segments ending at the point.
5. **Build and check** (section 4), then make the worked examples, the Canvas quiz, and the LibreTexts code.
6. **Independent audit** (section 5), fix, write `support-materials/<CODE>/<CODE>_audit.md` and the README row,
   commit, push, and confirm the Netlify deploy.
7. **Dr. Romero's review** (section 6) before the page is used or recorded.

## 2. Item rules

**Math first.** Every answer key, distractor value and explanation step is computed, not estimated. Exact answers
stay exact. If CheckIt prints an answer in a different but equal form, say so in the item or the Quick Summary.

Answer choices
- In a 4-item tab, the correct answers are not a, b, c and d once each. **(checked)**
- The correct choice is never the uniquely widest button. Items with fewer than 4 choices (fixed categories like
  Function / Not a function) are exempt. **(checked, rendered)**
- Every distractor comes from a real mistake, and its origin is named in the feedback with correct arithmetic.
  **(heuristic warning; a person confirms)**
- Feedback never refers to a choice by position ("the first one", "choice b"). **(checked)**
- No convergence giveaway. When each distractor changes one feature of the key (the slope, the intercept, a
  sign), the key is the only choice that has the most common value of every feature, so a student can find it
  without doing the math. Mix single and double errors so that no choice is the "intersection" of the others.
- Distractor values come from the generator's real range: do not use a slope, form or value CheckIt can never
  produce.

Spot the Slip
- "There is no mistake." is choice a in every slip. **(checked)**
- Exactly one slip has "There is no mistake." as its answer. **(checked)**
- Every slip prompt ends with "What is the mistake, if any?" **(checked)**

No giveaways (needs judgment)
- Nothing shown before the guess (titles, figure captions, table captions) states an answer. Phrases listed in
  `banPhrases` are blocked in titles and captions. **(checked)**
- Within a tab, no item's choices or feedback reveal another item's answer.
- The Quick Summary's examples do not match any Try It item.
- When an item's whole skill is reading a figure, set `collapse: true` on the figure so its text description
  starts closed. Screen readers still get it through aria-describedby.

## 3. Accessibility rules (WCAG 2.1 AA)

- Every figure has a title and a text description that is an accurate equivalent of the picture. **(checked)**
- Every choice written in math has a `speak` line. Conventions **(partly checked)**:
  - "the fraction A, over B, end fraction"
  - "the quantity …, end quantity"
  - "the square root of …, end root"
  - "angle C" and "side c", so capital and small letters are not confused
  - points as "the point negative 3 comma 5"
- Choices that mix words and math are written in plain Unicode text (x², √, −, ∪) with no speak line, because a
  rendered-math label with a separate spoken name fails axe's label-in-name rule.
- In content math, write `\lt` for a less-than sign; in HTML text fields, write `&lt;`.
- axe-core reports 0 violations on every tab at 1000 px and embedded at 320 px. **(checked)**
- At 320 px, with and without the WCAG text-spacing override, the page never scrolls sideways and no equation
  sticks out. A display equation that is still too wide scrolls inside its own box, which then becomes a
  keyboard tab stop; prefer splitting long displays into aligned rows. A data table may scroll inside its own
  frame. **(checked, rendered)**
- Video embeds use youtube-nocookie.com. Captions are reviewed in YouTube Studio before a video is shared.

## 4. The checks, in order

Run from the repository root:

```
node build.js
python3 tools/checkit_lint.py dist/<code>/index.html --ban '<banPhrases>'
python3 tools/rules_check.py <CODE>
node tools/render_checks.js <code>
node tools/axe_tabs.js dist/<code>/index.html
bash tools/derive.sh <CODE>
python3 tools/canvas-quiz/make_quiz.py <CODE> && python3 tools/canvas-quiz/check_quiz.py <CODE>
```

`render_checks.js` renders the pages with the same KaTeX version the live site loads (pinned in `build.js` and
`tools/package.json`), including its fonts, so widths match what students see.

## 5. The independent audit

A separate agent that did not build the page reviews it. It gets the page, the CheckIt generator, the worked
examples and this checklist, and it:

1. Recomputes every key, distractor and explanation, and checks the figures numerically from their scripts.
2. Simulates the generator and lists cases the items do not practice, and any convention that contradicts CheckIt.
3. Looks for giveaways within each tab, and checks the Quick Summary against the generator.
4. Checks the speak lines and the worked-examples PDF.

The scripts in section 4 catch the mechanical rules, so the audit can focus on math, coverage and judgment.

## 6. Dr. Romero's review

The pages carry Dr. Romero's name, so he reviews each one before it is used:

1. Look through the live page and the worked-examples PDF.
2. For an independent math check, run `python3 tools/review_packet.py <CODE>`. It writes
   `review/<CODE>_math_review.md` (not published), a plain file with every question, choice, marked answer and
   explanation. Paste it into another AI and ask it to verify the math, then bring any findings back.
3. Accessibility audits here are AI-assisted, not a compliance certification. Final acceptance goes through
   SAC/RSCCD's accessibility review, with testing on real assistive technology.

## 7. Standing agreements

- Finished outcomes are pushed straight to main, after the audit fixes are in.
- The shared-template accessibility advisories and MyOpenMath are not changed unless Dr. Romero asks.
- Dr. Romero pastes the LibreTexts code, imports the Canvas quizzes, and records the videos.
- When revising, keep the item count fixed. After a video is recorded, keep the example numbers.
