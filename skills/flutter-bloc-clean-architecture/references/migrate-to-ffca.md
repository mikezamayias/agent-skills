# Moving a single-package app to FFCA

Feature-First Clean Architecture (FFCA) is Very Good Ventures' layout of one pub workspace with `apps/`, `features/` and `shared/` folders and separate domain, data and presentation packages per feature.
The conventions themselves live in the `ffca-*` skills from VGV's vgv-ffca-plugin, starting with `ffca-architecture`.
This file covers only the move from a single package with `lib/features/<feature>/` folders.

Untangle the features inside the single package first, where moving a file is cheap and the app keeps building.
Extract packages only after the import graph already obeys the dependency rules, because a package boundary rejects every violation at once.

## 1. Map the import graph

Run this from the app's root, replacing `<app>` with the package name in `pubspec.yaml`:

```bash
for dir in lib/features/*/; do
  feature=$(basename "$dir")
  for layer in domain data presentation; do
    [ -d "$dir$layer" ] || continue
    grep -rhoE "package:<app>/features/[a-z_]+/(domain|data|presentation)/" "$dir$layer" \
      | grep -v "/features/$feature/" \
      | sed -E "s|package:<app>/features/([a-z_]+)/([a-z]+)/|$feature/$layer -> \1/\2|" \
      | sort -u
  done
done
```

Each line reads as "this feature's layer imports that feature's layer".
Also list imports of shared folders such as `lib/core/`, because those become shared packages or move into a feature.

## 2. Fix what packages will reject

Fix these inside the single package, one at a time, with the tests green after each:

| Finding                                                          | Fix                                                                                                                                                                                   |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A cycle between features, for example `a -> b -> a`              | Move the shared model or interface down into the lower feature's domain, or into a new small feature.                                                                                 |
| Presentation imports another feature's presentation              | Let the app place the widget through a slot, import it through a narrow barrel for that one widget, or compose the screens in a presentation-only feature (see `ffca-cross-feature`). |
| Any layer imports another feature's data                         | Depend on that feature's domain interface instead.                                                                                                                                    |
| Domain imports Flutter, a database, a network client or a plugin | Move the code into data, or put it behind a domain interface.                                                                                                                         |
| A service locator call outside the app                           | Pass the dependency through the screen module's constructor.                                                                                                                          |
| Navigation by string path inside a feature                       | Give the screen module a callback, and let the app navigate with typed routes (see `ffca-routing`).                                                                                   |
| A file in `lib/core/` used by one feature                        | Move it into that feature.                                                                                                                                                            |

## 3. Create the workspace

1. Move the app into `apps/<name>_app/` with `git mv`, so history follows the files.
2. Add the root `pubspec.yaml` with a `workspace:` list, and add `resolution: workspace` to the app.
   Pub workspaces need Dart 3.6 or later, and globs in the list need Dart 3.11 or later.
3. Update every path that pointed at the old location: CI working directories, Fastlane, signing and flavor scripts, Firebase or other platform config, and editor launch configurations.
4. Run `dart pub get` at the root, then the app's tests and a build for each platform it ships.

Commit this step on its own, because it touches every path and nothing else.

## 4. Extract packages

1. Extract shared packages first: UI kit, localizations, API client, database schema.
2. Extract features in dependency order, starting with features that depend on no other feature.
3. Within a feature, extract domain, then data, then presentation.
4. Create each package with `very_good create dart_package` (domain and data) or `very_good create flutter_package` (presentation).
5. Name the folder under `features/` after the package prefix.
   `features/import/` holds `import_domain`, `import_data` and `import_presentation`, never `anki_import_data`.
6. Move the files with `git mv` into the layer folders `ffca-architecture` names, such as `models/`, `repositories/`, `data_sources/`, `mappers/`, and `<screen>/bloc/` and `<screen>/views/`.
7. Rewrite imports from `package:<app>/features/<feature>/...` to the package barrel, for example `package:<feature>_domain/<feature>_domain.dart`.
8. Move the feature's tests into the package's `test/`.
9. After each package, run `dart pub get`, the FFCA validator with `--all`, `flutter analyze`, `very_good test --recursive`, and an app build.

Extract one feature per pull request so each review stays readable.

## 5. Finish

The move is done when:

- the app's `lib/` has no `features/` folder
- the FFCA validator reports no violations
- an `ffca-audit` run reports no violations
- only the app wires repositories into screen modules
