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
