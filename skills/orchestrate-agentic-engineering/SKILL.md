---
name: orchestrate-agentic-engineering
description: >-
  Coordinate non-trivial software delivery through one human captain, one orchestrator and bounded specialist agents. Use for greenfield apps, cross-stack features, migrations or complex projects that need parallel agents. It runs from discovery to real end-to-end proof while reducing the human's context switching.
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

Parallelize only independent nodes. Define integration owner where contracts meet.

### 6. Dispatch bounded implementation

- Keep orchestrator free for monitoring, steering, and dependency resolution.
- Route follow-up work to existing owner when scope matches.
- Require specialists to commit coherent changes and run relevant checks.
- Give reviewers raw artifacts and task contract, not desired conclusion.
- Tighten review and merge policy as prototype becomes production code.

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

### 9. Review architecture and release

- Review API surface, authorization, data model, core boundaries, cost, and operational burden.
- Remove needless complexity introduced during parallel work.
- Build release or test-distribution artifact only after acceptance scenario passes.
- Require explicit captain approval before production writes, external sends, publication, spending, or destructive actions.

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

## Context and Handoff Discipline

Keep orchestrator context limited to:

- Settled decisions.
- Dependency graph.
- Workstream state.
- Blockers and authority needs.
- Artifact paths and proof.

Close completed specialist sessions. After compaction or handoff, reload repository artifacts before acting. Prefer reviewable artifacts over long report walls.

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

Read [references/video-notes.md](references/video-notes.md) when provenance, observed examples, or tool-agnostic adaptation choices matter. Keep normal execution on this file's workflow.
