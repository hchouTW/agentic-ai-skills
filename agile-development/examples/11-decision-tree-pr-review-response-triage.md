---
role: Staff Software Engineer
skill: agile-development
archetype: decision-tree
scenario: reviewing a colleague's pull request and deciding how to respond to each category of finding
---

## Triage Matrix

Formalizes `references/risk-and-quality.md`'s "Reviewing Someone Else's
Change" section - "distinguish severity explicitly... a correctness or
security problem blocks merge; a style or naming preference does not" - into
an explicit finding-to-response mapping:

| Trigger | Resolution Strategy |
|---|---|
| The change's intent isn't stated and isn't clear from the diff itself | Ask the author what problem this solves before reviewing the implementation against a guessed goal |
| A correctness or security defect is found (a race condition, an unvalidated input, a leaked credential) | Block merge with a specific, actionable comment describing the exact failure scenario, not a general "this looks unsafe" |
| The diff's tests exist and pass, but don't actually exercise the stated acceptance criteria or bug report | Block merge and request a test that would fail without the fix, not just any passing test |
| Only a style or naming preference is at stake, with no violated, enforced project convention | Leave it as a non-blocking suggestion and approve once the blocking items (if any) are resolved |
| The description claims something checkable ("ran the full suite," "verified in staging") | Verify the claim directly (CI status, a linked run) before trusting it, rather than approving on the strength of the claim alone |

## Selected Branch

The PR under review changes the checkout discount-calculation path. Its
description says "ran the full suite locally, all green," but the linked CI
run on the PR itself shows a red X on the integration-test job. This matches
the fifth row: a checkable claim that should be verified directly rather than
trusted, per `references/risk-and-quality.md`'s explicit instruction to check
a linked run rather than take the claim at face value.

## End-to-End Execution Script

1. Open the PR's CI run directly rather than trusting the description:
   `gh pr checks 4821` shows `integration-tests: fail`, contradicting "all
   green."
2. Read the failing job's log: `test_discount_stacking_order_independence`
   fails, asserting `apply_discounts(50.00, [FLAT5, PCT10]) ==
   apply_discounts(50.00, [PCT10, FLAT5])` - exactly the kind of behavior
   this diff touches.
3. Post a review comment, specific and actionable rather than generic: "The
   PR description says the full suite passed locally, but the CI run linked
   on this PR (`gh pr checks 4821`) shows `integration-tests` failing on
   `test_discount_stacking_order_independence` - can you confirm whether
   this was run against the latest commit? Blocking on this until CI is
   green, since it's exactly the behavior this diff changes."
4. Mark the review "Request changes," not "Comment," since a failing test
   covering the exact changed behavior is a correctness question, not a
   style note - per the matrix's severity-distinction row.
5. Once the author pushes a fix and CI goes green on the same commit, verify
   the specific previously-failing test now passes in that run (not just that
   the job is green overall) before approving.

## Fallback Safeguards

If the author replies that the local run was against an older commit and the
new push fixes it, do not approve on that explanation alone - re-check the
now-current CI run's status directly, since the same "trust the claim, don't
check the linked run" gap that caused the original miss would also excuse
approving on a second unverified claim. If the failing test turns out to be
flaky rather than a real regression (i.e., re-running the same commit's CI
passes on retry with no code change), re-triage against the matrix's third
row instead - confirm the test actually exercises the intended behavior
before dismissing the failure as flakiness, since a flaky test that happens
to cover real behavior is still worth stabilizing, not just re-running.
