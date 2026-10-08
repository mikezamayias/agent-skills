# Flutter harness and failure signatures

The default path for any Flutter project.
Covers the worst-case widget test, goldens, device checks, the optional debug toggle, and what each break looks like.

## Widget test

Pump the real widget with each fixture across a matrix of size, text scale, direction and theme.
A `RenderFlex` overflow is reported as an exception, so the test fails on its own and the test is the detector.
Put fixtures in `test/` (for example `test/fixtures/members_fixtures.dart`) so they cannot reach a release build.
Use the repository's `pumpApp` helper when it has one, so theme, localizations and providers match the app.
Follow `vgv-testing` for file layout and naming.

```dart
const sizes = {
  'small': Size(320, 568),
  'phone': Size(390, 844),
  'landscape': Size(844, 390),
  'tablet': Size(1024, 1366),
};
const scales = [1.0, 1.3, 2.0, 3.1];

for (final fixture in MembersFixtures.all) { // demo, worst, empty, one, huge
  for (final MapEntry(key: sizeName, value: size) in sizes.entries) {
    for (final scale in scales) {
      for (final direction in TextDirection.values) {
        testWidgets('${fixture.name} $sizeName x$scale ${direction.name}', (tester) async {
          tester.view
            ..physicalSize = size
            ..devicePixelRatio = 1;
          addTearDown(tester.view.reset);
          await tester.pumpWidget(
            MaterialApp(
              theme: AppTheme.light, // repeat with AppTheme.dark when the app has one
              builder: (context, child) => MediaQuery(
                data: MediaQuery.of(context).copyWith(textScaler: TextScaler.linear(scale)),
                child: Directionality(textDirection: direction, child: child!),
              ),
              home: Scaffold(body: MemberList(members: fixture.members)),
            ),
          );
          expect(tester.takeException(), isNull);
        });
      }
    }
  }
}
```

Scale 2.0 is the Android maximum and about 3.1 matches the largest iOS accessibility size.
Trim the matrix to the axes the screen can actually meet, for example drop `tablet` for a phone-only app.
For text breaks ("1 members", `null`, wrong initials), add `find.text` expectations against the worst and one fixtures.
For the huge fixture, check that the list builds lazily (`ListView.builder`, slivers) instead of timing it in a widget test.
Profile on a device with `flutter run --profile` only when scrolling is suspect.

## Limits of the widget test

The default test font draws every glyph as a box, so widths differ from the real font and CJK, Greek and emoji do not render as text.
Treat a test overflow as a real signal, and a pass as "no overflow with the test font", not as visual proof.
Load the app's fonts with `FontLoader` in test setup when width accuracy matters.

## Goldens

Add a golden for the states worth a visual record, typically worst at `small`, scale 2.0 and 3.1, and RTL.
Use the built-in `matchesGoldenFile` and do not add a golden package for this.
Load real fonts first, or the golden shows boxes instead of text.
Generate with `flutter test --update-goldens` and run goldens on one platform only, because rendering differs between macOS and Linux.

```dart
await expectLater(
  find.byType(MemberList),
  matchesGoldenFile('goldens/member_list_worst_small_x3.1_rtl.png'),
);
```

## Device check

Confirm visually on a simulator or emulator with the system text size raised.

- iOS Simulator: `xcrun simctl ui booted content_size accessibility-extra-extra-extra-large`, then back to `large`.
- Android emulator: `adb shell settings put system font_scale 2.0`, then back to `1.0`.

## Debug toggle (only when asked)

Gate it at the repository or data source, behind a compile-time define and `kDebugMode`, so profile and release builds drop the branch.

```dart
const _breakUi = String.fromEnvironment('BREAK_UI'); // worst | empty | one | huge

Future<List<Member>> fetchMembers() async {
  if (kDebugMode && _breakUi.isNotEmpty) return DebugFixtures.members(_breakUi);
  return _api.fetchMembers();
}
```

Run with `flutter run --dart-define=BREAK_UI=worst`.
This path needs the fixture under `lib/`, so name it as debug-only and keep it out of any public package export.

## Failure signatures

| What you see                                           | Cause                                                                 | Fix                                                                                                                  |
| ------------------------------------------------------ | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Yellow and black stripe, "RenderFlex overflowed"       | `Text` in a `Row` without a flex parent                               | Wrap the text in `Expanded` or `Flexible`, then choose wrap or `maxLines` with `TextOverflow.ellipsis`               |
| Trailing button or menu pushed off the row             | Middle content took all the space                                     | `Expanded` on the middle column only, trailing widget keeps its intrinsic size                                       |
| Text clipped at large text scale                       | Fixed `SizedBox` or `Container` height                                | `ConstrainedBox` with `minHeight`, let content grow                                                                  |
| Button label overflows or clips                        | Fixed button width                                                    | Size from content with a minimum, allow two lines for long translations                                              |
| Text stays normal size at scale 2.0                    | `FittedBox` or `scaleDown` used as a fix                              | Remove it, it defeats the user's text size, restructure the layout instead                                           |
| Leading icon adrift beside a wrapped name              | `CrossAxisAlignment.center` on rows of varying height                 | `CrossAxisAlignment.start` once text can wrap                                                                        |
| Bottom overflow in landscape or with the keyboard open | Non-scrolling column                                                  | `SingleChildScrollView` or slivers, keep the submit action reachable                                                 |
| `"null"` or `"Instance of"` on screen                  | String interpolation of a nullable or object                          | Null-check and omit the line, or format explicitly                                                                   |
| Initials `�`, or `J` for "Jo"                          | `name[0]` and naive splitting                                         | `characters.first` per word, first and last word, icon fallback                                                      |
| "1 members"                                            | Hard-coded plural                                                     | ICU plural in the ARB file (`{count, plural, =1{...} other{...}}`)                                                   |
| `1284` or `1284.0`                                     | Raw `toString()`                                                      | `NumberFormat.decimalPattern(locale)` or `NumberFormat.currency` from `intl`                                         |
| Digits jitter on update                                | Proportional figures                                                  | `FontFeature.tabularFigures()` in the text style                                                                     |
| Grey box or error icon in the avatar                   | No image error handling                                               | `errorBuilder`, or `onForegroundImageError` on `CircleAvatar`, falling back to initials                              |
| Padding or chevron on the wrong side in RTL            | `EdgeInsets.only(left:)`, `Alignment.centerLeft`, `Positioned(left:)` | `EdgeInsetsDirectional`, `AlignmentDirectional`, `Positioned.directional`, `matchTextDirection` on directional icons |
| Diacritics clipped top or bottom                       | Tight `height` in the text style with clipping                        | Looser height, no clip on text                                                                                       |
| Jank on 1,000 rows                                     | `ListView(children:)` or a `Column` in a scroll view                  | `ListView.builder` or slivers                                                                                        |
