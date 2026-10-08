---
name: gplay-console
description: >-
  Automate and preflight Google Play Console releases for Android and Flutter apps. Use when publishing to Google Play, uploading AABs, managing tracks and staged rollouts or syncing store listings. Also covers Data safety, Play Billing products, reviews, Android vitals and a Play counterpart to asc workflows.
---

# Google Play Console

Use this skill as the Google Play counterpart to the `asc-*` App Store Connect skills. Prefer official Google Play Developer APIs, Fastlane `supply`, or an installed Google Play MCP when available; use browser automation only for gaps that are not API-safe.

## References

- Load `references/api-map.md` before choosing the automation path or writing commands.
- Load `references/play-go-live-checklist.md` before release readiness, submission, or policy work.
- Load `references/research-notes.md` when deciding whether to install or configure a third-party MCP/skill.

## Required Intake

Before making changes, identify:

- Package name, app name, and whether the app already exists in Play Console.
- Target track: internal, closed, open, production, or staged rollout.
- Artifact path: signed `.aab`, mapping file, native debug symbols, and release notes.
- Listing source: `fastlane/metadata/android/`, `metadata/`, `store_assets/`, or Play Console only.
- Credential path and auth mode. Never commit service-account JSON keys.
- Manual declarations still needed: app content, content rating, target audience, ads, financial products, government apps, health, Data safety, privacy policy, and account deletion.

## Automation Path

1. Prefer an already configured MCP or CLI wrapper if present in the environment.
2. Use Fastlane `supply` when the repo already has `fastlane/metadata/android/` or Fastlane lanes.
3. Use Android Publisher REST/API clients for direct, transactional release automation.
4. Use browser automation only for first app creation or Play Console declarations that cannot be safely handled by API.

First-time app creation is a Play Console UI flow. The Publishing API generally operates after an app/package exists in the developer account.

## Workflow

1. Discover the Android project: package name, version code/name, signing config, flavors, target SDK, permissions, billing, analytics, and store metadata paths.
2. Run go-live preflight: target API, signed AAB, Play App Signing, privacy policy, Data safety, store assets, metadata, release notes, billing, age/content declarations.
3. Build or locate the signed AAB. Validate it before upload.
4. Create a Play edit or use Fastlane `supply`; upload artifact, mapping/symbols, listing text, images, and track release notes.
5. Update the intended track with status and rollout fraction. Commit only after verifying every staged change.
6. Check Play Console review/managed publishing status and report any manual gates.
7. Produce a short go/no-go report with exact next commands, manual items, and rollback/pause instructions.

## Safety Rules

- Do not store service-account JSON, OAuth refresh tokens, keystores, or passwords in repo files.
- Prefer Keychain, SOPS/direnv, CI secrets, or ignored local paths for credentials.
- Treat production rollout, price changes, subscription changes, and policy declarations as approval-gated.
- Do not claim a Play policy form is complete unless it was read from Play Console/API or the user explicitly confirmed it.
- If Managed Publishing is on, distinguish "submitted/approved" from "published"; the final publish step may still be manual.

## Done State

- Artifact and metadata source paths are recorded.
- Track, release status, rollout percent, and version codes are explicit.
- Data safety and policy declarations are either completed or listed as manual blockers.
- Play listing assets and text pass the checklist.
- The final report says `SHIP`, `HOLD`, or `BLOCK` with concrete reasons.
