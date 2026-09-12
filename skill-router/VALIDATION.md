# Package Validation Record

Validation date: 2026-09-05. Helper test environment: Python 3, standard library
only.

## Completeness pass (2026-09-05)

This pass brought the package in line with the completeness level already
established for `hep-analysis` in this collection: a structural bundle validator,
an automated test suite, dual-environment (Codex/Claude Code) install docs
(`README.md`, `agents/openai.yaml`), and this validation record. `skill-router`
previously shipped as a single `SKILL.md` file with no `scripts/`, `tests/`, or
`agents/` - this pass added all three alongside the pre-existing `README.md`.

- `scripts/validate_skill_bundle.py` was added. Beyond the standard file-presence/
  frontmatter/README-section checks used across this collection's other skills, it
  also parses SKILL.md's routing-rule bullets into a skill-name list and, when run
  next to the other skill folders (as it is in the installed collection), notes any
  routed name with no matching sibling folder - informationally only, since
  routing to an uninstalled skill is expected behavior, not a bug, per this
  package's own documented design ("it only routes to skills that are actually
  installed").
- `tests/test_skill_router.py` was added (7 tests,
  `python3 -m unittest discover -s tests -v`):
  - `extract_routed_skill_names` was checked against the real, shipped `SKILL.md`
    (correctly recovers `agile-development`, `deep-learning`, `hep-analysis` in
    order), against a synthetic two-entry routing table, and against prose
    containing bold text outside a routing-bullet position (correctly yields
    nothing).
  - `find_sibling_skill_dirs` was checked against a scratch directory tree: it
    finds a sibling folder that contains its own `SKILL.md`, excludes the skill's
    own folder from the result, and returns an empty set when no sibling looks
    like an installed skill.
  - The `validate_skill_bundle.py` CLI was run against the real, shipped bundle
    (passes) and against a scratch copy with every README section header removed
    on purpose (correctly fails with `README.md is missing sections`).
- `README.md`'s documented quick check (parsing `SKILL.md`'s frontmatter with
  PyYAML) was run as documented and succeeds.
- `agents/openai.yaml` was parsed with PyYAML and confirmed to carry
  `display_name`/`short_description`/`default_prompt`.

No behavioral defects were found in `SKILL.md` itself during this pass - the
routing rules, trigger keywords, and behavior steps were reviewed for internal
consistency and matched correctly against the three domain skills' own
frontmatter descriptions (`agile-development`, `deep-learning`, `hep-analysis`).

## Add academic-papers to the routing table (2026-09-10)

Added `academic-papers` as a fourth routing rule (placed first, alphabetically),
by explicit request rather than as a bug fix - this skill was previously and
deliberately excluded from routing (it's a reading/writing/formatting skill, not
a coding-domain one), and that exclusion is now reversed.

- `SKILL.md`: added the frontmatter `description` keywords for paper reading/
  writing/formatting/rebuttal tasks, and a new `- **academic-papers** - ...`
  routing bullet, explicit that it's the write-up layer, not the underlying
  statistical/ML/physics analysis (which still routes to `deep-learning`/
  `hep-analysis`).
- `tests/test_skill_router.py`: `test_extracts_names_from_real_skill_md`'s
  expected list was updated to
  `["academic-papers", "agile-development", "deep-learning", "hep-analysis"]`
  (order-sensitive, since it asserts the real, shipped `SKILL.md`'s bullet
  order) - this is the only test that needed a change, since the parsing logic
  itself (`extract_routed_skill_names`) is already generic over bullet count.
- `README.md`: updated every place that enumerated the three routed skills by
  name (the intro paragraph, "it only routes to..." caveat, the coverage
  paragraph) to include `academic-papers`, and added a matching example prompt.
- Re-ran `scripts/validate_skill_bundle.py` (now reports 4 routing entries,
  up from 3) and the full test suite (7 tests, unchanged count) - both clean.
- The top-level repository `README.md`'s `academic-papers` row previously
  stated "not part of `skill-router`'s routing set" - that statement is now
  false and was corrected in the same change (see that file's own history).

**Follow-up consistency check (2026-09-10, same day):** a subsequent "check
and reorganize" pass over this package caught one file the addition above
missed - `agents/openai.yaml`'s `short_description` and `default_prompt`
still enumerated only the original three skills (`agile-development`,
`deep-learning`, `hep-analysis`). Neither `validate_skill_bundle.py` nor the
test suite parses this file's routing-relevant text (only its presence and
YAML-parseability are checked), so a hand review was the only way to catch
it. Fixed to include `academic-papers`; re-parsed with `yaml.safe_load` to
confirm it's still valid YAML. No other staleness found on this pass:
`SKILL.md`'s per-skill routing bullets were cross-checked against each
target skill's actual current content (all four still accurate) and
`README.md`/`VALIDATION.md` were re-read end to end.

## Example-authoring rollout and discoverability pass (2026-09-10)

Two related changes from `agile-development`'s example-authoring initiative
(see that skill's `references/example-authoring.md` for the generation prompt
and format spec):

**Phase 3 - this skill's own pilot example.** Added
`examples/01-adding-a-routing-rule-without-overlap.md`, scaffolded with
`agile-development`'s `generate_skill_example.py --skill skill-router --role
"Senior Platform / Developer-Experience Engineer" --use-case "adding a new
routing rule to the table without creating overlap or ambiguity with an
existing rule"`, then filled in by hand around a real gap in this skill's own
tooling: `extract_routed_skill_names` in `scripts/validate_skill_bundle.py`
checks routing-bullet *format*, not semantic overlap between rules. Verified
directly, not just asserted: imported `extract_routed_skill_names` from the
real script and ran it against both the weak and expert routing-rule text
extracted from the finished example file - both parse to the identical
`['data-engineering']`, confirming the validator cannot distinguish a
well-scoped rule from an ambiguous one, which is the example's central point.
`python3 scripts/validate_skill_example.py` (from `agile-development`) reports
`ok` on the finished file.

Added `examples/README.md` and both new files to
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` (bundle now reports 8
files, up from 6). This broke `tests/test_skill_router.py`'s
`test_cli_reports_missing_readme_section`, which builds a synthetic scratch
bundle by hand and didn't include the new `examples/` files - it was failing
on "missing files" before ever reaching the README-section check the test is
actually about. Fixed by adding stub `examples/README.md` and
`examples/01-adding-a-routing-rule-without-overlap.md` files to the scratch
bundle fixture; this is a regression the `REQUIRED_PATHS` change caused
directly, not a pre-existing issue.

**Phase 4 - discoverability.** Extended the `agile-development` bullet in
`SKILL.md`'s routing table with one clause routing "author or generate a
canonical worked example for this or another installed skill's `examples/`
directory" to `agile-development`, and added a matching example prompt to
`README.md`'s "Example prompts" section.

Re-ran `python3 scripts/validate_skill_bundle.py` (8 files OK, 4 routing
entries) and `python3 -m unittest discover -s tests -v` (7 tests, all passing
including the fixed one) after both changes.

## Example expansion to three (2026-09-10)

Expanded `examples/` from the one pilot entry above to three, per the user's
request to bring every installed skill's `examples/` up to three entries with
genuinely different content each. Unlike the pilot entry (which is about
*authoring* a new routing rule), both new entries are about applying the
existing routing logic to a real incoming request.

- Scaffolded `examples/02-multi-skill-primary-secondary-routing.md` and
  `examples/03-negative-carve-out-not-a-match.md` with `agile-development`'s
  `generate_skill_example.py --skill skill-router`, then filled both in by
  hand, grounded in the actual text of `SKILL.md` rather than paraphrased
  from memory:
  - `02` is a request ("write the systematics paragraph for my paper's
    cutflow-based cross-section measurement") that matches both
    `hep-analysis` ("cutflows... systematic uncertainties") and
    `academic-papers` ("tightening scientific prose") at once. The weak
    approach invokes only the first-matching rule and treats the request as
    fully handled; the expert approach checks every rule before invoking
    any, then follows `SKILL.md`'s own Behavior rule 3 verbatim - stating
    "Using `hep-analysis` skill (primary), with `academic-papers` for
    manuscript prose," matching the exact phrasing pattern `SKILL.md` itself
    gives as an example ("Using `deep-learning` skill (primary), with
    `agile-development` for task breakdown").
  - `03` is a CI-permissions request containing the substring "root" ("fix
    the root cause of this failing CI job... permission to write to
    `/opt/build-cache`"), which superficially matches `hep-analysis`'s "ROOT
    C++, PyROOT" text. `hep-analysis`'s own routing rule was quoted verbatim
    from `SKILL.md` to confirm its carve-out text is exactly "Not for
    unrelated uses of 'root' (Linux root users, Android rooting,
    certificates, math or plant roots)" - the request is a Linux
    file-permissions problem, squarely inside that exclusion. The weak
    approach pattern-matches the keyword and invokes `hep-analysis` anyway;
    the expert approach checks the carve-out, finds no rule applies, and
    follows Behavior rule 4 ("proceed normally without mentioning this
    skill") verbatim.
  - `python3 ../agile-development/scripts/validate_skill_example.py` reports
    `ok` for both files - no structural or placeholder findings.
- Added both new rows to `examples/README.md`'s index table and both new
  files to `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`. As with the
  pilot addition above, this required adding matching stub files to
  `tests/test_skill_router.py`'s `test_cli_reports_missing_readme_section`
  scratch-bundle fixture (same regression mechanism as before, fixed the same
  way) - confirmed by re-running the full suite, not just re-reading the
  pilot's note and assuming the same fix still applied.
- Re-ran `python3 scripts/validate_skill_bundle.py` (10 files OK, 4 routing
  entries) and `python3 -m unittest discover -s tests -v` (7 tests, all
  passing) after the changes.

## Example-authoring: Decision-Tree pilot (2026-09-11)

Added this skill's first non-Contrast example, per Phase 3 of
`agile-development`'s four-archetype example-authoring revision (see that
skill's `references/example-authoring.md` for the full archetype spec; this
skill depends on `agile-development` being installed alongside it for the
tooling).

- Scaffolded and filled
  `examples/04-decision-tree-multi-skill-ambiguous-routing.md` (Decision-Tree
  archetype, role "Lead Platform / Developer-Experience Engineer"): a request
  touching multiple skills at once ("refactor this PyTorch training loop so a
  paper's reproducibility section can describe it accurately"), the exact
  scenario named in the source initiative's Phase 3 table for this skill.
  Formalizes `SKILL.md`'s Behavior rules 2-4 into a 5-row triage matrix, and
  adds one row not directly in those rules but implicit in them: when a
  domain skill's own specific rule (`deep-learning`'s "training and eval
  loops") already covers a code-change verb that `agile-development`'s
  generic rule would also match, the domain skill is treated as sufficient
  and `agile-development` is not separately invoked as a third skill.
- `python3 ../agile-development/scripts/validate_skill_example.py
  examples/04-decision-tree-multi-skill-ambiguous-routing.md` passes with no
  structural or placeholder findings.
- Added one row to `examples/README.md`'s index (now four columns) and the
  new file to `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`. As with
  every prior addition to this skill's `examples/`, this required adding a
  matching stub file to `tests/test_skill_router.py`'s
  `test_cli_reports_missing_readme_section` scratch-bundle fixture (same
  regression mechanism noted in the two prior passes above, fixed the same
  way) - the full suite was run and caught the omission on the first attempt
  (1 failure), not assumed fixed from the pattern alone.
- Re-ran `python3 scripts/validate_skill_bundle.py` (11 files OK, 4 routing
  entries) and `python3 -m unittest discover -s tests -v` (7 tests, all
  passing) after the fix.
- Updated `SKILL.md`'s `agile-development` routing-rule bullet (Phase 4.1 of
  the source initiative) to name all four archetypes by name instead of only
  "a Weak vs. Expert contrast plus key takeaways."

**Backlog (explicitly deferred, not silently missing):** three archetypes
remain unpiloted for this skill, per the source initiative's Phase 3 backlog
table - Contrast (routing-rule wording, ambiguous vs. precise), Execution
Trajectory (one raw ambiguous request walked through rule-matching to
invocation), and Gated Pipeline (adding a new routing rule without keyword
collision, phase-gated on a collision check). None were started in this pass.

## Example-authoring: expansion to 3 examples per archetype (2026-09-11)

Per an explicit follow-up request ("expand number of examples to three
examples per each archetype... These examples have very different
content"), expanded Execution Trajectory, Gated Pipeline, and Decision-Tree
from 1 example each to 3 each - 8 new files total (`05`-`12`), closing the
Trajectory and Gated Pipeline backlog items noted above in full. The
Contrast backlog item (routing-rule wording, ambiguous vs. precise) remains
open and out of scope for this pass.

Every new example is grounded in this skill's own live `SKILL.md` text (read
fresh before writing, not paraphrased from memory) or in `scripts/
validate_skill_bundle.py`'s actual parsing logic, and every literal command/
grep/regex output shown was actually run and its real output used - two were
caught and corrected during authoring, not after: a claimed `True` result
from a substring check that was actually `False` until whitespace
normalization was added (the routing bullets wrap across lines), and a
claimed "zero collision" grep result for the word "pipeline" that was
actually two real hits (`deep-learning`'s "tensor/pipeline/sequence" and
`hep-analysis`'s "columnar pipelines") once the exact command was run instead
of assumed clean.

- **Execution Trajectory** (`05`-`07`, alongside existing `04`): `05` walks a
  clean single-rule match (`academic-papers`) for a manuscript-abstract
  request that is physics-adjacent but not analysis work; `06` routes a
  "refactor... fix" ROOT-macro request to `hep-analysis` alone, since its
  domain-specific rule outranks `agile-development`'s generic code-change
  trigger for that exact code path (the same reasoning example `04`'s matrix
  states, applied here as a single-request walk-through instead of a general
  rule); `07` is a clean no-match case (a Wi-Fi troubleshooting request) with
  zero keyword overlap with any rule at all, distinct from `03`'s single
  false-positive-keyword case.
- **Gated Pipeline** (`08`-`10`): `08` adds a new `devops-infrastructure`
  routing rule, catches a real "pipeline" collision with two existing rules
  at the Phase 1/2 collision-check gate, and catches a second, later
  collision ("build," from the draft's own prose) only at the Phase 3
  red-team stage - demonstrating why the final gate re-checks the drafted
  bullet's *own* text, not just the original candidate keyword list; `09`
  resolves a real observed ambiguity between `academic-papers` and
  `hep-analysis` for figure/plot-interpretation requests, and its red-team
  phase confirms a genuine two-layer request should still trigger the
  existing primary/secondary rule rather than be treated as newly resolved;
  `10` expands `hep-analysis`'s existing "root" carve-out after a real
  false-positive category (a dental "root canal" question) and honestly logs
  - rather than papering over - the structural fact that an enumerated
  carve-out list can never be exhaustive against open-ended English idioms.
- **Decision-Tree** (`11`-`12`, alongside existing `04`): `11` formalizes the
  figure-interpretation boundary from `09` into a reusable 5-row matrix
  covering `academic-papers`/`hep-analysis`/`deep-learning`; `12` handles a
  request with four simultaneous surface keyword hits across two different
  rules (LaTeX, fix, refactor, update, in a personal-resume request) where
  every single hit resolves to "does not apply" on inspection - a harder case
  than `03`'s one-keyword carve-out, and distinct from `04`'s "genuine
  multi-skill match" case in the opposite direction (many surface matches,
  zero real ones).
- `python3 ../agile-development/scripts/validate_skill_example.py` reports
  `ok` for all 8 new files - no structural or placeholder findings.
- Added 8 rows to `examples/README.md`'s index and 8 new file paths to
  `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`. As with every prior
  addition to this skill's `examples/`, this required adding 8 matching stub
  files to `tests/test_skill_router.py`'s
  `test_cli_reports_missing_readme_section` scratch-bundle fixture (the same
  regression mechanism noted in the two prior passes) - this time the fix
  was applied before running the suite rather than found by a failure, and
  the full suite was still run afterward to confirm rather than assumed.
- Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 19 files
  present and non-empty, 4 routing entries", up from 11) and
  `python3 -m unittest discover -s tests -v` ("Ran 7 tests" / "OK", unchanged
  - this pass added example content and one test fixture update, not new
  test cases) after all changes.

**Archetype coverage is now symmetric**: every archetype (Contrast,
Execution Trajectory, Gated Pipeline, Decision-Tree) has exactly 3 examples
in this skill's `examples/`. The only remaining backlog item from the source
initiative's Phase 3 table is the Contrast one noted above (routing-rule
wording, ambiguous vs. precise) - not started here, since Contrast already
has 3 examples and this pass's brief was the three non-Contrast archetypes.

## Consistency audit, no defects found (2026-09-11)

A "check and reorganize" pass with no content changes: re-ran the bundle
validator and full test suite, diffed `REQUIRED_PATHS` against every file
actually on disk, checked every relative Markdown link across the package
(including `examples/README.md`'s cross-repository link into
`agile-development/references/example-authoring.md`) for a broken target,
swept for `[[wiki-link]]` syntax, validated all 12 `examples/*.md` files with
`agile-development`'s `validate_skill_example.py`, cross-checked
`examples/README.md`'s Archetype column against each file's actual
`archetype:` frontmatter (or its absence, for the three pre-archetype-field
legacy files `01`-`03`, which the shared validator treats as Contrast), and
re-read `SKILL.md`, `README.md`, and `agents/openai.yaml` end to end for
staleness against each other.

- No defects found. `scripts/validate_skill_bundle.py` reports "Bundle OK: 19
  files present and non-empty, 4 routing entries found (academic-papers,
  agile-development, deep-learning, hep-analysis)." with no path missing from
  `REQUIRED_PATHS` or vice versa; all 7 tests in
  `tests/test_skill_router.py` pass, including the scratch-bundle fixture in
  `test_cli_reports_missing_readme_section`, which still lists all 12
  `examples/` stub files; all 12 real example files validate clean; every
  link resolves; `agents/openai.yaml`'s `short_description`/`default_prompt`
  still name all four routed skills.
- This is a smaller surface than `agile-development`'s equivalent audit the
  same day (which found and fixed a real gap): `skill-router` ships no
  `references/` or `assets/` directory and only one script, so there was
  correspondingly less for documentation to drift out of sync with.

## Second-wave example-authoring pass: Adversarial Audit, Test-First (2026-09-12)

Added two new canonical examples in `agile-development`'s second-wave
archetypes, continuing the four-archetype example-authoring plan (Contrast/
Trajectory/Gated Pipeline/Decision-Tree already covered this skill; this
pass adds Adversarial Audit and Test-First). Both are about `skill-router`'s
own routing-table mechanics, since this skill has no other domain.

- `examples/13-adversarial-audit-new-routing-rule-proposal.md`: attacks a
  proposed `frontend-design` routing-rule bullet for a hypothetical sixth
  skill, finding an unflagged keyword collision with `agile-development`'s
  real "UI work" trigger and a missing "Not for X" exclusion clause (both
  checked directly against the real `SKILL.md` routing table), patched with
  an explicit primary/secondary resolution mirroring
  `examples/04-decision-tree-multi-skill-ambiguous-routing.md`'s existing
  precedent.
- `examples/14-test-first-routing-parser-primary-secondary.md`: a
  hypothetical `resolve_primary_secondary()` function, red on an
  alphabetical-order resolver that wrongly promotes `agile-development` to
  primary, green on a resolver that demotes the generic fallback per
  Behavior rule 2's own worked example - dogfoods `tests/test_skill_router.py`'s
  real `unittest`/`sys.path`-insert style. Does not modify any real
  `skill-router` source file; the illustrative "implementation" lives
  entirely inside the example's own fenced code blocks.
- Both pass `agile-development/scripts/validate_skill_example.py` and the
  diversity checker (`check_example_diversity.py`) shows no archetype/skill
  repeats across the 12-file second-wave batch.
- `examples/README.md`'s intro line updated from "four archetypes" to
  "eight archetypes"; two rows added to its index (14 rows total).
- `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` extended with the
  two new example files. This exposed a real gap:
  `tests/test_skill_router.py`'s `test_cli_reports_missing_readme_section`
  builds a synthetic scratch bundle with a hardcoded file list mirroring
  `REQUIRED_PATHS` at the time the test was written, and had not been
  updated for the two new required files - the validator correctly reported
  them "missing" before the test ever reached the README-section check it
  actually exercises. Fixed by adding two more placeholder-file lines to
  the scratch fixture, matching its existing pattern. Re-ran
  `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 21 files present
  and non-empty, 4 routing entries found") and
  `python3 -m unittest discover -s tests -v` (7 tests, all passing after
  the fixture fix) after the change.

## Expand all four second-wave archetypes to three examples per skill (2026-09-12)

Every archetype now ships 3 examples per skill (not 3 total, one per skill) -
matching how Contrast/Trajectory/Gated-Pipeline/Decision-Tree already work
here. Added 10 new examples (15-24) to close the gap: Adversarial Audit and
Test-First each had 1, now have 3; Elicitation and Postmortem had none, now
have 3 each. All 10 are about `skill-router`'s own routing-table mechanics,
since this skill has no other domain.

- `examples/15-17` (Elicitation): "add a new skill for technical writing",
  "this request should probably use two skills, can you check?", "make the
  router better at catching edge cases" - three underspecified requests
  resolved against the real `SKILL.md` routing rules and Behavior section
  (a new bullet plus a non-regressing carve-out; a concrete
  deep-learning/agile-development two-skill test case; a single confirmed
  "fit" false-positive fix).
- `examples/18-19` (Adversarial Audit): attack a proposed Behavior-rule-3
  rewrite that would narrate every non-match (closed by keeping the
  precision in the routing rules' own carve-out text) and a proposal to
  merge the academic-papers/hep-analysis bullets (closed by keeping them
  separate so each skill's own reference set stays attached to a bullet that
  matches its actual scope).
- `examples/20-21` (Test-First): a `find_sibling_skill_dirs` invariant
  (excluding a sibling whose `SKILL.md` exists but is empty) and a bundle-
  validator invariant (rejecting a `SKILL.md` whose frontmatter exceeds the
  1024-character plugin spec limit, the same class of issue this repository
  hit for real in the `5c6ecc2` frontmatter-trim commit) - both dogfood real
  functions in `scripts/validate_skill_bundle.py`.
- `examples/22-24` (Postmortem): a missing-carve-out keyword hijack, a
  frontmatter-length truncation silently breaking a routing bullet, and two
  bullets both claiming a generic verb causing ambiguous double-routing -
  all three grounded in the real current `SKILL.md` routing rules and
  Behavior section, with 5-Whys chains terminating in a missing mechanical
  check rather than "human error".
- All 10 pass `agile-development/scripts/validate_skill_example.py`; zero
  placeholder markers.
- `examples/README.md`: added 10 rows (15-24), 24 rows total.
- `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` extended with the 10
  new example files. This exposed the same fixture-staleness gap as the
  prior pass: `tests/test_skill_router.py`'s
  `test_cli_reports_missing_readme_section` scratch bundle's hardcoded file
  list had not been updated for the 10 new required files. Fixed by adding
  10 more placeholder-file lines to the fixture, matching its existing
  pattern - the same class of maintenance gap the prior pass's note already
  flagged, now recurring because the fixture is still a hand-maintained
  mirror of `REQUIRED_PATHS` rather than derived from it.
- `agile-development/scripts/check_example_diversity.py`'s cross-skill
  constraint no longer applies to this skill's second-wave archetypes (each
  now deliberately repeats this skill 3x per archetype) - see
  `agile-development/references/example-authoring.md`'s revised "Diversity
  rule". This batch was hand-curated instead: each trio targets a
  conceptually distinct request/proposal/invariant/incident.
- Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 31 files
  present and non-empty, 4 routing entries found") and
  `python3 -m unittest discover -s tests -v` (7 tests, all passing after the
  fixture fix) after the change.

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

- `05-trajectory-single-clean-match-academic-papers.md` -> `04-trajectory-single-clean-match-academic-papers.md`
- `06-trajectory-generic-verb-vs-domain-specific-rule.md` -> `05-trajectory-generic-verb-vs-domain-specific-rule.md`
- `07-trajectory-clean-no-match-proceed-normally.md` -> `06-trajectory-clean-no-match-proceed-normally.md`
- `08-gated-pipeline-adding-a-new-rule.md` -> `07-gated-pipeline-adding-a-new-rule.md`
- `09-gated-pipeline-disambiguating-figure-interpretation.md` -> `08-gated-pipeline-disambiguating-figure-interpretation.md`
- `10-gated-pipeline-expanding-a-carve-out.md` -> `09-gated-pipeline-expanding-a-carve-out.md`
- `04-decision-tree-multi-skill-ambiguous-routing.md` -> `10-decision-tree-multi-skill-ambiguous-routing.md`
- `15-elicitation-new-skill-request.md` -> `13-elicitation-new-skill-request.md`
- `16-elicitation-two-skills-request.md` -> `14-elicitation-two-skills-request.md`
- `17-elicitation-router-edge-case-request.md` -> `15-elicitation-router-edge-case-request.md`
- `13-adversarial-audit-new-routing-rule-proposal.md` -> `16-adversarial-audit-new-routing-rule-proposal.md`
- `18-adversarial-audit-fallback-text-proposal.md` -> `17-adversarial-audit-fallback-text-proposal.md`
- `19-adversarial-audit-bullet-consolidation-proposal.md` -> `18-adversarial-audit-bullet-consolidation-proposal.md`
- `14-test-first-routing-parser-primary-secondary.md` -> `19-test-first-routing-parser-primary-secondary.md`

This rename also touched 5 example files' own prose, which cross-reference sibling example filenames by name as precedent (including one cross-skill reference into `academic-papers/examples/`) - all updated to the new names. `tests/test_skill_router.py`'s scratch-bundle fixture list was updated to the new filenames (order not re-sorted there since it is fixture setup, not documentation). Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 31 files present and non-empty, 4 routing entries found") and `python3 -m unittest discover -s tests -v` (7 tests, all passing) after the rename. All 24 example files individually re-validated with `agile-development/scripts/validate_skill_example.py` ("ok").

## Full-bundle audit: stale post-move example prompt (2026-09-12)

A full audit of this skill (bundle validator, test suite, every relative
Markdown link, and every routing bullet cross-checked against the sibling
skills' own `SKILL.md` descriptions) found one stale line: the earlier
"Move example-authoring and prompt-engineering-and-token-optimization to
task-authoring" change updated this skill's own `SKILL.md` and
`examples/README.md` to point the canonical-example-authoring capability at
`task-authoring`, but missed `README.md`'s "Example prompts" section, which
still claimed "Generate a canonical `examples/` entry for the
`hep-analysis` skill." routed to `agile-development`. Since `task-authoring`
capabilities are explicitly carved out of this skill's routing table (see
`SKILL.md`'s `agile-development` bullet), repointing the line to
`task-authoring` would have been equally wrong; fixed it to state plainly
that the request is a `task-authoring` capability not routed through this
table at all, cross-referencing the carve-out note. No other stale
reference, broken relative link, missing file, or routing-bullet/sibling-
skill drift was found. Re-ran `python3 scripts/validate_skill_bundle.py`
("Bundle OK: 31 files present and non-empty, 4 routing entries found") and
`python3 -m unittest discover -s tests -v` (7 tests, all passing) after the
fix.

## Add `task-authoring` as a fifth routing entry (2026-09-12)

Promoted `task-authoring` from an explicit carve-out (its three capabilities -
canonical example authoring, prompt engineering/token budgeting, and now also
standalone Task Markdown authoring - were previously named only inside the
`agile-development` bullet as "not routed through this table") to a full fifth
routing-table bullet, alphabetically last (`academic-papers`,
`agile-development`, `deep-learning`, `hep-analysis`, `task-authoring`).

- `SKILL.md`: added the `task-authoring` bullet (trigger phrases, and a
  two-way carve-out against `agile-development` - live scoping/implementation
  stays with `agile-development`, a standalone written task/ticket/spec goes
  to `task-authoring`); rewrote the `agile-development` bullet's note to
  point at the new bullet instead of saying "not routed through this table";
  extended the frontmatter `description` to name `task-authoring` and its
  three capabilities. Description length checked explicitly (956/1024 chars)
  given this skill's own `examples/23-postmortem-frontmatter-length-
  truncation.md` is a worked example of exactly this failure mode.
- `README.md`: added `task-authoring` to the domain-skill list, the
  partial-install note, and "Coverage and boundaries"; fixed the "Example
  prompts" line that previously (see the audit entry above) claimed the
  canonical-example-authoring prompt was unrouted - it now correctly routes
  to `task-authoring` - and added a second example prompt disambiguating a
  `task-authoring` request from a similarly-worded `agile-development` one.
- `agents/openai.yaml`: added `task-authoring` to `short_description` and
  `default_prompt`.
- `tests/test_skill_router.py`: updated
  `test_extracts_names_from_real_skill_md`'s expected name list to include
  `task-authoring`.
- Updated every place in `examples/` that stated the routing table's size as
  a literal fact rather than flavor text: eight "four routing rules"/"four
  bullets"/"four domain [skills]" mentions across
  `examples/04-trajectory-single-clean-match-academic-papers.md`,
  `06-trajectory-clean-no-match-proceed-normally.md`,
  `07-gated-pipeline-adding-a-new-rule.md` (two),
  `08-gated-pipeline-disambiguating-figure-interpretation.md`,
  `15-elicitation-router-edge-case-request.md`,
  `17-adversarial-audit-fallback-text-proposal.md` (two), and
  `examples/README.md`, all changed to "five" - and the literal reproducible
  `Bundle OK` transcript in
  `examples/21-test-first-bundle-validator-message-invariant.md`, updated
  from the real validator's new output (this also corrected a pre-existing,
  unrelated error in that line: it previously said "24 files present",
  which undercounted even the old 31-file bundle). `examples/12-decision-
  tree-multiple-false-positive-keywords.md`'s "four simultaneous surface
  keyword matches" and `09-gated-pipeline-expanding-a-carve-out.md`'s "four
  specific categories" were left unchanged - both count something other than
  the size of the routing table (keyword hits in one request; the `hep-
  analysis` "root" carve-out's enumerated list) and are unaffected by this
  change.
- Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 31 files
  present and non-empty, 5 routing entries found (academic-papers,
  agile-development, deep-learning, hep-analysis, task-authoring)") and
  `python3 -m unittest discover -s tests -v` (7 tests, all passing) after
  every change above, and re-confirmed zero broken relative Markdown links
  across the bundle.
- Not done as part of this change: no new `examples/` entries were added
  specifically illustrating the new `task-authoring` bullet (e.g. a
  Contrast or Decision-Tree scenario disambiguating it from
  `agile-development`) - the existing 24 examples (3 per archetype x 8
  archetypes) were updated only where they asserted a stale fact about the
  old 4-rule table, not expanded. Whether a dedicated `task-authoring`
  worked example should be added to reach the same 3-per-archetype
  treatment other bullets get is an open follow-up, not resolved here.

## Limitations

- `skill-router` contains no code that acts on real user requests - its entire
  effect is instructing an LLM which other skill to invoke. This cannot be
  exercised by an automated test in the way a CLI script can; the tests above
  validate the bundle's structure and the routing table's machine-parseable shape,
  not whether an LLM actually follows the routing instructions correctly on a
  given prompt.
- The sibling-folder check in `validate_skill_bundle.py` is opportunistic: it only
  runs meaningfully when this folder sits next to other skill folders (as in the
  installed `~/.agentic_ai_skills` collection). Run standalone, or copied
  elsewhere without its sibling skills, that check is silently skipped rather than
  failing.
