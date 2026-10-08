# PostgREST & Deno-Postgres Type Mappings

## PostgreSQL → PostgREST JSON

| PostgreSQL Type               | PostgREST JSON      | Notes                                    |
| ----------------------------- | ------------------- | ---------------------------------------- |
| `integer` / `int4`            | number              | Safe                                     |
| `bigint` / `int8`             | number              | Lossy past 2^53 in JS/web; cast `::text` |
| `smallint` / `int2`           | number              | Safe                                     |
| `numeric` / `decimal`         | number              | Integral values decode as Dart `int`     |
| `real` / `float4`             | number              | Safe                                     |
| `double precision` / `float8` | number              | Safe                                     |
| `boolean`                     | boolean             | Safe                                     |
| `text` / `varchar`            | string              | Safe                                     |
| `timestamp`                   | string (ISO 8601)   | Always string, no offset                 |
| `timestamptz`                 | string (ISO 8601)   | Includes timezone                        |
| `date`                        | string (YYYY-MM-DD) | Always string                            |
| `uuid`                        | string              | Safe                                     |
| `jsonb` / `json`              | object/array        | Parsed, not string                       |
| `bytea`                       | string (hex)        | Escaped                                  |
| `interval`                    | string              | PostgreSQL interval format               |
| `array`                       | JSON array          | Nested types follow same rules           |

## PostgreSQL → Deno-Postgres (deno-postgres driver)

| PostgreSQL Type | JS Type       | Notes                              |
| --------------- | ------------- | ---------------------------------- |
| `integer`       | number        | Safe                               |
| `bigint`        | **bigint**    | JS BigInt, `JSON.stringify` throws |
| `numeric`       | **string**    | Always string                      |
| `float8`        | **string**    | Always string                      |
| `boolean`       | boolean       | Safe                               |
| `timestamp(tz)` | Date object   | Automatic conversion               |
| `jsonb`         | parsed object | Automatic                          |

## Dart Safe Parsing Rules

For every type above, the Dart client must handle:

- The expected type (int for integer)
- String representation (for bigint, numeric, or columns cast with `::text`)
- Null (for nullable columns)
- Unexpected types (double when int expected, etc.)

## Common Traps

1. **bigint IDs or counters** - JS BigInt from deno-postgres and a JSON number from PostgREST, so convert before `JSON.stringify` on the server.
2. **SUM/COUNT aggregates** - `count()` and `sum()` of integers return bigint, and `sum()` of bigint returns numeric.
3. **numeric for money/precision** - String from deno-postgres and a JSON number from PostgREST that Dart decodes as `int` when integral, so never use `as double`.
4. **Epoch timestamps as bigint** - JS BigInt from deno-postgres, not a number.
5. **SERIAL/BIGSERIAL primary keys** - SERIAL is int4 (safe), and BIGSERIAL is int8 (BigInt in deno-postgres, lossy past 2^53 in JS and on Flutter web).
6. **Need an exact value over PostgREST** - Cast the column to text in the query (`?select=amount::text`) or in a view.

## Sources

- <https://docs.postgrest.org/en/stable/references/api/tables_views.html>
- <https://www.postgresql.org/docs/current/functions-json.html>
- <https://www.postgresql.org/docs/current/functions-aggregate.html>
- <https://github.com/denodrivers/postgres/blob/main/query/decode.ts>
- <https://dart.dev/resources/language/number-representation>
