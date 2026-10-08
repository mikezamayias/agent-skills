---
name: flutter-error-logging-conventions
description: >-
  Enforce consistent error handling and logging patterns in Flutter apps. Use when reviewing catch blocks, adding error handling, or fixing silent failures. Prevents the catch (_) anti-pattern.
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
debugPrint('ONBOARDING_CUBIT: Failed to save preferences: $e');
```

## Common Prefixes

| Layer        | Prefix Pattern           | Example                             |
| ------------ | ------------------------ | ----------------------------------- |
| Services     | `{SERVICE_NAME}_SERVICE` | `USER_SERVICE`, `CART_SERVICE`      |
| Cubits       | `{FEATURE}_CUBIT`        | `ONBOARDING_CUBIT`, `PROFILE_CUBIT` |
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

## Sources

- <https://dart.dev/effective-dart/usage#error-handling>
- <https://docs.flutter.dev/testing/code-debugging>
