---
role: Staff Software Engineer / Incident Commander
skill: agile-development
use_case: responding to and writing the postmortem for a production incident where a database migration run during a deploy caused a 20-minute checkout outage
---

## Scenario

A routine deploy includes a schema migration that adds a `NOT NULL` column with
a default to the `orders` table. On a table with tens of millions of rows, the
migration takes an exclusive lock while it backfills the default value, and
every checkout request that tries to touch `orders` during that window queues
behind the lock instead of failing fast. Checkout starts returning timeouts
company-wide two minutes after the deploy starts. The on-call engineer is paged
by the checkout error-rate alert and has to both stop the bleeding and later
explain what happened.

## Common Weak Approach

The on-call engineer sees checkout timeouts spiking and immediately starts
digging into application logs, suspecting a code bug in the new checkout
release rather than the migration that shipped alongside it:

```
14:02  Paged: checkout error rate > 5%.
14:04  Pulled up checkout service logs, seeing lots of "query timeout" errors.
14:07  Started reading the checkout service diff for the release, looking for
       a bug in the payment retry logic (unrelated to this incident).
14:15  Noticed the `orders` table migration in the same deploy, checked
       pg_stat_activity, saw the ALTER TABLE holding an exclusive lock.
14:19  Manually killed the migration's backend process.
14:22  Checkout recovers.
```

Twenty minutes of user-facing downtime pass before the actual mitigation - the
migration is what's holding the lock - is even identified, because the
engineer spent the first thirteen minutes investigating the wrong subsystem
instead of first asking "what changed, and can we safely undo it." The
postmortem that follows reflects the same instinct to explain by narrowing to
a single cause and a single person, rather than to the system's missing
safeguards:

```markdown
# Postmortem: Checkout outage, 2026-08-14

## What happened
Checkout was down for about 20 minutes because of a bad migration.

## Root cause
The migration added a NOT NULL column to the orders table without a default
that could be applied without locking the table. This was written by Priya
and should have been caught in review.

## Fix
Priya's migration was reverted. She will be more careful with migrations
going forward.

## Action items
- Be more careful reviewing migrations before merging.
```

There is no timeline with real timestamps, no distinction between the
immediate trigger and any systemic gap that let it happen, the document names
and blames an individual by name for a change that presumably passed code
review and CI, and the only action item ("be more careful") is not something
that can be tracked, assigned, or verified as done - it will not prevent the
next engineer's migration from doing the same thing.

## Expert-Level Best Practice

The moment checkout timeouts are confirmed to correlate with the deploy that
just went out, the incident commander's first move is to stabilize, not
investigate - roll back the deploy (which also halts the in-progress
migration) rather than root-causing live:

```
14:02  Paged: checkout error rate > 5% (PagerDuty alert #48213).
14:03  Incident declared, IC role taken by on-call engineer (self).
14:03  Checked recent deploys: checkout-service v482 rolled out at 14:00,
       two minutes before the alert fired. Correlation in time is strong
       enough to act on without further diagnosis.
14:04  Posted first status update to #incidents: "Investigating checkout
       timeouts, correlates with 14:00 deploy of checkout-service v482.
       Rolling back now. Next update in 5 min."
14:05  Triggered rollback of checkout-service v482 to the prior release.
14:06  Rollback deploy started. Checkout error rate still elevated (rollback
       does not retroactively release the migration's table lock).
14:07  Ran `SELECT * FROM pg_stat_activity WHERE state != 'idle'` against the
       primary; found the v482 migration's ALTER TABLE still holding an
       AccessExclusiveLock on `orders`, 7 minutes in.
14:08  Killed the migration's backend PID directly (`SELECT
       pg_terminate_backend(pid)`), since the code rollback would not release
       an already-held lock on its own.
14:09  Checkout error rate begins dropping.
14:11  Checkout error rate back to baseline. Posted update: "Checkout
       recovered as of 14:11. Continuing to monitor; investigation into root
       cause ongoing, next update in 15 min or when we have findings."
14:22  Confirmed stable for 10+ minutes. Incident downgraded from active to
       resolved-pending-writeup.
```

The mitigation (roll back, then kill the lock holder) happened before the
migration's exact mechanism was understood, because stopping user impact does
not require first understanding it - and root-causing under live impact would
have traded users' time for the responder's understanding, which is exactly
the trade the playbook says not to make by default. The postmortem written
afterward is blameless, timestamped, and names the missing safeguard rather
than the person:

```markdown
# Postmortem: Checkout outage, 2026-08-14, 14:02-14:11 UTC

## Impact
Checkout was unavailable or severely degraded for approximately 9 minutes of
user-facing impact (14:02-14:11 UTC), with total incident duration of 20
minutes from page to confirmed-stable. Estimated 2,200 checkout attempts
failed or timed out based on the checkout-service error-rate dashboard for
that window.

## Timeline (UTC)
- 14:00 - checkout-service v482 deployed, including a migration adding a
  `NOT NULL` column with a default to `orders` (46M rows).
- 14:02 - checkout error rate exceeds 5%; PagerDuty alert #48213 fires;
  incident declared.
- 14:03 - IC identifies the 14:00 deploy as the most likely trigger by time
  correlation and begins rollback rather than investigating further first.
- 14:05-14:06 - checkout-service code rollback deployed; error rate does not
  immediately recover.
- 14:07 - `pg_stat_activity` shows the migration's `ALTER TABLE` still holding
  an `AccessExclusiveLock` on `orders`, unaffected by the application-level
  rollback.
- 14:08 - migration's backend process terminated directly via
  `pg_terminate_backend`, releasing the lock.
- 14:09-14:11 - checkout error rate returns to baseline.
- 14:22 - incident downgraded to resolved-pending-writeup after 10+ minutes
  stable.

## Immediate trigger
Adding a `NOT NULL` column with a default to `orders` requires PostgreSQL (on
the version in use) to rewrite the table and hold an `AccessExclusiveLock` for
the duration, blocking all reads and writes - including every in-flight
checkout - for as long as the rewrite takes on a 46M-row table.

## Contributing systemic factors (what let this reach production, not who)
- Migrations run automatically as part of the deploy pipeline with no
  lock-timeout or statement-timeout guard, so a long-held lock blocks
  production traffic indefinitely instead of failing the migration step fast
  and safely.
- There is no staging environment with a production-scale copy of `orders`, so
  this migration's duration and locking behavior were never observed before
  hitting the real table; on the much smaller staging table the same migration
  completes in under a second and shows no problem.
- The migration review checklist in use at the time does not include a
  specific check for locking behavior on large tables, so a reviewer following
  the checklist as documented would not have been prompted to ask about it.
- The application-level rollback path does not account for in-flight,
  lock-holding schema changes - rolling back the code does not undo a
  migration already in progress, which extended the incident by roughly 3
  minutes (14:06-14:09) past when the rollback alone completed.

## What worked
- Time-correlation with the recent deploy was used to justify an immediate
  rollback instead of waiting for a confirmed root cause, which capped user
  impact at 9 minutes.
- Status updates went out on a fixed cadence even before the cause was known,
  which kept dependent teams informed without waiting on investigation to
  finish.

## What didn't work
- The rollback alone was insufficient because it doesn't touch an
  already-in-progress migration holding a lock; the responder had to know to
  check `pg_stat_activity` and act on it separately, which is not yet
  documented anywhere as a standard step.

## Action items
- Add a `statement_timeout` (30s) to the migration runner's database session
  so any migration that would hold a long lock fails fast and rolls back
  automatically instead of blocking traffic. Owner: Priya. Due: 2026-08-21.
- Add a staging database seeded with a production-scale (or sampled,
  >=10M row) copy of `orders` and the other largest tables, refreshed weekly,
  and require migrations affecting those tables to run against it before
  merge. Owner: Marcus. Due: 2026-09-04.
- Add "does this lock a table above N rows for more than a few milliseconds,
  and if so does it use a lock-safe pattern (e.g. add column nullable, backfill
  in batches, then add the NOT NULL constraint separately)" as an explicit item
  on the migration review checklist. Owner: Priya. Due: 2026-08-21.
- Document "check `pg_stat_activity` for lock-holding backends from the
  deploy's migration and terminate them if found" as a standard step in the
  checkout-outage runbook, since an application rollback alone does not
  release an already-held table lock. Owner: on-call engineer (self). Due:
  2026-08-18.
```

## Key Takeaways

- Stabilize before you understand. The weak approach spent the first thirteen
  minutes of a twenty-minute outage investigating the wrong subsystem because
  it treated "find the root cause" as the first step; the expert approach
  rolled back based on time-correlation alone within one minute of declaring
  the incident, because a rollback that turns out to be wrong is cheap to
  reverse, while continued user-facing downtime while investigating is not.
  Root-causing under live impact trades users' time for the responder's
  understanding - don't make that trade by default.
- A code-level rollback and releasing a held database lock are two different
  mitigations, not one. The weak approach never separated them, and would have
  stayed down for the full lock duration even after "fixing" the deploy. The
  expert approach recognized that an in-progress `ALTER TABLE` is a piece of
  state a code rollback doesn't touch, and treated killing the lock-holder as
  its own explicit mitigation step - this is a systemic gap (rollback tooling
  that doesn't account for in-flight schema changes) worth an action item on
  its own.
- Blameless means naming the missing safeguard, not the person who tripped
  over its absence. The weak postmortem's root cause was "Priya's migration"
  and its fix was "Priya will be more careful" - which explains nothing about
  why the system allowed a lock-holding migration to reach a 46M-row
  production table unguarded, and predicts the exact same incident the next
  time any engineer, however careful, writes a similar migration. The expert
  postmortem's contributing factors (no statement timeout, no production-scale
  staging rehearsal, no locking-behavior item on the review checklist) each
  describe a gap the system will keep having until someone closes it,
  regardless of who authors the next migration.
- Separate the immediate trigger from contributing systemic factors, and give
  every action item an owner and a date. "Be more careful next time" cannot be
  verified as done and does not change what happens next time; "add a 30s
  statement_timeout to the migration runner, owned by Priya, due 2026-08-21"
  can be checked off, checked up on, and would have prevented this specific
  incident regardless of who wrote the migration. A postmortem whose action
  items are never tracked to completion is analysis without the benefit it was
  meant to produce.
