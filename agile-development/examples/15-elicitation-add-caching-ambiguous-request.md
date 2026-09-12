---
role: Principal Software Engineer
skill: agile-development
archetype: elicitation
user_request: "Can you add caching to speed things up?"
---

## 1. Raw Ambiguous Input

Slack message from a product manager, cross-posted from a customer escalation
thread:

> Can you add caching to speed things up? The dashboard is slow and a
> customer flagged it today.

No named endpoint, no staleness tolerance, no traffic-pattern data, and no
invalidation strategy specified.

## 2. Missing Constraint Analysis

Per `references/software-architecture.md`, introducing a cache changes a
"cross-cutting quality attribute" (performance) and can introduce a new
consistency boundary between the cache and its source of truth - the wrong
staleness assumption is "something expensive to reverse" once callers start
depending on cached-but-stale data. "The dashboard" also spans several
independently-owned read paths (summary widgets, a live activity feed, and
an account-settings panel), each with a different staleness tolerance.

Specifically missing:
- **Which read path** is actually slow - the dashboard aggregates at least
  three independently-owned queries, and the complaint doesn't say which
  one the customer hit.
- **Staleness tolerance** - some data (e.g. account settings) must reflect
  the latest write immediately; other data (e.g. an aggregate usage count)
  can tolerate being a few minutes stale without anyone noticing.
- **Traffic pattern** - a cache only pays for itself if the same query is
  requested repeatedly by many users; a rarely-repeated, per-user query
  gains nothing from caching and just adds an invalidation-correctness
  risk.
- **Invalidation trigger** - a fixed TTL (simple, but always somewhat
  stale) versus explicit invalidation on write (fresher, but requires
  wiring every write path that touches the cached data) are different
  architectures with different failure modes.

## 3. Socratic Clarification Round

1. Which part of the dashboard did the customer report as slow?
   a) The summary widgets (aggregate counts and charts)
   b) The live activity feed (recent events, expected to be near-real-time)
   c) The account-settings panel
   d) Not specified - could be any of the above; needs a support-ticket
      follow-up first
2. How stale can the slow data be without anyone noticing or objecting?
   a) A few seconds is fine
   b) A few minutes is fine
   c) Must always reflect the latest write - no staleness acceptable
3. Is the same underlying query requested repeatedly by many different
   users, or mostly once per user?
   a) Repeatedly by many users - the same aggregate is computed for every
      viewer of a shared dashboard
   b) Mostly once per user - each user's view is personalized and rarely
      re-requested within a short window
   c) Unknown - no query-level metrics exist yet
4. Should invalidation be a fixed TTL or triggered explicitly on the
   relevant writes?
   a) Fixed TTL - simpler, and the staleness tolerance from Q2 makes a TTL
      acceptable
   b) Explicit invalidation on write - needed because staleness tolerance
      is near-zero
   c) Undecided - depends on the answer to Q2

## 4. User Feedback Integration

The product manager's answers, after pulling the actual support ticket:

- Q1 -> **a) The summary widgets.** The ticket specifically calls out the
  "usage this month" chart taking 8+ seconds to load.
- Q2 -> **b) A few minutes is fine.** The usage chart is informational, not
  used for billing or real-time decisions; product confirms a few minutes
  of staleness is unnoticeable and acceptable.
- Q3 -> **a) Repeatedly by many users.** The usage chart aggregates
  org-wide data, so every user viewing the dashboard for the same
  organization triggers the same underlying query.
- Q4 -> **a) Fixed TTL.** Given the few-minutes staleness tolerance from
  Q2, a TTL cache is simpler than wiring explicit invalidation across every
  write path that touches usage data, and meets the actual requirement.

Each answer resolves one gap from section 2: Q1 names the specific slow
query (not the whole dashboard), Q2 supplies a concrete staleness budget,
Q3 confirms the access pattern actually benefits from caching (shared,
repeated reads), and Q4 picks the simpler invalidation strategy that the
staleness tolerance permits.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** Add a per-organization, TTL-based cache in front of the
"usage this month" aggregate query powering the dashboard's summary chart,
reducing its load time from 8+ seconds to under 500ms for cached reads.

**In scope:** The single usage-aggregate query behind the summary chart;
a TTL of 5 minutes (within the confirmed staleness tolerance); a cache key
scoped per organization (matching the query's actual granularity).

**Out of scope:** The live activity feed and account-settings panel - no
complaint or staleness analysis covers them, and caching either without a
stated need would exceed the smallest coherent slice for this ticket.

**Acceptance criteria (given/when/then):**
- Given a cache miss, when a user loads the summary chart, then the
  underlying aggregate query runs once and the result is cached for 5
  minutes.
- Given a cache hit within the 5-minute TTL, when any user in the same
  organization loads the summary chart, then the response comes from cache
  in under 500ms, with no re-execution of the underlying query.
- Given the TTL expires, when the next request arrives, then the cache is
  repopulated from a fresh query - no manual invalidation path is required
  for this scope.

**Explicit non-goals:** This does not add explicit write-triggered
invalidation (the TTL alone satisfies the confirmed staleness tolerance),
and does not extend caching to the activity feed or settings panel without
a separate, explicit request for those paths.
