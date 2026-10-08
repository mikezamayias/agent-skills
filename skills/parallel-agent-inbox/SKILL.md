---
name: parallel-agent-inbox
description: >-
  Run many coding-agent threads as an inbox: fire problems, isolate work, and only attend when done or blocked. Use when juggling parallel agent tasks, derisking merges, or keeping work going after the laptop closes. Also use when threads pile up, agents collide on the same checkout, or review waits dominate throughput.
metadata:
  provenance: local
---

# Parallel Agent Inbox

Keep many coding-agent threads in flight without becoming the bottleneck.
Treat each thread as a task in an inbox: send a problem with enough context to finish, isolate the checkout, ignore it while it works, and only return when it is done or blocked.

## Scope and handoffs

This skill covers day-to-day parallel coding throughput: prompting, isolation, review timing, and remote always-on runners.

Hand off where another skill goes deeper:

- Multi-agent product/architecture orchestration: `orchestrate-agentic-engineering`.
- Scheduled crash triage into fix PRs: `proactive-crash-repair-loop`.

Use the project's existing agent host, CI, and git workflow.
Do not require a specific IDE brand.

## 1. Set the operating constraints

Before spinning threads:

1. Confirm auth is meant for developer coding agents, not for serving end-user inference.
2. Prefer one stable network path for subscription-backed coding tools when the provider is sensitive to datacenter IPs.
3. Have an always-on worker available (home Linux box or equivalent) so threads survive closing the laptop.
4. Confirm revert is cheap: a bad merge must be undoable in seconds, or slow down until it is.

## 2. Intake problems, not patches

When a bug, feature, or question appears:

1. Open a new thread immediately.
2. Describe the problem, evidence, and success condition.
3. Ask whether a simple approach already exists before prescribing files and diffs.
4. If the agent solves it, spend human time reviewing.
5. If it fails, that failure is the signal to think harder yourself.

Do not wait until you have designed the solution before involving the agent.

## 3. Make the next visit merge-ready

Pack the first prompt so the next time you open the thread you can decide, not drip more chores:

- Implement or investigate.
- Run the relevant checks.
- Open or update the PR.
- Attach preview/env access when needed.
- Babysit CI/review comments until green or clearly blocked.
- State merge conditions if the host may merge without you.

Add only the tools and repo context required for that outcome.

## 4. Isolate parallel work

Default each active thread to its own worktree or otherwise isolated checkout and branch.
Do not put two writers on the same dirty tree.
If git or worktree collisions appear, let the agent recover unless it is stuck after a clear retry.

## 5. Run the inbox loop

Human attention rules:

1. Fire the thread and leave. Do not watch streaming tokens.
2. Attend only to done or needs-input items.
3. Working threads stay out of focus.
4. After a decision (merge, follow-up, drop), clear the thread from the active inbox (settle/archive).
5. Aim to end the day with only running work or an empty inbox.

Across machines, route new threads onto always-on workers when the local device will sleep or leave the network.

## 6. Spend tokens where they buy attention back

Bias spend toward verification, reproduction, PR triage, and unexplained diffs from teammates.
Use exploratory or "silly" prompts only when quota would otherwise expire unused and the work cannot harm production.
Keep secrets, customer data, and production credentials out of prompts unless the user explicitly authorizes that path.

## Guardrails

- Do not stack or share accounts to evade provider terms, and do not turn coding subs into a public API.
- Do not auto-merge or auto-deploy without stated checks and human policy for production.
- Do not babysit a healthy working thread.
- Do not start aggressive parallel shipping if revert is slow or CI is untrusted.
- Do not prescribe a single vendor's UI; require inbox semantics, isolation, and remote runners as capabilities.

## Output contract

Return:

1. Current inbox snapshot: running, needs-input, done.
2. New threads filed, each with problem statement and merge-ready success condition.
3. Isolation choice per thread (worktree/branch/machine).
4. Verification and revert posture before more concurrency.
5. Decisions taken on done items (merge, follow-up, drop) and inbox leftovers.
6. Any blocked items that need human thought because the agent failed.

## Source notes

Workflow distilled from Theo - t3.gg's YouTube video “If you have a Claude sub, watch this” (2026-10-02).
See `references/video-notes.md` for source extraction, limits, and adaptation choices.
Read that file when provenance matters.
