---
name: flutter-paywall-and-review-timing
description: >-
  Times paywalls and review prompts in paid Flutter, SwiftUI or Kotlin apps and never binds requestReview to a button. Use when wiring RevenueCat, StoreKit or Play Billing, adding a review prompt or setting paywall cadence. Also use when copying a paywall from a screenshot gallery.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter paywall and review timing

Two systems. **Paywall cadence** is yours. **Review prompts** are Apple's and heavily capped.

The timing rules are platform-independent.
The code samples are Flutter, and the section "Native Swift and Kotlin projects" has the SwiftUI and Kotlin equivalents.
The directory keeps its `flutter-` name so existing links keep working.

## IAP (Flutter `in_app_purchase` 3.x)

Subscribe to `purchaseStream` in `initState`. `queryProductDetails`. `buyNonConsumable` / `buyConsumable`. `restorePurchases()`. If `pendingCompletePurchase`, call `completePurchase` **after** verify + deliver (Android refunds after 3 days if you don't; iOS redelivers forever).

Do not invent RevenueCat dashboard APIs.

## Reviews - never from a button

```dart
final review = InAppReview.instance;
if (await review.isAvailable()) {
  await review.requestReview(); // system may no-op
}
```

Permanent Settings CTA uses `openStoreListing(appStoreId: '123')` or `https://apps.apple.com/app/id123?action=write-review`.
The same write-review URL is Apple's documented route for a review the person starts from a button.
Apple's "Requesting App Store reviews" page uses it for "a review as a result of an action in the UI" (read 2026-11-05).
It has no three-per-year cap.
A maker reports that they count their own calls and taps in `UserDefaults` and, once the count suggests the cap is spent, show a "Write a review" button that opens this URL in place of another `requestReview` call (single report, and their count cannot see whether the sheet appeared).
Use the URL as the second step of any rating flow, and as the fallback when your own log says the system sheet may not show.

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
A launch from a widget, a notification, a Spotlight result or a deep link is a task in progress, so defer any rating ask until that task is done (a reply on a maker's thread, which they accepted, single report; the HIG says to avoid interrupting people while they're performing a task, read 2026-11-05).
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
Whether decorative stars next to a system popup count as a custom review prompt under Guideline 5.6.1 is not settled.
The guideline says "Use the provided API to prompt users to review your app ... and we will disallow custom review prompts" (Apple guidelines page, read 2026-11-05), and it does not define "custom review prompt".
The rule above stays: do not prompt during onboarding.

No "Do you like the app?" gate in front of the prompt, and no routing of unhappy users away from it.
Google's in-app review developer guide says the app shouldn't ask any question before or while showing the review card, including "Do you like the app?".
App Review Guideline 5.6.1 says "we will disallow custom review prompts".
The Section 3 preamble names "paid, incentivized, filtered, or fake feedback" as manipulation that can lead to expulsion from the Apple Developer Program.
Apple never defines gating, so reading a gate as "filtered" feedback is an inference, but it is the risk the gate takes.
Never trade offer codes or anything of value for reviews, because the same preamble treats incentivized feedback as manipulation.
Offer feedback through a separate, always-available "Send feedback" entry instead.

A full-screen lead-in whose Continue button calls `requestReview` is the same open question and adds a second one.
Apple's "Requesting App Store reviews" page says to avoid "requesting a review as the result of a user action" and to avoid asking "immediately when a user launches your app, even if it isn't the first time" (read 2026-11-05).
One maker (X thread, October to November 2026) ships such a lead-in after a major update, with a cooldown, and reports that App Review raised no objection, but they did not show the review.
They have since removed the "Rate 5 stars" line, changed "Not happy? Send feedback" as possibly manipulative, and submitted a new version asking App Review to confirm (single report, no Apple answer captured).
Two other readers, one of them an AI chat, said 5.6.1 forbids it, which is opinion.
If you ship a lead-in, keep the system prompt as the only rating control, never name a star count, give the screen an always-visible close control, and put a question for App Review in the review notes before release.
That advice sits against the rule above that `requestReview` is never bound to a button, because a Continue handler that calls it is exactly that, so this skill does not recommend a lead-in screen (inference).

Showing other people's reviews on an in-app screen or in a screenshot needs the reviewer's permission.
Apple's "Ratings, reviews, and responses" page says "Customer reviews may be used in marketing materials only if permission from the reviewer is granted" (read 2026-11-05).
A maker's lead-in screen shows cards labelled App Store, YouTube and X with names and handles, and they say the App Store ones are "people that I know" (single report).
Apple's page does not say whether an in-app screen is marketing material (inference), so ask the reviewer, keep the written permission, and prefer a count or your own wording over a quoted review.

Asking only people with an active purchase selects by purchase state and not by sentiment.
Apple's guidelines name no rule on choosing who is asked by purchase state, and the HIG endorses asking after demonstrated engagement, which a purchase is (read 2026-11-07).
The Section 3 preamble's "filtered" feedback line, quoted in the no-gating paragraph above, is the same inference risk, so treat this as a design choice and not a documented violation or a safe harbour.
It biases the store average upward against all users, because a purchaser rates the product they chose.
Do not read a rating from purchasers only as a measure of the free experience.
Count written reviews and star ratings apart: the App Store Connect panel counts ratings.
Ask non-purchasers only after a completed win, as above, and keep the separate "Send feedback" entry for them.

Replies to App Store reviews are public and one reply per review shows on the product page.
Apple notifies the reviewer, who can then update the review (Apple ratings and reviews page, read 2026-11-07).
A reply can take up to 24 hours to appear, can be edited at any time, and needs the Admin, Account Holder or Customer Support role.
Apple's help page says you can set up email alerts in App Store Connect for when a user edits a review you replied to, so turn that alert on and count the edits.
Guideline 5.6.1 asks for replies "targeted to the user's comments" with no personal information, spam or marketing.
Write each reply to the content of that review, and say "fixed in the latest update" only when the update fixes what that review reports.
One founder (November 2026, single post, no counts) says they replied to every 1-star this way and "a lot of them changed their rating".
That claim is unverified.

App Store Connect can reset the overview rating when you release a new version (Apple help, read 2026-11-07).
The reset covers every country and region at once, applies to the platform you pick for a universal app, and cannot be undone once the version is released.
Written reviews stay visible.
The product page shows a "recently reset" message and no new overview rating until enough people have rated the new version.
The role needed is Admin or App Manager.
The HIG says to "weigh the benefits of resetting your summary rating against the potential disadvantage of showing fewer ratings" and Apple's ratings page says to use it sparingly.
Reset only when the old average reflects a version you have since replaced, and record the old histogram first.
One founder (November 2026, single post) resets after fixing a buggy launch build and shows 4.6 from 101 ratings a month later, with no before figures.

## Native Swift and Kotlin projects

Same rules, different calls.

### IAP

- iOS (StoreKit 2): `Product.products(for:)`, `product.purchase()`, a `Task` that iterates `Transaction.updates` from app launch, `Transaction.currentEntitlements` for the unlocked state, `transaction.finish()` after delivery, and `AppStore.sync()` behind the Restore button.
  Verify with the `VerificationResult` the API returns and ignore `.unverified` transactions.
- Android (Play Billing): `BillingClient` with `PurchasesUpdatedListener`, `queryProductDetailsAsync`, `launchBillingFlow`, `queryPurchasesAsync` at startup, and `acknowledgePurchase` after delivery.
  Play refunds an unacknowledged purchase after 3 days.
- Do not add RevenueCat to a native app that has no third-party dependencies just for this.
  Full API table: `paywall-conversion-flow`, section "Native Swift and Kotlin implementation".

### Reviews

```swift
import StoreKit
import SwiftUI

struct SessionDoneView: View {
    @Environment(\.requestReview) private var requestReview

    var body: some View {
        // ...
        .task { if shouldAskForReview() { requestReview() } }
    }
}
```

- `requestReview` (iOS 16 and later, macOS 13 and later) is the SwiftUI form of `RequestReviewAction`.
  The caps above apply unchanged.
  Call it from a state change after a completed action and not from a Button handler.
  Call it in `.task` or `.onChange` on the success state.
- UIKit and AppKit apps use `AppStore.requestReview(in:)`.
  `SKStoreReviewController.requestReview(in:)` is the older form.
- Permanent Settings entry: open `https://apps.apple.com/app/id<ID>?action=write-review` with `openURL`.
- A Mac app distributed outside the App Store has no store review sheet.
  Link to the cask page, the download page or the repository instead.
- Android: Google's in-app review API (`ReviewManagerFactory.create(context)`, `requestReviewFlow()`, `launchReviewFlow(activity, info)`) lives in `com.google.android.play:review`, a Google Play library and not AndroidX.
  When the project's dependency rule allows only AndroidX, skip the in-app card and open the Play listing from Settings with `market://details?id=<package>`.
  The test rules above apply: it needs a Play-installed build.
- The same no-gating rule applies to Swift and Kotlin prompts.
- Keep your own call log in `UserDefaults` (Swift) or DataStore or `SharedPreferences` (Kotlin), with the screen name per call.

### Paywall schedule in Swift and Kotlin

Persist `firstOpen` and `lastShown` in `UserDefaults` or DataStore.
Port the loop from the next section as is.
Kotlin `when` and Swift `switch` do not fall through either, so a literal port of the Dart `switch` is safe, and a paraphrase is not.
Skip the paywall when `Transaction.currentEntitlements` or `queryPurchasesAsync` already shows an unlock.

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

Do **not** paraphrase this as "every 4 days through day 7" - that is wrong. The 4-day step emits 7, 11, 15.

## Paywall UX to copy vs drop

Copy: trial attached to annual; Day 0 / Day 5 / Day 7 timeline; free-vs-premium table; optional pay-once lifetime; real annual price visible.

An exit offer after a cancelled purchase sheet is covered in [Paywall conversion flow](../paywall-conversion-flow/SKILL.md), item 6 of "The Order That Works".

A screenshot gallery shows a paywall but not what its close button does, what follows a declined offer, or whether the trial line depends on eligibility.
Before copying one, walk the app on a device with a fresh account, as in the Onboarding flow reference of [Paywall conversion flow](../paywall-conversion-flow/SKILL.md).

Introductory offers cannot be edited and each storefront allows one current and one future offer per product.
See Step D of `asc-revenuecat-catalog-sync` for the limits.
Overlapping introductory offers overwrite the earlier one: Apple says "the latest action overwrites existing introductory offers" when new offers have overlapping dates.
Free trial durations for any standard subscription duration are 3 days, 1 or 2 weeks, 1, 2, 3 or 6 months, and 1 year.
Source: <https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-introductory-offers-for-auto-renewable-subscriptions/>, read 2026-10-23.

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
- <https://developer.apple.com/documentation/swiftui/environmentvalues/requestreview>
- <https://developer.apple.com/documentation/storekit/transaction/updates>
- <https://developer.android.com/google/play/billing/integrate>
- <https://pub.dev/packages/in_app_purchase>
- <https://developer.android.com/guide/playcore/in-app-review/test>
- <https://toomanypaywalls.com>
