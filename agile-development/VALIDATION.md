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

## Limitations

- No real project repository, CI system, or code-review tooling was available to
  exercise the workflow guidance in `SKILL.md`/`references/*.md` end to end - those
  are process guidance for an LLM to follow, not independently executable, and are
  reviewed for internal consistency (cross-links, terminology) rather than run.
- `references/cpp-balanced-design-guidelines.md` is shared verbatim with
  `deep-learning`'s copy of the same file; consistency between the two copies was
  checked (byte-identical) but the guidance itself was not re-validated here.
