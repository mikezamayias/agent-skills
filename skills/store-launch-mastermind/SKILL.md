---
name: store-launch-mastermind
description: >-
  Orchestrates end-to-end public go-live readiness for App Store and Google Play apps, ending in a go or no-go decision. Use when launching a Flutter, Swift or Kotlin app or running store health checks, including Mac direct release. Also covers assets, metadata, privacy, legal docs, ratings, Data safety, billing, TestFlight and rollouts.
metadata:
  docs-verified: "2026-09-28"
---

# Store Launch Mastermind

Use this as the top-level launch orchestrator. Do not inline every store workflow; route specialized work to the focused skills and collect their results into one go/no-go report.

## References

- Load `references/phase-map.md` before planning or running a launch.

## Required Intake

Ask or infer, then confirm:

- Project type per target: Flutter, native Swift (iPhone, Watch, widgets, Mac) or native Kotlin (Android).
- Target stores: App Store, Google Play, or both.
- Mac distribution: Mac App Store, or Developer ID with notarization and a direct download or Homebrew cask.
- Current phase: first app creation, beta/internal testing, metadata/assets, review submission, approved-but-not-published, public rollout, or rejection fix.
- App identifiers: bundle ID, package name, SKU, app ID, version/build/version code.
- Monetization: free, paid, IAP, subscriptions, ads, external physical goods/services.
- Sensitive features: kids/family, UGC, social, health, location, camera/photos, finance, government, gambling, crypto, VPN, news, AI-generated content.
- Data practices: accounts, analytics, crash reporting, tracking, third-party SDKs, data deletion, privacy policy, ToS.
- Asset state: icons, feature graphic, screenshots, app preview/video, App Store creative assets (product page header, search results), localized listing text.
- Deadline and risk tolerance.

## Orchestration Flow

1. Discover project stack and store state.
   Detect Flutter (`pubspec.yaml`), native Apple (`project.yml`, `*.xcodeproj`, `Package.swift`) and native Android (`settings.gradle.kts`, `gradlew`) as `launch-readiness` does, and run every later step per project.
2. Run `launch-readiness` for code, policy, store-compliance, security, accessibility, localization, performance, and polish gates.
3. Route asset gaps to `app-graphics` and `app-screenshots`.
4. Route App Store operations (release flow, submission health, metadata sync, ASO audit, screenshot upload) to the installed App Store Connect tooling, such as the `asc` CLI or skills built on it.
   If a guideline interpretation is borderline, the user can book a Meet with Apple appointment before submitting.
   Where: the Meet with Apple schedule page on developer.apple.com.
   Steps: request a slot and include the app's Apple ID, if one exists, and the specific questions.
   Cost: a 30-minute Webex video call on Tuesdays and Thursdays, and slots can fill quickly (two X posts report full schedules, both unverified).
   Open the schedule page a few weeks before the planned submission, because Apple's page states no date for new slots.
   The appointment is informational only and does not pre-approve or expedite a review.
5. Route Google Play operations to the installed Google Play Console tooling, such as the Play Developer API or Fastlane `supply`.
6. Route paywall/subscription concerns to `paywall-conversion-flow`, subscription localization in App Store Connect, RevenueCat/catalog skills when applicable, and Play Billing checks.
7. For privacy policies, terms, consent copy, appeal letters, or legal letters, involve legal review skills if available and clearly label the output as drafting support, not legal advice.
8. Produce a single launch report with verdict, blockers, manual gates, exact commands, and owner/action/date.

## Native Swift and Kotlin projects

The flow is the same.
Only the build, signing and crash tooling change.

| Step             | Flutter                          | Native Apple                                                                               | Native Android                                       |
| ---------------- | -------------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| Generate project | `flutter pub get`                | `xcodegen generate` when `project.yml` exists                                              | none                                                 |
| Tests            | `flutter test`                   | `xcodebuild test -scheme <TestScheme> -destination '<dest>'`, `swift test` in packages     | `./gradlew :app:testDebugUnitTest`                   |
| Release build    | `flutter build ipa`, `appbundle` | `xcodebuild archive -scheme <App> -destination 'generic/platform=iOS' -archivePath <path>` | `./gradlew :app:bundleRelease`                       |
| Upload           | `asc` or Fastlane                | `asc builds upload` or the `asc-xcode-build` skill                                         | Play Console or Play Developer API                   |
| Crash source     | Sentry or Crashlytics            | MetricKit, App Store Connect crash reports, `asc-crash-triage`, or the project's SDK       | Android vitals in Play Console, or the project's SDK |
| Subscriptions    | RevenueCat or `in_app_purchase`  | StoreKit 2 or RevenueCat                                                                   | Google Play Billing or RevenueCat                    |

- A watchOS app and its widgets ship inside the iPhone archive and are reviewed with it.
  Check their bundle IDs and entitlements as part of the iPhone build.
- A Mac app outside the App Store has no review.
  Its gate is Developer ID signing, hardened runtime, notarization, a stapled ticket and the cask or download page, per `launch-readiness` and `asc-notarization`.
  Skip the Mac App Store checklist for it.
- Android needs JDK setup from the project's own docs before `./gradlew`.
- Without a crash SDK, "crash reporting" in the intake means store-provided reports, so confirm someone reads them.

## Verdict Rules

- `BLOCK`: legal/policy blocker, missing privacy policy/Data safety/App Privacy, build cannot be submitted, missing required assets, payment policy violation, target SDK/API blocker, app crashes, or required account access/test credentials missing.
- `HOLD`: no hard blocker, but high-risk manual declarations, weak assets, missing localization, ASO gaps, unverified subscription restore/purchase flow, or incomplete staged rollout plan.
- `SHIP`: all hard gates clear, manual store forms confirmed, assets and metadata complete, build/release status verified, and rollback/pause plan documented.

## Manual Gates

Stop and ask for explicit user confirmation before:

- Submitting for review.
- Publishing or starting production rollout.
- Changing price, availability, subscriptions, base plans, offers, or IAPs.
- Declaring Data safety, App Privacy, age/content ratings, target audience, ads, health, finance, or other legal/policy claims.
- Sending appeal/legal letters.

## Output Format

Write or update `tasks/store-launch-report.md` in the project root when working inside a repo.

Include:

- Verdict: `SHIP`, `HOLD`, or `BLOCK`.
- Store matrix: App Store status, Google Play status.
- Blockers and high-risk items.
- Required manual declarations.
- Assets checklist.
- Metadata/localization checklist.
- Build/release commands already run and their result.
- Next commands or UI steps.
- Rollback/pause plan.

## Sources

- <https://support.google.com/googleplay/android-developer/answer/14151465>
- <https://developers.google.com/android-publisher>
- <https://docs.fastlane.tools/actions/supply/>
- <https://github.com/rudrankriyam/App-Store-Connect-CLI>
