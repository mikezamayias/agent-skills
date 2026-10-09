---
name: flutter-bloc-clean-architecture
description: >-
  Apply BLoC or Cubit with Clean Architecture layers, Very Good Ventures conventions and separate packages per feature layer. Use when scaffolding Flutter features or reviewing PRs that drift from this architecture.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Bash
metadata:
  docs-verified: "2026-09-28"
---

# Flutter — BLoC + Clean Architecture

## Stack

- BLoC/Cubit: primary state management
- Clean Architecture: data → domain → presentation
- Very Good Ventures tooling: CLI, analysis_options, coverage gate
- Riverpod: acceptable alternative
- Provider: legacy

## Layout (feature packages)

Each feature is split into `<feature>_domain`, `<feature>_data` and `<feature>_presentation` packages in one pub workspace, and the app only composes them.
Follow `feature-first-clean-architecture` for the tree, the dependency rules and the migration from a single package.

```text
apps/<name>_app/          # routing, dependency wiring, flavors
features/<feature>/
  <feature>_domain/       # models, repository interfaces
  <feature>_data/         # data sources, DTOs, repository implementations
  <feature>_presentation/ # cubit/bloc + views + screen modules
shared/                   # UI kit, database, localizations
```

## Required conventions

- `isClosed` guard after every `await` in cubits (see flutter-async-cubit-safety)
- Catch blocks log to Sentry (see flutter-error-logging-conventions)
- Time-based smart caching (see flutter-cubit-smart-caching)
- bloc_test + mocktail
- very_good_cli coverage gate

## State-mgmt decision tree

1. Stream of values, no event fan-out → Cubit
2. Multiple discrete user events → Bloc
3. Cross-feature shared state → Cubit + another feature's domain repository, wired by the app (get_it only in the app, NOT Provider)
4. Many-input derived UI → consider Riverpod (greenfield only)

## Provider lookups fail at runtime

`BlocProvider`, `context.read` and `context.watch` come from the `provider` package, which flutter_bloc depends on.
A lookup with no matching provider above it compiles and then throws `ProviderNotFoundException` at runtime, when the lookup runs.

- Provide each cubit at the route boundary, in the screen module that the route builder creates, for example in a go_router `builder`.
- Use `context.read` and `context.watch` only inside that route's subtree.
- Dialogs, bottom sheets and pushed pages build in a new route outside that subtree.
  Pass them the cubit through the constructor, or wrap their content in `BlocProvider.value`.
- Add a widget test per route that builds the page through the real router and its real providers, so a missing provider fails in CI instead of in production.

## When NOT to use

- Native (non-Flutter) apps
- Prototypes <2 weeks (use setState)

## Sources

Distilled from LinkedIn posts by Sebastian Röhl, Ethiel A., Dinko Marinac,
Krisztián Kemenes, Very Good Ventures, Stanislav Sydorenko, Vladimír Čimbora,
Taha Tesser, Cagatay Ulusoy, and Antonio Cappiello.

- <https://bloclibrary.dev/>
- <https://pub.dev/packages/very_good_cli>
- <https://pub.dev/packages/very_good_analysis>
- <https://pub.dev/packages/get_it>
