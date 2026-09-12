---
role: Site Reliability / Principal Skill-Router Maintainer
skill: skill-router
archetype: postmortem
incident: A new routing-rule bullet was merged without a carve-out against an existing rule's keyword, causing the router to hijack unrelated requests for two days before it was noticed
---

## 1. Incident Symptom & Alert Payload

```
[User-reported session transcript, 2025-08-04]
User: "can you check if this dataset has a memory leak in the dataloader?"
Assistant: "Using `hep-analysis` skill." <- WRONG: this is a PyTorch
  DataLoader question, not a HEP dataset question; deep-learning never
  triggered.

--- skill-router maintainer's own regression log, retroactively run ---
prompt: "can you check if this dataset has a memory leak in the dataloader?"
matched rule: hep-analysis (keyword: "dataset")
matched rule: deep-learning (keyword: "DataLoader", "memory")
router behavior observed: hep-analysis invoked alone (first-listed rule
  in SKILL.md wins on unresolved multi-match - undocumented behavior,
  not a designed tie-break)
```

The `hep-analysis` bullet's addition of the bare word "dataset" (added two
days earlier, in the same edit that added "ntuples, event selections") had
no carve-out excluding the very common phrase "this dataset" in a
non-physics, PyTorch-specific context.

## 2. Immediate Triage & Blast-Radius Mitigation

Per the actual current `SKILL.md` Behavior rule 2 ("multiple relevant:
state the primary and any secondary skill(s)... invoke the primary
first"), the router maintainer's first action was to revert the specific
`SKILL.md` edit that added the bare "dataset" keyword to the
`hep-analysis` bullet, rather than attempting to add a carve-out under
time pressure - a revert restores the previously-correct, tested behavior
immediately, while a new carve-out risks introducing its own gap without
review. The revert was a one-line change to `SKILL.md` and took effect
immediately since routing is evaluated fresh on every request with no
caching or rollout delay.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did a PyTorch DataLoader question get routed to `hep-analysis`
   instead of `deep-learning`?** Because `hep-analysis`'s routing bullet
   was edited two days earlier to add the bare keyword "dataset" (intended
   to catch phrases like "our HEP dataset"), and the word "dataset" alone,
   with no accompanying HEP-specific term, also matches countless
   PyTorch/ML requests that mention "this dataset" or "the dataset."
2. **Why did adding "dataset" to `hep-analysis`'s rule cause it to win
   over `deep-learning`'s rule, which clearly also matched via
   "DataLoader"?** Because `SKILL.md`'s Behavior section documents what to
   do when multiple skills are relevant (state primary and secondary), but
   the actual routing decision in this session picked only `hep-analysis`
   and never mentioned `deep-learning` at all - the "multiple relevant"
   path was never reached because the triage step stopped at the first
   rule whose bullet text happened to contain a literal substring match,
   rather than evaluating every rule's full text as the Behavior section
   assumes.
3. **Why did the PR that added "dataset" to the `hep-analysis` bullet not
   get flagged during review as a likely collision?** Because there is no
   automated check that a newly-added keyword in one skill's routing
   bullet doesn't also appear, unqualified, in a way that plausibly
   matches another skill's core domain - review relied entirely on the
   reviewer manually noticing the collision, and the reviewer approving
   this specific change was focused on the HEP-specific terms in the same
   diff ("ntuples, event selections") and did not separately stress-test
   the newly-added bare word "dataset" against unrelated domains.
4. **Why does `skill-router`'s own bundle validator not catch an
   overly-generic keyword addition?** Because
   `scripts/validate_skill_bundle.py` checks structural properties of the
   bundle (required files, README sections, routing-table skill names
   matching sibling directories) but has no check for keyword specificity
   or cross-rule collision risk - that class of check does not exist in
   this repository's tooling today.
5. **Why did it take a user-reported wrong routing, rather than internal
   testing, to surface the collision?** Because this repository's example
   suite (`examples/*trajectory*`, `*decision-tree*`) covers specific,
   hand-picked ambiguous-routing scenarios chosen in advance, not a
   systematic sweep of "does any single-word rule addition collide with
   another skill's core vocabulary" - a new keyword's blast radius against
   the *existing* rule set was never mechanically checked before merge.

Root cause: a routing-rule edit added a single, unqualified, high-frequency
keyword ("dataset") to one skill's bullet without checking it against
every other skill's core vocabulary, and no tooling in this repository
checks a new keyword's collision risk before merge - the gap was only
found when a real ambiguous request happened to hit it.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/skill-router/SKILL.md
+++ b/skill-router/SKILL.md
@@ -49,7 +49,8 @@
 - **hep-analysis** - collider and particle-physics data and simulation: ROOT
   C++, PyROOT, RDataFrame, uproot/awkward columnar pipelines, ntuples, event
-  selections, cutflows, histograms, efficiencies and scale factors, dataset,
+  selections, cutflows, histograms, efficiencies and scale factors, a
+  physics dataset/ntuple production or selection (not a PyTorch
+  Dataset/DataLoader - see deep-learning for that),
   backgrounds, unfolding, systematic uncertainties, RooFit/RooStats, pyhf,
```

```diff
--- a/skill-router/scripts/check_keyword_collisions.py
+++ b/skill-router/scripts/check_keyword_collisions.py
@@ -0,0 +1,18 @@
+#!/usr/bin/env python3
+"""Flag any bare, unqualified keyword added to one skill's routing bullet
+that also appears as a bare term in another skill's own domain vocabulary
+list (see postmortem: 'dataset' collision between hep-analysis and
+deep-learning). Run in CI on every SKILL.md diff."""
+GENERIC_TERM_DENYLIST = {"dataset", "model", "data", "pipeline", "test"}
+
+def check_no_bare_generic_terms(rule_text: str, skill_name: str) -> list[str]:
+    problems = []
+    for term in GENERIC_TERM_DENYLIST:
+        if bare_word_present(rule_text, term):
+            problems.append(
+                f"{skill_name}: bare generic term {term!r} needs a "
+                f"qualifying phrase or an explicit carve-out"
+            )
+    return problems
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the reviewer who approved the "dataset" keyword
addition was correctly focused on the HEP-specific content of that same
diff, and had no tooling flagging that a bare, unqualified term was being
added - the review process gave no signal that this specific word carried
cross-domain collision risk.

**What worked:** reverting the single-line keyword addition, rather than
attempting to hand-craft a carve-out under time pressure, restored correct
routing immediately with no risk of introducing a second, different gap.

**What didn't work:** the repository's example-based regression suite
covers scenarios chosen in advance and gave no signal about this specific,
newly-introduced collision - a new keyword's risk against the full
existing rule set was never mechanically checked.

**Preventative monitoring rule:** `scripts/check_keyword_collisions.py`
runs in CI on every `SKILL.md` change and blocks (non-zero exit) merging
any routing-bullet edit where more than 0% of its newly-added bare terms
match the cross-skill denylist without an accompanying qualifying phrase
or carve-out clause in the same diff.
