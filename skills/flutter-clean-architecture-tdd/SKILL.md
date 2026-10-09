---
name: flutter-clean-architecture-tdd
description: >-
  Build a Flutter feature test-first across its domain, data and presentation packages, one failing test at a time. Use when implementing, planning or reviewing a Flutter feature with TDD, or checking that each layer has tests. Also use when moving a Flutter app's local storage off Hive with tests first.
metadata:
  docs-verified: "2026-10-09"
---

# Flutter Clean Architecture TDD

Write each behavior's failing test before its code, starting in the domain package and moving outward.
The package layout, naming and dependency rules come from the `ffca-*` skills in VGV's vgv-ffca-plugin, starting with `ffca-architecture` and `ffca-feature`.
The state-management and stack conventions come from `flutter-bloc-clean-architecture`.

Load `references/tdd-feature-checklist.md` before implementation, code review or final verification.

## Intake

Before scaffolding a new app or feature, confirm these decisions, or state the choice the codebase already makes and ask whether to follow it:

1. State management: Cubit, Bloc with events, or the project's existing convention.
2. Backend: REST, GraphQL, Firebase, Supabase, a custom backend, local-only, or the existing backend.
3. Design system: Material 3, adaptive Material and Cupertino, a custom design system, or the existing one.

Do not silently pick a default for greenfield work.

## Workflow

1. Read the workspace root `pubspec.yaml`, the feature's packages, their tests, and the app's router and dependency wiring.
2. Name the feature's user-visible behavior and the packages it needs.
3. Write failing tests in the domain package first, then data, then presentation, then the app wiring.
4. Write the least code that makes each test pass.
5. Refactor only while the tests are green.
6. Run format, code generation, analysis and every package's tests before calling the work done.

## Rules

- Mock only across a package boundary.
  Command and Query tests mock repository interfaces, repository tests mock data sources, cubit tests mock domain repositories, Commands or Queries.
- Domain tests use `package:test` and import no Flutter, database or network package.
- Keep fixtures in the `test/fixtures/` folder of the package that reads them.
- Map infrastructure errors to domain failures in the data package, so no exception crosses a package boundary.
- Keep cubits to orchestration and state transitions, with no serialization, caching or network code.

## Hive projects

If any `pubspec.yaml` depends on `hive`, `hive_flutter`, `hive_ce` or `hive_ce_flutter`, tell the human the project should migrate its local storage to drift and ask whether to plan that migration now.
Do not add new Hive boxes, adapters or type IDs, even when the human defers the migration.

When the human agrees, migrate with tests first:

1. Add `drift`, `drift_flutter` and `path_provider`, plus `drift_dev` and `build_runner` as dev dependencies, in the package that owns local storage.
2. Model each Hive box as a drift table.
   Key-value caches become a table with a primary key column and a `blob()` or typed value column.
3. Keep the local data source interfaces unchanged, so repository and cubit tests keep passing while only the data source implementation changes.
4. Write a one-time importer that runs on first launch after the update.
   It reads every Hive box, writes the rows into drift in one transaction, and records completion in drift.
5. Test the importer against Hive fixtures, including empty boxes, corrupt entries, and a second run that must do nothing.
6. Delete the Hive boxes from disk only after the import succeeded.
7. Remove the Hive dependencies, adapters and generated code once the importer has shipped for at least one release.
8. Manage later schema changes with `dart run drift_dev make-migrations` and its generated migration tests.

## Review gate

Before finishing, verify:

- Tests were written before or alongside the code for every changed behavior.
- Each changed package has focused tests at its own level.
- No DTO or generated type appears in a domain API, a cubit state or a widget.
- Generated code is current.
- `dart format`, `flutter analyze` and `very_good test --recursive` pass, or the blocker is reported.

## Sources

- <https://pub.dev/packages/bloc_test>
- <https://pub.dev/packages/mocktail>
- <https://pub.dev/packages/drift>
- <https://drift.simonbinder.eu/migrations/>
- <https://cli.vgv.dev/>
