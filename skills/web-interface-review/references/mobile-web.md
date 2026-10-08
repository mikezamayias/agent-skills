# Mobile-web checks

Apply when the target is a PWA, is used on phones, or is a landing page.
Each check names the symptom, the cause, what to look for in code, and the fix.
Almost every fix is one CSS declaration or one meta tag, so flag JavaScript workarounds such as touch detection hooks or `touchmove` listeners as the wrong tool.

Contents: checks M1 to M11, global placement per framework, conflicts with the live rules, and the never-ship list.

## Checks

| Code | Symptom                                                               | Look for                                                                                   | Fix                                                                                                                                                                   |
| ---- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M1   | Hover style stays on after a tap                                      | Any `:hover` rule outside a capability query                                               | Wrap in `@media (hover: hover) and (pointer: fine)` and give touch its feedback through `:active`                                                                     |
| M2   | Gray or blue flash on tap                                             | No `-webkit-tap-highlight-color` on `html`                                                 | `-webkit-tap-highlight-color: transparent` once on `html`, plus an `:active` state on every tappable element                                                          |
| M3   | Bottom UI hidden under the URL bar, or page overflows on load         | `100vh` or `h-screen` on an app shell, drawer, or bottom-pinned element                    | `100dvh` for app shells and sheets, `100svh` as `min-height` for heroes                                                                                               |
| M4   | iOS zooms into a focused field and never zooms back                   | Input, textarea, or select font size under 16px                                            | 16px minimum, optionally only under `@media (pointer: coarse)`                                                                                                        |
| M5   | Taps feel late                                                        | No `touch-action` on controls, press feedback only on `click`                              | `touch-action: manipulation` on buttons, links, and `[role="button"]`, `:active` styling or `pointerdown` for instant feedback                                        |
| M6   | Pull-to-refresh or page bounce fights the app                         | Inner scroll areas, sheets, or canvases with no `overscroll-behavior`                      | `overscroll-behavior: contain` on inner scrollers and sheets, root handling per the conflict table below                                                              |
| M7   | Content clipped by the notch or home indicator, or a letterboxed edge | `env(safe-area-inset-*)` without `viewport-fit=cover`, or fixed bars with no inset padding | `viewport-fit=cover` in the viewport meta, then `env(safe-area-inset-*, 0px)` padding on fixed headers, tab bars, toasts, and sheets                                  |
| M8   | Long-press selects a button label or opens the link callout           | Controls with selectable text                                                              | `user-select: none` with the `-webkit-` prefix and `-webkit-touch-callout: none` on controls only, never on `body` or content                                         |
| M9   | Swiping a carousel also scrolls the page                              | Custom horizontal gesture surface with no `touch-action`                                   | `touch-action: pan-y` on a horizontal gesture surface, or native `scroll-snap-type: x mandatory` instead of a JavaScript gesture                                      |
| M10  | Status bar color clashes in one color scheme                          | A single `theme-color`, or none                                                            | One `theme-color` meta per `prefers-color-scheme` matching the top-of-page background, plus `color-scheme`, and the PWA manifest `theme_color` kept consistent        |
| M11  | Keyboard or field type is wrong on the phone                          | Missing `type`, `inputmode`, `enterkeyhint`, `autocapitalize`                              | `inputmode="numeric"` for codes, `"decimal"` for amounts, `type="email"` or `"tel"`, `autocapitalize="none"` on usernames and codes, `enterkeyhint` naming the action |

Notes that change the verdict:

- M3: `dvh` resizes while the URL bar moves, which suits app shells but shifts marketing content mid-scroll, so heroes take `svh`.
- M6: `touch-action: none` is only for elements that own every axis, such as a drag-to-dismiss handle, because users cannot scroll past it.
- M7: without `viewport-fit=cover` every `env()` inset resolves to `0px`, so the padding silently does nothing.
- M10: if the theme toggles by class instead of the OS setting, the meta must be updated on toggle.
- Android keyboard: `interactive-widget=resizes-content` in the viewport meta makes the keyboard shrink the layout so `dvh` and bottom-pinned inputs react as on iOS.
- Landscape text inflation: `-webkit-text-size-adjust: 100%` on `html`.

## Baseline for a phone-first app

```html
<meta
  name="viewport"
  content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content"
/>
<meta
  name="theme-color"
  media="(prefers-color-scheme: light)"
  content="#ffffff"
/>
<meta
  name="theme-color"
  media="(prefers-color-scheme: dark)"
  content="#0a0a0a"
/>
```

```css
html {
  -webkit-tap-highlight-color: transparent;
  -webkit-text-size-adjust: 100%;
}
input,
textarea,
select {
  font-size: 16px;
}
button,
a,
[role="button"] {
  touch-action: manipulation;
}
```

Replace the colors with the real top-of-page backgrounds.

## Global placement

| Stack      | Viewport and theme-color                                                                                                        | Base CSS                                                   |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Nuxt       | `app.head.viewport` and `app.head.meta` in `nuxt.config.ts`, or `useHead` in `app.vue`, and `pwa.manifest` for `@vite-pwa/nuxt` | The global stylesheet listed in `css:` in `nuxt.config.ts` |
| SvelteKit  | `src/app.html`, and the manifest of `@vite-pwa/sveltekit`                                                                       | The stylesheet imported by the root `+layout.svelte`       |
| Plain HTML | The document `<head>` and the web manifest                                                                                      | The site stylesheet                                        |

Tailwind v4 already compiles `hover:` inside `@media (hover: hover)`, which covers M1.
Tailwind v3 needs `future.hoverOnlyWhenSupported: true`.
`h-screen` is `100vh`, so M3 wants `h-dvh` or `min-h-svh`.

## Conflicts with the live rules

| Topic           | Live rules                                                                          | Mobile-web                      | Resolution                                                                                                                                              |
| --------------- | ----------------------------------------------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Root overscroll | `none` on `html` only under `@media (pointer: fine)`, keep pull-to-refresh on touch | `none` on `html, body` for apps | Installed or standalone PWA with its own scroll containers takes `none`. A document site such as a landing page or personal site follows the live rule. |
| Hover states    | Buttons and links need a hover state                                                | Hover must be capability-gated  | Require both: a hover state that lives inside the capability query, plus `:active` for touch.                                                           |

## Never ship

- `user-scalable=no` or `maximum-scale=1`, because they block zoom for low-vision users.
  Fix M4 instead.
- User-agent or screen-width sniffing to detect touch, instead of `(hover)` and `(pointer)` queries.
- `touchmove` with `preventDefault()` to stop overscroll, which blocks scrolling and makes the listener non-passive.
- `user-select: none` on `body`, because users copy addresses, codes, and error text.
- A mobile fix declared done from desktop device emulation.

## Needs a phone

Emulation reproduces none of these: sticky hover, tap highlight, URL-bar height changes, input zoom, tap delay, rubber-banding, safe areas, the software keyboard, and standalone PWA mode.
Report them as code-verified only, and name the device test: dev server on `0.0.0.0` opened by LAN IP, Safari Web Inspector for iOS or `chrome://inspect` for Android, with the keyboard open, once in landscape, and once installed when the target is a PWA.

Source: condensed and paraphrased from Emil Kowalski's `mobile-native` skill (MIT, Copyright (c) 2026 Emil Kowalski).
