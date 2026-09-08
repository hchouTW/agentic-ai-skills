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

## Limitations

- No real project repository, CI system, or code-review tooling was available to
  exercise the workflow guidance in `SKILL.md`/`references/*.md` end to end - those
  are process guidance for an LLM to follow, not independently executable, and are
  reviewed for internal consistency (cross-links, terminology) rather than run.
- `references/cpp-balanced-design-guidelines.md` is shared verbatim with
  `deep-learning`'s copy of the same file; consistency between the two copies was
  checked (byte-identical) but the guidance itself was not re-validated here.
