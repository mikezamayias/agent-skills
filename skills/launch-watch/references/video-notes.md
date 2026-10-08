# Video notes: launch checklist and monitoring

## Source

- Title: "Launching something soon, this is my checklist AND how i monitor the launch"
- Creator: Chris Raroque
- URL: <https://www.youtube.com/watch?v=wFx1qYD8OsI>
- Share URL: <https://youtube.com/shorts/wFx1qYD8OsI>
- Published: 2026-10-07
- Duration: 65 seconds
- Reviewed from the YouTube transcript plus the creator's caption checklist.

No full copy is stored.
The notes below paraphrase the source.
The video is a paid partnership for OpenAI's always-on agent product.

## Core claim

Launch tooling only helps if someone acts on it, and the first two to three weeks after launch are when crashes, drop-off and feedback shape product decisions.
An always-on agent with the launch checklist and tool access can watch those signals, investigate anomalies and prepare fixes while the developer keeps building.

## Method kept

- **0:00-0:20:** Four launch channels: product analytics, crash reporting, a welcome email sequence, and an in-app feedback board.
  The caption adds that each must be tested before launch: events visible, a test error sent, email trigger, timing and links checked, and the board easy to find in the app.
- **0:20-0:35:** Tools are only useful if someone acts on them, so give a watcher the checklist, the launch date, what a successful signup looks like, and access to the tools.
- **0:35-0:55:** Worked case: analytics showed users not completing onboarding.
  With access to the code and server logs, the watcher traced it to a server bug that rendered one onboarding step blank, prepared a fix and opened a PR for review.
- **0:55-1:05:** The developer still reviews changes before they go live.
- **Caption:** The suggested instruction is to check daily for three weeks, flag urgent issues, deliver a weekly summary with evidence per suggestion, update the plan when dates or priorities change, and ask before changing code or sending email.

## Case-study numbers, not benchmarks

- The creator says it is their fifth app launch.
- The three-week window and daily cadence are the creator's choice, used here as defaults, not proven optimums.

## Limits of source

- No thresholds for what counts as urgent.
- No guidance on small samples, alert deduplication, PII in reports, credential scope, symbolication, email consent, or store reviews as a feedback source.
- No scheduler detail beyond the vendor product.

## Adaptation choices

- Product names (Dots, GPT-6 Astra, PostHog, Sentry, Loops, UserJot) replaced with capability requirements, defaulting to Sentry, PostHog, RevenueCat and `asc` where they are available.
- The vendor's always-on agent replaced with any persistent scheduler, with T3 `schedule_task` first and a warning that session-only cron jobs expire after 7 days.
- Derived, not claimed by the source: round-trip evidence per channel, symbolicated test crash, revenue and server-log channels, store reviews, default urgent triggers, small-sample reporting, one alert per problem, read-only credentials, PII-free reports, EU email consent, and the window close-out.
- Crash fixes defer to `proactive-crash-repair-loop`, which adapts an earlier short by the same creator.
- Pre-submission checks stay with `launch-readiness` and `store-launch-mastermind`.
