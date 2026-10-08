---
name: flutter-async-at-the-edge
description: >-
  Keep Flutter async work at a Service or Repository edge so views render synchronous sealed state. Use whenever a Flutter screen loads network, Firestore, stream or sensor data. Use for FutureBuilder or StreamBuilder in build(), refetching rebuilds, spinner storms or tests stuck on pumpAndSettle.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter async at the edge

App state does not live in widgets. Services talk to the network. Repositories retry, cache, and map. ViewModels expose **synchronous** sealed UI state. Views only switch on that state.

## Classify first

- **Ephemeral view state** (tab index, text field, animation) stays in the widget.
- **App state** (user, list, subscription, scores) does not.

## Ban this

```dart
Widget build(BuildContext context) {
  return FutureBuilder(
    future: api.fetchProfile(id), // new Future every rebuild
    builder: ...
  );
}
```

Creating the Future in `GoRoute.builder` has the same refetch bug. Caching the Future in `initState` plus `FutureBuilder` still collapses layers and traps data in `State`.

Official rule: do not create the Future in `build()`. Community "never use FutureBuilder" is stronger than the docs; follow the architecture below instead of arguing about the widget.

## Service at the edge

One class per API. Returns `Future`/`Stream`. Holds no cache.

```dart
class UserApi {
  UserApi(this._client);
  final http.Client _client;
  Future<UserDto> fetchProfile(String id) =>
      _client.get(Uri.parse('$base/users/$id')).then(parse);
}
```

## Repository: retry + cache + mapping

```dart
final _profileCache = AsyncCache<User>(const Duration(minutes: 5));

Future<User> profile(String id) => _profileCache.fetch(() {
  return retry(
    () => _api.fetchProfile(id).timeout(const Duration(seconds: 5)),
    retryIf: (e) => e is SocketException || e is TimeoutException,
  ).then(User.fromDto);
});
```

- `AsyncCache` is from `package:async`, not `dart:async`.
- `AsyncCache.ephemeral()` de-dupes in-flight calls without time-caching.
- `retryIf` must stay false for 401/403/404 or you hammer a dead endpoint.
- Catch `Exception`, not `Error`.

## ViewModel emits sealed state

Load in the constructor / `init`, not in `build`. `refresh()` invalidates the cache then re-fetches.

```dart
sealed class ProfileUi { const ProfileUi(); }
class ProfileLoading extends ProfileUi { const ProfileLoading(); }
class ProfileData extends ProfileUi { const ProfileData(this.user); final User user; }
class ProfileError extends ProfileUi { const ProfileError(this.message); final String message; }
```

The View switches on that state only. Zero `ConnectionState`, zero `snapshot.hasError`, zero HTTP.

Coordinate a screen with **one** ViewModel. Do not give each card its own FutureBuilder (spinner storm / layout shift).

## Tests

Inject a fake repository that returns `User` synchronously. Assert widgets on frame 1. Do not mock HTTP in widget tests.

Do not add BlocSignal (`package:bloc_signals`, Randal Schwartz's BLoC-on-signals library) or `package:signals` just for this.
Official Views + ViewModels + Repositories is enough.
If the project already uses signals, `futureSignal` is an acceptable edge wrapper.

## Sources

- <https://docs.flutter.dev/app-architecture/guide>
- <https://pub.dev/packages/retry>
- <https://pub.dev/documentation/async/latest/async/AsyncCache-class.html>
- <https://api.flutter.dev/flutter/widgets/FutureBuilder-class.html>
- <https://pub.dev/packages/bloc_signals>
- <https://github.com/RandalSchwartz/BlocSignal>
- <https://pub.dev/packages/signals>
- <https://pub.dev/documentation/signals/latest/signals/futureSignal.html>
