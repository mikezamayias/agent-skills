---
name: consumer-app-from-behavior
description: >-
  Turn observed consumer behavior into a focused mobile app, from trend mining and teardowns to core loop and build spec. Use when looking for a consumer (B2C) app idea or deciding whether a trend is worth building on. Also use to define an app's core loop, turn references into an MVP spec, or decide whether a v1 is ready to ship.
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

Output: a list of candidate problems, each with the verbatim evidence and its source.

## 2. Pick a format

Most consumer apps fit one of three structures.

| Format         | Job                                                                                               | Value comes from                                            |
| -------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Tracker        | Turn invisible behavior into numbers (spending, sleep, mood, focus, sobriety).                    | Vague progress becomes a visible number.                    |
| Coach          | Help someone become a slightly different version of themselves (plans, daily missions, feedback). | It removes decisions by saying "do this next".              |
| Simple utility | Make one annoying thing pleasant (timer, list, journal, scanner, widget).                         | One feature used daily, with an experience that feels good. |

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

Read [references/article-notes.md](references/article-notes.md) when provenance or adaptation choices matter.
