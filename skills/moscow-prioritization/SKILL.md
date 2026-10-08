---
name: moscow-prioritization
description: >-
  Cut a noisy backlog with MoSCoW (Must / Should / Could / Won't). Use when the backlog has more than 30 items, when standups feel pointless, or before any sprint kickoff.
---

# MoSCoW Prioritization

A backlog with no priority is a graveyard. MoSCoW forces you to commit. Every item lands in exactly one of four buckets:

- **Must** — release fails without it. Non-negotiable.
- **Should** — important but the release survives. Cut first under pressure.
- **Could** — nice if time remains. Default = won't happen.
- **Won't (this cycle)** — explicitly deferred. The honesty bucket.

## The rules that make it work

1. **Must is rare.** If more than 60% of items are Must, you haven't prioritized — you're hoping. Cut Musts until the sum fits in the cycle's capacity.
2. **Won't is mandatory.** Every triage must move at least 3 items into Won't. If nothing is dropped, nothing was decided.
3. **Re-rank weekly.** Priorities decay. A Must from last week may be a Could now.
4. **One MoSCoW per cycle.** Don't ladder-rank inside a bucket. The point is the cut, not the ordering.

## Solo founder usage

For one person, the practical mapping:

- Must = ship this week.
- Should = ship next week.
- Could = unscheduled.
- Won't = archived (with a date — review next quarter).

Run the triage at the start of each week, before opening any code.

## Anti-patterns

- "P0 / P1 / P2 / P3" with no time bound — nothing forces a cut.
- Endless re-ordering instead of dropping items.
- Treating MoSCoW as a label instead of a commitment.
