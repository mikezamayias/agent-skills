---
name: flutter-shorebird-ota
description: >-
  Ship App Store-safe Dart over-the-air patches with Shorebird after a store binary is out. Use for Dart-only hotfixes that should not wait for App Review, or to add Shorebird to GitHub Actions IPA or AAB builds. It cannot patch native code, assets or plugin native changes.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter Shorebird OTA

App Store-safe **Dart-only** patches after a store binary is out. Native code, assets, Info.plist / AndroidManifest, engine version, and plugins with native diffs still need a store release.

Users see a patch only after the **next app restart**.

## Release then patch

```sh
shorebird init          # writes app_id to shorebird.yaml
shorebird release ios --flutter-version=x.y.z
shorebird release android --flutter-version=x.y.z
# Dart-only fix against that store binary:
shorebird patch ios --release-version x.y.z+n
shorebird patch android --release-version x.y.z+n
```

`patch` does **not** take `--flutter-version`. Pin the engine on `release`.

## CI

- On GitHub Actions use `shorebirdtech/setup-shorebird@v1` (or the `shorebird-release` / `shorebird-patch` actions).
- On other CI, install with the official install script.
- Set `SHOREBIRD_TOKEN` from a Shorebird Console API key.
- Replace `flutter build --release` with `shorebird release`.
- `--dry-run` on PRs.
- iOS runner without certs: `--no-codesign`, then sign the `.xcarchive` elsewhere.

Do not treat Flutter's "how we stay ahead of iOS releases" blog as a shipping recipe. That is the Flutter team's WWDC process, not yours.

## Sources

- <https://docs.shorebird.dev/code-push/>
- <https://docs.shorebird.dev/code-push/ci/generic/>
- <https://docs.shorebird.dev/code-push/ci/github/>
- <https://docs.shorebird.dev/code-push/release/>
- <https://docs.shorebird.dev/code-push/patch/>
