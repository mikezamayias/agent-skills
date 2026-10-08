# TDD Feature Checklist

Use this order when adding a new feature. Keep each step small enough that a failing test identifies one missing behavior.

## Intake

Before creating files, identify:

- Feature name and route or entry point.
- User-visible behavior.
- API endpoint or local data source.
- Entity fields and validation rules.
- Cache behavior and invalidation.
- Loading, empty, success, and failure UI states.
- Localization strings.

## Phase 1: Domain Layer

1. Write `test/features/<feature>/domain/entities/<feature>_entity_test.dart`.
2. Implement `lib/features/<feature>/domain/entities/<feature>_entity.dart`.
3. Write `test/features/<feature>/domain/repositories/<feature>_repository_test.dart` only when repository contract behavior needs documentation.
4. Define `lib/features/<feature>/domain/repositories/<feature>_repository.dart`.
5. Write `test/features/<feature>/domain/usecases/<action>_<feature>_usecase_test.dart`.
6. Implement `lib/features/<feature>/domain/usecases/<action>_<feature>_usecase.dart`.

Domain tests should not import Flutter, Dio, drift, FlatBuffers, or generated DTOs.

## Phase 2: Data Layer

1. Define or update FlatBuffer schema in `lib/core/fbs/` or the feature's data model folder.
2. Generate FlatBuffer Dart accessors.
3. Add or update binary fixtures in `test/fixtures/`.
4. Write data-source tests under `test/features/<feature>/data/sources/`.
5. Implement remote and local data sources.
6. Write repository implementation tests under `test/features/<feature>/data/implements/`.
7. Implement repository orchestration, failure mapping, caching, and DTO-to-entity conversion.

Repository tests should prove:

- Cache hit returns the expected entity without network access.
- Cache miss fetches remote data and caches bytes when appropriate.
- Server, cache, and parse failures map to the correct `Failure`.
- Generated DTOs do not leak from the repository interface.

## Phase 3: Presentation Layer

1. Write Cubit tests under `test/features/<feature>/presentation/cubit/`.
2. Implement Cubit and states.
3. Write page or widget tests under `test/features/<feature>/presentation/pages/` or `widgets/`.
4. Implement screens and feature widgets.

Cubit tests should cover:

- Initial state.
- Loading -> success.
- Loading -> empty when applicable.
- Loading -> failure.
- Refresh or retry behavior.
- Cancellation or closed-Cubit guards after awaits if the existing codebase requires them.

Widget tests should cover:

- Initial render.
- Loading indicator.
- Empty state.
- Error state and retry.
- Successful data render.
- Key user interaction and navigation.

## Phase 4: Integration and Wiring

1. Register data sources, repositories, use cases, and Cubits in DI.
2. Add routes and route tests when routing logic is non-trivial.
3. Add localization keys and regenerate l10n when needed.
4. Add integration tests for the critical feature flow.
5. Update fixtures, helpers, fakes, and test setup.

## Verification Commands

Run the applicable subset:

```bash
flatc --dart -o lib/core/fbs/generated/ lib/core/fbs/*.fbs
dart run build_runner build
dart format lib/ test/
flutter analyze
flutter test
```

When only one feature changed, run the focused tests first, then broaden to the full suite if shared wiring changed.

## Review Checklist

- Domain APIs contain no infrastructure types.
- Tests match the behavior the user requested, not only implementation details.
- Generated files are current.
- `Either<Failure, T>` is folded in presentation and not ignored.
- Mocks are reset between tests.
- Fixture data is deterministic.
- UI states are reachable and covered by tests.
- No unrelated refactors or package changes are bundled into the feature.
