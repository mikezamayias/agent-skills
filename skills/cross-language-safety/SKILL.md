---
name: cross-language-safety
description: >-
  Prevent cross-language type mismatches in full-stack apps (Dart/Flutter ↔ JSON ↔ PostgreSQL/PostgREST/Deno). Use when building or auditing APIs, DTOs, sync engines, or any server↔client data flow. Also use when setting up observability (logging, Sentry, analytics) for API communication layers.
metadata:
  docs-verified: "2026-09-28"
---

# Cross-Language Type Safety

## The Problem

PostgreSQL, PostgREST, Deno, and Dart each serialize types differently:

- `bigint` -> deno-postgres returns a JS **`bigint`**, which `JSON.stringify` cannot serialize.
- `bigint` -> PostgREST returns a JSON number, which loses precision past 2^53 in JS and on Flutter web.
- `numeric` -> deno-postgres returns a **string**.
- `numeric` -> PostgREST returns a JSON number, which Dart decodes as `int` when it has no fractional digits.
- `boolean` → some drivers return `0`/`1`
- `timestamp` → format varies by driver config
- `jsonb` → may be string or parsed object

Dart's `as int?` throws `TypeError` on strings. These bugs are silent — no server error, no 4xx/5xx, just a client-side crash.

## Rules

### Server Side (API)

1. **Explicitly cast all types before JSON response.** Wrap every numeric DB field with `Number()` in Deno/JS. Never trust the driver's default serialization.

2. **Structured JSON logging on every endpoint:**
   - Request: method, path, user_id (from JWT), duration_ms, status_code
   - Error: full stack trace, sanitized request body (no tokens/passwords), user context
   - Propagate `X-Request-ID` header through the chain

3. **Health endpoint:** `GET /health` that checks DB connection, returns service versions.

### Client Side (Flutter/Dart)

1. **Never use `as Type` on server data.** Always use safe parsers:

   ```dart
   // BAD
   final version = json['version'] as int?;

   // GOOD
   final version = SafeJson.parseInt(json['version']);
   ```

2. **Build a `SafeJson` utility class:**
   - `parseInt(dynamic)` — handles int, string, double, null
   - `parseDouble(dynamic)` — handles double, string, int, null
   - `parseString(dynamic)` — handles string, num, null
   - `parseBool(dynamic)` — handles bool, int, string, null
   - `parseDateTime(dynamic)` — handles ISO string, int (epoch), null

3. **Every DTO/model `fromJson` must use SafeJson**, never raw casts.

4. **Sentry integration for API layer:**
   - Capture all deserialization failures with full context (endpoint, raw response, expected type)
   - Add transaction tracing for API calls (request and response parsing as spans)
   - Log type coercions as breadcrumbs (when SafeJson converts string→int, etc.)

5. **PostHog events:** Track API call success/failure with timing, auth refresh events.

### PostgREST Specifics

1. **Know PostgREST type mappings:** See [references/postgrest-types.md](references/postgrest-types.md)

### Audit Checklist

When auditing an existing codebase, see [references/audit-checklist.md](references/audit-checklist.md)

## For Sub-Agents

Include this in every Flutter task prompt that touches API code:

> "Use SafeJson for all server response parsing. Never use `as Type` on JSON data. Log deserialization anomalies to Sentry."

## Sources

- <https://docs.postgrest.org/en/stable/references/api/tables_views.html>
- <https://www.postgresql.org/docs/current/functions-json.html>
- <https://github.com/denodrivers/postgres/blob/main/query/decode.ts>
- <https://dart.dev/resources/language/number-representation>
- <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt>
