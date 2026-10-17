---
name: paywall-transparency
description: >-
  Use when designing or auditing in-app paywalls, trial flows, or subscription onboarding. Codifies the transparency-wins pattern, where explicit pre-paywall screens raise trial-to-paid conversion.
allowed-tools:
  - Read
  - Edit
  - Grep
metadata:
  docs-verified: "2026-09-28"
---

# Paywall Transparency

## Principle

Founders fear that reminding users about charge dates causes cancellations.
Opposite is true — users who want to cancel will cancel regardless. Users
who trust you convert at much higher rates.

## When to invoke

- New paywall or trial flow.
- A/B testing trial-start or trial-end variants.
- Conversion-rate drop in subscription apps.

## The 2 screens

1. **"Here's exactly what you get"** — concrete feature list with checkmarks,
   ≤7 items, plain language.
2. **"Here's exactly when you'll be charged"** — trial timeline: today free
   → reminder 2 days before charge → charge with localized price.

## Implementation checklist

- [ ] Trial-start screen lists features in plain language.
- [ ] Charge timeline visible BEFORE the App Store / web checkout modal.
- [ ] Reminder push/email scheduled 48h before charge.
- [ ] On a one-screen paywall, the trial line under the plan states the length, the charge with its period and the reminder ("7 days, then €29.99 a year. We remind you 2 days before."), and the reminder is actually scheduled.
- [ ] Settings → "Manage subscription" deep-link is one tap.
- [ ] Localized prices per storefront.

## Anti-patterns

- Hiding price until last screen.
- "Free trial" without showing duration.
- Charge happens silently with no pre-notice.
- Bait-and-switch pricing, meaning a price or trial shown on the paywall that differs from what checkout charges.
  Apple Developer Program License Agreement (ADPLA) Section 3.2 bans "bait-and-switch pricing", and the Developer Code of Conduct in Guideline 5.6 bans tricking users into unwanted purchases or raising prices "in a tricky manner".
  Neither text names paywalls, so applying them here is a reading of the rules.
  Guideline 5.6 says the developer account will be terminated for conduct that breaks the Code.

## Sources

- Steve P. Young, LinkedIn post: <https://www.linkedin.com/feed/update/urn:li:activity:7368447689010634755/>
- Emil Nilimaa, LinkedIn post: <https://www.linkedin.com/feed/update/urn:li:activity:7437905259609624576/>
- Apple App Review Guideline 3.1.2 (subscriptions and subscription information): <https://developer.apple.com/app-store/review/guidelines/#subscriptions>
- Apple Developer Code of Conduct (Guideline 5.6): <https://developer.apple.com/app-store/review/guidelines/#code-of-conduct>
- Apple Developer Program License Agreement, Section 3.2: <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>
- Google Play subscriptions policy (free trial disclosure and cancellation): <https://support.google.com/googleplay/android-developer/answer/9900533>
