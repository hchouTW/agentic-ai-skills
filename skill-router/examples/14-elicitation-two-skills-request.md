---
role: Principal Skill-Router Maintainer
skill: skill-router
archetype: elicitation
user_request: "This request should probably use two skills, can you check?"
---

## 1. Raw Ambiguous Input

Message from a contributor reviewing a routing bug report:

> This request should probably use two skills, can you check? Someone said
> the router only picked one.

No named skills, no example request text, and no statement of which skill
the router actually picked versus which one it should have also picked.

## 2. Missing Constraint Analysis

Per `SKILL.md`'s "Behavior" section, rule 2 explicitly covers the
multi-skill case: "Multiple relevant: state the primary and any secondary
skill(s) ... Invoke the primary first." Diagnosing a reported miss requires
knowing the actual request text and which two (or more) skills' routing
rules plausibly match it - without that, there's no way to tell whether
this is a genuine primary+secondary case the router missed, or a case
where only one skill actually applies and the bug report is mistaken.

Specifically missing:
- **The actual request text** - "someone said" is secondhand; the exact
  wording determines which routing-rule keywords are or aren't present.
- **Which two skills** are plausibly both relevant - `SKILL.md`'s own
  worked example is `deep-learning` (primary) + `agile-development` (task
  breakdown, secondary), but this report could involve any pair.
- **Which one is primary** - the behavior section requires stating a
  primary/secondary order, not just "both apply"; without knowing the
  request's actual center of gravity, the order can't be determined.
- **What the router actually did** - picked only one skill and stopped, or
  picked one and silently ignored the second, or didn't route to any skill
  at all - each is a different failure mode with a different fix.

## 3. Socratic Clarification Round

1. What is the exact request text that triggered the bug report?
   a) "Can you refactor this PyTorch training loop and also write up the
      acceptance criteria for the change?"
   b) A different request - would need to pull the exact wording from the
      original report
   c) Not available - the report only has a paraphrase
2. Which two skills are plausibly both relevant to that request?
   a) `deep-learning` and `agile-development`
   b) `hep-analysis` and `agile-development`
   c) `academic-papers` and `agile-development`
3. Which of the two should be primary?
   a) `deep-learning` primary (the request is fundamentally a PyTorch
      code change), `agile-development` secondary (for the acceptance-
      criteria framing)
   b) `agile-development` primary, the other secondary
   c) Not yet clear - depends on which part of the request came first or
      matters more to the requester
4. What did the router actually do when given this request?
   a) Routed to `deep-learning` only, silently dropping the
      `agile-development` secondary mention
   b) Routed to `agile-development` only, silently dropping `deep-learning`
   c) Didn't route to either skill

## 4. User Feedback Integration

The contributor's answers, after locating the original bug report thread:

- Q1 -> **a) The exact text is confirmed**: "Can you refactor this PyTorch
  training loop and also write up the acceptance criteria for the change?"
- Q2 -> **a) `deep-learning` and `agile-development`.** Both routing-rule
  bullets plausibly match: "PyTorch engineering... training/eval loops" and
  "scoping, task breakdown, acceptance criteria."
- Q3 -> **a) `deep-learning` primary.** The request's main verb and object
  ("refactor this PyTorch training loop") is the deep-learning change; the
  acceptance-criteria ask is in service of that change, matching
  `SKILL.md`'s own worked example pattern exactly.
- Q4 -> **a) Routed to `deep-learning` only**, dropping the secondary
  `agile-development` mention - confirmed from the session transcript in
  the bug report.

Each answer resolves one gap from section 2: Q1 supplies the exact request
text needed to check against routing-rule wording, Q2 identifies the two
plausibly-relevant skills, Q3 fixes the primary/secondary order per
`SKILL.md`'s own worked example, and Q4 confirms the actual failure mode
(secondary skill silently dropped, not a full non-route or a wrong single
route).

## 5. Final Mutually-Agreed Specification Document

**Outcome:** Confirm this is a genuine multi-skill routing case per
`SKILL.md`'s Behavior rule 2, and add a canonical example (or extend
existing test coverage) demonstrating the correct primary+secondary
statement for this request pattern, so future similar requests are
answered consistently.

**In scope:** Documenting the confirmed correct routing statement -
"Using `deep-learning` skill (primary), with `agile-development` for task
breakdown" - as the expected output for this request text; adding this
case to `skill-router`'s example/test coverage of multi-skill routing.

**Out of scope:** Changing the wording of either the `deep-learning` or
`agile-development` routing-rule bullets - both already correctly match
this request; the actual gap is in the *behavior* step (stating both,
not just the first match), not the routing-rule text.

**Acceptance criteria (given/when/then):**
- Given the request "Can you refactor this PyTorch training loop and also
  write up the acceptance criteria for the change?", when routed, then the
  response states `deep-learning` as primary and `agile-development` as
  secondary, per `SKILL.md`'s Behavior rule 2 wording pattern.
- Given the new example/test case, when reviewed, then it documents both
  the request text and the expected primary/secondary statement, so a
  future regression is detectable.

**Explicit non-goals:** This does not change either routing-rule bullet's
wording, and does not attempt to enumerate every possible two-skill
combination - only the confirmed, reported case is addressed.
