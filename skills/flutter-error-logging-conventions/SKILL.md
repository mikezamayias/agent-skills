---
name: flutter-error-logging-conventions
description: >-
  Enforces consistent error handling and logging patterns in Flutter apps. Use when reviewing catch blocks, adding error handling, or fixing silent failures. Prevents the catch (_) anti-pattern.
metadata:
  docs-verified: "2026-09-28"
  version: 1.0.0
---

# Flutter Error Logging Conventions

Ensure every error is captured, logged with context, and never silently swallowed.

## The Rule

**Never use `catch (_)`**. Always capture the exception and log it.

```dart
// BAD - silent failure, impossible to debug
catch (_) { return null; }

// GOOD - logged with service context
catch (e) {
  debugPrint('PRODUCT_SERVICE: Failed to fetch products: $e');
  return null;
}
```

## Logging Format

```text
PREFIX: Operation description: $e
```

- **PREFIX**: Uppercase service/class name for easy log filtering
- **Operation**: What was being attempted
- **$e**: The exception

### Examples

```dart
debugPrint('USER_SERVICE: Failed to load profile: $e');
debugPrint('CART_SERVICE: Failed to persist cart: $e');
debugPrint('SETTINGS_SECTION: Settings load failed: $e');
debugPrint('UPLOAD_SERVICE: Photo permission denied: $e');
debugPrint('SEARCH_CUBIT: Failed to save recent searches: $e');
```

## Common Prefixes

| Layer        | Prefix Pattern           | Example                             |
| ------------ | ------------------------ | ----------------------------------- |
| Services     | `{SERVICE_NAME}_SERVICE` | `USER_SERVICE`, `CART_SERVICE`      |
| Cubits       | `{FEATURE}_CUBIT`        | `SEARCH_CUBIT`, `PROFILE_CUBIT`     |
| Widgets      | `{WIDGET_NAME}`          | `SETTINGS_SECTION`, `ORDER_SUMMARY` |
| Repositories | `{FEATURE}_REPO`         | `ITEM_REPO`, `PROFILE_REPO`         |

## Patterns

### Service method that serves cache on failure

```dart
Future<List<Product>?> fetchProducts() async {
  try {
    return await _api.fetchProducts(category);
  } catch (e) {
    debugPrint('PRODUCT_SERVICE: Failed to fetch products: $e');
    return _getCachedProducts();  // Serve cached copy instead
  }
}
```

### Widget async init

```dart
Future<void> _initService() async {
  try {
    await _service.init();
    if (mounted) setState(() {});
  } catch (e) {
    debugPrint('MY_WIDGET: Service init failed: $e');
  }
}
```

### Cubit with Either result

```dart
final result = await _useCase(params);
result.fold(
  (failure) {
    debugPrint('FEATURE_CUBIT: Use case failed: ${failure.message}');
    emit(FeatureError(failure.message ?? 'Unknown error'));
  },
  (data) => emit(FeatureLoaded(data: data)),
);
```

## Audit Command

Find all `catch (_)` violations:

```bash
grep -rn "catch (_)" lib/
```

Find catch blocks without logging:

```bash
grep -rn -A2 "catch (e)" lib/ | grep -B1 "return\|rethrow" | grep -v "debugPrint"
```

## Widget Lifecycle Safety

When calling async methods from widget `initState()`:

1. Move to a separate `_initX()` async method (never await in initState)
2. Wrap in try/catch with logging
3. Check `mounted` before calling `setState` after the await

```dart
@override
void initState() {
  super.initState();
  _initSettings();  // Fire-and-forget
}

Future<void> _initSettings() async {
  try {
    await _service.init();
    if (mounted) setState(() {});
  } catch (e) {
    debugPrint('SETTINGS_SECTION: Settings load failed: $e');
  }
}
```

### After any await in a widget

- Check `mounted` before `setState` after every await, not only in `initState` paths.
- Use `context.mounted` before `Navigator`, `ScaffoldMessenger`, `showDialog` or any other use of a `BuildContext` after an await.
  Inside a `State`, the `use_build_context_synchronously` lint accepts the State's `mounted` for the State's own `context`.
  For a `BuildContext` passed in or held in a local variable, it requires that context's own `mounted` (dart.dev lint page, read 2026-11-03).
- Do not wrap `setState` in a try/catch to silence "setState() called after dispose()".
  The framework throws that error inside an `assert`, so it appears only in debug and profile builds.
  A release build skips it and fails later on `_element!.markNeedsBuild()`, so a catch hides a real failure (inference from reading `framework.dart` on master, read 2026-11-03).
- Prefer cancelling the timer, animation listener or stream subscription in `dispose()`, which the framework's own error text calls "the preferred solution".
  `mounted` is the fallback for a one-shot Future that cannot be cancelled.
- The `mounted` check stops UI work and does not cancel the request or its side effects, so do not rely on it for a payment or verification call that must finish.
  One reply on the source post reports a crash in a payment flow when the user left the screen mid verification call (single reply report).

## Sources

- <https://dart.dev/effective-dart/usage#error-handling>
- <https://docs.flutter.dev/testing/code-debugging>
