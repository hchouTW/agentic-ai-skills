# Validation

What `scripts/validate_skill_bundle.py` and the test suite check for this skill
bundle, and what `scripts/check_manuscript.py` / `scripts/build_lit_matrix.py` check
for a user's own manuscript or reading notes (a different, deliberately separate
concern).

## `validate_skill_bundle.py` — checks on this skill bundle

1. **`SKILL.md` exists** and starts with a `---`-delimited YAML frontmatter block.
2. **`name` and `description` are present and non-empty** in that frontmatter, and
   `description` is long enough to plausibly describe triggering conditions (a cheap
   proxy for "did someone forget to fill this in").
3. **`name` matches the containing folder's name** (`academic-papers`), catching
   copy/rename mistakes.
4. **Every backtick-quoted path under `references/`, `scripts/`, or `assets/`
   mentioned in `SKILL.md` actually exists on disk** — catches references to files
   that were renamed or deleted without updating `SKILL.md`.
5. **Every file under `references/`, `scripts/`, and `assets/` is mentioned somewhere
   in `SKILL.md`** (except the validator script itself, `__pycache__`/`.pyc`
   artifacts, and the test suite) — catches orphaned files nobody points to, which
   would never get loaded by an agent using the skill.
6. **Every `.py` file under `scripts/` parses as valid Python** (a syntax check via
   `ast.parse`; nothing is executed).

Run:
```bash
python3 scripts/validate_skill_bundle.py
```
Exit code `0` on success, `1` if any check fails, with a list of the specific issues
found.

## Test suite (`tests/`)

`tests/test_skill_bundle.py`:
- Confirms the **actual shipped bundle** passes `validate_skill_bundle.py` with zero
  errors (a regression guard — this is the test most likely to catch an accidental
  break when the skill is later edited, e.g. after this reading-skill integration).
- Exercises the validator against small synthetic bundles built in a temp directory,
  covering: missing `SKILL.md`, missing frontmatter, name mismatch, a valid minimal
  bundle, an orphaned reference file, and a `.py` file with a syntax error.

`tests/test_check_manuscript.py`:
- Exercises `check_manuscript.py`'s `scan()` and `report()` functions against small
  synthetic `.tex`/`.bib` fixtures in a temp directory, covering: a fully clean
  manuscript, a missing bib entry, an unused bib entry, a duplicate label, an
  undefined `\ref`, `TODO`/`[VALUE NEEDED]` markers, placeholder text (`???`,
  `[FIGURE HERE]`), and the exit codes returned in both the clean and issue-found
  cases.

`tests/test_build_lit_matrix.py`:
- Exercises `build_lit_matrix.py`'s CSV reading, numeric/text sorting (ascending and
  descending), markdown-cell escaping (pipes, newlines), full table formatting, and
  the CLI entry point's success/error exit codes (missing file, unknown `--sort-by`
  column).

Run all three:
```bash
python3 -m unittest discover -s tests -v
```

## `check_manuscript.py` and `build_lit_matrix.py` — checks/tools on the *user's* own files

Neither is part of the skill's own integrity checking — they are tools the skill
offers to the user, run against their own `.tex`/`.bib` manuscript files or their own
CSV of reading notes. See each script's module docstring and `SKILL.md`'s "Bundled
scripts" section for what they do. Both are read-only with respect to their input:
`check_manuscript.py` never modifies the user's manuscript, and `build_lit_matrix.py`
only ever writes the single markdown file it's asked to produce (or prints to
stdout).
