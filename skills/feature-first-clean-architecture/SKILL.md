---
name: feature-first-clean-architecture
description: >-
  Structure a Flutter app as a pub workspace with separate domain, data and presentation packages for each feature. Use when scaffolding a Flutter app, feature or package, or reviewing package boundaries and dependency direction. Also use when splitting a single-package Flutter app into feature packages.
metadata:
  provenance: local
  docs-verified: "2026-10-09"
---

# Feature-first clean architecture

Split each feature into up to three Dart packages in one pub workspace, and keep the app as a thin shell that composes them.
A package boundary is enforced by the toolchain: importing a package that is not in `pubspec.yaml` fails analysis.
Layer rules then hold without anyone remembering them, and an agent always knows which package a file belongs in.

This follows Very Good Ventures' Feature-First Clean Architecture (FFCA) guide.
Read `references/package-layout.md` before creating packages or moving files.
Read `references/migrate-single-package.md` before splitting an existing app.

A single package with `lib/features/<feature>/` folders is acceptable only for a prototype or an app with fewer than three features.

## Repository shape

```text
<repo>/
  pubspec.yaml                  # workspace root: lists every package
  apps/
    <name>_app/                 # Flutter: entry points, flavors, routing, dependency wiring
  features/
    <feature>/
      <feature>_domain/         # Dart: models, repository interfaces, business rules
      <feature>_data/           # Dart: data sources, DTOs, mappers, repository implementations
      <feature>_presentation/   # Flutter: blocs or cubits, views, one module per screen
  shared/
    <name>/                     # generic code that knows no feature: UI kit, API client, database
```

## Packages in a feature

| Package                  | Holds                                                              | Never holds                                  |
| ------------------------ | ------------------------------------------------------------------ | -------------------------------------------- |
| `<feature>_domain`       | models, repository interfaces, use cases that combine repositories | Flutter, database, network or plugin imports |
| `<feature>_data`         | data sources, DTOs, mappers, repository implementations            | widgets, blocs                               |
| `<feature>_presentation` | blocs or cubits, views, screen modules                             | data sources, DTOs, generated database types |

- Create only the packages a feature needs.
  A headless feature such as auth or analytics has domain and data only.
  A presentation-only feature such as a dashboard composes other features' domain packages.
- Name a data package after its backend when there could be more than one, for example `auth_data_firebase`.
- Make data a Flutter package only when a plugin it uses requires Flutter.

## Dependency rules

```text
<feature>_presentation ──> <feature>_domain <── <feature>_data
            ^                                         ^
            └───────────── apps/<name>_app ───────────┘
```

1. Domain depends on no other layer.
2. Presentation never depends on any `_data` package, including its own feature's.
   The app builds the data implementations and passes them in as domain interfaces.
3. A feature may depend on another feature's domain package.
   It never depends on another feature's data package.
4. Presentation depends on another feature's presentation package only through a dedicated entry-point library for one screen.
   Prefer composing the two screens in the app or in a presentation-only feature.
5. Shared packages never import a feature package.
6. No dependency cycles at any layer.
   Break a cycle by moving the shared concept down into the lower feature's domain, or into a new small domain package.
7. Generated types, such as database rows, DTOs and JSON classes, never leave the data package.
8. Only the app uses a service locator such as `get_it`.
   Feature packages receive dependencies through constructors.

## Screens and the app

- Each screen in a presentation package exposes a module widget.
  The module takes domain interfaces and navigation callbacks through its constructor and builds its own `BlocProvider` tree.
- The app's router creates each module in its route builder and passes callbacks that navigate.
  Routing stays in the app, and every provider lookup stays inside the module's subtree (see `flutter-bloc-clean-architecture`).
- The app owns entry points, flavors, environment configuration, the router, dependency wiring and observability setup.
  Feature code does not live in the app.

## Tooling

- Use pub workspaces, which need Dart 3.6 or later: the root `pubspec.yaml` lists members under `workspace:`, and each member declares `resolution: workspace`.
  One `pubspec.lock` at the root resolves every package to the same versions.
- Scaffold packages with `very_good create dart_package` and `very_good create flutter_package`.
- Run every package's tests with `very_good test --recursive`.
- Keep `very_good_analysis` (or at least the `depend_on_referenced_packages` and `implementation_imports` lints) on in every package, because those two lints enforce the boundaries.

## Review checklist

- [ ] Every new file has one feature owner and one layer owner.
- [ ] No presentation package lists a `_data` package in its `pubspec.yaml`.
- [ ] No domain package imports Flutter, a database, a network client or a plugin.
- [ ] Cross-feature dependencies point at domain packages, and no cycle exists.
- [ ] Shared packages import no feature.
- [ ] No DTO or generated type appears in a domain API, a bloc state or a widget.
- [ ] Only the app references the service locator.
- [ ] Each changed package has its own tests, and `very_good test --recursive` passes.
- [ ] No empty layer or pass-through abstraction was added.

## Sources

- <https://engineering.verygood.ventures/architecture/ffca/overview/>
- <https://engineering.verygood.ventures/architecture/ffca/project_structure/>
- <https://verygood.ventures/blog/feature-first-clean-architecture/>
- <https://dart.dev/tools/pub/workspaces>
- <https://cli.vgv.dev/>
