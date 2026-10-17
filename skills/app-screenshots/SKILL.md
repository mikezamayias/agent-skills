---
name: app-screenshots
description: >-
  End-to-end App Store and Play Store screenshot pipeline for a Flutter app: compliance, capture, framing and locales. Use when preparing submission-ready store screenshots, for example "take store screenshots" or "frame the captures". Defers to the asc-* skills wherever they already cover a step.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
metadata:
  docs-verified: "2026-09-28"
  openclaw:
    emoji: 📸
    os:
      - darwin
    requires:
      bins:
        - flutter
        - xcrun
        - asc
    install:
      - id: asc-cli
        kind: manual
        label: Install asc CLI
        url: https://github.com/rudrankriyam/App-Store-Connect-CLI
---

# app-screenshots

Single skill for the **screenshot pipeline** — App Store + Play Store, release flavor only, production environment. The pipeline reuses the `asc` App Store Connect CLI and any installed App Store Connect skills; this skill is the orchestrator on top.

## When to invoke

User says: "take store screenshots", "generate App Store shots for X", "do the screenshot run", "ship screenshots for tomorrow's submission", "frame the captures I just did".

## Activation rules

1. CWD must be a Flutter project root (has `pubspec.yaml`).
2. **Mobile-mcp must be connected** for capture; if it's not, skip to the framing-only path (skill prompts the human to confirm).

## Phases

| Phase | What                                                                | Tooling                                                                         |
| ----- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 0     | **Compliance pre-flight** — block capture if red items remain       | `launch-readiness --tier 1`, App Store Connect ASO and submission-health checks |
| 1     | Production release build, signed                                    | Xcode archive, signing, and build upload tooling (for example the `asc` CLI)    |
| 2     | **Capture** via mobile-mcp on an iPhone simulator + Pixel 8 Pro AVD | (mobile-mcp tools directly)                                                     |
| 3     | **Frame** via Koubou (pinned to 0.20.0)                             | Koubou                                                                          |
| 4     | **Locale fan-out**                                                  | App Store Connect metadata and subscription localization                        |
| 5     | Pre-submit final gate                                               | App Store Connect submission check                                              |
| 6     | Upload to App Store Connect / Play Console                          | `asc` CLI screenshot upload, Play Console listing upload                        |

## Per-app spec input

The skill expects to find the app's screen sequence + captions at one of these paths (project-managed):

```text
store_assets/
├── README.md                              # documents intent + sequence
└── templates/screenshot_text.json         # captions per locale (en, es, de, …)
```

If neither exists, the skill prompts the human to draft a 6-screen sequence + caption matrix before going further. Do not invent the sequence — reviewers reject screenshots that don't match the app's actual UX.
Draft and review captions with [references/copy-and-design.md](references/copy-and-design.md) before capture, so each capture is chosen to prove its headline.

Locales: read them from `store_assets/templates/screenshot_text.json`.
When the app has an in-app language switch, use it for locale fan-out instead of changing the device language, because it is faster.
If the project does not declare its locales, ask the human.

## Output paths

```text
store_assets/screenshots/
├── raw/<locale>/                # native sim/emulator capture
│   ├── 01_<screen-id>.png
│   ├── 02_…
│   └── …
└── framed/<locale>/             # Koubou-framed marketing version
    ├── 01_<screen-id>.png
    ├── 02_…
    └── …
```

iOS target: the required iPhone slot, which Apple now labels "iPhone with Dynamic Island (medium display)", at 1206×2622 or 1179×2556 portrait.
Apple accepts either size and does not tie either one to a device.
Capture at the chosen size on a simulator that produces it, never by resizing a capture from another size.
The slot labeled "iPhone with Dynamic Island (large display)" (1260×2736, 1290×2796 or 1320×2868) has no requirement line.
Apple says that when the interface is consistent across sizes, only the highest required resolution is needed and App Store Connect scales it down.
Apps that run on iPad also need 13" iPad screenshots (2064×2752 or 2048×2732).
App Store Connect accepts 1 to 10 screenshots per device size and locale, as PNG or JPEG without alpha.

iPhone Duo: outer display 1398×2034 or 2034×1398, inner display 2007×2853 or 2853×2007.
Apple's screenshot specifications require Duo screenshots starting April 2027 for apps built with the iOS 27.1 SDK or later, and the October 5, 2026 developer news says any app submitted from April 2027.
Submitting Duo screenshots adds an "optimized for iPhone Duo" badge to the product page.
Capture each display on the iPhone Duo simulator at its exact size, never by stretching another iPhone capture.
Koubou 0.20.0, the version `asc` pins, has no Duo frame (`asc screenshots list-frame-devices` lists none), so Duo framing is an open step: log it as `Stuck` and ask the human rather than improvising a frame.
Duo deck design rules are in [references/copy-and-design.md](references/copy-and-design.md).
Android target: 1080×1920 portrait (9:16, Play Store phone).
Play rejects screenshots whose long side is more than twice the short side, so raw 20:9 captures such as 1080×2400 must be framed to 9:16.
Play accepts up to 8 phone screenshots as JPEG or 24-bit PNG without alpha, and promotion eligibility needs at least 4 at 1080 px or more.

## Production-environment hard requirements

Apple/Google reject screenshots that show debug overlays or staging data. Verify all of:

- [ ] No debug banner (`MaterialApp.debugShowCheckedModeBanner = false` or release mode forces it off)
- [ ] No performance overlay, no debug paint, no leak tracker
- [ ] Status bar locked to a clean state via `xcrun simctl status_bar booted override --time "9:41" --batteryLevel 100 --cellularBars 4 --wifiBars 3 --cellularMode active --dataNetwork wifi`
- [ ] Test account looks realistic (no "test test test", no `lorem ipsum`)
- [ ] No PII (real names, real emails, real bank balances)
- [ ] Light mode by default; add a dark mode pass when the listing calls for it
- [ ] More than half of the screenshots for each supported device show the app in use (Guideline 2.3.3). With 3 screenshots per device, 2 must show the app in use on that device, and with 4, 3 must. Title art, a login page, and a splash screen do not count.

## Tooling notes

- Do not write a custom Python framing pipeline. Frame with Koubou 0.20.0, the version the `asc` CLI pins.
- Reference other skills by name rather than inlining their work.
- If a locale cannot be captured or framed correctly, log it as `Stuck` in `store_assets/SCREENSHOTS_LOG.md` and ask the human.

## Done state

- `store_assets/screenshots/{raw,framed}/<locale>/` populated for every required locale
- Dimensions verified (`sips -g pixelWidth -g pixelHeight <file>`)
- `store_assets/SCREENSHOTS_LOG.md` written with what shipped + what was skipped
- One line appended to `store_assets/screenshots-runs-log.md`:

  ```text
  YYYY-MM-DD HH:MM — <project> — <locale>×N shots
  ```

## Related skills

- `launch-readiness` — Phase 0 dep
- `app-graphics` — adjacent skill for icons, banners and App Store creative assets (product page header and search results). Don't generate them here. Without a search result creative asset, the App Store shows in-app events, app previews and screenshots in search results.
- `app-landing-page` — adjacent skill, uses screenshots from this one

## Sources

- <https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications>
- <https://developer.apple.com/news/?id=kkphp5qo>
- <https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots>
- <https://support.google.com/googleplay/android-developer/answer/9866151>
- <https://github.com/rudrankriyam/App-Store-Connect-CLI>
- <https://github.com/bitomule/koubou>
