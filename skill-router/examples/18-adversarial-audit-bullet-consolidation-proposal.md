---
role: ruthless Staff Prompt Engineer / Red-Teamer
skill: skill-router
archetype: adversarial-audit
candidate_artifact: "Proposal to merge the academic-papers and hep-analysis routing-rule bullets into one combined \"physics-writing-and-analysis\" bullet, to reduce duplication between two entries that both mention physics terminology."
---

## 1. Initial Candidate Artifact

A contributor proposes merging `SKILL.md`'s `academic-papers` and
`hep-analysis` bullets, arguing they overlap heavily (both mention physics
terminology, both can apply to the same paper-writing task) and that
maintaining two separate carve-out clauses that reference each other is
duplicative. The proposed merged bullet:

```
- **physics-writing-and-analysis** - reading, critiquing, or writing
  scientific papers and physics analyses: manuscript drafting/formatting,
  literature reviews, referee responses, LaTeX/BibTeX work, ROOT/PyROOT/
  RDataFrame pipelines, cutflows, histograms, systematics, fits, limits,
  and detector/simulation topics. Covers the full pipeline from running an
  analysis to writing it up.
```

This looks like a reasonable simplification: the current bullets do
explicitly cross-reference each other ("Not the underlying statistical/
ML/physics analysis - see `deep-learning`/`hep-analysis` for that" and
implicitly the reverse), and "reduce duplication" is a stated goal
`references/software-architecture.md`-style guidance elsewhere in this
repository generally favors when a real, stable shared abstraction exists.

## 2. Attack Vectors & Stress-Tests

**Attack Vector 1: the merge deletes the one clause that currently prevents
"analysis" language from routing every physics-writing request to the wrong
half of the actual work.**
The current `academic-papers` bullet's carve-out - "Not the underlying
statistical/ML/physics analysis - see `deep-learning`/`hep-analysis` for
that; this is the reading/writing/formatting layer on top of it" - exists
specifically to keep "writing about a fit result" (academic-papers'
territory: prose, structure, citations) separate from "producing the fit
result" (hep-analysis's territory: RooFit, systematics, the actual
numbers). The merged bullet's combined trigger list ("cutflows, histograms,
systematics, fits, limits" alongside "manuscript drafting") reintroduces
exactly the keyword collision the carve-out currently prevents: a request
like "improve the wording of this systematics paragraph" would now match
"systematics" in the same bullet that also claims manuscript drafting, with
no signal for whether the request wants prose editing (previously
academic-papers, ~90% of this repository's academic-papers examples) or a
redone systematics study (previously hep-analysis).

**Attack Vector 2: "the full pipeline from running an analysis to writing
it up" is not one skill's actual competency area - it silently drops both
skills' `description` frontmatter specialization, which is what the router
actually uses for triage in practice, not just the bullet prose.**
Both current skills carry a highly specific `description:` field
(academic-papers' opens with paper-lifecycle language; hep-analysis's
covers ROOT/PyROOT/RDataFrame/detector-systems tooling) that a downstream
router or model uses as the actual matching signal, with the `SKILL.md`
bullet serving secondary, human-readable documentation of the same
boundary. Merging the bullets without also merging the two skills'
entire reference libraries (14 hep-analysis reference docs on detector
physics and statistics vs. 36 academic-papers reference docs on writing
and publication process - two non-overlapping bodies of domain material)
would route a request to a single named skill whose actual `SKILL.md`
content and reference set still only cover half of what the merged bullet
now claims, silently breaking the promise the merged bullet makes.

## 3. Concrete Counter-Example / Exploit Proof

Checking the merged bullet against a request already covered by an
existing worked example in this repository - `academic-papers/examples/
16-adversarial-audit-statistical-significance-derivation.md` - which
audits a manuscript's *derivation* of a significance claim (a writing/
argument-structure task, resolved via `mathematical-reasoning-and-proof.md`)
as distinct from *computing* a significance value from data (a hep-analysis
task, resolved via `08-inference.md`/`09-statistical-tools.md`):

```
Request: "This paper's significance claim looks off - can you check it?"
```

```
Against current (unmerged) bullets:
- academic-papers matches: "reading, critiquing... scientific papers,"
  with the explicit carve-out directing "the underlying statistical...
  analysis" to hep-analysis - so the router can ask (or infer from
  context) whether "check it" means check the paper's argument/derivation
  or recompute the analysis, and route accordingly.

Against the proposed merged bullet:
- "physics-writing-and-analysis" matches on both "reading... papers" and
  "fits, limits" simultaneously, inside one bullet with no internal
  boundary - the router has no textual basis left to distinguish "audit
  the paper's math" (a `mathematical-reasoning-and-proof.md` task) from
  "redo the significance calculation" (a `references/08-inference.md`
  task), because the clause that used to draw that line was deleted along
  with the bullet split.
```

The merge does not just reduce line count - it deletes the router's only
mechanism for resolving this exact, already-documented ambiguity, on a
request type this repository already has a worked example proving needs
disambiguation.

## 4. Hardened Architectural Patch

```diff
--- a/proposals/merge_academic_papers_hep_analysis.md
+++ b/proposals/merge_academic_papers_hep_analysis.md
@@
-- **physics-writing-and-analysis** - reading, critiquing, or writing
-  scientific papers and physics analyses: manuscript drafting/formatting,
-  literature reviews, referee responses, LaTeX/BibTeX work, ROOT/PyROOT/
-  RDataFrame pipelines, cutflows, histograms, systematics, fits, limits,
-  and detector/simulation topics. Covers the full pipeline from running an
-  analysis to writing it up.
+Proposal withdrawn as a bullet merge. The two skills' carve-out clauses
+are not duplication to be removed - they are the disambiguation mechanism
+for a genuinely recurring overlap (writing about a result vs. computing
+it), documented as needing exactly this distinction in
+academic-papers/examples/16-adversarial-audit-statistical-significance-derivation.md.
+If bullet *wording* duplication is the actual concern (e.g. both bullets
+separately spelling out a similar carve-out sentence structure), address
+it by keeping both bullets and both carve-outs, but cross-referencing them
+more tersely:
+
+- **academic-papers** - ...(unchanged)... Not the underlying statistical/
+  ML/physics analysis - see `deep-learning`/`hep-analysis` for that; this
+  is the reading/writing/formatting layer on top of it.
+- **hep-analysis** - ...(unchanged)... For the paper-writing layer on top
+  of an analysis (drafting, formatting, citations), see `academic-papers`
+  instead - this bullet covers producing the analysis result itself.
```

The hardened outcome is not a smaller merged bullet but a decision *not* to
merge, with the disambiguation clause kept on both sides and made
symmetric (each bullet now points to the other, not just one direction) so
future edits are less likely to drop the pointer from only one side.

## 5. Proof of Robustness Post-Fix

Re-running Section 3's exploit request against the hardened (unmerged,
now-symmetric) bullets: "This paper's significance claim looks off - can
you check it?" still matches both bullets' surface vocabulary, but each
bullet's carve-out now explicitly names the other as the destination for
the half of the request it doesn't own, in both directions - a router (or
a human reading `SKILL.md`) has textual grounds to ask "do you mean the
argument/derivation in the paper, or the underlying computed value?" and
route to `academic-papers` or `hep-analysis` respectively, exactly matching
the disambiguation already demonstrated as necessary in the existing
adversarial-audit example. Re-running Attack Vector 2's reference-library
check: since no merge occurred, each skill's own reference set
(hep-analysis's statistics/detector docs, academic-papers' writing/
publication docs) remains attached to the bullet that actually documents
matching competency, so no request is routed to a skill whose own
`SKILL.md` and references cover only half of what its bullet claims.
