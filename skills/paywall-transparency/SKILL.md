---
name: paywall-transparency
description: >-
  Codifies the transparency-wins pattern, where explicit pre-paywall screens raise trial-to-paid conversion. Use when designing or auditing in-app paywalls, trial flows, or subscription onboarding.
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
- [ ] A win-back or retention offer states the price after the offer ends, the billing period and the renewal date, the same as any trial.
- [ ] On a one-screen paywall, the trial line under the plan states the length, the charge with its period and the reminder ("7 days, then €29.99 a year. We remind you 2 days before."), and the reminder is actually scheduled.
- [ ] If the user picks the reminder lead time, ask on a screen before the paywall, and the paywall timeline shows the chosen day.
      Seen in one gym app recording (X post, 2026-10-23), with no notification prompt shown and no effect on conversion or cancellations reported.
- [ ] Settings → "Manage subscription" deep-link is one tap.
- [ ] The account or settings page states the current plan, when it ends, whether it renews and who bills it.
      One planner (walked on a device, 2026-10-30) shows the trial's end date followed by "then renews", and "Your trial is billed through Apple. Manage or cancel it in Apple Subscriptions." with a one-tap button, and during free days granted outside the store it says "There's nothing to pay, and nothing can charge you at the end."
- [ ] Localized prices per storefront.

## Anti-patterns

- Hiding price until last screen.
- "Free trial" without showing duration.
- Charge happens silently with no pre-notice.
- Bait-and-switch pricing, meaning a price or trial shown on the paywall that differs from what checkout charges.
  Apple Developer Program License Agreement (ADPLA) Section 3.2 bans "bait-and-switch pricing", and the Developer Code of Conduct in Guideline 5.6 bans tricking users into unwanted purchases or raising prices "in a tricky manner".
  Neither text names paywalls, so applying them here is a reading of the rules.
  Guideline 5.6 says the developer account will be terminated for conduct that breaks the Code.
- A crossed-out reference price or a "SAVE x%" badge whose comparison the screen does not state.
  Apple's subscriptions page says a savings figure compared with weekly or monthly plans should be "displayed in a subordinate position and size" to the billed amount, and Guideline 2.3.1(a) lists "promoting a false price" as grounds for removal (Apple pages, read 2026-10-25).
  Example from one X thread (single report): "SAVE 88%" on a $39.99 yearly plan beside a $6.99 weekly plan.
  The weekly price over 52 weeks is $363.48 and the true saving is 89.0%, while 88% matches a 48-week year, so the badge uses an unstated period (arithmetic).
  A reply shows a lifetime plan at $39.99 with a struck-through $363.48, which is 52 weeks of the weekly plan, a price no plan on that screen charges as a single amount.
  State the comparison in words next to the figure, and compute it from the real billing period.
- A low introductory price shown much larger on screen than the renewal price, on a plan that renews weekly.
  Apple's Guideline 5.6.4 names "excessive refund requests" among the signs of poor quality and says poor quality "may be a factor" in judging conduct under the Developer Code of Conduct, with no threshold (Apple guidelines, read 2026-10-24).
  It does not name intro offers, so reading it as a rule against this pattern is an inference.
  One reply in an X thread (single report) says Apple counts refund spikes against an account, which is stronger than the text.
  Guidelines 3.1.2, 5.6 and 5.6.4 set no size rule for an intro price against the renewal price.
  Apple's Auto-renewable Subscriptions page does require the "Full renewal price, shown clearly and prominently" on the sign-up screen.
  It also says "the amount that will be billed must be the most prominent pricing element in the layout" and that a breakdown price or a savings figure should be "displayed in a subordinate position and size" to the annual price (Apple page, read 2026-10-25).
  For a pay as you go intro offer the amount billed at purchase is the intro price, so the page does not settle the relative size of the two numbers (inference).
  A layout that makes the intro price the largest number and the renewal price small and grey rests only on the "Full renewal price, shown clearly and prominently" requirement, and a reviewer can read it either way (inference).
  One reply in an X thread (single report, 2026-10-24) predicts a flag for this exact layout, and another reports rejections "for way less" (single report).
  Keep the renewal price as legible as the introductory price and track refund rate per plan.

Do not treat another developer's "it passed review" as proof that a paywall is allowed.
One reply describes reviewers as inconsistent (X reply, 2026-10-24, single report), and a thread of 12 replies showed no Apple message or screenshot approving the layout in question.
Apple's Guideline 5.6 says "repeated manipulative or misleading behavior" will lead to removal from the Apple Developer Program, so a passed review does not clear the layout (Apple guidelines, read 2026-10-25).
Judge a paywall against the Apple text in this file, and record the review outcome as one datapoint.

## Sources

- Steve P. Young, LinkedIn post: <https://www.linkedin.com/feed/update/urn:li:activity:7368447689010634755/>
- Emil Nilimaa, LinkedIn post: <https://www.linkedin.com/feed/update/urn:li:activity:7437905259609624576/>
- Apple App Review Guideline 3.1.2 (subscriptions and subscription information): <https://developer.apple.com/app-store/review/guidelines/#subscriptions>
- Apple Developer Code of Conduct (Guideline 5.6): <https://developer.apple.com/app-store/review/guidelines/#code-of-conduct>
- Apple Developer Program License Agreement, Section 3.2: <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>
- Google Play subscriptions policy (free trial disclosure and cancellation): <https://support.google.com/googleplay/android-developer/answer/9900533>
