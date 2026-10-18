---
name: ship-first-dollar-app
description: >-
  Validates and monetizes solo-built apps: proves paid pain, scopes a one-feature MVP, instruments revenue, ships fast. Use when evaluating an app idea, defining a first-revenue MVP, planning a launch sprint or auditing funnel evidence. Also use when deciding what to build, market, stop or scale after launch.
---

# Ship First-Dollar App

Turn an app idea or early product into a bounded evidence loop: paid problem → focused solution → real usage → first payment → measured iteration.

## Intake

Ask for or infer:

- Target user and painful job.
- Current workaround, substitutes, and paid competitors.
- Proposed differentiator and monetization model.
- Build deadline, budget, platform, and available distribution channels.
- Current product state, bugs, requests, funnel data, and channel data.

State missing evidence. Do not invent conversion, retention, pricing, or market facts.

## Workflow

### 1. Prove paid pain

- Treat existing paid competitors as demand evidence, not automatic disqualification.
- Identify buyer, painful moment, current spend or costly workaround, and narrow differentiation.
- Distinguish personal enthusiasm from willingness-to-pay evidence.
- Produce a build, research, or reject decision.

Pass gate only when problem is painful and payment evidence or strong substitute spend exists.

### 2. Define one-feature wedge

- Choose one feature that completes one valuable user outcome.
- Express core loop as: trigger → action → result.
- Describe clearest, most satisfying result as a 5–15 second demo.
- Set non-goals. Remove adjacent workflows, imagined scale, and broad parity.

If value cannot be demonstrated clearly, rescope before coding.

### 3. Set build boundary

- Write small spec, acceptance scenario, deadline, and ship criteria.
- Use AI to accelerate planning and implementation, but understand generated code.
- Apply full rigor to auth, payments, privacy, secrets, data loss, and destructive operations.
- Use lighter process only for reversible experiments.
- Avoid architecture designed for demand not yet proven.

### 4. Instrument money path

Define and verify events for:

1. Visit or install.
2. Activation.
3. Core action completed.
4. Trial or checkout started.
5. Payment completed.
6. Retained, cancelled, or refunded.

Attach channel and creative attribution. Verify event delivery before buying traffic.

### 5. Ship to real users

- Ship when core action works and sensitive paths pass review.
- Collect evidence against original assumptions.
- Do not wait for a broad feature set or speculative scalability.
- Treat listing or website publication as availability, not distribution.

### 6. Run bounded distribution experiments

- Test at least three creative angles: pain-first, product demo, and wildcard.
- Separate active outreach from intent-based paid acquisition.
- Start with small, trusted audiences and bounded spend.
- Log outreach volume, replies, placements, spend, traffic, trials, payments, refunds, and revenue.
- Feed winning hooks and objections into next creative variants.
- Before paying creators, post the angles yourself on short video platforms, and hire creators only after a format has won.
- For an iOS app, run the first intent-based test on Apple Ads with [references/apple-ads.md](references/apple-ads.md).
- For Meta and TikTok campaigns, creator marketplaces, Reddit, Discord, YouTube Shorts and influencer deals, read [references/distribution-channels.md](references/distribution-channels.md).
- On Reddit, help in the community first and follow each subreddit's own self-promotion rule, because moderators set local limits and Reddit's spam rules ban mass-posting repetitive content for exposure or financial gain.
- Disclose any creator who is paid by revenue share, commission or cash, inside the video itself.

Do not scale a creator, ad, or channel without attribution and acceptable unit economics.

Keep an ad running while its cost per acquisition (CPA, the cost of one paying user) stays below lifetime value (LTV, net proceeds per paying user) within a payback window and spend cap set in advance, such as 6 or 12 months.
An ad just above that line may run through its learning period under the cap, then stops if it does not cross the line.
Write the inequality as CPA below LTV and never let a loss run without a window and a cap.

### 7. Reallocate work weekly

Allow product work when evidence shows:

- A bug blocks core value or payment.
- Multiple target users request same improvement.
- Funnel data identifies a specific conversion blocker.

Otherwise prioritize distribution, conversion, and buyer learning. End each review with one of: fix, market, revise, scale, pause, or stop.

## Decision Metrics

Track only metrics that change decisions:

- Days to first user, first payment, and first ten payments.
- Visit/install → activation.
- Activation → core action.
- Core action → trial/checkout.
- Trial/checkout → paid.
- Paid retention, cancellations, refunds, and churn.
- Outreach volume, reply rate, and reply → placement rate.
- Spend, CAC, revenue, ROAS, and payback by channel.
- Bugs and repeated requests by frequency and revenue impact.
- Product time versus distribution time.

Do not mistake revenue, downloads, replies, or impressions for profitability.

## Output Contract

Return:

1. Market-evidence brief and build gate.
2. One-feature MVP spec with non-goals.
3. Demo statement and core-loop acceptance scenario.
4. Funnel event map.
5. Channel and creative experiment ledger.
6. Ranked next-action queue.
7. Weekly fix/market/revise/scale/stop decision.

Make assumptions, missing evidence, owner, deadline, budget cap, and success threshold explicit.

## Guardrails

- Do not demand novelty when existing buyers prove market demand.
- Do not use more features as substitute for distribution.
- Do not apply casual vibe-coding standards to sensitive paths.
- Do not buy traffic before attribution works.
- Do not scale from one anecdote or one creative.
- Do not restart creative ideation from zero; reuse measured learning.
- Do not copy case-study benchmarks as universal targets.

## Apple account risk

Running several apps from one template in one Apple developer account puts the account at risk, not only each app.
Guideline 4.3(a) bans multiple Bundle IDs of the same app and advises considering one app with the variations sold through in-app purchase.
Guideline 4.3(b) says repeated submissions of low-effort, indistinguishable apps may lead to removal from the Apple Developer Program.
One developer kept his account only after cutting his portfolio to one app per category, and now also ships to Android, the web and macOS so that one account decision cannot remove all revenue.
That is one account, not Apple policy, so treat it as a reason to consolidate early rather than as a safe app count.

## Sources

Distilled from Cole Caccamise's video _How I Code Apps SOLO That ACTUALLY MAKE MONEY (Full Guide)_: <https://www.youtube.com/watch?v=WoKmZNN6qLo>.

Read [references/video-notes.md](references/video-notes.md) when provenance, case-study numbers, timestamps, or adaptation choices matter. Keep normal execution on this file's workflow.
