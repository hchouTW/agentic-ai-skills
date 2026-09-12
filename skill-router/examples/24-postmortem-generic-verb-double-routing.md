---
role: Site Reliability / Principal Skill-Router Maintainer
skill: skill-router
archetype: postmortem
incident: Two routing-rule bullets both claimed the generic verb "update" with no specificity ordering between them, causing recurring ambiguous double-routing on real requests
---

## 1. Incident Symptom & Alert Payload

```
[Recurring pattern flagged in weekly session-quality review, 2025-01-09]
occurrences_this_week: 6
example transcript 1: "can you update the checkpoint-loading code to handle
  the new optimizer state format?"
  -> Assistant stated "Using `agile-development` skill" only; deep-learning
     never mentioned, despite "checkpoint," "optimizer state" being clearly
     PyTorch-specific.
example transcript 2 (same week, different session): identical prompt
  wording style -> Assistant stated "Using `deep-learning` skill (primary),
  with `agile-development` for task breakdown" - the OPPOSITE resolution
  for a near-identical request.
```

Both `agile-development` (triggers on the verb "update") and
`deep-learning` (covering "checkpointing" and "optimizer" content) matched
these requests, but which one won - or whether both were named - varied
session to session with no consistent rule producing the difference.

## 2. Immediate Triage & Blast-Radius Mitigation

Per `SKILL.md`'s own Behavior section (checked against the actual routing
text, not assumed from memory), the router maintainer confirmed that
neither rule's text contained an explicit specificity ordering or carve-out
for this overlap - unlike the precedent already established in example
`10-decision-tree-multi-skill-ambiguous-routing.md` for a different
overlap pair, this exact "update... optimizer/checkpoint code" overlap had
never been resolved in writing. Since the inconsistency was a
routing-quality issue rather than an active incorrect action being taken,
the maintainer's mitigation was to add an explicit resolution note to
`SKILL.md` immediately (rather than waiting for a larger rule rewrite),
so any session reading the current rules from that point forward would
resolve the case the same way.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did the same style of request route two different ways in two
   different sessions?** Because both `agile-development`'s bullet
   (triggering on the bare verb "update... code") and `deep-learning`'s
   bullet (covering "checkpointing," "optimizer," "mixed precision")
   matched the request text, and `SKILL.md` gave no explicit rule for
   which one takes precedence when both match on a request that is
   simultaneously "a code update" and "PyTorch-specific."
2. **Why did `SKILL.md` have no explicit precedence rule for this
   overlap?** Because the specificity-ordering precedent that does exist
   in this repository (example `04-decision-tree-multi-skill-ambiguous-
   routing.md`'s "a more specific domain rule wins over a generic
   code-change trigger for the same code path") was established for a
   different concrete overlap (ROOT-macro refactor requests versus
   `agile-development`'s generic fix/refactor trigger) and was never
   generalized into `SKILL.md`'s own rule text as a standing principle
   applicable to *any* generic-verb-versus-domain-rule overlap.
3. **Why wasn't the precedent generalized into `SKILL.md` itself instead
   of living only in one example file?** Because examples in this
   repository are illustrative worked cases, not themselves part of the
   enforced routing logic - `SKILL.md`'s Behavior section is the only text
   actually consulted at routing time, and a lesson captured only in an
   example file has no effect on a session that reads `SKILL.md` without
   also happening to have that example in context.
4. **Why did different sessions produce different resolutions of the
   same ambiguity if none of them had the precedent available either?**
   Because with no written rule to anchor the decision, the choice of
   "invoke primary + secondary" versus "invoke one alone" became sensitive
   to incidental differences in how each session's context happened to
   frame the request - an unanchored judgment call, not a deterministic
   rule application, will vary run to run.
5. **Why did this take six occurrences in one week, rather than the first
   occurrence, to get flagged?** Because no automated check compares
   routing decisions across sessions for the same or similar prompt
   patterns - the inconsistency was only visible because a human
   reviewer happened to read two transcripts with near-identical wording
   in the same weekly review batch.

Root cause: a specificity-ordering principle needed to resolve the
"generic verb versus domain-specific rule" overlap class existed only as
an illustrative precedent in one example file, not as an explicit,
generalized rule in `SKILL.md` itself, so any request falling in that
overlap had no anchored resolution and routing outcomes varied
unpredictably session to session.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/skill-router/SKILL.md
+++ b/skill-router/SKILL.md
@@ -68,6 +68,11 @@
 ## Behavior
 
+**Specificity ordering for a generic code-change verb (implement/fix/add/
+refactor/migrate/update) that also matches a domain skill's own more
+specific content:** the domain skill's rule wins alone when the request's
+substance is fully covered by that domain's own terms (e.g. "update the
+checkpoint-loading code for the new optimizer state format" is
+`deep-learning` alone, not `deep-learning` + `agile-development`) - see
+`examples/10-decision-tree-multi-skill-ambiguous-routing.md` for the
+worked precedent this rule generalizes.
+
 1. Exactly one skill relevant: state "Using `<skill-name>` skill." and invoke
```

```diff
--- a/skill-router/tests/test_skill_router.py
+++ b/skill-router/tests/test_skill_router.py
@@ -80,3 +80,10 @@ class RoutingRuleParsingTests(unittest.TestCase):
+    def test_specificity_ordering_rule_present_in_behavior_section(self):
+        text = Path("SKILL.md").read_text()
+        behavior_section = text.split("## Behavior")[1]
+        self.assertIn(
+            "Specificity ordering for a generic code-change verb",
+            behavior_section,
+        )
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the specificity-ordering precedent was
correctly worked out and documented for the concrete case it was written
for, and nothing at the time indicated that lesson needed to be
generalized into the enforced rule text rather than left as one
illustrative example among many.

**What worked:** the weekly session-quality review, even though manual,
was the actual mechanism that caught the inconsistency - without it, six
occurrences in one week could easily have continued indefinitely with no
signal.

**What didn't work:** relying on an example file to carry a
generally-applicable principle meant the principle only helped a session
that happened to have that specific example in context, rather than every
session reading `SKILL.md` - a lesson learned once was not a lesson
applied everywhere.

**Preventative monitoring rule:**
`test_specificity_ordering_rule_present_in_behavior_section` runs in CI
and blocks (non-zero exit) any `SKILL.md` change that removes the
specificity-ordering rule text from the Behavior section, and the weekly
session-quality review now explicitly flags any prompt pair with greater
than 80% text similarity that received two different routing decisions
within the same 7-day window.
