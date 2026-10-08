# Web and SwiftUI harnesses and failure signatures

Secondary stacks: Nuxt and Vue, Svelte, and SwiftUI.
Read only the section for the stack under test.
Flutter lives in flutter.md.

## Web (Nuxt, Vue, Svelte)

### Web harness

Hand web interface guideline review to `web-interface-review`.
Component tests in Vitest run in jsdom or happy-dom, which have no layout engine.
Use them only for text breaks: plurals, `null` rendering, number and date formatting, escaping, initials.
Use Playwright for layout, and add `@playwright/test` if the project lacks it.
Inject fixtures at the network boundary with `page.route` and `route.fulfill({ json })`, or seed storage with `page.addInitScript` for local-first apps, so nothing ships in the bundle.

- Width: `page.setViewportSize({ width: 320, height: 800 })`, then the real container width and the widest layout.
- Zoom: 200% browser zoom on a 1280 px window equals a 640 px viewport, so the width matrix covers layout zoom.
- Text-only scale: raise the root font size (`html { font-size: 200% }`).
  Text that does not grow uses `px` font sizes, which is a finding in itself.
- RTL: set `dir="rtl"` on `document.documentElement`.
- Dark mode: use the app's own theme switch (`@nuxtjs/color-mode` uses a class, not only the media query).
- Horizontal overflow check: `document.documentElement.scrollWidth > window.innerWidth`.
- Visual record: `toHaveScreenshot` only if the repository already stores screenshots.

### Live toggle (only when asked)

Read `?data=worst|empty|one|huge` where the fixture is chosen, and load the fixture with a dynamic `import()` inside a dev-only branch so production builds exclude it.

- Nuxt: `if (import.meta.dev)`.
- Vite with Svelte: `if (import.meta.env.DEV)`.

Render a small neutral segmented control fixed at bottom centre, labelled Demo, Worst, Empty, One, Huge, with no animation on the content.

### Web failure signatures

| What you see                                     | Cause                                     | Fix (CSS, then Tailwind)                                                                |
| ------------------------------------------------ | ----------------------------------------- | --------------------------------------------------------------------------------------- |
| Avatar or icon squished into an oval             | Flex child shrinking                      | `flex-shrink: 0`, `shrink-0`                                                            |
| Text overflows instead of wrapping or truncating | Flex or grid child with `min-width: auto` | `min-width: 0` or `minmax(0, 1fr)`, `min-w-0`                                           |
| Email or URL runs past the edge                  | No break opportunity                      | `overflow-wrap: anywhere`, `[overflow-wrap:anywhere]` or `wrap-anywhere` on Tailwind v4 |
| Trailing action pushed off or clipped            | Middle content took the space             | `min-w-0` on the middle, `shrink-0` on the action                                       |
| Badge wraps to two lines                         | Badge allowed to shrink                   | `whitespace-nowrap shrink-0`, then decide what yields                                   |
| Long word broken mid-word in a heading           | `word-break: break-all` (`break-all`)     | `overflow-wrap: anywhere` breaks only when needed                                       |
| Last row cut mid-glyph                           | Fixed height with `overflow: hidden`      | Scroll affordance or fade, confirm the overflow is intended                             |
| Truncated text with no way to read it            | Ellipsis alone                            | `title` or tooltip, and the full value in a detail view                                 |
| "1 members"                                      | Hard-coded plural                         | `@nuxtjs/i18n` plural messages where installed, otherwise `Intl.PluralRules`            |
| `1284`, `NaN`, `undefined`                       | Raw number                                | `Intl.NumberFormat` with the user's locale, guard null                                  |
| Digits jitter, columns misalign                  | Proportional figures                      | `font-variant-numeric: tabular-nums`, `tabular-nums`                                    |
| Broken-image icon                                | No error handler                          | Image error event swaps to initials, `object-fit: cover`                                |
| Raw `<b>` or `&amp;`                             | Wrong escaping layer                      | Default text interpolation, never `v-html` or `{@html}` on user data without sanitising |
| Hover-only action on touch                       | Visibility tied to `:hover`               | Always visible on coarse pointers                                                       |
| Jank on 1,000 rows                               | Every row in the DOM                      | Virtualise or paginate, and say which                                                   |

## SwiftUI

### SwiftUI harness

Add one `#Preview` per fixture and environment, with fixtures under `#if DEBUG` or in the target's development assets so release builds exclude them.
Put the logic that turns data into text (initials, plurals, formatting, fallbacks) in a type covered by Swift Testing (`import Testing`) with the worst-case fixtures.
For headless images of a layout, `ImageRenderer` can render a view at a fixed width inside a test.

- Width: `.frame(width: 320)`, the real container or popover width, and the widest window.
- Text size on iOS: `.environment(\.dynamicTypeSize, .accessibility5)`.
- macOS has no system-wide Dynamic Type, so lean on long localized strings and the smallest window or `MenuBarExtra` width instead.
- RTL: `.environment(\.layoutDirection, .rightToLeft)`.
- Locale: `.environment(\.locale, Locale(identifier: "de"))` and `el`.
- Dark mode: `.preferredColorScheme(.dark)`.

Hand SwiftUI code review to `swiftui-pro` and test structure to `swift-testing-pro`.

### SwiftUI failure signatures

| What you see                                      | Cause                                         | Fix                                                                                                             |
| ------------------------------------------------- | --------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Text silently truncated to one line               | Default line limit in a tight `HStack`        | Allow wrapping (`.fixedSize(horizontal: false, vertical: true)`), set `layoutPriority` on the text that matters |
| Clipped text at accessibility sizes               | Fixed `.frame(height:)`                       | Remove the height, use `@ScaledMetric` for spacing                                                              |
| `HStack` cannot fit at accessibility sizes        | Horizontal layout only                        | `ViewThatFits`, or switch to `VStack` when `dynamicTypeSize.isAccessibilitySize`                                |
| Popover or menu bar window clips content          | Fixed window or frame width                   | Test the longest localized string, let height grow                                                              |
| "1 members"                                       | Hard-coded plural                             | String Catalog plural variants, or `^[\(count) member](inflect: true)`                                          |
| `Optional("Jo")` or `nil` on screen               | Interpolating an optional                     | Unwrap and omit the line                                                                                        |
| `1284` or too many decimals                       | Raw interpolation                             | `Text(value, format: .number)` or `.formatted()`                                                                |
| Digits jitter                                     | Proportional figures                          | `.monospacedDigit()`                                                                                            |
| Empty space or spinner forever for a failed image | `AsyncImage` failure phase ignored            | Handle `.failure` with the initials fallback                                                                    |
| Distorted image                                   | Missing aspect handling                       | `.resizable().scaledToFill()` with `.clipped()` in a fixed frame                                                |
| Chevron or padding on the wrong side in RTL       | `.padding(.left)` style edges or fixed images | `.leading` and `.trailing`, `.flipsForRightToLeftLayoutDirection(true)` on directional images                   |
| Jank on 1,000 rows                                | `VStack` in a `ScrollView`                    | `List` or `LazyVStack`                                                                                          |
