---
name: app-landing-page
description: >-
  Generate five distinct landing page versions for an app, each a complete deployable single-file HTML. Use when creating or refreshing an app's landing page. Each version follows a different design philosophy rather than five drafts of the same page.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
metadata:
  openclaw:
    emoji: 🛬
---

# app-landing-page

This skill produces 5 distinct landing page attempts for an app.
Each version is a complete deployable single-file HTML page with inline CSS and JS.
The 5 versions follow 5 different design philosophies so the human can pick one, instead of 5 drafts of the same page.

## When to invoke

The human says something like "make a landing page for this app", "I need 5 landing-page attempts", "draft a launch page", or "let multiple models try the landing page for X".

## Activation rules

1. The working directory must be a project root with a `pubspec.yaml`, `package.json`, or `README.md`.
2. No specific model or tool is required.
   The current agent can write all 5 versions itself.
3. If the human asks for several models, or the environment offers other models or agents, such as subagents, another agent CLI, or a model API, you may hand some versions to them for more variety.
   Use only tools that are already installed and signed in.
   Do not install or sign up for a tool without the human's approval.

## The 5 design philosophies

These are 5 distinct framings with no overlap.
Keep all 5, because the variety is the point.

| Version                   | Philosophy                                                       | Typical structure                                                                      |
| ------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **v1 - Hero-led**         | Above-the-fold sells the entire pitch                            | Big hero, 1 strong CTA, 3-feature row, footer                                          |
| **v2 - Story-led**        | Linear narrative scroll, problem → solution → proof              | Long-form sections, no hero CTA, and the CTA shows up mid-scroll once the case is made |
| **v3 - Product-tour-led** | Annotated screenshots are the page, and copy supports them       | Big screenshot stack, captions, minimal chrome, mobile-first                           |
| **v4 - Social-proof-led** | Testimonials, install counts, GitHub stars front-loaded          | Stats bar at top, quotes mid, CTA + screenshot bottom                                  |
| **v5 - Manifesto-led**    | Opinionated essay style, "why this exists", indie / founder tone | Wall of text, signature, single download link, no marketing language                   |

## Who writes each version

By default the current agent writes every version.
Write each one as a fresh attempt from the brief and that version's philosophy, not as an edit of an earlier version.

When other models or agents are available, spread the versions across them, for example one model per version, and give each one the same prompt template.
Record which model or tool produced each version in `INDEX.md`.

## Project discovery (Phase 0)

Build the brief from these files only:

- `pubspec.yaml` → `name`, `description`
- `README.md` → first heading + first paragraph
- `store_assets/BRAND_PROFILE.md` (if `app-graphics` ran already) → colors, voice
- `store_assets/graphics/app_icon/app_store_1024x1024.png` (if exists) → reference for visual style
- `store_assets/screenshots/framed/en-US/` (if exists) → screenshots to embed

Write `landing-pages/LANDING_BRIEF.md`:

```markdown
# <App> landing brief (built <YYYY-MM-DD>)

- Name: …
- One-liner: …
- Target audience: …
- Primary CTA: <e.g. "Join the TestFlight", "Download on the App Store", "Get on GitHub">
- Anchor colors: …
- Voice: …
- Key proof points (max 5): …
- Available screenshots: <relative paths or "none">
```

**Stop and ask the human** if you cannot confidently fill these fields.
Do not invent them.

## Output structure

```text
landing-pages/
├── LANDING_BRIEF.md
├── INDEX.md                  # which model or tool produced which version + verdict
├── v1-hero-led.html
├── v2-story-led.html
├── v3-product-tour-led.html
├── v4-social-proof-led.html
└── v5-manifesto-led.html
```

Each `.html` is a **single file** with inline CSS and inline JS.
Use base64 images only if absolutely needed, and otherwise reference images by relative path to `store_assets/`.
There is no build step, so the file works when dropped on any static host, such as Cloudflare Pages, Vercel, or GitHub Pages.

## Per-version prompt template

Build the prompt for each version from the brief and the version's design philosophy.
Use it as the instruction for yourself, or send it unchanged to another model.

```text
Build a single-file HTML+CSS+JS landing page for "<App name>".

One-liner: <…>
Target audience: <…>
Primary CTA: <…>
Anchor palette: <hex codes>
Voice: <…>

Design philosophy for THIS version: <one of the 5 above, copied from the table>

Constraints:
- Single .html file. Inline all CSS and JS. No external dependencies except Google Fonts (one family max) and an optional inline SVG icon set.
- Mobile-first responsive (works at 375×667).
- One primary CTA on the page; secondary CTAs allowed but visually subordinate.
- Real copy only. No "Lorem ipsum", no placeholders.
- No marketing puffery: no "transformative", "revolutionary", "the best", "simplify your life", "unlock the power of". Write headlines in plain, specific language.
- Light mode default; dark mode via `prefers-color-scheme: dark` if the philosophy fits.
- Screenshots: <relative paths from LANDING_BRIEF, or "none, design around it">
- Accessibility: semantic landmarks, alt text, color contrast WCAG AA.

Return only the complete HTML file. No commentary.
```

When another model returns the page, save only the HTML and strip any commentary around it.

## Verification per version

For each generated HTML:

- [ ] Loads in a browser without console errors.
- [ ] Mobile viewport (375×667) renders without horizontal scroll.
- [ ] No "Lorem ipsum" or placeholder text leaked through.
- [ ] Primary CTA is wired to a real URL, or to `# TODO: …` clearly marked if not yet known.
- [ ] No external script tags from untrusted CDNs (audit `<script src=`).
- [ ] Color contrast passes WCAG AA on body text, checked with a contrast tool.

Use a browser automation tool if one is available.
Otherwise open the file in a local browser and ask the human to check what you cannot see.

If a version fails, revise it with a targeted fix, using the same model or tool that produced it.
If it still cannot be made to work, mark it `Stuck` in `INDEX.md` and move on.

## Write the INDEX

After all 5 are generated, write `landing-pages/INDEX.md`:

```markdown
# Landing page versions for <App name> (built <YYYY-MM-DD>)

| Version | Philosophy       | Model or tool | Words | Verdict (human fill) | Path                                   |
| ------- | ---------------- | ------------- | ----- | -------------------- | -------------------------------------- |
| v1      | Hero-led         | <model>       | XXX   |                      | landing-pages/v1-hero-led.html         |
| v2      | Story-led        | <model>       | XXX   |                      | landing-pages/v2-story-led.html        |
| v3      | Product-tour-led | <model>       | XXX   |                      | landing-pages/v3-product-tour-led.html |
| v4      | Social-proof-led | <model>       | XXX   |                      | landing-pages/v4-social-proof-led.html |
| v5      | Manifesto-led    | <model>       | XXX   |                      | landing-pages/v5-manifesto-led.html    |

## Stuck / skipped

- (list any version that did not generate, with the model and the failure reason)
```

## Run log

Append one line to `landing-pages/runs-log.md`:

```text
YYYY-MM-DD HH:MM - <project> - 5 versions (<model> x N, ...)
```

## Related skills

- `app-graphics` generates the icon and OG card this landing page references.
- `app-screenshots` generates the framed screenshots this landing page embeds.
