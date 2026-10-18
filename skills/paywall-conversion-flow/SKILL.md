---
name: paywall-conversion-flow
description: >-
  Design value-first onboarding and paywalls that convert in freemium iOS or Flutter apps. Use when adding or auditing IAP, RevenueCat paywalls, free trial flows or onboarding screens.
metadata:
  docs-verified: "2026-09-28"
---

# Paywall Conversion Flow

The single biggest lever in a freemium app is the first 30 seconds and the placement of the paywall.
Most indies lose conversion by following the wrong order.

## The Order That Works

1. **Show value before asking for anything.** Skip the tutorial. Drop the user into a working "test project" or pre-filled state so they feel a win in <30s.
2. **Rating prompt BEFORE paywall.** Asking for a rating after a "win moment" captures the 5-star sentiment. If you flip the order, users 1-star you out of spite the second they see pricing.
3. **Hard paywall AFTER a success event** — never on launch, never on tab switch. Wait for: streak day 3, first export, first AI generation, first item saved.
4. **Free trial requires card on file.** It removes freeloaders and raises trial-to-paid conversion.
   In First Page Sage's SaaS benchmark (86 companies, 2022-2025), card-required trials converted 48.8% to paid vs 18.2% for cardless, but visitor-to-trial fell from 8.5% to 2.5%, so judge the whole funnel, not trial-to-paid alone.
   Make the cancel path easy to keep ratings intact.
   Google Play already verifies a valid payment method before a store free trial starts, so a cardless trial only exists outside store billing.
   Judge a trial by paid conversion, not trial-start rate.
   One indie fasting app in October 2026 reported a 20% trial-start week with zero trials converting, while its no-trial weeks reached 12-19% paid, on samples in the tens.
   The founder's own explanation, which he did not test, is that paid ads optimized on trial starts find users who start trials and never pay.
5. **Offer weekly + yearly, not just monthly.** Weekly lowers commitment fear and converts the "let me test it" segment that monthly scares off.
6. **Add one exit offer after the buyer cancels the store purchase sheet.**
   Superwall's `transaction_abandon` placement fires when a user dismisses the store purchase sheet before the transaction completes, and a matching paywall replaces the current one.
   RevenueCat's closest feature is Exit offers, which show a second paywall when the user dismisses the paywall without buying.
   Its docs do not say it fires on a cancelled purchase sheet, and it works only with `presentPaywall` or `presentPaywallIfNeeded`, so it is not shown to be equivalent.
   One indie fasting app shows a single discounted yearly plan with a close button, a 5 minute timer and the real billed price, and its author reported that the exit paywall produced 23% of its results over two weeks (author's figure, unit not stated, not verified).
   A second founder adds the offer in a follow-up release, after the base paywall is live.
   Ship it in a reviewed update, describe it in Notes for Review, and measure it on its own line so the base paywall rate stays clean.
   Never mention it in What's New, because that text is public and shows the offer to every user.

## Anti-patterns to remove

- Paywall on cold launch.
- "Subscribe to continue" gate before any value is delivered.
- Tutorial screens explaining features (vs showing outcomes).
- Yearly-only pricing with no escape hatch for low-trust buyers.
- Paragraphs on the paywall. Keep each plan to a price, a period and one concrete line.
- Abstract value claims. Anchor the price to something real instead ("€49 is three takeaways").
- Fake countdowns or a price that only appears after tapping.
- A one-time offer whose claims are not true. A countdown offer is legitimate only when the shown state persists so the offer never reappears for that user, the timer does not reset on reopen or relaunch, and claims such as "lowest price we've offered" are true for that storefront's price history.
  In the EU, Annex I point 7 of the Unfair Commercial Practices Directive (2005/29/EC) bans in all circumstances, with no harm test, falsely stating that a product will only be available for a very limited time in order to elicit an immediate decision.

## Audit checklist (use before each release)

- [ ] First successful action happens within 30 seconds.
- [ ] Rating prompt fires after a clear win, never before.
- [ ] Paywall fires after a success event, not on launch.
- [ ] Plans visible: Weekly, Yearly, Lifetime (if applicable).
- [ ] Free trial CTA prominent; cancel path documented in-app.
- [ ] Restore Purchases link is on the paywall (App Review Guideline 3.1.1 requires a restore mechanism for restorable purchases, and the paywall placement builds trust).

## Onboarding flow reference

A high-performing onboarding structure to pair with the order above:

1. Value screens or an instant first win, with progress indicators and Skip.
2. Goal and motivation questions ("why are you here?", multi-select chips) so the experience feels tailored early.
3. Personalized result, recommendations or community previews based on the answers.
4. Optional account creation, one-tap social or pre-filled, with a visible Skip.
5. Soft premium upgrade with clear benefits and trial (this is the "after value" slot from the order above).
6. Celebration / "creating your space" animation → main app.

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

## Measure

- Paid conversion is weekly unique buyers divided by unique paywall viewers.
- Keep trial starts on a separate line and never count them as paid.
- Bucket weekly when daily paywall views are under about 20, because daily rates are noise.
- Annotate every price, offer and onboarding change on the chart, and exclude the developer's own country or test devices.
- Never report a partial-week point as a result.
  One indie's chart headlined a dashed, incomplete week at 22.2%.
  An earlier capture of the same chart read 14.1% for its then-partial point against 12.2% once the week completed, an inference from two captures with unconfirmed week boundaries.
- Report a 95% interval with each rate. For example, 23 buyers out of 104 viewers is 22% with a range of about 15-31%.

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
