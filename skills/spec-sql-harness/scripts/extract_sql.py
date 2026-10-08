#!/usr/bin/env python3
"""Print every ```sql fenced block from the given Markdown files, in order.

  python3 extract_sql.py SCHEMA.md [MORE.md ...] > schema.sql

Only fences tagged exactly `sql` are taken. Tag illustrative snippets that must
not run as `sql-example` (or anything else) and they are skipped.
"""
import re
import sys

FENCE = re.compile(r"^```sql\n(.*?)^```", re.S | re.M)

if len(sys.argv) < 2:
    sys.exit(__doc__)
for path in sys.argv[1:]:
    blocks = FENCE.findall(open(path, encoding="utf-8").read())
    print(f"-- {path}: {len(blocks)} blocks", file=sys.stderr)
    sys.stdout.write("\n".join(blocks))
    sys.stdout.write("\n")
