#!/usr/bin/env bash
# Run the SQL written in spec documents against a real Postgres, then the smoke suites.
#   bash run.sh               load stubs, the spec's SQL, then every smoke/*.sql in order
#   bash run.sh nodefaults    same, after nodefaults.sql revokes the platform's default grants
# Settings come from harness.env next to this script:
#   SPEC_FILES  Markdown files holding ```sql blocks, relative to REPO_ROOT, in load order
#   REPO_ROOT   repository root, relative to this script (default ../..)
#   PG_IMAGE    the exact image production runs, for example supabase/postgres:17.6.1.177 (pin the version production runs)
#   PG_ADMIN    superuser inside the image (supabase_admin for Supabase, postgres otherwise)
#   CONTAINER   container name
# Exits non-zero if the schema fails to load, a suite errors, or any check fails.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=../..
PG_ADMIN=postgres
CONTAINER=spec-sql-harness
# shellcheck source=/dev/null
source "$HERE/harness.env"
ROOT=$(cd "$HERE/$REPO_ROOT" && pwd)

specs=()
for f in $SPEC_FILES; do specs+=("$ROOT/$f"); done
python3 "$HERE/extract_sql.py" "${specs[@]}" > "$HERE/.schema.sql"

docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$CONTAINER" -e POSTGRES_PASSWORD=postgres "$PG_IMAGE" >/dev/null
for _ in $(seq 1 60); do docker exec "$CONTAINER" pg_isready -U postgres -h localhost >/dev/null 2>&1 && break; sleep 2; done
sleep 6 # images with init scripts report ready before their roles exist

psql() { docker exec -i "$CONTAINER" psql -U "$PG_ADMIN" -d postgres "$@"; }
load() { # load <file>: stop at the first error and show it
  local out
  if ! out=$(psql -v ON_ERROR_STOP=1 -q < "$1" 2>&1); then
    echo "LOAD FAILED: $1"; echo "$out" | grep -v NOTICE | tail -20; exit 1
  fi
}

[ -f "$HERE/stubs.sql" ] && load "$HERE/stubs.sql"
if [ "${1:-}" = nodefaults ]; then load "$HERE/nodefaults.sql"; echo "mode: without default grants"; fi
load "$HERE/.schema.sql"
echo "schema loaded"

passed=0 total=0 bad=0
for suite in "$HERE"/smoke/*.sql; do
  out=$(psql < "$suite" 2>&1) || true
  counts=$(echo "$out" | grep -E '^[0-9]+\|[0-9]+$' | tail -1)
  errors=$(echo "$out" | grep -E 'ERROR' || true)
  fails=$(echo "$out" | grep -E '\|f$' || true)
  name=$(basename "$suite")
  if [ -z "$counts" ] || [ -n "$errors" ]; then
    echo "$name: ERROR"; echo "$errors" | head -5; bad=1; continue
  fi
  p=${counts%|*} t=${counts#*|}
  passed=$((passed + p)) total=$((total + t))
  echo "$name: $p/$t"
  if [ -n "$fails" ]; then echo "$fails" | sed 's/^/  FAIL /'; bad=1; fi
done
echo "total: $passed/$total"
[ "${KEEP:-0}" = 1 ] || docker rm -f "$CONTAINER" >/dev/null
exit $bad
