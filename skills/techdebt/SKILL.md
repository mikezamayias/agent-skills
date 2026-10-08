---
name: techdebt
description: >-
  Scan the current project for duplicate code, dead code, TODOs, unused imports and inconsistent patterns. It writes a prioritized report to `tasks/techdebt.md`. Use at session end or when the user says techdebt, tech debt, cleanup, dead code or duplicated code.
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

#### Agent A — Duplication

- Find functions/methods with near-identical logic
- Find copy-pasted blocks (10+ lines repeated 2+ times)
- Find duplicate type definitions or constants

#### Agent B — Dead Code

- Exported symbols never imported elsewhere
- Functions defined but never called
- Variables assigned but never read
- Commented-out code blocks older than obvious debugging

#### Agent C — Hygiene

- TODO/FIXME/HACK/XXX comments — list each with file:line
- Unused imports/dependencies
- Inconsistent naming patterns (camelCase vs snake_case in same file)
- Magic numbers/strings that should be constants

### 3. Prioritize Findings

| Priority     | Criteria                                   | Action                |
| ------------ | ------------------------------------------ | --------------------- |
| **Critical** | Dead code, duplicate logic causing bugs    | Remove immediately    |
| **High**     | Duplicate functions, unused exports        | Refactor this session |
| **Low**      | TODOs, style inconsistencies, magic values | Note for later        |

### 4. Write Report

Create `tasks/techdebt.md` with:

```markdown
# Tech Debt Report — [DATE]

## Critical (remove now)

- [file:line] description

## High (refactor soon)

- [file:line] description

## Low (note for later)

- [file:line] description

## Stats

- Files scanned: N
- Issues found: N critical, N high, N low
```

### 5. Offer to Fix

After writing the report, ask:

> "I found N critical and N high-priority issues. Should I fix the critical ones now?"

If yes: fix critical items first, then offer high-priority items.

## Notes

- Do NOT refactor working code unless it's clearly duplicated or dead
- Do NOT add TODOs — the report itself is the record
- Run this at the end of every development session
