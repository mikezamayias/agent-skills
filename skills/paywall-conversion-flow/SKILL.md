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
5. **Offer weekly + yearly, not just monthly.** Weekly lowers commitment fear and converts the "let me test it" segment that monthly scares off.

## Anti-patterns to remove

- Paywall on cold launch.
- "Subscribe to continue" gate before any value is delivered.
- Tutorial screens explaining features (vs showing outcomes).
- Yearly-only pricing with no escape hatch for low-trust buyers.

## Audit checklist (use before each release)

- [ ] First successful action happens within 30 seconds.
- [ ] Rating prompt fires after a clear win, never before.
- [ ] Paywall fires after a success event, not on launch.
- [ ] Plans visible: Weekly, Yearly, Lifetime (if applicable).
- [ ] Free trial CTA prominent; cancel path documented in-app.
- [ ] Restore Purchases link is on the paywall (App Review Guideline 3.1.1 requires a restore mechanism for restorable purchases, and the paywall placement builds trust).

## Onboarding flow reference

A high-performing onboarding structure to pair with the order above:

1. Splash → immediate account creation with one-tap social buttons plus a visible Skip.
2. Minimal account creation (pre-filled or one-tap).
3. Value screens with progress indicators and Skip.
4. Interest / goal selection (multi-select chips) so the experience feels tailored early.
5. Personalized recommendations or community previews based on the selections.
6. Soft premium upgrade with clear benefits and trial (this is the "after value" slot from the order above).
7. Celebration / "creating your space" animation → main app.

Execution details that matter: always a visible Skip or back, pre-select popular options to cut decision fatigue, show real social-proof numbers, keep the whole flow under 30-45 seconds. Track onboarding completion rate, time to first meaningful action, day-1 retention, and first-session conversion.

## When in doubt

Deliver the first win fast, then show the paywall in the same session.
RevenueCat's State of Subscription Apps 2026 (115,000+ apps) found 50.6% of download-to-paid conversions happen on Day 0 and 78-90% of trials start on Day 0, depending on category.
The same report found hard paywalls convert 10.7% download-to-paid by Day 35 vs 2.1% for freemium, with nearly identical one-year retention.
Moving the paywall late costs conversions, so A/B test placement instead of assuming later is better.

## Sources

- <https://developer.apple.com/app-store/review/guidelines/#in-app-purchase>
- <https://developer.android.com/google/play/billing/subscriptions>
- <https://www.revenuecat.com/state-of-subscription-apps>
- <https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026>
- <https://firstpagesage.com/seo-blog/saas-free-trial-conversion-rate-benchmarks/>
