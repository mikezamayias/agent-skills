---
name: orchestrate-agentic-engineering
description: >-
  Coordinates non-trivial software delivery through one human captain, one orchestrator and bounded specialist agents. Use for greenfield apps, cross-stack features, migrations or complex projects that need parallel agents. It runs from discovery to real end-to-end proof while reducing the human's context switching.
---

# Orchestrate Agentic Engineering

Run one steering interface while specialist agents execute bounded work. Persist decisions and evidence in repository so delivery survives parallelism and context compaction.

## Role Model

### Captain

- Provide raw intent, users, constraints, success criteria, and non-goals.
- Decide product tradeoffs, cost, security posture, scope, and production access.
- Review artifacts and proof instead of every tool call.
- Approve irreversible actions and actions only human can perform.

### Orchestrator

- Convert narrative into decisions, unknowns, workstreams, dependencies, and gates.
- Delegate execution and remain responsive to steering.
- Persist task state, artifact paths, branches, commits, blockers, and evidence.
- Integrate results and surface only material choices or real blockers.
- Never claim completion from plans, mocks, or workflow status alone.

### Specialists

- Own one bounded outcome per session.
- Work in isolated branches or worktrees when code changes can overlap.
- Return artifact, evidence, assumptions, risks, and next dependency.
- Diagnose failures before escalating.
- Ask captain only for authority, credentials, consent, or decisions agents cannot make.

Delegate only when host supports subagents and work can run independently. Otherwise execute same work graph sequentially.

## Workflow

### 1. Capture intent

Accept a long, imperfect narrative. Extract:

- Problem and target users.
- Must-haves and explicit exclusions.
- Constraints, budget, deadline, and environments.
- Core user journey and verifiable definition of done.
- Assumptions, unresolved decisions, and authority boundaries.

Ask only questions whose answers materially change direction.

### 2. Dispatch parallel discovery

Run independent tracks when useful:

- Market or user research.
- Technical feasibility and architecture options.
- Low-fidelity UX journey or prototype.
- Existing-system and operational-state audit.

Do not implement before research can still invalidate product, scope, or architecture.

### 3. Run judgment loop

- Present findings as diagrams, prototypes, comparisons, or short decision records.
  Local rule: draw a diagram only when the reader learns more from it than from a paragraph or a 3-column table.
- Let captain accept, reject, or edit assumptions.
- Verify cost, platform, and vendor claims against primary evidence.
- Remove hidden scope: premature environments, audit systems, exports, enterprise controls, and imagined scale.
- Mark unresolved decisions explicitly; do not bury them in prose.

Stop and re-plan when new evidence invalidates dependency graph.

### 4. Persist foundation

Write settled state into repository before major implementation:

- PRD or concise product brief.
- Executable acceptance scenario.
- Architecture decisions and design rules.
- Decision log with rejected options.
- Dependency-aware work ledger.

Treat repository artifacts as recovery source after compaction. Never rely on chat history alone.

### 5. Build dependency graph

For each work item record:

- Outcome and owner.
- Inputs and dependencies.
- Allowed files or system boundary.
- Acceptance checks.
- Branch/worktree or execution context.
- Expected artifact and handoff proof.
- Authority required.
- Stop condition and the maximum attempts before the item is escalated.
- Timeout for the handoff, and whether repeating it is safe.

Parallelize only independent nodes. Define integration owner where contracts meet.

### 6. Dispatch bounded implementation

- Keep orchestrator free for monitoring, steering, and dependency resolution.
- Route follow-up work to existing owner when scope matches.
- Require specialists to commit coherent changes and run relevant checks.
- Give reviewers raw artifacts and task contract, not desired conclusion.
- Tighten review and merge policy as prototype becomes production code.

When one verification run takes hours, open one branch per candidate fix and let the builds run in parallel.
Keep one Markdown file as source of truth for root cause, test cases, branches and build status.
Have a human test the resulting artifacts.
Evidence: Grab Engineering blog (single author, self-reported, read on 2026-10-21), where it replaced one-by-one 2-hour CI waits.

### 7. Integrate real system

Verify cross-stream contracts:

- Frontend uses real backend where completion requires integration.
- Authentication, schema, names, URLs, and environment identity agree.
- Secrets remain outside prompts, source, logs, and ordinary config files.
- Deployment and runtime configuration point to intended environment.
- Mocks are identified and removed from core acceptance path.

Reject mock-only completion.

### 8. Prove end to end

Execute real core journey. Example:

1. Authenticate.
2. Create or mutate state.
3. Observe state through second relevant view or actor.
4. Restart or sign out.
5. Sign in again.
6. Confirm persistence and authorization.

Collect exact commit, commands, checks, endpoint/config identity, concise logs or screenshots, and remaining risks. Workflow success without user-journey proof is insufficient.

Drive the real user path, never internal setters, test-only endpoints or handlers invoked through eval.
Use eval only to read state after the user path ran.
Run a health check first, because a recording against a stale build or the wrong instance is not evidence.
Capture the trigger and the stable end state in the same recording or log, and check side effects in the store that holds them.
Exercise every reachable entry point the change touches, plus its success, cancel, error, empty and persistence paths.
Report an unreachable path with its concrete blocker and cover the closest real path that remains, never claiming it verified through a different path.
For a bug fix, run the same proof against the base commit and the branch, and require it to fail on the base. A proof that passes on both is not evidence.
For a repeatable recipe per project, use `create-verification-skill` and keep it honest with `maintain-verification-skill`.

### 9. Review architecture and release

- Review API surface, authorization, data model, core boundaries, cost, and operational burden.
- Remove needless complexity introduced during parallel work.
- Build release or test-distribution artifact only after acceptance scenario passes.
- Require explicit captain approval before production writes, external sends, publication, spending, or destructive actions.

## Unattended agent charter

Before an agent runs without a human watching, record:

- A spend cap.
- A separate credential and login for each agent.
- An append-only action log that someone reviews on a schedule.
- An approval gate for anything sent in a person's name, including negotiation emails.
- A kill switch.

This is standard least-privilege practice, not a claim from a source.

## Gates

### Research Gate

- User and problem explicit.
- Market gap or differentiation stated.
- Technical options compared with evidence.
- Major assumptions and unresolved risks visible.

### Planning Gate

- Minimal scope frozen.
- Core journey reviewable and executable.
- Current-scale architecture chosen.
- Human decisions persisted.
- Work graph respects dependencies and file ownership.

### Implementation Gate

- Each specialist has bounded outcome and contract.
- Code changes isolated where needed.
- Tests and checks pass.
- Security-sensitive changes receive proportional review.
- Production mutation remains human-authorized.

### Verification Gate

- Real integration, not mocks.
- Core journey passes end to end.
- Persistence and restart behavior checked when relevant.
- Architecture reviewed for security and overengineering.
- Exact source and evidence captured.
- A model-reported bug is a claim until a repro test fails on the assertion that encodes it. A repro failing for another reason means the test is wrong. A passing repro rejects the finding.
  Local rule: confirm the run report lists the repro as executed, because an excluded or unselected test proves nothing either way.
- A claim that cannot be executed needs an independent verdict, and a change the agent both proposed and judged on the same task is a hypothesis.
  The verifier is a fresh agent that did not produce the claim and defaults to "false positive".
  It rules a finding true only with a file and line for the source, the sink and the absence of a mitigation it read.
  Count votes in code, not in prose, and let a vote lower a severity but never raise it.
  Count a self-judged change as verified only after an independent check such as a held-out task, a human review or a test the agent did not write.
  Evidence: the verifier rules are restated from Claude Security's plugin files (commit e68e375) and Cloudflare's security-audit skill README (MIT).
  The self-judged rule is inference from the Harness2 design (Google, Apache-2.0, commit 1cfe254) and reply-level opinion, not a statement in that repository.
- Evidence survives cleanup and every later run, and is checked at its named location after teardown.
  Local rule: a harness that reuses one results directory overwrites the proof on the next run, so name a per-proof output directory or copy the artifacts out first.
- When an agent run is scored against a public benchmark, rubric or test, block the answer hosts at network level for the executor and record the restriction with the result.
  Harness2's `docs/EXPERIMENTS.md` (commit 1cfe254, read 2026-10-20) documents a Codex rollout that downloaded its own rubric without being told to, and states that its own release does not block it.

## Context and Handoff Discipline

Keep orchestrator context limited to:

- Settled decisions.
- Dependency graph.
- Workstream state.
- Blockers and authority needs.
- Artifact paths and proof.

Close completed specialist sessions. After compaction or handoff, reload repository artifacts before acting. Prefer reviewable artifacts over long report walls.

Bound code search output, because raw search hits are a large share of an agent's input tokens.
List matching files first (`grep -l` or `rg -l`), cap matches per file (`-m`), keep context to a few lines, and narrow by path or type before reading whole files.
The flags above (`rg -l`, `-m`) were not tested by the benchmark below, which tested ranked top-20 output after `-C 3` context, so treat them as untested.
In Context.dev's vendor-run sgrep benchmark (October 2026, 100 SWE-bench Verified attempts per arm, tool output capped at 8,000 o200k tokens), plain ripgrep returned about 4,100 search tokens per attempt and hit the cap in 88 searches, against about 1,500 tokens and 4 capped searches for `rg --json -C 3` piped into sgrep.
Mean API cost was 21.3% lower, but total cost moved -0.4% with an interval spanning zero, median agent time was slower at 56.1 s against 52.5 s, and the solve rate of 0.70 against 0.68 has a paired interval of -3 to +8 points, which does not establish a gain.
Adopt output bounds, not a new search tool.

Use this handoff shape:

```text
Outcome:
Owner:
Status:
Artifact/branch/commit:
Checks run:
Evidence:
Assumptions:
Risks:
Dependencies unblocked:
Authority still needed:
```

## Running Many Helpers at Once

- Give each helper disjoint files, directories, or design pages.
  Two helpers editing one file at once break the checks.
  Disjoint files are not enough for Xcode work, because two helpers building one checkout into the same DerivedData collide.
  Give each its own `-derivedDataPath` or its own worktree.
- Helpers never commit.
  The orchestrator reviews the diff, runs the checks against the final state, and commits.
- Brief each helper with the rulings verbatim, the files it owns, the files it must not touch, and the report shape, including "choices no ruling settled".
- Verify each helper's key claims before relaying them, especially figures from research: estimates, prices, latencies, and terms clauses.
- Every product choice or assumption a helper made goes to the user.
  None stands by default.
- A resumed helper first checks what already exists, so it does not duplicate frames, files, or rows.
- Expect helpers to die from usage limits or stall watchdogs.
  Keep each brief small enough to resume, resume through the platform's message mechanism with the original context, and re-verify the state it left.
- A systematic defect needs a sweep of every instance.
  When one helper finds a pattern, such as an off-centre component, a wrong token, or a stale string, launch a sweep rather than fixing the samples.
  Check that the sweep only touched what it should.
- Keep the user oriented while helpers run.
  On a status request, answer with what is running, what is done with evidence, what is left, and whether design and documents agree.

### Briefs, limits, and proof

- Size each brief to finish in 20 to 30 minutes.
  Long helper runs are where hangs and dropped connections happen, and a short brief is cheap to rerun.
- Launch every helper with a hard wall-clock limit, and check for file activity once a run passes about 30 minutes.
  A process that is alive at 0% CPU with no file changes has stalled, and waiting for its exit notice can waste hours.
- Give every fact in a brief its provenance: the file and line, the command output, or the design node.
  For a design measurement, name the node, say whether it is the placed instance or the component, and read overrides such as stroke, radius, and clipping from the design tool's object model, not from generated code.
- Attach the project's pre-report checklist to every implementation brief, so the helper checks the recurring slips before it reports.
- Treat a helper's report as a claim.
  Before committing, the orchestrator reruns the gate on the final state and checks the facts a mistake would hide, such as lockfiles, measured sizes, and resource leases.
- Route the review to a reviewer that did not write the change, with the raw diff and the task contract.
  Put every finding through a fix round with its own review.
  The orchestrator does not wave findings through.
- When a helper restarts after a crash or a limit, tell it to inspect the working tree first and continue from it.
- When the same slip returns in round after round, fix its source (a pinned tool, a check that fails) instead of adding another manual step to every brief.
- A dead-code sweep must check the data a removed path wrote, not only its callers.
  A writer whose callers were removed can still feed data that live code reads.
- Stop patching and re-plan when a third fix round on one change still finds a blocking gap.
  Present the simpler design to the user.
- A text-only end of turn from a worker is a report and not proof of completion.
  Keep the task parts in a checklist the worker updates, in a to-do tool or a file.
  If a turn ends with items open and no blocker stated, send one short message naming them.
  State the completion condition up front, and optionally have a smaller model check it at each end of turn.
  If a background command or subagent is still running, do not treat the task as done.
  Stop after two or three automatic continuations on the same task and review it.
  For a fully unattended agent, Anthropic offers a standing system-prompt paragraph that names four early-stop patterns: a long summary announcing the next step, offering to continue unless redirected, listing non-blocking decisions, and reporting at a milestone.
  Use it only in unattended harnesses, keep confirmation for risky or irreversible actions, and expect more tool calls and output tokens.
  Source: Anthropic "Prompting Claude Opus 5.5", section "Unattended agentic runs" (official docs, read 2026-10-20).
  The separate checker model and the running-subagent rule are our additions.

### Process hygiene for agent shells

Record every background process an agent starts with `echo $! > name.pid` at spawn time.
Check liveness with `kill -0 "$(cat name.pid)"`, and stop a process with `kill "$(cat name.pid)"` before deleting the file.
Never use `pkill -f` or `pgrep`, because a command-line pattern can match the agent's own shell and some sandboxes lack `pgrep`.
An agent's shell shows output only when a command ends, so start any command that blocks on a human approval in the background, poll its log for the approval URL for a bounded time, print the URL and exit.
Give every CLI that can fall back to interactive login an explicit timeout, such as Tailscale's `--timeout=90s`.
In a readiness poll, stop waiting as soon as the started process is no longer alive.
Set `umask 077` before writing state or logs that hold login URLs or node identities.
Exit 1 only when a named human step is needed or the service failed, and exit 0 once the core service serves, saying what optional part is missing.
When a one-time login URL is consumed, kill by PID file, delete the stored identity and start fresh, instead of re-printing the dead URL.
Put the next action in the failure output, including what not to do.
A setup script writes its target directory first and, on failure, prints the one variable that moves it, before it downloads anything.
Pin the release version in the script and fetch the asset URL directly.
One installer script claims a latest-release redirect is refused in some sandboxes, which was not tested here.

### Bug bash fan-out

A bug bash is many exploration runs, one charter each, then a pass that proves every claimed bug.
A charter is one area, one posture and one sentence naming the start route and the account.
Plan 5 to 10 charters with postures such as first-time user, numbers and copy, edge input, state and error paths.
An edge-input charter names its exact input matrix, or it spends its budget before judging a result.
Run charters four at a time, each with its own output directory and its own seeded disposable account, because explorers sharing an account report each other's edits as bugs.
Local rule: read each run's step log before triage, because an exit code does not prove the charter ran.
A run that aborted, executed no step, or surveyed the app instead of its charter did not cover that charter, whatever its exit code, and goes under areas no charter reached.
Against a deployed site that others use, charters are read-only: no signups, submissions, injection-shaped URLs or request loops.
Before running code from a repository you did not write, or code an agent generated while hunting bugs, run it in an OS-enforced sandbox.
The sandbox has no external network, an empty environment plus an explicit allowlist, a read-only target, writes limited to a scratch directory, and hard CPU, memory and time limits.
If the sandbox cannot be enforced, do not run the code and record the lead as needing validation.
Check that no `.env` or credential file in the tree points at a shared or live service.
Sort every finding into explorer artifact, environment, design, fixture or candidate by reading the source, and write repro tests only for candidates.
Report confirmed bugs with their failing repro first, then unverified risks, then rejected findings grouped by reason, then areas no charter reached.
Adapted from tester-army/e2e `bug-bash.md` (Apache-2.0, read 2026-10-13).
The sandbox rule is restated from the READMEs of Cloudflare's security-audit skill, Mantis and Claude Security (read 2026-10-20).

## Failure Modes

- Orchestrator performs specialist work and becomes unavailable.
- Parallel agents edit overlapping files or assume incompatible contracts.
- Decisions exist only in chat and disappear after compaction.
- Vendor recommendation becomes architecture decision without human judgment.
- Mock client is mistaken for completed integration.
- Agent introduces unnecessary environments or enterprise controls.
- Specialist exposes secret through prompt, source, command, or log.
- Captain approves “done” without executable evidence.
- Team keeps patching after dependency plan becomes invalid.
- Reviewer receives expected answer and merely confirms it.
- A stalled helper runs for hours because the orchestrator only watches for its exit.
- An orchestrator's wrong fact in a brief is implemented faithfully and costs a review round.
- Cleanup kills processes by name instead of the process it started, and takes down the user's own session.
- Cleanup deletes the proof artifacts along with the scratch state.
- A verification recipe is handed over without being executed once end to end.
- A verification map is edited to match a regression, which hides a product bug as documentation drift.

## Output Contract

Return:

1. Normalized brief and unresolved decision list.
2. Parallel discovery plan.
3. Persisted decision and architecture artifacts.
4. Dependency-aware task ledger.
5. Workstream handoffs with branches, commits, and checks.
6. Integration findings and fixes.
7. End-to-end evidence.
8. Release decision, remaining risks, and authority requests.

## Sources

Distilled from Kun Chen's video _L8 Principal Building a Full Stack App with Agentic Engineering_: <https://www.youtube.com/watch?v=kPN564Kol14>.

Search output numbers: <https://github.com/context-dot-dev/sgrep> (7452784, `benchmarks/README.md` and `benchmarks/swe-bench/results/analysis.json`, plus `benchmarks/swe-bench/harness/PROTOCOL.md` for the 8,000-token cap).
The benchmark files were unchanged at commit dec6122 (2026-10-15).

Verification and stop rules: Harness2 <https://github.com/google-research/harness2> (commit 1cfe254), Anthropic's "Prompting Claude Opus 5.5" guide, and the security tools named in the bug bash section.

Read [references/video-notes.md](references/video-notes.md) when provenance, observed examples, or tool-agnostic adaptation choices matter. Keep normal execution on this file's workflow.
