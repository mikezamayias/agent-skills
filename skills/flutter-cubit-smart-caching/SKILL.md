---
name: flutter-cubit-smart-caching
description: >-
  Add time-based smart caching to Flutter BlocCubit data cubits to prevent unnecessary reloads on navigation. Use when adding new cubits, fixing redundant API calls, or optimizing navigation performance in Flutter apps.
metadata:
  docs-verified: "2026-09-28"
  version: 1.0.0
---

# Flutter Cubit Smart Caching Pattern

Prevent unnecessary data reloads when users navigate between tabs/pages by adding time-based freshness checks to `Cubit` classes.

## The Problem

Flutter apps using `BlocProvider` at root level keep cubits alive across navigation. But pages often call `loadData()` in their `initState` or `_EmptyView`, triggering a full reload every time the user switches tabs. This causes:

- Unnecessary API/database calls
- Loading spinners on every tab switch
- Wasted bandwidth and battery

## The Pattern

Add three things to every data cubit:

### 1. Freshness Tracking

```dart
DateTime? _fetchedAt;
static const _staleAfter = Duration(minutes: 5);
```

### 2. Skip Logic in Load Method

```dart
Future<void> loadData({bool force = false}) async {
  // Skip if data is fresh (unless forced)
  if (!force && state is DataLoaded && _fetchedAt != null) {
    if (DateTime.now().difference(_fetchedAt!) < _staleAfter) {
      return;
    }
  }

  // Only show loading spinner on FIRST load
  if (state is! DataLoaded) {
    emit(const DataLoading());
  }

  // ... fetch data ...

  _fetchedAt = DateTime.now();
  emit(DataLoaded(data: result));
}
```

### 3. Force Refresh on Mutations

```dart
Future<void> addItem(Item item) async {
  await _repository.add(item);
  await loadData(force: true);  // Force refresh after mutation
}
```

## Key Decisions

| Decision         | Choice                                                     | Why                                                           |
| ---------------- | ---------------------------------------------------------- | ------------------------------------------------------------- |
| Refresh interval | 5 min for data, 30 min for expensive or rate-limited calls | Balances freshness vs cost                                    |
| Loading spinner  | Only on first load                                         | Users see stale data briefly rather than spinner on every tab |
| Force parameter  | Defaults to `false`                                        | Pages call without force; mutations call with `force: true`   |
| Cubit placement  | Root `MultiBlocProvider`                                   | Cubit persists across navigation, cache survives tab switches |

## Checklist

When adding smart caching to a cubit:

- [ ] Add `DateTime? _fetchedAt` field
- [ ] Add `static const _staleAfter` with appropriate duration
- [ ] Add `bool force = false` parameter to load method
- [ ] Add freshness check at top of load method
- [ ] Only emit Loading state on first load (`state is! DataLoaded`)
- [ ] Set `_fetchedAt = DateTime.now()` before emitting loaded state
- [ ] Add `force: true` to all mutation methods that need immediate refresh
- [ ] Ensure cubit is in root `MultiBlocProvider` (not created per-page)

## Anti-Patterns

- Constructing a cubit inside `build()`, such as `BlocProvider.value(value: DataCubit())`, which creates a new instance on every build
- Providing a data cubit per page with `BlocProvider(create: ...)`, which disposes the cubit and its cache when the page leaves the tree
- Calling `loadData()` unconditionally in every page's `initState`
- Showing loading spinner on every navigation (users see flicker)
- Not forcing refresh after add/delete/update mutations

## Sources

- <https://pub.dev/documentation/flutter_bloc/latest/flutter_bloc/BlocProvider-class.html>
