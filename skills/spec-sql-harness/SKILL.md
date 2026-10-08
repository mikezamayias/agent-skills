---
name: spec-sql-harness
description: >-
  Prove SQL from design documents such as SCHEMA.md by loading it into the production Postgres image with smoke tests. Use when a spec repository defines a database in Markdown, or when a schema, migration, RLS policy or grant changes. Also use when asked whether the schema actually works.
metadata:
  provenance: local
---

# Spec SQL harness

SQL in a design document is untested code.
Loading it into the real database image and running the calls the app will make finds real bugs before any app exists.
Typical classes of bug this finds:

- a function that reads a dropped column
- an index predicate using `now()`, which Postgres rejects
- a function that crashes on an empty input
- an RPC (database function the app calls) returning null where the app expects a row
- a privacy hole where a query returns another user's private field

The harness lives in the repository.
A harness kept in `/tmp` loses its checks between runs.

## Files

- `scripts/run.sh` extracts the SQL, starts a fresh container, loads stubs, the schema, and every `smoke/*.sql` in name order, prints `passed/total` per suite, and exits non-zero on any failure.
  `bash run.sh nodefaults` does the same after revoking the platform's default grants.
- `scripts/extract_sql.py` prints every fenced block tagged exactly `sql` from the given Markdown files.
  Tag illustrative snippets that must not run as `sql-example`.
- `references/smoke-template.sql` is the suite format: one row per check, holding a sentence and a boolean.
- `references/supabase-stubs.sql` stands in for what Supabase's services create on a real project: `auth.jwt()`, `auth.sessions`, `realtime.messages`, `realtime.send`, and `storage.buckets` and `objects`.
- `references/supabase-nodefaults.sql` simulates projects without default grants to `anon` and `authenticated`.

## Set up in a repository

1. Create `tools/schema-test/`.
   Copy `run.sh` and `extract_sql.py` into it, and add `.schema.sql` to a `.gitignore` there.
2. Write `tools/schema-test/harness.env`:

   ```bash
   SPEC_FILES="SCHEMA.md"            # Markdown files with the SQL, in load order, relative to REPO_ROOT
   REPO_ROOT=../..
   PG_IMAGE=supabase/postgres:17.6.1.177   # example version, pin the exact image and version production runs
   PG_ADMIN=supabase_admin           # postgres for a plain Postgres image
   CONTAINER=myapp-schema-test
   ```

3. For Supabase, copy both reference SQL files in as `stubs.sql` and `nodefaults.sql`.
   For another platform, write stubs for whatever it provides outside the schema.
4. Add suites as `smoke/01.sql`, `smoke/02.sql`, and so on.
   They run in one database in name order, so later suites may use earlier rows, and each suite's header says which it depends on.
5. Record the command in the project's `AGENTS.md` next to the other checks.

## Writing checks

- Name each check as a sentence about behaviour: `'07 a user cannot read another user's private row'`.
- Act as each role the app uses.
  With Supabase that means `set role authenticated` with `request.jwt.claims` set, `set role anon`, and the service role for server paths.
- For every table and function, test that the right role can, the wrong role cannot, and that server-only functions are closed to the app, with `has_function_privilege`.
- Test the privacy promises directly: what another user can see, what deletion removes, and what the retention jobs purge (see `promise-audit`).
- Wrap checks on queued side effects, such as pg_net or job queues, in one transaction, so a background worker cannot drain the queue before the check reads it.
- Add a check for every bug you fix and every rule the decision-maker calls critical, so the regression cannot come back silently.

## Run it

- Run both `bash tools/schema-test/run.sh` and `bash tools/schema-test/run.sh nodefaults` after any schema change and before committing.
  Report the totals.
- `KEEP=1` leaves the container running for inspection.
- It needs Docker and a few GB of disk.
  Check for free disk space first, because a failed write looks like a schema failure.

## Platform notes

- Supabase planned to stop default grants to `anon` and `authenticated` in `public` for projects created after 30 Oct 2026, and legacy anon keys retire at the end of 2026.
  Re-check both on Supabase's changelog before relying on these dates.
  Grant explicitly in the schema, and keep the `nodefaults` run green.
- Declare every extension the schema uses, such as `pg_net`, `pgcrypto`, or `pg_cron`.
  The image may ship with it enabled while a fresh project does not.
- Postgres rejects functions that are not immutable, such as `now()`, in partial-index predicates.
