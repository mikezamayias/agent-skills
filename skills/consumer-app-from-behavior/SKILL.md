---
name: consumer-app-from-behavior
description: >-
  Turns observed consumer behavior into a mobile app, from trend mining and teardowns to core loop and build spec. Use when looking for a consumer (B2C) app idea or deciding whether a trend is worth building on. Also use to define an app's core loop, turn references into an MVP spec, or decide whether a v1 is ready to ship.
---

# Consumer App From Behavior

Find a real behavior, turn it into one loop, borrow proven patterns, and ship the smallest version that tests whether anyone comes back.

The technical barrier to a v1 is low. The work that decides the outcome is choosing the behavior, the loop, and the return reason.

## Scope and handoffs

This skill covers discovery through a ship-ready spec.
Hand off where an existing skill goes deeper:

- Paid-pain validation, funnel events, and distribution experiments: `ship-first-dollar-app`.
- Gathering and critiquing reference screens for Flutter: `mobile-ui-reference`.
- Onboarding order and paywall placement: `paywall-conversion-flow`.

Build with the project's existing stack.
The source article promotes a specific AI app builder, and this skill does not depend on it.

## 1. Find demand before an idea

Do not brainstorm ideas from a blank page.
Watch people first, on TikTok, Reels, Shorts, Reddit, or app reviews.
Look for human behavior, not virality:

- Recurring complaints.
- Habits people are trying to quit.
- Insecurities and things people flex about.
- Things people obsessively track.
- New aesthetics, identities, and challenges.
- Skills people wish they had.
- Routines people keep sharing.
- Repeated requests for help.
- Behaviors that already need an annoying workaround.

Separate the trend from the problem under it.
Example: "underconsumption core" is the trend.
"I impulse-buy when stressed" and "I want to feel rewarded for not buying" are the problems.
Build for the problem, not the trend name.

Mine comments for unprompted requests such as "someone needs to make an app for this", "is there an app that does this", and "I wish something tracked this automatically".
Unprompted statements are stronger evidence than asking "would you use an app that does X".

Before committing to an idea, answer four questions:

- Are several competitors making serious money?
- How large are the biggest?
- What do their users dislike?
- Where do those companies find customers?

Then test whether distribution can shape the idea.
Can the app be shown in a 7 second clip, do users share its results, and does it suit before-and-after content?
These questions are the opinion of one promotional article (published 2026-10-19), unverified.

To learn which post format works in a niche, study format and not accounts.
List 100 or more public accounts in the niche.
Save each post's link, views, likes, saves, caption and slides.
Label each post for the traits you care about, such as hook type, number of slides, ending and app placement.
Compare only inside each account: posts with a trait against that same account's posts without it, and count in how many accounts the trait wins.
Require at least 2 posts with and 2 without per account.
Report the change in views and the accounts won, and drop rows with fewer than about 20 accounts.
One founder ran this over 13,196 posts for about 172 dollars, mostly LLM labeling, in 1.5 to 2 days elapsed time (self-reported, 2026-10-17, dataset unpublished).
The result shows correlation with views, so verify any finding with your own post before building on it.
Read only public pages and check the platform's terms and rate limits first.
For the per-post label list, see `ship-first-dollar-app` [references/tiktok-slideshow-format.md](../ship-first-dollar-app/references/tiktok-slideshow-format.md).

To size a category, read a studio portfolio page the same way, as a worked example.
One screenshot (2026-10-19, a third-party tool's 30-day estimate and not a reported figure) showed a studio with 27 sudoku, crossword and word search apps at about $1.1M and 1.7M downloads.
Check release dates first.
The top 4 apps carry about half the revenue, and 3 of those 4 date from 2017, so the earnings come from old titles.
Check how many new apps earn anything.
Of the 6 apps released in 2026, two earned $52.2K and $17.3K, and the other four earned $5.8K, $4.3K, $373.94 and $0.
Check revenue per download, which ranged from about $0.08 to $3.67 and averaged about $0.65 across the page.
The post's nationality and older-audience claims were not supported by the screenshot.
Replies say word, crossword and sudoku apps have been saturated for over a decade (single accounts, unverified).

Output: a list of candidate problems, each with the verbatim evidence and its source.

Views are not demand.
One founder reports 1.8 million creator views that produced 5 weekly subscriptions on an app he did not care about, and 1 million views that produced about 17,000 dollars on an app for his own sport.
His two retellings differ (1.5 million views and 15 dollars on a vendor page), so this is self-reported and inconsistent.
Use it only as a reason to check conversion per creative before buying more reach.

## 2. Pick a format

Most consumer apps fit one of three structures.

| Format         | Job                                                                                               | Value comes from                                            |
| -------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Tracker        | Turn invisible behavior into numbers (spending, sleep, mood, focus, sobriety).                    | Vague progress becomes a visible number.                    |
| Coach          | Help someone become a slightly different version of themselves (plans, daily missions, feedback). | It removes decisions by saying "do this next".              |
| Simple utility | Make one annoying thing pleasant (timer, list, journal, scanner, widget).                         | One feature used daily, with an experience that feels good. |

### Shareable creative format

Before launch, consider one proven reaction or reveal format from another product, with one element swapped for a polarizing or timely statistic your app can produce.
Creators then clone the format one for one.
One founder reports this for a camera-roll "wrapped" app with a "most toxic person" statistic, and says single videos reached 10 to 15 million views and that outside influencers copied the format.
This is a single unverified account from a video that promotes the founder's own tool, so test it as a hypothesis and not as a benchmark.
See `ship-first-dollar-app` for how many creators to start with.

## 3. Define the loop before code

State what the user repeatedly does, as one sentence of steps.
Examples:

- Spending: almost buy something, log it, resist, see money saved, feel progress, repeat.
- Fitness: open app, get today's workout, complete it, see progress, return tomorrow.
- Focus: choose task, start timer, finish session, extend streak, repeat.

If the loop does not fit one sentence, the app is too complicated.

Answer the five gate questions:

1. What makes someone download it? There must be one obvious promise.
2. What makes it understood in 10 seconds without a tutorial?
3. What is the first win, and how fast does it arrive?
4. What makes them open it tomorrow?
5. What is the single sentence loop above?

Question 4 is the one most often skipped.
Retention is the product, and downloads are not.

Name the one feature a viewer understands from a 3 to 5 second clip with no voiceover, for example "photo of food, get calories".
Lead every creative with that feature.
Push a second feature only after a creator's returns fall, and note the date and the return before and after.
Then hand the phone to someone who does not use apps for fun and ask what it does without helping.
If they cannot say, simplify the screen before spending on distribution.
Source: George Lampropoulos on the Startup Ideas Podcast, self-reported with no store data.

## 4. Borrow the patterns, not the pixels

Use 5-10 shipped apps around the same behavior.
They do not need to be direct competitors.
Install and use them, and capture: first launch, signup, onboarding, home, navigation, core action, empty states, progress, streaks, notifications, upgrade prompts, paywall, and settings.
For Flutter work, run this capture through `mobile-ui-reference`.

Record the decisions, not the styling:

- Where and how many questions onboarding asks.
- When the real product first appears.
- When notification permission is requested.
- When money is requested.
- Time to first win.
- What stays visible and what is hidden.
- What brings the user back tomorrow.

Use screenshots and reviews for the reasons behind a decision.
Use numbers only for what the data source contains, because a competitor's private conversion and retention are not visible.
A study of winning apps alone shows shared traits, not causes, so compare with failed apps or label the finding a hypothesis (the survivorship caveat, raised by a reply to the source below).

For each paywall, record every tier's name, price and billing period, the trial length, any discount claim, the exact CTA text, and whether it is hard or soft.
Convert every yearly and lifetime price to a monthly equivalent before comparing apps.
Capture the top, middle and bottom of a scrolling paywall, and read renewal terms and fine print from the full accessibility tree, including off-screen nodes.
When the paywall is not obvious, look under settings, subscription, profile and upgrade entries, or trigger a gated feature.
Note pre-selected expensive tiers, hard-to-find close buttons, a hidden Restore Purchases link and a price that changes between paywall and checkout as dark patterns.
Apple's license agreement bans bait-and-switch pricing, so do not copy that last pattern into your own app.

For a marketing teardown of a competitor, label each claim with one of four evidence labels.

- Observation: seen at a URL.
- Derivation: computed from observations.
- Inference: prefix it with "Likely".
- Unknown: not checked.

A negative claim needs a source that was checked and found empty.
A tracking pixel shows intent, not spend.
Never state a dollar spend that a source does not give, and use spend proxies such as active ads, ad longevity and launch rate instead.
Say "in the sample" for ad library counts.

Default patterns for younger consumer audiences:

- One obvious action per screen.
- Large type and little text.
- Visible progress, streaks, milestones, and satisfying numbers.
- Early personalization.
- Obvious feedback on completion.

Make progress impossible to miss.
Show the 7-day streak, the 18% improvement, and the $143 saved.
The user should always see that the app is working.

## 5. Write the build spec

Collect the idea, core user, promised outcome, loop, and reference captures.
Ask a model to produce the spec before any code, using this prompt:

> I'm building a mobile app that helps {user} achieve {outcome}. Study the attached references and break down their UX patterns, visual hierarchy, onboarding, navigation, and interactions. Redesign those patterns around my product. Define every MVP screen, what happens on each, the full onboarding journey, main navigation, the core user loop, and one mechanism that gives users a reason to return regularly. Remove anything not necessary for the first version. Finally, turn everything into a detailed build prompt.

Read the output, cut what is unnecessary, and add what it missed.
Then build from the spec and iterate with concrete directions, for example "move the paywall after the first result", "cut onboarding in half", or "make one action dominant on this screen".

During every iteration, check each screen against these questions:

- What does the user see first?
- What must they understand here?
- What is the single most important action?
- How fast do they reach the main benefit?
- Where could they get confused?
- What can be removed?
- What makes this satisfying?
- What gives them a reason to open it tomorrow?

Prefer these questions over requests for new features.

## 6. Make v1 good enough to charge for

Stop adding features once the core loop works.
Then work on three things only.

Onboarding:

- Deliver understanding and value within 30 seconds.
- Every screen must earn its place.
- Use every answer you collect.
- Explain every permission before asking.
- Defer anything that can wait.
- Do not copy a long onboarding because other apps have one.
- When auditing a flow, score each screen's friction from 1 (clear value, one tap) to 5 (confusing or hostile). A signup wall scores 4 even when well designed.
- Per screen, record what is asked, which permission is requested, the taps to advance and whether skip exists. Score every system permission dialog as its own screen.
- Per screen also judge whether the user sees what they get, whether a permission is requested at the moment of use or too early, whether progress is visible and whether the user can leave.
- Report the average friction score and the top 3 to 5 fixes ranked by impact.

Monetization:

- Place the paywall in the path of continuing a value the user has already felt, after a first result, session, or plan.
- Do not debate price points without data. Weekly plus annual is a normal starting shape, and it is tested later.
- Hand off to `paywall-conversion-flow` for details.

Polish by acting like a user:

- Start from a fresh account.
- Tap in odd orders.
- Deny permissions.
- Kill the app mid-onboarding and reopen it.
- Leave fields blank and use absurd inputs.
- Return the next morning.
- Hand it to someone without explanation and watch where they stall.

The goal is a finished-feeling loop, not a perfect app.

## 7. Ship before feeling ready

Ship when the core loop works.
Do not add social features, achievements, AI assistants, themes, or extra settings first.
v1 answers one question: does anyone want this?

After release, make content about the problem, send people to it, and watch:

- Onboarding drop-off.
- The share of users who reach the core action.
- Next-day and 7-day return.
- Who pays.
- What reviews say.

A useful early signal is 100 downloads with about 25 still opening the app a week later.
This comes from the source article and is a rule of thumb, not a benchmark.

Start with iOS and add Android only once the idea earns it.
Keep to one audience, one problem, one promise, and one loop.
Growing an app later is easy, but shrinking a 30-feature app is not.

## Output contract

Return:

1. Candidate problems, each with verbatim evidence and its source.
2. The chosen problem, its format, and the one-line promise.
3. The core loop sentence and answers to the five gate questions.
4. A reference teardown table with app, screen, decision, and why it works.
5. The MVP build spec, with the screen list, onboarding, navigation, the return mechanism, and non-goals.
6. A ship checklist covering loop complete, onboarding under 30 seconds, paywall after first value, and the polish pass done.
7. The post-launch metrics to watch.

Mark assumptions and missing evidence explicitly.
Do not invent demand, retention, or revenue numbers.

## Guardrails

- Do not build for a trend name. Build for the behavior under it.
- Do not treat hypothetical interest ("would you use") as demand.
- Do not copy visual styling as a substitute for understanding the decisions behind it.
- Do not ship a spec whose loop needs more than one sentence.
- Do not add features to delay shipping.
- Keep full rigor on auth, payments, privacy, and data loss, even in a fast v1.

## Sources

Adapted from David Ch's article _Jev studied 438,122 apps doing $10k/mo+ for me. The bar is stupidly low_: <https://x.com/chhddavid/status/2103052210904989770>.

The shareable creative format note comes from a founder's video: <https://x.com/Jibran_05/status/2111125040225735055>.

The gotcha-feature test and the reach-versus-revenue caution come from a podcast interview shared in a post, self-reported: <https://x.com/GeorgeLampro20/status/2112452949561463082>.

The within-account format comparison method comes from a founder's analysis, self-reported and unpublished: <https://x.com/ericcosulea/status/2112214949736898809>.

The studio portfolio example comes from one screenshot of a third-party estimate tool: <https://x.com/alexcooldev/status/2112218472709329038>.

The competitor teardown evidence labels come from the evidence contract of a third-party repo created about 2026-10-18 (29 stars on 2026-10-19), unverified: <https://x.com/danielhangan_/status/2111899646306230593>.

The pre-idea questions and the competitor-data limits come from a later X article by the same authors (published 2026-10-19), which promotes their own app builder, with figures that are unverified and no failed apps in its sample: <https://x.com/chhddavid/status/2112113481495318700>.

Read [references/article-notes.md](references/article-notes.md) when provenance or adaptation choices matter.
