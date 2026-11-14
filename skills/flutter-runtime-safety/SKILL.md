---
name: flutter-runtime-safety
description: >-
  Catches the errors that escape try-catch and prevents stale-data crashes. Use when wiring crash reporting, hardening release builds, or debugging "impossible" production crashes.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter Runtime Safety

Four invisible bugs sink most production Flutter apps. Each takes 10 minutes to fix and prevents days of forensic debugging.

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

- If the app should still survive a phone change, replace the silent restore with an explicit backup and restore screen, so the user chooses what comes back.
  Android Auto Backup keeps one backup per app user, up to 25 MB, in a private Drive folder that the user and other apps cannot read, and each new backup replaces the last (Android Developers, "Back up user data with Auto Backup", read 2026-11-04).
  One indie habit app's announced Google Drive backup shows a different design: a visible backup list with the date, habit count and device, a "Back up now" button, an export to a file, and a restore dialog that states how many records will replace the current data (maker's promo video, not a shipped build, single report).
- Before a restore replaces local data, save the current data first as its own restorable copy.
  The same promo's dialog does this, and it also warns that the saved copy may need repair if it already held damaged data, so do not promise that the safety copy is restorable.

## 3. App lifecycle: pause heavy work in the background and save progress

When the app backgrounds, timers and streams keep running.
Battery drain, websocket reconnect storms, and "ghost" notifications follow.
Pausing app-wide work stays at the root: implement the observer in your root state and pause cubits/streams on `AppLifecycleState.paused`.
Saving a feature's own progress sits with that feature, as the bullets below describe.

- For new code, prefer `AppLifecycleListener` (Flutter 3.13 and later) over a `WidgetsBindingObserver` mixin with a switch.
  It has one callback per transition (`onHide`, `onResume`, `onPause`, `onExitRequested` and others), needs no mixin, and several listeners can exist at once.
  Create it in `initState`, keep it next to the feature that owns the concern, and call `dispose()` on it in `dispose()` (Flutter API docs, read 2026-11-14).
- Save user progress on `onHide`, not on `onPause` alone.
  Flutter's docs say `onHide` runs on mobile usually just before another app replaces this one, on desktop when the app is minimized or hidden, and on the web when the tab is hidden.
  `onPause` is called on mobile only and is not called on desktop or the web (Flutter API docs, read 2026-11-14).
- On desktop, `onExitRequested` is a last chance to flush pending writes before the app quits, and answering `AppExitResponse.cancel` keeps the app open.
  Use it only for data that is already safe to lose or replay, because Flutter's `handleRequestAppExit` docs warn against relying on that hook to save important data (see the next bullet).
  Flutter's docs say cancelling a quit is currently only supported on macOS and Linux (`handleRequestAppExit` page, read 2026-11-14).
  Flutter calls every registered listener and cancels the exit if any one of them answers cancel (checked on Flutter's current master, read 2026-11-14, so older releases may differ).
  `onExitRequested` runs only when the exit is cancelable, which Flutter's docs say.
  That it is not called on phones is inference, so do not rely on it there.
- Do not make saving depend on any lifecycle callback.
  Flutter's own docs say an app killed from a task manager, by a kill signal, or by power loss gets no notification, and some states can be skipped (Flutter API docs for `AppLifecycleState`, read 2026-11-14).
  Save progress as it happens or at natural checkpoints, and treat the `onHide` save as a bonus that narrows the loss window.
  Write pending data so that replaying it on the next launch is safe (one commenter on a Flutter lifecycle post made this point, single report, and it follows from the docs).

## 4. Platform channel handlers: reply once, keep slow native calls off the main thread

- Every branch of a Kotlin or Swift `MethodChannel` handler ends in exactly one of `success`, `error` or `notImplemented` (`FlutterMethodNotImplemented` on iOS), as Flutter's platform channel docs show.
  One tutorial reports that a branch with no reply leaves the Dart `await` pending forever (single report, not in Flutter's docs).
- Use the same channel name on both sides, prefixed with a domain you own, and do not reuse a name inside one app.
- Android runs a channel handler on the platform main thread unless the channel is created with a task queue (`binaryMessenger.makeBackgroundTaskQueue()`).
  `NetworkStatsManager.querySummaryForDevice` and its sibling query methods "may take several seconds to complete, so it should only be called from a worker thread" (Android Developers, read 2026-11-08), so give such a handler a task queue and do not run the query in the default callback.
- On the Dart side catch `PlatformException` and `MissingPluginException` around `invokeMethod`.
  `MissingPluginException` completes the future when no platform plugin handles the method, which includes a platform that never registered the handler (api.flutter.dev, read 2026-11-08).
- For a new bridge, Flutter's docs recommend Pigeon, FFIgen and JNIgen over a raw `MethodChannel`, which "is not type safe" (Flutter docs, "Writing custom platform-specific code", read 2026-11-08).

## Verification

- Force an unhandled error in a `Future.delayed` callback → confirm Sentry receives it.
- Install on a device with an old version that had a known bad state → confirm clean state on reinstall.
- If the app offers its own backup and restore, test the round trip on a second device or after a reinstall: back up, wipe, restore, and compare the record counts.
  Also restore a backup that was made from a state you know is corrupt, and confirm the app either repairs it or refuses with a clear message instead of crashing.
- Profile battery usage with the app backgrounded for 1 hour → no spikes.
- For a screen that holds unsaved user progress, test two cases.
  First, start the task, send the app to the background, swipe it away from the task switcher, relaunch, and confirm the progress is either restored or the loss is acceptable and stated.
  Second, kill the app while it is in the foreground and check the same.
  No callback is guaranteed to run in either case (Flutter API docs for `AppLifecycleState`, read 2026-11-14).
- For each native channel handler, list its branches and confirm each one replies once, then call each method on a platform with no handler and confirm the app handles `MissingPluginException`.

## Sources

- <https://docs.flutter.dev/testing/errors>
- <https://docs.sentry.io/platforms/dart/guides/flutter/usage/>
- <https://developer.android.com/identity/data/autobackup>
- <https://api.flutter.dev/flutter/dart-ui/AppLifecycleState.html>
- <https://api.flutter.dev/flutter/widgets/AppLifecycleListener-class.html>
- <https://api.flutter.dev/flutter/widgets/AppLifecycleListener/onExitRequested.html>
- <https://api.flutter.dev/flutter/widgets/AppLifecycleListener/onPause.html>
- <https://api.flutter.dev/flutter/widgets/WidgetsBinding/handleRequestAppExit.html>
