---
name: flutter-precommit-cleanup
description: >-
  Run formatting, analysis and codegen before committing in a Flutter or Dart repository, then squash WIP commits. Use before any commit or PR in a Flutter project, or when asked to tidy a branch before review.
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

## Boundaries

- Never squash or rebase commits that are already pushed to a shared branch without explicit authorization.
- Never add co-author tags to commit messages.
- Formatting and analysis passing does not authorize pushing, merging, or releasing.

## Sources

- <https://dart.dev/tools/dart-format>
- <https://docs.flutter.dev/reference/flutter-cli>
- <https://pub.dev/packages/build_runner/changelog>
