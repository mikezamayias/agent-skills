---
name: store-launch-mastermind
description: >-
  Orchestrate end-to-end public go-live readiness for App Store and Google Play apps, ending in a go or no-go decision. Use when preparing a Flutter or mobile app for public launch or running App Store or Play Store health checks. Also covers assets, metadata, privacy and legal docs, ratings, Data safety, billing, TestFlight and staged rollouts.
metadata:
  docs-verified: "2026-09-28"
---

# Store Launch Mastermind

Use this as the top-level launch orchestrator. Do not inline every store workflow; route specialized work to the focused skills and collect their results into one go/no-go report.

## References

- Load `references/phase-map.md` before planning or running a launch.

## Required Intake

Ask or infer, then confirm:

- Target stores: App Store, Google Play, or both.
- Current phase: first app creation, beta/internal testing, metadata/assets, review submission, approved-but-not-published, public rollout, or rejection fix.
- App identifiers: bundle ID, package name, SKU, app ID, version/build/version code.
- Monetization: free, paid, IAP, subscriptions, ads, external physical goods/services.
- Sensitive features: kids/family, UGC, social, health, location, camera/photos, finance, government, gambling, crypto, VPN, news, AI-generated content.
- Data practices: accounts, analytics, crash reporting, tracking, third-party SDKs, data deletion, privacy policy, ToS.
- Asset state: icons, feature graphic, screenshots, app preview/video, localized listing text.
- Deadline and risk tolerance.

## Orchestration Flow

1. Discover project stack and store state.
2. Run `launch-readiness` for code, policy, store-compliance, security, accessibility, localization, performance, and polish gates.
3. Route asset gaps to `app-graphics` and `app-screenshots`.
4. Route App Store operations (release flow, submission health, metadata sync, ASO audit, screenshot upload) to the installed App Store Connect tooling, such as the `asc` CLI or skills built on it.
5. Route Google Play operations to the installed Google Play Console tooling, such as the Play Developer API or Fastlane `supply`.
6. Route paywall/subscription concerns to `paywall-conversion-flow`, subscription localization in App Store Connect, RevenueCat/catalog skills when applicable, and Play Billing checks.
7. For privacy policies, terms, consent copy, appeal letters, or legal letters, involve legal review skills if available and clearly label the output as drafting support, not legal advice.
8. Produce a single launch report with verdict, blockers, manual gates, exact commands, and owner/action/date.

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
