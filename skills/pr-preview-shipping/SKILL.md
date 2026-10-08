---
name: pr-preview-shipping
description: >-
  Make every PR produce an installable or clickable preview within minutes, per stack. Use when reviewing CI/CD for mobile, web or API projects, or when someone says to pull the branch and run it. Based on Alberto Moedano (Code with Beto).
allowed-tools:
  - Read
  - Edit
  - Bash
metadata:
  docs-verified: "2026-09-28"
---

# PR-Preview Shipping

## Principle

If a stakeholder, QA, or future-you needs to "pull and run" to review,
the loop is too slow. Every PR yields a clickable preview.

## Per-stack recipe

| Stack                       | Preview channel                                          |
| --------------------------- | -------------------------------------------------------- |
| Mobile app                  | Firebase App Distribution per PR, or TestFlight internal |
| Mobile app (Android)        | Firebase App Distribution + signed APK                   |
| Mobile + serverless backend | TestFlight internal, plus a per-PR backend staging URL   |
| Desktop app                 | Pre-release artifact, for example on GitHub Releases     |
| SSR web framework           | Host preview deployment, for example Cloudflare Pages    |
| API server                  | Tunnel preview against the PR branch                     |

## Required PR comment

```text
✅ Preview ready
• iOS:   TestFlight internal group (build N)
• Web:   {branch}.{project}.pages.dev
• Notes: {what changed}
```

App Store Connect documents no per-build link for internal builds.
Internal testers install from the TestFlight app after the build is added to their group.
Cloudflare Pages preview aliases are per branch (`<branch>.<project>.pages.dev`, lowercased, non-alphanumerics become `-`), not per PR number.

## Acceptance

- Push → preview link <90s web, <12min iOS.
- Preview shows branch + short SHA in about screen.
- Zero manual reviewer setup.

## Sources

- Alberto Moedano (Code with Beto), LinkedIn post: <https://www.linkedin.com/feed/update/urn:li:activity:7398756359166599168/>
- <https://developer.apple.com/help/app-store-connect/test-a-beta-version/add-internal-testers>
- <https://developers.cloudflare.com/pages/configuration/preview-deployments/>
- <https://firebase.google.com/docs/app-distribution>
