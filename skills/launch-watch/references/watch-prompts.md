# Watch prompts

Fill the placeholders and paste into the scheduler.
Both prompts point at the brief so a changed brief changes the watch without editing the schedule.

## Daily

```text
Run the launch-watch daily check for <app>.
Read docs/launch-watch.md first and follow its channels, thresholds, approval rules and log.
Check each channel for what is new or worse since the last run.
Investigate every urgent item down to a cause, using the code and server logs.
Prepare fixes on a branch or as a draft PR only.
Ask before merging, deploying, sending or editing email, replying to users or changing prices.
Update the log in the brief.
If nothing is new or worse, report "No change" and stop.
Today is day <n> of the window. Stop and tell me when the window has ended.
```

## Weekly

```text
Run the launch-watch weekly summary for <app>.
Read docs/launch-watch.md and its log.
Deliver the weekly summary from the launch-watch output contract: fix now, watch and ignore lists with evidence, funnel numbers against baseline with sample sizes, ranked feedback themes, and decisions waiting for me.
Do not change code or send anything.
```

Schedule the weekly prompt on the same weekday as launch, after the daily run.
