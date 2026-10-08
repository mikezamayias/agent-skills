---
name: flutter-observability-instrumentation
description: >-
  Implement type-safe analytics, tracing, metrics and breadcrumbs in Flutter apps with Sentry and PostHog. Use when adding observability to a new project, instrumenting features, or auditing telemetry for magic strings.
metadata:
  docs-verified: "2026-09-28"
  version: 1.0.0
---

# Flutter Observability Instrumentation

Build a type-safe, consent-aware observability layer with enums for all telemetry names and a clean service abstraction over Sentry.

## When to Use

- Setting up analytics/observability from scratch in a Flutter app
- Adding tracing, metrics, or breadcrumbs to an existing app
- Replacing raw string `trackEvent('event_name')` calls with type-safe enums
- Auditing existing telemetry for magic strings or inconsistencies

## Architecture Overview

```text
core/observability/
├── observability.dart              # Barrel export
├── events.dart                     # AnalyticsEvent enum — all trackEvent() names
├── spans.dart                      # SpanOp + TransactionName enums — Sentry tracing
├── metrics.dart                    # MetricName enum — Sentry custom metrics
├── breadcrumbs.dart                # BreadcrumbCategory enum — Sentry breadcrumbs
├── attributes.dart                 # TelemetryKeys static constants — span data keys
├── i_observability_service.dart    # Abstract interface (DI-friendly)
└── observability_service.dart      # Concrete Sentry implementation
```

### Principles

| Principle                | Application                                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| **No Magic Strings**     | Every event name, span op, metric name, breadcrumb category, and attribute key is an enum or constant                    |
| **Dependency Inversion** | Cubits/services depend on `TelemetryService` (abstract), not Sentry directly                                             |
| **Consent-Aware**        | All methods check `isEnabled` before calling Sentry APIs; no-op when disabled                                            |
| **NoOp Pattern**         | `_DisabledSpan` implements `ISentrySpan` so callers don't need null-checks when disabled                                 |
| **Separation**           | `AnalyticsService` handles event tracking (PostHog); `ObservabilityService` handles tracing/metrics/breadcrumbs (Sentry) |

## Step-by-Step Implementation

### Step 1: Dependencies & SDK Setup

```yaml
# pubspec.yaml
dependencies:
  sentry_flutter: ^9.0.0
  posthog_flutter: ^5.0.0 # or latest
```

```dart
// main.dart — SentryFlutter.init options
options.tracesSampleRate = isProduction ? 0.1 : 1.0;
options.enableAutoPerformanceTracing = true;  // auto app start, slow/frozen frames
```

**Auto-instrumentation (free spans with zero code):**

```dart
// app_router.dart — add SentryNavigatorObserver for auto page load transactions
GoRouter(
  observers: [
    YourAnalyticsRouteObserver(),
    SentryNavigatorObserver(),
  ],
)
```

### Step 2: Create Enum Files

#### `events.dart` — Analytics Event Names

Group by feature. Every `trackEvent()` call uses this enum.

```dart
/// All analytics event names used with `trackEvent()`.
/// Add new events here — never use raw strings for event names.
enum AnalyticsEvent {
  // Auth
  authLoginStarted('auth_login_started'),
  authLoginSuccess('auth_login_success'),
  authLoginFailed('auth_login_failed'),
  authLogout('auth_logout'),

  // Navigation
  screenView('screen_view'),

  // Feature-specific events...
  ;

  const AnalyticsEvent(this.value);
  final String value;
}
```

#### `spans.dart` — Sentry Span Operations & Transaction Names

```dart
/// Span operation names for Sentry tracing.
enum SpanOp {
  // Checkout
  checkoutSubmit('checkout.submit'),
  paymentRequest('payment.request'),

  // HTTP
  httpClient('http.client'),

  // Upload
  uploadFile('upload.file'),
  uploadAttempt('upload.attempt'),

  // Database
  dbQuery('db.query'),
  ;

  const SpanOp(this.value);
  final String value;
}

/// Transaction names — top-level operations visible in Sentry Performance.
enum TransactionName {
  checkout('checkout'),
  upload('upload'),
  feedLoad('feed.load'),
  ;

  const TransactionName(this.value);
  final String value;
}
```

#### `metrics.dart` — Sentry Metric Names

```dart
/// All Sentry custom metric names.
enum MetricName {
  checkoutDuration('checkout.duration'),
  uploadDuration('upload.duration'),
  httpRequestDuration('http.request_duration'),
  ;

  const MetricName(this.value);
  final String value;
}
```

#### `breadcrumbs.dart` — Breadcrumb Categories

```dart
/// All breadcrumb categories for Sentry.
enum BreadcrumbCategory {
  auth('auth'),
  cart('cart'),
  upload('upload'),
  http('http'),
  analyticsEvent('analytics.event'),
  ;

  const BreadcrumbCategory(this.value);
  final String value;
}
```

#### `attributes.dart` — Span Data Key Constants

```dart
/// Static keys for span data and metric attributes.
abstract final class TelemetryKeys {
  static const endpointCount = 'upload.endpoint_count';
  static const endpoint = 'upload.endpoint';
  static const fileSize = 'upload.file_size';
  static const httpMethod = 'http.request.method';
  static const httpStatusCode = 'http.response.status_code';
  static const httpUrl = 'url.full';
}
```

### Step 3: Create ObservabilityService

#### Abstract Interface (`i_observability_service.dart`)

```dart
import 'package:sentry_flutter/sentry_flutter.dart';
import 'breadcrumbs.dart';
import 'metrics.dart';
import 'spans.dart';

/// Abstract observability contract.
/// Depends only on our own enums + Sentry's span interfaces.
abstract class TelemetryService {
  bool get isEnabled;

  // Tracing
  ISentrySpan startTransaction(TransactionName name, SpanOp op, {bool bindToScope = true});
  ISentrySpan? startChildSpan(ISentrySpan parent, SpanOp op, {String? description});
  ISentrySpan? startSpanFromCurrent(SpanOp op, {String? description});

  // Metrics
  void count(MetricName name, int value, {Map<String, SentryAttribute>? attributes});
  void distribution(MetricName name, double value, {String? unit, Map<String, SentryAttribute>? attributes});
  void gauge(MetricName name, double value, {String? unit, Map<String, SentryAttribute>? attributes});

  // Breadcrumbs
  void addBreadcrumb(String message, BreadcrumbCategory category, {SentryLevel level, Map<String, dynamic>? data});

  // Convenience
  Future<T> measure<T>(MetricName metric, SpanOp op, Future<T> Function() operation, {String? description});
}
```

#### Concrete Implementation (`observability_service.dart`)

```dart
import 'package:injectable/injectable.dart';
import 'package:sentry_flutter/sentry_flutter.dart';
import 'i_observability_service.dart';
// ... other imports

@LazySingleton(as: TelemetryService)
class ObservabilityService implements TelemetryService {
  ObservabilityService(this._analyticsService);
  final AnalyticsService _analyticsService;

  @override
  bool get isEnabled => _analyticsService.isEnabled;

  @override
  ISentrySpan startTransaction(TransactionName name, SpanOp op, {bool bindToScope = true}) {
    if (!isEnabled) return _DisabledSpan();
    return Sentry.startTransaction(name.value, op.value, bindToScope: bindToScope);
  }

  @override
  ISentrySpan? startChildSpan(ISentrySpan parent, SpanOp op, {String? description}) {
    if (!isEnabled) return null;
    return parent.startChild(op.value, description: description);
  }

  @override
  ISentrySpan? startSpanFromCurrent(SpanOp op, {String? description}) {
    if (!isEnabled) return null;
    return Sentry.getSpan()?.startChild(op.value, description: description);
  }

  @override
  void count(MetricName name, int value, {Map<String, SentryAttribute>? attributes}) {
    if (!isEnabled) return;
    Sentry.metrics.count(name.value, value, attributes: attributes ?? {});
  }

  @override
  void distribution(MetricName name, double value, {String? unit, Map<String, SentryAttribute>? attributes}) {
    if (!isEnabled) return;
    Sentry.metrics.distribution(name.value, value, unit: unit, attributes: attributes ?? {});
  }

  @override
  void gauge(MetricName name, double value, {String? unit, Map<String, SentryAttribute>? attributes}) {
    if (!isEnabled) return;
    Sentry.metrics.gauge(name.value, value, unit: unit, attributes: attributes ?? {});
  }

  @override
  void addBreadcrumb(String message, BreadcrumbCategory category, {SentryLevel level = SentryLevel.info, Map<String, dynamic>? data}) {
    if (!isEnabled) return;
    Sentry.addBreadcrumb(Breadcrumb(message: message, category: category.value, level: level, data: data));
  }

  @override
  Future<T> measure<T>(MetricName metric, SpanOp op, Future<T> Function() operation, {String? description}) async {
    final span = startSpanFromCurrent(op, description: description);
    final stopwatch = Stopwatch()..start();
    try {
      final result = await operation();
      span?.status = SpanStatus.ok();
      return result;
    } catch (e) {
      span?.throwable = e;
      span?.status = SpanStatus.internalError();
      rethrow;
    } finally {
      stopwatch.stop();
      distribution(metric, stopwatch.elapsedMilliseconds.toDouble(), unit: 'millisecond');
      await span?.finish();
    }
  }
}
```

#### NoOp Span (`_DisabledSpan`)

Implement the full `ISentrySpan` interface with no-ops. This lets callers use `transaction.setData(...)` and `transaction.finish()` without null-checks when observability is disabled.

**Important Sentry 9.x API notes:**

- `Sentry.startTransaction()` returns `ISentrySpan` (there is NO public `ISentryTransaction` type)
- `SpanStatus.ok()` uses parentheses (const constructor)
- `options.enableMetrics` defaults to `true`, but since 9.28.0 it only gates automatic metrics.
  `Sentry.metrics` calls are always sent, so the `isEnabled` check in this service is the only consent gate.
- `SentryAttribute` factory constructors: `.string()`, `.bool()`, `.int()`, `.double()`

### Step 4: User Consent

```dart
// AnalyticsService — default based on environment
bool get isEnabled => _prefs.getBool(_kKey) ?? !isProduction;
```

- Development/staging: ON by default
- Production: OFF by default (user must opt in)
- All `ObservabilityService` methods check `isEnabled` before calling Sentry

### Step 5: Instrument Services & Cubits

#### Pattern: Transaction with Child Spans

```dart
Future<Result> performOperation() async {
  final transaction = _observability.startTransaction(
    TransactionName.operationName,
    SpanOp.operationOp,
  );
  final stopwatch = Stopwatch()..start();

  try {
    // Step 1
    final span1 = _observability.startChildSpan(
      transaction, SpanOp.subOp, description: 'step 1',
    );
    final result1 = await _doStep1();
    span1?.setData('count', result1.length);
    await span1?.finish();

    // Step 2
    final span2 = _observability.startChildSpan(
      transaction, SpanOp.subOp2, description: 'step 2',
    );
    final result2 = await _doStep2();
    await span2?.finish();

    // Record metrics
    stopwatch.stop();
    _observability.distribution(
      MetricName.operationDuration,
      stopwatch.elapsedMilliseconds.toDouble(),
      unit: 'millisecond',
    );

    transaction.status = SpanStatus.ok();
    return result;
  } catch (e) {
    transaction.throwable = e;
    transaction.status = SpanStatus.internalError();
    rethrow;
  } finally {
    await transaction.finish();
  }
}
```

#### Pattern: Event Tracking in Cubits

```dart
// Inject AnalyticsService for events
_analytics.trackEvent(AnalyticsEvent.featureAction.value, properties: {
  'key': value,
});
```

#### Pattern: Breadcrumbs for State Changes

```dart
_observability.addBreadcrumb(
  'Token refresh triggered by 401',
  BreadcrumbCategory.auth,
  level: SentryLevel.warning,
  data: {'endpoint': path},
);
```

#### Pattern: Retry Across Providers

When one operation tries several providers in order, wrap the whole attempt in one transaction and give each provider its own child span.

```dart
final transaction = _observability.startTransaction(
  TransactionName.upload, SpanOp.uploadFile,
);
transaction.setData(TelemetryKeys.endpointCount, endpoints.length);

for (final endpoint in endpoints) {
  final span = _observability.startChildSpan(
    transaction, SpanOp.uploadAttempt, description: endpoint.name,
  );
  span?.setData(TelemetryKeys.endpoint, endpoint.id);

  try {
    await endpoint.upload(file);
    span?.status = SpanStatus.ok();
    await span?.finish();

    _observability.count(MetricName.uploadSuccess, 1, attributes: {
      'endpoint': SentryAttribute.string(endpoint.id),
    });
    break;  // Success - stop trying providers
  } catch (e) {
    span?.throwable = e;
    span?.status = SpanStatus.internalError();
    await span?.finish();

    _observability.count(MetricName.uploadRetry, 1, attributes: {
      'from': SentryAttribute.string(endpoint.id),
    });
    continue;  // Try next provider
  }
}

await transaction.finish();
```

### Step 6: Refactor Existing String Literals

Find and replace all raw strings with enum values:

```bash
# Find all raw trackEvent() calls
grep -rn "trackEvent('" lib/

# Find all raw breadcrumb categories
grep -rn "category: '" lib/
```

Replace pattern:

```dart
// BEFORE
_analytics.trackEvent('item_added', properties: {...});

// AFTER
_analytics.trackEvent(AnalyticsEvent.itemAdded.value, properties: {...});
```

```dart
// BEFORE
Sentry.addBreadcrumb(Breadcrumb(message: 'msg', category: 'auth.token'));

// AFTER
_observability.addBreadcrumb('msg', BreadcrumbCategory.authToken);
```

## Audit Checklist

Run these to verify all telemetry uses enums:

```bash
# Should return ZERO results after migration
grep -rn "trackEvent('" lib/                    # Raw event strings
grep -rn "category: '" lib/ | grep Breadcrumb   # Raw breadcrumb categories
grep -rn "Sentry.addBreadcrumb" lib/            # Direct Sentry calls (should use ObservabilityService)
grep -rn "Sentry.metrics" lib/                  # Direct metric calls
grep -rn "Sentry.startTransaction" lib/         # Direct transaction calls (only in ObservabilityService)
```

## Adding Observability to a New Feature

1. Add events to `AnalyticsEvent` enum in `events.dart`
2. Add span ops to `SpanOp` enum if the feature has async/network operations
3. Add metrics to `MetricName` enum if tracking durations or counts
4. Add breadcrumb category to `BreadcrumbCategory` if needed
5. Inject `TelemetryService` into the cubit/service constructor
6. Add `trackEvent()` calls for user-facing operations
7. Wrap async operations in transactions/spans
8. Record performance metrics with `distribution()`
9. Run `dart run build_runner build --delete-conflicting-outputs`

## Coverage Targets

| Layer                    | What to Instrument                                                                     |
| ------------------------ | -------------------------------------------------------------------------------------- |
| **Auth flows**           | Transaction per login/register/verify + events for each step                           |
| **Checkout**             | Transaction per checkout + child spans for each step + duration metrics                |
| **Multi-provider calls** | Transaction wrapping all attempts + one child span per provider + success/retry counts |
| **Uploads**              | Transaction per upload + per-attempt child spans + count/duration metrics              |
| **HTTP client**          | Auto via `SentryHttpClient` wrapper + error count metrics                              |
| **Screen load**          | Transaction with child spans for each data source                                      |
| **Navigation**           | Auto via `SentryNavigatorObserver` + `AnalyticsRouteObserver` for events               |
| **User interactions**    | Events for CRUD operations, setting changes, feature toggles                           |
| **Background tasks**     | Breadcrumbs for state changes (connectivity, websocket, token refresh)                 |

## Common Pitfalls

1. **`ISentryTransaction` doesn't exist** — Sentry Flutter 9.x returns `ISentrySpan` from `startTransaction()`
2. **`SentryTraceHeader.empty()` doesn't exist** — Use `SentryTraceHeader(SentryId.empty(), SpanId.empty())`
3. **`@internal` on private members** — `@internal` from `package:meta` is only for public elements; private classes don't need it
4. **Const constructors can't read runtime values** - A `const` constructor cannot read environment or config at runtime, so pass those values in from the code that creates the instance
5. **Some code cannot receive injected services** - Code built outside dependency injection, such as a static helper or a third-party callback, may keep a direct `Sentry.addBreadcrumb()` call.
   It must still use enum values for the category, and each such exception should be listed so the audit grep can skip it.
6. **`options.enableMetrics`** - Defaults to `true` in sentry_flutter 9.11+, so there is no need to set it explicitly.
   Since 9.28.0, setting it to `false` does not stop manual `Sentry.metrics` calls, so gate consent in the service.

## Sources

- <https://pub.dev/packages/sentry_flutter/changelog>
- <https://pub.dev/packages/posthog_flutter/changelog>
- <https://docs.sentry.io/platforms/dart/guides/flutter/metrics/>
- <https://docs.sentry.io/platforms/dart/guides/flutter/configuration/options/>
- <https://github.com/getsentry/sentry-conventions/tree/main/model/attributes>
