# Google Play Automation Map

Use the narrowest automation surface that can do the job reliably.

## Official API Scope

The Google Play Developer API covers publishing, reporting, reviews, permissions, purchases, subscriptions, and app-management operations. The Android Publisher API uses transactional `edits`: create an edit, make changes, validate, then commit.

Useful API areas:

- `edits.apks`, `edits.bundles`: upload APKs/AABs.
- `edits.tracks`: assign uploaded versions to internal, closed, open, or production tracks.
- `edits.listings`: update title, short description, full description, and video per locale.
- `edits.images`: upload icons, feature graphics, screenshots, and other image assets.
- `edits.details`: update app-level details.
- `applications.dataSafety`: upload Data safety responses as Safety Labels CSV.
- `monetization.onetimeproducts`, `monetization.subscriptions`, `basePlans`, `offers`: manage Play Billing catalog.
- `reviews`: list and reply to production reviews.
- Reporting API: Android vitals, crashes, ANRs, and quality metrics.

Do not assume every Play Console page has an API. First app creation, some policy declarations, and managed publishing controls may require the Play Console UI.

## Auth

Recommended setup:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/google-play/service-account.json"
gcloud auth application-default print-access-token
```

Keep the JSON key outside the repo and load its path from Keychain/SOPS/direnv/CI secrets.

The service account must have Play Console permissions for the target app and operation. API access also requires the Google Play Android Developer API to be enabled for the Google Cloud project.

## Fastlane Supply

Use Fastlane when the project already has Fastlane lanes or `fastlane/metadata/android/`.

Common metadata layout:

```text
fastlane/metadata/android/
  en-US/
    title.txt
    short_description.txt
    full_description.txt
    changelogs/default.txt
    images/
      phoneScreenshots/
      sevenInchScreenshots/
      tenInchScreenshots/
      featureGraphic.png
      icon.png
```

Example release:

```bash
bundle exec fastlane supply \
  --package_name "com.example.app" \
  --aab "build/app/outputs/bundle/release/app-release.aab" \
  --track "internal" \
  --metadata_path "fastlane/metadata/android" \
  --json_key "$GOOGLE_APPLICATION_CREDENTIALS"
```

Use `--validate_only` or an internal track first when changing metadata and artifacts together.

## Direct REST Shape

For direct API work:

1. Insert edit.
2. Upload AAB.
3. Upload mapping/native symbols if applicable.
4. Update listings/images.
5. Update track release.
6. Validate edit.
7. Commit edit.

If any step fails before commit, delete the edit and report the exact failing request.

## MCP Candidates

Public search found these candidates. Review before installing:

- `devinwang/google-play-developer-mcp`: broad MCP server for Android Publisher API and Reporting API.
- `play-store-mcp` on PyPI: MCP server for deploys, releases, reviews, and related Play Developer API operations.
- `dmitry-kotorov/google-play-console-mcp`: listing/localization-focused MCP.
- `pabal-mcp`: combined App Store and Google Play ASO/store-management MCP.
