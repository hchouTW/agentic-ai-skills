# Add a `--format json` Output Mode to Each Skill's `validate_skill_bundle.py`

## Background

Every skill in `agentic-ai-skills` (`skill-router`, `agile-development`,
`deep-learning`, `hep-analysis`, `academic-papers`) ships its own
`scripts/validate_skill_bundle.py`, and each currently prints a human-
readable summary (`"Bundle OK: N files present and non-empty."` on success,
`"missing files:"` / `"empty files:"` lists on failure) to stdout, with the
process exit code as the only machine-checkable signal. A maintainer who
wants to aggregate validation results across all five skills - for example
in a future CI job or a repo-wide status dashboard - currently has to parse
that free-text output, which is fragile against any wording change.

## Objective

Each skill's `validate_skill_bundle.py` accepts an optional `--format json`
flag that prints a single machine-readable JSON object describing the
validation result, while the default (no flag) invocation keeps its existing
human-readable output unchanged.

## Scope

### In Scope

- Add `--format {text,json}` (default `text`) to each of the five skills'
  `scripts/validate_skill_bundle.py`.
- Define one JSON shape used identically across all five scripts.
- Update each skill's `README.md` Quick checks section with the new flag.
- Add or extend each skill's test suite to cover the new flag.

### Out of Scope

- Wiring this into any CI system - no CI configuration exists in this
  repository today (confirmed: no `.github/` directory and no CI-related
  YAML file anywhere in the tree).
- Building a cross-skill aggregator script that calls all five validators
  and merges their JSON - not requested, and not needed for this task to be
  useful on its own.
- Changing the default (`text`) output format or any existing exit code
  semantics.

## Repository Context

Verified by direct inspection on 2026-09-12:

- `agile-development/scripts/validate_skill_bundle.py` and
  `skill-router/scripts/validate_skill_bundle.py` were read in full. Both
  follow the same structure: a `REQUIRED_PATHS` list, a
  `REQUIRED_README_SECTIONS` list, a `main()` that checks missing/empty
  files, then `SKILL.md` frontmatter, then `README.md` sections, printing
  human-readable text and calling `raise SystemExit(1)` on any failure or
  printing a one-line `"Bundle OK: ..."` message and returning normally on
  success.
- `deep-learning/scripts/validate_skill_bundle.py`,
  `hep-analysis/scripts/validate_skill_bundle.py`, and
  `academic-papers/scripts/validate_skill_bundle.py` were confirmed to exist
  (not read in full for this task) - each skill has its own copy, there is
  no shared/imported validator module across skills.
- Each skill has its own `tests/` directory
  (`agile-development/tests/test_agile_skill.py`,
  `skill-router/tests/test_skill_router.py`, and similar in the other three)
  run independently via `python3 -m unittest discover -s tests -v` from
  inside that skill's folder.

## Technical Approach

1. Read each of the five `validate_skill_bundle.py` scripts in full to
   confirm the current failure/success branches before changing any of
   them (`skill-router`'s script additionally reports routing-table/sibling
   information that the JSON shape needs to account for).
2. Define one shared JSON shape, e.g.
   `{"ok": bool, "missing": [...], "empty": [...], "issues": [...]}`,
   used identically by all five scripts so a future aggregator can rely on
   it.
3. Add `argparse` (or equivalent) handling for `--format {text,json}` to
   each script, defaulting to `text`, preserving the exact current text
   output and exit codes for that default path.
4. For `--format json`, emit the JSON object to stdout instead of the
   human-readable lines, still using exit code 0/1 the same way.
5. Update each skill's test suite with at least one test asserting the JSON
   output parses and reports `"ok": true` on the shipped bundle, and one
   asserting it reports the expected missing/empty entries against a
   doctored scratch copy (mirroring the existing scratch-copy pattern
   already used in, e.g., `skill-router/tests/test_skill_router.py`).
6. Update each skill's `README.md` Quick checks section with one example
   `--format json` invocation.

## Deliverables

- Updated `scripts/validate_skill_bundle.py` in all five skills.
- Updated `README.md` Quick checks section in all five skills.
- New or extended tests in all five skills' `tests/` directories.
- A one-paragraph note in each touched skill's `VALIDATION.md` describing
  what was added and what was run.

## Acceptance Criteria

- Running `python3 scripts/validate_skill_bundle.py` with no arguments in
  any of the five skills produces byte-identical output to before this
  change on the currently-shipped (passing) bundle.
- Running `python3 scripts/validate_skill_bundle.py --format json` in any of
  the five skills prints a single JSON object to stdout that parses with
  the standard library `json` module and includes an `"ok"` boolean.
- The JSON shape is identical across all five skills' scripts (same key
  names, same types).
- `python3 -m unittest discover -s tests -v` passes in all five skills
  after the change.
- Any skill's validator that fails (a doctored missing/empty file in a test
  fixture) reports the failure in the JSON object rather than only via a
  non-zero exit code.

## Validation

- Run `python3 scripts/validate_skill_bundle.py` and
  `python3 scripts/validate_skill_bundle.py --format json` in each of the
  five skill folders and inspect both outputs.
- Run `python3 -m unittest discover -s tests -v` in each of the five skill
  folders.
- Manually diff the default-mode output before and after the change to
  confirm it is unchanged.

## Open Questions

- Should the shared JSON shape be factored into one importable module (e.g.
  a repo-root `scripts/` helper) rather than duplicated five times, given
  that today each skill's validator is fully standalone with no shared
  imports? **Requires Confirmation** - this task, as scoped, keeps the
  five scripts independent to match the existing convention, but a shared
  module would reduce duplication if a sixth skill is added later.
- Is there a concrete near-term consumer of this JSON output (a CI job, a
  dashboard), or is this speculative tooling ahead of an actual need?
  **TBD** - no such consumer was found in this repository during
  inspection, and none was named by the requester.

## References

- `agentic-ai-skills/agile-development/scripts/validate_skill_bundle.py` -
  the validator implementation this task extends.
- `agentic-ai-skills/skill-router/scripts/validate_skill_bundle.py` and
  `agentic-ai-skills/skill-router/tests/test_skill_router.py` - the
  scratch-copy test pattern to extend for the JSON-mode tests.
- `agentic-ai-skills/README.md` - "Verifying a skill bundle" section,
  documenting the existing `python3 scripts/validate_skill_bundle.py`
  convention this task must not break.
