---
name: flutter-router-decision
description: >-
  Choose Flutter routing, defaulting to go_router, with guidance on auth redirects, deep links and nested tabs. Use when starting routing on a new Flutter app or when someone claims go_router is in maintenance mode. Use before adding zenrouter, navigation_utils or auto_route to an app that already uses go_router.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter router decision

Check pub.dev, not Twitter.
As of 2026-09-28: **go_router 18.0.1**, publisher flutter.dev, feature-complete = bugfix-stable, **not abandoned**.
Changelog tracks Flutter 3.44.

## Default

Stay on (or start with) **go_router**. Use Flutter's official declarative routing skill for bootstrap, deep links, and `StatefulShellRoute`.

Leave go_router only with a concrete need:

| Need                                                                | Choose                                             |
| ------------------------------------------------------------------- | -------------------------------------------------- |
| URL + deep links + nested tabs, standard app                        | go_router                                          |
| Type-safe `RouteTarget` + mixins, no codegen, Coordinator URI parse | zenrouter                                          |
| Codegen typed routes on top of go_router                            | go_router + go_router_builder                      |
| "go_router is dead" rumor                                           | **do not migrate**                                 |
| navigation_utils                                                    | **do not pick as default** (nested nav still BETA) |

go_router 18 requires Flutter 3.44 / Dart 3.12. Don't bump the package without bumping the SDK.

## Auth redirect

```dart
redirect: (context, state) {
  final loggedIn = auth.currentUser != null;
  final loggingIn = state.matchedLocation == '/login';
  if (!loggedIn && !loggingIn) return '/login';
  if (loggedIn && loggingIn) return '/';
  return null;
},
redirectLimit: 5,
```

## Deep links and extra

`extra` is **not** in the URL. Don't put objects that must survive a web refresh or a cold-start deep link in `extra`. Put an id in the path and rehydrate from a repository.

## Nested tabs

`StatefulShellRoute.indexedStack` + `navigationShell.goBranch(index, initialLocation: index == current)`. Child paths omit the leading `/`.

Creating Futures inside route `builder`s causes the Future to be recreated and refetched on every rebuild. Load in a ViewModel instead.

## If (and only if) zenrouter Coordinator

Implement `parseRouteFromUri`, give every route `RouteUnique.toUri()`, use `RouteGuard`/`RouteRedirect` mixins, wire `MaterialApp.router(routerConfig: coordinator)`. Imperative `NavigationPath` is enough when you do not need URLs.

## Sources

- <https://pub.dev/packages/go_router>
- <https://pub.dev/packages/zenrouter>
- <https://pub.dev/packages/go_router/changelog>
- <https://pub.dev/documentation/go_router/latest/go_router/StatefulNavigationShell/goBranch.html>
- <https://pub.dev/packages/navigation_utils>
