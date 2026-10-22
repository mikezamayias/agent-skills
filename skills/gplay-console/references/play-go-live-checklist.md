# Google Play Go-Live Checklist

Fetch current Google Play policy pages before final submission because requirements change.

## Account Gate

- Account type is recorded as personal or organization, and the creation date is recorded.
- A personal account created after 2023-11-13 must run a closed test with at least 12 testers opted in continuously for 14 days before Production is enabled.
  A tester who opts out early does not count, and production-access review usually takes 7 days or less.
- An organization account needs a D-U-N-S number, and Google does not state a tester exemption, so confirm in the Dashboard that Production is not locked.
- The registration fee is a US$25 one-time payment.
- Never plan a launch date from the tester rule until the Dashboard shows the account's actual status.
- Evidence: Google Play Help pages read on 2026-10-20 through a page-summarizing tool, except the last line, which is our rule.

## Build and Platform

- Signed Android App Bundle exists (`.aab`), not only APK.
- Version code is higher than any released artifact on the target track.
- Package name is final; package names are permanent once used.
- Play App Signing status is known.
- Target API meets the current Play requirement. As of 2026-05-29, new apps and updates need Android 15/API 35 or higher, except Wear OS, Android Automotive OS, and Android TV targets, which need Android 14/API 34 or higher.
- Native debug symbols and ProGuard/R8 mapping files are ready when applicable.
- The build uploads the R8 mapping file to the crash reporter (Crashlytics or Sentry) and bundles it for Play Console, so post-release ANR and crash clusters are readable.
- Play vitals ANR rate and crash rate are checked after each release against Google's bad-behavior thresholds.
  Overall, the user-perceived crash rate threshold is 1.09% and the user-perceived ANR rate threshold is 0.47%.
  Per phone model, both are 8%, and per watch model the crash threshold is 4% and the ANR threshold is 5%.
  Above a threshold, Play "may reduce the visibility of your title" and "may also show users a warning on your store listing".
  Play uses the last 28 days of data, and flags an emerging crash or ANR once it has affected devices for more than 7 days.
- Evidence: Grab's Android case study, self-reported, read on 2026-10-21.
- Evidence for the thresholds: <https://developer.android.com/topic/performance/vitals>, fetched with curl and read 2026-10-23.

## Store Listing

- App title is 30 characters or fewer.
- Short description is 80 characters or fewer.
- Full description exists and is not placeholder or keyword-stuffed.
- Release notes exist for the version code.
- Category and tags are documented.
- Privacy policy URL is live.
- Support email is configured.
- Website and support URL are present when available.

## Assets

- Play icon: 512x512, 32-bit PNG with alpha, 1024 KB max.
- Feature graphic: 1024x500, JPEG or 24-bit PNG, no alpha.
- Screenshots: minimum two total; for strong eligibility, provide at least four app screenshots at 1080px+ resolution.
- Phone screenshots are 9:16 portrait or 16:9 landscape, PNG/JPEG, no alpha, min 320px and max 3840px per side.
- Screenshots show the actual app, no debug data, no misleading claims, no store badges, no ranking/price/accolade text.
- Alt text is prepared for images where Play Console requests it.

## Policy and Legal

- Data safety form is complete and matches the app, SDKs, privacy policy, and backend behavior.
- Privacy policy covers all collected/shared data and deletion/contact paths.
- Account deletion URL is available when accounts can be created.
- Content rating questionnaire is complete.
- Target audience and Families policy status are complete.
- Ads declaration is complete.
- App access instructions/test account are complete if login or gated content exists.
- Financial products, health, government, gambling, news, crypto, VPN, background location, photos/videos, and other sensitive declarations are handled if relevant.
- Payments for digital goods use Google Play Billing.

## Release

- Track is explicit: internal, closed, open, production.
- Tester groups are configured for non-production tracks.
- Rollout percentage is explicit for staged production releases.
- Managed Publishing status is known.
- Review status, policy warnings, and publishing overview are checked after submission.
- Rollback/pause plan is documented.
