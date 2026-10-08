---
name: task-blitz
description: >-
  Fetch open tasks from Notion, group them by independence and run them with parallel sub-agents that plan before coding. Use when asked to work through open tasks, tackle the backlog, blitz tasks or execute a project action plan.
---

# task-blitz

Execute open tasks in parallel by spawning independent sub-agents.

## Workflow

### 1. Fetch Open Tasks

Query Notion for open tasks (Status = "To Do" or "In Progress"):

```bash
NOTION_KEY="${NOTION_KEY:-${NOTION_API_KEY:?set NOTION_API_KEY}}"
DB_ID="${DB_ID:-${NOTION_TASKS_DB_ID:?set NOTION_TASKS_DB_ID to your Notion tasks database ID}}"
curl -s -X POST "https://api.notion.com/v1/databases/$DB_ID/query" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter":{"or":[{"property":"Status","select":{"equals":"To Do"}},{"property":"Status","select":{"equals":"In Progress"}}]}}'
```

If user specifies a project and the database has a project property, filter on it: `{"property":"<project property>","select":{"equals":"<project>"}}`.

### 2. Analyze & Group

For each task, determine:

- **What repo/codebase** it touches
- **What files/modules** it likely affects
- **Dependencies** on other tasks (does task B need task A's output?)

Group tasks into **independent work streams** — tasks that touch different files/modules and can run in parallel without merge conflicts. Tasks that touch the same files must be sequential within their stream.

Present the plan to the user:

```text
## Action Plan

### Stream 1 (parallel): "Feature A"
- Add the library feature A needs
- Build the feature A screen
- Add feature A to the dashboard

### Stream 2 (parallel): "Navigation fixes"
- Add a back button to screen X
- Add a back button to screen Y

### Stream 3 (parallel): "Settings"
- Add a new settings toggle

### Sequential dependency: Stream 1 must complete before "Feature A polish" task
```

Wait for user approval before proceeding.

### 3. Spawn Sub-Agents

For each independent stream, spawn a sub-agent with `sessions_spawn`. Each sub-agent task prompt MUST include:

```text
## Constraints
- You are working on branch: `<branch-name>` (create from `dev`)
- ONLY modify files related to your task. Do not touch unrelated code.
- Use `gh` for GitHub CLI commands.

## Phase 1: Plan (DO NOT WRITE CODE YET)
Before writing any code:
1. Read the relevant source files in the repo
2. Understand the current architecture and patterns
3. Write a detailed implementation plan:
   - Which files to create/modify
   - What changes in each file
   - What tests to add/update
4. Output the plan

## Phase 2: Execute
Only after completing your plan:
1. Clone the repo and create your feature branch from `dev`
2. Implement changes following your plan
3. Run tests/linting to verify
4. Commit with conventional commit messages
5. Push and create a PR to `dev`

## Phase 3: Report
Summarize what was done, what was changed, and any issues encountered.
```

#### Branch naming convention

Each sub-agent gets a unique branch: `fix/<task-slug>` or `feat/<task-slug>`.

#### Key rules

- **Never spawn two sub-agents that modify the same files.** If unsure, make them sequential.
- **Each sub-agent must plan before coding.** The plan phase is mandatory.
- **Sub-agents must create PRs**, not push directly to `dev`.
- **Include repo path and project context** in each sub-agent's task prompt so it knows where to work.

### 4. Code Review (Mandatory)

Every PR gets a Claude Code review before merge. **No exceptions.**

When a sub-agent completes and creates a PR, run **Claude Code** (`claude -p`) for review:

```bash
REVIEW_DIR=$(mktemp -d)
git clone <repo-url> "$REVIEW_DIR"
cd "$REVIEW_DIR" && git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'
DIFF=$(git diff origin/dev...origin/pr/<number>)
claude -p "You are a code reviewer. Review this PR diff for bugs (🔴), security (🔴), code quality (🟡), architecture (🟡), style (🟢). Be thorough. PR #<number>: <title>. $DIFF"
```

Run reviews in parallel (one `claude -p` per PR). Post results as PR comments via `gh pr comment`. Clean up temp dir after.

Alternatively, spawn a **review sub-agent** for it:

```text
## Task: Review PR #<number> on <repo>

Use `gh` for GitHub CLI.

1. Fetch the diff: `gh pr diff <number> --repo <owner/repo>`
2. Fetch PR details: `gh pr view <number> --repo <owner/repo> --json title,body,files`
3. Review for:
   - 🔴 Bugs, logic errors, race conditions
   - 🔴 Security issues (secrets, injection, auth bypass)
   - 🟡 Code quality (naming, duplication, dead code)
   - 🟡 Architecture compliance (the project's own conventions)
   - 🟢 Style (formatting, imports, conventions)
4. Also check CodeRabbit reviews: `gh pr view <number> --repo <owner/repo> --comments --json comments,reviews`
   - Read all comments from `coderabbitai` and address actionable findings
5. Post review as a PR comment: `gh pr comment <number> --repo <owner/repo> --body "<review>"`
6. If critical issues found (🔴), request changes. Otherwise approve.
7. Report: list of findings with severity, whether PR is approved or needs changes.
```

Review sub-agents can run in parallel (one per PR). Label them `review-pr-<number>`.

### 5. Monitor & Report

After spawning, monitor sub-agents via `sessions_list`. When all complete:

1. Summarize results (PRs created, reviews done, issues found)
2. Update Notion task statuses
3. Flag any PRs that need changes based on review findings

## Notion Integration

Update task status as work progresses:

- When sub-agent spawned → set Status to "In Progress"
- When sub-agent completes successfully → set Status to "Done"
- When sub-agent fails → keep Status as "In Progress", add note

To update a Notion page:

```bash
NOTION_KEY="${NOTION_KEY:-${NOTION_API_KEY:?set NOTION_API_KEY}}"
curl -s -X PATCH "https://api.notion.com/v1/pages/<page_id>" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"Status":{"select":{"name":"Done"}}}}'
```

## Tips

- Prioritize High/Critical tasks first
- For large tasks, break them into subtasks before spawning
- If a project has strict branch protocols, such as always opening PRs against `dev`, include that in the sub-agent prompt
- Set reasonable `runTimeoutSeconds` based on task complexity (300-600s for small tasks, 900-1200s for large ones)
