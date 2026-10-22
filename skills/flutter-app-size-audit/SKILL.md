---
name: flutter-app-size-audit
description: >-
  Cuts Flutter app install size by attacking build defaults, asset formats, and shrinking flags, and measures the result. Use when install conversion is dropping, when reviewers cite size, or before any major release.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter App Size Audit

Many app size problems come from build defaults you never questioned, not from your assets.
Check all five layers and measure each change with `--analyze-size`.

## Why iOS download size matters

- iOS can ask the user to confirm a download over a mobile network.
  Apple's size guide says the App Store "limits the size of the apps they can install over a mobile connection" and tells you to keep the app "well below the size limit", and it gives no number.
  Apple's iPhone guide shows the choices "Always Allow, Ask If Over 200 MB, or Always Ask" for Books, and two news articles from 2019 and 2020 say the App Store uses the same choices with "Ask If Over 200 MB" as the default (inference, third-party, iOS 13 era).
  Treat 200 MB as the default prompt threshold on current iOS and check it on a device before quoting it.
- The prompt can be overridden, so it is friction and not a block.
  The same articles say the prompt always appears while roaming, so a small app can still trigger one (a reply screenshot shows a 52 MB app prompting on a roaming connection).
- The number that counts is the thinned compressed download size per device variant, not the `.app`, the `.xcarchive` or the IPA.
  Apple says none of those is suitable for measuring.
- One X post claims "5-15% more installs" from getting under the threshold and that apps over 500 MB are often deferred and forgotten (single report, no study, no app named, and the 500 MB claim has no Apple source, where 500 MB is Apple's executable-size limit).
  Do not quote these numbers to a client.
  Measure your own cellular install rate before and after.
- The "30-60%" size cut this skill used to promise in its description had no source and is dropped (unverified).

Evidence: Apple pages read 2026-10-23, the Apple size guide through its page JSON.
The 200 MB default is unconfirmed on current iOS.

## The 5-step cut

1. **Split per ABI.** `flutter build apk --split-per-abi` (or use App Bundle for Play). Stops shipping arm64 + armv7 + x86_64 to every device.
   Play already delivers one ABI per device from an App Bundle, so this mainly shrinks APKs distributed outside Play.
2. **WebP instead of PNG.** Convert all bitmaps.
   Google measures lossless WebP 26% smaller than PNG and lossy WebP 25-34% smaller than JPEG at equal SSIM.
   No quality setting is universally visually lossless (`cwebp` and Android Studio default to 75), so compare each lossy result against the original, or use `-lossless` / `-near_lossless` for UI art.
   Use `cwebp` in a pre-commit hook.
3. **Keep R8 on and add resource shrinking.** Flutter release APK/AAB builds always run R8 code shrinking.
   The Flutter Gradle plugin already enables minify and resource shrinking for release builds (see the defaults below), so do not add them to `android/app/build.gradle(.kts)`.
   Check instead that nothing turns them off, such as the Gradle property `shrink=false` or an explicit `isMinifyEnabled = false`.
   R8 only touches JVM code, so add keep rules only for native Android dependencies that use reflection and ship no consumer rules.
   Pure Dart packages, such as JSON serializers, are unaffected.
   What Flutter sets by default, verified on 2026-10-21:
   - The app template's `buildTypes.release` block sets only a signing config, with no minify, resource shrinking or ProGuard line.
   - The Flutter Gradle plugin in Flutter 3.47.7 (`FlutterPlugin.kt`, read from a local install) sets `isMinifyEnabled = true`, `isShrinkResources` for apps and adds `proguard-android-optimize.txt`, `flutter_proguard_rules.pro` and the app's `proguard-rules.pro` when it exists.
   - It skips that block only when the Gradle property `shrink` is `false`.
   - `docs.flutter.dev/deployment/android` says R8 is "enabled by default when you build a release APK or AAB" and "Code shrinking is always enabled in release builds".
     It does not mention `proguard-android-optimize.txt`, so the plugin source is the evidence for that file.
   - Check the app's own `build.gradle(.kts)` and `gradle.properties` for an override before assuming these defaults.
   - Check that nothing swaps the plugin's `proguard-android-optimize.txt` for the legacy `proguard-android.txt`, such as an explicit `proguardFiles(getDefaultProguardFile("proguard-android.txt"), ...)` in a build type.
     Grab and the Android Developers Blog report that moving from the legacy file to the optimize file is what turns on R8 optimization (self-reported, one organization).
     Whether an explicit `proguardFiles` call replaces or adds to the plugin's files was not tested here, so inspect the merged result before relying on either.
     For Flutter apps with a lot of their own Kotlin or Java code, Grab's Android case study adds the practices below.
   - Treat the R8 optimizer (compat mode) and R8 full mode as separate rollouts, and verify each one on release builds before shipping.
   - Write narrow keep rules for the specific reflected classes, not broad exceptions, and require a justification and review for each new rule.
   - Score keep-rule hygiene with the R8 Configuration Analyzer.
     Grab reports that trimming rules raised its scores by 1.5 to 6.2 points and cut download size by about 3.6%.
   - Treat Grab's numbers (16%, 14% and 3.6% size cuts) as self-reported by Google and Grab, from an app with more than 10 million lines of code.
     A typical Flutter app is mostly Dart AOT code that R8 does not touch, so expect much less.
4. **Tree-shake icons.** `--tree-shake-icons` is on by default in release builds — verify it's not disabled. Custom icon fonts should be subsetted.
5. **Audit fonts and Lottie.** A single unused static weight costs roughly 150KB (Poppins Bold) to 630KB (Noto Sans Bold).
   Lottie JSONs often carry unused layers, embedded images, and more frames than needed, so re-export at 30fps with simplified paths and compare file sizes.

## Verification

```bash
flutter build apk --analyze-size --target-platform android-arm64
flutter build ios --analyze-size  # generates a report
```

`--analyze-size` needs a single Android `--target-platform`, cannot be combined with `--split-debug-info`, and on iOS measures a `.app`, not the IPA.
For shipping builds, add `--split-debug-info=<dir>` (optionally with `--obfuscate`), which Flutter's app-size guide recommends to reduce code size.

- For the iOS number users download, archive the build, export it as Ad Hoc, Development or Enterprise with "All compatible device variants" for app thinning, and read `App Thinning Size Report.txt`.
  Its compressed size per variant is the download size.
  In a script, run `xcodebuild -exportArchive` with an export options plist whose `thinning` key is `<thin-for-all-variants>`.
  The export command was read from Apple's page and not run on a Flutter archive, so it is unverified.
- For a build that is on the App Store or TestFlight, App Store Connect shows each variant's size and warns when it is over the limit for a mobile download.
  Apple says that is the most accurate source, and that a TestFlight build is larger than the App Store build.
- Compare the largest variant, which is the one a user on an older or larger device gets, and not only the smallest (inference, Apple has no sentence about the largest).

Open the size report and look for the top 5 contributors. If a single asset > 1MB, attack it first.

For Android host code and libraries, Grab's open-source App Sizer (MIT) attributes download size to teams, modules and libraries from APK, AAR and JAR input, through a Gradle plugin or a CLI.
It does not read Flutter Dart AOT size, so keep `--analyze-size` for that.
Its README warns class sizes are estimates that suit trends, not exact figures.
Evidence: README read on 2026-10-21, tool not run.

## When NOT to optimize

If your install conversion is fine and reviewers don't complain, ship features instead. Size optimization is a one-day pass before a marketing push, not a continuous activity.
Check the thinned download size first.
If the largest variant is well under 200 MB and the app is not near a prompt on cellular, skip the pass.

## Sources

- <https://docs.flutter.dev/perf/app-size>
- <https://developer.apple.com/documentation/xcode/reducing-your-app-s-size> (read through the page's JSON)
- <https://developer.apple.com/help/app-store-connect/reference/app-uploads/maximum-build-file-sizes/>
- <https://support.apple.com/guide/iphone/buy-books-and-audiobooks-iphab21972d/ios> (the only Apple text read with the 200 MB choices, for Books)
- <https://docs.flutter.dev/deployment/android>
- <https://docs.flutter.dev/deployment/obfuscate>
- <https://developer.android.com/topic/performance/app-optimization/enable-app-optimization>
- <https://developer.android.com/blog/posts/grab-r8-profile-guided-optimization-anr-startup-time> (Grab case study, self-reported, read through a summarizing tool)
- <https://engineering.grab.com/r8-optimization-at-scale-with-ai-assisted-debugging>
- <https://github.com/grab/app-sizer>
- <https://developers.google.com/speed/webp>
- <https://developers.google.com/speed/webp/docs/cwebp>
- <https://developer.android.com/studio/write/convert-webp>
- <https://github.com/google/fonts/tree/main/ofl/poppins>
- <https://github.com/notofonts/notofonts.github.io/tree/main/fonts/NotoSans>
