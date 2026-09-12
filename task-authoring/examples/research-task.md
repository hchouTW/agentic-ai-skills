# Investigate Whether Shared Reference Files Should Be Deduplicated Across Skills

## Background

`agile-development/references/cpp-balanced-design-guidelines.md` and
`deep-learning/references/cpp-balanced-design-guidelines.md` are two
independent copies of the same content (confirmed byte-identical by direct
diff). `agile-development/VALIDATION.md` already notes, in its own
Limitations section, that the two files are "shared verbatim" and that
"consistency between the two copies was checked... but the guidance itself
was not re-validated" by that process - meaning the duplication is a known,
accepted state today, maintained by hand rather than by tooling. This task
investigates whether that hand-maintained duplication should become a single
shared source instead, before it silently drifts.

## Objective

Produce a recommendation - not an implementation - on whether
`agentic-ai-skills` should deduplicate reference files shared verbatim across
multiple skills (starting with `cpp-balanced-design-guidelines.md`), backed
by a concrete inventory of what is currently duplicated, the tradeoffs of
each deduplication mechanism available in this repository's constraints, and
a recommended path forward.

## Scope

### In Scope

- Inventory every reference file that is byte-identical (or near-identical)
  across two or more skills in this repository.
- Evaluate deduplication mechanisms compatible with this repository's
  constraint that skills must remain self-contained, portable folders (per
  the root `README.md`'s description) copyable independently into
  `~/.claude/skills/`, `~/.codex/skills/`, etc.
- Recommend one approach (keep hand-duplicated with a drift check, symlink,
  a shared top-level `shared/` folder with per-skill copy-in tooling, or
  another option found during investigation) with explicit tradeoffs.

### Out of Scope

- Actually performing the deduplication - this is a research/investigation
  task; implementation is a separate, later task once a direction is
  chosen.
- Auditing content correctness of the duplicated guidance itself (whether
  the C++ guidelines are good guidelines) - out of scope, this task is about
  duplication mechanics only.

## Repository Context

Verified by direct inspection on 2026-09-12:

- `agile-development/references/cpp-balanced-design-guidelines.md` and
  `deep-learning/references/cpp-balanced-design-guidelines.md` are
  byte-identical (`diff -q` reports no difference).
- `agile-development/VALIDATION.md`'s "Limitations" section already
  documents this specific duplication and states it was checked for
  byte-equality but not otherwise re-validated - this is Confirmed prior
  awareness, not a new finding.
- The root `README.md` describes every skill as "a self-contained folder"
  with no dependency on an MCP server, cloud account, or paid service, and
  documents installation as a plain `cp -r` of individual skill folders into
  a target skills directory - any deduplication mechanism that breaks
  independent copy-ability of a single skill folder would conflict with this
  documented installation model.
- No other duplicated reference file was confirmed during this pass - a
  full pairwise diff across all `references/` directories in all five skills
  was not performed as part of authoring this task and is itself part of
  the requested inventory (Technical Approach step 1).

## Technical Approach

1. Run a pairwise comparison of every `references/*.md` file across all five
   skills (`skill-router`, `agile-development`, `deep-learning`,
   `hep-analysis`, `academic-papers`) to build a complete inventory of
   byte-identical or near-identical files, not just the one pair already
   known.
2. For each duplicated set found, note which skills reference it and how
   central it is to each skill's own `SKILL.md` routing.
3. Enumerate deduplication mechanisms compatible with the `cp -r`,
   single-folder installation model documented in the root `README.md`
   (e.g.: keep as-is with a repo-level script that fails CI-style checks on
   drift; a symlink within the repository, which would not survive a plain
   `cp -r` of a single skill folder into an external skills directory
   without also copying the link target; a `shared/` top-level folder with
   a build step that copies content into each skill's `references/` before
   distribution).
4. Recommend one mechanism, with explicit tradeoffs against the others,
   including what happens when a skill folder is copied out of this
   repository on its own (the primary installation path today).

## Deliverables

- A written inventory of every duplicated reference file across all five
  skills, as a table (skill pairs, file path, byte-identical yes/no).
- A short comparison of deduplication mechanisms and their tradeoffs against
  the single-folder installation model.
- A concrete recommendation, including any follow-up implementation task
  this investigation should spawn if the recommendation is to proceed.

## Acceptance Criteria

- The inventory covers all five skills' `references/` directories, not just
  the already-known `cpp-balanced-design-guidelines.md` pair.
- Each duplication finding states how it was verified (e.g. `diff -q`
  output), not just asserted.
- The recommendation explicitly addresses the single-folder,
  independently-copyable installation model documented in the root
  `README.md` - a recommendation that silently breaks that model is not
  acceptable without calling out the tradeoff.
- The task's own Open Questions are resolved or explicitly deferred with a
  stated reason, not left silently unaddressed in the final write-up.

## Validation

- Re-run the pairwise `diff` comparisons underlying the inventory and
  confirm the reported results are reproducible.
- Manual review of the recommendation against the root `README.md`'s
  documented installation and portability constraints.

## Open Questions

- Is any additional duplicated reference file expected beyond
  `cpp-balanced-design-guidelines.md`, or is that pair the only instance in
  the repository today? **TBD** - this task's own Technical Approach step 1
  is the mechanism to answer this; it was not pre-answered here to avoid
  duplicating that step's work.
- Would the repository's maintainer accept a symlink-based approach that
  changes the "plain `cp -r` of a self-contained folder" installation
  story, or is preserving that story a hard constraint? **Requires
  Confirmation.**
- Should this investigation also cover duplicated `assets/` or `examples/`
  content, or is it scoped to `references/` only as stated? **Requires
  Confirmation** - this task assumes `references/` only, per the specific
  finding that motivated it, but the same duplication risk could exist
  elsewhere and was not checked here.

## References

- `agentic-ai-skills/agile-development/VALIDATION.md` - "Limitations"
  section, the existing prior-awareness note this task builds on.
- `agentic-ai-skills/agile-development/references/cpp-balanced-design-guidelines.md`
  and
  `agentic-ai-skills/deep-learning/references/cpp-balanced-design-guidelines.md` -
  the confirmed duplicated pair.
- `agentic-ai-skills/README.md` - the documented single-folder installation
  model this task's recommendation must account for.
