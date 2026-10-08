---
name: flutter-bloc-clean-architecture
description: >-
  Apply BLoC or Cubit with Clean Architecture layers, Very Good Ventures conventions and a feature-first layout. Use when scaffolding Flutter features or reviewing PRs that drift from this architecture.
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

## Layout (feature-first)

```text
lib/
  features/<feature>/
    data/         # repos, data sources, DTOs
    domain/       # entities, use cases, contracts
    presentation/ # cubit/bloc + widgets + screens
  core/
    di/ error/ network/ theme/
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
3. Cross-feature shared state → Cubit + repo via get_it (NOT Provider)
4. Many-input derived UI → consider Riverpod (greenfield only)

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
