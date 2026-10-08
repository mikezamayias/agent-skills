---
name: flutter-app-size-audit
description: >-
  Cut Flutter app install size by 30-60% by attacking build defaults, asset formats, and shrinking flags. Use when install conversion is dropping, when reviewers cite size, or before any major release.
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
   In `android/app/build.gradle(.kts)` set `isMinifyEnabled = true` and `isShrinkResources = true` (AGP 9.3+: `optimization { enable = true }`).
   R8 only touches JVM code, so add keep rules only for native Android dependencies that use reflection and ship no consumer rules.
   Pure Dart packages, such as JSON serializers, are unaffected.
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

## When NOT to optimize

If your install conversion is fine and reviewers don't complain, ship features instead. Size optimization is a one-day pass before a marketing push, not a continuous activity.

## Sources

- <https://docs.flutter.dev/perf/app-size>
- <https://docs.flutter.dev/deployment/android>
- <https://docs.flutter.dev/deployment/obfuscate>
- <https://developer.android.com/topic/performance/app-optimization/enable-app-optimization>
- <https://developers.google.com/speed/webp>
- <https://developers.google.com/speed/webp/docs/cwebp>
- <https://developer.android.com/studio/write/convert-webp>
- <https://github.com/google/fonts/tree/main/ofl/poppins>
- <https://github.com/notofonts/notofonts.github.io/tree/main/fonts/NotoSans>
