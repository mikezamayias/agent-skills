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
- Before charging a developer audience, search GitHub for an open source clone of the product and read its README setup time and update path.
  A clone that deploys on a free tier and is built with an AI coding agent can undercut a paid tool within a day, so write down what you sell that the clone does not, such as hosting, updates, support or a non-technical buyer.
  This is a screening step based on one case (inference), not a result.
- Identify buyer, painful moment, current spend or costly workaround, and narrow differentiation.
- Distinguish personal enthusiasm from willingness-to-pay evidence.
- Produce a build, research, or reject decision.
- For an iOS idea, check search demand before building by listing the candidate's App Store keywords with a keyword tool (Astro is a paid third-party tool, and any install or MCP use goes through the code-gate rule) and noting popularity, difficulty and the age of the data.
  A low difficulty score alone is not demand evidence, because it can mean nobody searches for the thing.
  Read the live top 10 for each keyword, and carry only the keywords that have paid apps in the top 10 into the Apple Ads test in `references/apple-ads.md`.
  The "low difficulty plus existing demand" method comes from one unproven post (X, October 2026) that reports no results, so treat it as a screening idea and not as a result.

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

#### Where the funnel is stuck

Name the highest tier the content reaches, and the missing metric says what to fix next.
The tiers are one author's framework with no data behind them, from an article that promotes the authors' own app builder (published 2026-10-19), so use them as a checklist and not as a benchmark.

| Tier | Reached              | Missing metric, fix next                                            |
| ---- | -------------------- | ------------------------------------------------------------------- |
| 0    | Low views            | Views. Fix the hook.                                                |
| 1    | Views                | Engagement. Fix the demo and the first seconds.                     |
| 2    | Views and engagement | Downloads. Fix the call to action and how fast the product appears. |
| 3    | Plus downloads       | Conversions. Fix onboarding and the paywall.                        |
| 4    | Plus conversions     | Low churn. Fix retention in the product.                            |
| 5    | Plus low churn       | Nothing missing. Scale what survived the whole funnel.              |

Views and engagement are not buying intent.
The article says 5 million views can earn less than 100 thousand views from the right audience, without data.

### 5. Ship to real users

- Ship when core action works and sensitive paths pass review.
- Collect evidence against original assumptions.
- Do not wait for a broad feature set or speculative scalability.
- Treat listing or website publication as availability, not distribution.
- A site is availability. A site with queries, comparison pages and crawler access is an owned acquisition channel, measured by GA4 AI-assistant sessions and Search Console, see `app-landing-page/references/seo-and-ai-answers.md`. Check results after four weeks before counting it as distribution. The outcome is unmeasured.

### 6. Run bounded distribution experiments

- Test at least three creative angles: pain-first, product demo, and wildcard.
  - For slideshows, also test two variables on the same angle: the last slide (no CTA against "save this + follow") and the app's slide (not shown, or after slide 6). Evidence is weak, one correlation study plus contrary replies.
- Separate active outreach from intent-based paid acquisition.
- Start with small, trusted audiences and bounded spend.
- Log outreach volume, replies, placements, spend, traffic, trials, payments, refunds, and revenue.
- Judge a post format by installs per post, not by views.
  Give each post or creative a way to be attributed, such as a distinct link, custom product page or promo code, or at least log app-page taps and installs against the post's post time.
  A format that raises views can lower installs.
  Public format studies measure views only.
- Before spending on content, tap the bio link from inside the TikTok and Instagram apps on a real iPhone and a real Android phone, and confirm the store page opens.
  A store link can fail inside those apps' in-app browsers, see the link-in-bio notes in [references/distribution-channels.md](references/distribution-channels.md).
  Log taps on the bridge page against App Store page views so the leak is measured.
  This check is an inference from one founder's claim and is untested.
- Feed winning hooks and objections into next creative variants.
- Before paying creators, post the angles yourself on short video platforms, and hire creators only after a format has won.
- Before the first post, write down how many posts and what view or install threshold count as honest testing, and drop the format if it misses.
  One founder says to kill a format that does not move after honest testing but gives no threshold (October 2026, no data), so the number is yours to set.
- For TikTok photo slideshows, read [references/tiktok-slideshow-format.md](references/tiktok-slideshow-format.md) before writing posts.
- For a game, wait for a day-1 return number before pushing organic clips, using the retention signal in `consumer-app-from-behavior` section 7. The day-1 timing is one reply's assertion.
- For game ad creative and the cross-promotion note, read the Games section of [references/distribution-channels.md](references/distribution-channels.md).
- For an iOS app, run the first intent-based test on Apple Ads with [references/apple-ads.md](references/apple-ads.md).
- For Meta and TikTok campaigns, creator marketplaces, Reddit, Discord, YouTube Shorts and influencer deals, read [references/distribution-channels.md](references/distribution-channels.md).
- For App Store Connect organic work that costs no media spend, read the In-App Events section of [references/distribution-channels.md](references/distribution-channels.md), and choose new locales from territory data in App Analytics.
- For a product that already has a paid web workflow, test an MCP-backed ChatGPT plugin as a channel only after reading the plugin section of [references/distribution-channels.md](references/distribution-channels.md), and log listing approval time, plugin-attributed sign-ups and revenue per sign-up like any other channel.
- On Reddit, help in the community first and follow each subreddit's own self-promotion rule, because moderators set local limits and Reddit's spam rules ban mass-posting repetitive content for exposure or financial gain.
- Disclose any creator who is paid by revenue share, commission or cash, inside the video itself.

Do not scale a creator, ad, or channel without attribution and acceptable unit economics.

Run paid only on concepts that already won organically, and measure cost per install, install-to-trial and trial-to-paid per campaign.
This order is the opinion of one article (published 2026-10-19).
Its sequence of 1,000 dollars buying 500 installs, 50 trials and 20 payers is an illustration and not data.

Keep an ad running while its cost per acquisition (CPA, the cost of one paying user) stays below lifetime value (LTV, net proceeds per paying user) within a payback window and spend cap set in advance, such as 6 or 12 months.
An ad just above that line may run through its learning period under the cap, then stops if it does not cross the line.
Write the inequality as CPA below LTV and never let a loss run without a window and a cap.
Write the stop rule for each ad before launch: the spend, the number of days and the CPA line.
Apply it only when the ad reaches that spend or those days, and do not pause an ad for a quiet morning.
One founder reports pausing ads that were profitable over several days (October 2026, X article, single report, no figures).
Set the CPA line below expected net value to leave room for error, for example half of the net proceeds expected in the payback window.
Count trial conversion, retention, refunds and store fees in that net figure.
One founder's X article (October 2026) gives $40 net and a $20 CPA line as an illustration and not a measured rule.

### 7. Reallocate work weekly

Allow product work when evidence shows:

- A bug blocks core value or payment.
- Multiple target users request same improvement.
- Funnel data identifies a specific conversion blocker.

Otherwise prioritize distribution, conversion, and buyer learning. End each review with one of: fix, market, revise, scale, pause, or stop.

When funnel data shows most installs leave before the paywall, spend the week on onboarding and the paywall before adding traffic.
One founder's order was onboarding from analytics data, then a second paywall offer, then more content, and their own result was +$30 MRR in a day on a one-month-old app (X post, October 2026, author claim, no control), which is an anecdote and not a test.

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
- Reported early heuristics from one founder, not benchmarks: start reading conversion at about 100 downloads a day, and aim for about 2 dollars of revenue per download in month one.
  Expect a lower figure from broad UGC reach and a higher one from creator posts that explain the app.
  If retention is poor, add useful adjacent features and measure churn before and after.
  A second founder says to put acquisition ahead of funnel and paywall work until about 300 downloads a day, unless something is obviously broken, and says "that isn't a magic testing threshold" (October 2026, X article, no data).
  The same founder earlier said to leave pricing alone until 500 downloads a day.
  Treat 100, 300 and 500 as three unsourced guesses, and size the real threshold from the sample sizes in `paywall-conversion-flow`.

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
A second reported data point, secondhand and unverified (article published 2026-10-19): an app called Journable passed 100 thousand dollars a month in the crowded calorie tracking category, with most of that revenue reportedly from Android.

An Android release is an extra revenue channel only after the Play account gate in `gplay-console` is cleared, so weigh the cost of a company registration against 14 days of testing.
An organization account may avoid the test, unconfirmed by Google.
The source gives no Android revenue figure, and one reply saying Android subscriptions exceed iOS for that developer is anecdotal.

## Sources

Distilled from Cole Caccamise's video _How I Code Apps SOLO That ACTUALLY MAKE MONEY (Full Guide)_: <https://www.youtube.com/watch?v=WoKmZNN6qLo>.

The bio-link check comes from a founder's post (2026-10-20), unverified: <https://x.com/MaxHirsch13/status/2112626598524465296>.

The kill-rule note comes from a founder's post (2026-10-20), unverified, whose author has a commercial interest in TikTok tooling: <https://x.com/devmelv/status/2112632240593158297>.

The funnel tiers, the paid-after-organic order and the Journable figure come from an X article promoting the authors' own app builder, with figures that are unverified and a study of winners only: <https://x.com/chhddavid/status/2112113481495318700>.

Read [references/video-notes.md](references/video-notes.md) when provenance, case-study numbers, timestamps, or adaptation choices matter. Keep normal execution on this file's workflow.
