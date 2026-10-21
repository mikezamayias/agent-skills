---
name: flutter-paywall-and-review-timing
description: >-
  Times paywalls and App Store review prompts in paid Flutter or SwiftUI apps and never binds requestReview to a button. Use when wiring RevenueCat or StoreKit, adding a review prompt or designing onboarding and paywall cadence. Also use when copying a paywall from a screenshot gallery.
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

Apple's docs do not say whether a new app version resets the 3-per-365-days cap for users who have not rated, so treat that as undocumented.
`requestReview` returns nothing on either platform, so the app never learns whether the sheet appeared, whether the user rated, or what they gave.
Keep your own log of calls if you need spacing or analytics.
Log each call with the screen name, so a per-placement rate can be computed from exposures and from ratings per day in App Store Connect.
App Store Connect shows ratings per storefront, so one country page shows fewer than your total, and Apple never says which user rated.
A claim such as "none of my 1-star raters subscribed" cannot be checked from store data and needs another method, such as an in-app survey.
Wire several value moments rather than one, since Apple's developer page says to ask when people have "completed an action, level, or task".
Space the calls, because the HIG says "Avoid pestering people".
One reply on a founder's post (October 2026, unverified, no sample size) reports that moving the prompt from about 10 to about 20 minutes into the first session raised ratings from 2.7 to 4.6 per day.
The same founder also asks a second time after the app's first "wow moment" and keeps a permanent "Rate us" entry in Settings, which must open the store listing and not a custom star UI.

Trigger only after a completed valuable action. Never on cold start, never mid-task, never from a "Rate us" button.
Not during onboarding either.
The HIG, which is advisory design guidance, says "Avoid asking for a rating on first launch or during onboarding".
Good first triggers are the end of a first completed session, workout or lesson.

Reported counterexample (X post, October 2026, one founder, unverified, no controlled test): a prompt as the last onboarding screen, right before the paywall.
The screen has a title, decorative stars that cannot be tapped, and Apple's own `requestReview` popup, which opens by itself.
The founder reports 50 ratings and 4.3 stars in 4 weeks on 738 downloads across all countries, with 6 one-star ratings, and says App Review approved every update with the screen.
The popup first opened after 3.5 seconds, so a user who tapped Continue earlier never saw it, and on 2026-10-06 the founder cut the delay to 1 second.
The reported 5 ratings from 62 viewers (8.1%) before and 45 from about 440 (10.2%) after are my recomputation, and the gap is within noise.
Exposure also grew, so this is not a measured effect of the delay.
If you test a timed popup, trigger the request when the screen appears or after a short fixed delay, and make sure the Continue handler cannot cancel it (hypothesis from one post, not a rule).
A first-hand reply reports that App Review rejected a similar end-of-onboarding rating screen after two weeks live, because "the user does not interact with the app enough to demand rating".
The founder says he tracked 5 of the 1-star raters and that none subscribed, but he also says Apple never tells you who rated, and he gives no method.
The HIG line is advisory and Guideline 3.2.2(x) bars only forcing a rating for access (Apple guidelines page, read 2026-10-21), so the risk is a rejected build, not a documented ban.
Whether decorative stars next to a system popup count as a custom review prompt under Guideline 5.6.1 is not settled (my inference, Apple's text not re-read).
The rule above stays: do not prompt during onboarding.

No "Do you like the app?" gate in front of the prompt, and no routing of unhappy users away from it.
Google's in-app review developer guide says the app shouldn't ask any question before or while showing the review card, including "Do you like the app?".
App Review Guideline 5.6.1 says "we will disallow custom review prompts".
The Section 3 preamble names "paid, incentivized, filtered, or fake feedback" as manipulation that can lead to expulsion from the Apple Developer Program.
Apple never defines gating, so reading a gate as "filtered" feedback is an inference, but it is the risk the gate takes.
Never trade offer codes or anything of value for reviews, because the same preamble treats incentivized feedback as manipulation.
Offer feedback through a separate, always-available "Send feedback" entry instead.

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

An exit offer after a cancelled purchase sheet is covered in [Paywall conversion flow](../paywall-conversion-flow/SKILL.md), item 6 of "The Order That Works".

Introductory offers cannot be edited and each storefront allows one current and one future offer per product.
See Step D of `asc-revenuecat-catalog-sync` for the limits.

Do **not** copy: fake countdown timers, weekly decoys at €200+/yr as the default, close-button-less hard walls, trial-length upsells that silently multiply annual price.

Use [iOS distribution feature flags](../ios-distribution-feature-flags/SKILL.md) to disable the paywall for TestFlight testers. Do not expect `requestReview` there.

Showing a paywall on every launch trains swipe-away. The decaying schedule exists to stop that.

## Sources

- <https://gist.github.com/lukepighetti/344095c57c962cfa86af97f9115b8a4b>
- <https://developer.apple.com/documentation/storekit/requestreviewaction.md>
- <https://developer.apple.com/documentation/storekit/requesting-app-store-reviews>
- <https://developer.apple.com/app-store/ratings-and-reviews/>
- <https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews>
- <https://developer.apple.com/app-store/review/guidelines/#app-store-reviews>
- <https://developer.android.com/guide/playcore/in-app-review>
- <https://x.com/zakisbuilding/status/2112823780821049807>
- <https://x.com/endyjtwn/status/2112826319239307625>
- <https://pub.dev/packages/in_app_review>
- <https://pub.dev/packages/in_app_purchase>
- <https://developer.android.com/guide/playcore/in-app-review/test>
- <https://toomanypaywalls.com>
