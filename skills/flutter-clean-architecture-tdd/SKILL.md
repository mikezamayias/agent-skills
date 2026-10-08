---
name: flutter-clean-architecture-tdd
description: >-
  Build, scaffold, plan or review Flutter apps with Clean Architecture, TDD, feature-first modules and BLoC or Cubit. Covers GetIt, FlatBuffers, dart_mappable, dartz Either, Hive and GoRouter with full test coverage. Use when creating a Flutter project or feature, designing layer boundaries, or reviewing repository architecture.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter Clean Architecture TDD

Use this skill to create or review Flutter work that should follow feature-first Clean Architecture with strict test-first implementation.

## References

- Load `references/core-architecture.md` before designing a project, scaffold, or feature architecture.
- Load `references/customization-matrix.md` when stack choices are open or the project differs from the defaults.
- Load `references/tdd-feature-checklist.md` before implementation, code review, or final verification.

## Required Intake

Before scaffolding a new app, creating a feature architecture, or making architecture-level choices, ask or confirm these three decisions:

1. State management: BLoC/Cubit, Bloc with events, Riverpod, Provider/ChangeNotifier, or existing project convention.
2. Backend: REST, GraphQL, Firebase, Supabase, custom backend, local-only/mock data, or existing backend.
3. Frontend design system: Material 3, adaptive Material/Cupertino, Shadcn-style Flutter components, custom design system, or existing project convention.

If the existing codebase already makes one of these decisions obvious, state the inferred choice and ask whether to follow it. Do not silently default for greenfield work.

## Defaults

When the existing project does not already choose a different pattern, default to:

- State: `flutter_bloc` with one Cubit per screen or feature workflow.
- Dependency injection: `get_it`.
- Networking: `dio`.
- Serialization: FlatBuffers for DTOs and wire/cache bytes.
- Domain entities: `dart_mappable` classes.
- Result handling: `Either<Failure, T>` from `dartz`.
- Local storage: `drift` (SQLite) through `drift_flutter`, storing raw FlatBuffer bytes in `blob()` columns where practical.
- Routing: `go_router`.
- Localization: Flutter built-in l10n with ARB files.
- Tests: `flutter_test`, `bloc_test`, `mocktail`, fixtures under `test/fixtures/`.

Prefer existing project conventions over these defaults when a codebase is already established.
Hive is the exception: steer projects off it.

## Hive Projects

If `pubspec.yaml` depends on `hive`, `hive_flutter`, `hive_ce`, or `hive_ce_flutter`, tell the human the project should migrate its local storage to drift and ask whether to plan that migration now.
Do not add new Hive boxes, adapters, or type IDs, even when the human defers the migration.

When the human agrees, migrate with tests first:

1. Add `drift`, `drift_flutter`, and `path_provider`, plus `drift_dev` and `build_runner` as dev dependencies.
2. Model each Hive box as a drift table.
   Key-value caches become a table with a primary key column and a `blob()` or typed value column.
3. Keep the local data source interfaces unchanged, so repository and Cubit tests keep passing while only the data source implementation changes.
4. Write a one-time importer that runs on first launch after the update.
   It reads every Hive box, writes the rows into drift in one transaction, and records completion in drift.
5. Test the importer against Hive fixtures, including empty boxes, corrupt entries, and a second run that must do nothing.
6. Delete the Hive boxes from disk only after the import succeeded.
7. Remove the Hive dependencies, adapters, and generated code once the importer has shipped for at least one release.
8. Manage later schema changes with `dart run drift_dev make-migrations` and its generated migration tests.

## Workflow

1. Inspect `pubspec.yaml`, `lib/`, `test/`, existing feature folders, state management, DI, routing, storage, and code generation setup.
2. Ask or confirm the required intake decisions: state management, backend, and frontend design system.
3. Identify the feature boundary and public behavior before writing implementation code.
4. Write failing tests first, starting with the domain layer and moving outward.
5. Implement the minimum code needed for each test to pass.
6. Refactor only after tests are green, keeping generated DTOs out of domain and presentation layers.
7. Register dependencies, routes, localization keys, and fixtures only when the feature needs them.
8. Run format, generation, static analysis, and tests before marking the work complete.

## Layer Rules

- Keep `data`, `domain`, and `presentation` dependencies one-way: presentation -> domain -> data contracts, with data implementing domain repositories.
- Keep generated FlatBuffer classes inside the data boundary. Convert to domain entities before returning from repositories.
- Do not throw exceptions across layer boundaries. Map infrastructure errors into `Failure` types.
- Keep use cases single-purpose and test them against repository interfaces.
- Keep Cubits focused on orchestration and state transitions. Do not put serialization, caching, or network details in Cubits.
- Store binary fixtures for FlatBuffer tests in `test/fixtures/`.

## Review Gate

Before finishing, verify:

- Tests were written before or alongside implementation for every changed behavior.
- Data sources, repositories, use cases, Cubits, and widgets have focused tests at the right level.
- No DTO or generated FlatBuffer type leaks into UI widgets, Cubit public state, or domain APIs.
- Code generation output is current when schemas, `dart_mappable`, drift, routes, or injectable code changed.
- `dart format`, `flutter analyze`, and relevant `flutter test` commands pass or any blocker is reported.

## Sources

- <https://pub.dev/packages/build_runner/changelog>
- <https://pub.dev/packages/dart_mappable>
- <https://pub.dev/packages/dart_mappable/changelog>
- <https://flatbuffers.dev/languages/dart/>
- <https://pub.dev/packages/dartz>
- <https://pub.dev/packages/drift>
- <https://drift.simonbinder.eu/setup/>
- <https://drift.simonbinder.eu/dart_api/tables/>
- <https://drift.simonbinder.eu/migrations/>
- <https://drift.simonbinder.eu/platforms/web/>
