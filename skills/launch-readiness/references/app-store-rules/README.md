# App Store rejection rules

Checklists by app type and single-rule files for common App Store rejections.
Copied from [moasq/ios-dev-agent](https://github.com/moasq/ios-dev-agent/tree/5985b6c8e39f73b301f976a75ed326c7707cd1e8/.agents/skills/app-store-preflight/references) at commit `5985b6c` (26 May 2026, MIT, see `../../LICENSE-ios-dev-agent`).

These lists are a snapshot.
The live App Store Review Guidelines fetched by `phases/store-compliance.md` win whenever the two disagree, and a guideline number here is a pointer to check, not a quote.

Load `guidelines/by-app-type/all_apps.md` for every iOS or macOS release, then only the app-type lists that fit the app:

| The app has                                                       | Load                                           |
| ----------------------------------------------------------------- | ---------------------------------------------- |
| Subscriptions or in-app purchases                                 | `guidelines/by-app-type/subscription_iap.md`   |
| AI or generative features                                         | `guidelines/by-app-type/ai_apps.md`            |
| HealthKit or health data                                          | `guidelines/by-app-type/health_fitness.md`     |
| User-generated content or social features                         | `guidelines/by-app-type/social_ugc.md`         |
| A kids category, games, VPN, crypto or finance, or a macOS target | the matching file in `guidelines/by-app-type/` |

Then check the rule files in `rules/` (metadata, subscription, privacy, design, entitlements) against the project.
