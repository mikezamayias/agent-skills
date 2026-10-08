---
name: flutter-async-cubit-safety
description: >-
  Prevent "emit after close" crashes in Flutter BlocCubit by adding isClosed guards after every await. Use when writing async cubit methods, fixing Sentry StateError crashes, or reviewing cubit lifecycle safety.
metadata:
  docs-verified: "2026-09-28"
  version: 1.0.0
---

# Flutter Async Cubit Safety

Prevent `StateError: Cannot emit new states after calling close` crashes by guarding every `emit()` after an `await`.

## The Problem

When a Cubit has async methods with multiple `await` calls, the cubit can be disposed (closed) while an async operation is in flight. The async continuation then runs and calls `emit()` on a closed cubit, causing:

```text
StateError: Cannot emit new states after calling close
```

This is a top Sentry crash pattern in Flutter apps. It happens when:

- User navigates away while data is loading
- Widget tree rebuilds and old cubit is disposed
- App goes to background during async operations

## The Fix

Add `if (isClosed) return;` after **every** `await` in cubit methods:

```dart
Future<void> loadData() async {
  emit(const DataLoading());

  final result1 = await _service.fetchFirst();
  if (isClosed) return;  // Guard #1

  final result2 = await _service.fetchSecond(result1);
  if (isClosed) return;  // Guard #2

  final result3 = await _service.fetchThird(result2);
  if (isClosed) return;  // Guard #3

  emit(DataLoaded(data: result3));
}
```

## Rules

1. **Every `await` needs a guard** - even if the next line isn't `emit()`, because later code may depend on cubit being open
2. **Guard immediately after the await** - before any other logic
3. **Use `return`, not `throw`** - silently bail out, the cubit is already disposed
4. **Also guard `refresh()` methods** - they typically call the load method internally

## Common Patterns

### Sequential awaits

```dart
final profile = await _userService.fetchProfile();
if (isClosed) return;

final feed = await _feedService.fetchFeed(profile.id);
if (isClosed) return;

emit(Loaded(profile: profile, feed: feed));
```

### Try-catch with awaits

```dart
try {
  final data = await _repo.fetch();
  if (isClosed) return;
  emit(Loaded(data));
} catch (e) {
  if (isClosed) return;  // Also guard in catch!
  emit(Error(e.toString()));
}
```

### Refresh that calls load

```dart
Future<void> refresh() async {
  await _service.clearCache();
  if (isClosed) return;
  await loadData(force: true);
  // No guard needed here - loadData has its own guards
}
```

## Checklist

When writing or reviewing async cubit methods:

- [ ] Identify every `await` in the method
- [ ] Add `if (isClosed) return;` after each one
- [ ] Check catch blocks for emits after awaits
- [ ] Check refresh/retry methods that call load methods
- [ ] Search for `emit(` and verify each has a guard if preceded by `await`

## Detection

Search for cubits missing guards:

```bash
# Find async cubit methods
grep -rn "Future<void>.*async" lib/features/*/presentation/cubit/

# Find emits after awaits (manual review needed)
grep -rn "emit(" lib/features/*/presentation/cubit/ | grep -v "isClosed"
```

## Sources

- <https://github.com/felangel/bloc/blob/master/packages/bloc/lib/src/bloc_base.dart>
- <https://pub.dev/documentation/bloc/latest/bloc/BlocBase/isClosed.html>
