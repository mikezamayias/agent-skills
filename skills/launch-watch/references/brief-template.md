# Launch watch brief template

Copy into the project as `docs/launch-watch.md`.
The scheduled watch reads this file on every run, so keep it current.
No secrets, user names, emails or user IDs belong here.

## Launch

- App and platforms:
- Release versions under watch:
- Launch date:
- Watch window: launch date to launch date + 21 days
- Approver: the user

## Activation

- Activation event (what a successful signup looks like):
- Funnel, in order: install or signup -> ... -> activation event
- Return events: day 1, day 7

## Channels

| Channel            | Tool                | Read access for the watch | Round-trip test                               | Evidence | Status |
| ------------------ | ------------------- | ------------------------- | --------------------------------------------- | -------- | ------ |
| Analytics          |                     |                           | Funnel fired from a release-like build        |          |        |
| Crashes and errors |                     |                           | Test error from a release build, symbolicated |          |        |
| Lifecycle email    |                     |                           | Welcome sequence to a test address            |          |        |
| In-app feedback    |                     |                           | Test submission                               |          |        |
| Store reviews      | `asc`, Play Console |                           |                                               |          |        |
| Revenue            |                     |                           | Sandbox purchase                              |          |        |
| Server logs        |                     |                           |                                               |          |        |

## Baseline

Pre-launch or beta numbers per metric, each marked with its sample size.

## Thresholds

Default urgent triggers live in the skill.
Override them here with numbers once the baseline exists, for example a crash-free session rate floor or a funnel step completion floor.

## Approval rules

The watch may read every channel above and prepare fixes on branches or draft PRs.
It asks before code merges, deploys, emails, user replies or price changes.

## Log

One entry per flagged problem: date first seen, channel, summary, evidence, status, last update.
Update entries in place instead of adding duplicates.
