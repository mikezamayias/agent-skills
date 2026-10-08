---
name: flutter-paywall-and-review-timing
description: >-
  Time paywalls and App Store review prompts in paid Flutter or SwiftUI apps, and never bind requestReview to a button. Use when wiring RevenueCat or StoreKit, adding a review prompt or designing onboarding and paywall cadence. Also use when copying a paywall from a screenshot gallery.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter paywall and review timing

Two systems. **Paywall cadence** is yours. **Review prompts** are Apple's and heavily capped.

## IAP (Flutter `in_app_purchase` 3.x)

Subscribe to `purchaseStream` in `initState`. `queryProductDetails`. `buyNonConsumable` / `buyConsumable`. `restorePurchases()`. If `pendingCompletePurchase`, call `completePurchase` **after** verify + deliver (Android refunds after 3 days if you don't; iOS redelivers forever).

Do not invent RevenueCat dashboard APIs.

## Reviews — never from a button

```dart
final review = InAppReview.instance;
if (await review.isAvailable()) {
  await review.requestReview(); // system may no-op
}
```

Permanent Settings CTA uses `openStoreListing(appStoreId: '123')` or `https://apps.apple.com/app/id123?action=write-review`.

Apple caps (`RequestReviewAction`):

- User has **not** reviewed on this device: at most **3 prompts per 365 days**.
- User **has** reviewed: only on a **new version** and **more than 365 days** later.
- Dev builds always show UI. **TestFlight does nothing.**
- Android `requestReview` needs a Play-installed build to test, from an internal test track or internal app sharing.
  Internal app sharing disables the submit button, and quotas apply only to production installs.

Trigger only after a completed valuable action. Never on cold start, never mid-task, never from a "Rate us" button.

## Paywall app-open schedule

Pighetti gist math (Dart 3 `switch` does **not** fall through). Skip if already subscribed. Persist `firstOpen` and `lastShown` (ISO-8601).

Copy the **loop**, not the gist file (it imports private `let.dart` / `$revenueCat`):

```text
x = -1
for i in 1..29:
  i <= 4  → x += 1   // days 0, 1, 2, 3
  i <= 7  → x += 4   // 7, 11, 15
  i <= 14 → x += 7   // 22 … 64
  else    → x += 14
```

Do **not** paraphrase this as "every 4 days through day 7" — that is wrong. The 4-day step emits 7, 11, 15.

## Paywall UX to copy vs drop

Copy: trial attached to annual; Day 0 / Day 5 / Day 7 timeline; free-vs-premium table; optional pay-once lifetime; real annual price visible.

Do **not** copy: fake countdown timers, weekly decoys at €200+/yr as the default, close-button-less hard walls, trial-length upsells that silently multiply annual price.

Use [iOS distribution feature flags](../ios-distribution-feature-flags/SKILL.md) to disable the paywall for TestFlight testers. Do not expect `requestReview` there.

Showing a paywall on every launch trains swipe-away. The decaying schedule exists to stop that.

## Sources

- <https://gist.github.com/lukepighetti/344095c57c962cfa86af97f9115b8a4b>
- <https://developer.apple.com/documentation/storekit/requestreviewaction.md>
- <https://pub.dev/packages/in_app_review>
- <https://pub.dev/packages/in_app_purchase>
- <https://developer.android.com/guide/playcore/in-app-review/test>
- <https://toomanypaywalls.com>
