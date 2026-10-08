---
name: flutter-runtime-safety
description: >-
  Catch the errors that escape try-catch and prevent stale-data crashes. Use when wiring crash reporting, hardening release builds, or debugging "impossible" production crashes.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter Runtime Safety

Three invisible bugs sink most production Flutter apps. Each takes 10 minutes to fix and prevents days of forensic debugging.

## 1. `FlutterError.onError` + `PlatformDispatcher.onError` - error boundary for the whole app

`try/catch` only catches synchronous errors and awaited futures. Fire-and-forget futures, microtasks, and timers escape.
Flutter routes framework errors to `FlutterError.onError` and errors raised outside Flutter callbacks to `PlatformDispatcher.instance.onError`.
`SentryFlutter.init` hooks both automatically on Flutter 3.3+, so start the app through `appRunner` instead of wrapping `main()` in `runZonedGuarded`:

```dart
Future<void> main() async {
  await SentryFlutter.init(
    (options) => options.dsn = const String.fromEnvironment('SENTRY_DSN'),
    appRunner: () => runApp(const App()),
  );
}
```

Without an SDK that installs the hooks, set both yourself:

```dart
FlutterError.onError = (details) {
  FlutterError.presentError(details);
  report(details.exception, details.stack);
};
PlatformDispatcher.instance.onError = (error, stack) {
  report(error, stack);
  return true;
};
```

Now any unhandled async error gets reported, not silently dropped.

## 2. `android:allowBackup` — the manifest line that resurrects bugs

By default, Android backs up `SharedPreferences` and local database files, such as drift or Hive, and restores them on a new install.
Users hit a bug, uninstall, and reinstall, and the corrupt state comes back with them.
Set in `AndroidManifest.xml`:

```xml
<application android:allowBackup="false" ...>
```

On Android 12+ some manufacturers still run device-to-device transfer when `allowBackup="false"`, so also exclude the data in the `<device-transfer>` section of `android:dataExtractionRules`.

Or write a first-launch migration that clears stale keys.

## 3. `WidgetsBindingObserver` — pause heavy work in background

When the app backgrounds, timers and streams keep running. Battery drain, websocket reconnect storms, and "ghost" notifications follow. Implement the observer in your root state and pause cubits/streams on `AppLifecycleState.paused`.

## Verification

- Force an unhandled error in a `Future.delayed` callback → confirm Sentry receives it.
- Install on a device with an old version that had a known bad state → confirm clean state on reinstall.
- Profile battery usage with the app backgrounded for 1 hour → no spikes.

## Sources

- <https://docs.flutter.dev/testing/errors>
- <https://docs.sentry.io/platforms/dart/guides/flutter/usage/>
- <https://developer.android.com/identity/data/autobackup>
- <https://api.flutter.dev/flutter/dart-ui/AppLifecycleState.html>
