---
name: mobile-ui-reference
description: >-
  Design or restyle a Flutter screen from 5 to 8 shipped references, a written spec, Flutter code first and Figma last. Use for onboarding, paywall, settings, empty state or permission screens instead of model-generated UI. Also use when a Flutter screen looks Material on iOS, or when dropping running-app shots into Figma.
metadata:
  docs-verified: "2026-09-28"
---

# Mobile UI reference

Flutter-first, code-first. Gather shipped screens, write a spec, build the UI, then park screenshots in Figma as a **reference board**. Figma is not the source of truth until a human must approve mocks before code.

Do **not** start with ui-ux-pro-max `--design-system` (landing-page palettes). Do not prompt "generate a paywall." Split turns: research note, then implement.

## 0. Name the job

One sentence. Feature + job to be done. Example: "Hard-paywall after onboarding quiz, annual default, skip control visible."

Platform default: iPhone-first Flutter (Cupertino + HIG) unless the product is branded (Forui / own tokens) or Android-first (Material 3).

## 1. Gather 5–8 shipped references

Research, not generate. Stop at 8. Critique exists **before** any Dart.

**Preferred (paid Mobbin MCP, Pro/Team/Enterprise):** `https://api.mobbin.com/mcp`.
Tools: `search_screens`, `search_flows`, `search_sections` (web sections).
Empty tool errors usually mean unpaid, so fall back and don't invent patterns.

Mix:

- 2 named apps in the same category
- 2 category hits ("iOS onboarding productivity")
- 1 adjacent category (so you do not clone one brand)
- 1 anti-example you will **not** copy

Stay in research mode: "Show 6 iOS onboarding flows that ask for notification permission after value, not before. Describe structure, do not generate UI."

**Other reference sources** (checked 2026-10-13, prices from live pages):

| Source        | Covers                                                                          | Agent access                                                                                                                                                            | Cost                                            | Use for                                                                           |
| ------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------- |
| Refero        | Web and iOS screens, flows, curated styles                                      | MCP at `https://api.refero.design/mcp`, tools `refero_search_screens`, `refero_search_flows`, `refero_search_app`, `refero_search_styles`, 8,000 calls a month per seat | Pro, Team or Lifetime plan, prices not readable | Second opinion to Mobbin, and `refero_search_styles` for a landing page direction |
| Gummble       | iOS, Android and web, vendor claims 300,000+ screens                            | Read-only MCP on Browse and up, API on Team                                                                                                                             | Browse $9.99/mo, Pro $14.99/mo                  | Cheapest MCP source that covers Android                                           |
| ScreensDesign | 2,805+ top-chart iOS apps with videos, paywalls, onboarding and revenue signals | MCP and API, licensed for interactive research only                                                                                                                     | Not readable                                    | Paywall and onboarding research tied to revenue                                   |
| Page Flows    | Recorded flows for iOS, Android, web and email                                  | None                                                                                                                                                                    | $8.25/mo billed yearly, $2.95 3-day trial       | Whole multi-step flows, watched by the human                                      |

All four terms forbid bulk download or building a dataset, so keep each pull to the 5 to 8 references this step needs.

**No Mobbin:** screenshot 3–5 apps on a device. Save under `design-refs/<feature>/`. Paywalls: <https://toomanypaywalls.com> for **pattern labels**, not chrome.

### 1b. Concept, then three directions

References show structure. They do not give the app a face.
Before any screen, name one real-world object or place the app _is_, such as a running app as an athletics track, a sleep app as a village going to sleep, or a plant app as paper cut-outs.
Let that concept set type, palette, illustration style and motion.
"Clean", "minimal", "modern" and "premium" are not directions.
Sketch the main screen three ways from the concept, pick one with the human, then build every other screen from the chosen one.
The method is Tobia Donadon's free "Stop Making your Apps Look Like AI Slop" article (October 2026). His paid skill packages it.

## 2. Critique

| Lens          | What to write                                                             |
| ------------- | ------------------------------------------------------------------------- |
| Hierarchy     | 1st / 2nd / 3rd glance                                                    |
| Type          | Size, weight, SF-style vs custom. HIG: title / body / footnote            |
| Layout        | Safe area, bottom CTA pinned or inline, sheet vs full screen              |
| Radius        | Superellipse vs circular vs sharp                                         |
| Motion        | None / implicit Flutter / Rive state machine                              |
| Copy          | CTA verb, price presentation, trial framing, word count per screen        |
| Escape        | Skip, X, "not now", or none (hard wall)                                   |
| Dark pattern? | Countdown, decoy weekly, default-off reminder, no close — **do not copy** |

Fail-closed iPhone-first checks:

- Type: HIG sizes (~34pt large title, 17pt body, 13pt footnote). Fail: Roboto / Material 3 defaults on iOS
- Shape: superellipse, `cornerSmoothing` ≥ 0.6. Fail: `BorderRadius.circular` everywhere
- Press: opacity, no Material ink. Fail: splash/ripple
- Color: one seed → shade ramp. Fail: unrelated accent per screen
- Touch: 44pt min, 8pt+ gap
- Safe area: home indicator, notch, keyboard
- Compact chrome: concentric inner shapes; no empty "forehead"
- A11y: 4.5:1 light **and** dark, label not icon-only, Reduce Motion via `MediaQuery.disableAnimationsOf(context)`
- Motion: Flutter springs for layout; Rive only for a state-machine/character

Paywall/onboarding: warm ask after a **win**. Soft = visible skip. Hard = after commitment. **No close button is a dark pattern.** Trial: timeline before price. Permissions after value. Duolingo's 19–38 quiz screens are a habit game, not a utility template.

IAP wiring belongs in [Flutter paywall and review timing](../flutter-paywall-and-review-timing/SKILL.md).

Live Activity / Dynamic Island (only if the feature is compact chrome): concentric margins, compact snug to the sensor, expanded hugs the sensor, minimal still shows data. Flutter cannot host the island.

## 3. Apply in Flutter first

UI only. Fake data. No RevenueCat, no repository, no `FutureBuilder`.

1. Prefer `CupertinoApp` / `CupertinoPageScaffold` / `CupertinoListSection` / `CupertinoButton`.
   Import `package:flutter/widgets.dart` + `package:cupertino_ui/cupertino_ui.dart` (Flutter 3.47+, add with `flutter pub add cupertino_ui`).
   Material and Cupertino now ship as standalone `material_ui` / `cupertino_ui` packages, and the `package:flutter/material.dart` / `cupertino.dart` imports are slated for deprecation, so stop treating `material.dart` as the framework.
   If the app is already `MaterialApp`, still do not add ink splash on new screens.
2. Superellipse, not `BorderRadius.circular`:

```dart
import 'package:figma_squircle/figma_squircle.dart';

decoration: ShapeDecoration(
  color: const Color(0xFFFFFFFF),
  shape: SmoothRectangleBorder(
    borderRadius: SmoothBorderRadius(
      cornerRadius: 20,
      cornerSmoothing: 1,
    ),
  ),
)
```

Clip children with `ClipSmoothRect`.

1. Kill Material splash. No `InkWell` / default `ElevatedButton` splash. Use a `GestureDetector` + opacity dip (<150ms). Disabled = opacity ~0.4, not a grey box. Hit area ≥ 44×44. `SafeArea` on headers, tab bars, bottom CTAs.
2. Rive vs Flutter:

| Use Rive                                         | Use Flutter                                                |
| ------------------------------------------------ | ---------------------------------------------------------- |
| Character, illustrated scene, state-machine icon | Opacity, route transition, chevron rotate, keyboard insets |
| Designer owns `.riv`                             | `AnimationController` would be <30 lines                   |

Rive files play through the official `rive` package (0.14.11 on pub.dev, checked 2026-10-13).
Lottie files play through `lottie` (3.6.1), a third-party package by xvrh, not an official Airbnb release.
Use Lottie for a one-shot or looping illustration with no inputs, and Rive when the animation reacts to app state through a state machine.
Rive's free plan exports with a splash screen, so a shipped `.riv` needs a paid seat.
Lottielab exports Lottie JSON only on a paid plan, and Jitter's free tier exports at 720p 30fps with a watermark.

Never Rive a page route. `liquid_glass_renderer` is 0.2.0-dev, Impeller-only, 16-shape cap — not a layout system. Never on Web/Skia.

## 4. Drop running UI into Figma

1. iPhone simulator. Capture UI-only, plus one with chrome if island/home-indicator context matters.
2. Figma page `Refs / <feature>`. Place PNGs as reference frames. Do **not** rebuild from components first.
3. Slice only repeating pieces (row, chip, CTA) if a second screen will reuse them.
4. Do not use web-only Figma generate-design capture. Do not round-trip through Figma SwiftUI. Do not run Specs Classic (deprecated).

If later you want production Figma components linked to Flutter, that is a different installed Figma skill.

## 5. Pre-delivery

- No emoji as icons
- Contrast ≥ 4.5:1 light and dark
- List content not hidden behind the CTA
- Reduced motion: skip Rive / glass stretch
- Dynamic Type: titles wrap, CTAs don't clip
- Pressed state does not shift layout bounds

Render the built screens on the simulator at device resolution, then run a separate critic pass that fails any of these AI tells:

- Purple or blue gradient hero card
- Emoji standing in for illustration or icons
- Repeated identical cards with uniform padding
- Plain avatar circle and a generic title such as "My Savings Goals"
- Gradients with no job
- Body-text sentences where a concrete number or object would do ("€49 to go", "€49 is three takeaways")
- A screen that is tidy but could belong to any app

Give every screen a word budget before writing copy.
No em dashes or AI stock phrases ("Unlock your potential", "Seamless. Effortless. Powerful.") in UI strings.

Paste the spec + 2–3 reference links **before** asking a model to write widgets.

## Sources

- <https://mobbin.com/mcp>
- <https://mobbin.com/blog/how-to-use-mobbin-mcp>
- <https://toomanypaywalls.com>
- <https://docs.flutter.dev/ui/widgets/cupertino>
- <https://pub.dev/packages/figma_squircle>
- <https://developer.apple.com/videos/play/wwdc2023/10194/>
- <https://docs.flutter.dev/release/breaking-changes/material-ui-and-cupertino-ui>
- <https://pub.dev/packages/liquid_glass_renderer>
- <https://developer.apple.com/design/human-interface-guidelines/typography>
- <https://developer.apple.com/design/human-interface-guidelines/accessibility>
- <https://api.flutter.dev/flutter/widgets/MediaQuery/disableAnimationsOf.html>
- <https://x.com/i/article/2106430529113301163> (Tobia Donadon, concept-first method)
