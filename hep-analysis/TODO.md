# TODO for future Claude sessions (hep-analysis)

State (verified 2026-10-02 on `main`, all work merged through PR #102): `python3 scripts/validate_skill_bundle.py` OK (121 files); `python3 -m unittest discover -s tests` 222 tests OK. There are 12 skips without the optional environments: 7 ROOT, 4 pyhf, 1 Combine. There are 5 skips with `HEP_ROOT_PYTHON` set. P1-P4 and follow-up rounds 3-6 are done, and the 2026-10-02 passes (ref 13 and AMS checks, awkward, run-before-deliver, units, P03 and P08 wording) are merged. Open: one decision, one dated re-check and two recurring checks. Read `VALIDATION.md` first, then this file.

Working rules:
- Work on a branch and ask before pushing or merging.
- Run `python3 -m unittest discover -s tests` and `python3 scripts/validate_skill_bundle.py` before committing.
- Keep `SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` `REQUIRED_PATHS` and `agents/openai.yaml` in sync.
- Record every result, including negative ones, in `VALIDATION.md`.
- Do not change physics behavior in a template or reference without saying so.
- Haiku in `claude -p` loads `SKILL.md` but almost never opens a reference, so anything that must happen goes in `SKILL.md`.
- Grade code-writing prompts (P02) by executing the scripts they deliver, and read the Bash commands that `tests/prompts_eval.py` records in each `result.json`; reading the code is not enough. Fix an automatic scorer on the baseline before trying new wording.

**Description is frozen** at the round-5 wording: 6 of 1024 characters are left. The round-6 "quick calculations" variant gained only noise (70/80 vs 65/80). A *fifth* fresh set, `trigger_queries_task.json` (task-style requests: review/write/debug with pasted configs and errors; balanced collider / space / IACT-neutrino-air-shower; 20 positives, 20 negatives of which 8 are non-HEP and 12 sibling near-misses), was built 2026-10-02 and has **not been run**: keep it unrun until a description change is actually proposed, then run it once as the deciding set. A sixth set is needed after that. Spent sets: `trigger_queries.json` (tuning), `trigger_queries_holdout.json`, `trigger_queries_formula.json`, `trigger_queries_calc.json`. After any change, rerun `tests/routing_eval.py` on Sonnet and Haiku, and run the sibling skills' validators and tests.

## Environment facts (re-check, they may have changed)

- PyROOT works only under `/opt/homebrew/bin/python3.14` (Homebrew ROOT 6.38). Set `HEP_ROOT_PYTHON` to it for `tests/test_root_integration.py`. Under the miniconda `python3`, `import ROOT` fails with a cppyy symbol error (Python ABI mismatch).
- `~/.zshrc` sets `ROOT_INCLUDE_PATH` to Xcode's libc++ and sources Homebrew `thisroot.sh`. This breaks cling in any other ROOT, so run conda ROOT or Combine under `env -i`.
- ACLiC (`macro.C+`) fails on Homebrew ROOT, even for an empty macro, because of a CLT/Xcode SDK mismatch. It works on conda-forge ROOT 6.34 in a clean env.
- pyhf, uproot/awkward and Combine v11 are not in the base env. They were run from scratch envs; Combine was built against conda-forge ROOT 6.34.10. Install into a scratchpad env, never into the user's conda base.
- Only `tests/routing_eval.py` is a valid sibling-routing test: it uses `claude -p --setting-sources project` with the 7 repo skills symlinked in. `claude plugin eval` is not valid for this, because its child sees about 112 user skills, many without descriptions.
- `tests/prompts_eval.py` runs `tests/prompts.md` through isolated `claude -p`. Give each agent its own output directory.

## Open

- [x] **No-data prompts (decided 2026-10-02, not adopted):** a rule to build a labelled synthetic sample instead of asking was tried; P05 delivered in 1 of 8 runs (0 of 8 before) and that run presented synthetic numbers as informative, while P02 already delivers 8 of 8. The `SKILL.md` change was reverted; details in `VALIDATION.md`. Reopen only if a user asks for the behavior.
- [x] **P02 turn limit (fixed 2026-10-02):** the turns went to learning uproot's writing API for the test data and the output histogram. `scripts/make_synthetic_nanoaod.py` now builds the sample and prints the expected numbers, and `SKILL.md` says not to write ROOT output unless asked: P02 x16 went from 3/24 turn-limit runs to 0/16, with all 16 scripts verified against the known numbers. Details in `VALIDATION.md`.
- [ ] **Dated re-check (after mid-2027):** check the AMS-02 Layer-0 status in ref 38. The installation creates a new detector era, and the schedule is known only from a CERN news item (ams-analysis C102).
- [ ] **Recurring, on any change to references 02/17/37 or the `SKILL.md` invariants, procedure or "Check first" rows:** re-run `tests/prompts.md` on Haiku with `tests/prompts_eval.py`, at least 2 samples per prompt (about $1.5-1.8, 32 runs). Last run 2026-10-02 after every change of that day: 30 PASS, 8 -> 2 PARTIAL over seven reruns, 0 FAIL. Per-prompt results are in `VALIDATION.md`.
- [ ] **Recurring, after each pass:** update the `VALIDATION.md` header date and counts (file count, test count, skips). Last done 2026-10-02 (121 files, 222 tests, 12 skips).

Accepted residuals (not tasks unless priorities change):
- Haiku skips the skill for self-contained numeric questions: calorimeter resolution 0/4, Cherenkov angle, photoelectron yield, TOF reach.
- Sonnet routes the AMS-vocabulary TOF+rigidity mass question to `ams-analysis`. Generic wordings go here 4/4. The case is marked `also_ok`.

## Done (do not redo; details in `VALIDATION.md`)

**P1 - verification gaps (2026-09-24/25)**
- All ROOT assets (`assets/*.cpp`, `plot_branch.C`, the PyROOT assets) and `scripts/new_root_cpp_project.sh` were run through a full cmake build on a synthetic TTree. The five PyROOT scripts were run on a real file and workspace, with the fixture generator in `tests/make_root_fixtures.py`.
- `assets/uproot_awkward_analysis.py` was run; a missing sumw2 was fixed. Its config's `selection.cuts` and `histograms` blocks are now labeled documentation-only.
- `assets/pyhf-counting.json` was validated with pyhf. The Combine datacard template's limit matches pyhf within 1% (`tests/test_combine_template.py`).
- ACLiC `plot_branch.C+` was verified on conda-forge ROOT 6.34: bin-identical to the interpreted run.
- Physics helpers were cross-checked against independent references (`tests/test_reference_values.py`). A Stormer vertical-cutoff bug was fixed.
- The numbers in refs 18-50 were audited from knowledge, with 2 corrections. The latest-results list in ref 13 was re-checked live: PDG links moved to 2026, the ref 30 knee/ankle values were corrected, and the ref 33 IACT scale is now 10-20%.

**P2 - behavior and triggering (2026-09-24 to 09-28)**
- Wrote 16 prompts in `tests/prompts.md` and ran them with and without the skill on Opus and Haiku. Haiku scored 3/16 PASS without the skill and 15/16 with it.
- Fixes: P05 blinding and P07 prior-tuning in `SKILL.md`/ref 01; P01 and P10 in refs 03 and 35. The P08 flux invariant says "no" to sqrt(N) and gives the exact `cosmic_ray_flux.py` command plus a Garwood table, guarded by a test.
- Description tuned: Haiku recall went from 22/40 to 38/40 runs (suite in `evals/`).
- Held-out set: Haiku 34/40, Sonnet 40/40, at most 1/40 false triggers.
- Formula set: Haiku recall went from 48/80 to 58/80.
- Calc set: the variant was not adopted.
- Routing hygiene: all near-misses go to the right sibling. The sibling under-triggering findings were moved to those skills' TODO lists (PR #24).
- All 24 examples validate against their archetype rules; the runnable ones were run.

**P3 - content and structure (2026-09-24/25)**
- Progressive disclosure: agents read 1-3 references per task. Ref 14 got a task-to-section map.
- Overlap with `ams-analysis` and ref 38 is clean. 5 duplicated rows were removed from ref 49 Table 8.
- For the missing example topics, the user chose verified walkthroughs in refs 07/09/20/28/33/35 over new archetype examples (Geant4 not executed).
- Every script except the bundle validator has a test. Added an end-to-end sample analysis (`assets/end_to_end_sample_analysis.py`, `tests/test_end_to_end.py`).
- Multi-platform check: no Claude-only tool dependencies. `agents/openai.yaml` is current.
- Skill-reviewer pass applied, with 3 findings declined for stated reasons.

**P4 - decisions**
- `__pycache__` is already gitignored.
- The user said all three experiment families matter equally: AMS-02/space, CMS/ATLAS collider, IACT/neutrino/air shower. Balance the prompts across them.
- The latest-results policy is in `references/13-sources.md`.

**P5 - SKILL.md hardening from Haiku reruns (2026-10-02, PR #90-#102; details in `VALIDATION.md`)**
- Ref 13 live re-check and IACT caveats corrected (CTA requirement <10%, VERITAS flux ~25%); AMS-02 numbers checked against Phys. Rept. 894; fifth query set built and kept unrun.
- `SKILL.md` additions: cycle-24 solar epoch (P10), awkward leading-object rule (P02), run-delivered-code step with a three-fix cap and run-bundled-scripts line, MC-normalization units note and RDataFrame code request (P01), per-cut yield check for kinematic systematics (P03), run `cosmic_ray_flux.py` with Bash and quote its output (P08). Each has a guard test; tests 205 -> 214.
- `tests/prompts_eval.py` records Bash commands per run. Seven full Haiku reruns that day went from 24/8/0 to 30/2/0 (PASS/PARTIAL/FAIL).
- `scripts/make_synthetic_nanoaod.py` (synthetic NanoAOD-like sample with known expected counts) fixed the P02 turn-limit failures; a rule to build a synthetic sample when no data is given was tried and not adopted.
