---
role: Principal Software Engineer
skill: agile-development
archetype: elicitation
user_request: "Can you migrate us off the old database?"
---

## 1. Raw Ambiguous Input

Message from the VP of Engineering, posted in the platform-team channel:

> Can you migrate us off the old database? It's holding us back and I want
> a plan.

No target engine named, no downtime budget, no data-volume figure, and no
statement of whether this is driven by a hard deadline or general
modernization appetite.

## 2. Missing Constraint Analysis

Per `references/software-architecture.md`, a database migration changes
"ownership of persistent data" and "deployment/runtime topology" -
two of the explicit architectural-decision triggers - and is "something
expensive to reverse." Starting a cutover plan before knowing the target
engine, the acceptable downtime window, or the actual driver risks weeks of
work on the wrong migration strategy (a dual-write pipeline is a very
different project than a maintenance-window dump-and-restore).

Specifically missing:
- **Target engine** - "the old database" alone doesn't say what it's moving
  to; a like-for-like version upgrade, a relational-to-relational move, and
  a relational-to-document move each require a different migration
  strategy and different application-code changes.
- **Downtime budget** - whether the business can tolerate a maintenance
  window (hours) or requires near-zero downtime (a dual-write/backfill
  approach) determines the entire migration architecture, not just its
  timeline.
- **Data volume and access pattern** - a few GB migrates differently than
  multiple TB with continuous writes; this also determines whether a
  backfill-then-cutover or a live dual-write strategy is even feasible.
- **Driver** - a hard deadline (e.g. the current vendor's contract or
  end-of-life date) forces a fixed-date, risk-managed cutover; general
  modernization appetite allows a slower, lower-risk incremental approach.

## 3. Socratic Clarification Round

1. What is the target database engine?
   a) A newer major version of the same engine (e.g. Postgres 11 -> 16)
   b) A different relational engine (e.g. MySQL -> Postgres)
   c) A different data model entirely (e.g. relational -> a document store)
2. What downtime is acceptable for the cutover?
   a) A scheduled maintenance window of a few hours is fine
   b) Near-zero downtime is required - the service is used continuously,
      including by customers in other time zones
   c) Not yet decided - depends on what the business stakeholders will
      accept once they see the tradeoffs
3. What is the current data volume and write pattern?
   a) Under 50 GB, moderate write volume - a single backfill pass is
      plausible within a maintenance window
   b) Several TB, high continuous write volume - a single-pass backfill
      would take longer than any acceptable maintenance window
   c) Unknown - no current measurement exists
4. What is driving the timeline?
   a) A hard external deadline (e.g. the current vendor's license or
      support contract expires on a specific date)
   b) General modernization appetite, no fixed deadline
   c) A specific pain point (e.g. repeated capacity incidents) that needs
      relief soon but has no contractual deadline

## 4. User Feedback Integration

The VP's answers, relayed after checking with the platform-ops lead:

- Q1 -> **b) A different relational engine.** Moving from a self-managed
  MySQL cluster to a managed Postgres service.
- Q2 -> **b) Near-zero downtime required.** The service handles customer
  traffic across three time zones with no acceptable global maintenance
  window.
- Q3 -> **b) Several TB, high continuous write volume.** Current cluster is
  ~4.2 TB with a sustained write rate that would take an estimated 30+
  hours for a single-pass dump-and-restore - far beyond any acceptable
  window.
- Q4 -> **a) A hard external deadline.** The current MySQL vendor's
  extended-support contract expires in 5 months; after that, security
  patches stop.

Each answer resolves one gap from section 2: Q1 fixes the target engine and
therefore the migration-strategy family (cross-engine, not an in-place
upgrade), Q2 and Q3 together rule out a single-pass backfill and point to a
dual-write-then-cutover architecture, and Q4 supplies a hard, non-negotiable
deadline that shapes the schedule and risk tolerance.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** A dual-write migration from the self-managed MySQL cluster to
a managed Postgres service, completed before the MySQL vendor's
extended-support contract expires in 5 months, with near-zero customer-
facing downtime during cutover.

**In scope:** Schema translation and a dual-write layer (writes go to both
databases during the transition), a backfill of the ~4.2 TB of existing
data into Postgres, a consistency-verification pass comparing both stores
before cutover, and a final read-path cutover to Postgres with MySQL kept
as a rollback target for a defined bake-in period.

**Out of scope:** Any application-level schema redesign beyond what the
engine change strictly requires - per `software-architecture.md`'s
"prefer the existing architecture," this migration preserves the current
data model rather than opportunistically redesigning it alongside the
engine change.

**Acceptance criteria (given/when/then):**
- Given the dual-write layer is live, when a write is made to any
  service that touches this database, then the write succeeds in both
  MySQL and Postgres or is retried/alerted - no write is silently lost in
  either store.
- Given the backfill and consistency-verification pass, when cutover is
  proposed, then a row-count and checksum comparison between MySQL and
  Postgres shows zero unexplained discrepancies.
- Given cutover happens, when customers use the service, then no
  customer-visible downtime or error-rate increase is observed, measured
  against the existing SLO dashboards.
- Given the 5-month deadline, when the migration plan is finalized, then it
  includes at least 3 weeks of buffer before the vendor contract expires,
  for an unplanned rollback if cutover reveals an issue.

**Explicit non-goals:** This does not redesign the schema, does not migrate
any auxiliary read replicas or analytics pipelines beyond what's needed for
the primary cutover, and does not commit to decommissioning MySQL
infrastructure on the same timeline - that is a separate follow-up once the
bake-in period confirms Postgres is stable.
