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

## Limitations

- No real project repository, CI system, or code-review tooling was available to
  exercise the workflow guidance in `SKILL.md`/`references/*.md` end to end - those
  are process guidance for an LLM to follow, not independently executable, and are
  reviewed for internal consistency (cross-links, terminology) rather than run.
- `references/cpp-balanced-design-guidelines.md` is shared verbatim with
  `deep-learning`'s copy of the same file; consistency between the two copies was
  checked (byte-identical) but the guidance itself was not re-validated here.
