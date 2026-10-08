# Cross-Language Safety Audit Checklist

## 1. Server Endpoints (API)

- [ ] List ALL endpoints and their response shapes
- [ ] For each endpoint, identify every field's PostgreSQL source type
- [ ] Verify explicit type casting before JSON serialization:
  - `Number()` for all numeric fields from Postgres
  - `.toISOString()` for all timestamps
  - `Boolean()` for all boolean fields
- [ ] Verify structured logging (method, path, user_id, duration_ms, status_code)
- [ ] Verify error logging with stack traces and sanitized request body
- [ ] Verify X-Request-ID propagation
- [ ] Verify health check endpoint exists

## 2. PostgREST Layer

- [ ] Check all RPC functions — what types do they return?
- [ ] Check all direct table queries — any bigint/numeric columns?
- [ ] Verify PostgREST content-type headers (should be `application/json`)
- [ ] Test with `curl` and verify actual JSON types (use `python3 -c "import json; ..."` to check types)

## 3. Flutter DTOs / Models

- [ ] `grep -rn "as int" lib/` — every hit is a potential bug
- [ ] `grep -rn "as double" lib/` — same
- [ ] `grep -rn "as String" lib/` — usually safe, but check nullability
- [ ] `grep -rn "as bool" lib/` — check for int→bool coercion
- [ ] `grep -rn "as Map" lib/` — check for string→map (jsonb)
- [ ] `grep -rn "as List" lib/` — check for null lists
- [ ] Verify ALL `fromJson` / `fromMap` factories use SafeJson
- [ ] Verify no raw `json['key']` without null/type safety

## 4. Observability

- [ ] Sentry captures deserialization errors with context (endpoint, raw response)
- [ ] Sentry transaction tracing on API calls
- [ ] PostHog tracks API call success/failure events with timing
- [ ] Type coercions logged as Sentry breadcrumbs
- [ ] Server logs accessible (container or platform logs, or log aggregation)

## 5. Integration Tests

- [ ] Script/test that hits every endpoint and validates response type matches DTO expectations
- [ ] Test with edge cases: empty results, null fields, max bigint values
- [ ] Test token refresh flow under concurrent API calls

## Quick Grep Commands

```bash
# Find all unsafe casts in Flutter
grep -rn "as int\|as double\|as num\|as bool" lib/ | grep -v "test/" | grep -v ".g.dart"

# Find all fromJson factories
grep -rn "fromJson\|fromMap" lib/ | grep -v "test/" | grep -v ".g.dart"

# Find all direct json access without safety
grep -rn "json\['" lib/ | grep -v "SafeJson\|test/" | grep -v ".g.dart"

# Server: find all uncast DB results
grep -rn "rows\[" server/src/ | grep -v "Number\|String\|Boolean"
```
