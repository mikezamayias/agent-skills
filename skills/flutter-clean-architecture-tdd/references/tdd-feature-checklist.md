# TDD feature checklist

Use this order when adding a feature.
Keep each step small enough that one failing test points at one missing behavior.
Paths assume the layout in `feature-first-clean-architecture`, with the feature at `features/<feature>/`.

## Intake

Before creating files, identify:

- the feature name and its route or entry point
- the user-visible behavior
- the API endpoint or local data source
- model fields and validation rules
- cache behavior and invalidation
- loading, empty, success and failure UI states
- localization strings
- which packages the feature needs: domain only, domain and data, presentation only, or all three

## Phase 1: Domain package

1. Write `<feature>_domain/test/src/models/<model>_test.dart`.
2. Implement `<feature>_domain/lib/src/models/<model>.dart`.
3. Define `<feature>_domain/lib/src/repositories/<feature>_repository.dart` as an `abstract interface class`.
4. When a rule combines several repositories, write `<feature>_domain/test/src/use_cases/<action>_test.dart`, then implement the use case.
5. Export the public API from `<feature>_domain/lib/<feature>_domain.dart`.

Domain tests import no Flutter, database, network or generated DTO code.

## Phase 2: Data package

1. Add fixtures under `<feature>_data/test/fixtures/`.
2. Write data source tests under `<feature>_data/test/src/data_sources/`.
3. Implement the remote and local data sources.
4. Write mapper tests under `<feature>_data/test/src/mappers/`, then the mappers.
5. Write repository tests under `<feature>_data/test/src/repositories/`, with the data sources mocked.
6. Implement the repository: source selection, caching, failure mapping and DTO-to-model conversion.

Repository tests should prove:

- A cache hit returns the expected model without network access.
- A cache miss fetches remote data and caches it when appropriate.
- Server, cache and parse failures map to the right domain failure.
- No DTO or generated type leaks from the repository interface.

## Phase 3: Presentation package

1. Write cubit or bloc tests under `<feature>_presentation/test/src/<screen>/bloc/`, with the domain repository mocked.
2. Implement the cubit or bloc and its states.
3. Write view tests under `<feature>_presentation/test/src/<screen>/views/`, with the cubit mocked.
4. Implement the views and the screen module.

Cubit tests should cover:

- the initial state
- loading to success
- loading to empty, when applicable
- loading to failure
- refresh or retry
- no emit after close, when an `await` precedes an `emit`

View tests should cover:

- initial render
- loading indicator
- empty state
- error state and retry
- successful data render
- the key user interaction and the navigation callback it fires

## Phase 4: App wiring

1. Construct the data implementation in the app's composition root and expose it as the domain interface.
2. Add the route that creates the screen module, and a route test that builds the page through the real router.
3. Add localization keys and regenerate localizations.
4. Add an integration test for the critical flow.

## Verification commands

Run from the workspace root:

```bash
dart format .
flutter analyze
very_good test --recursive
```

Run `dart run build_runner build` inside each package whose generated code changed.
When only one package changed, run its tests first, then the full workspace if wiring or shared packages changed.

## Review checklist

- Domain APIs contain no infrastructure types.
- Tests check the behavior the user asked for, not only implementation details.
- Generated files are current.
- Mocks are reset between tests.
- Fixture data is deterministic.
- Every UI state is reachable and tested.
- No unrelated refactor or dependency change is bundled into the feature.
