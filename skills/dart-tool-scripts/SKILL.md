---
name: dart-tool-scripts
description: >-
  Move growing shell logic into `tool/*.dart` scripts run with `dart run` instead of Bash. Use when a GitHub Actions step or repo bootstrap grows branches, loops, JSON, test sharding or macOS versus Linux sed.
metadata:
  docs-verified: "2026-09-28"
---

# Dart tool scripts

Keep Bash/Make for single commands: `dart format .`, `dart analyze`, `flutter test`.

The moment the script has branches, JSON, sharding, or portable path logic, put it in `tool/<name>.dart` and run `dart run tool/<name>.dart`.

## Rules

1. Parse args in Dart (`package:args`), not `shift` / positional bash.
2. Prefer calling Dart APIs over shelling out (typed config, e.g. ffigen `FfiGenerator(...)`).
3. Use `dart:io` `Platform.isWindows` and `package:path`. Never assume GNU `sed`.
4. Package authors: export a function main so other CLIs can import it without spawning a process.
5. Don't rewrite `flutter test` itself. Wrap selection, sharding, and coverage around it.
6. `dart run` from a Flutter repo needs an SDK constraint the CI image actually has.

## CI sharding

```yaml
strategy:
  matrix: { shard: [0, 1, 2] }
steps:
  - uses: dart-lang/setup-dart@v1
  - run: dart run tool/shard_tests.dart --index ${{ matrix.shard }} --total 3
```

A 10-line bash pipe is still fine. This skill starts when the script has branches.

## Sources

- <https://lazebny.io/i-stopped-writing-bash-scripts/>
- <https://dart.dev/tools/dart-run>
- <https://pub.dev/packages/args>
- <https://pub.dev/packages/ffigen>
- <https://github.com/dart-lang/setup-dart>
