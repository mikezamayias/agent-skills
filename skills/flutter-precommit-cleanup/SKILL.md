---
name: flutter-precommit-cleanup
description: >-
  Runs formatting, analysis and codegen before committing in a Flutter or Dart repository, then squashes WIP commits. Use before any commit or PR in a Flutter project, or when asked to tidy a branch before review.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter pre-commit cleanup

## Overview

Two passes that run before code leaves a branch.
The first makes the working tree clean.
The second makes the history readable.

## Pass 1: working tree

Run in order.
Stop and fix failures rather than committing through them.

```bash
dart format lib/ test/                                    # Format
flutter analyze                                           # Static analysis
dart run build_runner build                               # Regen, only if models or DI changed
```

Since `build_runner` 2.7.0, conflicting outputs are always deleted, and 2.15.0+ warns that `--delete-conflicting-outputs` (`-d`) is a removed, ignored option.
Keep the flag only for projects pinned below 2.7.0.

Skip `build_runner` when no generated source changed.
It is the slowest step and rerunning it without cause produces noisy diffs.

Follow with a quality pass over the changed code before committing.

## Pass 2: history

Intermediate WIP commits make a PR log every save instead of telling a story.
Squash them into clean logical commits before opening the PR.

```bash
git rebase -i origin/dev   # or the repository's integration branch
```

Confirm the base branch from the repository rather than assuming `dev` or `main`.

## Enforce the rules in a Claude Code session

A line in CLAUDE.md is advice and a hook is enforced, so put the rules that must never be broken in hooks.
Hooks go under a `hooks` key in `.claude/settings.json`, not in a file called `.claude/hooks.json`.
Each matcher group holds a nested `hooks` array with `"type": "command"`.
The tool input arrives as JSON on stdin, and the path is `tool_input.file_path`.
An exit code of 2 blocks, and exit code 1 only warns (verified in Anthropic's hooks reference, read 2026-10-31).

Block hand edits to generated Dart files in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-generated.sh"
          }
        ]
      }
    ]
  }
}
```

Then put this in `.claude/hooks/block-generated.sh`:

```bash
#!/usr/bin/env bash
path=$(jq -r '.tool_input.file_path // empty')
case "$path" in
  *.g.dart|*.freezed.dart|*.mocks.dart)
    echo "Blocked: $path is generated. Change the source file and run dart run build_runner build." >&2
    exit 2 ;;
esac
exit 0
```

The script blocked the three generated suffixes and allowed a plain `.dart` file in a test run with fabricated JSON input on 2026-10-31, and it was not run inside a live Claude Code session.
It stops the Edit and Write tools only, because a `sed -i` through the Bash tool still reaches the file (inference).
Do not copy a snippet that reads `$CLAUDE_TOOL_INPUT_PATH`, because that variable is not in the hooks reference.
Do not copy a snippet that sets `--delete-conflicting-outputs` unless the project pins `build_runner` below 2.7.0, because later versions ignore the flag.

To stop a session from ending while analysis fails, add a `Stop` hook that exits 2, wired under a `Stop` key in the same `hooks` object:

```bash
#!/usr/bin/env bash
out=$(flutter analyze 2>&1) && exit 0
printf 'flutter analyze reports issues, fix them before stopping:\n%s\n' "$out" >&2
exit 2
```

Exit 2 on a `Stop` hook sends Claude back to keep working.
Claude Code ends the turn anyway after eight stop-hook continuations in a row, and each stop hook also receives `stop_hook_active` so a script can give up early (verified in the hooks reference, 2026-10-31).
`flutter analyze` treats infos and warnings as fatal by default in Flutter 3.47.7 (`--[no-]fatal-infos` and `--[no-]fatal-warnings` both default to on, read from `flutter analyze --help` on 2026-10-31), so the gate also fails on lints.
The cost is one analyzer run at the end of every turn, including turns that changed no Dart file, so scope it to a repository where `flutter analyze` finishes in seconds, or keep it as a manual step in Pass 1.
This script was run against a stub `flutter` that failed and one that passed on 2026-10-31, and it exited 2 and 0, but it was not run inside a live Claude Code session.
A `pre-push` git hook that runs the same format and analyze commands covers pushes made outside a Claude Code session.

## Boundaries

- Never squash or rebase commits that are already pushed to a shared branch without explicit authorization.
- Never add co-author tags to commit messages.
- Formatting and analysis passing does not authorize pushing, merging, or releasing.

## Sources

- <https://dart.dev/tools/dart-format>
- <https://docs.flutter.dev/reference/flutter-cli>
- <https://pub.dev/packages/build_runner/changelog>
