# "AI is generating this" reveal effect

Source: the free `transitions-ui-generation` skill in [Jakubantalik/transitions.dev](https://github.com/Jakubantalik/transitions.dev), read in full at commit df2d4d0 (2026-10-12).
Its license allows unlimited personal and commercial use and modification.
It forbids republishing the collection as a competing animation kit, so copy the two runtime files into the landing page project only, never into this catalog or the public mirror.

## What it does

It draws a dotted wireframe of a real DOM element, measured from the element itself: outline, child boxes, text lines, inline SVG icons, guides and size labels.
It then reveals the element top to bottom behind a scan line.
`skeleton` mode is the drawing and reveal only.
`skeleton-texts` mode adds an agent log and a CSS panel beside the element, placed only where the page is empty.
One run lasts about 2.6 seconds at the default `duration: 2400`.

## Use

Copy `ui-generation.js` and `ui-generation.css` from the skill folder into the page, with no dependencies.

```html
<link rel="stylesheet" href="ui-generation.css" />
<script type="module">
  import { generate } from "./ui-generation.js";
  await document.fonts.ready;
  generate(document.querySelector("#feature-card"), { mode: "skeleton-texts" });
</script>
```

Build the target as real HTML.
On an `<img>` such as a framed screenshot it draws one rectangle and nothing else.
To reproduce the launch video's `MOTION.CSS // 05 RECIPES` panel, pass your own `code: [...]` lines, because the shipped panel prints generic derived CSS.

## Traps

1. `auto()` hides the element with `opacity: 0` and waits for 35% of it to be visible (IntersectionObserver `threshold: 0.35`, `ui-generation.js:471`). An element taller than about 2.86 viewports never reaches that ratio and stays invisible on phones. Use `generate()` on cards, or lower the threshold in your copy.
2. Never use it on the hero. The element is invisible for the whole run, which delays Largest Contentful Paint (LCP).
3. Cost grows with element area. Every dot is updated each frame, so a 1200×700 block is about 4,600 dots. Keep it to cards.
4. The overlay is placed once in page coordinates. It does not follow resize, scrolling containers, or sticky and fixed elements.
5. The element stays focusable while hidden. Play it once, after load, away from the first interaction.
6. Reduced motion is respected: the drawing is skipped and the element fades in over 200 ms.

## Promo videos

HyperFrames renders by seeking frames and forbids `requestAnimationFrame` and `performance.now()`.
The runtime uses both and exports neither `measure` nor `frame`, so it does not render in HyperFrames as shipped.
Screen-record the browser at 60 fps and import the clip, or fork the file to export a `seek(p)` driven by `hf-seek`.

## Never run the CLI

Do not run `npx transitions-agent`.
A plain scan copies a skill into `~/.claude/skills` and appends an instruction block to `~/.codex/AGENTS.md` without asking (`agent/bin/transitions-agent.mjs:87-108`, called at line 523).
On the user's machine `~/.codex/AGENTS.md` is a symlink to the global `instructions/AGENTS.md`, so one scan would inject third-party instructions into every agent.
