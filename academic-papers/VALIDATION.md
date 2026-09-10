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

## `examples/` expansion to three entries (2026-09-10)

Expanded this skill's `examples/` directory from one entry to three, per a
follow-up request to bring every skill's `examples/` to three worked
examples with genuinely different content.

- Scaffolded `examples/02-related-work-synthesis.md` with
  `agile-development`'s `generate_skill_example.py --skill academic-papers
  --role "Senior Postdoctoral Researcher / Literature Review Editor"
  --use-case "synthesizing a related-work section from a stack of papers
  instead of listing them"`, then filled it in by hand against
  `references/literature-review.md`'s own "list vs. synthesis" and
  "spotting the gap" guidance: five papers on dark-matter direct-detection
  combination methods, contrasting an annotated-bibliography-style paragraph
  (one sentence per paper, no comparison, no gap statement) against a
  paragraph organized methodologically by each prior method's specific
  approximation and the evidence against it, closing with a checkable
  coverage-gap statement.
- Scaffolded `examples/03-citation-claim-verification.md` with `--role
  "Research Integrity Reviewer / Co-Author" --use-case "verifying that a
  citation actually supports the specific numeric claim attached to it
  before submission"`, then filled it in against
  `references/citation-verification.md`'s verification-steps and ledger
  format: a manuscript cites a review article for a specific local
  dark-matter density value; the weak pass approves the citation on an
  abstract-level topic match, the expert pass traces the claim to the
  review's actual stated range, finds the specific number unsupported as
  stated, and produces a verification-ledger entry with a support verdict
  and a downstream fix (recomputing a rate prediction that depended on the
  corrected value).
- Both new files were checked with `python3
  ../agile-development/scripts/validate_skill_example.py examples/<file>` -
  both report `ok` (no missing sections, no out-of-order sections, 4 Key
  Takeaways each, zero placeholder markers).
- Confirmed (again, not assumed) that this skill's `validate_skill_bundle.py`
  still only scans `references/`, `scripts/`, and `assets/` for its orphan
  and existence checks - `examples/` is untouched by it, so no
  `REQUIRED_PATHS`-equivalent update was needed for the two new files, unlike
  the sibling skills whose validators track `examples/` explicitly.
- Added both new rows to `examples/README.md`'s index table.
- Re-ran `python3 scripts/validate_skill_bundle.py` (`OK`) and `python3 -m
  unittest discover -s tests -v` (27 tests, unchanged) after the additions -
  both clean.

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

## Example-authoring: Gated Pipeline pilot (2026-09-11)

Added this skill's first non-Contrast example, per Phase 3 of
`agile-development`'s four-archetype example-authoring revision (see that
skill's `references/example-authoring.md` for the full archetype spec; this
skill depends on `agile-development` being installed alongside it for the
tooling).

- Scaffolded and filled `examples/04-gated-pipeline-manuscript-submission.md`
  (Gated Pipeline archetype, role "Principal Research Scientist / Manuscript
  Editor"): preparing and submitting a cross-section-measurement manuscript
  to a target physics journal, structured across the three fixed phases.
  Phase 2's "specific regulatory/evaluation criteria" requirement (this
  initiative's own Open Question 4, flagged as a human/agent review
  responsibility rather than mechanically checkable) is met by citing
  `references/submission-and-peer-review.md`'s Pre-submission checklist and
  "Cover letters" section by name and by content, rather than a vague
  "industry best practices"; both section names and their bulleted content
  were read from the actual file before being cited, not assumed. Phase 3's
  red-team pass is grounded in `references/reviewer-style-assessment.md`'s
  Major/Minor concern classification and finds a systematic previously folded
  into "other systematics" is actually comparable to the statistical
  uncertainty in the highest-purity bin - a Major concern - before the final
  submit gate.
- One wording defect (an article/grammar slip, "not a incremental update")
  was caught by re-reading the draft and fixed before validation.
- `python3 ../agile-development/scripts/validate_skill_example.py
  examples/04-gated-pipeline-manuscript-submission.md` passes with no
  structural or placeholder findings - notably including the zero-placeholder
  scan, which meant avoiding the literal words this skill's own
  `submission-and-peer-review.md` checklist names as things to search a
  manuscript for (leftover placeholder markers), since quoting them verbatim
  would have been flagged by the same scan this example is meant to pass.
- Added one row to `examples/README.md`'s index (now four columns). No change
  was needed to `scripts/validate_skill_bundle.py`: it does not track
  `examples/` at all (only `references/`, `scripts/`, `assets/` are checked
  for orphaned/missing files), confirmed by re-reading the script rather than
  assumed - matching the exact caveat `agile-development`'s
  `references/example-authoring.md` already documents for this case. Re-ran
  `python3 scripts/validate_skill_bundle.py` (`OK`) and
  `python3 -m unittest discover -s tests -v` (27 tests, unchanged).

**Backlog (explicitly deferred, not silently missing):** three archetypes
remain unpiloted for this skill, per the source initiative's Phase 3 backlog
table - Contrast (a referee-response rewrite), Execution Trajectory (a raw
referee report through revision and cover letter), and Decision-Tree
(reviewer-comment triage: methodology objection vs. typo vs. major rewrite
vs. out-of-scope request). None were started in this pass.

## Examples expanded to three per archetype (2026-09-11)

Per an explicit follow-up request ("expand number of examples to three
examples per each archetype... These examples have very different content"),
brought Execution Trajectory, Gated Pipeline, and Decision-Tree each up to 3
examples (from 0/0/1 respectively), closing the backlog gap noted above for
Trajectory and Decision-Tree, and adding scenario diversity within Gated
Pipeline beyond the single manuscript-submission pilot. 8 new files added:

- **Execution Trajectory** (`05`-`07`): a three-comment referee report
  walked through triage to a resubmission cover letter (per
  `references/submission-and-peer-review.md`'s "Responding to referee
  reports"); a reproducibility audit of a paper's headline fitted slope that
  initially fails to reproduce, traced to a released config omitting a
  weighting step the paper's own Methods section describes (per
  `references/reproducibility-auditing.md`); and a symbol-reuse audit that
  builds a ledger to confirm a contradictory (not merely differing)
  definition of σ across two sections and numerically verifies the fix
  doesn't change the quoted result (per
  `references/equation-and-notation-auditing.md`).
- **Gated Pipeline** (`08`-`09`, plus the existing `04`): an NSF-style grant
  proposal (per `references/grant-and-fellowship-proposal-writing.md`,
  including its explicit prohibition on inventing budget/effort figures);
  and a thesis-by-publication assembly across three papers at different
  publication stages (per `references/thesis-by-publication-assembly.md`),
  whose red-team phase finds a genuine cross-paper notation clash (ε used
  for two different quantities before/after a collaboration-wide notation
  change) requiring a reconciling footnote rather than silent harmonization.
- **Decision-Tree** (`10`-`12`): referee-comment triage into five response
  categories (per `references/submission-and-peer-review.md`); systematic-
  review record screening, distinguishing a retrieval limitation from an
  ineligibility exclusion (per `references/systematic-review-screening.md`);
  and erratum/corrigendum/addendum classification for a post-publication
  error report, with worked before/after branching-fraction arithmetic (per
  `references/erratum-and-corrigendum-drafting.md`).
- All arithmetic in the new examples (uncertainty combination in `06` and
  `10`, the significance recomputation in `07`, the branching-fraction
  values in `12`) was independently computed (via `python3 -c "..."`), not
  just hand-checked, before being written into the files.
- One wording issue was caught and fixed during drafting: `12`'s first draft
  described the acceptance-correction error ambiguously as "applied twice";
  reworked to state precisely that the correct denominator already includes
  the correction once and the published version applied it an erroneous
  second time, with the arithmetic re-verified after the rewording.
- Avoided quoting `references/submission-and-peer-review.md`'s own
  Pre-submission-checklist wording for leftover placeholder markers
  verbatim in any new file, since this skill's own validator scans for
  exactly those literal words and would flag them even inside a quote (the
  same caveat noted in the `04` pilot's VALIDATION.md entry).
- `python3 ../agile-development/scripts/validate_skill_example.py
  examples/<file>.md` was run against all 8 new files individually and
  printed `: ok` for each, with no structural or placeholder findings.
- Added one row per new file to `examples/README.md`'s index (12 rows total,
  4 columns). No change to `scripts/validate_skill_bundle.py`: confirmed
  again that it does not track `examples/` (only `references/`, `scripts/`,
  `assets/`), so no `REQUIRED_PATHS`-equivalent update was needed or made.
- Re-ran `python3 scripts/validate_skill_bundle.py` (`OK: ... passed all
  checks.`) and `python3 -m unittest discover -s tests -v` (27 tests,
  unchanged - this pass added example content, not new test-relevant code)
  after the additions.

This closes the Execution Trajectory and Decision-Tree items from the prior
entry's backlog. The only remaining deferred item for this skill is the
Contrast archetype's fourth topic (a referee-response rewrite distinct from
the three Contrast examples already shipped) - not part of this follow-up
request, since it asked specifically about the three non-Contrast archetypes.
