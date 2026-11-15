---
name: parallel-agent-inbox
description: >-
  Runs many coding-agent threads as an inbox: fires problems, isolates work, and only attends when done or blocked. Use when juggling parallel agent tasks, derisking merges, or keeping work going after the laptop closes. Also use when threads pile up, agents collide on the same checkout, or review waits dominate throughput.
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
  The `babysit-pr` skill holds the full procedure and its `pr-wait` script, and `full-send` and `full-stop` hold the merge gate.
  Wait with one watcher per pull request and never a hand-written sleep loop.
  Every watcher on one GitHub account draws on the same rate limit.
  The thread that owns the pull request is the only one that watches it, and a delegated reviewer never does.
  A wake-up is news and not a merge decision, so check the merge conditions yourself each time.
  Stop watching before you hand off or ask a question, so the thread does not keep showing as busy.
  If GraphQL is used up, GitHub says the REST API has a separate primary limit (GitHub docs read 2026-11-14), so read the pull request and its check runs through REST instead.
  One open-source skill pack reports that the `gh pr` commands use GraphQL (repo text, not run).
  The rest of this bullet follows one repository's practice (single report from one author's skill pack, not measured).
  Act only on checks and comments that are newer than the latest push.
  Check each bot finding against the source before changing code, fix the real ones and answer the rest with a written reason.
  Tell a repository failure from an infrastructure failure before you rerun or change anything, and name which one it was in the report.
  Write down the signal you used, such as the same test failing on the base branch or a runner error before any test ran, because that skill gives no method for the split.
  Keep the pull request at the size of the goal.
  Decline unneeded tests, guards for rare cases and small speed costs with a written reason, list them as follow-ups, and prefer the fix that deletes or narrows code.
- State merge conditions if the host may merge without you.

When the owner wants a decision and not a finished merge, one repository's practice (single report from one author's skill pack) is a stop-at-ready mode.
Under a stated grant to push, the agent may commit, push and rebase its own branch with a lease-protected force push, but never merges, enables auto-merge or enters a merge queue.
It turns off any auto-merge that already exists before it starts, checks again before each push, and reports one of three states: ready to merge, waiting only on a required human approval, or blocked with what it tried.
A question for the owner goes through the harness question tool, because a plain message leaves the thread looking finished.
If no question tool exists, leave the pull request open and unmerged and start the final message with the question.

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

## Cloud sandbox limits

Before handing a task to a cloud-hosted agent, list every host the task must reach and check the sandbox allows each one.
Claude Code on the web (docs read 2026-10-13): `api.github.com` is allowed and REST through `gh api` works for attached repos, but GraphQL (`gh pr`, `gh issue`) and other repos return 403, and the proxy rejects pushes of anything but a branch, such as a tag.
Repo `.mcp.json` servers and connectors load there, while user-scope `claude mcp add` servers do not.
Codex cloud blocks internet access in the agent phase by default and can be set to limited or unrestricted access per environment, while setup scripts always run with internet access (the page is labeled Codex Cloud Legacy and now lives under <https://learn.chatgpt.com/docs/environments/cloud-environment>).
Cursor cloud agents do not run Tailscale in their default networking mode.
A Tailscale auth-key join needs egress to `*.tailscale.com`, and ephemeral keys are single use.
A phone can show Online in `tailscale status` and answer pings while refusing every TCP connection. Fix it by reconnecting the phone to Wi-Fi, toggle Tailscale and keep the target app in the foreground.
Keep signing secrets on the CI runner, never in a cloud agent sandbox.

## Guardrails

- Do not stack or share accounts to evade provider terms, and do not turn coding subs into a public API.
- Do not auto-merge or auto-deploy without stated checks and human policy for production.
  When the owner does grant a merge, write the conditions that "State merge conditions if the host may merge without you." in "3. Make the next visit merge-ready" asks for into the task.
  One repository's merge gate, a single report from one author's skill pack, uses these: proof that covers every change in the diff, required checks green on the latest commit, review bots finished with each finding fixed or declined in writing, no human review asking for changes, and a branch that is up to date and mergeable.
  Never use an admin override or another bypass of branch protection to meet them.
  Run `git fetch` and re-read the pull request right before the merge.
  If proof is not possible, stop and ask, because the missing proof is the answer.
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
