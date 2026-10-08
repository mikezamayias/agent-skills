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
- **Critical if**: Overly permissive security rules or unauthed webhooks
- **Method**: Read security rule files or webhook handlers

### 9. Overlay Checks

- Read the matched overlay's Security section
- Execute each additional check
- Severity: as specified in overlay, default to High

## Severity Rules Summary

| Check                        | Critical | High | Medium | Low |
| ---------------------------- | -------- | ---- | ------ | --- |
| Hardcoded secrets            | X        |      |        |     |
| Insecure token storage       | X        |      |        |     |
| HTTP without TLS             | X        |      |        |     |
| Permissive security rules    | X        |      |        |     |
| catch (\_)                   |          | X    |        |     |
| Missing input validation     |          | X    |        |     |
| Timing-vulnerable comparison |          | X    |        |     |
| Deps with CVEs               |          |      | X      |     |
| Deps without CVEs            |          |      |        | X   |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: yes/no | fix_action: {description}
```

Auto-fixable: `catch (_)` → `catch (e) { debugPrint('CONTEXT: operation failed: $e'); }` (but needs manual context for prefix).
