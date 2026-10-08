# Google Play Go-Live Checklist

Fetch current Google Play policy pages before final submission because requirements change.

## Build and Platform

- Signed Android App Bundle exists (`.aab`), not only APK.
- Version code is higher than any released artifact on the target track.
- Package name is final; package names are permanent once used.
- Play App Signing status is known.
- Target API meets the current Play requirement. As of 2026-05-29, new apps and updates need Android 15/API 35 or higher, except Wear OS, Android Automotive OS, and Android TV targets, which need Android 14/API 34 or higher.
- Native debug symbols and ProGuard/R8 mapping files are ready when applicable.

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
