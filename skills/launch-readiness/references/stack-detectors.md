# Stack Detection Rules

How to detect each concern from `pubspec.yaml` dependencies.

## State Management

| Package            | Detection                       | Variant                                           |
| ------------------ | ------------------------------- | ------------------------------------------------- |
| `flutter_bloc`     | `dependencies.flutter_bloc`     | Check for `hydrated_bloc` → HydratedCubit pattern |
| `flutter_riverpod` | `dependencies.flutter_riverpod` | Check for `riverpod_annotation` → codegen pattern |
| `provider`         | `dependencies.provider`         | Basic ChangeNotifier                              |
| `get`              | `dependencies.get`              | GetX pattern                                      |
| `flutter_mobx`     | `dependencies.flutter_mobx`     | MobX observables                                  |

If none detected: assume StatefulWidget + setState.

## Analytics

| Package              | Detection                         | Event pattern                                |
| -------------------- | --------------------------------- | -------------------------------------------- |
| `posthog_flutter`    | `dependencies.posthog_flutter`    | Typed event constants, `Posthog().capture()` |
| `firebase_analytics` | `dependencies.firebase_analytics` | `FirebaseAnalytics.instance.logEvent()`      |
| `amplitude_flutter`  | `dependencies.amplitude_flutter`  | `amplitude.track(BaseEvent(...))`            |
| `mixpanel_flutter`   | `dependencies.mixpanel_flutter`   | `mixpanel.track()`                           |

## Crash Reporting

| Package                | Detection                           | Integration                                  |
| ---------------------- | ----------------------------------- | -------------------------------------------- |
| `sentry_flutter`       | `dependencies.sentry_flutter`       | `SentryFlutter.init()`, breadcrumbs, spans   |
| `firebase_crashlytics` | `dependencies.firebase_crashlytics` | `FirebaseCrashlytics.instance.recordError()` |

## Subscriptions

| Package             | Detection                        | Pattern                 |
| ------------------- | -------------------------------- | ----------------------- |
| `purchases_flutter` | `dependencies.purchases_flutter` | RevenueCat SDK          |
| `in_app_purchase`   | `dependencies.in_app_purchase`   | Native StoreKit/Billing |

## UI Framework

| Package     | Detection                                           | Implications                           |
| ----------- | --------------------------------------------------- | -------------------------------------- |
| `shadcn_ui` | `dependencies.shadcn_ui`                            | ShadApp, ShadTheme, LucideIcons        |
| Material    | Default (always available)                          | MaterialApp, ThemeData, Material icons |
| Cupertino   | `import 'package:flutter/cupertino.dart'` in source | CupertinoApp, CupertinoIcons           |

Check CLAUDE.md for banned imports.
If it bans a UI package, flag any import of that package.

## Navigation

| Package             | Detection                 | Screen detection                            |
| ------------------- | ------------------------- | ------------------------------------------- |
| `go_router`         | `dependencies.go_router`  | GoRoute path definitions                    |
| `auto_route`        | `dependencies.auto_route` | @RoutePage annotations                      |
| Navigator (default) | No routing package        | MaterialPageRoute/CupertinoPageRoute pushes |

## Dependency Injection

| Package    | Detection                | Pattern                                  |
| ---------- | ------------------------ | ---------------------------------------- |
| `get_it`   | `dependencies.get_it`    | Check for `injectable` → codegen pattern |
| `riverpod` | Same as state management | Provider-based DI                        |
| `provider` | Same as state management | Widget tree DI                           |

## Localization

| System              | Detection                                                   |
| ------------------- | ----------------------------------------------------------- |
| `intl` + ARB        | `l10n.yaml` exists, or `*.arb` files in `lib/l10n/`         |
| `easy_localization` | `dependencies.easy_localization`, `translations/` directory |
| `slang`             | `dependencies.slang`, `slang.yaml` or `i18n/` directory     |
| Manual              | Custom `AppLocalizations` class without above packages      |

## Testing

| Tool            | Detection                                                           |
| --------------- | ------------------------------------------------------------------- |
| `very_good_cli` | `dev_dependencies.very_good_analysis` or `very_good` in CI workflow |
| `flutter_test`  | Default (always available)                                          |
