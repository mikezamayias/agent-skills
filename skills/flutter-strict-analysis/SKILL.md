---
name: flutter-strict-analysis
description: >-
  Set up a strict Flutter analysis policy with a --fatal-infos CI gate, not just dart analyze. Use when setting up a new Flutter repo, when flutter_lints feels too loose or CI analyze is noisy. Also use when a PR should not compile with missing returns.
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
