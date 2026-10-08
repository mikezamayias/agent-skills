# Auto-Hook Setup: T1 on Every Push/PR

This documents how to configure an automatic Tier 1 (Testing + Security + Store Compliance) check that fires before pushing code or creating PRs.

## How It Works

A `UserPromptSubmit` hook fires when the user submits a prompt.
Claude Code passes the prompt as JSON on stdin in the `prompt` field.
A gate script checks if the prompt contains push/PR intent and prints a reminder, which Claude Code adds as context.

## Setup

### 1. Create the hook script

Save this to `.claude/hooks/launch-readiness-gate.mjs` in your project:

```javascript
#!/usr/bin/env node

// Launch Readiness T1 Gate
// Fires on UserPromptSubmit, checks if the prompt indicates push/PR intent

import { readFileSync } from "node:fs";

// Claude Code sends hook input as JSON on stdin; the prompt is in `prompt`
const input = JSON.parse(readFileSync(0, "utf8") || "{}");
const lowerPrompt = (input.prompt || "").toLowerCase();

const pushPatterns = [
  "/commit",
  "commit-push-pr",
  "gh pr create",
  "git push",
  "push to",
  "create pr",
  "create a pr",
  "open pr",
  "merge into",
  "push and create",
];

const isPrePush = pushPatterns.some((pattern) => lowerPrompt.includes(pattern));

if (isPrePush) {
  // Plain-text stdout from UserPromptSubmit is added as context Claude sees
  console.log(
    "Launch Readiness T1 gate: Run `/launch-readiness --tier 1 --changed --auto` before pushing. If T1 passes, proceed with the push/PR.",
  );
}

// Always exit 0 — this is advisory, not blocking
// The skill itself handles blocking logic based on findings
process.exit(0);
```

### 2. Add to settings

In `.claude/settings.local.json` (`UserPromptSubmit` does not support matchers, so none is set):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node .claude/hooks/launch-readiness-gate.mjs"
          }
        ]
      }
    ]
  }
}
```

### 3. Make the script executable

```bash
chmod +x .claude/hooks/launch-readiness-gate.mjs
```

## Branch-Specific Behavior

The skill itself determines strictness based on the target branch:

| Target                                    | Scope                     | On Failure           |
| ----------------------------------------- | ------------------------- | -------------------- |
| Integration (for example `develop`)       | Changed files only        | Warn, allow override |
| Release candidate (for example `release`) | Changed files + importers | Block, must fix      |
| Production (for example `main`)           | Full codebase             | Block, must fix      |

## Disabling

Remove the hook entry from `.claude/settings.local.json` to disable.

## Troubleshooting

- **Hook not firing**: Check that `.claude/settings.local.json` is valid JSON
- **False positives**: Adjust `pushPatterns` array in the gate script
- **Too slow**: The T1 check runs testing, security, and store compliance on changed files only.
