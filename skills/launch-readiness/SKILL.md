---
name: launch-readiness
description: >-
  Run Flutter and mobile launch readiness checks before App Store or Google Play go-live, scored as SHIP, HOLD or BLOCK. Covers store compliance, privacy, legal, data safety, assets, metadata, testing, security, accessibility, performance. Use for /launch-readiness or a public release preflight.
metadata:
  docs-verified: "2026-09-28"
---

# Launch Readiness

A library-agnostic Flutter launch readiness skill. Auto-detects project stack, runs tiered parallel quality checks, produces a scored go/no-go report, offers auto-fixes, and improves itself after each run.

## Invocation

```text
/launch-readiness              # Full 3-tier sweep, entire codebase
/launch-readiness --changed    # Full 3-tier sweep, changed files only
/launch-readiness --tier 1     # Only T1 (testing + security + store compliance)
/launch-readiness --tier 2     # T1 + T2
/launch-readiness --overlay X  # Use specific overlay file
/launch-readiness --fix        # Run + auto-fix without asking
/launch-readiness --auto       # Hook mode: condensed output, no prompts
```

## Orchestrator Flow

```text
1. DISCOVER  → Read pubspec.yaml, CLAUDE.md, overlay → emit stack profile
2. SCOPE     → Determine file scope (--changed or full)
3. DISPATCH  → Launch tier phases as parallel subagents
4. GATE      → Collect results, enforce tier gates
5. SCORECARD → Aggregate into unified report
6. FIX OFFER → "N issues auto-fixable. Fix now?"
7. LEARN     → Mine new patterns, propose phase updates
```

## Step 1: Stack Discovery

Read these sources in parallel:

### 1a. `pubspec.yaml`

Detect dependencies to build a stack profile:

| Concern          | Packages to detect                                                                  |
| ---------------- | ----------------------------------------------------------------------------------- |
| State management | `flutter_bloc` / `riverpod` / `provider` / `get` / `mobx`                           |
| Analytics        | `posthog_flutter` / `firebase_analytics` / `amplitude_flutter` / `mixpanel_flutter` |
| Crash reporting  | `sentry_flutter` / `firebase_crashlytics`                                           |
| Subscriptions    | `purchases_flutter` / `in_app_purchase` / none                                      |
| UI framework     | `shadcn_ui` / `material` (default) / `cupertino` / mixed                            |
| Navigation       | `go_router` / `auto_route` / `navigator` (default)                                  |
| DI               | `get_it` / `riverpod` / `provider` / none                                           |
| Localization     | `intl` / `easy_localization` / `slang` / none                                       |
| Testing          | `very_good_cli` (check dev_dependencies) / `flutter_test` (default)                 |

See `references/stack-detectors.md` for detailed detection rules.

### 1b. `CLAUDE.md`

If a `CLAUDE.md` exists at the project root (or any parent), extract:

- Banned imports (e.g., a banned UI package)
- Theme constant rules (e.g., "use spacing tokens, not raw values")
- Naming conventions
- Coverage thresholds
- Code quality rules

### 1c. Overlay

Resolve overlay using this priority:

1. `--overlay <name>` flag (explicit)
2. `name` field from `pubspec.yaml` (e.g., `name: my_app` matches `overlays/my_app.md`)
3. Git repository root directory name
4. No overlay (generic checks only)

If multiple overlays could match, ask the user.

### Stack Profile Output

Emit a profile object that every phase subagent receives:

```text
Stack Profile:
- state: {detected state management}
- analytics: {detected analytics}
- crash: {detected crash reporting}
- subs: {detected subscriptions}
- ui: {detected UI framework}
- nav: {detected navigation}
- di: {detected DI}
- l10n: {detected localization}
- test_runner: {detected test runner}
- rules: [extracted from CLAUDE.md]
- overlay: {matched overlay name or "none"}
```

## Step 2: Scope Resolution

Determine which files to check:

- **Full codebase** (default, or `--changed` not specified): All `.dart` files under `lib/`
- **Changed files** (`--changed` or auto-hook mode): `git diff --name-only $(git merge-base HEAD <target-branch>)..HEAD`
- **Target branch detection**: From PR target (`gh pr view`), from branch naming (feature branches target the integration branch, hotfix branches target the production branch), or default to the integration branch.
  Branch roles are integration, release candidate, and production (for example `develop`, `release`, `main`).
- **Import expansion** (release-candidate and production targets only): For each changed file, resolve direct importers via grep to catch ripple effects

## Step 3: Dispatch Tier Phases

### Tier Structure

| Tier                     | Purpose      | Phases                                             | Gate                                       |
| ------------------------ | ------------ | -------------------------------------------------- | ------------------------------------------ |
| **T1 — Ship Blockers**   | Must pass    | Testing, Security, Store Compliance                | Critical = STOP                            |
| **T2 — Quality Gates**   | Should pass  | Hardening, Accessibility, Responsive, Localization | Critical = STOP, High = warn + acknowledge |
| **T3 — Polish & Verify** | Nice to pass | Analytics, Performance, Polish                     | Advisory only                              |

Launch all phases within a tier as **parallel subagents** using the Agent tool. Each subagent receives:

- The stack profile from Step 1
- The file scope from Step 2
- The phase instructions from `phases/{phase}.md`
- Any overlay additions from `overlays/{overlay}.md` for that phase

### Phase File Location

Phase prompts live in `phases/` directory relative to this skill file. Read the phase file and pass its content as the subagent prompt, prepending the stack profile and scope.

### Subagent Error Handling

If a phase subagent fails (timeout, crash, malformed output):

1. Retry once with the same inputs
2. If retry fails: mark the phase as **INCONCLUSIVE**
3. Inconclusive in T1/T2 → treated as **critical** (fail-closed)
4. Inconclusive in T3 → treated as **warning** (advisory tier)
5. Include error details in the report

## Step 4: Gate Enforcement

After all phases in a tier complete:

- If any **critical** findings → STOP. Present findings, offer to fix. Do NOT proceed to next tier.
- If **high** findings in T2 → present each and ask for acknowledgment:

  ```text
  [phase] file:line — description
  Acknowledge? (y = accept risk / n = will fix) [y/n]:
  ```

  - `y`: marked acknowledged, doesn't count toward HOLD
  - `n`: remains unacknowledged, counts toward HOLD

- If `--auto` mode: all highs are unacknowledged (no interactive prompt)
- If tier clears → proceed to next tier

### Auto-Hook Gate by Branch

| Target                                    | T1 Scope            | On Failure           |
| ----------------------------------------- | ------------------- | -------------------- |
| Integration (for example `develop`)       | Changed files       | Warn, allow override |
| Release candidate (for example `release`) | Changed + importers | Block                |
| Production (for example `main`)           | Full codebase       | Block                |

## Step 5: Scorecard Generation

After all tiers complete (or short-circuit), generate the report.

### Verdict Logic

| Verdict   | Condition                                      |
| --------- | ---------------------------------------------- |
| **BLOCK** | 1+ critical findings                           |
| **HOLD**  | 0 criticals, 3+ unacknowledged highs           |
| **SHIP**  | 0 criticals, all highs acknowledged or 0 highs |

### Severity Definitions

| Severity | Meaning                                      | Gate Impact             |
| -------- | -------------------------------------------- | ----------------------- |
| Critical | App is broken, insecure, or will be rejected | Blocks tier             |
| High     | Significant UX/quality degradation           | Accumulates toward HOLD |
| Medium   | Suboptimal but functional                    | Informational           |
| Low      | Style nit, minor inconsistency               | Informational           |

### Report Template

Use the template in `references/scorecard-template.md`. Write the report to `docs/launch-readiness-report.md` in the project root.

## Step 6: Fix Offer

After presenting the scorecard:

1. Count auto-fixable issues (those with `fix_action` in phase output)
2. Present: "N issues can be fixed automatically. Fix now?"
3. If `--fix` flag: skip prompt, fix immediately
4. On approval: apply fixes grouped by phase
5. After fixing: re-run only affected phases to verify
6. Present updated scorecard with delta

## Step 7: Self-Improvement

After every run, perform learning extraction.

### Pattern Mining

Scan findings for recurring patterns not already in phase check lists:

- New code patterns that should be checked
- Check refinements (broader scope than current check)
- Project-specific discoveries

### Learning Persistence

Append to `references/learnings.md`:

```text
## {date} — {project} run
- NEW CHECK ({phase}): {description}
- REFINEMENT ({phase}): {description}
```

### Pruning

On each run, scan `learnings.md` and:

- Remove entries older than 90 days not promoted to a phase/overlay
- Deduplicate identical check descriptions
- Cap at 100 entries (oldest unpromoted pruned first)

### Phase Update Proposals

Present at end of report:

> "I discovered N patterns not covered by current checks. Update phase files?"

On approval:

- Generic patterns → update `phases/{phase}.md`
- Project-specific patterns → update `overlays/{project}.md`

## Auto-Hook Mode

When invoked with `--auto` (from a UserPromptSubmit hook):

- Run T1 only, scoped to changed files
- Condensed output:

  ```text
  Launch Readiness (T1):
    Testing:  PASS (N tests, 0 failures)
    Security: PASS (0 criticals)
    Store Compliance: PASS (0 criticals)
    → Proceeding.
  ```

- No interactive prompts (highs are unacknowledged)
- On failure: print findings and block

### Hook Setup

See `hooks/pre-push.md` for configuration instructions.

## Sources

- <https://api.flutter.dev/flutter/widgets/MediaQuery/textScalerOf.html>
- <https://docs.flutter.dev/ui/accessibility/accessibility-testing>
- <https://riverpod.dev/docs/whats_new>
- <https://www.w3.org/TR/WCAG22/>
- <https://posthog.com/docs/libraries/flutter>
- <https://firebase.google.com/docs/analytics/flutter/events>
- <https://amplitude.com/docs/sdks/analytics/flutter/flutter-sdk-4>
- <https://developer.apple.com/app-store/review/guidelines/>
- <https://developer.apple.com/app-store/user-privacy-and-data-use/>
- <https://developer.apple.com/news/upcoming-requirements/>
- <https://developer.apple.com/support/third-party-SDK-requirements/>
- <https://developer.apple.com/documentation/bundleresources/privacy-manifest-files>
- <https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications>
- <https://developer.apple.com/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions>
- <https://developer.apple.com/documentation/xcode/configuring-your-app-icon>
- <https://support.google.com/googleplay/android-developer/answer/11926878>
- <https://support.google.com/googleplay/android-developer/answer/10787469>
- <https://support.google.com/googleplay/android-developer/answer/9888076>
- <https://support.google.com/googleplay/android-developer/answer/13327111>
- <https://support.google.com/googleplay/android-developer/answer/14115180>
- <https://support.google.com/googleplay/android-developer/answer/9866151>
- <https://developer.android.com/guide/practices/page-sizes>
- <https://developer.android.com/about/versions/13/behavior-changes-13#granular-media-permissions>
- <https://developers.google.com/android-publisher/api-ref/rest/v3/applications/dataSafety>
- <https://docs.sentry.io/concepts/key-terms/dsn-explainer/>
- <https://firebase.google.com/docs/projects/api-keys>
- <https://pub.dev/packages/mixpanel_flutter>
- <https://firebase.google.com/docs/crashlytics/flutter/customize-crash-reports>
- <https://docs.flutter.dev/ui/internationalization>
- <https://code.claude.com/docs/en/hooks>
- <https://cli.vgv.dev/docs/commands/test>
