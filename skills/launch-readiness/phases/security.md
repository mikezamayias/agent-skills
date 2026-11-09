# Phase: Security

## Tier

T1 — Ship Blocker

## Inputs

- Stack profile (DI, auth, subscriptions, crash reporting)
- Overlay checks (project-specific security requirements)
- Scope: file list or "all"

## Checks

### 1. Hardcoded Secrets

- Scan source files for patterns: API keys, passwords, tokens, DSNs in string literals
- Look for: `sk_live_`, `pk_live_`, `AIza`, `ghp_`, `Bearer`, password assignments, connection strings
- Exclude: `.env.example`, test fixtures, CLAUDE.md examples
- Exclude client identifiers that are public by design: Sentry DSNs and Firebase API keys (`AIza`) in Firebase config files, when those keys are restricted to Firebase services.
- Still flag an `AIza` key that is also enabled for other Google Cloud APIs, such as the Gemini API.
- **Critical if**: Any match in committed source code
- **Method**: Grep with regex patterns for common secret formats

### 2. Insecure Token Storage

- Check if tokens/credentials are stored in `SharedPreferences` instead of `flutter_secure_storage`
- Scan for: `SharedPreferences` usage near "token", "key", "secret", "password", "credential"
- **Critical if**: Tokens stored in SharedPreferences
- **Method**: Grep for SharedPreferences usage in auth/token-related files

### 3. Input Validation at Boundaries

- Scan API call sites and form handlers for missing validation
- Check: repository methods that accept user input, form onSubmit handlers
- **High if**: API boundary accepts input without validation
- **Method**: Read repository files, check for assert/validation before API calls

### 4. Silent Error Swallowing

- Scan for `catch (_)` or `catch (e)` with empty body
- **High if**: `catch (_)` anywhere in codebase
- **High if**: `catch (e)` with no logging or rethrow
- **Method**: Grep for catch patterns, read surrounding context

### 5. HTTP Without TLS

- Scan for `http://` URLs (not `https://`) in source code
- Exclude: localhost, 127.0.0.1, 10.x.x.x
- **Critical if**: Production HTTP endpoint without TLS
- **Method**: Grep for `http://` in source files

### 6. Timing-Vulnerable Comparisons

- Scan auth-related code for string equality comparisons on secrets/tokens
- Look for: `==` or `!=` on variables named token, secret, key, hash, signature
- **High if**: Direct string comparison in auth code
- **Method**: Grep auth files for equality operators on sensitive variables

### 7. Dependency Vulnerabilities

- Run `dart pub outdated` to check for outdated packages
- On a Flutter iOS app, also check which dependency manager each plugin builds through.
  CocoaPods stops accepting new pods and new versions of existing pods on 2 December 2026, existing builds keep working, and a pod-only dependency stops receiving updates, security fixes included (CocoaPods blog, "CocoaPods Trunk Read-Only Plan", read 2026-11-08).
- Firebase Apple SDK 13 and later is not published to CocoaPods, so a Flutter app that still builds Firebase through CocoaPods stays on Firebase 12 (Firebase iOS release notes, 13.0.0 and 12.19.0, read 2026-11-08).
  Confirm that `Podfile.lock` or `Package.resolved` holds a Firebase release that contains the latest Firestore security fix, which is 12.19.3 on Firebase 12 and 13.1.1 on Firebase 13 (release notes, read 2026-11-08).
- A `$FirebaseSDKVersion = '12.19.0'` line at the top of `ios/Podfile` is a workaround one author used for a failed `pod install`.
  `firebase_core.podspec` passes the value as an exact dependency, so the override probably holds Firestore at 12.19.0 and drops the 12.19.3 fix (inference from the podspec, resolution not run).
  Read `Podfile.lock` after adding it and treat a Firestore version below 12.19.3 as a finding.
- To list the plugins that still need CocoaPods, run `flutter build ios` once and read the "do not support Swift Package Manager" warning, which is Flutter's own list.
  The `is:swiftpm-plugin` tag in a package's pub.dev API score tags is a quick hint, and a missing tag means check, not fail (the tag was absent for `path_provider_foundation` on 2026-11-08 while one author's build listed only two other plugins).
  On a native Swift app read `Package.resolved` and treat a `Podfile` as a migration finding, and on Android there is no equivalent check.
- A plugin that moves to Swift Package Manager through a community repackaging of a vendor binary, such as the ML Kit plugins through `d-date/google-mlkit-swiftpm`, is remote code and goes through the code-gate remote-code rule before the app adopts it.
- Cross-reference with known CVE databases if available
- **Medium if**: Outdated dependencies with known CVEs
- **Medium if**: a plugin on the Swift Package Manager warning list has no maintained replacement and the date is before 2 December 2026 (inference, our severity, not a cited standard)
- **Low if**: Outdated dependencies without known CVEs
- **Method**: Run dart pub outdated, parse output

### 8. Stack-Aware Checks

- If `firebase_*`: Check Firestore/RTDB security rules files for overly permissive rules
- If Supabase: Check RLS policies for missing row-level security
- If `purchases_flutter`: Check webhook handlers for auth verification
- If Supabase: for every table the `authenticated` role may UPDATE, list the columns it can write.
  RLS restricts rows, not columns, and `authenticated` holds table-level UPDATE by default, so a plain owner UPDATE policy lets the owner update every column of their own row.
  Flag any billing, entitlement, quota, role or counter column (for example `is_premium`, `credits`, `ai_daily_limit`, `role`) that the owner can write as Critical.
  A correct `WITH CHECK` such as `auth.uid() = user_id` does not fix this, because it only stops ownership transfer.
- If Supabase: flag an UPDATE policy with `USING (true)` and no `WITH CHECK`.
  Without `WITH CHECK`, the `USING` expression also decides which new rows are allowed, so it accepts any new value.
- If Supabase: the documented column fix is `revoke update on table <table> from authenticated`, then `grant update (<safe columns>) on table <table> to authenticated`.
  The revoke must come first, or the table-level grant stays in effect.
  Supabase calls column privileges an advanced feature and recommends RLS policies plus a dedicated table for user roles for most users.
  Moving billing or quota fields to their own table the user cannot write follows from that advice, but Supabase does not state it for those fields.
- If Supabase: flag any `security definer` function in a schema listed under Exposed schemas.
  Supabase functions are owned by `postgres`, which bypasses RLS, so the Data API can call such a function with the creator's privileges, and any role, including `anon`, can execute a function by default.
  Fix with `security invoker` where possible, `set search_path = ''` on every definer function, and `revoke execute` from `public` and `anon`.
- If `firebase_*`: on documents that hold entitlement or quota fields, flag update rules that do not restrict which fields change.
  Firebase calls an allowlist, `request.resource.data.diff(resource.data).affectedKeys().hasOnly([...])`, more secure than a denylist, because writes to new fields are then disallowed by default.
  Per-field equality checks pin only the fields they name and leave every other field writable.
- **Critical if**: Overly permissive security rules or unauthed webhooks
- **Method**: Read security rule files or webhook handlers
- **Sources**: [Supabase column-level security](https://supabase.com/docs/guides/database/postgres/column-level-security), [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [Supabase functions](https://supabase.com/docs/guides/database/functions), [Firebase rules fields](https://firebase.google.com/docs/firestore/security/rules-fields)

### 9. Overlay Checks

- Read the matched overlay's Security section
- Execute each additional check
- Severity: as specified in overlay, default to High

### 10. Server-Side Rate Limits

- Every endpoint that calls an AI provider, sends email or SMS, or triggers billed reads, writes or bandwidth has a limit enforced on the server.
- A limit that exists only in the app is not a limit, because anyone can call the endpoint directly.
  The same holds for a limit that exists only in a front layer such as a web server route or a gateway, because a mobile app, a script or another service can reach the backend without it.
  Enforce the limit on the backend too, or make the backend reachable only through the layer.
- Use a per-user limit and a per-IP limit together, because each alone is defeated by new accounts or rotated IPs.
- The counter and the limit live where the user cannot write them (see check 8).
- This is our own rule, not a cited standard.
- A per-IP limit needs the real client address.
  h3's documentation says the first `x-forwarded-for` entry is client input that lets any caller choose their own address and defeat rate limiting, and says to configure the server to trust its proxy instead (h3.dev, read 2026-10-23, h3 v2 docs, so the option names may differ in the h3 version a given Nuxt app ships).
  Check how the framework resolves the client address behind the host's proxy.
- **Critical if**: an AI or email endpoint has no server-side limit
- **Method**: Read the backend or serverless function for each such endpoint and find the limit check

### 11. Spend Caps

- Every billed provider the app uses (cloud, database, AI, email) has a spend cap where the provider offers one, and a budget alert where it does not.
- On Google Cloud and Firebase, an alerts-only budget does not cap spend.
  Google documents spend cap budgets for supported services, which pause those services until the cap is lifted by hand.
  Which services support them, and whether the feature is generally available, is not verified here.
- The older cut-off is a function triggered by budget notifications that disables billing.
  Disabling billing stops every service in the project, resources might be irretrievably deleted, and recovery is not guaranteed.
  Notifications arrive after costs are incurred, so spend can still exceed the budget.
- Record which choice was made for each provider.
- Do not assume an AI provider offers a hard cap, and confirm it on the provider's own console or docs.
- **High if**: a billed provider has neither a cap nor an alert
- **Method**: Ask the decision-maker or read the provider console through its CLI, because this is not visible in source
- **Sources**: [Google Cloud budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets), [Disable billing with notifications](https://docs.cloud.google.com/billing/docs/how-to/disable-billing-with-notifications)

## Abuse Scenarios

A generic "review security" prompt can miss flaws where each rule is correct but the data model is not.
For every table, endpoint and paid feature, answer each question with a file and line or a test:

- Can a user grant themselves premium, credits or a higher limit by updating their own row (check 8)?
- Can a user read or change another user's row by changing an ID (check 8)?
- Can a user call a paid endpoint without passing the server-side limit (check 10)?
- Can a stolen client key be used outside the app (check 1)?

## Native Swift and Kotlin projects

For native Apple and Android projects the Flutter methods above map as follows.
Full detail is in [native-projects.md](../references/native-projects.md).

Scan `*.plist`, `*.xcconfig`, `*.entitlements`, `local.properties` and `gradle.properties` as well as source.
Tokens in `UserDefaults` or plain `SharedPreferences` are Critical, use Keychain or Keystore-backed storage.
Flag `NSAllowsArbitraryLoads`, cleartext traffic and unneeded exported Android components.
SwiftPM and Gradle have no outdated command, so compare `Package.resolved` and `libs.versions.toml` pins against releases.
Zero third-party dependencies is a pass.

## Severity Rules Summary

| Check                        | Critical | High | Medium | Low |
| ---------------------------- | -------- | ---- | ------ | --- |
| Hardcoded secrets            | X        |      |        |     |
| Insecure token storage       | X        |      |        |     |
| HTTP without TLS             | X        |      |        |     |
| Permissive security rules    | X        |      |        |     |
| No server-side rate limit    | X        |      |        |     |
| catch (\_)                   |          | X    |        |     |
| Missing input validation     |          | X    |        |     |
| Timing-vulnerable comparison |          | X    |        |     |
| No spend cap or alert        |          | X    |        |     |
| Deps with CVEs               |          |      | X      |     |
| Deps without CVEs            |          |      |        | X   |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: yes/no | fix_action: {description}
```

Auto-fixable: `catch (_)` → `catch (e) { debugPrint('CONTEXT: operation failed: $e'); }` (but needs manual context for prefix).
