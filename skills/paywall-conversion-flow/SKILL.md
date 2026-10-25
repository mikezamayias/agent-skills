---
name: paywall-conversion-flow
description: >-
  Designs value-first onboarding and paywalls that convert in freemium Flutter, native Swift or native Kotlin apps. Use when adding or auditing IAP, StoreKit, Play Billing, RevenueCat paywalls, free trial flows or onboarding screens.
metadata:
  docs-verified: "2026-09-28"
---

# Paywall Conversion Flow

The single biggest lever in a freemium app is the first 30 seconds and the placement of the paywall.
Most indies lose conversion by following the wrong order.

## The Order That Works

1. **Show value before asking for anything.** Skip the tutorial. Drop the user into a working "test project" or pre-filled state so they feel a win in <30s.
2. **Ask for a rating after a win in the main app, never during onboarding and not on the way to the paywall.** The rule, Apple's caps and the rejection risk are in [Flutter paywall and review timing](../flutter-paywall-and-review-timing/SKILL.md).
   One founder (X post, October 2026, unverified) reports a rating screen as the last onboarding step before the paywall, with 50 ratings and 4.3 stars in 4 weeks.
   His 5 of 62 viewers (8.1%) before and 45 of about 440 (10.2%) after a popup delay change are my recomputation and sit within noise.
   A first-hand reply reports that App Review rejected a similar screen.
   He says none of the 5 one-star raters he tracked subscribed, but Apple never reveals who rated, so any claim about raters needs another method.
   Judge the placement by paid conversion, not by rating count.
3. **Hard paywall AFTER a success event** — never on launch, never on tab switch. Wait for: streak day 3, first export, first AI generation, first item saved.
4. **Free trial requires card on file.** It removes freeloaders and raises trial-to-paid conversion.
   In First Page Sage's SaaS benchmark (86 companies, 2022-2025), card-required trials converted 48.8% to paid vs 18.2% for cardless, but visitor-to-trial fell from 8.5% to 2.5%, so judge the whole funnel, not trial-to-paid alone.
   Make the cancel path easy to keep ratings intact.
   Google Play already verifies a valid payment method before a store free trial starts, so a cardless trial only exists outside store billing.
   Judge a trial by paid conversion, not trial-start rate.
   RevenueCat's State of Subscription Apps 2026 (metrics for 2025, read 2026-10-24) reports median trial-to-paid conversion of 25.5% for trials of 4 days or less, 37.4% for 5 to 9 days and 42.5% for 17 to 32 days.
   It also reports that 55% of 3-day trial cancellations happen on Day 0, and that 84% of 3-day and 64% of 7-day trial cancellations happen by Day 1.
   These medians compare different apps, so they are a reason to test a longer trial and not the lift to expect.
   Change the trial length alone and write the date in the test notes, because a longer trial delays the first conversions by the length difference (inference), which makes the next days look slow.
   One indie fasting app in October 2026 reported a 20% trial-start week with zero trials converting, while its no-trial weeks reached 12-19% paid, on samples in the tens.
   The founder's own explanation, which they did not test, is that paid ads optimized on trial starts find users who start trials and never pay.
   Apple allows one introductory offer per person per subscription group.
   When a ladder mixes a free trial, a paid introductory offer and a no-trial plan, record which products share a group.
   Check eligibility before showing the offer (StoreKit 2 `isEligibleForIntroOffer`) and show no trial CTA to an ineligible user, since that repeats a misleading claim under Guideline 3.1.2.
   Apple's page does not state what happens to a user who bought another product in the group at full price, so do not assume either way (Apple help page, read 2026-10-20).
   One observed paywall (Liftoff, screen recording, X post 2026-10-23, no results reported) offers a free 7-day trial and a 30-day pay-up-front introductory offer at 2.99 EUR side by side, both renewing at 79.99 EUR a year.
   A product has one current introductory offer per storefront, so such a pair is most likely two products (inference), and the subscription groups were not visible.
   Its "SAVE 55%" badge matches the first month against the annual price per month, which the screen does not say.
   If you test such a pair, say on the badge what the saving is compared with, and read paid conversion per paywall viewer and refund rate for both plans.
   In one founder's transaction lists (single report, October 2026, two screenshots), 4 of 7 visible trial rows carry a cancelled badge within hours of starting.
   The sample is tiny and the badge meaning is unverified, so use it only as a reason to read the cancel timing column before judging a trial.
5. **Offer weekly + yearly, not just monthly.** Weekly lowers commitment fear and converts the "let me test it" segment that monthly scares off.
   One operator's recipe (X post, October 2026, unverified, no conversion, refund or revenue figure given) pairs one trial with one no-trial plan in two ladders.
   Ladder A is yearly at $39.99 with a free 3 day trial plus a weekly plan with no trial.
   Ladder B is weekly at $9.99 with a free 7 day trial plus a yearly plan with no trial.
   The post does not define "direct", so the no-trial reading is an inference, and it names no weekly price for A or yearly price for B.
   Apple permits both trial lengths (Apple help page, read 2026-10-20).
   Treat both as hypotheses to A/B test, not defaults.
   Judge each on paid conversion per paywall viewer, refund rate and revenue per viewer after the first renewal, not on trial starts.
   Write the annualized weekly cost in the test notes, since $9.99 per week is $519.48 per year, 13 times the $39.99 yearly plan (arithmetic).
   One indie (single report, October 2026, a month of data, one screenshot) runs $5 per week and $49.99 per year, both with free trials, and a $24.99 yearly exit offer that is inferred from the product list.
   Treat it as one datapoint, not a price benchmark.
   A third operator recipe (X post by @ChadAppDev, 2026-10-24, unverified, no conversion, refund or revenue figure given) pairs $39.99 per year with $6.99 per week and a $0.99 first week, on a hard paywall.
   The author calls the $0.99 week a trial, but it fits Apple's pay as you go introductory offer type (inference from the offer types page).
   They say users "forget to cancel at roughly the same rate as free trials" and that "in just 6 weeks" they pay more than the yearly price, and they give no data for either.
   The break-even claim is one week early: 6 weeks cost $0.99 plus 5 times $6.99, which is $35.94, and 7 weeks cost $42.93 (arithmetic), before Apple's commission and any refund.
   $6.99 per week is $363.48 per year, about 9.1 times the $39.99 yearly plan (arithmetic), just under the 10 times heuristic in the anti-patterns.
   If you test it, show the $6.99 price at a size and contrast next to the $0.99, read refund rate and revenue per paywall viewer at week 8, and judge it against a free-trial ladder on the same traffic.
6. **Add one exit offer after the buyer cancels the store purchase sheet.**
   Superwall's `transaction_abandon` placement fires when a user dismisses the store purchase sheet before the transaction completes, and a matching paywall replaces the current one.
   RevenueCat's closest feature is Exit offers, which show a second paywall when the user dismisses the paywall without buying.
   Its docs do not say it fires on a cancelled purchase sheet, and it works only with `presentPaywall` or `presentPaywallIfNeeded`, so it is not shown to be equivalent.
   One indie fasting app shows a single discounted yearly plan with a close button, a 5 minute timer and the real billed price, and its author reported that the exit paywall produced 23% of its results over two weeks (author's figure, unit not stated, not verified).
   A second founder adds the offer in a follow-up release, after the base paywall is live.
   Ship it in a reviewed update, describe it in Notes for Review, and measure it on its own line so the base paywall rate stays clean.
   One indie article (2026-08-09, single source, unverified) gives the reason: reviewers judge a transaction abandon offer subjectively, and a first submission with a contested feature may go to a slower review track.
   Apple publishes no review tiers (Apple App Review page, read 2026-10-25), so treat the tier claim as a guess.
   The part that matches Apple's text is to describe the offer in the notes, because Guideline 2.3.1(a) requires new features to be described with specificity.
   Tag its events with a `placement` property, see [Flutter observability instrumentation](../flutter-observability-instrumentation/SKILL.md).
   Never mention it in What's New, because that text is public and shows the offer to every user.
7. **After the first purchase and after a lapse, sequence offers by user state, and test each as its own line.**
   One LinkedIn post (October 2026, unsourced, no data) lists five add-ons to onboarding and a paywall for larger apps: an upsell to new subscribers, a downsell to users who declined, email follow-up for non-purchasers, a retention offer when a subscriber leaves, and a win-back offer after a lapse.
   Treat the list as a checklist of what to measure, not as evidence that each pays.
   The same post says "up to 10% resubscribe within a year", with no source, so do not plan on it.
   Apple's offer types, eligibility and limits are in [subscription offers](references/subscription-offers.md).
   - Win-back on iOS: use Apple's win-back offer, not a custom price.
     It is per product, needs a subscription approved by App Review, and is for churned subscribers only (`expirationDate` in the past and `willAutoRenew` false).
     Set Minimum Paid Duration, Time Since Last Subscribed (1 to 24 months) and Wait Between Offers (2 to 24 months) deliberately, and write the chosen window in the test notes, because the post's "3-6 months" is a guess.
   - Retention offer for a subscriber who turned auto-renew off on iOS: use a promotional offer.
     Apple deems anyone with an existing or expired subscription in the app eligible, and you add your own criteria.
     Listen for the `DID_CHANGE_RENEWAL_STATUS` server notification, let the server decide eligibility and tell the app to show the offer.
     Redeeming needs a server-generated signature, and it works on iOS 12.2 and later.
   - Downsell for a user who never subscribed: a promotional or win-back offer is not available to that user, so use a separate cheaper product or an offer code, and give it its own `placement` value.
   - Pause: Google Play lists pause as a subscriber action.
     The Apple pages read describe no pause, so do not promise one on iOS.
   - Email follow-up needs an address, so decide where it is collected, and see `launch-watch` for EU consent and an unsubscribe link before the first send.
   - Keep every offer out of What's New, see `asc-whats-new-writer`.
   - Judge each stage by incremental revenue per eligible user, refund rate and churn, not by redemptions.

## Native Swift and Kotlin implementation

The order, copy and tests above do not depend on Flutter.
Only the purchase plumbing changes.
Do not add RevenueCat to a native app that has no third-party dependencies unless the user asks, because StoreKit 2 and Play Billing cover purchase, restore and entitlement checks.

| Need                      | Flutter `in_app_purchase` | Native iOS (StoreKit 2)                                                              | Native Android (Play Billing)                                                |
| ------------------------- | ------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| Load products             | `queryProductDetails`     | `Product.products(for: ids)`                                                         | `BillingClient.queryProductDetailsAsync`                                     |
| Buy                       | `buyNonConsumable`        | `try await product.purchase()` and handle `.success`, `.userCancelled`, `.pending`   | `launchBillingFlow` with the chosen offer token                              |
| Live updates and renewals | `purchaseStream`          | `for await` over `Transaction.updates`, started at launch                            | `PurchasesUpdatedListener`                                                   |
| Current entitlement       | verify and deliver        | `Transaction.currentEntitlements`, verified results only                             | `queryPurchasesAsync` at startup                                             |
| Finish the purchase       | `completePurchase`        | `await transaction.finish()` after delivering                                        | `acknowledgePurchase` or `consumeAsync` within 3 days, or Play refunds       |
| Restore                   | `restorePurchases()`      | `try await AppStore.sync()` behind a visible Restore button                          | `queryPurchasesAsync`, no separate store call                                |
| Trial eligibility         | store response            | `product.subscription?.isEligibleForIntroOffer`                                      | offers returned for the user in `ProductDetails`, show only what is returned |
| Manage or cancel          | store link                | `.manageSubscriptionsSheet(isPresented:)` or `AppStore.showManageSubscriptions(in:)` | deep link to Play subscription management                                    |

- SwiftUI can use `SubscriptionStoreView` or `StoreView` for a standard paywall.
  A custom paywall needs the price, period, trial end date and Restore control from the audit checklist.
- Test iOS purchases with a StoreKit configuration file in the scheme (simulator and Xcode runs) and with `SKTestSession` in unit tests.
  Sandbox and TestFlight tests need the products in App Store Connect.
  Manage them with the `asc-*` skills.
- Test Android purchases from a Play-installed build on an internal test track with a license tester account.
  Billing does not work from a sideloaded debug APK.
- A one-time unlock is a non-consumable on both stores.
  The free-versus-paid check is an entitlement read at launch, not a stored flag.
- Do not sell a Mac app distributed outside the App Store with StoreKit.
  Licensing and trials for it are in `macos-direct-sales`, and the web checkout route is in `app-to-web-checkout`.
- The paywall schedule and review prompt timing code is in [Flutter paywall and review timing](../flutter-paywall-and-review-timing/SKILL.md), which has Swift and Kotlin versions.

## Anti-patterns to remove

- Paywall on cold launch.
- "Subscribe to continue" gate before any value is delivered.
- Tutorial screens explaining features (vs showing outcomes).
- Yearly-only pricing with no escape hatch for low-trust buyers.
- A weekly plan whose annualized price is above about 10 times the yearly price as the headline plan (my heuristic, not from Apple or any source). If you test it, show the weekly price, the billing period and the trial end date, and describe what the user gets for the price, as Guideline 3.1.2(c) requires.
  The $6.99 weekly and $39.99 yearly pair on one founder's X paywall is 9.1 times, so a 10 times line would not flag it (arithmetic).
  Read the heuristic as a floor for suspicion, not a pass.
- Replacing the concrete feature list with an outcome headline as the default.
  Keep the list, as in [Paywall transparency](../paywall-transparency/SKILL.md), and treat an outcome headline as an A/B test idea with no data behind it.
  One founder (X post, October 2026) says selling the result instead of listing features raised conversion "immediately", with no figure or sample size.
  A reply gives one example, "on-device AI reads your receipt" becoming "you're in the shop, do you still have milk?", also with no data.
  Test the headline with the feature list kept below it, and judge it on paid conversion per paywall viewer.
- Paragraphs on the paywall. Keep each plan to a price, a period and one concrete line.
- Abstract value claims. Anchor the price to something real instead ("€49 is three takeaways").
- Fake countdowns or a price that only appears after tapping.
- A one-time offer whose claims are not true. A countdown offer is legitimate only when the shown state persists so the offer never reappears for that user, the timer does not reset on reopen or relaunch, and claims such as "lowest price we've offered" are true for that storefront's price history.
  In the EU, Annex I point 7 of the Unfair Commercial Practices Directive (2005/29/EC) bans in all circumstances, with no harm test, falsely stating that a product will only be available for a very limited time in order to elicit an immediate decision.

## Audit checklist (use before each release)

- [ ] First successful action happens within 30 seconds.
- [ ] Rating prompt fires after a clear win in the main app, never during onboarding and not before the paywall (see [Flutter paywall and review timing](../flutter-paywall-and-review-timing/SKILL.md)).
- [ ] Paywall fires after a success event, not on launch.
- [ ] Plans visible: Weekly, Yearly, Lifetime (if applicable).
- [ ] Free trial CTA prominent; cancel path documented in-app.
- [ ] Native iOS: `Transaction.updates` is listened to at launch and every transaction is finished after delivery.
- [ ] Native Android: purchases are acknowledged within 3 days and `queryPurchasesAsync` runs at startup.
- [ ] Restore Purchases link is on the paywall (App Review Guideline 3.1.1 requires a restore mechanism for restorable purchases, and the paywall placement builds trust).

## Onboarding flow reference

A high-performing onboarding structure to pair with the order above:

1. Value screens or an instant first win, with progress indicators and Skip.
2. Goal and motivation questions ("why are you here?", multi-select chips) so the experience feels tailored early.
3. Personalized result, recommendations or community previews based on the answers.
4. Optional account creation, one-tap social or pre-filled, with a visible Skip.
5. Soft premium upgrade with clear benefits and trial (this is the "after value" slot from the order above).
6. Celebration / "creating your space" animation → main app.

Apple's Human Interface Guidelines on onboarding (read 2026-10-23, last changed June 10, 2024) set the limits for this list.
They say to design a flow that is "fast, fun, and optional", to "Teach through interactivity", and to "Postpone nonessential setup flows or customization steps" with reasonable defaults.
They say to put a permission request inside onboarding only when the app needs that access before it can function, and otherwise to ask when the person first uses the feature that needs it.
They say to let people experience the app before asking for a rating or a purchase.
A concept mock or a design showcase is design evidence and not conversion evidence, so check a flow against shipped apps and measured results before copying it.

A result gated behind the paywall must come from the user's real input.
Do not show a fabricated score or a fake loading analysis to drive a purchase.
One founder (X post, October 2026, self-reported) describes a long analysis animation followed by "unlock your rating" and says the sunk cost of about 20 questions raises conversion.
Treat that as a risk of a misleading claim (my inference) and keep the paywall honest about what unlocks.
A positive example: one gym app (Liftoff, screen recording, X post 2026-10-23, no conversion figure) asks for one real input, shows the rank result free, and only then shows the paywall.
Its timed "Compiling user profile" screen still falls under the fake-analysis rule above, because its real work is unknown.

Treat signup as deferrable.
Duolingo's iOS onboarding grew from 6 screens in 2018 to 24 in 2023-2024 and 20 in 2026, observed by Zach Witzel (Helium) in dated screenshots from August 2026.
Third-party teardowns describe its order as language, goal and motivation questions, then a first lesson, then signup.
So Duolingo asks its questions before it delivers value, and it is no example of "value first".
Duolingo's own word on this is a 2017 First Round Review interview, where Gina Gotthilf says moving the signup screen back "a few steps" raised daily active users by about 20%, without saying where it moved to.
The 2025 and 2026 screenshots also show an add-widget step after the notification permission.
Duolingo's own blog says only that it tested a widget promotion after learners finished a lesson.
A reply on the post reports a 3-step full-screen paywall with a close button after the outcome-promise step, which is not in the screenshots and is unverified.
None of this is published test data, and the flow may differ by cohort and date.

Execution details that matter: always a visible Skip or back, pre-select popular options to cut decision fatigue, show real social-proof numbers, keep the whole flow under 30-45 seconds. Track onboarding completion rate, time to first meaningful action, day-1 retention, and first-session conversion.

One founder's numbers, from a single account (October 2026, a screenshot of $12,698 in 28-day revenue, unverified): 12-13 onboarding screens, a 90% completion target, and under 80% treated as a sign something is wrong.
He does not say how completion is defined, and this is not a benchmark.

Treat the first onboarding as hypothesis one and chart the funnel by cohort: onboarding start, abandonment screen, paywall reached, trial started, paid.
A promotional X article (October 2026, by the makers of an app builder) quotes Cal AI as having run 123 A/B experiments, 160 paywall designs, 424 variants and 61 onboarding paywall experiments, with monthly revenue up more than 3x and trial-to-paid up 31%.
These are unverified secondhand figures, which the article itself marks "reportedly", so use them as a reported example and not as a benchmark.

## Measure

- Before reading any paywall result, trigger each placement on a test device and confirm its event reaches the analytics log with a nonzero viewer count.
  A rate divided by zero viewers looks like a flat test.
  One reply on a founder's post (October 2026, single unverified anecdote) describes three tests run on an app whose paywall event never fired.
- Paid conversion is weekly unique buyers divided by unique paywall viewers.
- Keep trial starts on a separate line and never count them as paid.
- Keep trial starts, trial conversions (the first paid renewal after a trial) and paid introductory offer starts (pay up front or pay as you go) on three separate lines, and never add them together.
  Report a paid introductory offer start as revenue, not as a trial conversion.
  In RevenueCat webhooks they are `INITIAL_PURCHASE` with `period_type` `TRIAL`, `RENEWAL` with `is_trial_conversion` true, and `INITIAL_PURCHASE` with `period_type` `INTRO` (event types page, read 2026-10-20).
  Dashboard labels such as "Trial Convert" and "Intro Offer Start" came from an unnamed tool in a source screenshot and are not RevenueCat event names, so map them to the documented fields before counting.
- Read active trials and new trial starts next to revenue.
  Revenue on a given day mostly comes from trials started a trial-length earlier, so a rising revenue day with falling active trials predicts a weaker next week (inference from subscription arithmetic).
  One founder's Day 12 and Day 13 posts (October 2026, single report, screenshots not verified) show the lag: Day 13's whole $199.96 was four yearly trial conversions while active trials fell to 26.
- Bucket weekly when daily paywall views are under about 20, because daily rates are noise.
- Annotate every price, offer and onboarding change on the chart, and exclude the developer's own country or test devices.
- Never report a partial-week point as a result.
  One indie's chart headlined a dashed, incomplete week at 22.2%.
  An earlier capture of the same chart read 14.1% for its then-partial point against 12.2% once the week completed, an inference from two captures with unconfirmed week boundaries.
- When a founder reports a one-day jump, attribute it from that day's transaction list.
  Read each row's product, price and type (new subscription, trial start, trial conversion, cancelled trial), and add the rows to the day total before crediting a feature.
  A 28-day tile also moves when old days roll out of the window (unverified inference from the tile label, not checked against RevenueCat docs).
- Report a 95% interval with each rate. For example, 23 buyers out of 104 viewers is 22% with a range of about 15-31%.
- Fix the number of paywall viewers per arm before a test starts, and do not stop on a good-looking day, because stopping early produces false wins.
  At a two-sided 5% significance level and 80% power, a 5% baseline needs about 31,000 viewers per arm to detect a 10% relative lift, about 8,200 for 20% and about 1,500 for 50%.
  A 10% baseline needs about 14,800, 3,800 and 700.
  A small app cannot reach these numbers for small changes, so test large changes (price, offer, paywall position) and treat anything below the planned count as a direction, not a result.
  (Computed 2026-10-23 with the standard pooled two-proportion sample-size formula, not a tool's output.)
  Check it with a calculator before quoting it.
- Before changing a price because conversion is low, split paywall conversion by acquisition source (each ad creative, organic post, search, referral).
  If one source converts far better than another at the same price, price is not the first suspect.
  Change price and traffic source in different weeks, because changing both at once hides which one moved the number.
  Source: one founder's X post and two agreeing replies (October 2026, no data), so this is a cheap check and not a finding.
- Change trial length, the trial reminder and the paywall timeline in different releases too.
  One build-in-public founder shipped all three in one release, and a reply pointed out they could not tell which one reduced cancellations (single reply, no data).

## When in doubt

Deliver the first win fast, then show the paywall in the same session.
RevenueCat's State of Subscription Apps 2026 (115,000+ apps) found 50.6% of download-to-paid conversions happen on Day 0 and 78-90% of trials start on Day 0, depending on category.
The same report found hard paywalls convert 10.7% download-to-paid by Day 35 vs 2.1% for freemium, with nearly identical one-year retention.
Moving the paywall late costs conversions, so A/B test placement instead of assuming later is better.

## Sources

- <https://developer.apple.com/app-store/review/guidelines/#in-app-purchase>
- <https://superwall.com/docs/campaigns-standard-placements>
- <https://www.revenuecat.com/docs/tools/paywalls/displaying-paywalls>
- <https://x.com/samuel_yostt/status/2109698766530048174>
- <https://x.com/frederickjames/status/2111137088871555182>
- <https://developer.android.com/google/play/billing/subscriptions>
- <https://www.revenuecat.com/state-of-subscription-apps>
- <https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026>
- <https://firstpagesage.com/seo-blog/saas-free-trial-conversion-rate-benchmarks/>
- <https://x.com/zzwitz/status/2109310052343644367> (quotes <https://x.com/zzwitz/status/2091879951897166069>)
- <https://firstround.com/review/the-tenets-of-a-b-testing-from-duolingos-master-growth-hacker/>
- <https://relaunch.ai/blog/duolingo-onboarding-teardown-7-b-tests-behind-their-9-conver.html>
- <https://www.appcues.com/blog/gradual-engagement-mobile-app-first-screen>
- <https://blog.duolingo.com/widget-feature>
- <https://revyl.com/atlas/duolingo/>
- <https://x.com/eglitisX/status/2112412118213640419>
- <https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-introductory-offers-for-auto-renewable-subscriptions/>
- <https://www.revenuecat.com/docs/integrations/webhooks/event-types-and-fields>
- <https://x.com/itsbongoo/status/2112401557946069175>
- <https://x.com/GeorgeLampro20/status/2112452949561463082>
- <https://x.com/zakisbuilding/status/2112823780821049807>
- <https://x.com/devmelv/status/2112632240593158297>
- <https://x.com/chddaniel/status/2112392363725537783> (quotes <https://x.com/chhddavid/status/2112113481495318700>)
