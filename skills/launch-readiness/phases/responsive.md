# Phase: Responsive

## Tier

T2 — Quality Gate

## Inputs

- Stack profile (UI framework)
- Overlay checks (project-specific responsive requirements)
- Scope: file list or "all"

## Checks

### 1. Hardcoded Widths

- Scan for `width:` constraints with literal values > 200 logical pixels
- Exclude: icon sizes, tap targets, design system constants
- **Critical if**: Hardcoded width > 300 that would overflow on 375pt screen (iPhone SE)
- **High if**: Hardcoded width 200-300 in a layout that doesn't scroll horizontally
- **Method**: Grep for `width:` with numeric literals, check context

### 2. Horizontal Overflow Patterns

- Scan for `Row` widgets without `Expanded`, `Flexible`, or `SingleChildScrollView` wrapping
- Check for multiple `Text` widgets in a `Row` where content could exceed screen width
- **Critical if**: Visible content clipped/invisible on 375pt width
- **Medium if**: Row without flex children where overflow is theoretically possible
- **Method**: Read widget files, check Row children for flex wrappers

### 3. Text Scaling Tolerance

- Check if the app handles text scaling from `MediaQuery.textScalerOf(context)` up to 2.0x (`textScaleFactorOf` is deprecated)
- Scan for fixed-height containers wrapping `Text` widgets
- **Medium if**: Fixed-height container around text that would clip at 2.0x scale
- **Method**: Check for fixed height + Text combinations

### 4. Missing Breakpoint Usage

- Scan layout pages for responsive patterns
- **Medium if**: Full-screen layout with no breakpoint/MediaQuery adaptation
- Stack-aware: check for `ShadBreakpoints` (shadcn_ui), `LayoutBuilder` (Material), `MediaQuery` (generic)
- **Method**: Read page files, check for responsive pattern usage

### 5. iPhone Duo Compatibility

- Read the App Store Connect and developer account banners for an iPhone Duo notice and record its exact text.
  The banner claim is the author's own (Tobia Donadon, October 2026) and unverified.
- Check the build SDK.
  An Xcode 26 build runs on iPhone Duo in a compatibility area, so flag it as Medium when the product page promises Duo support.
  The SDK fact comes from `swiftui-pro/references/resizability.md`.
- For Flutter and React Native, check that layouts branch on available width and not on device idiom or rotation.
  Flutter `LayoutBuilder` and `MediaQuery.sizeOf` apply.
  Folding changes the available size without relaunching the app.
  This line is inference.
- For Expo apps, audit each screen for the side rail inset.
  Expo's SDK 58 post (October 23, 2026) says the rail "needs either an 84pt left or right inset" (<https://expo.dev/blog/supporting-iphone-duo>, read 2026-10-29).
  The same post says "The work that remains is auditing your screens and applying additional safe areas, and making decisions for your app's internal layout."
  It names `Stack` and `NativeTabs` as handled and says `contentInsetAdjustmentBehavior="automatic"` "will handle this alone in a future React Native patch".
  Custom JavaScript headers and tab bars get only "minimal compat behaviour for custom JS `<Stack>` header and `<TabList>` components", which Expo says render "not following any iPhone Duo conventions", so audit those screens too.
  Read the inset from the safe-area API and never hardcode 84.
  One creator's guide says Expo already adapts and the fold needs no detection.
  That holds for navigation and the fold, and the guide is incomplete for safe areas.
- Check the Duo store steps when the product page promises Duo support.
  Apple lists three separate actions: build with the iOS 27.1 SDK, submit iPhone Duo screenshots (they trigger the product page badge), and submit a featuring nomination in App Store Connect, where "In the Helpful Details section, you can specify that your app is optimized for iPhone Duo, including support for all device poses" (Apple's exact words, confirmed in `prep.html` on 2026-10-23).
  Apple's October 22, 2026 newsroom post says editorial collections for iPhone Duo apps and games go live on October 23 and does not say how apps are chosen or whether the badge changes search rank.
  Do not promise store placement.
  `asc nominations create` exists in `asc` 5.16.0 and its help text has no Duo field, so the Duo statement probably goes in the description or notes (inference, help text read and not run).
  Apple's nomination help places "Helpful Details" under Additional Information and says the type and related apps cannot change after submission, so save the nomination as a draft first and check the Duo statement in App Store Connect before submitting.
  Apple recommends at least 3 weeks of lead time for a nomination (help page read 2026-10-24).
- **Method**: grep for orientation locks and fixed idiom checks, then ask the human to test both displays in the Duo simulator.

### 6. Touch Target Sizing

- Scan interactive elements for explicit size constraints
- **High if**: Touch target < 44x44 on any viewport size (48x48 dp on Android)
- Note: overlaps with Accessibility phase but here we check across breakpoints
- **Method**: Check interactive element sizes

### 7. Scrollability

- Check screens with multiple sections for scroll wrapper
- **High if**: Screen content likely exceeds viewport height on small devices without scroll
- **Method**: Read page files, check for ScrollView or equivalent wrapper

### 8. Overlay Checks

- Read the matched overlay's Responsive section
- Execute each additional check

## Native Swift and Kotlin projects

For native Apple and Android projects the Flutter methods above map as follows.
Full detail is in [native-projects.md](../references/native-projects.md).

SwiftUI: `ViewThatFits`, size classes, Dynamic Type sizes, and the smallest and largest watch case sizes.
Compose: `WindowSizeClass`, `BoxWithConstraints` and `fontScale` 2.0.
Mac: minimum window size and full screen.

## Severity Rules Summary

| Check                        | Critical | High | Medium | Low |
| ---------------------------- | -------- | ---- | ------ | --- |
| Overflow on 375pt            | X        |      |        |     |
| Hardcoded width > 300        | X        |      |        |     |
| Hardcoded width 200-300      |          | X    |        |     |
| No scroll on long content    |          | X    |        |     |
| Touch target < 44pt          |          | X    |        |     |
| Text scaling clip            |          |      | X      |     |
| No breakpoint usage          |          |      | X      |     |
| Suboptimal layout adaptation |          |      |        | X   |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: yes/no | fix_action: {description}
```
