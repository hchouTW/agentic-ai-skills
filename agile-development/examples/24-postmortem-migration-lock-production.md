---
role: Site Reliability Engineer
skill: agile-development
archetype: postmortem
incident: A database migration adding a column with a non-null default locked a hot orders table during peak traffic, causing request timeouts across three dependent services
---

## 1. Incident Symptom & Alert Payload

```
ALERT [FIRING] request-timeout-spike
services: orders-api, billing-api, fulfillment-api
p99_latency: 28400ms (threshold: 800ms)
window: 3m
started_at: 2025-02-06T18:03:00Z

--- database slow-query log ---
[18:03:01] LOCK WAIT: ALTER TABLE orders ADD COLUMN loyalty_tier
  VARCHAR(16) NOT NULL DEFAULT 'standard'
  waiting_on: ACCESS EXCLUSIVE lock on "orders"
  blocked_queries: 214 and climbing
[18:03:01] STATEMENT TIMEOUT: SELECT ... FROM orders WHERE id = $1
  (blocked 8.2s, client disconnected)
... (blocked-query count continues climbing for 6 additional minutes)
```

The migration was deployed during the daily 18:00 peak-traffic window
(evening order volume), not during the previously-used low-traffic
maintenance window, because the release calendar for this deploy did not
flag it as traffic-sensitive.

## 2. Immediate Triage & Blast-Radius Mitigation

Per `references/engineering-playbook.md`'s Database Migration guidance to
"test migration behavior against representative data... document
operational sequencing," the on-call engineer's first action was to
cancel the running `ALTER TABLE` statement directly at the database level
(`SELECT pg_cancel_backend(...)` on the blocking session), rather than
waiting for it to complete - canceling an in-progress lock-holding DDL
statement is faster and safer than trying to drain the 214 queued
requests behind it. The lock released within 15 seconds of cancellation,
and the three dependent services' p99 latency returned to baseline within
one minute. The migration was left un-applied and the deploy was marked
failed pending a redesigned approach, rather than being retried
immediately at the same traffic level.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did the `orders` table become locked for 214+ queued queries?**
   Because `ALTER TABLE orders ADD COLUMN ... NOT NULL DEFAULT 'standard'`
   takes an `ACCESS EXCLUSIVE` lock on the whole table for the duration of
   rewriting every existing row to populate the new column's default
   value, and `orders` has enough rows that this rewrite took over six
   minutes.
2. **Why does adding a column with a default value rewrite every existing
   row?** Because the database version in use (confirmed via
   `SELECT version()` during triage) predates the optimization that lets a
   `NOT NULL DEFAULT` column be added as a fast, metadata-only change -
   that optimization only applies to a small window of recent versions,
   and this table's underlying database was not on one of them.
3. **Why wasn't the migration written to avoid a full-table rewrite
   regardless of database version?** Because the standard, portable
   pattern - add the column as nullable with no default first, backfill
   in batches, then add the `NOT NULL` constraint separately once
   backfilled - is more steps than a single `ALTER TABLE ... NOT NULL
   DEFAULT`, and the engineer who wrote this migration used the simpler
   single-statement form that works safely on some database versions but
   not this one, without checking which behavior this specific production
   database has.
4. **Why did pre-deploy testing not catch the lock duration?** Because the
   migration was tested against the staging database, which is
   restored from a much smaller, older data snapshot - the same
   `ALTER TABLE` statement completes in under a second against staging's
   row count, giving no signal that it would take over six minutes
   against production's actual row count.
5. **Why did the release calendar not flag this as a traffic-sensitive
   deploy requiring a maintenance window?** Because the calendar's
   traffic-sensitivity flag is currently set manually by whoever schedules
   the deploy, based on their own judgment of "does this look risky," and
   `ALTER TABLE` statements are not automatically classified as
   lock-risking regardless of the table's size or traffic pattern.

Root cause: the migration used a single-statement `ADD COLUMN ... NOT
NULL DEFAULT` pattern whose lock behavior depends on the database
version, staging's much smaller dataset gave no warning of the resulting
full-table-rewrite duration in production, and the deploy calendar has no
automated way to flag a schema-changing migration against a hot table as
requiring a low-traffic window.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/migrations/2025_02_06_add_loyalty_tier.sql
+++ b/migrations/2025_02_06_add_loyalty_tier.sql
@@ -1,3 +1,11 @@
--- ALTER TABLE orders ADD COLUMN loyalty_tier VARCHAR(16)
--   NOT NULL DEFAULT 'standard';
+-- Step 1 (safe, metadata-only): add nullable, no default.
+ALTER TABLE orders ADD COLUMN loyalty_tier VARCHAR(16);
+
+-- Step 2 (separate deploy, run in batches of 5,000 rows to bound lock
+-- duration and replication lag):
+-- UPDATE orders SET loyalty_tier = 'standard'
+--   WHERE id BETWEEN :batch_start AND :batch_end AND loyalty_tier IS NULL;
+
+-- Step 3 (separate deploy, after backfill confirmed complete):
+-- ALTER TABLE orders ALTER COLUMN loyalty_tier SET NOT NULL;
+-- ALTER TABLE orders ALTER COLUMN loyalty_tier SET DEFAULT 'standard';
```

```diff
--- a/tools/deploy_calendar_check.py
+++ b/tools/deploy_calendar_check.py
@@ -1,5 +1,14 @@
 #!/usr/bin/env python3
+"""Flag schema migrations against tables above the size threshold as
+requiring a low-traffic maintenance window (see postmortem: migration
+lock on orders table)."""
+HOT_TABLE_ROW_THRESHOLD = 1_000_000
+
+def requires_maintenance_window(migration_sql: str, table_row_counts: dict) -> bool:
+    table = extract_target_table(migration_sql)
+    if is_full_rewrite_statement(migration_sql) and \
+            table_row_counts.get(table, 0) > HOT_TABLE_ROW_THRESHOLD:
+        return True
+    return False
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the single-statement `ADD COLUMN ... NOT NULL
DEFAULT` pattern is correct, fast, and safe on a majority of currently
deployed database versions, and the engineer had no reason to suspect this
specific production database's version fell outside that set without
being told to check - that check was not part of the migration-review
checklist.

**What worked:** canceling the blocking statement directly at the
database level, rather than waiting for the migration to complete or
trying to drain queued requests, resolved user-facing impact in under a
minute of the mitigation decision being made.

**What didn't work:** staging's much smaller dataset made the migration
look instant in pre-deploy testing, giving false confidence about
production behavior that scales with row count, not with correctness of
the SQL.

**Preventative monitoring rule:** `tools/deploy_calendar_check.py` blocks
(non-zero exit) scheduling any migration classified as a full-table
rewrite against a table with more than 1,000,000 rows outside the
declared low-traffic maintenance window, and pages the database
on-call if a running DDL statement holds a table lock for more than 30
seconds in production.
