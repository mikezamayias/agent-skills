---
name: flutter-app-size-audit
description: >-
  Cuts Flutter app install size by 30-60% by attacking build defaults, asset formats, and shrinking flags. Use when install conversion is dropping, when reviewers cite size, or before any major release.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter App Size Audit

Many app size problems come from build defaults you never questioned, not from your assets.
Check all five layers and measure each change with `--analyze-size`.

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

Open the size report and look for the top 5 contributors. If a single asset > 1MB, attack it first.

For Android host code and libraries, Grab's open-source App Sizer (MIT) attributes download size to teams, modules and libraries from APK, AAR and JAR input, through a Gradle plugin or a CLI.
It does not read Flutter Dart AOT size, so keep `--analyze-size` for that.
Its README warns class sizes are estimates that suit trends, not exact figures.
Evidence: README read on 2026-10-21, tool not run.

## When NOT to optimize

If your install conversion is fine and reviewers don't complain, ship features instead. Size optimization is a one-day pass before a marketing push, not a continuous activity.

## Sources

- <https://docs.flutter.dev/perf/app-size>
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
