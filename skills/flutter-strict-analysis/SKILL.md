---
name: flutter-strict-analysis
description: >-
  Sets up a strict Flutter analysis policy with a --fatal-infos CI gate, not just dart analyze. Use when setting up a new Flutter repo, when flutter_lints feels too loose or CI analyze is noisy. Also use when a PR should not compile with missing returns.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter strict analysis

Do not ship production apps on default `flutter_lints`.
As of Dart 3.13, the linter has 244 non-deprecated, non-removed rules (233 stable, 11 experimental).
`flutter_lints` 6.0.0 (with `lints` 6.1.0) enables 102 of them (~42%).
The Flutter framework repo enables 177 (~72%), and `very_good_analysis` 11.0.0 enables 214 (~88%).
Recount when these packages or the SDK update.

This is **policy**, not "run dart analyze".

## Pick one policy

- **Package:** `very_good_analysis` (strictest maintained set) or `lint` (slightly less strict, `strict`/`casual`/`package` flavors).
- **Manual (once you care):** include all rules, disable a short documented list.
  Copy the list from <https://dart.dev/tools/linter-rules/all> into `all_lint_rules.yaml` and refresh it on SDK upgrades.
  Do not depend on `all_lint_rules_community`, which was last published in November 2024 (0.0.43) and misses newer rules.

Never add `pedantic` or `effective_dart` (deprecated).

## Manual skeleton

```yaml
include: all_lint_rules.yaml # copied from dart.dev/tools/linter-rules/all
analyzer:
  exclude:
    ["**/*.g.dart", "**/*.freezed.dart", "**/*.mocks.dart", "lib/generated/**"]
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
  errors:
    included_file_warning: ignore
    missing_required_param: error
    missing_return: error
    record_literal_one_positional_no_trailing_comma: error
    parameter_assignments: warning
    todo: ignore
formatter:
  page_width: 120
  trailing_commas: preserve # Dart >= 3.8
linter:
  rules:
    prefer_double_quotes: false
    sort_constructors_first: false
    # every disable gets a why-comment
```

The all-rules list contains conflicting pairs such as `prefer_single_quotes` and `prefer_double_quotes`.
Without `included_file_warning: ignore`, the analyzer reports that conflict as a warning on the `include`, and `dart analyze` fails on warnings by default.
Disable one rule of each conflicting pair in `linter: rules:`.

After enabling: `dart fix --apply` then `dart analyze`.

When a rule fights you, disable it **with a comment**. Do not `// ignore:` across the repo.

## CI

```yaml
- run: dart format --output=none --set-exit-if-changed .
- run: dart analyze --fatal-infos
```

`dart format` reads `formatter: page_width` from `analysis_options.yaml` (default 80).
Keep the width only there so CI and editors agree.

## Repo rules for repeated agent mistakes

- When the same review comment appears twice on agent-written code, turn it into a lint rule instead of a line in `AGENTS.md`.
  A rule fails the agent's own check run, and a prose rule only asks (a recommendation inferred from the T3 Code and qmd rule sets, untested here).
- One engineer who ships about 1,000 agent PRs a month ranks enforcement from strongest to weakest as codebase conventions, then static checks that fail CI (lint, compiler, import-boundary checks), then rules, a review bot and skills, which agents "can still forget" (single report, a 2026-10 talk).
  They call a human enforcing an invariant in PR review a code smell, and ask whether the check can be a lint rule, a CI failure or a design that removes the problem.
  Their concrete examples are an import check that fails when one layer's directory imports another's and a ban on code comments, because agents write comments about past instructions.
  This skill does not adopt the comment ban, because every suppression here needs a reason comment.
  For a layered Flutter app, a CI check that fails on a forbidden package import is the same idea, and `ffca-audit` owns the layer rules (inference, not checked against that skill's text).
  Its `validate_layers.dart` script reads only pubspec dependencies between workspace packages (read 2026-10-29).
- In a single-package app with `lib/features/<feature>/presentation` and `data` folders, a pubspec-based layer check has nothing to read.
  Write the check as a script that greps `import` and `export` lines.
  One developer's version greps `lib/features/*/presentation` for `import .*/data/`, prints the hits, prints "presentation/ must not import data/" and exits 1 (single report, from a post image).
  That nine-line version has three flaws, each reproduced on 2026-10-29 with the system `grep`.
  With `|| true` after the grep and no directory test, a missing or renamed folder gives exit 0, so the check passes while checking nothing.
  It does not match `export` lines.
  It does not match an `import` whose path is on the next line.
  Test the directory first and exit non-zero when it is absent, match lines that start with `import` or `export`, and restrict the search to `--include='*.dart'`.
- The same developer's published checker (MIT, `Ethiel97/flutter-clean-riverpod-skills`, `skills/flutter-feature-scaffold/scripts/check_boundaries.sh`) does these three things and checks five rules.
  Its smoke test injects one violation per rule and asserts each is reported.
  It also asserts that a legitimate cross-feature domain import is not flagged.
  Copy the idea, and treat any use of the repo's files as remote code that goes through the code-gate rule.
- Dart supports project rules through analyzer plugins since Dart 3.10, with the `analysis_server_plugin` package.
  A plugin registers its rules in `lib/main.dart`, and a lint rule a plugin defines stays off until `analysis_options.yaml` lists it under `plugins: <name>: diagnostics:`.
  The page does not cover the older `custom_lint` package, so check which one a repo already uses before adding the other.
  Adding either package is a new dependency and goes through the code-gate rule.
- Require a reason on every suppression, as T3 Code's `require-suppression-reason` rule does, so the "disable it with a comment" policy above is checked by a tool.
- Keep the set small and name each rule after the mistake it stops.
- Make the failure output state the rule and the fix, for example "presentation/ must not import data/, go through the repository interface in domain/".
  The agent reads CI output in the same loop as its test results, so the message is the one instruction it is sure to see.
  The author of one post calls this their most effective prompt, which is one author's opinion with no measurement.

## Sources

- <https://rydmike.com/blog_flutter_linting>
- <https://dart.dev/tools/linter-rules/all>
- <https://dart.dev/tools/analysis>
- <https://dart.dev/tools/dart-format>
- <https://dart.dev/tools/dart-analyze>
- <https://pub.dev/packages/lint>
- <https://pub.dev/packages/very_good_analysis>
- <https://dart.dev/tools/linter-rules>
- <https://dart.dev/tools/diagnostics/included_file_warning>
- <https://github.com/dart-lang/sdk/issues/55975>
- <https://pub.dev/packages/flutter_lints>
- <https://pub.dev/packages/lints>
- <https://pub.dev/packages/all_lint_rules_community>
- <https://github.com/flutter/flutter/blob/master/analysis_options_common.yaml>
- <https://github.com/VeryGoodOpenSource/very_good_analysis>
- <https://github.com/VeryGoodOpenSource/very_good_templates/blob/main/very_good_core/__brick__/analysis_options.yaml>
