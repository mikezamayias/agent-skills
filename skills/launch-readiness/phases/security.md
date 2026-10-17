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
- Cross-reference with known CVE databases if available
- **Medium if**: Outdated dependencies with known CVEs
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
- Use a per-user limit and a per-IP limit together, because each alone is defeated by new accounts or rotated IPs.
- The counter and the limit live where the user cannot write them (see check 8).
- This is our own rule, not a cited standard.
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
