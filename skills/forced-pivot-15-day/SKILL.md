---
name: forced-pivot-15-day
description: >-
  Sequence a 1 to 3 week pivot forced by an external constraint so it ships before the launch is killed. Use when an App Store guideline change, RevenueCat policy, regulatory deadline or paywall rejection forces a pivot. Based on Emil Nilimaa (Minglify), whose 15-day rewrite followed Apple guideline 1.2.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - AskUserQuestion
---

# Forced Pivot — 15-Day Sprint

## Trigger

External event with hard deadline that breaks current monetization or
distribution.

## Sequence

| Day   | Phase                | Output                                           |
| ----- | -------------------- | ------------------------------------------------ |
| 0     | Triage               | Single doc: what broke, what changes, what stays |
| 1     | Cut surface          | Remove offending feature behind a flag           |
| 2-3   | Rebuild monetization | New paywall + ASO drafted                        |
| 4-7   | Onboarding rewrite   | Replacement feature for top-of-funnel            |
| 8-10  | A/B variants         | 2 variants live; promo/screenshots updated       |
| 11-13 | Submit + iterate     | Submit, fix rejections same-day                  |
| 14-15 | Buffer               | Reserved for unknown rejection                   |

## Heuristics

- Patch the wound; rewrite later.
- Monetization first, polish last.
- One A/B test at a time during a pivot.
- Cap overtime. A pivot sprint is not a reason to burn out.

## When NOT to use

- Speculative pivot. Use only with external clock.
- Pre-traction products.

## Source

- urn:li:activity:7437905259609624576 (Emil Nilimaa)
