# "AI is generating this" reveal effect

Source: the free `transitions-ui-generation` skill in [Jakubantalik/transitions.dev](https://github.com/Jakubantalik/transitions.dev), read in full at commit df2d4d0 (2026-10-12) and re-checked unchanged at 6c4de54 (2026-10-15).
Its license allows unlimited personal and commercial use and modification.
It forbids republishing the collection as a competing animation kit, so copy the two runtime files into the landing page project only, never into this catalog or the public mirror.

## What it does

It draws a dotted wireframe of a real DOM element, measured from the element itself: outline, child boxes, text lines, inline SVG icons, guides and size labels.
It then reveals the element top to bottom behind a scan line.
`skeleton` mode is the drawing and reveal only.
`skeleton-texts` mode adds an agent log and a CSS panel beside the element, placed only where the page is empty.
One run lasts about 2.6 seconds at the default `duration: 2400`.
`duration` accepts 1600 to 3600 ms, and the upstream homepage uses 1600 on its small prompt box.
Use 1600 on a small card so the run stays under 2 s.

## Use

Copy `ui-generation.js` and `ui-generation.css` from the skill folder into the page, with no dependencies.

```html
<link rel="stylesheet" href="ui-generation.css" />
<script type="module">
  import { generate } from "./ui-generation.js";
  await Promise.race([
    document.fonts.ready,
    new Promise((r) => setTimeout(r, 600)),
  ]);
  generate(document.querySelector("#feature-card"), { mode: "skeleton-texts" });
</script>
```

Build the target as real HTML.
On an `<img>` such as a framed screenshot it draws one rectangle and nothing else.
To reproduce the launch video's `MOTION.CSS // 05 RECIPES` panel, pass your own `code: [...]` lines, because the shipped panel prints generic derived CSS.
The font wait has a 600 ms ceiling so a slow font never delays the reveal, the same ceiling the upstream homepage uses in `assets/community/composer-generate.js`.
The upstream site's own runtime has a fade reveal without the scan line (`reveal: "fade"`, `fadeDuration`, `revealAt`), but that file sits outside both license sections in the repository `LICENSE`, so do not copy it.
Use the skill copy's scan reveal.

## Traps

1. `auto()` hides the element with `opacity: 0` and waits for 35% of it to be visible (IntersectionObserver `threshold: 0.35`, `ui-generation.js:471`). An element taller than about 2.86 viewports never reaches that ratio and stays invisible on phones. Use `generate()` on cards, or lower the threshold in your copy.
2. Never use it on the hero. The element is invisible for the whole run, which delays Largest Contentful Paint (LCP).
   The ban can be lifted only when a throttled lab run keeps LCP at or under 2.5 s with the effect running on the hero element.
   Use the 4x CPU and slow 4G profile from "Verification per version" in `SKILL.md`.
   The 2.5 s threshold is assessed on the 75th percentile of real page loads, so a lab run only gates the lift and does not prove the field figure (web.dev, "Defining the Core Web Vitals metrics thresholds").
   The upstream homepage runs the effect on its above-the-fold prompt box at `duration: 1600`, and nobody measured whether that box is its LCP element.
3. Cost grows with element area. Every dot is updated each frame, so a 1200×700 block is about 4,600 dots. Keep it to cards.
4. The overlay is placed once in page coordinates. It does not follow resize, scrolling containers, or sticky and fixed elements.
5. The element stays focusable while hidden. Play it once, after load. If anything near it can be clicked or typed into, call `run.cancel()` on the first capture-phase `pointerdown`, `keydown` or `focusin`, and remove those listeners when `run.finished` resolves.
   `cancel()` shows the element at once.
   The upstream homepage wires it this way.
6. Reduced motion is respected: the drawing is skipped and the element fades in over 200 ms.
7. `generate()` sets `opacity: 0` itself, so a module script that calls it can leave the element visible for one paint first.
   This is inferred from the code and was not measured.
   The upstream homepage hides the element before first paint with a class set from an inline head script, unless reduced motion is on.
   It removes the class once `generate()` has run and also with a 4 s `setTimeout` as a failsafe.
   Copy that pattern: `.gen-pending #feature-card { opacity: 0 }`.
8. The shipped runtime can show the finished wireframe for one frame before the drawing starts.
   Upstream commit `fe16dc2` fixes this in the site's own runtime with one call, `frame(G, 0, 0, D);`, made right after the overlay is built and before the first `requestAnimationFrame(tick)`.
   The skill copy still lacks it.
   In your copy of `ui-generation.js`, add that line after `const D = ..., t0 = performance.now();` inside `generate()`, before `const tick`.
   The skill license allows modifying its files.

## Promo videos

HyperFrames renders by seeking frames and forbids `requestAnimationFrame` and `performance.now()`.
The runtime uses both and exports neither `measure` nor `frame`, so it does not render in HyperFrames as shipped.
Screen-record the browser at 60 fps and import the clip, or fork the file to export a `seek(p)` driven by `hf-seek`.

## Never run the CLI

Do not run `npx transitions-agent`, and do not run `npx transitions-agent skill --codex` either, because that subcommand installs a managed block in `~/.codex/AGENTS.md` on request.
A plain scan copies a skill into `~/.claude/skills` and appends an instruction block to `~/.codex/AGENTS.md` without asking (`agent/bin/transitions-agent.mjs:87-108`, called at line 523).
On the user's machine `~/.codex/AGENTS.md` is a symlink to the global `instructions/AGENTS.md`, so one scan would inject third-party instructions into every agent.
The `skill --codex` write is verified for version 0.3.6 (PR #23, merged 2026-09-29) and not read in the source of the current 0.11.1, so treat both as written.
