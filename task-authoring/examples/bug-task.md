# Fix `academic-papers`' Bundle Validator Silently Skipping `examples/` Paths

## Background

`academic-papers/scripts/validate_skill_bundle.py` scans `SKILL.md` for
backtick-quoted relative paths so it can (a) confirm each referenced file
exists on disk, and (b) flag files in the bundle that `SKILL.md` never
mentions. The regex it uses to find those paths is:

```python
BACKTICK_PATH_RE = re.compile(r"`((?:references|scripts|assets)/[^`\s]+)`")
```

This only matches paths under `references/`, `scripts/`, or `assets/`. The
bundle also ships an `examples/` directory (25 files), and `SKILL.md` points
at it, but nothing in `SKILL.md`, the validator's docstring, or `README.md`
says that `examples/` paths are deliberately left unchecked. It's a side
effect of the regex's fixed prefix list. If `SKILL.md` gained a backtick
reference to a missing or misspelled file such as `examples/no-such-file.md`,
the validator would still report success, even though the same typo under
`references/` fails. The orphaned-file check has the same gap, because it
walks only `references/`, `scripts/`, and `assets/`.

## Objective

`academic-papers/scripts/validate_skill_bundle.py` either (a) checks
backtick-quoted `examples/` paths in `SKILL.md` the same way it checks
`references/` paths, or (b) documents `examples/` as deliberately out of
scope in its docstring and `README.md`. The right choice depends on what the
maintainer intends (see Open Questions).

## Scope

### In Scope

- Decide (with the maintainer) whether `examples/` belongs to the set of
  directories the validator checks, or should stay excluded on purpose.
- Update `BACKTICK_PATH_RE` and the directory tuple in
  `check_no_orphaned_files()` to match that decision, or document the
  exclusion.
- Add a regression test covering the case that currently passes silently.

### Out of Scope

- Moving, renaming, or renumbering any of the existing examples.
- Checking example *content*, such as archetype rules. `task-authoring`'s
  `validate_skill_example.py` already does that.
- The other directories the validator also ignores (`agents/`, `tests/`),
  unless the maintainer asks for them together.

## Repository Context

Verified by direct inspection on 2026-09-23:

- `academic-papers/scripts/validate_skill_bundle.py` defines
  `BACKTICK_PATH_RE` as shown above. `check_referenced_paths_exist()`
  applies that regex, and `check_no_orphaned_files()` iterates over the
  hard-coded tuple `("references", "scripts", "assets")`.
- `academic-papers/examples/` exists and holds 25 files. `SKILL.md` mentions
  it only as the bare directory `` `examples/` ``, so no file-level
  reference exists yet. The bug is latent, not currently visible in the
  shipped bundle.
- A scratch copy of the bundle, with backtick references to both
  `examples/no-such-file.md` and `references/no-such-file.md` appended to
  `SKILL.md`, reported only the `references/` path as missing. The
  `examples/` path passed silently.
- `academic-papers/tests/test_skill_bundle.py`'s `TestSyntheticBundles`
  class builds synthetic bundles in a temporary directory. None of its cases
  uses an `examples/` path.

## Technical Approach

1. Confirm with the maintainer whether `examples/` files should be required
   to be referenced from `SKILL.md`. Checking that referenced paths exist is
   cheap. Requiring every file to be referenced (the orphan check) would fail
   today, because `SKILL.md` points only at the directory.
2. If `examples/` should be checked: add `examples` to the regex prefix list
   so referenced paths must exist. Also add it to the orphan-check tuple
   only if the maintainer wants that stricter rule. The existing
   `any(rel.startswith(r.rstrip("/") + "/") ...)` clause already treats a
   bare `examples/` reference as covering every file under it, but the
   regex's `[^`\s]+` part requires at least one character after the slash,
   so re-check that a bare directory reference is still matched.
3. If `examples/` should stay excluded: list that choice in the module
   docstring's "Checks" section and in `README.md`, so the gap is documented
   instead of accidental.
4. Add a test to `TestSyntheticBundles` that writes a synthetic `SKILL.md`
   referencing a missing `examples/` file and asserts the chosen behavior.

## Deliverables

- Updated `academic-papers/scripts/validate_skill_bundle.py`.
- A new regression test in `academic-papers/tests/test_skill_bundle.py`.
- A short note in `academic-papers/VALIDATION.md` describing the fix and
  which resolution was chosen (checked or documented as excluded).

## Acceptance Criteria

- A synthetic `SKILL.md` that references a missing `examples/` file no
  longer passes silently. The validator either reports the missing path, or
  the exclusion is documented and a test asserts it.
- Every `references/`, `scripts/`, and `assets/` path the validator checks
  today is still checked exactly as before.
- `python3 scripts/validate_skill_bundle.py` still exits `0` on the current,
  unmodified `academic-papers` bundle.
- `python3 -m unittest discover -s tests -v` passes, including the new
  regression test.

## Validation

- Run `python3 -m unittest discover -s tests -v` from `academic-papers/` and
  confirm the new test and all existing tests pass.
- Run `python3 scripts/validate_skill_bundle.py` from `academic-papers/` and
  confirm it still reports "passed all checks" on the real bundle.
- Repeat the scratch-copy experiment from Repository Context and confirm the
  `examples/no-such-file.md` reference now behaves as chosen.

## Open Questions

- Should the validator check `examples/` paths (option a), or should
  `examples/` stay deliberately unchecked and be documented as such
  (option b)? **Requires Confirmation.** The gap was found during
  inspection, and no one has said which behavior is intended.
- If `examples/` is checked, should the orphan check also require every
  example to be referenced from `SKILL.md`, or is the bare `examples/`
  directory reference enough? **TBD.**
- Is this worth fixing now, while `SKILL.md` has no file-level `examples/`
  references, or should it wait until one is added? **TBD.**

## References

- `agentic-ai-skills/academic-papers/scripts/validate_skill_bundle.py`: the
  file containing the regex and the orphan-check directory tuple.
- `agentic-ai-skills/academic-papers/tests/test_skill_bundle.py`: the
  existing synthetic-bundle test class to extend.
- `agentic-ai-skills/academic-papers/SKILL.md`: the document the regex
  scans.
