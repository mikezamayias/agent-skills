# Native Swift and Kotlin projects

How each launch readiness phase runs on a native Apple project (Swift, SwiftUI, XcodeGen, Swift packages), a native Android project (Kotlin, Jetpack Compose, Gradle) and a Mac app distributed outside the App Store.
The phase files describe Flutter methods first.
Each phase file points here for the native equivalent.
Findings, severities and the output format stay the same.

## Detect the project

Run the detection from the project root.

```bash
ls pubspec.yaml project.yml Package.swift settings.gradle.kts settings.gradle gradlew 2>/dev/null
find . -maxdepth 3 -name '*.xcodeproj' -not -path './build/*' -not -path './.build/*'
find . -maxdepth 4 -name Package.swift -not -path '*/.build/*' -not -path './build/*'
find . -maxdepth 4 -name AndroidManifest.xml -not -path '*/build/*'
```

- A repository can hold more than one type.
  Resolve the commands below once per project and keep them in the stack profile under `commands`.
- With `project.yml`, the `.xcodeproj` is generated.
  Run `xcodegen generate` before any `xcodebuild` call, and never edit the generated project by hand.
- Read the scheme names from `project.yml` `schemes:` or from `xcodebuild -list -project <name>.xcodeproj`.
  Test schemes are often separate from app schemes.
- Read the Android module names from `settings.gradle.kts`.
  The usual app module is `:app`.
- Pick simulator names from `xcrun simctl list devices available`, never from memory.
- Android builds need the JDK the project documents.
  Read it from the project's `AGENTS.md`, `README.md` or `gradle.properties` and export `JAVA_HOME` before `./gradlew`.

## Distribution targets

Resolve each target's distribution path first, because it decides which store checks apply.

| Target                 | Typical path                                            | Store review                         |
| ---------------------- | ------------------------------------------------------- | ------------------------------------ |
| iPhone, iPad           | App Store, TestFlight                                   | App Review                           |
| Apple Watch, widgets   | Embedded in the iPhone app                              | Reviewed with the iPhone app         |
| Mac, App Store         | Mac App Store                                           | App Review, sandbox required         |
| Mac, outside the store | Developer ID signed, notarized, direct or Homebrew cask | None, Apple notarization only        |
| Android                | Google Play, signed AAB                                 | Play review, Data safety, target SDK |

A watchOS app and its widgets ship inside the iPhone archive.
Check their bundle IDs, entitlements and `Info.plist` keys with the iPhone app.

## Command map

| Need                  | Flutter                            | Native Apple                                                                                                                     | Native Android                                    |
| --------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Generate project      | `flutter pub get`                  | `xcodegen generate` when `project.yml` exists                                                                                    | none                                              |
| Static analysis       | `flutter analyze`                  | `xcodebuild build` warnings, optional `swiftlint` when configured                                                                | `./gradlew :app:lintDebug`                        |
| Unit tests            | `flutter test`                     | `xcodebuild test -project <P>.xcodeproj -scheme <TestScheme> -destination '<dest>'`, `swift test` in a package                   | `./gradlew :app:testDebugUnitTest`                |
| UI tests              | `integration_test`                 | `xcodebuild test` with a UI test scheme                                                                                          | `./gradlew :app:connectedDebugAndroidTest`        |
| Release build         | `flutter build ipa` or `appbundle` | `xcodebuild archive -scheme <App> -configuration Release -destination 'generic/platform=iOS' -archivePath build/<App>.xcarchive` | `./gradlew :app:bundleRelease`                    |
| Outdated dependencies | `dart pub outdated`                | read `Package.resolved` against each package's releases                                                                          | read `gradle/libs.versions.toml` against releases |

Destinations for `xcodebuild`:

| Platform | `-destination`                                       |
| -------- | ---------------------------------------------------- |
| iPhone   | `'platform=iOS Simulator,name=<simulator name>'`     |
| Watch    | `'platform=watchOS Simulator,name=<simulator name>'` |
| Mac      | `'platform=macOS'`                                   |
| Archive  | `'generic/platform=iOS'`, `'generic/platform=macOS'` |

A real device uses `xcrun devicectl list devices` for the identifier and `-destination 'id=<identifier>'`.
Export an archive for upload with `xcodebuild -exportArchive` or the `asc-xcode-build` skill.

## Phase map

### Testing

- Run every test scheme and every Swift package test target the project has, plus the Android unit tests.
  A failure in any of them is Critical.
- Swift Testing and XCTest run through the same `xcodebuild test` and `swift test` commands.
- Coverage on Apple: add `-enableCodeCoverage YES -resultBundlePath build/tests.xcresult`, then `xcrun xccov view --report build/tests.xcresult`.
- Coverage on Android: only when the project already configures JaCoCo or a similar tool.
  When no coverage tool exists, record a Medium finding, skip the threshold and do not add a dependency.
- Skipped tests need a reason.
  Swift Testing: `.disabled("reason")`.
  XCTest: `XCTSkip("reason")`.
  Kotlin: `@Ignore("reason")`.
  A skip without a reason is High.
- Excluded tests: look for `-skip-testing`, test plan `skippedTests`, and Gradle `-x test` or `-x` flags in scripts and CI.
- State tests: each `@Observable` class, `ObservableObject` or view model should have a test file.
  On Android each `ViewModel` should have a JUnit test.
- Tests that write files or images, such as render tests, should say which environment variable turns them on.
  Run them only when the report needs them.

### Security

- Secrets: the same regexes apply.
  Also scan `*.plist`, `*.xcconfig`, `*.entitlements`, `local.properties` and `gradle.properties`.
  `local.properties` must be ignored by git.
- Token storage on Apple: tokens in `UserDefaults` or `@AppStorage` are Critical.
  Use the Keychain.
- Token storage on Android: tokens in plain `SharedPreferences` or a plain DataStore file are Critical.
  Use Android Keystore-backed storage.
- Transport on Apple: flag `NSAllowsArbitraryLoads` and other `NSAppTransportSecurity` exceptions in `Info.plist`.
- Transport on Android: flag `usesCleartextTraffic="true"`, a permissive `network_security_config.xml`, and `android:exported="true"` components without an intent filter need.
  Flag `allowBackup="true"` when the app stores sensitive data.
- Mac: list the entitlements in `Config/**/*.entitlements` and justify each.
  A Developer ID app should enable the hardened runtime and request no exceptions it does not use.
- Dependencies: SwiftPM and Gradle have no built-in outdated report.
  Read the pinned versions in `Package.resolved` or `libs.versions.toml` and check each against its release notes and GitHub security advisories.
  Zero third-party dependencies is a pass.
- Stack-aware: RevenueCat webhook handlers (`purchases-ios`, `purchases-android`) and Supabase RLS checks are the same as Flutter.

### Store compliance

Apple targets that ship through the App Store:

- Privacy policy, App Privacy answers, ATT, Sign in with Apple, IAP and restore rules are unchanged.
  Replace the pubspec checks with `Package.resolved`, `project.yml` `packages` and `import` statements.
- Privacy manifest: look for `PrivacyInfo.xcprivacy` in each app and extension target, and check required-reason API use such as `UserDefaults`, file timestamps and disk space.
  See `app-store-rules/rules/privacy/privacy_manifest.md`.
- ATT: check `NSUserTrackingUsageDescription` in `Info.plist` or `project.yml` `info.properties`, and `import AppTrackingTransparency`.
  An app with no ad or attribution SDK and no ATT import does not track.
- Purchases: StoreKit 2 needs `Transaction.updates` listened to at launch, `Transaction.currentEntitlements` for the unlocked state and a visible restore control that calls `AppStore.sync()`.
  A StoreKit configuration file such as `Config/iOS/App.storekit` is for simulator runs only.
- Icon and launch screen: `AppIcon.appiconset` must contain the 1024 pt marketing icon, every target must have an icon, and no template placeholder remains.
  The watchOS app and widget extensions need their own icons or accent colors as Xcode requires.
- Launch crash: `xcodebuild build` of the release configuration must succeed, and launching on a simulator (`xcrun simctl launch`) must not crash.
- Usage strings: every `NS*UsageDescription` key needs matching API use in the code, and every protected API call needs its key.
- Metadata: `asc` reads `store/metadata` style folders.
  Route to `asc-metadata-sync` and `asc-release-flow`.

Mac app distributed outside the App Store:

- The Mac App Store checklist in `app-store-rules/guidelines/by-app-type/macos.md` does not apply, because no App Review happens.
  Privacy, trademark and metadata honesty rules still apply to the website and the cask.
- Required: Developer ID Application signature, hardened runtime, notarization and a stapled ticket.
  Check with:

  ```bash
  codesign --verify --deep --strict --verbose=2 <App>.app
  spctl --assess --type execute --verbose=4 <App>.app
  xcrun stapler validate <App>.app
  ```

- Notarization and signing steps are in `asc-notarization` and `asc-signing-setup`.
  Update, licensing and trial design is in `macos-direct-sales`.
- Homebrew cask: the download URL must serve the exact notarized artifact, `sha256` must match it, and `brew audit --cask --online <cask>` and `brew style <cask>` must pass.
  A cask is a Ruby file, so reading it needs no execution.
- Scope the verdict per target.
  A missing App Review item on the Mac target is not a finding when the Mac app is not in the store.

Android:

- Data safety, permissions, account deletion and billing policy are unchanged.
  Replace the Dart usage cross-check with a read of `AndroidManifest.xml` against Kotlin code.
- Target SDK: read `targetSdk` in `app/build.gradle.kts`.
  There is no `flutter.targetSdkVersion` to resolve.
  Apply the current Play minimum from the Store Compliance phase.
- 16 KB page size: a pure Kotlin and Compose app with no NDK code and no native libraries has nothing to align.
  Confirm with `unzip -l app/build/outputs/bundle/release/app-release.aab | grep '\.so'`.
- Billing: Google Play Billing is `com.android.billingclient:billing-ktx`.
  Check `queryPurchasesAsync` at startup, acknowledgement within 3 days, and a restore path.
  An app with no digital goods has nothing to check.
- Launcher icon: `res/mipmap-anydpi-v26/ic_launcher.xml` must reference the app's own foreground, background and monochrome layers, not the Android Studio template.
- Release build: `./gradlew :app:bundleRelease` must produce a signed AAB.
  Signing config values must come from the environment or an ignored file, never from tracked source.
- Deprecated APIs: `./gradlew :app:lintDebug` and the compiler warnings from the build replace `flutter analyze`.

### Hardening

- Loading, empty and error states: a SwiftUI view that shows async data needs a state for each.
  Look for `.task`, `.refreshable` and `ProgressView`, and for `if items.isEmpty` branches.
  On Compose look for a sealed UI state with loading, empty and error cases.
- Lifecycle guard, Swift: after an `await` in a view model, check `Task.isCancelled` or `try Task.checkCancellation()` before writing state, and mark view models `@MainActor`.
  Avoid strong `self` capture in long-lived closures and `Combine` sinks.
- Lifecycle guard, Kotlin: collect flows with `collectAsStateWithLifecycle()`, launch in `viewModelScope`, and never write state from `GlobalScope`.
- Text overflow: SwiftUI `lineLimit`, `minimumScaleFactor` and `fixedSize`.
  Compose `maxLines` with `overflow = TextOverflow.Ellipsis`.

### Accessibility

- Interactive elements, SwiftUI: `onTapGesture` on a non-`Button` view needs `.accessibilityAddTraits(.isButton)` and `.accessibilityLabel`.
  A `Button` with an image-only label needs `.accessibilityLabel`.
  `.accessibilityHidden(true)` on an interactive element is High.
- Interactive elements, Compose: `clickable` needs a `role` and the node needs readable text or `contentDescription`.
  An icon-only `IconButton` needs a `contentDescription`.
  `clearAndSetSemantics {}` on an interactive node is High.
- Tap targets: 44 by 44 pt on Apple and 48 by 48 dp on Android.
  Compose `minimumInteractiveComponentSize()` or a `Modifier.size` below 48.dp is a finding.
  On Apple look for `.frame(width:` or `.frame(height:` under 44 on a tappable view.
- Informational icons: SF Symbols in `Image(systemName:)` need a label unless decorative.
- Headings: SwiftUI `.accessibilityAddTraits(.isHeader)`.
  Compose `Modifier.semantics { heading() }`.
- Dynamic Type: SwiftUI fixed font sizes (`.font(.system(size: 14))`) ignore it.
  Prefer text styles or `@ScaledMetric`.
  Compose text uses `sp` and layouts survive `fontScale` 2.0.
- Automated: XCUITest `try app.performAccessibilityAudit()` runs an audit on a screen.
  Compose tests can assert semantics with `onNodeWithContentDescription`.
  Android lint reports missing content descriptions.
- Watch: check text size and tap targets on the smallest case size too.

### Responsive

- SwiftUI: `ViewThatFits`, `horizontalSizeClass`, `dynamicTypeSize` and `GeometryReader` replace `LayoutBuilder` and `MediaQuery`.
  Fixed frames around `Text` fail at large Dynamic Type sizes.
- Compose: `WindowSizeClass`, `BoxWithConstraints` and `LocalConfiguration.fontScale`.
- Watch: test the smallest and largest watch case sizes from `xcrun simctl list devices available`.
- Mac: windows resize, so check minimum window size, split views and full-screen.
- iPhone Duo: the same width-based rule applies.
  See `swiftui-pro/references/resizability.md`.

### Localization

- Apple: `*.xcstrings` String Catalogs replace ARB files.
  Parse the JSON for entries whose `localizations` miss a supported language or have state `new` or `needs_review`.
  `Text("literal")` is a localizable key, so the finding is a string that bypasses the catalog, such as `Text(verbatim:)` with user-facing copy, string concatenation, or a `String` built in code.
- Android: `res/values/strings.xml` and `res/values-<lang>/strings.xml` replace ARB files.
  `./gradlew :app:lintDebug` reports `MissingTranslation` and `HardcodedText`.
  In Compose, flag user-facing string literals in `Text("...")` instead of `stringResource`.
- Per-app language: `res/xml/locales_config.xml` on Android, and the in-app language setting if the app has one.
- Targets: Watch, widgets and the Mac app have their own string catalogs or share one.
  Check each target ships the languages the store listing promises.

### Analytics

- Screen detection, SwiftUI: each top-level `View` reached by a `NavigationStack` destination, `.sheet` or `TabView` tab is one screen.
  Compose: each `composable("route")` in the `NavHost`.
- Actions: `Button` actions and `.onTapGesture` handlers in SwiftUI, `onClick` lambdas in Compose.
- No analytics SDK is a valid result.
  Mark the phase N/A and record that no event is required, then check the privacy label says "Data Not Collected" only when that is true.
- Crash reporting without a third-party SDK:
  - Apple: MetricKit (`MXMetricManagerSubscriber`) and the crash reports in App Store Connect and Xcode Organizer.
    Triage with `asc-crash-triage` and `testflight-feedback`.
  - Android: Android vitals in Play Console.
  - Mac outside the store: Console and `~/Library/Logs/DiagnosticReports`, plus any report the user sends.
- Post-launch watching: `launch-watch` has the round trip for each channel.

### Performance

- Expensive work in `body`: sorting, filtering, formatting, file or network calls inside a SwiftUI `body` or a Compose function body without `remember` is High.
- Rebuild breadth: SwiftUI views that read a whole `@Observable` model when they need one property, and `@State` objects recreated in `body`.
  Compose lambdas and classes that are unstable and force recomposition, and missing `key` in `LazyColumn` items.
- Images: oversized assets in asset catalogs or `res/drawable`, and full-size decoding for thumbnails.
- Tools: Instruments (`xcrun xctrace record`) on Apple, Android Studio profiler and Baseline Profiles on Android.
  A launch time or hitch measurement needs a release build.
- `const` widget checks are Flutter only.

### Polish

- Raw colors: SwiftUI `Color(red:green:blue:)` or hex initializers, and Compose `Color(0xFF...)` outside the theme file.
- Raw spacing: numeric literals in `.padding(` and `.frame(` in SwiftUI, and `.padding(16.dp)` in Compose, where the project has spacing tokens.
- Raw typography: `.font(.system(size:` and `TextStyle(fontSize =` outside the theme file.
- Read the token names from the project's `AGENTS.md` or `CLAUDE.md` as usual.
