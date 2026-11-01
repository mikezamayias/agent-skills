---
name: flutter-web-first-paint
description: >-
  Speeds up Flutter web first paint with an HTML splash, deferred imports, first-screen preload and Wasm, not hosting. Use when deploying Flutter web (especially to Firebase Hosting) or when first load shows a blank screen. Also use when the CanvasKit download dominates time to interactive or when enabling Wasm.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter web first paint

CanvasKit is ~1.5MB. A blank `body` while `main.dart.js` downloads is a bug.

## When Flutter web is the wrong tool

Flutter's web FAQ says Flutter is not suitable for static websites with text-rich, flow-based content such as blog articles, and that its web output "doesn't align with what search engines need to properly index" (<https://docs.flutter.dev/platform-integration/web/faq>, read 2026-11-01).
The FAQ gives the reason as Flutter web prioritizing performance, fidelity and consistency for app-centric experiences.
It does not say that drawing to a canvas is the cause, so do not give that as the reason.
For static or document-like web content, the FAQ recommends either Jaspr, a community Dart package that builds a DOM-based site where SEO works as on a traditional website, or plain HTML for the landing, marketing and help pages next to a Flutter app.
It says the Dart, Flutter documentation and Flutter marketing sites were migrated to Jaspr.
Jaspr is MIT-licensed and supports server-side rendering and static generation (docs.jaspr.site, read 2026-10-30).
The author of the Made in Dart site reports moving to Jaspr for server-rendered, indexable pages (single report, no benchmark).
Decide this before tuning first paint for a public content or marketing site that must be indexed.
Jaspr is third-party code, so any use, including `dart pub add jaspr` or `dart pub global activate jaspr_cli`, goes through the code-gate remote-code rule.

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
