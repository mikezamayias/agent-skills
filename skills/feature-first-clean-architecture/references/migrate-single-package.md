# Splitting a single-package app

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

| Finding                                                          | Fix                                                                                                          |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| A cycle between features, for example `a -> b -> a`              | Move the shared model or interface down into the lower feature's domain, or into a new small domain package. |
| Presentation imports another feature's presentation              | Compose the screens in the app's router, or move the composing screen into a presentation-only feature.      |
| Any layer imports another feature's data                         | Depend on that feature's domain interface instead.                                                           |
| Domain imports Flutter, a database, a network client or a plugin | Move the code into data, or put it behind a domain interface.                                                |
| A service locator call outside the composition root              | Pass the dependency through a constructor.                                                                   |
| A file in `lib/core/` used by one feature                        | Move it into that feature.                                                                                   |

## 3. Create the workspace

1. Move the app into `apps/<name>_app/` with `git mv`, so history follows the files.
2. Add the root `pubspec.yaml` with `workspace:` and add `resolution: workspace` to the app.
3. Update every path that pointed at the old location: CI working directories, Fastlane, signing and flavor scripts, Firebase or other platform config, and editor launch configurations.
4. Run `dart pub get` at the root, then the app's tests and a build for each platform it ships.

Commit this step on its own, because it touches every path and nothing else.

## 4. Extract packages

1. Extract shared packages first: database schema, UI kit, localizations, API client.
2. Extract features in dependency order, starting with features that depend on no other feature.
3. Within a feature, extract domain, then data, then presentation.
4. Create each package with `very_good create dart_package` or `very_good create flutter_package`, then move the files with `git mv` into `lib/src/`.
5. Rewrite imports from `package:<app>/features/<feature>/...` to the package barrel, for example `package:<feature>_domain/<feature>_domain.dart`.
6. Move the feature's tests into the package's `test/`.
7. After each package: `dart pub get`, `dart analyze`, `very_good test --recursive`, and an app build.

Extract one feature per pull request so each review stays readable.

## 5. Finish

The split is done when:

- the app's `lib/` has no `features/` folder
- only the app imports a service locator
- every feature and shared package has its own tests
- no presentation package lists a `_data` package in its `pubspec.yaml`
