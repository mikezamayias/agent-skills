---
name: app-screenshots
description: >-
  Runs the App Store and Play Store screenshot pipeline for a Flutter, Swift or Kotlin app. Covers compliance, capture, framing and locales. Use when preparing submission-ready store screenshots or framing captures, deferring to asc-* skills.
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

1. CWD must be a project root: Flutter (`pubspec.yaml`), native Apple (`project.yml`, `*.xcodeproj` or `Package.swift`) or native Android (`settings.gradle.kts` with `gradlew`).
2. **Mobile-mcp must be connected** for capture, or the project must have its own capture path (see "Native Swift and Kotlin projects").
   If neither exists, skip to the framing-only path (skill prompts the human to confirm).

## Phases

| Phase | What                                                                                           | Tooling                                                                         |
| ----- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 0     | **Compliance pre-flight** — block capture if red items remain                                  | `launch-readiness --tier 1`, App Store Connect ASO and submission-health checks |
| 1     | Production release build, signed                                                               | Xcode archive, signing, and build upload tooling (for example the `asc` CLI)    |
| 2     | **Capture** via mobile-mcp on an iPhone simulator + Pixel 8 Pro AVD, or the native paths below | mobile-mcp tools, `xcrun simctl`, `adb`, or the project's render tests          |
| 3     | **Frame** via Koubou (pinned to 0.20.0)                                                        | Koubou                                                                          |
| 4     | **Locale fan-out**                                                                             | App Store Connect metadata and subscription localization                        |
| 5     | Pre-submit final gate                                                                          | App Store Connect submission check                                              |
| 6     | Upload to App Store Connect / Play Console                                                     | `asc` CLI screenshot upload, Play Console listing upload                        |

## Per-app spec input

The skill expects to find the app's screen sequence + captions at one of these paths (project-managed):

```text
store_assets/
├── README.md                              # documents intent + sequence
└── templates/screenshot_text.json         # captions per locale (en, es, de, …)
```

If neither exists, the skill prompts the human to draft a 6-screen sequence + caption matrix before going further. Do not invent the sequence — reviewers reject screenshots that don't match the app's actual UX.
Draft and review captions with [references/copy-and-design.md](references/copy-and-design.md) before capture, so each capture is chosen to prove its headline.
Before drafting captions, write the one-sentence value prop and the one deck-level outcome described in that reference.
Keep Apple-designated recognitions such as Editor's Choice or App of the Day, and unverifiable awards, out of the screenshots.

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
Submitting Duo screenshots in App Store Connect adds a badge to the product page.
Apple's developer pages say it shows the app is "optimized for iPhone Duo", and Apple's October 22, 2026 newsroom post calls it the "Made for iPhone Duo" badge.
Apple's pages tie the badge to the screenshot submission and describe the iOS 27.1 SDK build as what makes an app optimized, but they do not say what happens to the badge without that build.
One secondary report (9to5Mac, October 5) says the Xcode 27.1 build triggers it, which conflicts with Apple's current pages.
Do both steps, and check the live product page on a device after approval.
Capture each display on the iPhone Duo simulator at its exact size, never by stretching another iPhone capture.
Koubou 0.20.0, the version `asc` pins, has no Duo frame (`asc screenshots list-frame-devices` lists none), so Duo framing is an open step: log it as `Stuck` and ask the human rather than improvising a frame.
Duo deck design rules are in [references/copy-and-design.md](references/copy-and-design.md).
Optional for the human, not for the store deck: one author composites app captures into an image-model render of a hand holding a Duo for social and press visuals (Tobia Donadon, product page read 2026-10-20, one sentence, unverified, untested here).
Apple's store screenshots still use the exact simulator captures from the step above.
Never use a generated device render as a store screenshot.
Android target: 1080×1920 portrait (9:16, Play Store phone).
Play rejects screenshots whose long side is more than twice the short side, so raw 20:9 captures such as 1080×2400 must be framed to 9:16.
Play accepts up to 8 phone screenshots as JPEG or 24-bit PNG without alpha, and promotion eligibility needs at least 4 at 1080 px or more.

## Production-environment hard requirements

Apple/Google reject screenshots that show debug overlays or staging data. Verify all of:

- [ ] No debug banner (Flutter: `MaterialApp.debugShowCheckedModeBanner = false` or release mode forces it off. Native: no debug-only overlay, banner or `#if DEBUG` UI in the captured build)
- [ ] No performance overlay, no debug paint, no leak tracker
- [ ] Status bar locked to a clean state via `xcrun simctl status_bar booted override --time "9:41" --batteryLevel 100 --cellularBars 4 --wifiBars 3 --cellularMode active --dataNetwork wifi`
- [ ] Test account looks realistic (no "test test test", no `lorem ipsum`)
- [ ] No PII (real names, real emails, real bank balances)
- [ ] Light mode by default; add a dark mode pass when the listing calls for it
- [ ] More than half of the screenshots for each supported device show the app in use (Guideline 2.3.3). With 3 screenshots per device, 2 must show the app in use on that device, and with 4, 3 must. Title art, a login page, and a splash screen do not count.
      Count a slide as showing the app in use only if it contains a real or realistic screen of the running app.
      A mascot, photo, orbiting-avatar graphic, floating money chips, a lone notification or a placeholder grey-row mock does not count.
      Apple's 2.3.3 text as fetched allows overlays and text, so the test is the presence of a real screen and not the absence of decoration.
      Before `asc screenshots upload`, write a slide-by-slide table (slide, headline, real screen yes or no), and do the same for decks designed by a third party.
      Example from one agency-deck post (October 2026, image reading, inference, no review outcome known): of four agency decks of six slides, one had no real screen by that reading and the others had 4 or 5.

## Native Swift and Kotlin projects

Everything above applies.
Only the build and capture steps differ.
Pick the capture path the project already has before inventing one.

1. Project render tests.
   Some native projects draw store screenshots from their own views inside a test target, which needs no running app and no device.
   Look for `scripts/render-*.sh`, a `StoreScreenshotTests` file, or an environment switch that turns render tests on.
   Run the script and read its output folder.
   These renders are the app's real screens, so they count as "app in use" under Guideline 2.3.3.
2. Apple simulator capture, when no render path exists:

   ```bash
   xcodegen generate                      # only when project.yml exists
   xcrun simctl list devices available    # pick the simulator that produces the required size
   xcodebuild build -project <P>.xcodeproj -scheme <App> -configuration Release \
     -destination 'platform=iOS Simulator,name=<simulator>' -derivedDataPath build/shots-dd
   xcrun simctl boot "<simulator>"
   xcrun simctl install booted build/shots-dd/Build/Products/Release-iphonesimulator/<App>.app
   xcrun simctl status_bar booted override --time "9:41" --batteryLevel 100 --cellularBars 4 --wifiBars 3 --cellularMode active --dataNetwork wifi
   xcrun simctl launch booted <bundle id>
   xcrun simctl io booted screenshot --type=png store_assets/screenshots/raw/en-US/01_home.png
   ```

   Drive the app to each screen with launch arguments, deep links (`xcrun simctl openurl booted <url>`) or a UI test.
   Watch captures use a paired watchOS simulator the same way.
   A StoreKit configuration file only applies to Xcode runs, so for paywall shots use a UI test or run from Xcode.

3. Android emulator capture:

   ```bash
   ./gradlew :app:installRelease          # or the release-like build type the project defines
   adb exec-out screencap -p > store_assets/screenshots/raw/en-US/01_home.png
   ```

   Lock the status bar with demo mode: `adb shell settings put global sysui_demo_allowed 1`, then `adb shell am broadcast -a com.android.systemui.demo -e command clock -e hhmm 0941`.
   Use an AVD that yields 1080×1920 or frame the capture to 9:16 as above.

4. Mac app.
   A Mac app distributed outside the App Store has no App Store screenshot slot.
   Capture it for the landing page and cask page with a render test, or with `screencap`-style window capture (`screencapture -l <window id> file.png`), and hand the files to `app-landing-page`.
   Mac App Store sizes apply only if the app ships there.
5. Devices: `xcrun devicectl list devices` lists connected devices, but `simctl` and the emulator give the exact sizes the stores require.

Strip alpha and check sizes after any path: `sips -g pixelWidth -g pixelHeight -g hasAlpha <file>`.
The release build for Phase 1 is `xcodebuild archive` (Apple) or `./gradlew :app:bundleRelease` (Android), and the uploaded store build comes from `asc-xcode-build`.

## App previews (optional)

Make two cuts from one recording.

- Store cut: a screen capture of the app itself.
  Guideline 2.3.4 says "previews may only use video screen captures of the app itself" and allows narration and video or textual overlays.
  Apple does not name device frames in 2.3.4 or on its app previews page, so keeping frames out of the store cut is our own rule.
  A developer forum thread quotes a 2.3.4 rejection that cites device frames.
- Social cut: framed device on a backdrop, for social posts and the landing page.
  Framing here is our own rule, and this cut is never uploaded to a store.
- Apple spec: 15 to 30 seconds, up to 30 fps, `.mov`, `.m4v` or `.mp4` for H.264 or `.mov` for ProRes 422 HQ, 500 MB maximum, up to three previews per device size and language.
  Accepted resolution is 886×1920 portrait or 1920×886 landscape for iPhone Duo and the Dynamic Island and Face ID classes, 1080×1920 for Home Button (large) and 750×1334 for Home Button (medium).
  Apple says to use the accepted resolution, not the device resolution.
- Apple's app previews page says "Don't include specific prices, as pricing and currencies vary across regions."
  It also says that if you display features only available through in-app purchase, or your app uses a subscription model or requires login, "you must disclose this", in the footage or the end frame.
  Previews play muted by default, so carry the meaning in on-screen text.
- Record with `xcrun simctl io booted recordVideo --codec=h264` (Android: `adb shell screenrecord`), because `recordVideo` defaults to HEVC and accepts `--codec=h264`.
  Then scale the file to the accepted resolution at 30 fps or less.
  Neither Apple page says whether a preview with no audio track uploads, so test the upload.
- Google Play: one YouTube video, ads disabled, no maximum length, and only the first 30 seconds autoplay.
  The video must be public or unlisted, embeddable and not age-restricted.

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
- <https://developer.apple.com/app-store/review/guidelines/>
- <https://developer.apple.com/help/app-store-connect/reference/app-preview-specifications/>
- <https://developer.apple.com/app-store/app-previews/>
- <https://developer.apple.com/forums/thread/656342>
- <https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots>
- <https://support.google.com/googleplay/android-developer/answer/9866151>
- <https://github.com/rudrankriyam/App-Store-Connect-CLI>
- <https://github.com/bitomule/koubou>
