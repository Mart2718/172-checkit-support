# 172 CheckIt Support

One repository and one Netlify site for the CheckIt support pages in Math 172 (*Building Toward Calculus*, Santa Ana College).
Each learning outcome is a single content file. A shared template turns it into an accessible page.

## What is where

| Folder or file | What it is | Do you edit it? |
|---|---|---|
| `content/FN1.yml` | All the words, numbers, answers and explanations for one outcome | Yes, this is the file you edit |
| `figures/FN1/*.svg` | The pictures (mapping diagram, graphs) for that outcome | Rarely |
| `template/styles.css`, `template/app.js` | Look and behavior shared by every page | Only to change all pages at once |
| `build.js` | Turns each content file into a page and builds the hub page | No |
| `tools/` | Accessibility checks and the worked-examples generator | No (Claude uses these) |
| `netlify.toml`, `package.json` | Tell Netlify how to build | No |
| `dist/` | The finished site (created by the build, not stored in GitHub) | Never |

## Web addresses

- Hub page: `https://YOUR-SITE.netlify.app/`
- One outcome: `https://YOUR-SITE.netlify.app/fn1/`
- For the LibreTexts iframe add `?embed=1`: `https://YOUR-SITE.netlify.app/fn1/?embed=1`

## Fix or change something

1. On GitHub, open `content/FN1.yml` and click the pencil (Edit) icon.
2. Change the text. Keep the indentation (spaces, never tabs) and keep the quote marks.
3. Click **Commit changes**. Netlify rebuilds in under a minute and the page updates everywhere, including inside LibreTexts.
4. If something is wrong the build stops with a plain message that names the outcome and the item, and the last good version stays live. Open **Deploys** in Netlify and click the failed deploy to read it.

Math is typed as normal LaTeX between backslash-paren markers, for example `\( y^2 \)`. In `content/*.yml` you do NOT need to double the backslashes.

## Add the video later

In `content/FN1.yml` add these lines at the top level (no indentation):

```yaml
video:
  url: https://www.youtube.com/watch?v=VIDEO_ID
  embed: https://www.youtube.com/embed/VIDEO_ID
  title: "FN1 video walkthrough: is a relation a function?"
  transcript: https://example.com/fn1-transcript
```

The `transcript` line is optional. Commit, and the Video tab shows a link and the player in place of "coming soon".

## Add a new outcome

1. Copy `content/FN1.yml` to `content/FN2.yml` and replace the content (Claude can draft this for you).
2. Put its pictures in `figures/FN2/`.
3. Commit. The new page appears at `/fn2/` and is added to the hub automatically.

## After you record the video

Keep the example numbers as they are. If you change the numbers, the video, the worked-examples document and the page stop matching. Wording and accessibility fixes are always safe.

## Safety checks built in

The build refuses to publish a page when a figure has no text description, a table has no caption, a "correct" answer is not one of the choices, math delimiters are unbalanced, or a figure or table caption gives away the answer before the student guesses (using the phrases listed under `banPhrases` in each content file).

## Licensing

TBIL content is CC BY-NC-SA 4.0 (Steven Clontz and Drew Lewis). These pages are published under the same license (non-commercial, share-alike).
