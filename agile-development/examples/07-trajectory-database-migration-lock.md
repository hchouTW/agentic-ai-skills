---
role: Senior Software Engineer
skill: agile-development
archetype: trajectory
problem_input: a database migration that adds a NOT NULL column to a large production table held an exclusive lock for several minutes during a deploy, causing request timeouts
---

## 1. Task Input & Context

Incident channel excerpt, timestamps as posted:

> 14:02 - Deploy started, includes migration `0047_add_loyalty_tier.sql`:
> `ALTER TABLE orders ADD COLUMN loyalty_tier TEXT NOT NULL DEFAULT
> 'standard';` against the `orders` table (11.2M rows, PostgreSQL 11).
> 14:03 - API error rate spikes; `orders`-table queries timing out.
> 14:07 - Migration completes; error rate returns to baseline.
> 14:08 - Postmortem requested: this table has 11M rows and is on the
> checkout hot path; a 5-minute lock is not acceptable for any future
> migration touching it.

## 2. Root-Cause Triage & Action Plan

Adding a column with a constant default is metadata-only in PostgreSQL 11 and
would not explain a 5-minute lock by itself. Reading `pg_stat_activity`
captured during the incident shows the actual cause: the single `ALTER TABLE
... ADD COLUMN ... NOT NULL ...` statement also has to validate the `NOT NULL`
constraint against every existing row, and PostgreSQL does that validation
under the same `ACCESS EXCLUSIVE` lock the statement already holds for the
metadata change - so the lock's duration scales with table size (a full
sequential scan of 11.2M rows), not with the (trivial) metadata change alone.
Per `references/risk-and-quality.md`'s "Data and Persistence" guidance to
"prefer backward-compatible schema migrations that support rolling
deployment" and keep migrations "deterministic and safe against partial
execution," a single statement that locks proportionally to table size is not
an acceptable pattern for this table going forward.

Action plan: split the change into three separately-deployable migrations
that never hold a table-scanning lock: (1) add the column as nullable with no
`NOT NULL` yet - metadata-only, near-instant; (2) backfill existing rows in
small batches so no single transaction scans or locks the whole table; (3)
add the `NOT NULL` constraint using PostgreSQL's `NOT VALID` +
`VALIDATE CONSTRAINT` pattern, which validates the existing data under a much
weaker lock (`SHARE UPDATE EXCLUSIVE`) that does not block concurrent reads or
writes, instead of the single-statement form that validates under
`ACCESS EXCLUSIVE`.

## 3. Surgical Execution

```diff
-- 0047_add_loyalty_tier.sql (as deployed - caused the incident)
-ALTER TABLE orders ADD COLUMN loyalty_tier TEXT NOT NULL DEFAULT 'standard';
+-- 0047a_add_loyalty_tier_nullable.sql
+ALTER TABLE orders ADD COLUMN loyalty_tier TEXT DEFAULT 'standard';
+-- (metadata-only; no table rewrite, no long lock)
+
+-- 0047b_backfill_loyalty_tier.sql (run by a batch script, not one statement)
+-- UPDATE orders SET loyalty_tier = 'standard'
+--   WHERE id BETWEEN :batch_start AND :batch_end AND loyalty_tier IS NULL;
+-- (looped in application code over 11,200 batches of 1,000 rows each,
+-- committing after every batch)
+
+-- 0047c_enforce_not_null.sql
+ALTER TABLE orders ADD CONSTRAINT loyalty_tier_not_null
+  CHECK (loyalty_tier IS NOT NULL) NOT VALID;
+ALTER TABLE orders VALIDATE CONSTRAINT loyalty_tier_not_null;
+-- VALIDATE CONSTRAINT takes SHARE UPDATE EXCLUSIVE, which blocks other DDL
+-- but not concurrent reads/writes, unlike the original single-statement form.
```

## 4. Verification Evidence

```
$ psql -h staging-replica -d appdb -f 0047a_add_loyalty_tier_nullable.sql
ALTER TABLE
Time: 41.203 ms
$ python3 scripts/backfill_loyalty_tier.py --batch-size 1000 --env staging
backfilled 11,200,000 / 11,200,000 rows in 11,200 batches, max batch duration 38ms
$ psql -h staging-replica -d appdb -f 0047c_enforce_not_null.sql
ALTER TABLE
ALTER TABLE
Time: 2841.117 ms
$ python3 scripts/measure_lock_duration.py --table orders --during-migration 0047c
max ACCESS EXCLUSIVE hold time: 0ms (VALIDATE CONSTRAINT used SHARE UPDATE EXCLUSIVE only)
concurrent read/write probe during migration: 0 timeouts, p99 latency 12ms (baseline: 11ms)
```

The staging replay, seeded with a production-scale snapshot (11.2M rows), ran
the full three-step sequence in under 3 seconds of combined DDL time with zero
observed query timeouts against a concurrent read/write probe, compared to the
5-minute `ACCESS EXCLUSIVE` hold measured in production for the original
single-statement migration.

## 5. Final Deliverable Summary

Replaced the single locking migration with a three-step nullable-add /
batched-backfill / validated-constraint sequence that never holds a
table-scanning lock, verified against an 11.2M-row staging replica with zero
timeouts under concurrent load. Documented the three-step pattern as the
required approach for any future `NOT NULL` addition to a table of comparable
size, per this skill's own migration-safety guidance.
