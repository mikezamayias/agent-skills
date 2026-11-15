---
name: techdebt
description: >-
  Scans the current project for duplicate code, dead code, TODOs, unused imports and inconsistent patterns. It writes a prioritized report to `tasks/techdebt.md`. Use at session end or when the user says techdebt, tech debt, cleanup, dead code or duplicated code.
---

# Tech Debt Audit

The idea comes from tip 4 in [Boris Cherny's Claude Code team tips](https://x.com/bcherny/status/2017742741636321619): a `/techdebt` command run at the end of every session.

You have been invoked to perform a tech debt audit of the current project.

## Process

### 1. Identify Scope

- If inside a git repo: audit that project root
- If not in a project: audit recently modified files; write to `~/.claude/tasks/techdebt-global.md`
- Output file: `tasks/techdebt.md` (relative to project root)

### 2. Scan for Issues

Use subagents to scan in parallel:

#### Agent A - Duplication

- Find functions/methods with near-identical logic
- Find copy-pasted blocks (10+ lines repeated 2+ times)
- Find duplicate type definitions or constants

#### Agent B - Dead Code

- Exported symbols never imported elsewhere
- Functions defined but never called
- Variables assigned but never read
- Commented-out code blocks older than obvious debugging

#### Agent C - Hygiene

- TODO/FIXME/HACK/XXX comments - list each with file:line
- Unused imports/dependencies
- Inconsistent naming patterns (camelCase vs snake_case in same file)
- Magic numbers/strings that should be constants

### 2b. Vet every finding

- Open each cited file and line yourself before it goes in the report, because scan agents over-report.
- Drop or correct three kinds: behavior that is intended (a platform convention, or a tradeoff recorded in an architecture decision record (ADR), `docs/decisions/` or the project's `AGENTS.md`), a real finding with the wrong file or line, and duplicates between agents.
- A decision record that the code no longer follows is itself a finding, because either the record or the code is wrong.

### 3. Prioritize Findings

| Priority     | Criteria                                   | Action                |
| ------------ | ------------------------------------------ | --------------------- |
| **Critical** | Dead code, duplicate logic causing bugs    | Remove immediately    |
| **High**     | Duplicate functions, unused exports        | Refactor this session |
| **Low**      | TODOs, style inconsistencies, magic values | Note for later        |

### 4. Write Report

Create `tasks/techdebt.md` with:

```markdown
# Tech Debt Report - [DATE]

## Critical (remove now)

- [file:line] description

## High (refactor soon)

- [file:line] description

## Low (note for later)

- [file:line] description

## Stats

- Files scanned: N
- Issues found: N critical, N high, N low

## Considered and rejected

- [file:line] dropped finding: reason
```

- When several findings share one cause, group them under one proposed fix, written above the findings it solves, each finding with its `file:line`.
- Keep this grouped list as a decision log in the report, so a long session can resume after compaction without rereading the code.
- End the report with "## Considered and rejected", one line per finding dropped in step 2b with its reason.
- This step recreates the report file on every run.
  Before overwriting `tasks/techdebt.md`, or `~/.claude/tasks/techdebt-global.md` outside a project, read its "Considered and rejected" list.
  Carry each line forward into the new report and do not report that item again, unless the code at that location changed, in which case vet it again like a new finding.

### 5. Offer to Fix

After writing the report, ask:

> "I found N critical and N high-priority issues. Should I fix the critical ones now?"

If yes: fix critical items first, then offer high-priority items.

## Notes

- Do NOT refactor working code unless it's clearly duplicated or dead
- Do NOT add TODOs - the report itself is the record
- Run this at the end of every development session
