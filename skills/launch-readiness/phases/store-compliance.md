# Phase: Store Compliance

## Tier

T1 — Ship Blocker

## Inputs

- Stack profile (subscriptions, analytics, UI framework)
- Overlay checks (project-specific store requirements)
- Scope: full project (not file-scoped — checks project-level config)
- Platform targets: detect from `pubspec.yaml` `platforms:` or presence of `ios/` and `android/` directories

## Guidelines Fetch

Before running checks, fetch the latest store guidelines:

### Apple App Store

- Fetch: <https://developer.apple.com/app-store/review/guidelines/>
- Index the content for searchable reference
- Key sections: 1.x (Safety), 2.x (Performance), 3.x (Business), 4.x (Design), 5.x (Legal)

### Google Play Store

- Fetch: <https://support.google.com/googleplay/android-developer/topic/9858052> (Policy Center)
- Fetch: <https://play.google.com/about/developer-content-policy/>
- Index for searchable reference
- Key areas: Privacy, Payments, Content, Ads, Store Listing

### Fallback

If fetch fails (network, rate limit), fall back to the built-in checklist below. Note in the report: "Guidelines fetched on {date}" or "Using cached checklist — fetch failed".

### Guideline Delta Detection

After fetching, compare against the last fetched version (stored in `references/store-guidelines-cache.md`):

- If new sections detected: flag as "NEW GUIDELINE — review manually"
- Update cache after successful fetch

### App-type rejection checklists

For iOS and macOS targets, also load [../references/app-store-rules/README.md](../references/app-store-rules/README.md) and run the app-type checklists and rule files it selects.
They catch rejections by app type, such as subscription disclosure, AI apps, health data and user-generated content.
The live guidelines fetched above win when the two disagree.

## Checks

### iOS — Apple App Store Review Guidelines

#### 1. Privacy (Section 5.1)

##### 1a. Info.plist Privacy Descriptions

- Every permission key in `ios/Runner/Info.plist` must have a user-facing description
- Required keys to check: `NSCameraUsageDescription`, `NSPhotoLibraryUsageDescription`, `NSLocationWhenInUseUsageDescription`, `NSHealthShareUsageDescription`, `NSMotionUsageDescription`, etc.
- **Critical if**: Permission key exists without description string
- **Critical if**: Description is generic ("This app needs access") instead of explaining specific use
- **Method**: Read Info.plist, check all NS\*UsageDescription keys

##### 1b. Privacy Policy

- App must have a privacy policy URL in the App Store Connect metadata field and an easily accessible link within the app (Guideline 5.1.1(i)).
- Info.plist has no privacy policy key.
- Check: repo store metadata (for example `fastlane/metadata/{locale}/privacy_url.txt`) and in-app links.
- **Critical if**: No privacy policy URL configured
- **Method**: Grep store metadata and presentation code for the privacy policy URL

##### 1c. App Tracking Transparency (ATT)

- If app tracks users, it must get permission through the App Tracking Transparency APIs (Guideline 5.1.2(i)).
- Apple defines tracking as linking user or device data from the app with other companies' data for targeted advertising or advertising measurement, or sharing it with data brokers.
- An analytics SDK such as `posthog_flutter` or `firebase_analytics` is not tracking by itself.
- Check: IDFA access, ad or attribution SDKs (`facebook_app_events`, `google_mobile_ads`, `appsflyer_sdk`, `adjust_sdk`, or similar), and data sharing with ad networks or data brokers.
- If tracking: verify `NSUserTrackingUsageDescription` in Info.plist and the ATT prompt in code.
- **Critical if**: Tracking present without ATT implementation
- **Method**: Check pubspec for ad and attribution SDKs and IDFA use, then check Info.plist for the ATT key

#### 2. Login Services (Section 4.8)

- If app uses a third-party or social login (Google, Facebook, X, or similar) for the primary account, it must also offer an equivalent login option that limits data collection to name and email, lets users keep their email private, and does not collect interactions for advertising without consent.
- Sign in with Apple meets these requirements, but Guideline 4.8 does not mandate it specifically.
- Check: Scan auth code for social login providers
- **Critical if**: Social login present without Sign in with Apple or another login option meeting the 4.8 criteria
- **Method**: Grep for Google/Facebook/X sign-in SDKs, then Sign in with Apple or another qualifying option

#### 3. In-App Purchase (Section 3.1)

- If app sells digital content/subscriptions: must use Apple IAP (not Stripe, PayPal, etc. for digital goods)
- Check: If `purchases_flutter` or `in_app_purchase` is present, this is handled
- **Critical if**: App charges for digital content via external payment (Stripe SDK for subscriptions)
- **High if**: App has subscription but no restore purchases button
- **Method**: Check pubspec for payment SDKs, check UI for restore button

##### 3a. Restore Purchases

- Apps with subscriptions must provide a "Restore Purchases" button
- **Critical if**: Subscription app with no restore mechanism
- **Method**: Grep for "restore" in subscription-related files

#### 4. Minimum Functionality (Section 4.2)

- App must provide sufficient functionality beyond a simple website wrapper
- **High if**: App appears to be primarily a WebView wrapper (check for `WebView` as primary content)
- **Method**: Check if main content uses WebView

#### 5. Launch Crash (Section 2.1)

- App must not crash on launch
- **Critical if**: `flutter test` or build fails (covered by Testing phase, but cross-reference)
- Note: This is a runtime check — the skill can verify the app builds, but launch testing requires device/simulator

#### 6. App Icons and Launch Screen

- Must have proper app icon (not default Flutter icon)
- Must have launch screen (not default Flutter splash)
- **High if**: Default Flutter icon detected (`ic_launcher.png` is the Flutter template icon)
- **High if**: Default Flutter launch screen (`launch_background.xml` is unmodified)
- **Method**: Check `ios/Runner/Assets.xcassets/AppIcon.appiconset/` and `android/app/src/main/res/`

#### 7. Metadata Completeness

- Bundle ID must not contain "example" or "com.example"
- Display name must be set (not "Runner")
- **Critical if**: Bundle ID contains "example"
- **High if**: Display name is "Runner" or default template name
- **Method**: Read `ios/Runner.xcodeproj/project.pbxproj` or Info.plist for bundle ID and display name

#### 7a. Automated Review SDK False Flags

Apple runs automated binary analysis as the first review stage (observed field behavior since April 2026).
It scans for SDK signatures and rejects on mismatches with declared metadata, even when the flagged capability is unused.

- Attribution and purchase SDKs (`purchases_flutter` / RevenueCat, `adjust_sdk`, `appsflyer_sdk`, similar) are flagged as "app includes advertising". Instant rejection if the Age Rating "Advertising" descriptor is "No" and no clarifying note exists.
- Auth SDKs in the binary (notably Firebase Anonymous Auth via `firebase_auth`) are flagged as "app has a login" and a demo account is demanded, even with no real login flow.
- Field-verified fix: state the facts in App Review Information notes ("This app has no ads and no login functionality") or provide a demo account. Devs report approval minutes after adding the note.
- **High if**: Stack profile has a purchase/attribution SDK but no ads, or `firebase_auth` without a full login flow, and no review-notes text covering it is found in repo metadata (`fastlane/metadata/review_information/`, asc metadata, `store_assets/`)
- **Method**: Cross-reference stack profile SDKs against age-rating intent and grep repo metadata for review notes / demo account entries

#### 7b. Account Deletion (Section 5.1.1(v))

- If the app supports account creation, it must offer account deletion within the app.
- **Critical if**: Account creation exists without an in-app deletion path
- **Method**: Grep auth and settings code for sign-up and account deletion flows

#### 7c. Privacy Manifest and Required Reason APIs

- Uploads must declare approved reasons for required reason APIs used by the app or its SDKs, in a `PrivacyInfo.xcprivacy` privacy manifest.
- Apps with SDKs on Apple's commonly used third-party SDK list need those SDKs' privacy manifests and signatures.
- Plugins and SDKs ship their own manifests, and the app's `ios/Runner/PrivacyInfo.xcprivacy` covers the app's own code.
- **Critical if**: App code uses required reason APIs without a manifest declaring them, or a plugin/SDK that uses them is pinned to a version without its own manifest
- **Method**: Check for the manifest file, then generate Xcode's privacy report for the archive and look for missing reasons

#### 7d. Build Toolchain

- Since April 28, 2026, uploads must be built with Xcode 26 or later using the iOS 26 SDK.
- Since September 9, 2026, iOS and iPadOS uploads must target iOS 13 or later.
- Fetch the current requirement before final judgment.
- **Critical if**: CI or local build uses an older Xcode, or `IPHONEOS_DEPLOYMENT_TARGET` is below the minimum
- **Method**: Read CI workflow Xcode version and `ios/Podfile` / `project.pbxproj` deployment target

### Android — Google Play Store Policies

#### 8. Privacy Policy

- All Play apps must post a privacy policy link in Play Console and a privacy policy link or text within the app, even apps that access no personal and sensitive user data.
- **Critical if**: No privacy policy URL
- **Method**: Check AndroidManifest.xml for permissions, check for privacy policy configuration

#### 9. Permissions

- AndroidManifest.xml must only request permissions the app actually uses
- **High if**: Permission declared but not used in code (over-requesting)
- Common over-requests: `INTERNET` (always needed), `CAMERA`, `READ_EXTERNAL_STORAGE`, `ACCESS_FINE_LOCATION`
- `READ_EXTERNAL_STORAGE` grants no media access for apps targeting Android 13 (API 33) or higher, which must use granular media permissions instead.
- Play's Photo and Video Permissions policy allows `READ_MEDIA_IMAGES` and `READ_MEDIA_VIDEO` only for apps whose core functionality needs broad photo or video access, and other apps must use the system photo picker.
- **Critical if**: `READ_MEDIA_IMAGES` or `READ_MEDIA_VIDEO` declared without a core broad-access use case
- **Method**: Read AndroidManifest.xml, cross-reference permissions with actual usage in Dart code

#### 10. Target SDK Version

- Google Play requires `targetSdkVersion` to meet the current minimum. Fetch the current requirement before final judgment.
- Since August 31, 2026, new apps and updates must target Android 16 (API 36) or higher, except Wear OS and Android Automotive OS (API 35 or higher) and Android TV and Android XR (API 34 or higher).
- Extensions to November 1, 2026 can be requested in Play Console.
- Apps targeting Android 15 (API 35) or higher must support 16 KB memory page sizes on 64-bit devices, and from February 1, 2027 updates without 16 KB support cannot be released.
- **High if**: Native libraries (plugins or NDK code) are not 16 KB aligned
- **Critical if**: `targetSdkVersion` below Play Store minimum
- **Method**: Read `android/app/build.gradle` or `build.gradle.kts` for `targetSdk` / `targetSdkVersion`, noting Flutter's default `flutter.targetSdkVersion`

#### 11. Data Safety

- All published Play apps, including those on closed, open, or production testing tracks, must complete the Data safety form, even if they collect no user data.
- **High if**: No Data safety declaration is configured or drafted
- Data safety can be drafted from repo evidence and uploaded through the Android Publisher API `applications.dataSafety` when a Safety Labels CSV is available, but user confirmation is required because the declaration is a legal/policy claim.

#### 11a. Account Deletion

- Apps that enable account creation must provide an in-app path to delete the account and associated data, and a web link resource where users can request deletion.
- **Critical if**: Account creation exists without both the in-app path and the web deletion link
- **Method**: Grep auth and settings code for deletion flows, and check store metadata for the deletion URL

#### 12. Billing Policy

- Digital goods must use Google Play Billing (similar to Apple IAP rule)
- **Critical if**: External payment for digital subscriptions without Play Billing
- **Method**: Same check as iOS IAP — verify `purchases_flutter` or `in_app_purchase`

### Store Assets & Marketing Materials

#### 13. Store Screenshots

Store screenshots must exist in the project repo. Expected location: `store_assets/screenshots/` or `assets/store/screenshots/` or `metadata/screenshots/`.

##### 13a. Screenshot Existence

- **Critical if**: No store screenshots directory found in the repo
- **Critical if**: Screenshot directory exists but is empty
- **Method**: Glob for common screenshot directory patterns

##### 13b. Screenshot Completeness (iOS)

- Required device sizes: iPhone 6.9" (or 6.5" when 6.9" is not provided), and iPad 13" if the app runs on iPad.
- App Store Connect scales these down for smaller displays.
- Minimum: 3 screenshots per device size (App Store accepts 1 to 10, but 3+ is rejection-safe)
- **High if**: Fewer than 3 screenshots per required device size
- **Method**: Count image files per device size subdirectory

##### 13c. Screenshot Completeness (Android)

- Required: At least 2 screenshots across device types, max 8 per device type
- Optional: 7-inch tablet, 10-inch tablet
- **High if**: Fewer than 2 phone screenshots
- **Method**: Count image files in Android screenshot directory

##### 13d. Screenshot Format

- iOS: PNG or JPEG, correct resolution per device, no alpha channel or transparency
- Android: JPEG or 24-bit PNG (no alpha), min 320px, max 3840px per side, and the longer side cannot exceed twice the shorter side
- **High if**: Screenshots in wrong format or resolution
- **Method**: Read image dimensions (if possible) or check file extensions

#### 14. Privacy Policy & Terms of Service

##### 14a. Privacy Policy Page

- A privacy policy must be accessible via URL and the URL must be live
- Check for: `privacy_policy_url` in project config, URL in Info.plist, URL in app settings
- Also check: if a privacy policy markdown/HTML file exists in the repo (e.g., `docs/privacy-policy.md`, `web/privacy.html`)
- **Critical if**: No privacy policy URL or document found anywhere in the project
- **Method**: Grep for "privacy" in config files, check for policy documents

##### 14b. Terms of Service

- If app has subscriptions or user accounts: ToS is required
- Check for: ToS URL in project config, ToS document in repo
- **Critical if**: App has subscriptions/accounts but no ToS found
- **Method**: Grep for "terms" in config files, check for ToS documents

##### 14c. Policy Accessibility

- Privacy policy and ToS must be accessible from within the app (not just the store listing)
- Check: settings page, paywall page, or onboarding for links to policy/ToS
- **High if**: Policy exists but is not linked from within the app
- **Method**: Grep presentation layer for privacy/terms URL references

#### 15. Store Listing Metadata

##### 15a. App Description

- Check for store description text in repo (e.g., `store_assets/description.txt`, `metadata/en-US/full_description.txt`, `fastlane/metadata/`)
- **Critical if**: No app description found in repo
- **High if**: Description is placeholder text or under 100 characters
- **Method**: Glob for description files, read content

##### 15b. Short Description / Subtitle

- iOS: Subtitle (30 chars max)
- Android: Short description (80 chars max)
- **High if**: Not found in repo
- **Method**: Glob for short description / subtitle files

##### 15c. Keywords

- iOS: Keywords field (100 chars max, comma-separated)
- **Medium if**: No keywords file found
- **Method**: Glob for keywords file

##### 15d. What's New / Release Notes

- Text for the current version's "What's New" section
- **High if**: No release notes found for current version
- **Method**: Check for `CHANGELOG.md`, `metadata/en-US/changelogs/`, `fastlane/metadata/en-US/release_notes.txt`

##### 15e. Category Selection

- Verify app category is documented (even if set in store console)
- **Low if**: No category documented in repo
- **Method**: Grep for category references

#### 16. App Icons & Branding Assets

##### 16a. App Icon — All Required Sizes

- iOS: Check `ios/Runner/Assets.xcassets/AppIcon.appiconset/Contents.json` for a 1024x1024 image.
- A single 1024x1024 image is enough for iOS and iPadOS because Xcode generates the other sizes, and per-size images (20, 29, 40, 58, 60, 76, 80, 87, 120, 152, 167, 180) are needed only when the asset catalog uses "All Sizes".
- Android: Check `android/app/src/main/res/mipmap-*/ic_launcher.png` for all densities (mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi)
- **Critical if**: Missing 1024x1024 App Store icon
- **High if**: Asset catalog uses "All Sizes" and any size is missing, or any Android density is missing
- **Method**: Read Contents.json, glob mipmap directories

##### 16b. Feature Graphic (Android)

- Google Play requires a feature graphic (1024x500)
- Check: `store_assets/feature_graphic.png` or `metadata/en-US/images/featureGraphic.png`
- **High if**: No feature graphic found
- **Method**: Glob for feature graphic patterns

##### 16c. Promotional Assets

- Check for any promotional banners, promotional text, or promo video URLs
- **Low if**: No promotional assets (not required, but recommended)
- **Method**: Glob for promo asset directories

#### 17. Adaptive Icon (Android)

- Modern Android requires adaptive icon (`ic_launcher_foreground.xml` and `ic_launcher_background.xml`)
- **Medium if**: No adaptive icon configured (only raster icons)
- **Method**: Check for `mipmap-anydpi-v26/ic_launcher.xml`

### Cross-Platform

#### 18. Age Rating Alignment

- If app has user-generated content, social features, or health data: may require higher age rating
- **Medium if**: App has health/social features — flag for manual age rating review
- **Method**: Check for health SDK, social features, UGC indicators

#### 19. Deprecated APIs

- Check for usage of deprecated Flutter/platform APIs that stores may flag
- **Medium if**: Deprecated API usage detected
- **Method**: Run `flutter analyze` and check for deprecation warnings (cross-reference with Testing phase)

#### 20. Fetched Guideline Cross-Reference

- After fetching latest guidelines, scan for any sections that mention keywords related to the app's detected features
- Example: If app uses health data, search guidelines for "health" sections and flag any requirements
- **Medium if**: Relevant guideline section found that isn't covered by above checks — flag for manual review
- **Method**: Keyword search against indexed guidelines using detected features as queries

## Severity Rules Summary

| Check                                    | Critical | High | Medium | Low |
| ---------------------------------------- | -------- | ---- | ------ | --- |
| Missing privacy descriptions             | X        |      |        |     |
| No privacy policy anywhere               | X        |      |        |     |
| No ToS (subscription/account app)        | X        |      |        |     |
| Tracking without ATT                     | X        |      |        |     |
| Social login without 4.8 login option    | X        |      |        |     |
| No in-app account deletion               | X        |      |        |     |
| Missing privacy manifest                 | X        |      |        |     |
| Xcode/SDK or deployment target too old   | X        |      |        |     |
| Broad media permission without core need | X        |      |        |     |
| No restore purchases                     | X        |      |        |     |
| External payment for digital goods       | X        |      |        |     |
| Bundle ID contains "example"             | X        |      |        |     |
| targetSdkVersion too low                 | X        |      |        |     |
| No screenshots in repo                   | X        |      |        |     |
| Empty screenshots directory              | X        |      |        |     |
| No app description in repo               | X        |      |        |     |
| Missing 1024x1024 App Store icon         | X        |      |        |     |
| Default app icon                         |          | X    |        |     |
| Default launch screen                    |          | X    |        |     |
| Display name is "Runner"                 |          | X    |        |     |
| WebView wrapper                          |          | X    |        |     |
| Over-requested permissions               |          | X    |        |     |
| Missing data safety                      |          | X    |        |     |
| Native libraries not 16 KB aligned       |          | X    |        |     |
| < 3 screenshots per device               |          | X    |        |     |
| No feature graphic (Android)             |          | X    |        |     |
| Missing icon sizes                       |          | X    |        |     |
| No release notes for version             |          | X    |        |     |
| Policy not linked in app                 |          | X    |        |     |
| No short description/subtitle            |          | X    |        |     |
| Placeholder description                  |          | X    |        |     |
| SDK auto-review flag without review note |          | X    |        |     |
| Age rating review needed                 |          |      | X      |     |
| Deprecated APIs                          |          |      | X      |     |
| No adaptive icon (Android)               |          |      | X      |     |
| No keywords file                         |          |      | X      |     |
| New guideline section (manual)           |          |      | X      |     |
| No promotional assets                    |          |      |        | X   |
| No category documented                   |          |      |        | X   |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: no | fix_action: {description}
```

Note: Many store compliance findings require manual action or explicit user confirmation (App Store Connect config, Play Console forms, legal/policy declarations, or design decisions). The skill flags them and routes Play automation to the installed Google Play Console tooling where possible.

## Guideline Cache

After a successful fetch, save a summary to `references/store-guidelines-cache.md`:

```markdown
# Store Guidelines Cache

## Last Fetched

- Apple: {date}
- Google: {date}

## Apple Key Sections (summary of current version)

{condensed key requirements}

## Google Key Sections (summary of current version)

{condensed key requirements}

## Change Log

- {date}: {new/changed section detected}
```

This allows the skill to detect when guidelines change between runs.
