# Store Launch Phase Map

Use this map to route work to focused skills and tools.
App Store Connect and Google Play Console tooling means whatever is installed, such as the `asc` CLI, the Play Developer API, or Fastlane.

| Phase              | App Store                                                    | Google Play                                                   | Shared                                                                      |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Code readiness     | `launch-readiness`                                           | `launch-readiness`                                            | testing, security, accessibility, localization, performance                 |
| Icons and graphics | `app-graphics`                                               | `app-graphics`                                                | store icons, feature graphics, social/press assets                          |
| Screenshots        | `app-screenshots`, App Store Connect screenshot upload       | `app-screenshots`, Play Console listing upload                | screenshot sequence, captions, localization, dimensions                     |
| Metadata           | App Store Connect metadata sync, localization, and ASO audit | Play Console listing sync                                     | title, subtitle/short description, description, keywords/ASO, release notes |
| Privacy and policy | `launch-readiness` store-compliance, legal drafting skills   | `launch-readiness` store-compliance, Play Console Data safety | privacy policy, ToS, data deletion, permissions, SDK review                 |
| Age/content        | App Store Connect forms                                      | Play Console forms                                            | UGC, kids, health, location, ads, regulated domains                         |
| Build and signing  | Xcode archive, signing, and build upload tooling             | Signed AAB upload tooling                                     | signed artifacts, versioning, symbols/mapping                               |
| Beta/testing       | TestFlight groups and tester feedback                        | Play internal/closed/open tracks                              | tester access, feedback, crash review                                       |
| Submission         | App Store Connect submission and review status               | Play Console review submission                                | review notes, app access, manual forms                                      |
| Rollout            | App Store phased release                                     | Play staged rollout                                           | pause/rollback plan, monitoring                                             |

## Minimum Public Launch Packet

Required before public go-live:

- Passing `launch-readiness` T1 and no unacknowledged T2 critical/high blockers.
- Store privacy/data forms confirmed by the user.
- Privacy policy live; ToS live when accounts/subscriptions exist.
- Store listing metadata complete for primary locale.
- Required screenshots and icons complete for each target store.
- Signed build uploaded to the intended review/testing/production track.
- Google Play personal developer accounts created after November 13, 2023: closed test with at least 12 testers opted in continuously for the preceding 14 days before applying for production access.
- Review status known.
- Rollout and rollback plan documented.

## Recommended Report Sections

```markdown
# Store Launch Report

## Verdict

## Store Status

## Blocking Issues

## Manual Declarations

## Assets

## Metadata and ASO

## Builds and Releases

## Monitoring and Rollback

## Next Actions
```
