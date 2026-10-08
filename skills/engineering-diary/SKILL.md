---
name: engineering-diary
description: >-
  Keep a short daily engineering diary in Markdown so decisions, lessons and open loops survive between sessions. Use when starting or ending a coding session, reviewing the week, or returning to a project after a break.
---

# Engineering Diary

Context that lives only in your head or in a chat session is gone within days.
A short daily log in plain Markdown keeps what you shipped, what you learned and what is still open.
It takes about five minutes a day.

## Structure

Write one file per day, such as `diary/YYYY-MM-DD.md`, in a notes folder of your choice.
Use three sections:

```md
# YYYY-MM-DD

## What I shipped

- Fixed the login timeout.
- Cached dependencies in CI.

## What I learned

- `FlutterError.onError` handles framework errors and `PlatformDispatcher.instance.onError` handles errors outside Flutter callbacks.
- BLoC `restartable()` cancels the in-flight event when a new one arrives, which suits typeahead. `droppable()` ignores new events while one is in flight.

## Open loops

- Renew the expiring signing certificate.
- Update the README install steps.
```

## When to write

- Write at the end of each working session, without formatting or editing.
- At the start of the next session, read the previous entry's open loops first.
- Once a week, carry any open loop that is still open into a task list or drop it on purpose.

## For agents

- At the end of a session, offer to append the day's entry with what changed, what was learned and what is left.
- Write facts with evidence, such as a commit, a file or a link, not impressions.
- At the start of a session, read the latest entry before planning.
- Never put secrets, credentials or personal data in the diary.

## Tooling

Plain Markdown in any editor is enough.
Useful additions are a snippet for the template, a shell alias that opens today's file, and a weekly review that lists the week's open loops.
Keep it boring, because the tool that survives is the one with the least friction.
