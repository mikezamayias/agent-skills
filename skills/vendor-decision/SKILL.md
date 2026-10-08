---
name: vendor-decision
description: >-
  Choose or re-check a backend, API or service from live evidence, mapping its competitors and gatekeepers first. Use when picking a stack or provider, when a feature depends on third-party platform data, or auditing a provider. Also use when asked for alternatives to a provider or for a cost estimate.
metadata:
  provenance: local
---

# Vendor decision

Provider claims from memory go wrong in predictable ways:

- terms can restrict the intended use of an API
- a benchmark can measure the wrong path
- estimates from memory drift, sometimes by several times
- a vendor's minimum data retention can exceed what the privacy policy promises

This skill makes each claim come from a live source and puts the decision-maker's choice on one page.

## Step 1: Map the field

List every realistic option before comparing any of them.
The user should never have to ask "what about X?" about an option that was missing.

- **Direct providers:** the obvious ones, plus options native to the project's stack (for a Flutter or Dart app, Dart-native backends such as Serverpod), EU or self-hosted options when data location matters, and "build it ourselves".
- **Competitors of the provider a feature depends on.** If the feature needs data from one platform, also map the other platforms users actually keep that data on, including the operating system's own data store.
  Say which user segments each covers, for example users who reach that data only through a third-party app.
- **Gatekeepers:** whoever controls access even when the provider is willing.
  - platform rules: App Store and Google Play review guidelines, and platform data-access rules
  - API terms and developer agreements, including display, storage, AI-training, and competition clauses
  - partner-program approvals and rate-limit tiers
  - regulators, for example data-protection rules for sensitive data, or sector regulators
    Record which clause gates what, with a link.
- **Competing products:** apps already doing the same job.
  Note how they solved it, because it shows which integrations are realistic.

## Step 2: Verify on live sources

For each option, fetch the live page and quote the clause or number with its URL and the date you read it.

- Terms: what the data may be used for, whether it may be shown to other users, storage limits, AI use, attribution, and termination.
- Price: the listed price, what triggers usage charges, the free tier, the renewal price, and the minimum commitment.
- Limits: rate limits, quotas, and features only in paid tiers.
- Runtime limits: deploy or bundle size, memory, CPU time, and request duration, from the provider's main limits page and its changelog.
  Size these against the planned growth, not today's code, because a limit hit later splits the system along the limit instead of along the design.
- Data: the region where data is stored and processed, retention (the minimum and whether it can be shortened), whether a data processing agreement (DPA, the GDPR contract with a processor) exists, whether data is used for training, and sub-processors.
- Inputs and outputs: what the API accepts, such as text only or images, and in what formats.

When a source cannot be found, say "unverified" and name what would verify it.
Never present an assumption as a fact.
Never ask the user to look something up that a fetch could answer.

## Step 3: Cost by kind and scale

Break the cost down, per option, at three or more user counts (for example a small, a medium, and a large monthly user count):

- fixed monthly cost
- usage cost, with the unit and the assumption behind it
- one-off build hours, including porting existing code, with the basis for the estimate
- upkeep hours per month
- legal and compliance work, such as DPAs, policy changes, and security reviews
- exit cost: what leaving would take

Give best, typical, and worst cases where the uncertainty is real.
State the evidence for every estimate, and say which figures are guesses.

## Step 4: Measure what the decision depends on

When performance matters, measure the path the decision depends on, not the easiest path to measure.
Latency to a CDN edge serving public data says nothing about authenticated writes to the primary database.
If you chart anything, chart that metric, and label the chart with what it does not show.

## Step 5: Recommend

End with one recommendation, covering:

- the concrete flow the user or the team gets
- the monthly cost range
- the harm it avoids
- what would make you switch, as a staged plan with triggers (for example, "move `<component>` to X past `<N>` monthly users")

If a gatekeeper blocks the preferred option, say so first and give the best route around it.
Put the choice on an answer sheet (see `answer-sheet`) when it is one of several open decisions.

## Output

- the field map: providers, competitors, gatekeepers, and competing products
- the evidence table, with the claim, source URL, date read, and quote
- the cost table by kind and scale
- measurements, if any
- the recommendation and switch triggers
- unverified items and what would verify them

## Pitfalls

- A first estimate stated confidently gets anchored on.
  Give ranges until they are verified.
- An earlier approval does not survive new evidence.
  If a gatekeeper clause invalidates an approved design, say so plainly and bring it back for a decision.
- Correct your own earlier wrong claims explicitly, naming what was wrong.
