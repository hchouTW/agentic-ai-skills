---
role: Lead Platform / Developer-Experience Engineer
skill: skill-router
archetype: decision-tree
scenario: an ambiguous request that touches multiple domain skills at once, e.g. refactoring a PyTorch training loop so a paper's reproducibility section can describe it accurately
---

## Triage Matrix

Generalizes the reasoning behind `SKILL.md`'s Behavior rules 2-4 into an
explicit trigger -> strategy mapping for the cases where more than one rule's
text plausibly matches the same request:

| Trigger | Resolution Strategy |
|---|---|
| Exactly one rule's territory matches, with no overlapping keyword from any other rule | Invoke that single skill only, per Behavior rule 2 |
| Two rules match genuinely different layers of the same request (e.g. the technical work vs. the manuscript prose describing it) | State the primary and secondary skill explicitly and invoke the primary first, per Behavior rule 3 |
| A request's code-change verb ("refactor", "fix", "add") is fully covered by a domain skill's own more specific rule for that exact code path (e.g. `deep-learning`'s "training and eval loops") | Treat that domain skill as sufficient for the code; do not also invoke `agile-development`'s generic code-change trigger on top of a domain skill that already owns this path |
| A keyword superficially matches a rule but that rule's own text carves it out explicitly | Proceed with no skill invoked, per Behavior rule 4 |
| Two rules plausibly both apply and nothing in the request signals which is primary | State the assumed primary/secondary split as an explicit assumption and proceed, rather than pausing to ask, since a routing choice is cheap to reverse if wrong |

## Selected Branch

The request: "Refactor this PyTorch training loop so the paper's
reproducibility section can describe it accurately." This matches the third
row: the code-change verb "refactor" applies to a training loop, which
`deep-learning`'s rule already covers by name ("training and eval loops...
reproducibility"), so `agile-development`'s generic "refactor... code"
trigger is not separately invoked on top of it. Combined with the second row,
the paper's reproducibility-section prose is a distinct write-up layer that
`academic-papers`'s rule owns ("drafting, restructuring, or polishing a paper
or section"). The selected branch is therefore: `deep-learning` as primary
(for the code), `academic-papers` as secondary (for the prose), and
`agile-development` not invoked as a third skill.

## End-to-End Execution Script

> Using `deep-learning` skill (primary), with `academic-papers` for the
> reproducibility-section prose.
>
> [`deep-learning` is invoked first and refactors the training loop per its
> own reproducibility guidance: extracting the scattered seed-setting and
> determinism-flag calls (`torch.manual_seed`, `torch.backends.cudnn.
> deterministic`, dataloader worker seeding) into a single
> `set_reproducible_mode(seed)` function called once at the start of
> training, and recording the exact package versions and hardware used in a
> `run_manifest.json` written alongside each checkpoint. This produces a
> concrete, itemized list of what changed and why each item affects
> reproducibility.]
>
> [That itemized list is then handed to `academic-papers`, which drafts the
> reproducibility-section prose describing exactly those changes in past
> tense, in the paper's established register, with a pointer to the public
> code repository's commit hash rather than restating the diff inline -
> matching this skill's own convention of describing what was done rather
> than including the code itself in manuscript prose.]
>
> [`agile-development`'s generic "refactor... code" trigger was checked and
> found to be fully subsumed by `deep-learning`'s own training-loop workflow
> for this specific change, so it was noted but not separately invoked.]

## Fallback Safeguards

If the training loop turns out to be part of a shared production pipeline
that other teams depend on - not a single paper's standalone experiment code
- `deep-learning`'s own workflow alone is no longer sufficient: escalate to
also invoking `agile-development` for the surrounding process discipline
(acceptance criteria, review, staged rollout) that a shared-dependency change
needs and a single-paper refactor does not. If instead the "reproducibility
section" turns out to require re-deriving a systematic uncertainty rather
than describing already-decided code changes in prose, the trigger was
misclassified: re-triage against the matrix's second row as a genuine
two-technical-layers case (recompute the uncertainty, then write it up)
instead of treating the write-up half as prose-only.
