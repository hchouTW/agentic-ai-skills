# Package Validation Record

Validation date: 2026-09-05. Helper test environment: Python 3, standard library only.

## Completeness pass (2026-09-05)

This pass brought the package in line with the completeness level already
established for `hep-analysis` in this collection: a structural bundle validator,
an automated test suite, dual-environment (Codex/Claude Code) install docs
(`README.md`, `agents/openai.yaml`), and this validation record.

- `scripts/validate_skill_bundle.py` was added and confirmed to report all 18
  expected files present and non-empty, to reject a missing/emptied file, a broken
  `SKILL.md` frontmatter field, and a renamed `README.md` section heading (each
  induced failure was verified individually, then reverted).
- `tests/test_agile_skill.py` was added (10 tests, standard library only,
  `python3 -m unittest discover -s tests -v`):
  - `create_story_card.build_card` was checked for its default acceptance-criteria/
    validation text when none is supplied, for correctly substituting supplied
    `--criteria`/`--validation` values in place of the defaults, and for correct
    actor/capability/outcome interpolation into the story line.
  - The `create_story_card.py` CLI was run end to end (produces a story card on
    stdout) and with a required flag omitted (fails with `usage:` on stderr, not a
    traceback).
  - `validate_agile_notes.normalize_heading` was checked against `#`/`##` headings
    and non-heading lines.
  - `validate_agile_notes.check_file` was checked against a note missing three of
    four required sections and against a note with all four present.
  - The `validate_agile_notes.py` CLI was run against the shipped
    `assets/story-card.md` template (passes) and against a nonexistent file
    (exits 2 with a one-line "file not found" message, not a traceback - this was
    a defect found and fixed in the same pass as this validation record, see
    below).
- `README.md`'s documented quick-check commands (`create_story_card.py` with
  `--actor`/`--capability`/`--outcome`, `validate_agile_notes.py <file>`) were run
  as documented and matched the actual CLI, which is itself notable: before this
  pass, `README.md`/`SKILL.md` incorrectly documented `--title`/`--as`/`--want`/
  `--so-that` flags that the script never accepted (see below).
- `agents/openai.yaml` was parsed with PyYAML and confirmed to carry
  `display_name`/`short_description`/`default_prompt`.

Two defects were found and fixed as part of reaching this completeness level (the
first during the preceding cross-environment audit, the second as part of writing
the test suite above):

- `SKILL.md` documented `scripts/create_story_card.py` as taking
  `--title`/`--as`/`--want`/`--so-that`, but the script has always taken
  `--actor`/`--capability`/`--outcome`. Following the documentation as written
  would have failed immediately. Fixed the documented flags to match the script.
- `scripts/validate_agile_notes.py` raised a raw `FileNotFoundError` traceback
  (and, for a directory path, a raw `IsADirectoryError` traceback) instead of a
  clean message when given a path that could not be read. Fixed to catch
  `OSError` around the read and exit 2 with a one-line message.

## Coverage expansion pass (2026-09-05)

Added one new reference file, `references/design-and-estimation.md` (design docs/
RFCs, estimation and spikes, feature flags and progressive rollout), and extended
two existing ones with new sections: `references/engineering-playbook.md` gained
"Incident Response / Production Outage" and "Legacy Code Without Tests" scenario
playbooks (matching its existing numbered-steps style), and
`references/risk-and-quality.md` gained a "Reviewing Someone Else's Change"
section (matching its existing bulleted-checklist style). `SKILL.md`'s reference-
routing list, its frontmatter `description`, `README.md`'s coverage section, and
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` were all updated to match
(bundle now reports 19 files).

This content is process/workflow guidance for an LLM to follow rather than
independently executable code, so verification took the same form as the rest of
this file's "Limitations" section already describes for the pre-existing
reference material: internal consistency review (all new cross-links resolve; the
new sections' internal references to other files/sections in this package -
`product-framing.md`'s Slicing section, `SKILL.md`'s Decision Rules, the Bug Fix/
Refactor playbooks - were checked against the files/sections that actually
exist), and confirming the new content doesn't contradict or duplicate existing
guidance in the same files. The bundle validator and the full existing test suite
(`tests/test_agile_skill.py`, unrelated to this content) were re-run after the
change and remain green - see the Completeness pass above for what that suite
covers; it was not extended by this pass since the new content is prose guidance
with no new script to test.

## Implementation-discipline pass (2026-09-09)

Added `references/implementation-discipline.md`, covering four failure modes that show
up in the diff rather than in the plan: deciding whether to ask or assume on an
ambiguous request, writing the minimum code that solves the problem, keeping changes
surgical, and defining verifiable success criteria. Hooked it into `SKILL.md` at six
points (Core Workflow steps 1 and 5, two new Decision Rules, the reference-routing
list, both Quick Checklists, and the frontmatter `description`), extended
`scripts/validate_agile_notes.py` with two opt-in structure checks, and updated
`README.md`, `agents/openai.yaml`, `scripts/validate_skill_bundle.py`, the sibling
`skill-router` skill, and the repository README to match. Bundle now reports 20 files,
up from 19.

**Source and attribution.** The content was prompted by the MIT-licensed
`karpathy-guidelines` skill, itself derived from Andrej Karpathy's published
observations on common LLM coding failures. It was **rewritten and restructured**
rather than vendored: the four topics were reshaped into this package's voice, merged
with guidance the package already carried, and extended with the ask-vs-assume cost
rule that the source does not contain. Attribution with a link to the origin appears in
a footer on the new reference. No license text was vendored, because no text was
copied. Note that this repository still has no top-level LICENSE file of its own; that
was considered during this pass and deliberately left out of scope.

**A direct contradiction was found and resolved rather than merged.** The source
instructed "If something is unclear, stop. Name what's confusing. Ask." `SKILL.md:15`
instructed "If it's ambiguous, state a reasonable assumption rather than blocking."
These are opposite defaults, and appending both would have left the skill
self-contradictory on the first step of its own workflow. Both were replaced with a
single conditional rule keyed to cost and reversibility: ask first when a wrong guess is
expensive or hard to undo (schema, migration, published contract, user-visible
behavior, anything outward-facing), otherwise assume and state the assumption. A grep
sweep over `SKILL.md`, every reference, and every asset confirms the only remaining
instance of the old wording is the "otherwise" branch of the new conditional itself.

Overlap with existing content was mapped before writing, so the new reference states
what is new and defers where the package already covers something:

- Ask/assume was partially covered (`SKILL.md:15`, and the "prefer repository evidence
  over assumptions" decision rule); presenting competing interpretations and pushing
  back on a simpler approach were absent.
- **Simplicity was essentially absent.** The package covered *scope* slicing ("pick the
  smallest coherent slice") but not code simplicity - a correctly-scoped change can
  still be twice the code it needs. This was the largest real gap.
- Surgical changes were partially covered ("avoid unrelated refactors or formatting
  churn"); the orphan asymmetry - remove what your change orphaned, mention rather than
  delete pre-existing dead code - was stated nowhere.
- Verifiable criteria were covered as acceptance criteria; the per-step
  `step -> verify` plan format was not.

`scripts/validate_agile_notes.py` gained `--require-plan-verification` (every numbered
step must carry a verification, and placeholders such as "looks right", "it works" or
"done" are rejected) and `--require-assumptions` (adds an Assumptions heading to the
existing requirements rather than replacing them, which the pre-existing `--require`
flag would do). **Both are opt-in and off by default**, so notes that passed before
still pass - this was the explicit regression gate, verified by a test that feeds the
new check a note it would fail and confirms the default invocation still exits zero.

Validation performed:

- Step parsing was checked against four verification spellings (`->`, `-->`, the
  Unicode arrow, and a bare `verify:`), the `verification:` variant, case-insensitivity,
  both `1.` and `1)` numbering, and multi-step ordering. Prose containing the word
  "verify" outside a numbered line is correctly not parsed as a step.
- Placeholder rejection was checked against eight weak strings and five real
  verifications, including case and trailing-punctuation variants.
- The plan check distinguishes a missing verification from a placeholder one, reports
  both kinds together when both occur, reports the step number, truncates long step
  text, and treats a note with no numbered plan at all as a failure rather than a pass.
- The CLI was exercised for the regression gate above, for each new flag passing and
  failing, for the shipped `assets/story-card.md` still passing by default, and for a
  missing file still exiting 2 without a traceback when the new flags are present.
- 22 new tests were added to `tests/test_agile_skill.py` (10 pre-existing + 22 new = 32
  total, `python3 -m unittest discover -s tests -v`). The 10 pre-existing tests were not
  modified.

Structural checks: every relative Markdown link in the package resolves; the
contradiction sweep above is clean; and the diff was reviewed for unrelated churn,
since a change about surgical edits that sprawled into adjacent text would contradict
its own content.

## Consistency audit (2026-09-10)

A "check and reorganize" pass with no new content: read every reference file in
full, checked every relative Markdown link's display text against its actual
target, and cross-checked `SKILL.md`/`README.md` claims (documented flags,
required README sections, file coverage) against the scripts and files
themselves.

- Found and fixed three link-text/target mismatches, where a link inside
  `references/` displayed a `references/`-prefixed path as its text while
  pointing (correctly) at a bare sibling filename - confusing to a reader
  scanning link text, though the links themselves resolved:
  `references/engineering-playbook.md`'s pointer to `communication.md`, and
  two pointers in `references/design-and-estimation.md` (one to
  `product-framing.md`, used twice, one to `engineering-playbook.md`). All
  three now show the bare filename as both text and target, matching the
  convention already used everywhere else (e.g.
  `references/implementation-discipline.md`).
- No other inconsistencies found: every heading structure, cross-reference,
  documented CLI flag (`create_story_card.py`, `validate_agile_notes.py`), and
  README-section requirement checked out against the actual files.
  `references/cpp-balanced-design-guidelines.md` was confirmed still
  byte-identical to `deep-learning`'s copy and was not edited, consistent with
  the shared-file note in Limitations below.
- Bundle validator and the full test suite (32 tests) re-run clean after the
  fixes.

## Example-authoring capability pass (2026-09-10)

Added a reusable procedure for producing a canonical `<skill>/examples/` entry - a
"Common Weak Approach" vs. "Expert-Level Best Practice" contrast plus N key
takeaways - starting with `agile-development` itself, per the parameterized
generation prompt supplied for this initiative.

- Added `references/example-authoring.md` (the generation prompt, workflow,
  format spec, and correctness-review/cross-skill-dependency notes), hooked into
  `SKILL.md`'s reference-routing list, one new "Example Prompts This Skill
  Handles Well" entry, and the frontmatter `description`.
- Added `scripts/generate_skill_example.py` (stdlib-only scaffold: emits
  frontmatter + the four required section headers with placeholder markers,
  `--skill`/`--role`/`--use-case`/`--takeaways`/`--output`, same CLI shape as
  `create_story_card.py`) and `scripts/validate_skill_example.py` (stdlib-only:
  checks frontmatter fields, section presence/order, a 3-6 item Key Takeaways
  list, and a placeholder scan for TODO/TBD/FIXME/XXX, Lorem ipsum, bracketed
  stand-ins, leftover scaffold comments, and standalone `...` lines - same
  contract as `validate_agile_notes.py`, including a clean exit 2 with no
  traceback on a missing file).
- Added `tests/test_example_authoring.py` (20 new tests, function-level and CLI
  subprocess coverage for both scripts, including a test that the scaffold
  script's own output fails validation until filled in - the regression gate
  that proves the two scripts are actually wired together correctly).
- Extended `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` with the four
  new files above (bundle now reports 24 files, up from 20) and documented the
  two new commands in `README.md`'s Quick checks and Coverage and boundaries
  sections.
- Confirmed `python3 scripts/validate_skill_bundle.py` (24 files OK) and
  `python3 -m unittest discover -s tests -v` (52 tests: the 32 pre-existing plus
  20 new, none modified) both pass.

No defects were found in this pass; the scaffold/validator round-trip
(scaffold -> intentionally fails validation -> fill in the shipped good-example
fixture in the test suite -> passes) was the main design risk and is covered by
`test_generated_scaffold_fails_validation_until_filled_in` and
`test_valid_example_passes`.

## Dogfood pilot example pass (2026-09-10)

Added `agile-development`'s own first `examples/` entry, per Phase 2 of the
example-authoring initiative: one pilot, not a bulk batch.

- Scaffolded `examples/01-bug-fix-scoping-review.md` with
  `generate_skill_example.py --role "Staff Software Engineer" --use-case
  "scoping and reviewing a bug fix for a cart total that is wrong when a
  discount code is applied"`, then filled it in by hand: a cart-total bug where
  a percentage discount and a flat discount stack incorrectly (the fourth
  report against the same code path, after three one-off patches for other
  code-pair combinations). The weak approach special-cases the exact reported
  code pair with no test; the expert approach writes a failing parametrized test
  first, root-causes the missing stacking contract and `float` rounding, then
  replaces the ad hoc branches with a typed `PercentDiscount`/`FlatDiscount`
  model over `Decimal`, and deletes the three superseded one-off patches in the
  same change.
- The expert approach's code and all five test-case numbers were independently
  executed (not just hand-checked) to confirm the arithmetic is actually
  correct, per this skill's own "never claim a command passed unless it
  actually ran" rule - all five passed.
- `python3 scripts/validate_skill_example.py examples/01-bug-fix-scoping-review.md`
  passes with no placeholder or structural findings.
- Added `examples/README.md` (one-row index table) and added both new files to
  `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`, per Open Question 4 of
  the initiative's task plan (don't require `examples/` until it is actually
  populated). Bundle now reports 26 files, up from 24.
- Re-ran `python3 scripts/validate_skill_bundle.py` (26 files OK) and
  `python3 -m unittest discover -s tests -v` (52 tests, unchanged from the
  tooling pass above - this pass added content, not new test code) after the
  change.

## Cross-repository consistency follow-up (2026-09-10)

A second "check and reorganize" pass across the whole collection (this skill plus
its four siblings) caught one thing the same-day Consistency audit above missed:
`SKILL.md`'s Caveats section referenced `[[deep-learning]]` and `[[hep-analysis]]`
using `[[wiki-link]]` double-bracket syntax - the linking convention this
repository's own memory files use, not skill markdown, and not the convention
used anywhere else in this file or its siblings (a plain backtick-quoted skill
name, e.g. `` `deep-learning` ``). It rendered as literal double brackets rather
than a link and was inconsistent with every other cross-skill mention in the
package. Fixed both to plain backticks. A repository-wide `grep -rn '\[\['`
confirmed this was the only such occurrence in this skill (two more were found
and fixed the same way in the sibling `deep-learning` and `hep-analysis`
packages). Bundle validator and full test suite re-run clean after the fix.

## Examples expansion to three canonical entries (2026-09-10)

Expanded `examples/` from the single Phase 2 pilot (`01-bug-fix-scoping-review.md`)
to three, per the next phase of the example-authoring initiative: one new-feature
scoping example and one production-incident-response example, chosen to be
genuinely different scenario types from the bug-fix pilot and from each other.

- Scaffolded `examples/02-new-feature-slicing-and-acceptance-criteria.md` with
  `generate_skill_example.py --role "Staff Software Engineer" --use-case
  "scoping a new \"let admins export a CSV of active users\" feature request"`
  (the exact feature prompt already listed in this skill's own README/SKILL.md
  "Example Prompts" section), then filled it in by hand: the weak approach
  skips acceptance criteria, bundles a dashboard page, a background job queue,
  and an email notifier into one unreviewable PR, and silently picks a
  definition of "active user" inside a query; the expert approach writes
  given/when/then acceptance criteria (vocabulary and pattern from
  `references/product-framing.md`'s Slicing section), states the "active
  user" definition as a visible assumption instead of guessing it, ships the
  smallest vertical slice (a synchronous, streamed CSV download), defers the
  job-queue/email/dashboard pieces as named follow-up tickets rather than
  scope creep, and adds a proportional test asserting the endpoint issues
  multiple bounded queries against a 5,000-row table instead of loading it all
  into memory at once.
- Scaffolded `examples/03-production-incident-response-postmortem.md` with
  `generate_skill_example.py --role "Staff Software Engineer / Incident
  Commander" --use-case "responding to and writing the postmortem for a
  production incident where a database migration run during a deploy caused a
  20-minute checkout outage"`, then filled it in by hand, following
  `references/engineering-playbook.md`'s Incident Response section: the weak
  approach root-causes during the live outage instead of stabilizing first,
  then writes a non-blameless postmortem that names the migration's author,
  has no real timeline, and ends in "be more careful next time" with no
  concrete action items; the expert approach rolls back first and separately
  identifies and kills the lock-holding migration process (a code rollback
  does not release an already-held table lock), then writes a blameless,
  timestamped postmortem that names the missing safeguards (no
  statement-timeout guard on migrations, no production-scale staging
  rehearsal, no locking-behavior item on the review checklist) rather than the
  person, and ends with four concrete, owned, dated action items.
- `python3 scripts/validate_skill_example.py
  examples/02-new-feature-slicing-and-acceptance-criteria.md` and the same
  command against `examples/03-production-incident-response-postmortem.md`
  each printed `<file>: ok` with zero structural or placeholder findings.
- Added both new file paths to `scripts/validate_skill_bundle.py`'s
  `REQUIRED_PATHS` and added one row per example to `examples/README.md`'s
  index table (same three-column format as the existing row).
- Checked `tests/test_agile_skill.py` and `tests/test_example_authoring.py`
  for the skill-router-style pattern of hand-building a scratch fixture
  directory from a hardcoded copy of `REQUIRED_PATHS`: no such coupling exists
  in this skill's test suite (both files test the scripts' functions and CLIs
  directly, with no fixture list mirroring `REQUIRED_PATHS`), so no test edits
  were needed for the two new example files.
- Re-ran `python3 scripts/validate_skill_bundle.py`, which reported
  "Bundle OK: 28 files present and non-empty." (up from 26), and
  `python3 -m unittest discover -s tests -v`, which reported "Ran 52 tests in
  0.429s" / "OK" - the same 52 tests as the prior pass, since this pass added
  example content, not new test code.

## Four-archetype example-authoring revision, tooling pass (2026-09-11)

Extended the example-authoring capability from a single archetype (Contrast)
to four - Contrast, `[A]` Execution Trajectory, `[B]` Gated Pipeline, and `[C]`
Decision-Tree - per a supplied revision to the original initiative. This pass
covers Phase 0 (design docs) and Phase 1 (tooling) only, scoped to
`agile-development` itself; no other skill folder or existing example file was
touched, and no new `examples/*.md` content was authored yet.

- Rewrote `references/example-authoring.md` to document all four generation
  prompts, the role/seniority escalation convention (senior -> senior ->
  principal -> lead), a short archetype-selection decision guide, and the full
  per-archetype format spec (required sections/order, frontmatter scenario
  field, and each archetype's extra structural rule). Updated `SKILL.md`'s
  "When to Load References" line, frontmatter `description`, and added one new
  "Example Prompts This Skill Handles Well" entry per archetype (reusing this
  skill's own already-named scenarios: the discount-code bug for Contrast,
  the same bug walked end-to-end for Trajectory, a feature-flagged rollout RFC
  for Gated Pipeline, and incident-page triage for Decision-Tree - matching
  Phase 2's scenario table in the source initiative). Updated `README.md`'s
  Quick checks (one invocation per archetype) and Coverage and boundaries
  sections to match.
- Rewrote `scripts/generate_skill_example.py` to be archetype-aware:
  `--archetype {contrast,trajectory,gated-pipeline,decision-tree}` selects one
  of four skeleton builders, each emitting that archetype's fixed section
  headers and an `archetype:` frontmatter field alongside the matching
  scenario flag (`--use-case` / `--problem-input` / `--high-stakes-task` /
  `--scenario`). The CLI rejects a scenario flag that doesn't match the chosen
  archetype, a missing one for the chosen archetype, and `--takeaways` used
  outside `--archetype contrast`.
- Rewrote `scripts/validate_skill_example.py` to read the `archetype:`
  frontmatter field and pick that archetype's rule set: Trajectory requires a
  fenced code block in both "3. Surgical Execution" and "4. Verification
  Evidence"; Gated Pipeline requires a non-empty `**Gate:**` line in all three
  phases plus assumption-language in Phase 3; Decision-Tree requires a Triage
  Matrix table with a Trigger/Resolution Strategy header and at least 3 data
  rows; Contrast keeps its existing 3-6 item Key Takeaways check. **A file
  with no `archetype:` frontmatter field is treated as `contrast`** - this was
  a deliberate design decision (not in the source initiative's literal spec,
  which lists `archetype:` as always-required) made to satisfy this phase's
  own acceptance check ("zero changes to any other skill folder yet"): all 15
  pre-existing example files across this repository's five skills predate the
  `archetype:` field, and requiring it unconditionally would have broken every
  one of them or forced touching four other skills' folders in what is
  supposed to be an `agile-development`-only phase. An explicit but unknown
  `archetype:` value (e.g. a typo) is still rejected, not defaulted.
- Rewrote `tests/test_example_authoring.py` with one good-example fixture per
  archetype (function-level `validate()` coverage plus CLI subprocess
  coverage), covering: valid-example-passes, the pre-revision legacy-fixture
  (no `archetype:` field) still passing, missing/out-of-order sections,
  archetype-specific structural failures (missing code fence, missing Gate
  line, Phase 3 without assumption language, missing/too-small Triage Matrix
  table), unknown `archetype:` value, CLI flag validation (wrong scenario flag
  for the archetype, missing scenario flag, `--takeaways` rejected outside
  Contrast), and the existing placeholder/regression-gate tests carried
  forward unchanged. 73 tests total, up from 52 (21 new; none of the 52
  pre-existing tests were deleted, though several were adapted to pass
  `archetype=` and the now-required `None` defaults for the other three
  scenario fields through `_scaffold_args`).
- Verified all 15 pre-existing example files (3 per skill across
  `agile-development`, `deep-learning`, `hep-analysis`, `academic-papers`,
  `skill-router`) still pass `validate_skill_example.py` unchanged, confirming
  the backward-compatibility decision above actually holds in practice, not
  just in the test fixtures.
- No `REQUIRED_PATHS` change was needed in `scripts/validate_skill_bundle.py`:
  this phase modified existing required files only and added no new ones.
  `python3 scripts/validate_skill_bundle.py` reports "Bundle OK: 28 files
  present and non-empty." (unchanged from the prior pass), and
  `python3 -m unittest discover -s tests -v` reports "Ran 73 tests" / "OK".

One defect was found and fixed during scaffolding: a first draft of the
Decision-Tree test for "too few matrix rows" removed only one row from the
4-row good fixture, leaving 3 - still at the documented minimum, so the
expected failure never fired. Fixed by removing two rows to actually cross
the threshold; caught by running the suite, not by inspection.

Explicitly out of scope for this pass, per the source initiative's own
phasing (Phase 2 dogfooding within `agile-development` and Phase 3 rollout to
the other four skills each require authored domain content and are tracked as
separate follow-up passes): no new `examples/*.md` file was scaffolded or
filled in for any of the three new archetypes, `examples/README.md`'s index
was not changed, and no other skill's `SKILL.md`/`README.md`/`VALIDATION.md`
was touched.

## Four-archetype revision, Phase 2 dogfood pilots (2026-09-11)

Added the three new archetypes' first `agile-development`-own examples, per
Phase 2 of the four-archetype revision - scenarios reused from this skill's
own already-named material rather than invented, so the pilot set also
validates that the archetypes fit the scenarios they were assigned:

- `examples/04-trajectory-discount-stacking-bug.md` (Execution Trajectory):
  the same discount-stacking bug family as `01-bug-fix-scoping-review.md`,
  walked as a single start-to-finish trajectory rather than a weak/expert
  contrast. Root cause: `apply_discounts` recomputed each discount from the
  original `total` instead of the running result, so only the last code in
  the loop took effect; fix compounds onto the running result in a canonical
  percent-then-flat order and deletes three superseded one-off patches. The
  arithmetic (`50.00 -> 40.00` for a 10%-then-$5 stack, order-independent) was
  independently executed in Python, not just hand-checked, before writing it
  into the example.
- `examples/05-gated-pipeline-payment-provider-rollout-rfc.md` (Gated
  Pipeline): drafting an RFC for a feature-flagged payment-provider rollout.
  Phase 2's "specific regulatory/evaluation criteria" requirement is met by
  citing this skill's own `references/design-and-estimation.md` by exact
  section name ("What a lightweight design doc should contain", "Feature
  flags and progressive rollout as risk-reduction tools") rather than a vague
  "best practices" - both section names were confirmed against the actual
  file's headings before writing the citation. Phase 3's red-team pass finds
  a false idempotency assumption in the draft and adds a required fix before
  the final merge gate.
- `examples/06-decision-tree-incident-mitigation-triage.md` (Decision-Tree):
  formalizes `references/engineering-playbook.md`'s Incident Response step 2
  (mitigate before fully understanding: rollback / flag-disable / traffic
  shift / kill switch, with an explicit exception when the mitigation itself
  is risky) into a 5-row Triage Matrix - the section's actual content was
  read first and the matrix's rows and their order were checked against it
  rather than invented independently.
- All three pass `python3 scripts/validate_skill_example.py <file>` with no
  structural or placeholder findings. One typo (a stray `°` character from a
  find-and-replace slip in the Gated Pipeline draft's "100%" rollout stage)
  was caught by re-reading the file and fixed before validation, not by the
  validator itself - a reminder that the validator checks structure and
  placeholders, not prose correctness.
- Added one row per new example to `examples/README.md`'s index (now four
  columns: `Example | Archetype | Scenario | One-line takeaway`, generalized
  from the three-column Contrast-only table) and added all three new files to
  `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`.
- Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 31 files
  present and non-empty.", up from 28) and
  `python3 -m unittest discover -s tests -v` ("Ran 73 tests" / "OK", unchanged
  from the tooling pass - this pass added example content, not new test code).

## Expand each new archetype to three examples (2026-09-11)

Brought Execution Trajectory, Gated Pipeline, and Decision-Tree up to three
examples each (matching Contrast's existing count), per an explicit request
that the additional examples within an archetype have genuinely different
content - different scenario and different reference material grounding each
one, not a variation on the same theme as the Phase 2 pilot or on each other.

- **Execution Trajectory** (`07`, `08`, alongside the existing `04`):
  - `07-trajectory-database-migration-lock.md`: a single-statement `ADD
    COLUMN ... NOT NULL` migration holds an `ACCESS EXCLUSIVE` lock
    proportional to table size because NOT NULL validation runs under the
    same lock as the metadata change, walked through a three-step nullable-
    add / batched-backfill / `NOT VALID` + `VALIDATE CONSTRAINT` fix. Grounds
    the fix in `references/risk-and-quality.md`'s "Data and Persistence"
    section ("prefer backward-compatible schema migrations that support
    rolling deployment") and `references/engineering-playbook.md`'s Database
    Migration playbook - neither used by any existing example in this skill.
  - `08-trajectory-dependency-update-silent-break.md`: a "minor" dependency
    version bump silently changes a rounding default (round-half-up to
    round-half-to-even), causing a $0.01-per-invoice discrepancy caught only
    by finance reconciliation weeks later, because no existing test fixture
    used an exact rounding-boundary value. Grounds the triage in
    `references/engineering-playbook.md`'s Dependency Update playbook. The
    rounding arithmetic (`12.345` -> `12.35` half-up vs. `12.34` half-even)
    was independently verified with Python's `decimal` module before being
    written into the example, not just asserted.
- **Gated Pipeline** (`09`, `10`, alongside the existing `05`):
  - `09-gated-pipeline-legacy-billing-strangler-fig.md`: replacing a legacy,
    untested billing module while it stays load-bearing. Grounds Phase 1/2 in
    `references/engineering-playbook.md`'s "Legacy Code Without Tests"
    playbook (characterize first, find a seam, strangler-fig rollout) and a
    dependency-direction decision in `references/software-architecture.md`'s
    "Boundaries and dependencies" section. Phase 3's red-team pass finds a
    false per-request independence assumption (old/new implementations round
    proration differently, so splitting one customer's invoices mid-cycle
    between them doesn't reconcile) and fixes the routing granularity.
  - `10-gated-pipeline-public-api-contract-change.md`: adding a required
    field to a shared public API contract without breaking six existing
    external integrations. Grounds Phase 1/2 in
    `references/risk-and-quality.md`'s "API and Interface Changes" section
    and an ADR per `references/software-architecture.md`'s "Recording the
    decision" section (named there as exactly this kind of consequential,
    hard-to-reverse case). Phase 3 finds one partner's strict response-schema
    parsing would break even on an "optional" field - a different failure
    mode from example `09`'s red-team finding, not a repeat of it.
- **Decision-Tree** (`11`, `12`, alongside the existing `06`):
  - `11-decision-tree-pr-review-response-triage.md`: formalizes
    `references/risk-and-quality.md`'s "Reviewing Someone Else's Change"
    section into a 5-row finding-to-response matrix; selects "verify the
    claim directly" for a PR whose description claims a passing suite while
    its own linked CI run shows a failing test covering the exact changed
    behavior.
  - `12-decision-tree-staging-vs-production-parity-triage.md`: formalizes
    `references/risk-and-quality.md`'s "Configuration and Environments" and
    "Observability" sections into a config/flag/scale/infrastructure/data
    elimination-order matrix; selects the missing-production-secret branch
    for a silently-failing scheduled email and fixes both the missing secret
    and the silent-failure (`os.environ.get` swallowing a missing required
    key) that hid it.
- All six new files pass `python3 scripts/validate_skill_example.py <file>`
  with no structural or placeholder findings.
- Added one row per new file to `examples/README.md`'s index and all six new
  paths to `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`.
- Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 37 files
  present and non-empty.", up from 31) and
  `python3 -m unittest discover -s tests -v` ("Ran 73 tests" / "OK", unchanged
  - this pass added example content, not new test code).

This pass is scoped to `agile-development` only, per the request; the other
four skills (`deep-learning`, `hep-analysis`, `academic-papers`,
`skill-router`) each still have exactly one pilot for their rolled-out
archetype and are not touched here.

## Consistency audit (2026-09-11)

A second "check and reorganize" pass with no new content: re-read `SKILL.md`
and `README.md` against the actual `references/` directory, diffed
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` against every real file
on disk, checked all relative Markdown links across the package for broken
targets and the link-text/target mismatch pattern found in the 2026-09-10
audit, re-ran every README-documented CLI command as written, and validated
all 12 shipped `examples/*.md` files.

- Found and fixed one real gap: `references/software-architecture.md` (added
  during the four-archetype example-authoring work, used by examples `09` and
  `10`, and already linked from `SKILL.md`'s "When to Load References") was
  never added to `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`, so the
  bundle validator was silently not checking that file's presence, and it was
  never mentioned in `README.md`'s "Coverage and boundaries" paragraph, so the
  package's own coverage summary was incomplete. Added the path (alphabetical
  slot between `risk-and-quality.md` and `validation-and-done.md`, matching
  the list's existing order) and one clause to the README paragraph
  (architectural-decision recognition, boundaries/dependency direction, data
  ownership, ADRs), in the same style as the paragraph's other reference
  summaries.
- No other inconsistencies found: every relative Markdown link resolves and
  none show the link-text/target mismatch fixed on 2026-09-10; every
  `references/*.md` file is linked from `SKILL.md`; `examples/README.md`'s
  12-row index matches the 12 files actually in `examples/`; every
  README-documented quick-check command (`create_story_card.py`,
  `validate_agile_notes.py`, all four `generate_skill_example.py`
  archetypes) was re-run and matched its documented behavior; no leftover
  placeholder markers outside the documented zero-placeholder rule text
  itself; `agents/openai.yaml` still consistent with `SKILL.md`.
- Bundle validator now reports "Bundle OK: 38 files present and non-empty."
  (up from 37 - the previously-untracked file, not new content). Full test
  suite (73 tests) and all 12 `validate_skill_example.py` runs re-confirmed
  clean after the fix.

## Second-wave example-authoring tooling pass (2026-09-12)

Extended the example-authoring capability with four new archetypes -
Interactive Elicitation ("Grill-Me"), Adversarial Audit / Red-Teaming,
Test-First / Red-to-Green, and Incident Postmortem & RCA - alongside the
existing Contrast/Trajectory/Gated Pipeline/Decision-Tree set, plus a new
cross-skill diversity rule and checker. This pass covers the tooling only
(Phase 0/1); the 12 planned examples across 5 skills land in a later pass.

- `references/example-authoring.md`: added the four archetypes' generation
  prompts, format specs, and section rules; added the "Actor-stance
  convention (second wave)" table (Elicitation: principal; Adversarial
  Audit: ruthless; Test-First: test-driven; Postmortem: Site
  Reliability/Principal); added the "Diversity rule" to the shared-conventions
  list; added a caveat under "Correctness review" noting the 5-Whys
  root-cause check and the diversity checker are both mechanical floors, not
  substitutes for domain/curation review; extended "Which archetype fits?"
  with all four new triggers.
- `SKILL.md`: extended the "Authoring a canonical worked example" reference
  line to name all eight archetypes, added one example prompt per new
  archetype, and re-worded the frontmatter `description` to name all eight
  archetypes while trimming two other clauses ("lightweight" ->  dropped,
  "even without saying" -> "without saying") to stay within the 1024-char
  frontmatter budget (984 -> 1015 chars).
- `scripts/generate_skill_example.py`: added `elicitation`,
  `adversarial-audit`, `test-first`, and `postmortem` to `ARCHETYPES` and
  `SCENARIO_FIELD`, added a `_build_*` skeleton function and CLI flag
  (`--user-request`/`--candidate-artifact`/`--target`/`--incident`) for each -
  the existing mutual-exclusion and required-scenario-flag validation in
  `parse_args` is generic over `SCENARIO_FIELD` and needed no changes.
- `scripts/validate_skill_example.py`: added the same four archetypes to
  `ARCHETYPES`/`SCENARIO_FIELD`/`REQUIRED_SECTIONS`, plus one check function
  each: `check_elicitation` (exactly 3-4 numbered questions, each with
  lettered options), `check_adversarial_audit` (>=2 distinctly-numbered
  "Attack Vector" labels, fenced artifacts in sections 3 and 4),
  `check_test_first` (a raw failure marker in section 2's fenced block, a
  numeric metric in section 4's), and `check_postmortem` (a fenced
  alert/log payload in section 1, exactly 5 numbered Why-steps with no
  "human error" stop in section 3, a fenced diff in section 4, a
  metric+action monitoring rule in section 5).
- `scripts/check_example_diversity.py` (new): groups a set of example files
  by `archetype:`/`skill:` frontmatter and reports any archetype group where
  two files share a skill. Reuses `validate_skill_example.parse_frontmatter`
  rather than re-implementing frontmatter parsing.
- `scripts/validate_skill_bundle.py`: added `scripts/check_example_diversity.py`
  to `REQUIRED_PATHS`.
- `README.md`: added the five new-archetype/diversity-checker commands to
  "Quick checks" (all re-run as documented, including a deliberate check that
  `check_example_diversity.py` correctly flags the 12 existing
  same-skill examples as violations for their own archetypes - expected,
  since the diversity rule is scoped to the new second-wave archetypes, not
  retroactive); extended the "Coverage and boundaries" archetype list to all
  eight.
- `tests/test_example_authoring.py`: added one scaffold test and one
  `Validate*Tests` class per new archetype (18 new tests: valid-passes,
  1-2 targeted violation cases, and scaffold-fails-until-filled, mirroring
  the existing four archetypes' test shape), plus a `DiversityCheckerTests`
  class (4 tests: no-violation across skills, violation on repeated skill,
  and both as CLI invocations). Full suite: 98 tests, all passing
  (`python3 -m unittest discover -s tests -v`).
- `scripts/validate_skill_bundle.py` reports "Bundle OK: 40 files present and
  non-empty." (up from 38 - one new script).

## Expand all four second-wave archetypes to three examples per skill (2026-09-12)

Superseded the second-wave batch's original "3 examples total per archetype,
one per skill, no skill repeated" shape with "3 examples per archetype, per
skill" - matching how Contrast/Trajectory/Gated-Pipeline/Decision-Tree have
always worked. Every skill (`academic-papers`, `agile-development`,
`deep-learning`, `hep-analysis`, `skill-router`) now carries all eight
archetypes x 3 examples = 24 example files; 48 new files were authored across
the 5 skills to close the gap (agile-development's own share: 10 new files,
examples 15-24).

- `references/example-authoring.md`: rewrote the "Diversity rule" bullet -
  it now states the requirement as intra-skill content distinctness (3
  genuinely different scenarios per `<skill>/archetype` pair, hand-curated,
  not mechanically checked) rather than cross-skill non-repetition. Marked
  `scripts/check_example_diversity.py` as historical: it enforced the
  original narrower "one example per skill, no repeats" batch and is not run
  as a gate on new example batches. Updated the "Correctness review" section's
  parallel note the same way.
- `README.md`: removed `check_example_diversity.py` from "Quick checks" and
  from the Coverage-and-boundaries cross-reference; updated the
  `validate_skill_example.py`/`generate_skill_example.py` description
  paragraph to drop the retired diversity-checker mention.
- `scripts/validate_skill_bundle.py`: added `examples/15-*.md` through
  `examples/24-*.md` (the 10 new agile-development example files) to
  `REQUIRED_PATHS`. `check_example_diversity.py` itself is left in place
  (and still in `REQUIRED_PATHS`) as working, documented-as-historical
  tooling - not deleted, since it remains correct for the narrower
  constraint it was built to check, just no longer the constraint this
  repository enforces going forward.
- `examples/README.md`: added 10 rows (15-24) covering the new
  elicitation/adversarial-audit/test-first/postmortem examples in this
  skill's own domain (database migration and caching elicitation; a hotfix
  PR, a backward-compatibility claim, and an acceptance-criteria claim for
  adversarial audit; the story-card generator, risk-register entry, and
  Definition-of-Done checklist for test-first; a feature-flag gap and a
  migration table-lock for postmortem).
- `root README.md` and `academic-papers/README.md`: updated stale counts and
  cross-skill-diversity wording repo-wide to match the new per-skill shape
  (academic-papers' file-tree comment: 14 -> 24 examples).
- Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 52 files
  present and non-empty") and `python3 -m unittest discover -s tests -v`
  (98 tests, all passing, unchanged - no test asserted the old cross-skill
  diversity constraint as a gate) after the change. All 10 new example files
  individually pass `scripts/validate_skill_example.py`.

## Renumber examples into canonical per-archetype order (2026-09-12)

The `examples/` numbering had drifted into an inconsistent, historically-
accreted order (the same archetype landing at different numbers in different
skills, and some archetypes' 3 examples not even contiguous within one skill -
e.g. this skill's own Postmortem trio was split across two ranges). Renamed
files (content unchanged) so every skill now uses the same canonical layout:
`01-03` Contrast, `04-06` Trajectory, `07-09` Gated-Pipeline, `10-12`
Decision-Tree, `13-15` Elicitation, `16-18` Adversarial-Audit, `19-21`
Test-First, `22-24` Postmortem - identical across all 5 skills. Updated
`examples/README.md`'s table (re-sorted into the new order) and, where
present, `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`; left every
prior dated entry in this file untouched, so filenames named in earlier
entries above refer to a file's *former* name - use the mapping below to
resolve them to the current filename.

Old name -> new name (this skill only):

- `07-trajectory-database-migration-lock.md` -> `05-trajectory-database-migration-lock.md`
- `08-trajectory-dependency-update-silent-break.md` -> `06-trajectory-dependency-update-silent-break.md`
- `05-gated-pipeline-payment-provider-rollout-rfc.md` -> `07-gated-pipeline-payment-provider-rollout-rfc.md`
- `09-gated-pipeline-legacy-billing-strangler-fig.md` -> `08-gated-pipeline-legacy-billing-strangler-fig.md`
- `10-gated-pipeline-public-api-contract-change.md` -> `09-gated-pipeline-public-api-contract-change.md`
- `06-decision-tree-incident-mitigation-triage.md` -> `10-decision-tree-incident-mitigation-triage.md`
- `15-elicitation-database-migration-ambiguous-request.md` -> `14-elicitation-database-migration-ambiguous-request.md`
- `16-elicitation-add-caching-ambiguous-request.md` -> `15-elicitation-add-caching-ambiguous-request.md`
- `17-adversarial-audit-hotfix-pr-description.md` -> `16-adversarial-audit-hotfix-pr-description.md`
- `18-adversarial-audit-backward-compatible-design-doc.md` -> `17-adversarial-audit-backward-compatible-design-doc.md`
- `19-adversarial-audit-acceptance-criteria-completeness.md` -> `18-adversarial-audit-acceptance-criteria-completeness.md`
- `20-test-first-story-card-generator-invariant.md` -> `19-test-first-story-card-generator-invariant.md`
- `21-test-first-risk-register-entry-invariant.md` -> `20-test-first-risk-register-entry-invariant.md`
- `22-test-first-definition-of-done-invariant.md` -> `21-test-first-definition-of-done-invariant.md`
- `14-postmortem-production-api-outage-bad-deploy.md` -> `22-postmortem-production-api-outage-bad-deploy.md`

Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 52 files present and non-empty") and `python3 -m unittest discover -s tests -v` (98 tests, all passing) after the rename. All 24 example files individually re-validated with `scripts/validate_skill_example.py` ("ok").

## Limitations

- No real project repository, CI system, or code-review tooling was available to
  exercise the workflow guidance in `SKILL.md`/`references/*.md` end to end - those
  are process guidance for an LLM to follow, not independently executable, and are
  reviewed for internal consistency (cross-links, terminology) rather than run.
- `references/cpp-balanced-design-guidelines.md` is shared verbatim with
  `deep-learning`'s copy of the same file; consistency between the two copies was
  checked (byte-identical) but the guidance itself was not re-validated here.
