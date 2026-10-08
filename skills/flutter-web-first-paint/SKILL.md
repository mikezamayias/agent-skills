---
name: flutter-web-first-paint
description: >-
  Speed up Flutter web first paint with an HTML splash, deferred imports, first-screen preload and Wasm, not hosting. Use when deploying Flutter web (especially to Firebase Hosting) or when first load shows a blank screen. Also use when the CanvasKit download dominates time to interactive or when enabling Wasm.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter web first paint

CanvasKit is ~1.5MB. A blank `body` while `main.dart.js` downloads is a bug.

## Splash

Put a real splash in `web/index.html` with HTML/CSS (Flutter Gallery pattern).

## Don't block runApp

```dart
void main() {
  unawaited(warmCache());
  runApp(const MyApp());
}
```

`unawaited` work that mutates UI after dispose will throw. Gate on `mounted` or a repository.

## Deferred imports

```dart
import 'settings.dart' deferred as settings;
Future<void> openSettings() async {
  await settings.loadLibrary();
  // push settings.SettingsPage()
}
```

## Preload only first-screen assets

Serve WebP/AVIF for hero images.

```html
<link rel="preload" href="assets/logo.webp" as="image" type="image/webp" />
```

Firebase Hosting:

```json
"headers": [{
  "source": "/",
  "headers": [{ "key": "Link", "value": "<assets/logo.webp>; rel=preload; as=image" }]
}]
```

Preloading assets that aren't on the first screen wastes bandwidth.

## Wasm

No `dart:html` / `dart:js`. Use `package:web` + `dart:js_interop`. Check every plugin is Wasm-ready (`camera_web` already is).
`flutter build web --wasm` is opt-in and also emits a JS build that runs when the browser lacks WasmGC.
Under Wasm, deferred imports are not split by default, and Wasm deferred loading (`--enable-wasm-deferred-loading`) is still experimental.

Optional: an HTML landing/login shell that loads instantly while `flutter_bootstrap.js` loads the app, then navigates in.

## Sources

- <https://flutter.dev/blog/best-practices-for-optimizing-flutter-web-loading-speed>
- <https://docs.flutter.dev/platform-integration/web/wasm>
- <https://docs.flutter.dev/platform-integration/web/initialization>
- <https://firebase.google.com/docs/hosting/full-config>
