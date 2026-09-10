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

## `examples/` — example-authoring rollout pass (2026-09-10)

Added this skill's first `examples/` entry, per Phase 3 of `agile-development`'s
example-authoring initiative (see that skill's `references/example-authoring.md`
for the generation prompt and format spec this follows). One pilot example, not
a bulk batch.

- Added a pointer to `agile-development`'s `references/example-authoring.md`
  under a new "Authoring a canonical worked example" group in SKILL.md's
  "Reference files" section, as a markdown link rather than a backtick-quoted
  path — this skill's own `validate_skill_bundle.py` treats any backtick text
  matching `references/...`/`scripts/...`/`assets/...` as a claim that the path
  exists inside *this* bundle, so a bare backtick reference to
  `agile-development`'s file would have failed that check; using a link instead
  of backticks around the cross-skill path avoids a false failure while still
  documenting the dependency explicitly.
- Scaffolded `examples/01-referee-response-significance-claim.md` with
  `agile-development`'s `generate_skill_example.py --skill academic-papers
  --role "Senior Research Scientist / Manuscript Editor" --use-case "responding
  to a referee report that questions a statistical-significance claim"`, then
  filled it in by hand: a referee questions whether a reported 3.5σ excess
  accounts for the look-elsewhere effect from scanning 20 independent mass
  points. The weak response restates the original number with no calculation
  and no manuscript change; the expert response quotes the comment, computes
  the trials-corrected global significance, and points to the exact revised
  manuscript text.
- The significance calculation was independently executed, not just
  hand-derived: extracted the code block from the finished markdown file
  (stripping the blockquote `> ` prefix) and ran it. Confirmed
  `p_local = 2.326e-4` (`z_local = 3.5σ`), and, after the 20-trial
  look-elsewhere correction, `p_global = 4.642e-3` (`z_global = 2.601σ`) -
  matching the file's stated `p_local = 2.3e-4`, `p_global = 4.6e-3`, and
  `z_global = 2.6σ` (rounded for prose). `python3 scripts/validate_skill_example.py`
  (from `agile-development`) reports `ok` - no structural or placeholder
  findings.
- Added `examples/README.md` (one-row index table, linking back to
  `agile-development`'s reference). This skill's `validate_skill_bundle.py`
  orphan check only scans `references/`, `scripts/`, and `assets/`, so
  `examples/` needed no `REQUIRED_PATHS`-equivalent change - confirmed by
  re-running `python3 scripts/validate_skill_bundle.py` after adding the new
  files, which still reports `OK` with no orphan or missing-reference findings.
- Re-ran `python3 -m unittest discover -s tests -v` (27 tests, unchanged - this
  pass added content, not new test code) after the change.

## Consistency audit and `agents/openai.yaml` addition (2026-09-10)

A "check and reorganize" pass covering this whole collection had already been run
against the other four skills (`skill-router`, `agile-development`,
`deep-learning`, `hep-analysis`, each with its own "Consistency audit" entry
dated the same day) but had not yet reached `academic-papers`. This pass closes
that gap.

- **Found and fixed a real structural gap**: this was the only skill in the
  collection without an `agents/openai.yaml`. Added one with the same
  `interface: display_name/short_description/default_prompt` shape used by all
  four siblings, parsed with `yaml.safe_load` to confirm it's valid YAML. Updated
  `README.md`'s file-tree diagram and "Per-agent invocation" section (previously
  a single merged "Codex and other skill-aware agents" bullet with no mention of
  `agents/openai.yaml`) to match the Codex bullet style used by every sibling
  README.
- Read `SKILL.md`, `README.md`, and every `references/*.md`/`examples/*.md` file's
  relative Markdown links with an anchor-aware resolver (stripping `#fragment`s
  before checking the target exists on disk): zero broken links found.
- Checked specifically for the `references/`-prefixed-display-text-with-bare-
  target mismatch pattern that the sibling audits found and fixed (3 occurrences
  in `agile-development`, 17 in `deep-learning`, 58 in `hep-analysis`): none found
  here - every cross-reference in this package already showed the bare filename
  as both link text and target.
- Checked specifically for `[[wiki-link]]` double-bracket syntax (found and fixed
  in `agile-development`, `deep-learning`, and `hep-analysis` in this same
  cross-repository pass): none found in this package - its cross-skill mentions
  (`hep-analysis`, `deep-learning`) already used plain backticks throughout.
- `scripts/validate_skill_bundle.py` does not check for `agents/` at all (only
  `references/`, `scripts/`, `assets/`), so adding the new file could not trigger
  a false "orphaned file" or "missing reference" finding; confirmed by re-running
  it (`OK`, no findings) both before and after the addition.
- Re-ran `python3 scripts/validate_skill_bundle.py` (`OK`) and
  `python3 -m unittest discover -s tests -v` (27 tests, unchanged - this pass
  added a metadata file and documentation, not new test-relevant code) after the
  changes.
