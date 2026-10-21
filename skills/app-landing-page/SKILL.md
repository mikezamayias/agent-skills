---
name: app-landing-page
description: >-
  Generates five distinct landing page versions for an app, each a complete deployable single-file HTML. Use when creating or refreshing an app's landing page. Each version follows a different design philosophy rather than five drafts of the same page.
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
- If the page receives TikTok or Instagram bio traffic, the primary CTA must still work inside their in-app browser. Add a full-screen overlay with an arrow to the ••• menu and "Tap ••• → Open in browser", and keep a visible Download button. One founder's claim (2026-10-20), untested, see the link-in-bio notes in `ship-first-dollar-app` references/distribution-channels.md.
- Real copy only. No "Lorem ipsum", no placeholders.
- No marketing puffery: no "transformative", "revolutionary", "the best", "simplify your life", "unlock the power of". Write headlines in plain, specific language.
- No AI-copy tells: no "where X meets Y", no "not just X but Y", no "scroll to explore", and no "hover" in copy a touch visitor reads.
- Avoid unless the concept demands it, and then say why in INDEX.md: a centered hero over a gradient blob, purple-blue gradients, cream with terracotta serif editorial, acid green on black, glassmorphism, an eyebrow label over every heading, and 01/02/03 numbering on content that is not a sequence.
- Light mode default; dark mode via `prefers-color-scheme: dark` if the philosophy fits.
- Screenshots: <relative paths from LANDING_BRIEF, or "none, design around it">
- Accessibility: semantic landmarks, alt text, color contrast WCAG AA.
- Concept: one sentence naming what this page is about that only this app could own, anchored in a real fact from the brief. If the sentence still works with another app's name swapped in, it is a style, not a concept. Carry it through every section, not just the hero.
- Type: body 16-18px with 1.45-1.6 line height, 45-70 characters per line, tabular figures for numbers, a non-breaking space between a number and its unit.
- Motion: animate only transform, opacity and clip-path. Under `prefers-reduced-motion`, all content must be visible with no scroll-driven animation.
- Autoplaying loops: motion that starts by itself, lasts more than 5 seconds and runs beside other content needs a control to pause, stop or hide it (WCAG 2.2 criterion 2.2.2, Level A), unless the motion is essential. Gating it behind `prefers-reduced-motion` does not satisfy 2.2.2. Content that updates automatically has no 5 second exception, and a control for the update frequency also satisfies it.
- Interaction: primary targets (CTA, nav, screenshot links) answer with one movement treatment per role (label roll, underline draw, fill, arrow nudge), never only a color change. Legal and social links may only change color. Put every :hover inside @media (hover: hover), give the same state to :focus-visible, and under prefers-reduced-motion keep a visible color or underline state instead of the movement.
- No em or en dashes in copy. Exactly one <h1>.
- The top third says what the app is, who it is for and what to do next. The last CTA on the page uses the same label as the first. A logo row holds at most 6 logos. Every metric carries a visible source line.

Return only the complete HTML file. No commentary.
```

The last constraint line is adapted from the `taste-landing-page` skill in madebymustafa/design-taste (MIT, read at commit `c4a6bff`, 2026-10-16).
Those are that skill's own rules, not findings from conversion research, so treat them as defaults and drop one when a version's philosophy needs to.

The copy tells, the avoid list and the movement-per-role rule in the template are adapted from juliobsz/skills `/awwwards` (MIT, read at commit `461fab3`, 2026-10-16), where the audit script flags the copy tells and the skill lists the avoid list.
The hover gating and reduced-motion lines rest on the CSS Media Queries Level 5 `hover` feature and MDN `prefers-reduced-motion`, not on that skill.
`hover: hover` means the primary pointing device can easily hover, and the query tests only the primary input.

When another model returns the page, save only the HTML and strip any commentary around it.

## Verification per version

For each generated HTML, measure in a real browser (`agent-browser`, the T3 preview, or Chrome DevTools MCP as in `web-perf`) rather than eyeballing:

- [ ] Zero console errors and zero failed requests.
- [ ] No horizontal overflow at 375×667. Name the offending element if there is one.
- [ ] Zero serious or critical axe-core violations at WCAG 2.1 AA, which also measures contrast ratios.
- [ ] Every tap target at least 24×24px.
- [ ] Keyboard: every focus stop visible, tab order follows the page, the CTA reachable.
- [ ] Reduced motion: emulate `prefers-reduced-motion: reduce` and confirm no text stays hidden.
- [ ] Throttled mobile (4× CPU, slow 4G): Largest Contentful Paint under 2.5s and Cumulative Layout Shift under 0.05.
- [ ] Text audit: no "Lorem ipsum", `TODO` outside the CTA, or bracketed placeholders; no repeated sentences; none of the copy tells "where X meets Y", "not just X but Y" or "scroll to explore"; exactly one `<h1>`; every image has `alt` and every link a name.
- [ ] Hover: capture each primary target at rest and under the pointer at the same clip. Fail any primary target with no visible change, and read every color-only change by eye. A full fill or inversion passes, and a text-color swap on a CTA or nav link does not.
- [ ] Idle: leave the pointer still for five seconds on desktop. If nothing that carries the concept moves, write "still by decision" in INDEX.md, or add a small idle motion on the concept itself, never a decorative floating shape. Any idle loop that runs more than 5 seconds beside other content follows the autoplaying loops rule above.
- [ ] Primary CTA is wired to a real URL, or to `# TODO: …` clearly marked if not yet known.
- [ ] No external script tags from untrusted CDNs (audit `<script src=`).
- [ ] Search and AI-answer ship checks from [references/seo-and-ai-answers.md](references/seo-and-ai-answers.md) pass for the chosen version, which also holds the recurring SEO loop.

Record any check you could not run as not verified in `INDEX.md`, rather than passing it.
If no browser tool is available, open the file in a local browser and ask the human to check what you cannot measure.

Then run a fresh critic: a new subagent that sees only the version's mobile and desktop screenshots and the check results, not the prompt or this conversation.
It writes one sentence on what the page is about, then scores Design, Usability, Creativity and Content from 1 to 10, starting each at 6 and citing a screenshot or check result for every point above it, and lists the top 3 fixes.
Give it the rest and hover screenshot pairs from the Hover check too.
Put the screenshots before the text in its message, because Anthropic's vision docs say Claude works best when images come before text, and describe image-then-text as a preference since other orders still perform well.
Launch a new critic after every revision, so it never anchors on an earlier score.
If its sentence does not match the version's Concept line, fix the page, not the critic.
Dispute a score only by naming the screenshot it misread.
Put its scores and the sentence in the `INDEX.md` Critic column. The human still picks the winner.
Before recording the verdict, cut the weakest decorative effect on each version. Hover, press and focus feedback are not decoration and stay.
Thresholds and the critic method are adapted from juliobsz/skills `/awwwards` (MIT, read at commit `461fab3`, 2026-10-16).

If a version fails, revise it with a targeted fix, using the same model or tool that produced it.
If it still cannot be made to work, mark it `Stuck` in `INDEX.md` and move on.

## Write the INDEX

After all 5 are generated, write `landing-pages/INDEX.md`:

```markdown
# Landing page versions for <App name> (built <YYYY-MM-DD>)

| Version | Philosophy       | Model or tool | Words | Critic (scores + sentence) | Verdict (human fill) | Path                                   |
| ------- | ---------------- | ------------- | ----- | -------------------------- | -------------------- | -------------------------------------- |
| v1      | Hero-led         | <model>       | XXX   |                            |                      | landing-pages/v1-hero-led.html         |
| v2      | Story-led        | <model>       | XXX   |                            |                      | landing-pages/v2-story-led.html        |
| v3      | Product-tour-led | <model>       | XXX   |                            |                      | landing-pages/v3-product-tour-led.html |
| v4      | Social-proof-led | <model>       | XXX   |                            |                      | landing-pages/v4-social-proof-led.html |
| v5      | Manifesto-led    | <model>       | XXX   |                            |                      | landing-pages/v5-manifesto-led.html    |

## Stuck / skipped

- (list any version that did not generate, with the model and the failure reason)
```

## Run log

Append one line to `landing-pages/runs-log.md`:

```text
YYYY-MM-DD HH:MM - <project> - 5 versions (<model> x N, ...)
```

## Several apps

For several apps use one Astro codebase with one content collection per app, so shared changes (crawler rules, JSON-LD, localization) land once.
Write the site recipe as a skill after the first app ships, naming where assets, copy and keyword data come from.
This is a preference stated in a video by Dan Kulkov (2026-10-19), not a comparison against other frameworks, and it applies to a site that outgrows the single-file pages above.

## Related skills

- `app-graphics` generates the icon and OG card this landing page references.
- `app-screenshots` generates the framed screenshots this landing page embeds.
- For a "how it works" figure, use the `anatomy` skill, at most one per page and only when the page must explain a mechanism, with every fact taken from the brief and never invented.
- For an "AI is building this" reveal on a feature card, read [references/ai-generation-effect.md](references/ai-generation-effect.md) first. Never on the hero, unless a throttled lab run with the effect on the hero element keeps Largest Contentful Paint at or under 2.5 s.
