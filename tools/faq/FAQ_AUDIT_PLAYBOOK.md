# FAQ / Guided-Learning Audit Playbook (Math 172)

How to audit Marty's FAQ and guided-learning pages, one GitHub repo per section (Mart2718/172*FAQ, about 32 repos; a few are combined, such as 172FN2-and-FN3, 172pr45faq, 172PR12FAQ, 172LF235FAQ, 172El56FAQ, 172LF1, 172FN1). TR1 (Mart2718/172TR1FAQ) is the finished pilot; use it as the model.

## Standing agreements with Marty
- Push finished fixes straight to each repo's `main`. Each repo stands alone.
- Fixes must be mathematically correct **and** consistent with CheckIt: its angle and value ranges, answer forms and pictures. If the math and CheckIt disagree, follow the math, say so, and point it out to Marty.
- Do not touch MyOpenMath or the shared-template advisories unless he asks.
- Keep the structure. Don't add or remove FAQs, videos or stops unless he agrees.
- Marty reviews by hand afterward and sends a ChatGPT review. Fold in what is correct; push back where it conflicts with CheckIt.

## Per-repo steps
1. Clone the repo. If a push fails, call `add_repo(owner "Mart2718", repo, access "push")`.
2. Packet: `python3 tools/faq/faq_packet.py <repo> <scratchpad>/<CODE>_faq_packet.md`. It lists FAQs, path stops, videos, apps and prompts, shows graphs as their descriptions, and flags graphs that are missing or unused.
3. Automated checks: `node tools/faq/faq_checks.js <repo>`. It checks KaTeX 0.16.47 rendering, graphs with no description, sideways scroll, and axe at 1000 px and 320 px. Run `npm install` in tools/faq first. Run it in the background if it's slow.
4. Links: shell and WebFetch can't reach YouTube or Netlify apps. Use Claude in Chrome:
   - Videos: open youtube.com/robots.txt, then fetch `/oembed?url=https://www.youtube.com/watch?v=ID&format=json` with javascript_tool. Look for status 200 and a title that matches.
   - Apps: navigate to each one and read document.title.
   - Chrome site permission is granted per domain. If a domain is blocked, skip it; Marty checks those himself.
5. Independent audit: a separate agent that hasn't seen your work checks the math, the CheckIt fit (compare against the support page content/<CODE>.yml and the CheckIt generator), the graphs and the prompts. It sorts findings into MUST FIX, SHOULD FIX and NIT.
6. Apply the fixes, rerun the checks, commit with the attribution lines, and push.
7. Report to Marty in a table: what changed, and the decisions waiting on him. Send the packet for ChatGPT.

## Content standards (from the TR1 pilot)
- **Scope notes:** where the FAQ goes past what CheckIt assesses (for example negative angles), label it "Extension" or "beyond the [CODE] CheckIt exercise". Never write "Beyond [CODE]": the learning objective is broader than the CheckIt exercise. Put one "Practice scope" line in the path intro, plus a one-line tag on each FAQ or video that goes beyond, because students open these one at a time.
- **Guided-path values must not repeat the support page's problems.** Compare against content/<CODE>.yml and swap in fresh values. Repeats inside the path (draw it in one stop, convert it in another) are fine.
- Make sure the path practices edge cases CheckIt can produce, such as angles on an axis. Add optional stretches when Marty agrees.
- **Precise wording,** for example:
  - "multiples of 30° **or** 45°"
  - "strictly between" for quadrant ranges, and say that axis angles are in no quadrant
  - "fractions of π" rather than "multiples of π"
  - "the denominator tells how many equal slices make a half turn"
  - Reflect questions with an exact answer: "which four angles from 0° up to 360°…"
- **Graphs:**
  - Every SVG gets `role="img"` and an `aria-label` (take it from its caption).
  - No clipped labels; widen the viewBox if needed.
  - Captions must not rely on color alone.
  - **Angle sides are rays with arrowheads**, as in CheckIt's answer pictures, which show arrowheads on both sides and a plain angle arc with its measure. On a unit circle with a marked point, the sides are segments ending at the point. Radii of a circle are segments. Turn arcs get an arrowhead showing direction.
  - Check graphs visually with a Playwright screenshot before pushing.
- **Template accessibility fixes** (index.html; every repo probably needs them):
  - `.gl-prompt-preview` gets `tabindex="0" role="region" aria-label="Prompt text"`.
  - Orange links (`.resource-card a`, `.video-card-body a`, inline `color:var(--orange)`) become `#a84d16` for contrast.

## AI prompt standard
Rubric for each prompt: fits the objective and CheckIt; coaches rather than answers; makes the AI's role visible and has the student critique it; doesn't overlap with the guided-path prompts; still works. Rate each one keep, revise or retire. Marty approved applying the drafted rewrites and reviewing later.
- Each prompt includes an error-catching step: the AI makes one deliberate mistake, or the student checks an AI claim against notes or CheckIt.
- Prompts with deliberate errors end with: "After I respond, check my reasoning and give me the fully corrected solution before we finish."
- Don't make students discover a definition cold. Start from what they know, give hints, then help them explain it.
- Prompts that reach past the section are retitled "Extension: …".
- Guided-path tutor template (index.html buildPrompt): step 7 is "Then solve one problem yourself and make one deliberate mistake. I'll find it and explain what went wrong. Then check my reasoning and show me the fully corrected solution." Step 8: "When I've solved your problem correctly and found your mistake, tell me…"

## Order
Do repos in batches of 3 to 5, grouped by chapter, matching the support-page batches. Report after each batch.
