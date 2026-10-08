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
- [ ] Settings → "Manage subscription" deep-link is one tap.
- [ ] Localized prices per storefront.

## Anti-patterns

- Hiding price until last screen.
- "Free trial" without showing duration.
- Charge happens silently with no pre-notice.

## Sources

- Steve P. Young, LinkedIn post: <https://www.linkedin.com/feed/update/urn:li:activity:7368447689010634755/>
- Emil Nilimaa, LinkedIn post: <https://www.linkedin.com/feed/update/urn:li:activity:7437905259609624576/>
- Apple App Review Guideline 3.1.2 (subscriptions and subscription information): <https://developer.apple.com/app-store/review/guidelines/#subscriptions>
- Google Play subscriptions policy (free trial disclosure and cancellation): <https://support.google.com/googleplay/android-developer/answer/9900533>
