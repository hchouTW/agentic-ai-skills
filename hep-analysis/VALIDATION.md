# Package Validation Record

Validation date: 2026-10-02, full Haiku rerun after PR #101 (latest pass; P03 per-cut check line the same day; full Haiku rerun after PR #99 the same day; P01 units note and P08 run-the-script rule the same day; full Haiku rerun after the rule and cap the same day; P02 run-before-deliver rule the same day; P02 awkward leading-object rule the same day; P10 solar-epoch fix and rerun the same day; Haiku `tests/prompts.md` rerun the same day; AMS-02 numbers vs Phys. Rept. 894 the same day; ref 13 caveat follow-up the same day; ref 13 live re-check the same day; round 6 on 2026-09-28; earlier passes dated below). Helper test
environment: Python 3, standard library plus PyYAML; optional scipy, and ROOT 6.38.04
(Homebrew) via `/opt/homebrew/bin/python3.14` for the ROOT integration tests; Combine v11
built against conda-forge ROOT 6.34.10 in a scratch env for `tests/test_combine_template.py`.
Current counts: bundle 119 required files (plus 40 eval cases in `evals/`); 214 tests (7 ROOT, 4 pyhf and 1 Combine test skip without their environments).

## Full Haiku rerun after PR #101 (2026-10-02, branch `hep-analysis-rerun-after-101`)

Follow-up to PR #101, on merged `main` with the P03 per-cut check, the P01 units note, the
run-the-script rule, the run-before-deliver rule and cap, and the awkward and cycle-24 lines all in
place. `prompts_eval.py --model haiku --runs 2 -j 4`, 32 runs, $1.72, no errors. **29 PASS, 3
PARTIAL, 0 FAIL.** Full reruns that day: 24/8/0, 26/6/0, 26/5/1, 24/8/0, 28/4/0, now 29/3/0.

- Fixed prompts stay fixed: P01 2 PASS (factor 1000, `genEventSumw`, code; 8 of 8 runs since PR
  #99), P03 2 PASS (flat scaling is only a normalization change, per-cut yield check with the
  identical-yields warning, and MET named in both; was 0 of 8 before PR #101), P10 2 PASS (solar
  maximum, 1.2x margin, backtracing, demodulation; epoch correct 13/13 since the cycle-24 sentence),
  P02 2 PASS (both scripts executed on the synthetic TTree: 185 events, weighted mean 263.2 GeV and
  range 22.9-1038.9 GeV, as the reference; no weight sum printed).
- PARTIAL x3, none seen the same way before:
  - P08 run 1: gives [1.37, 5.92] and the script command, but divides by hand and is a factor 10 too
    small (1.27e-8, 5.48e-8); run 0 PASS (2.78e-7, 1.27e-7, 5.48e-7, errors -1.51e-7 and +2.70e-7,
    spillover and background). The P08 factor-10 slip has now appeared in 5 of the last 12 runs.
  - P12 run 0: not a detection and a trials correction, but the local significance is stated as 2.54
    sigma (Li & Ma gives 2.74) and the post-trial value as 0.01 sigma; run 1 PASS (2.74, p 0.71).
  - P13 run 0: asks the user for the proton and iron means instead of answering, quotes one hadronic
    model only, and includes a confused example (Xmax(p) = 700 below the 780 measured); run 1 PASS
    (EPOS-LHC and QGSJet, sigma(Xmax), muon content).
- PASS: P04 (no signal-contamination point), P05 (both say the m > 1 TeV region is masked), P06, P07,
  P09, P11 (no skill loaded, no number given), P14, N01, N02.
- No effect of any of today's seven SKILL.md changes on the non-targeted prompts beyond noise;
  P12 and P13 PARTIALs are single-run slips with no change near them. Remaining open item for the
  prompts is P08 (about half the runs divide by hand).

## P03 per-cut check line (2026-10-02, branch `hep-analysis-p03-check`)

- Change: the `SKILL.md` "Scaling the final histogram for a kinematic systematic" row now reads: a flat
  bin scaling is only a normalization change; vary the object (and propagate to MET and jet ordering),
  rerun selection and migration, then check the templates by comparing yields per cut, nominal against
  varied: identical yields mean the variation did not propagate. `SkillKinematicSystematicRowTest`
  guards the three phrases. Tests 213 -> 214, bundle 119 files, description unchanged (1019 of 1024).
- Rerun `prompts_eval.py --model haiku --only P03 --runs 6 -j 6`, $0.27. **6/6 PASS**: every run says
  a flat scaling only changes the normalization, varies the jets and reruns the selection, and gives
  the per-cut yield comparison with the "identical yields mean it did not propagate" warning; run 3
  also points to `scripts/check_systematic_variations.py`. Before the line: 0 of the 2 runs in each
  of the last four full reruns gave any yield check.
- Not fully followed: MET propagation appears in only 2 of 6 answers (jet ordering in 5 of 6),
  although the row names both. It is a sub-item of the rubric, so the runs still pass.
- 6 samples on one prompt; no full rerun after this change.

## Full Haiku rerun after PR #99 (2026-10-02, branch `hep-analysis-rerun-after-99`)

Follow-up to PR #99, on merged `main` with the P01 units note, the run-the-script rule, the run-before-deliver
rule and its cap all in place. `prompts_eval.py --model haiku --runs 2 -j 4`, 32 runs, $1.70, no
errors. **28 PASS, 4 PARTIAL, 0 FAIL.** The same day's full reruns: 24/8/0, 26/6/0, 26/5/1, 24/8/0,
and now 28/4/0; with 2 samples per prompt the spread is about the size of the noise, but the
direction matches the fixes.

- P01 2 PASS: both use `lumi_fb * 1000 * xsec_pb / sum`, the signed full-sample `genEventSumw`,
  and give RDataFrame/ROOT code (6 of 6 P01 runs since PR #99; before it 0 of 4).
- P02 2 PASS: both scripts executed on the synthetic TTree. Run 0 delivered two scripts; the main
  one prints 185 events, weights 107.00, and the other 185 events, sum of weights 107.00 and
  integral 108.00 over its 0-1000 GeV range (reference 108 and 184 for that range). Run 1 prints
  185 events and a weighted integral of 95.00 with sumw2 169.00 (the 0-500 GeV reference).
- P10 2 PASS: solar maximum, 1.2x margin, backtracing and demodulation in both runs (11/11
  runs with the correct solar epoch since the cycle-24 sentence).
- P08 1 PASS + 1 PARTIAL: run 0 gives flux (2.78 +2.7 -1.5)e-7, interval [1.37, 5.92] and
  spillover/background, but then says sqrt(3)/exposure/dR is 1.6e-8 "a factor of ~10" away, a
  wrong comparison. Run 1 gives only the script command with no numbers.
- P05 1 PASS + 1 PARTIAL: run 1 asks to confirm the m > 1 TeV region stays hidden; run 0 never
  mentions blinding.
- P03 2 PARTIAL (unchanged in every rerun today): both say to vary the jets and rerun the
  selection, but neither gives a yield-comparison check or mentions MET propagation.
- PASS: P04 (no signal-contamination point in either), P06, P07, P09, P11 (no skill loaded in
  either run, no number given), P12 (post-trial p 0.70, and 0.76/0.67), P13, P14, N01, N02.
- Open candidate: the "Scaling the final histogram" row in `SKILL.md` could add "check by comparing
  yields per cut, nominal against varied", which is the one E item P03 keeps missing.

## P01 units note and P08 run-the-script rule (2026-10-02, branch `hep-analysis-p01-p08-fixes`)

- Changes in `SKILL.md`: (1) the MC-normalization "Check first" row now says lumi in fb^-1 times
  xsec in pb needs a factor 1000 (`lumi_fb * 1000 * xsec_pb / sumw`) and to show RDataFrame code
  reading `genEventSumw` from `Runs`; (2) the sqrt(N) row now says to run
  `scripts/cosmic_ray_flux.py` (bin width in the exposure's units, e.g. 0.6 for 1.2-1.8 TV), quote its
  `flux`, `flux_lower` and `flux_upper`, and not to divide by hand; (3) working-procedure step 4 asks
  to run a bundled script when it computes the number asked for. `SkillUnitsAndScriptRulesTest`
  guards the wording, the factor, and the script's output for N = 3, exposure 1.8e7, dR 0.6 (flux
  2.7778e-7, interval 1.2660e-7 to 5.4799e-7). Tests 208 -> 213, bundle 119 files, description
  unchanged (1019 of 1024).
- Rerun `prompts_eval.py --model haiku --only P01 P08 --runs 4 -j 4`, $0.40:
  - **P01: 4/4 PASS.** All four use `lumi_fb * 1000 * xsec_pb / sum` with the signed full-sample
    `genEventSumw` and give RDataFrame/ROOT code (before: 0 of the last 4 had the factor, and none
    had code). Some explanatory sentences are still loose (for example "sum(|weights|) >> count"),
    which the rubric does not grade.
  - **P08: 2 PASS, 2 PARTIAL** (before: 0 PASS, 2 PARTIAL in the last rerun). Runs 1 and 3 give
    flux 2.78e-7, interval 1.27e-7 to 5.48e-7, asymmetric errors, units, spillover and background,
    all equal to the script's output. Run 2 still divides by hand and is a factor 10 too small
    (2.78e-8) while advising the script; run 0 gives only the command and the count interval. So
    the rule is followed by about half the runs. The result files do not record tool calls, so I
    cannot say whether the correct runs executed the script or computed the numbers right.
- Reading: the units note works (4/4 against 0/4); the run-the-script line helps but does not make
  Haiku reliable at P08 (2/4). 4 samples; no full rerun after this change.

## Full Haiku rerun on merged main, rule and cap in place (2026-10-02, branch `hep-analysis-rerun-after-cap`)

Follow-up to PR #98. `prompts_eval.py --model haiku --runs 2 -j 4`, 32 runs, $1.56, no errors, no
turn-limit run. **24 PASS, 8 PARTIAL, 0 FAIL.** Sequence of full reruns today: 24/8/0 (no change),
26/6/0 (cycle-24 sentence), 26/5/1 (run-before-deliver rule, one turn-limit run), 24/8/0 (rule plus
cap). All differences except the single FAIL are within the noise of 2 samples per prompt.

- P02 2 PASS: both scripts were executed on the synthetic 400-event TTree. Run 0 prints 185 events,
  sum of weights 107 (reference 107.0). Run 1 prints 185 events, weighted integral 108.00 and 184
  unweighted entries, which equals the reference for its 0-1000 GeV range (the one event above
  1000 GeV has weight -1). Each ran its own test first.
- P10: 1 PASS + 1 PARTIAL. The solar epoch is correct in both runs (9/9 since the cycle-24
  sentence), but run 0 states the cutoff geography backwards ("higher at the poles, lower at the
  equator"; the vertical cutoff is highest at the equator).
- PARTIAL x2 each, recurring: **P01** (both runs again use `lumi_fb * xsec_pb / sumw` with no
  fb-to-pb factor of 1000; one writes "fb^-1 * pb / sumw -> dimensionless"; 4 of the last 4 P01
  runs have this slip, and neither run shows RDataFrame code), **P03** (no per-cut yield check, as
  in every rerun), **P08** (run 0 quotes the flux a factor 10 too small, 2.78e-8 instead of
  2.78e-7, and a wrong sqrt(3) comparison; run 1 leaves dR symbolic; neither runs
  `scripts/cosmic_ray_flux.py`, which the answers only print as a command).
- P05: 1 PASS + 1 PARTIAL (run 1 never mentions masking the signal region).
- PASS: P04, P06, P07, P09, P11, P12, P13, P14, N01, N02. P11 loaded no skill in either run and gave
  no number (0/2 routed; 1/2 in an earlier rerun). P04 runs mention neither signal contamination
  nor a data validation region beyond closure.
- No effect of the rule or cap on any non-code prompt (same cost per run, $0.02-0.07).
- Not fixed, candidates: a units note in the "Check first" row for MC normalization (lumi in
  fb^-1 times xsec in pb needs 1000), and a line telling the model to run the skill's own script
  (`cosmic_ray_flux.py`) and quote its output instead of doing the arithmetic. Both change
  `SKILL.md` and need a decision.

## P02 run-before-deliver rule (2026-10-02, branch `hep-analysis-run-before-deliver`)

- Change: step 4 of the `SKILL.md` working procedure now begins "Run any code you deliver before
  delivering it": on the user's sample if there is one, otherwise on a small synthetic sample
  built with the stated branch names; compare a count or yield with a hand-computed expectation;
  show the cutflow it printed; if it could not be run, say so. `SkillRunBeforeDeliverTest` guards
  the wording and its position before "API selection". Tests 207 -> 208, all passing; bundle
  119 files; description unchanged (1019 of 1024).
- Rerun: `prompts_eval.py --model haiku --only P02 --runs 4`, $0.54 (before: $0.28). The scripts
  were executed on the same synthetic 400-event TTree as before (reference: 185 events with two
  selected jets, 169 and weighted integral 95.0 inside a 0-500 GeV histogram range):
  - run 3: built its own synthetic file, ran the script and reported the output. On my file it
    gives 185 events and integral 95.00, matching the reference. Its printed mean mass
    (263.18) is the weighted mean over all 185 events, which I had not computed at the time (corrected
    2026-10-02: it is right);
  - run 1: built test data and a logic test. Its script reads the tree `events`, so on a
    NanoAOD-style `Events` tree it fails with `KeyInFileError`; on a file with the tree renamed it
    gives 185 events and integral 95.00. Its summary says "All code is verified", which overstates
    it (the file-reading path had not been run on a real tree);
  - runs 0 and 2: no code. Each asked where the ROOT file is, or offered to build a synthetic
    example, with no script delivered. Defensible for a prompt with no file, but not what the rule
    asks.
- Compared with the previous P02 rerun (0/4 scripts ran at all): 1/4 runs end to end, 1/4 runs
  except for a tree-name assumption, 2/4 ask a question instead. With 4 samples this shows the
  rule changes behaviour, not that it is reliable. Not checked: whether the rule shifts other
  prompts (more questions, more cost); the full `tests/prompts.md` rerun is in the last bullet of this section.
- **Full 16-prompt Haiku rerun with the rule** (`prompts_eval.py --model haiku --runs 2 -j 4`, 32
  runs, $1.63; one run ended by `error_max_turns`): **26 PASS, 5 PARTIAL, 1 FAIL** (before the rule:
  26 / 6 / 0). Every hinted run loaded hep-analysis; `reads=0` throughout; per-run cost $0.02-0.06
  except the two P02 runs.
  - FAIL: P02 run 0 hit the 25-turn limit while writing and debugging its own tests and returned
    no answer. Its script (`dijet_mass_analysis.py`) is correct on a NanoAOD-style tree (185
    events, sum of weights 107.00, integral 95.00, as the reference), so this is a new failure
    mode of the rule: the model spends its turns executing code. The harness limit is 25 turns.
  - P02 run 1 PASS: delivered a script and a test, and on my synthetic file it gives 185 events
    and a weighted integral 74.0 over its 0-300 GeV range, matching the reference (74.0).
  - PARTIAL: P01 x2 (both use `lumi_fb * xsec_pb / sumw` with no fb-to-pb factor, a 1000x unit
    error; one then claims the sum of weights equals `lumi_fb * xsec_pb`), P03 x2 (no yield check;
    run 0 also cites invented `docs.anthropic.com` links), P08 run 0 (flux and errors a factor 10
    too small, 1.27e-8 for 1.27e-7).
  - PASS: P02 run 1, P04-P07, P08 run 1, P09-P14, N01, N02. P10 solar epoch correct 2/2 (7/7 since
    the cycle-24 sentence). P11 loaded no skill in both runs: run 0 asked for WebSearch permission
    and gave no number, run 1 gave no number and generic method text. P14 run 1 names a
    nonexistent `TUnfold::GetL_Lcurve()`.
  - Reading: the rule does not change the non-code prompts (same PASS pattern and cost), and it
    gets one working script from two P02 runs, against none before; the cost is one run that
    exhausted its turns. With 2 samples per prompt the 26/6/0 -> 26/5/1 difference is within
    noise except for that new failure, which is not.
- **Iteration cap added to the same step** ("Keep this to a few runs: if the same failure survives
  three fixes, stop, deliver the code with the failing output, and say it does not yet work";
  `SkillRunBeforeDeliverTest` checks it; tests still 208, bundle 119 files, description
  unchanged). Rerun `prompts_eval.py --model haiku --only P02 --runs 6 -j 6`, $0.97 ($0.12-0.21 per
  run): **0/6 hit the turn limit** (before the cap: 1/6 of the full-rerun runs, plus 1/2 P02 runs).
  All six delivered a script, a test-data generator and a tested summary. Executed on the
  synthetic 400-event TTree, all six give 185 events with two selected jets; five print sum of
  weights 107.00 or integral 95.00 exactly as the reference, and one (run 4) prints entries 185,
  sum(w) 95.000 inside its histogram range and a warning that it cannot write a ROOT file without
  ROOT, then lists the bins. No run reports a result it did not obtain.
- Limits of this evidence: no run needed to stop and report a failure, so the cap itself was not
  exercised; 0/6 against 1/6 is not significant, and the P02 prompt is the only one that executes
  code. The other 15 prompts were not rerun for the cap (a one-sentence addition to a step that
  does not affect text-only answers); the previous full rerun stands for them.

## P02 awkward leading-object rule (2026-10-02, branch `hep-analysis-p02-awkward`)

- Problem: in 2 of 4 earlier Haiku P02 runs the leading jets were picked with
  `jets.pt[ak.argsort(jets.pt, axis=1)[:, 0]]`, which in awkward selects *events* by position and
  returns whole events (verified: `[[50,40,30]] * 3` instead of `[50, 60, 90]`). Reference 02 has
  the right ordered pattern, but Haiku does not open references.
- Change: one rule in the `SKILL.md` API-selection section (order each event with the argsort
  applied to the array, cut with `ak.num`, then index `[:, 0]`, `[:, 1]`; never index with the
  argsort result), a matching "do not" paragraph and an `ak.argmax(..., keepdims=True)` option in
  reference 02, and `SkillAwkwardLeadingObjectTest` in `tests/test_reference_values.py` (checks the
  rule text and demonstrates the failure and the fix with awkward; skips without awkward).
  Tests 205 -> 207, all passing; bundle 119 files; description unchanged (1019 of 1024).
- Rerun: `prompts_eval.py --model haiku --only P02 --runs 4`, $0.28. **The banned pattern appears in
  0/4 scripts** (before: 2/4); all four order the array and index `[:, 0]`.
- **But none of the four scripts runs.** Each was executed on a synthetic 400-event TTree
  (185 events with two selected jets, mean mjj 250.004, sumw 107.0 as the reference):
  - run 0: `ak.Record({...})` instead of `ak.zip` -> `IndexError: scalar Record cannot be sliced`;
  - run 1: calls `ak.take`, which does not exist in awkward -> `AttributeError`; it also builds
    the selection with `ak.mask`, so `ak.num` would count rejected jets even if it ran;
  - run 2: the analysis is correct (185 events, as the reference) and it crashes only when writing
    the output histogram (`TypeError: ... tuple`);
  - run 3: `ak.num(record_array, axis=1) >= 2` -> `ValueError: cannot broadcast records`.
  None of these is the targeted bug. They are untested code written in an empty working directory.
- Consequence for earlier grades: P02 was graded by reading the script. Executing exposes runtime
  failures that reading missed, so earlier P02 PASS grades (here and in older passes) overstate
  correctness. Other code-writing prompts may be affected the same way.
- Not done: a rule to run the code on a small synthetic file before delivering it. It would
  address this whole class, but it changes the `SKILL.md` working procedure, so it needs a decision.

## P10 solar-epoch fix, rerun (2026-10-02, branch `hep-analysis-p10-cycle24`)

- Change: one sentence added to the astroparticle invariant in `SKILL.md` (the solar-modulation
  bullet): take the epoch's phase from the sunspot record; cycle 24 had its minimum in Dec 2008
  and a double maximum (Nov 2011 and 2012-mid 2013, smoothed peak Apr 2014), so 2011-2013 is
  solar maximum, not a declining phase. It restates reference 35 and links to it. The
  description is unchanged (1019 of 1024 characters).
- Rerun: `tests/prompts_eval.py --model haiku --only P10 --runs 3`, $0.14, `reads=0` on all
  three runs again. **Epoch correct 3/3** (before: 0/2, "minimum" and "declining"). **2 PASS +
  1 PARTIAL.** Run 0 PARTIAL: it applies the 1.2x margin to the orbit-averaged Stormer cutoff
  with no per-event backtracing, and says Voyager 1 crossed the termination shock in late 2012
  (the heliopause crossing was August 2012). Runs 1 and 2 PASS: 1.2x margin, backtracing, solar
  maximum, demodulate the ISS flux and label TOA versus LIS; run 2 gives phi ~800-900 MV.
- Three samples only; the Voyager slip in run 0 is a new, unrelated error, and the sample is too
  small to say it is rare. Tests and bundle validator unchanged and passing (119 files, 205
  tests, 12 skips).
- **Full 16-prompt Haiku rerun after the change** (`prompts_eval.py --model haiku --runs 2 -j 4`,
  32 runs, $1.52, no errors; every hinted run loaded hep-analysis, and `reads=0` except one P04
  run that read one reference): **26 PASS, 6 PARTIAL, 0 FAIL** (before the change: 24 / 8 / 0).
  - PASS x2: P03, P04, P06, P07, P09, P11, P13, P14, N01, N02. P11 run 1 routed to
    `ams-analysis` (reads=4) and gave a sourced, dated antiproton result; run 0 loaded no skill and
    gave no number.
  - P01 PASS + PARTIAL: run 1 gives the right signed full-sample denominator but no RDataFrame
    code beyond prose.
  - P02 PASS + PARTIAL: run 0 masks first and indexes `[:, 0]`, `[:, 1]` with sumw2. Run 1 repeats
    the awkward bug `selected_pt[pt_argsort[:, 0]]`, which selects events, not jets.
  - P05 PASS + PARTIAL: run 1 says the observed SR values are set to NaN; run 0 offers a masked
    template with no explicit refusal.
  - P08 PASS + PARTIAL: both reject sqrt(N) and give [1.37, 5.92]. Run 1 then divides by 1.08e7
    and quotes 1.27e-8 and 5.48e-8; the correct values are 1.27e-7 and 5.48e-7 (a 10x
    arithmetic error).
  - P10 PASS + PARTIAL: **both runs say 2011-2013 is solar maximum.** Run 0 (PASS) has the 1.2x
    margin, a backtracing alternative and phi ~600-700 MV. Run 1 (PARTIAL) omits the 1.2x margin.
  - P12 PASS + PARTIAL: run 0 has 2.74 sigma and a post-trial p of 0.76 (exact 0.71). Run 1 gets
    2.67 sigma from a rounded logarithm, p_global 0.80, and calls a global p of 0.8 "a deficit".
  - Across all five P10 runs after the change the epoch is correct 5/5 (before: 0/2). Haiku's
    arithmetic slips (P08 run 1, P12 run 1, earlier P01) vary from run to run and are not tied to
    this change. With 2 samples per prompt, 24/8/0 against 26/6/0 is within noise: it shows no
    regression but does not show that the sentence helps anywhere except P10.

## Haiku prompts.md rerun, unchanged SKILL.md (2026-10-02, branch `hep-analysis-prompts-rerun`)

Recurring check. `python3 tests/prompts_eval.py --model haiku --runs 2 -j 4`, 16 prompts x 2 runs,
one fresh `claude -p` child each, reported cost $1.41. P01-P10 and P12-P14 get the "load
hep-analysis" hint; P11, N01 and N02 route on their own. No file under `references/` or
`SKILL.md` changed since the 2026-09-28 run. **32 runs: 24 PASS, 8 PARTIAL, 0 FAIL.** Every
hinted run loaded hep-analysis and none opened a reference (`reads=0`), so behaviour comes from
`SKILL.md` alone. The no-hint controls: N01 and N02 loaded no skill (correct); P11 also loaded no
skill (it did not route to `ams-analysis`) but gave no "latest" number and pointed to INSPIRE and
arXiv, so it meets E1.

| Prompt | Runs | Notes |
|---|---|---|
| P01 | PARTIAL, PASS | Run 0 used `138 fb^-1 * 833.9 pb / sumw` with no fb-to-pb factor, a 1000x unit error; run 1 used 138e3. Both correctly use the signed `genEventSumw` over the full sample. Neither shows weighted per-cut sums (graded as not part of the question) |
| P02 | PARTIAL, PARTIAL | Run 0 picks the leading jets with `jet_pt_sel[sorted_idx[:, 0]]`; in awkward that selects whole events, not jets (verified: every event returns the first event's jets), so the mass is wrong. Run 1 masks first and indexes `[:, 0]`, `[:, 1]` correctly but stores no sumw2 |
| P03 | PARTIAL, PASS | Both say to vary the jets and rerun the selection. Only run 1 gives the yield-comparison check and mentions MET |
| P04 | PASS, PASS | Both investigate the correlation and prefer a closure-derived correction. Neither mentions signal contamination in B/C/D |
| P05 | PARTIAL, PASS | Neither wrote code (empty directory). Run 1 states the SR data would be set to NaN; run 0 offers a masked plot without an explicit refusal |
| P06, P07 | PASS x4 | Overlap named and fixed; the prior change declined with pulls/impacts/GOF/CR offered |
| P08 | PASS, PARTIAL | Both reject sqrt(N) and give [1.37, 5.92]. Run 0 also gives the flux and errors (2.78e-7, -1.51e-7, +2.70e-7 per m^2 sr s TV, checked). Run 1 left dR symbolic and did not use the stated 1.2-1.8 TV bin |
| P09 | PASS x2 | Shared systematics cancel, charge confusion stays |
| P10 | PARTIAL, PARTIAL | Both give the 1.2x safety factor, a backtraced cutoff and demodulation of only the ISS flux. Both get the epoch wrong: run 0 calls 2011-2013 "post-solar-max" and "minimum", run 1 "minimum -> maximum -> minimum". Reference 35 has it right (rising to the April 2014 maximum), but Haiku did not open it |
| P11 | PASS x2 | No "latest" number. Run 1 adds generic method text that is unsourced and partly wrong (a TRD charge sign) |
| P12 | PASS x2 | Both 2.74 sigma and a post-trial p of 0.7 (run 0 wrote 0.68, an arithmetic slip; exact 0.71) |
| P13, P14 | PASS x4 | Model dependence, sigma(Xmax), muons; objective tau plus closure. P14 run 0 has wrong TUnfold code and claims native GCV support |
| N01, N02 | PASS x4 | No HEP content, no hep-analysis load |

Compared with 2026-09-28 (round 5: 0 FAIL, P08 2 PASS + 1 PARTIAL): still 0 FAIL, P08 1 PASS +
1 PARTIAL. P10 is the one change worth acting on: round 3 had P10 2/2 PASS because Haiku read the
cycle-24 paragraph; with `reads=0` it falls back to its own wrong epoch. The fix, if wanted, is one
line in the `SKILL.md` astroparticle invariant (cycle 24: minimum Dec 2008, maximum Apr 2014, so
2011-2013 is the rising phase near maximum). Not applied: it changes `SKILL.md`, which the TODO
says to ask about first. Counts unchanged: 119 files, 205 tests, 12 skips.

## AMS-02 numbers checked against Phys. Rept. 894 (2026-10-02, branch `hep-analysis-ams-physrep`)

- Source: the text of the publisher PDF (a local copy of Aguilar et al., Phys. Rept. 894 (2021)
  1-116, extracted to the scratchpad; the PDF is not added to the repository).
- Every subsystem claim named in the ref 13 AMS row was confirmed: RICH radiator (16 NaF tiles
  n = 1.33 + 92 aerogel tiles n = 1.05; beta thresholds 0.75 and 0.953), ACC (16 curved
  scintillator panels, tested efficiency 0.99999), tracker (9 layers, 5-10 um bending-plane
  resolution, proton MDR 2.0 TV), ECAL (17 X0, ~200 um and 0.3 degree at 1 TeV), magnet 1.4 kG.
- ECAL energy resolution: only in Fig. 28, no number in the text, so not quoted.
- Reference 38 still keeps no AMS numbers on purpose (they belong to `ams-analysis`); only the
  ref 13 source row and the status item changed. A stale "reference 40" in that row (the AMS
  case study is reference 38) was fixed.
- The numbers describe the pre-Layer-0 instrument.

## Fifth query set built, not run (2026-10-02, branch `hep-analysis-queryset5`)

- `tests/trigger_queries_task.json`: 40 cases, none duplicating the 160 in the other four sets.
  Style differs from the earlier sets (conceptual, formula, numeric): task-style requests with
  pasted datacards, error messages, review and write-a-script asks. Positives: 7 collider,
  7 space/cosmic-ray direct detection, 6 IACT/neutrino/air-shower (the user's equal-weight
  rule). Four space cases are AMS-style and carry `also_ok: ["ams-analysis"]`. Negatives: 8
  non-HEP with HEP-like vocabulary (root, weights, unfolding, Monte Carlo, broken power law) and
  12 sibling near-misses with `owner` set (3 ams-analysis, 3 deep-learning, 3 academic-papers,
  2 academic-diagrams, 1 task-authoring).
- Deliberately **not run**: running it now would spend it. No model results exist for it; it is
  reserved as the deciding set for the next proposed description change.
- Bundle validator `REQUIRED_PATHS` and README updated (118 -> 119 files).

## Ref 13 caveat follow-up (2026-10-02, branch `hep-analysis-ref13-caveats`)

- Full texts read for the IACT energy scale. CTA (arXiv:1508.07225): requirement <10% on the
  energy scale, baseline calibration methods ~15%. The earlier note "CTA calibration target
  ~15%" was wrong and is corrected in ref 13. VERITAS (arXiv:2111.04676): ~25% on the absolute
  flux for an index-2.5 source, no separate energy-scale percentage, so "up to ~20% for
  VERITAS" was unconfirmed. H.E.S.S. (arXiv:2403.12608): no single energy-scale percentage, ~10%
  residual atmospheric-transparency variation. Ref 33 now quotes these figures (range ~10-20%
  kept as an order of magnitude, checked 2026-10-02).
- Phys. Rept. 894 not read (publisher paywall). Ref 38 quotes no numeric instrument parameters
  beyond the Layer-0 status; the website-only subsystem numbers are in the ref 13 AMS row.
  Still open.

## Ref 13 latest-results re-check (2026-10-02, branch `hep-analysis-ref13-recheck`)

- PDG 2026 still current (pdg.lbl.gov). PDG 2026 cosmic-ray review text re-read: knee/second
  knee/ankle/instep/suppression values match reference 30 (revised March 2026).
- AMS Layer-0 (ref 38): CERN item of 2026-08-21 and the tracker page re-opened; Layer-0 not
  installed, schedule unchanged (Perugia to 30 Aug, CERN October, KSC January 2027, launch
  April 2027, connections May 2027).
- IACT energy scale (ref 33): MAGIC abstract (arXiv:1508.04575) says <15%. The CTA abstract
  (arXiv:1508.07225) gives no number, so the CTA ~15% target is unconfirmed; H.E.S.S. and
  VERITAS not re-opened. No reference text changed; only check dates and this caveat.
- Not re-checked: Phys. Rept. 894 against AMS instrument parameters (still open).

## TODO round 6: formula recall on a fourth set, TOF-mass routing (2026-09-28, branch `hep-analysis-todo-round6`)

- **Fourth fresh query set `tests/trigger_queries_calc.json`.** It has 20 quick calculations
  (detector, collider, statistics, astroparticle) and 20 negatives: 12 non-HEP calculations and
  8 owned by sibling skills. None of these queries was used to write the variant tested here.
- **One description variant tested:** "including quick calculations, formula lookups, how-to or
  conceptual questions" (1012 characters). To make room, it dropped "RooStats/" and "/data-driven".
  Isolated `routing_eval.py`, Haiku, 2 runs per query, two repetitions each:

  | Description | Recall | False triggers |
  |---|---|---|
  | current (round 5) | 35/40, 30/40 (65/80) | 0/80 |
  | variant | 35/40, 35/40 (70/80) | 0/80 |

  - **Not adopted.** The +5/80 is no larger than the spread between the two baseline repetitions
    (35 vs 30), and the variant removes keywords (RooStats, data-driven) that other queries
    rely on. The round-5 description stays. No further description tuning is planned; the
    wording change alone no longer shows a measurable effect.
  - Residual Haiku misses (both descriptions): the tracker sagitta calculation (8/8 runs missed),
    photon conversion probability, impact-parameter resolution, carbon rigidity per nucleon,
    integral proton flux, and the ttbar event count. These are self-contained arithmetic that
    Haiku answers directly.
  - Sibling misses seen in passing (not hep-analysis): deep-learning (GPU-hours, VAE KL) and
    agile-development (story points) got no skill 4/4. The Metropolis-Hastings flowchart went to
    the built-in `dataviz` and the prompt token budget went to `claude-api` (4/4 each).
- **TOF-mass routing decision.** The formula-set query "Mass from TOF and rigidity: m = R Z
  sqrt(1/beta^2 - 1) ..." went to ams-analysis in 4/4 Sonnet runs. Two detector-agnostic rewordings
  of the same physics went to hep-analysis in 4/4 runs each, and an AMS RICH control went to
  ams-analysis in 4/4. The trigger is AMS vocabulary: ams-analysis lists "rigidity/charge/velocity/mass
  observables". **Judged acceptable:** that case now has `also_ok: ["ams-analysis"]`. It is not a
  hep-analysis gap, because generic wording routes to hep-analysis.
- Tests: 205 OK (12 skips). Bundle OK (118 files).

## TODO round 5: Haiku prompt rerun, formula-lookup triggering (2026-09-28, branch `hep-analysis-todo-round5`)

- **New harness `tests/prompts_eval.py`.** It runs `tests/prompts.md` through real `claude -p`
  children (Claude Code, `--setting-sources project`, the seven repo skills symlinked as project
  skills as in `routing_eval.py`). Each run gets its own directory. P01-P10 and P12-P14 get the hint
  "Load the hep-analysis skill"; P11, N01 and N02 route on their own. The hep-analysis skill
  loaded in every hinted run, but Haiku opened a reference file in only 1 of 26 hinted runs. It
  answered from SKILL.md alone. Earlier passes used Agent-tool subagents, so this
  harness is stricter: guidance that lives only in a reference is invisible to Haiku.
- **Run A, current SKILL.md, Haiku, 2 runs each (P01-P14, 28 runs): 16 PASS, 8 PARTIAL, 4 FAIL.**
  - FAIL: P08 2/2 ("Yes, your formula is correct" for sqrt(3), although the flux invariant says
    to answer no); P01 once (normalized by the sum of |genWeight|); P05 once (asked whether to
    "mask entirely, or overlay it with a band/hatching").
  - PARTIAL: P01 (signed sum but over the skimmed sample), P03 (no check), P05 (no clear refusal),
    P10 2/2 (no backtracing, no 1.2x factor), P12 2/2 (a sqrt(ln N) heuristic and a wrong
    expected count; no correlated-trials caveat), P13 (mean only).
  - PASS: P02, P04, P06, P07, P09, P11 (routed to ams-analysis, dated sources), P14 2/2.
    N01 and N02 did not load hep-analysis (N02 loaded deep-learning once).
- **Fix 1: a "Check first" table at the top of SKILL.md.** Each row restates an existing
  invariant as the correction to a user proposal (normalization, sqrt(N), blinded plots, JES
  scaling, prior widening, ratio quadrature, scan trials, tau by agreement). The weight
  invariant now says "before any skim" and "not the sum of absolute weights". No physics change.
- **Run B, same prompts after fix 1: 21 PASS, 7 PARTIAL, 0 FAIL.** P08 now says no and names
  the script, spillover and background, but does not compute the interval (2 PARTIAL). P05 2/2
  PASS (NaN mask stated up front). P01 1 PASS, and 1 PARTIAL whose Runs-tree loop sums into its own
  branch buffer (a code bug). P10 2 PARTIAL, P13 2 PARTIAL, P12 1 PARTIAL. No regression elsewhere.
- **Fix 2: invariants.** The cutoff invariant now asks for a 1.2x safety factor over a backtraced
  cutoff (Stormer is only a planning estimate). The composition invariant now asks for more than one
  hadronic model and sigma(X_max). Both come from refs 35 and 31.
  - Rerun: P10 2/2 PASS and P13 2/2 PASS. One P13 run said protons have the *narrower*
    X_max distribution (reversed), so the invariant now gives the direction (protons fluctuate
    most, ~1/sqrt(A)). The P13 rerun after that is 2/2 PASS with the correct direction.
  - P08 2/2 PARTIAL, unchanged: no F signal, but the interval is still not computed.
- Total reported cost for the prompt runs: about $3.70.
- **Formula-lookup triggering (optional TODO item).** New third query set
  `tests/trigger_queries_formula.json` has 20 quick formula/number lookups across collider,
  detector and astroparticle topics. It also has 20 negatives: 12 unrelated physics, maths or coding
  formulas, and 8 owned by sibling skills (3 deep-learning, 3 ams-analysis, 1 academic-papers,
  1 academic-diagrams). It was not used to write the change.
  Only one description variant was tried on it, so it stays a fair test.
  - Description change (1018 -> 1019 characters): "quick formula lookups, how-to or conceptual
    questions"; "Detector subsystems and resolutions". To make room: "pipelines" and
    "/root-config" dropped, "incl." and "and" dropped.
  - Isolated `routing_eval.py`, 2 runs per query:

  | Set | Model | Before | After |
  |---|---|---|---|
  | formula (recall) | Haiku | 26/40, 22/40 (48/80) | 29/40, 29/40 (58/80) |
  | formula (false triggers) | Haiku | 0/40, 0/40 | 0/40, 2/40 (AMS tracker resolution, 1/2 runs each time) |
  | held-out (recall / FP) | Haiku | 34/40, 34/40 / 1, 0 | 34/40 / 0/40 |
  | tuning (recall / FP) | Haiku | 37/40 / 1/40 (round 4) | 39/40 / 1/40 |
  | formula (recall / FP) | Sonnet | not run | 35/40 / 0/40 |

  - A gain of about +10 runs out of 80 on formula lookups, with no loss on the held-out or tuning sets.
    Haiku still skips the skill for self-contained numeric questions: calorimeter resolution
    (0/4 after), Cherenkov angle in C4F10, photoelectron yield, TOF pi/K reach. Sonnet sent the
    TOF-plus-rigidity mass question to ams-analysis 2/2. In the second "after" Haiku formula run, 8 negative runs
    errored (a usage limit was hit mid-run). They were rerun once and are counted in the table (0/8 false triggers).
- Tests: 204 OK (12 skips). Bundle OK (117 files).
- **P08 follow-up (same day).** The check-first row now gives the exact `cosmic_ray_flux.py` command:
  in run B one run had invented a `--cl` flag. SKILL.md also has a table of exact 68.27% Garwood
  intervals for N = 0-10, computed with `scipy.stats.chi2` and matching `poisson_interval`.
  A new test (`SkillGarwoodTableTest` in `tests/test_reference_values.py`) keeps the table in sync with
  the script. A mutation check confirmed that it fails on a wrong value. P08 on Haiku, 3 runs: **2 PASS**
  (the interval [1.37, 5.92] counts, the flux [1.27, 5.48]e-7 (m^2 sr s TV)^-1, spillover and background),
  plus **1 PARTIAL** (it gave the interval but opened with "Yes, structurally that's right"). No FAIL. Tests: 205 OK (12 skips).

## Harness update (2026-09-27, during academic-papers round 1)

`tests/routing_eval.py` gained `--target <skill>` (recall and false triggers for any of
the seven repo skills; a case's `expect_target` field falls back to
`expect_hep_analysis`). Runs that end in an error before choosing a skill, and runs
whose result is the CLI's usage/spend-limit notice (returned as an ordinary result),
are now excluded from the counts and reported with a warning. Before this, a
usage-limited run counted as "no skill", which made recall look like 0. The
hep-analysis results recorded below were not affected: they have no errored runs.

## TODO round 4: isolated routing harness, held-out trigger set, Sonnet rerun (2026-09-26, branch `hep-analysis-todo-round3`)

- **Description change.** The mention of the "AMS-02 case study" was dropped from the topic
  list, and the negative clause now reads "Not for AMS-02-specific analyses (use ams-analysis)
  or unrelated 'root' (Linux/Android, certs)". The three "Also" connectors were removed to
  make room. Length is 1018 of 1024 characters. The bundle validator and all 204 tests pass.
- **Isolated sibling-routing harness: `tests/routing_eval.py`.** It runs each query through a
  real `claude -p` child (Claude Code 2.1.283) with `--setting-sources project`. The seven repo
  skills are symlinked into the child's project `.claude/skills/`, and the child is killed at
  its first Skill call. When asked to list its skills, the isolated child named exactly 19: the
  7 repo skills plus 12 built-ins, and none of the ~112 user skills or plugins. This fixes the
  `claude plugin eval` problem, where plugin skills were listed without descriptions.
  Skills are loaded as project skills, not with `--plugin-dir`. The earlier session that wrote
  the harness found that namespaced plugin entries triggered on Haiku in only 2 of 6 runs, against
  5 of 6 as project skills. That comparison was not rerun here.
- **New held-out trigger set, never used for tuning: `tests/trigger_queries_holdout.json`.**
  It has 20 should-trigger queries, balanced across collider, detector and astroparticle, and
  20 should-not-trigger queries. The negatives are 13 owned by sibling skills (3 deep-learning,
  3 ams-analysis, 3 academic-papers, 2 academic-diagrams, 1 task-authoring,
  1 agile-development) and 7 unrelated. Each case records its owner skill.
- **Results, 2 runs per query, all through the isolated harness.** Reported cost was about
  $2.60. Runs killed at their Skill call report no cost, so that figure is a lower bound.

  | Set | Model | hep-analysis recall | hep-analysis false triggers | Routed to owner |
  |---|---|---|---|---|
  | held-out | Haiku | 34/40 | 1/40 | 56/80 |
  | held-out | Sonnet | 40/40 | 0/40 | 73/80 |
  | tuning (`trigger_queries.json`) | Haiku | 37/40 | 1/40 | n/a (no owner field) |
  | tuning | Sonnet | 40/40 | 0/40 | n/a |

  - Haiku's held-out misses were all quick formula or conceptual detector and astroparticle
    questions, where it answered with no skill loaded: the Highland formula (2/2 runs), the
    calorimeter constant-term crossover (2/2), the force-field approximation (1/2) and the
    Cherenkov threshold (1/2). Held-out recall (34/40) is 3 runs lower than tuning-set
    recall (37/40), so the description generalizes, with a small gap on formula lookups.
    **Not tuned:** tuning on these misses would use up the held-out set. A further change needs
    a third fresh set, and the description has only 6 characters of headroom.
  - False triggers: Haiku routed "GNN for jet tagging overfits" to hep-analysis in 1 of 2 runs
    (owner: deep-learning), and on the tuning set routed "Design the AMS-02 antideuteron search
    selection" to hep-analysis in 1 of 2 runs (owner: ams-analysis). With `ams-analysis` now
    loaded beside it, the AMS false triggers from the round-3 `claude plugin eval` (3-5 of 40)
    fell to 1 of 40.
  - Routing misses that belong to sibling skills: in most of the 24 Haiku and 7 Sonnet misses, no
    skill was invoked at all, and the model answered directly. The affected skills were:
    academic-papers (BibTeX from INSPIRE and a paper critique, both models), academic-diagrams
    (Mermaid to SVG, both models), agile-development (sprint planning, both models), and on
    Haiku also deep-learning (3 queries) and academic-diagrams TikZ. Once, Haiku picked the
    built-in `dataviz` skill. These are findings about the sibling skills' descriptions, not
    hep-analysis, and were left for their own TODO lists.
  - Sonnet: no recall or false-trigger regression on either set after the description change,
    which closes the "rerun Sonnet" follow-up.

## TODO round 3: Combine, ACLiC, P08, Haiku trigger recall (2026-09-25, branch `hep-analysis-todo-round3`)

- **Combine datacard verified** (user allowed a scratch build). Built Combine from
  `cms-analysis/HiggsAnalysis-CombinedLimit` (commit db20e4d, v11.0.0) with CMake in a scratch
  conda-forge env (ROOT 6.34.10, boost, eigen, gsl, `-DUSE_VDT=OFF`). Nothing was installed system-wide.
  - Filled `assets/combine_datacard_template.txt` with the `pyhf-counting.json` model (s=5, b=20,
    n=20, background lnN 0.9/1.1) and a one-bin shapes file. `text2workspace.py` + `combine -M
    AsymptoticLimits`: observed r < 2.157; expected 2.5/16/50/84/97.5% = 1.112/1.512/2.156/3.128/4.373.
  - pyhf 0.7.6 on `pyhf-counting.json`, rerun: observed 2.153; expected -2..+2 sigma =
    1.097/1.503/2.153/3.129/4.419. Every band agrees within 1% (lnN vs normsys interpolation).
  - **Correction to the P1 record:** "expected 1.50" there was the -1 sigma band. The median is 2.153.
  - A shape nuisance (`bkg_shape shape - 1` with +-10% Up/Down histograms) exercises the template's
    `$CHANNEL/$PROCESS_$SYSTEMATIC` pattern and gives r < 2.157.
  - New `tests/test_combine_template.py`: placeholder set and column-consistency checks always run.
    The Combine run is skipped unless `combine` is on PATH or `HEP_COMBINE_WRAPPER` is set; it
    passed here with a wrapper that runs `env -i` in the scratch env.
- **Root cause of the macOS rootcling/ACLiC failures found.** The user's `~/.zshrc` exports
  `ROOT_INCLUDE_PATH=<Xcode SDK>/usr/include/c++/v1` and sources Homebrew's `thisroot.sh`
  (`ROOTSYS`, `PYTHONPATH`, `LD_LIBRARY_PATH` and `CMAKE_PREFIX_PATH` all point at Homebrew ROOT).
  A different ROOT's cling then picks up a mismatched libc++. For any second ROOT, run in a clean
  environment (`env -i`).
  - Homebrew ROOT 6.38 ACLiC still fails with or without that variable: its `rootcling` gets
    `-isysroot` CLT MacOSX26.sdk together with the Xcode libc++ path, and without the variable its
    `std_darwin.modulemap` headers are missing. Unchanged from the earlier diagnosis.
  - **`plot_branch.C+` verified with ACLiC on conda-forge ROOT 6.34.10** (clean env). It compiles,
    runs on the fixture `events.root`, and its `h_pt` is bin-identical to the interpreted run
    (5000 entries, mean 18.910).
- **P08 (Haiku + skill; one fresh agent and output directory per run; scripts allowed; 350-word cap)**
  - Round A (no skill change, script execution allowed): **2/2 FAIL**. Both ran
    `cosmic_ray_flux.py` and gave the exact interval [1.367, 5.918] with asymmetric errors, but both
    called `sqrt(3)` "correct/reasonable as a Gaussian approximation" (the F signal). Neither
    mentioned resolution/spillover or background. The runs read SKILL.md and ref 37 but never ref
    35, where the low-count subsection lives. Running scripts fixed the missing numbers; routing
    was the remaining gap.
  - Fix: the SKILL.md flux invariant now says to answer "no" (not "approximately right"), to run
    `cosmic_ray_flux.py`, and to address spillover and background, with a link to ref 35's
    low-count subsection. Ref 37's intro links there too.
  - Round B: **2/2 PASS**. Both said no, used 600 GV, gave [1.27, 5.48]e-10 (m^2 sr s GV)^-1 from
    the script, and covered MDR/resolution spillover and background.
  - Regression check after the invariant/ref 37 edit, run twice each: **P09 2/2 PASS; P10 1 PASS +
    1 PARTIAL** (one run gave backtracing but no 1.2x factor); **P12 1 PASS + 1 PARTIAL** (one run
    assumed independent trials with no correlated-trials caveat). The PARTIALs concern content
    the edit did not touch. No FAIL. The other prompts were not rerun: they do not route through
    refs 35/37 or the flux invariant.
- **Haiku trigger recall: description revised; eval suite committed in `evals/`** (40 cases built from
  `tests/trigger_queries.json`: a `tool_used: Skill` grader, min 1 for should-trigger and 0..0
  otherwise, max_turns 6). `claude plugin eval`, target mode (only hep-analysis loaded), Haiku,
  2 runs per case:

  | Description | Recall (runs) | False triggers (runs) | Cost |
  |---|---|---|---|
  | previous | 22/40 | 3/40 | $2.73 |
  | revised | 38/40 | 5/40 | $3.24 |

  - The revision opens with "including quick how-to or conceptual questions - load it before
    answering from memory". It adds ABCD/data-driven backgrounds, Combine impacts/datacards,
    crashes, X_max and neutrino effective area, and drops the two example quotes. It is 1024 characters.
  - Revised misses: pos12 Li & Ma (1/2) and pos14 pyhf workspace (1/2, the miss hit the turn cap).
  - Revised false triggers: neg12 Feynman/TikZ (1/2, same as before) and neg19 AMS antideuteron
    (2/2, same as before). New ones: neg06 physics-informed-NN DDP (1/2) and neg10 AMS positron
    fraction (1/2). All four belong to a sibling (academic-diagrams, ams-analysis, deep-learning)
    that target mode does not load.
  - **Sibling routing.** A plugin with all seven repo skills is not a valid harness test here. The
    eval child also loads the user's ~112 other skills, and the listing then shows plugin skills
    as bare names with no description (Haiku confirmed this when asked to echo the listing).
    Recall collapsed to 3/40 (previous) and 1/40 (revised), for reasons unrelated to the
    descriptions. Routing was therefore checked by simulation: Haiku was given all seven real
    descriptions and routed the 40 queries, 2 runs per variant. Previous: 20/20 recall and 0/20
    hep false triggers in both runs. Revised: 19/20 and 20/20 recall, 0/20 false triggers. Every
    near-miss went to its owner (deep-learning, ams-analysis, academic-papers/diagrams,
    task-authoring). The one revised miss sent the balloon-cutoff query to ams-analysis.
  - Caveats: 2 runs per case, and Haiku is noisy. The suite reuses the same 40 queries, so it
    shows the change helps on them, not that it generalizes.
- Tests: 204 OK (12 skips; the Combine test ran with the wrapper). Bundle OK (113 files).

## Follow-up pass (2026-09-25, branch `hep-analysis-followups`)

- **Examples removed.** Commit 86104f1 deleted `examples/`. That broke the bundle validator
  (25 missing `REQUIRED_PATHS`) and left a dead link in `SKILL.md`. Both references are now
  removed. The routing row that sends example authoring to `task-authoring` stays.
  Bundle OK (112 files); 201 tests pass (11 skips).
- **Latest-results live check** (`references/13-sources.md`). This is the first live check;
  the 2026-09-24 pass was from knowledge only.
  - PDG links moved from the 2025 to the 2026 edition; all four PDFs resolve.
  - Reference 30 corrected against the PDG 2026 cosmic-ray review (revised March 2026):
    - knee: `gamma` ~2.7 -> ~3 (was 3.1);
    - second knee: ~100 PeV, `gamma` -> ~3.3 (added);
    - ankle: ~5 EeV, `gamma` -> ~2.5 (was 5-8 EeV, 2.6);
    - instep and a ~50 EeV suppression added.
  - PDG words the instep as a "flattening". The Auger paper it cites (PRL 125 (2020)
    121106: 2.51 -> 3.05 at 13 EeV) shows a steepening, and reference 30 follows Auger.
  - IACT energy scale (reference 33): "~15-20%" changed to "~10-20%" (H.E.S.S./MAGIC ~10-15%,
    VERITAS ~20%).
  - AMS-02 (reference 38): the Layer-0 tracker upgrade is qualified but not yet installed.
    Its schedule (launch end of 2026, done by about May 2027) comes from secondary sources
    only, so it is flagged for a re-check.
- **ACLiC** still fails, now diagnosed. ROOT 6.38.04 (Homebrew) pairs
  `-isysroot .../CommandLineTools/SDKs/MacOSX26.sdk` with a hard-coded Xcode
  `.../MacOSX.sdk/usr/include/c++/v1`, and the mixed libc++/libc headers crash `rootcling`
  even for an empty macro. Setting `SDKROOT` (CLT 26 or default) or
  `DEVELOPER_DIR=CommandLineTools` still ends in a bus error or segfault. The path is baked
  into the Homebrew build. The fix is a ROOT rebuild or a different machine, not the macro.
- **Haiku + skill re-run of `tests/prompts.md`** (P01-P14, one fresh agent each). This run
  came after the examples were removed and after the SKILL.md invariants were regrouped
  under headings.
  - PASS: P02, P03, P04, P06, P09, P11, P12, P13, P14.
  - PARTIAL:
    - P01: correct denominator and signed weights, but no RDataFrame/`Runs`-tree code.
    - P08: exact interval correct ([1.37, 5.92] counts), but no units and no
      resolution note, as before.
    - P10: Stormer estimate only, with no cutoff safety factor or backtracing.
  - **FAIL:**
    - P05: the data/MC script plotted every observed point, including m > 1 TeV. A
      red box drawn *behind* the points was called "masking".
    - P07: it wrote the 5% -> 30% ttbar prior change into the datacard without
      challenge.
  - In the 2026-09-24 run both passed, so either the failure is sampling noise or the
    guidance was too weak for Haiku. Fixes:
    - `SKILL.md` blinding invariant and `references/01`: a mask removes observed values
      (NaN, dropped, or never read); shading is not masking.
    - `SKILL.md` no-tuning invariant: now names nuisance prior/constraint widths,
      parameter bounds and dropped nuisances, says not to write such a change on
      request, and lists the alternatives.
  - Reruns after the fixes, 2 per prompt:
    - P07 2/2 PASS: declined, explained the bias, offered pulls/impacts, a GoF test and
      a CR constraint.
    - P05 1 PASS (bins set to NaN before the ratio and plot) and 1 PARTIAL. The
      PARTIAL run's own script masked correctly, but it wrote into the shared scratch
      directory and offered the first run's leaky script as the real-data template.
      That is contamination from the test setup, not a skill failure.
  - Caveat: one run per prompt, graded by one judge. Haiku is noisy at this sample size.
- **Harness trigger eval** (`claude plugin eval`, Claude Code 2.1.282). The 40 queries in
  `tests/trigger_queries.json` became cases with a `tool_used: Skill` grader: at least one
  call for should-trigger, `min: 0, max: 0` otherwise. The suite was run from a scratch copy
  of the skill (with-arm only, 1 run each) and was not committed.
  - Only `hep-analysis` is loaded in the eval child; the siblings are not.
  - Haiku ($1.30): recall 12/20 (pos14 invoked the skill but hit the 6-turn cap), false
    triggers 1/20. The one false trigger is the AMS antideuteron design query, and
    `ams-analysis` was not available to take it. The recall misses:
    - JER->MET, knee/ankle, Gaisser-Hillas X_max, PyROOT segfault, RICH pi/K, ABCD;
    - CMake+RDataFrame (hit the turn cap), Combine impacts, IceCube effective area.
  - Haiku answered these from its own knowledge without loading the skill. The simulated
    P2 trigger test (20/20, 0/20) overstated recall on Haiku.
  - Sonnet ($4.43, 12-turn cap): recall 20/20, false triggers 2/20. Both false triggers are
    AMS queries (the latest positron fraction and the antideuteron design) that go to
    `ams-analysis` when it is installed.
  - Conclusion: the description works on Sonnet. The Haiku recall gap is Haiku preferring
    to answer from its own knowledge, so the description was left unchanged. A
    sibling-routing check under the harness needs a suite that loads all repo skills,
    which this target mode does not do.
- **P01/P08/P10 Haiku PARTIALs: reference fixes and reruns** (Haiku + skill, one fresh
  agent and one output directory per run, prompt text only, ~220-word cap, graded by one judge).
  The worked numbers added to the references differ from the test prompts, so the answers
  are not copied.
  - P01 (ref 03 never mentioned the NanoAOD `Runs` tree or skims). Added a PyROOT
    RDataFrame snippet: denominator from `Runs`/`genEventSumw` over every file, signed
    weights, and an N/sumw/sumw2 cutflow. The snippet was run on synthetic skimmed files,
    including one where the skim kept 0 events. Reruns: **2/2 PASS**; both used the
    `Runs` tree, with no `abs`.
  - P10, round 1 (ref 35 had the 1.2 safety factor only inside the walkthrough). Added a
    cutoff selection rule to the main section: backtraced maximum cutoff over the
    acceptance, with the same rule for events and exposure. Result: 1 PASS, 1 PARTIAL.
    The PARTIAL run copied the walkthrough's Störmer-first framing, so the walkthrough
    step now leads with the backtraced cutoff.
  - P10, round 2: 2/2 met E1/E2. Both runs called 2011-2013 "declining", and one said to
    demodulate the Voyager data too. The reference stated neither, so both were Haiku's own
    errors. Added a sourced paragraph:
    - cycle 24 minimum Dec 2008 and maximum Apr 2014, with a first peak in Nov 2011 and a
      2012-mid 2013 plateau (SILSO);
    - Voyager 1 heliopause Aug 2012 and Voyager 2 Nov 2018; demodulate only the 1 AU flux.
    - Round 3: **2/2 PASS**; both called 2011-2013 solar maximum and demodulated only the
      ISS data.
  - P08, round 1: added a low-count, high-rigidity subsection to ref 35: exact interval,
    GV units, MDR/spillover, background. Result: **2/2 FAIL**, worse than before. Both
    runs called `sqrt(3)` correct or "approximately correct" and divided by 0.6 (TV)
    instead of 600 GV, so their numbers were 1000x too large. One invented the interval
    [1, 5]; the exact one is [1.37, 5.92].
  - P08, round 2: the subsection now says the answer to `sqrt(N)` is "no", to run the
    script instead of estimating the interval, and to convert TV to GV. Result: **2/2
    PARTIAL**, with no F signal: both said no, flagged TV->GV, and gave the correct script
    command. Neither ran the script, so there are no interval numbers, and neither
    mentioned resolution/spillover. P08 has been PARTIAL on Haiku in every pass.
  - Tests 201 OK (11 skips); bundle OK after each edit.

## P3 content pass (2026-09-25)

- Progressive disclosure: in the P2 runs, with-skill agents read 1 reference (15 tasks),
  2 (12) or 3 (5), and never more. The one outlier by size, reference 14 (~1,300 lines), now
  opens with a task-to-section table, and its `SKILL.md` routing row says to read one section.
  All in-package Markdown anchors resolve (checked by script).
- Overlap:
  - Reference 38 and `ams-analysis` were already cleanly split: 38 keeps no AMS numbers and
    defers to the sibling, and the sibling's `SKILL.md` says it supersedes 38.
  - Reference 49 Table 8 repeated five rows of reference 47's systematics mapping (field
    map, alignment, material, dead channels, pileup/noise). They were removed; Table 8 now
    lists only specialized-detector nuisances and points to 47.
  - The tables in 42 and 45 complement 49 (budget terms and sensor properties versus
    technology comparisons) and were kept.
- Missing worked topics: by the user's choice, these were added as verified walkthroughs
  in the references rather than as new archetype examples, keeping 3 per archetype.
  - 07 RooFit fit: run on fixtures, numbers quoted.
  - 09 pyhf end to end.
  - 20 BDT without leakage: the snippet was extracted from the reference and run in a
    scratch venv with scikit-learn. The default-sized model shows AUC 0.93 on the training
    fold versus 0.71 held out, with KS p < 1e-3; the shallow configuration gives 0.751 versus
    0.739 and KS p = 0.26 and 0.53, against a Bayes-optimal 0.748.
  - 28 Geant4 setup: a decision checklist, **not executed** (no Geant4 installed).
  - 33 IACT ON/OFF with trials: 2.35 sigma local, p_global 0.046 over 5 thresholds.
  - 35 flux from counts with cutoff and demodulation.
  All quoted numbers were recomputed.
- New `assets/end_to_end_sample_analysis.py`, a synthetic chain from signed-weight ntuple
  to sumw/sumw2 cutflow, orthogonal SR/CR, pyhf fit and CLs, and a yield table. Results:
  - The full-sample sumw equals lumi x xsec exactly (6000, 200).
  - Fit with signal injected at mu = 1: mu = 0.91 +- 0.16 (Minuit), mu_bkg = 0.99 +- 0.02,
    observed CLs limit 1.19.
  - Background only: mu = 0, observed limit 0.25, inside the expected band.
  - A bug found while writing it: with the scipy optimizer, pyhf 0.7.6 ignores
    `return_uncertainties`. The script uses Minuit when `iminuit` is present and otherwise
    reports the errors as unavailable.
  - `tests/test_end_to_end.py` (4 tests) passes with pyhf and skips without it.
- `assets/analysis_config.yaml` now states that its `selection`/`histograms` blocks are
  documentation and that the templates hard-code the same cuts.

- `plugin-dev:skill-reviewer` pass. I verified each finding before acting on it.
  Applied:
  - A wrong cross-reference (`li_ma_significance.py` pointed to reference 39 instead of 37).
  - A stale README claim that the ROOT scripts were never executed.
  - An ambiguous "first seventeen" count, now clarified; all 17 commands were re-run and pass.
  - `examples/README.md` is now linked from `SKILL.md`.
  - A tie-break rule for the overlapping tag-and-probe/efficiency routing rows.
  - General vs astroparticle subheadings for the invariants.
  - Missing test-file entries.
  - The description example "'my AMS-02 flux calculation'" is now "'my cosmic-ray flux from
    counts'", so AMS-specific work is not pulled away from `ams-analysis` (981 characters).
    Haiku trigger retest after the edit: 20/20 recall, 0/20 false triggers, and AMS queries still route to `ams-analysis`.
  Declined:
  - Moving the executable-resources list out of `SKILL.md`: the P2 runs showed the weaker
    model finds and uses scripts through that list.
  - Moving the example-authoring routing row to the README: authoring an example is a real
    task for this skill.
  - Dropping "Maintained in English."

## P2 behavior pass: fresh-model prompt, trigger, and example tests (2026-09-24)

Method: `tests/prompts.md` holds 16 prompts (14 graded HEP prompts balanced across
collider, space-based/AMS, and IACT/neutrino/air-shower work, plus 2 negative controls),
each with its expected behaviors (E) and failure signals (F). Each prompt went to fresh
subagents that saw only the prompt text (never the E/F lists), in four arms:
{with skill, baseline without skill} x {Opus, Haiku}. With-skill agents read `SKILL.md` and
followed its routing; baseline agents were barred from the repo and from skills.
Answers were capped at ~220 words. I graded them against E/F. This grading is a single
judgment per answer, not a blind panel.

| Arm | PASS | PARTIAL | FAIL |
|---|---|---|---|
| Opus + skill | 16 | 0 | 0 |
| Opus baseline | 16 | 0 | 0 |
| Haiku + skill | 12 | 3 (P08, P09, P12) | 1 (P02) |
| Haiku baseline | 3 | 7 | 6 (P01, P02, P08, P09, P11, P13) |

Findings:
- On Opus the skill does not change verdicts. Opus already knows these conventions. With the
  skill it adds tool use (it ran `cosmic_ray_flux.py` and `li_ma_significance.py`), more
  explicit reporting (raw count, exposure and bin width stated separately), and deferral of
  "latest AMS" questions to `ams-analysis`.
- On Haiku the skill matters. Baseline Haiku endorsed sqrt(N) for 3 events, quadrature errors
  for a correlated ratio, "absolute or signed" NLO weights with a post-skim sum, and "~50%
  mixed" from mean X_max. It also claimed the TRD measures charge sign. The skill fixed all
  of these.
- Negative controls (Linux root, PyTorch AMP) were answered without the skill in every arm.
- Gaps the test exposed, and fixes:
  - P02: Haiku with the skill checked jet multiplicity *before* the object cuts, then indexed
    unselected jets. The cause was that both reference snippets showed the multiplicity check
    on an uncut collection. `references/02-data-pipelines.md` now shows the ordered pattern
    (object mask -> sort -> count -> event mask -> index; verified on a synthetic awkward
    array), and `references/17-python-hep-coding.md` points to it.
  - P09: charge confusion was listed as a shared systematic. The `SKILL.md` ratio invariant now
    says species-specific effects belong to one yield.
  - P12: the significance was estimated rather than computed, and there was no plain verdict.
    `references/37` deliverables now require the computed value, the post-trials p, and a verdict.
- Rerun on Haiku + skill after the fixes, on the same prompts:
  - P02 and P09 now pass: the ordered jagged pattern is used, and charge confusion is
    assigned to the antiproton yield only.
  - P12 still partially failed on the first rerun. The model did not run the script, and it
    claimed the effective trials could be 10,000, more than the 400 positions tested. The
    ref-37 look-elsewhere text said "sky area / PSF solid angle" with no upper bound. It now
    says `N_eff ~ min(N_positions, area/PSF)` and gives `p_global = 1-(1-p_local)^N_eff`,
    with a worked example deliberately using *different* numbers from the test prompt.
  - Second rerun: P12 passes. The model ran `li_ma_significance.py`, got 2.74 sigma and
    p_global of about 0.7, and gave the verdict "not a detection".
  - Final Haiku + skill score: 15 PASS, 1 PARTIAL (P08: exact interval and asymmetric errors
    are there, but no computed flux). Caveat: these reruns reuse the prompts that guided the
    fixes, so they show the fixes work, not that the skill generalizes. A fresh prompt set is
    needed for that.
- Added `tests/test_yield_table.py`: 6 CLI tests for `make_yield_table.py`, which had none,
  covering negative yields and the missing-file, missing-column, empty and non-numeric paths.

Trigger test (`tests/trigger_queries.json`): 20 should-trigger and 20 should-not-trigger
queries, including near-misses (AMS latest/design questions, PyTorch/HEP-ML, Linux/Android/
certificate "root", root-mean-square, polynomial roots, JHEP formatting, Feynman diagrams).
A fresh agent was given the real descriptions of all seven repo skills and chose which to load.
This is an approximation of the harness's own skill selection, not the harness itself.
- Opus: recall 20/20, false triggers 0/20. Haiku: 20/20, 0/20.
- Every near-miss went to the right sibling (`ams-analysis`, `deep-learning`,
  `academic-diagrams`, `academic-papers`, `task-authoring`, `agile-development`) or to none.
  The description was left unchanged (977 characters), so sibling validators did not need a rerun.

Examples:
- `task-authoring/scripts/validate_skill_example.py`: all 24 pass.
- `check_example_diversity.py` flags 3 examples per archetype for every skill in the repo,
  which is the repo-wide convention. Nothing was changed.
- Python blocks, 23 in total: 12 run standalone. The test-first examples (19-21) were run end to
  end by building each hypothetical module from the example's own code. The buggy
  implementation fails its test and doctest, and the fixed one passes both, as each example
  claims. Their three REPL transcripts are now fenced as `pycon`. The remaining failures are
  continuation fragments (16, 18) or imports of the hypothetical project under audit (17, 18),
  and the surrounding text presents them as such.

## P1 verification pass: ROOT assets run for real, physics cross-checks (2026-09-24)

Environment: PyROOT does not load under miniconda `python3` (ABI mismatch) but works
under Homebrew `python3.14`. uproot 5.7.4 / awkward 2.9.0 / scipy 1.17.1 under miniconda;
pyhf 0.7.6 in a throwaway scratch venv. New `tests/make_root_fixtures.py` writes a
synthetic `Events` tree (jagged muons, ~5% negative weights), nominal/`jes_Up`/`jes_Down`
histograms, a mass peak, and a RooWorkspace.

Run for real, all passing:
- CMake configure + build with ROOT of `cpp_rdataframe_analysis.cpp`, `rdf_analysis.cpp`,
  `fit_histogram.cpp`; the shipped `assets/CMakeLists.txt`; and a project scaffolded
  by `scripts/new_root_cpp_project.sh` (built and run). Executables ran on the fixture;
  bad-input paths exit non-zero with clear messages.
- `plot_branch.C` runs interpreted (`root -b -q`). **Not verified with ACLiC (`+`)**:
  ACLiC fails here even for an empty macro (macOS SDK header mismatch), which is an
  environment problem, not a problem in the template.
- `pyroot_rdataframe_analysis.py` yields a cutflow identical to the C++ one (5000 ->
  3044 -> 2718 -> 2223) and a bin-identical histogram.
- `pyroot_roofit_signal_background.py` recovers the injected peak (mean 90.89 +- 0.06
  vs 91.0, sigma 2.43 +- 0.05 vs 2.5, nsig 2944 +- 67 vs 3000), status 0, covQual 3.
- The five PyROOT scripts ran on the fixtures (now in `tests/test_root_integration.py`).
- `uproot_awkward_analysis.py` gives values identical to the C++/PyROOT output.
- `pyhf-counting.json`: validates against the pyhf schema; `pyhf cls` gives CLs_obs =
  0.335 at mu=1; 95% CLs upper limit mu < 2.15 (expected 1.50 [corrected 2026-09-25: 1.50 is the -1 sigma band; the median expected is 2.153, equal to the observed since n=b]), plausible for n=b=20
  with a 10% background normsys.
- **Combine datacard not verified**: building standalone Combine (cloning and
  compiling external code) was blocked in this session's permission mode. The template
  is placeholder text, not a parseable card.

Defects found and fixed:
- **Physics change: `geomagnetic_cutoff.py` was not the vertical cutoff.** It used
  `(1 + sqrt(1 + cos^3 lambda))^2` in the denominator, which is the Stormer cutoff for
  arrival from the western horizon, giving 10.2 GV at the equator. The vertical cutoff
  (Smart & Shea 2005) is `14.9 cos^4(lambda)/r^2` GV. Fixed in the script, in
  reference 35, and in the test, which had attributed the wrong value to Gaisser.
  `orbit_averaged_geomagnetic_cutoff.py` inherits the fix: all its cutoffs rise by a
  factor (1+sqrt(1+cos^3))^2/4, which is 1.46 at the equator and falls toward 1 at the poles.
- `uproot_awkward_analysis.py` wrote `(values, edges)`, which drops sum(w^2). Its bin
  errors were therefore sqrt(sum w), wrong with the negative weights. It now writes a
  full TH1D with `fSumw2`; errors, flow bins, and moments now match the RDataFrame output.
  Added a header noting that the config's `selection`/`histograms` blocks are
  descriptive (the selection is hard-coded).
- `inspect_root_file.py` printed an empty type `[]` for every leaf-list branch; it now
  falls back to the leaf type (e.g. `Float_t`).
- Docs: `solar_modulation_force_field.py` and reference 35 said energies could be
  per nucleon "consistently". The `|Z| phi` shift is only right for total kinetic
  energy; per nucleon it is `(|Z|/A) phi`. Doc fix only, code unchanged.

Independent physics cross-checks (`tests/test_reference_values.py`):
- Li & Ma eq. 17 equals a numerical Poisson profile-likelihood ratio (scipy) to 1e-6.
- Clopper-Pearson matches `scipy.stats.beta` quantiles, and the Garwood Poisson interval
  matches `scipy.stats.chi2` quantiles, to 1e-8 or better.
- Bethe-Bloch minimum for muons matches the PDG tables to within 0.05% in Ar/Ne/Xe. It
  is 1.8% (Si) and 2.5% (water) high because the density effect is omitted, as
  documented.
- Highland (PDG form, including the z^2 log term), Cherenkov threshold/saturation in
  water, the force field against Gleeson-Axford by hand, the Gaisser-Hillas peak,
  TOF differences, and the calorimeter fit recovering its generated terms.
- Constants and units assumed: Highland 13.6 MeV / 0.038; Bethe K = 0.307075 MeV
  cm^2/mol, PDG Z/A and I; Stormer C = 59.6 GV at dipole moment 8.05e25 G cm^3 and
  r_E = 6371 km; masses in GeV from PDG; rigidity in GV, energy in GeV, phi in GV.

Reference audit (references 18-50): every line with a hard number was checked against
standard PDG/textbook values from knowledge (not re-fetched live). Corrected: the
Bethe-Bloch upper validity limit in reference 40 (was `beta gamma ~ 100`; PDG gives ~1000
for muons, and electrons are not described by the formula), and the IACT light-pool radius
in reference 33 (was 100-250 m, now ~120-150 m). All other numbers were correct,
including the worked residual statistics in reference 46, which were recomputed.
Added sources (Smart & Shea, Gleeson & Axford, Clopper-Pearson, Garwood, Gaisser-Hillas)
and a latest-results policy to `references/13-sources.md`.

## Deep test pass (2026-09-05)

A more thorough pass tested actual behavior, not just structure, working from the
files as they existed on disk after the merge and rename (staged fresh rather than
reused from an earlier local copy, to avoid testing stale content).

- `audit_histograms.py` was exercised against deliberately broken bundles covering
  every documented failure mode: a NaN in `sumw`, negative `sumw2`, a negative
  Poisson-expectation rate, a missing required `Down` variation, an
  identical-to-nominal variation, and mismatched edges between nominal and a
  variation. Each produced exactly the documented error or warning and the correct
  exit code; a clean bundle round-tripped through the module without mutating the
  input in place.
- `counting_reference.py`'s documented zero-observed/zero-background 95% bound
  (2.9957322735539895) was cross-checked against an independent calculation of
  `-log(0.05)` (agrees to floating-point precision), plus additional points and its
  documented input-range rejection (observed must be an integer from 0 through 500).
- `make_yield_table.py` was run against a real CSV (including a row with a blank
  uncertainty) and produced correctly formatted per-region Markdown tables; missing
  required columns and a missing input file both raised a clear, correctly-exited
  error.
- `validate_skill_bundle.py` was tested against four induced failures (a missing
  file, an emptied file, a broken SKILL.md frontmatter field, a renamed README
  section) and correctly caught each one, then confirmed clean again after
  restoring.
- All five PyROOT-dependent scripts (`inspect_root_file.py`,
  `check_systematic_variations.py`, `compare_root_histograms.py`,
  `summarize_histogram_statistics.py`, `roofit_workspace_summary.py`) defer
  `import ROOT` into the function body, so `--help` and file-existence/argument
  validation work with no ROOT installed, and the ROOT-dependent path fails with a
  deliberate `SystemExit("PyROOT is required ...")` message rather than a raw
  `ModuleNotFoundError` traceback.
- `scripts/new_root_cpp_project.sh` was run to scaffold a project, and the result was
  fed to `cmake -S . -B build`: configuration proceeds correctly through
  `cmake_minimum_required`/`project`/`CMAKE_CXX_STANDARD` and fails only at
  `find_package(ROOT REQUIRED ...)`, confirming the generated `CMakeLists.txt` is
  syntactically correct up to the point that genuinely requires a ROOT installation
  this environment doesn't have.
- Cross-checked every `references/NN-*.md` filename mentioned in `SKILL.md`'s routing
  table, `scripts/validate_skill_bundle.py`'s manifest, and the reference files'
  own internal cross-links against the files that actually exist on disk: all
  consistent, no typos, no orphaned files.
- Confirmed the shipped `assets/analysis_config.yaml` template actually satisfies
  every config key `assets/uproot_awkward_analysis.py` reads from it
  (`inputs.tree`, `inputs.files`, `branches.required`, `output.directory`,
  `output.root_file`).

Two defects were found and fixed as part of this pass:

- `scripts/new_root_cpp_project.sh` accepted a project-name argument, created the
  directory with that name, and printed build instructions referencing it, but the
  `CMakeLists.txt` it generated always hardcoded `project(root_cpp_analysis ...)`
  regardless of the argument. Fixed to interpolate the actual project name while
  keeping `${ROOT_INCLUDE_DIRS}`/`${ROOT_LIBRARIES}` as literal CMake variables.
- `assets/plot_branch.C` used `TTree` (via `file->Get<TTree>(...)`,
  `tree->GetBranch(...)`, `tree->Print()`) without including `<TTree.h>`, unlike
  every other template in the package that touches `TTree`. Added the missing
  include.

Housekeeping: the executable bit on `scripts/*.py` and `scripts/*.sh` did not survive
an earlier file transfer and has been restored; stray `__pycache__` directories left
behind by earlier interactive test runs were removed from the live folder.

## Merge and rename (2026-09-05)

This package (published at the time as `hep-experiment-analysis`) absorbed the
content of a separate, coding-focused `hep-analysis` skill (ROOT C++/PyROOT/
RDataFrame/uproot coding patterns, CMake builds, debugging, code conventions, and
additional ROOT-based helper scripts and starting-template assets). The folder and
the `name:` field in SKILL.md were then renamed back to `hep-analysis`, so this single
package now carries both the original `hep-analysis` coding content and the former
`hep-experiment-analysis` statistics content under the `hep-analysis` name. The
following checks were run after the merge:

- `python3 -m unittest discover -s tests -v`: all 13 tests passed unchanged.
- `python3 scripts/validate_skill_bundle.py`: confirmed all 53 files this package's
  SKILL.md/README.md depend on (references, scripts, assets, tests) are present and
  non-empty, and that SKILL.md carries valid frontmatter and README.md its expected
  section headers.
- `python3 -m py_compile` on every `.py` file in the package: all compiled without
  error, including the newly added ROOT/PyROOT-dependent scripts (syntax only - see
  limitation below).
- `bash -n` on every `.sh` file: no syntax errors.
- All relative Markdown links across every reference file were resolved against the
  filesystem: none broken.
- All YAML files (`assets/*.yaml`, `agents/openai.yaml`) and the SKILL.md frontmatter
  were parsed with PyYAML; both JSON assets were parsed with the standard library
  `json` module.
- Searched the full package for stale references to the old per-file names from the
  original `hep-analysis/references/*.md` layout: none found. After the rename, the
  remaining mentions of `hep-experiment-analysis` are the intentional migration notes
  in README.md and this file.
- Re-ran the original synthetic histogram CLI check: for zero observations, zero
  background, and a 95% flat-signal-prior credible bound, the result is unchanged at
  2.9957322735539895.

## Coverage expansion pass (2026-09-05)

Added three new reference files to broaden and deepen physics-object, trigger/
luminosity, and multivariate-classifier coverage:
`references/20-physics-objects-jets-btagging-met.md`,
`references/21-triggers-luminosity-pileup.md`, and
`references/22-multivariate-classifiers-bdt-nn.md`. Added two new standard-library
scripts implementing the concrete methodology those references describe -
`scripts/tag_and_probe_efficiency.py` (exact Clopper-Pearson binomial confidence
intervals) and `scripts/pileup_reweight.py` (data/MC pileup reweighting with
explicit undefined-bin flagging) - plus `assets/pileup_profiles.example.json` as a
synthetic input for the latter. `SKILL.md`'s reference-routing table, executable-
resources list, and frontmatter `description`, `README.md`'s coverage section and
quick checks, and `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` were all
updated to match (bundle now reports 59 files).

Unlike the ROOT/PyROOT-dependent scripts, both new scripts are pure Python
standard library and were verified numerically, not just for syntax:

- `tag_and_probe_efficiency.py`'s Clopper-Pearson interval (implemented via a
  from-scratch, log-space exact binomial tail and bisection - no SciPy dependency
  at runtime) was checked against two independent references: the well-known
  textbook exact values for 0/10 and 10/10 at 95% (0 to 0.30849710781876385, and
  its 0.6915028921812392-to-1 mirror image), and, more broadly, against
  `scipy.stats.beta.ppf`-derived Clopper-Pearson bounds (SciPy happened to be
  available in this validation environment, used here only as an independent
  correctness oracle, not as a runtime dependency of the script) across 12
  (pass, total) cases - including the boundaries 0/n, n/n, and totals up to the
  documented 200000 cap - and 4 confidence levels each (48 cases total), agreeing
  to within 2.4e-11. Interval containment of the point estimate and monotonic
  widening with confidence level were also checked directly.
- `pileup_reweight.py`'s reweighting formula was checked for self-consistency: the
  mean of a synthetic MC pileup profile, reweighted by the computed factors, was
  confirmed to match the target data profile's mean to within 1e-6 (a closure
  check, using the shipped `assets/pileup_profiles.example.json` - a Poisson-like
  data profile at mean 38 vs. an MC profile generated assuming mean 30). The
  explicit-flagging behavior for a data-populated, MC-empty bin (an undefined
  reweighting factor) was verified to report `None`/a flagged bin index and a
  nonzero exit code, rather than silently producing `inf` or `0`, and to leave a
  bin where *both* profiles are zero unflagged (nothing needs reweighting there).
- Both scripts' CLIs were exercised for invalid input (`pass_count > total`,
  out-of-range `total`, mismatched profile lengths, a missing input file) and
  confirmed to fail with a clear one-line message and a nonzero exit code rather
  than a raw traceback.
- 16 new tests were added to `tests/test_helpers.py` (13 pre-existing + 16 new =
  29 total, `python3 -m unittest discover -s tests -v`) covering all of the above.

## Detector, reconstruction, and simulation expansion pass (2026-09-09)

Added nine reference files covering the detector, reconstruction, and simulation
layers beneath the existing analysis/statistics content, organized by detector
technology with no assumed experiment:
`references/23-detector-systems-overview.md`,
`references/24-tracking-and-vertexing.md`,
`references/25-calorimetry-ecal-hcal.md`,
`references/26-particle-identification.md`,
`references/27-event-reconstruction.md`,
`references/28-reconstruction-performance-and-truth-matching.md`,
`references/29-event-generation.md`,
`references/30-detector-simulation.md`, and
`references/31-calibration-and-alignment.md`. Added four new standard-library
scripts implementing the formulas those references rely on -
`scripts/multiple_scattering.py`, `scripts/calorimeter_resolution.py`,
`scripts/pid_separation_power.py`, and `scripts/cherenkov_angle.py` - plus
`assets/detector_stack.example.json` and
`assets/calorimeter_response.example.json` as synthetic inputs. `SKILL.md`'s
reference-routing table, executable-resources list, analysis invariants (two new
entries: no tuning of simulation/calibration to the measured observable, and
detector quantities are inferred rather than observed), example requests, and
frontmatter `description`; `README.md`'s coverage section and quick checks;
`references/13-sources.md`; `agents/openai.yaml`; and
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` were all updated to match
(bundle now reports 74 files, up from 59). The sibling `skill-router` skill and
the repository README were extended with the same routing keywords.

All four new scripts are pure Python standard library and were verified
numerically against independently recomputed closed forms, not merely for syntax:

- `multiple_scattering.py` was checked against the PDG Highland expression
  recomputed inline in the tests, including its exact `1/(beta p)` scaling
  (doubling rigidity halves the angle to 15 decimal places), the `sqrt(x/X0)`
  scaling with the logarithmic correction accounted for separately, and the fact
  that the explicit charge factors cancel in the prefactor (`p = zR`) and survive
  only inside the logarithm. The logarithmic correction turns negative for
  extremely thin layers; the clamp to zero (an RMS may not be negative) was
  verified rather than left to produce a negative angle. The Gluckstern intrinsic
  term was checked against its closed form, its exact linearity in rigidity, and
  its quadratic improvement with lever arm (a factor 4 for a doubled arm, to 12
  decimal places). The crossover rigidity was verified to be exactly where the two
  terms are equal, and the maximum detectable rigidity to be exactly where the
  quadrature sum reaches 1. For the shipped example stack the resulting values
  (0.0357 total x/X0, a 1.07% scattering term, a 33.2 GV crossover, a 3.1 TV MDR)
  were also confirmed by hand.
- `calorimeter_resolution.py` was validated by exact closure: the shipped asset is
  generated analytically from a = 0.10 sqrt(GeV), b = 0.20 GeV, c = 0.007, and the
  fit recovers all three to better than 1e-10 with a maximum residual in squared
  resolution of 2.6e-17. Three further parameter sets were recovered the same way,
  including one with a genuinely zero noise term (recovered to ~7e-9 absolute,
  limited by the conditioning of the 1/E^2 column). The determined case - exactly
  three distinct energies for three unknowns - was confirmed to pass through every
  point. The three analytic crossover energies (b^2/a^2, a^2/c^2, b/c) were checked
  both against their closed forms and by confirming the corresponding term
  contributions are equal there. A fit whose input keeps falling faster than
  1/sqrt(E) drives the constant term negative; that case was verified to be
  reported as a flagged failed separation with `constant: null`, not square-rooted
  into a NaN.
- `pid_separation_power.py` was checked against the defining identity
  `p = m beta gamma`, against the exact inversion `m = p sqrt(1/beta^2 - 1)`, and
  against the `dm/m = gamma^2 dbeta/beta` amplification that the reference text
  claims. Time of flight was checked against `L/(beta c)`, the timing-to-velocity
  conversion against `beta c sigma_t / L`, and TOF separation was confirmed to fall
  as roughly the inverse square of momentum (a factor between 3.5 and 4.5 for a
  doubled momentum). The separation ceiling was verified to be exactly where
  separation equals the requested threshold, to rise with both a longer path and
  better timing, and to be reported as `None` when a species pair is never
  separated. The Bethe-Bloch evaluation reproduces the textbook ionization minimum:
  scanning muons in silicon places it at beta*gamma = 3.17 with a loss of
  1.694 MeV cm^2/g, against the PDG value of about 1.66 MeV cm^2/g near
  beta*gamma = 3.5 - the small excess and the slightly lower position are the
  expected consequence of omitting the density-effect correction, which the script
  reports explicitly (`density_effect_omitted`) and flags when evaluated in the
  relativistic rise. The exact `z^2` charge scaling was verified to 9 decimal
  places.
- `cherenkov_angle.py` was checked against `cos(theta_c) = 1/(n beta)` directly,
  against the threshold `p_thr = m/sqrt(n^2 - 1)` (and, independently, by
  confirming that beta at that momentum equals exactly 1/n), against the
  saturation angle `arccos(1/n)` and the approach to it at high momentum, against
  the `sin^2(theta_c)` photon yield, the `1/sqrt(N)` improvement of the per-track
  angular resolution, and the `dbeta/beta = tan(theta_c) sigma_theta` propagation.
  Threshold ordering across pion, kaon, and proton was confirmed, and a
  below-threshold species was verified to report no ring rather than a spurious
  angle. For an n = 1.05 radiator the resulting thresholds (0.436, 1.542 and
  2.931 GeV/c) and the 309.8 mrad saturation angle were confirmed by hand.
- All four CLIs were exercised for invalid input (a stack file missing a required
  field, fewer than three distinct energies, two identical species, a refractive
  index below 1) and confirmed to fail with a clear one-line message and a nonzero
  exit code rather than a raw traceback.
- 69 new tests were added to `tests/test_helpers.py` (29 pre-existing + 69 new =
  98 total, `python3 -m unittest discover -s tests -v`) covering all of the above.

Additional structural checks for this pass: every relative Markdown link in the
package was confirmed to resolve to an existing file, and the new references,
scripts, and assets were grepped for experiment names (AMS, CMS, ATLAS, ALICE,
LHCb and others) to confirm the technology-organized, experiment-agnostic framing
holds and that no synthetic value is presented as a real detector's measurement.

## Astroparticle physics expansion pass (2026-09-09)

Added eight reference files covering astroparticle and cosmic-ray physics
alongside the existing collider-physics content:
`references/32-cosmic-ray-spectrum-and-composition.md`,
`references/33-extensive-air-showers.md`,
`references/34-ground-based-detection-arrays.md`,
`references/35-imaging-atmospheric-cherenkov.md`,
`references/36-neutrino-astronomy.md`,
`references/37-space-based-direct-detection.md`,
`references/38-multimessenger-analysis.md`, and
`references/39-astroparticle-statistics.md`. Added four new standard-library
scripts implementing the formulas those references rely on -
`scripts/li_ma_significance.py`, `scripts/geomagnetic_cutoff.py`,
`scripts/cr_spectrum_powerlaw_fit.py`, and `scripts/xmax_gaisser_hillas.py` -
plus `assets/cosmic_ray_spectrum.example.json` as a synthetic input, and
`tests/test_astroparticle.py` as a separate test module (kept apart from
`tests/test_helpers.py` given the distinct domain). `SKILL.md`'s title,
frontmatter `description`, reference-routing table, executable-resources list,
analysis invariants (three new entries: ON/OFF region non-overlap and trials
accounting, top-of-atmosphere vs. modulated flux and cutoff reporting, and no
single-observable composition claims given the muon-content/X_max
discrepancy), and example requests; `README.md`'s title, quick checks,
coverage section, and example prompts; `references/13-sources.md` (new
citations, using plain-text book/journal citations rather than a guessed URL
for sources without one, and hyperlinks only to stable official homepages);
`agents/openai.yaml` was left unchanged (its metadata is already
domain-agnostic); and `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`
were all updated to match (bundle now reports 88 files, up from 74). The
sibling `skill-router` skill and the repository README were extended with the
same routing keywords.

All four new scripts are pure Python standard library and were verified
numerically, not merely for syntax:

- `li_ma_significance.py` was checked against the closed-form boundary cases:
  `N_off = 0` reduces to `S = sqrt(2*N_on*ln(2))` for alpha=1 (confirmed to
  10 decimal places), `N_on = N_off = 0` returns exactly zero by convention,
  and `N_on = alpha*N_off` (zero excess) returns exactly zero rather than a
  tiny nonzero value from floating-point cancellation in the radicand. The
  sign of the significance was confirmed to track the sign of the excess in
  both directions (a symmetric-magnitude check swapping `N_on`/`N_off`), and
  significance was confirmed to increase monotonically with a growing excess
  at fixed alpha. Invalid input (negative or non-integer counts, nonpositive
  alpha) was confirmed to raise a clear error, and the CLI was confirmed to
  match the library function and to fail cleanly (no traceback) on bad input.
- `geomagnetic_cutoff.py` was checked against the textbook equatorial value
  (`59.6 / (1+sqrt(2))^2 ~= 10.23 GV` at the geomagnetic equator, sea level,
  matching the standard dipole-approximation figure quoted in the cosmic-ray
  literature), confirmed to fall monotonically from equator to pole, to be
  symmetric under latitude sign, to vanish at the pole, and to decrease with
  increasing altitude (larger `r`). The kinetic-energy-per-nucleon conversion
  was checked to stay strictly below the rigidity (momentum) it derives from,
  as required for a nonzero rest mass, and to reject non-positive or
  inconsistent (A < Z) charge/mass-number input. The CLI was confirmed to
  match the library function.
- `cr_spectrum_powerlaw_fit.py` was validated by exact closure: a single
  power law generated with no scatter at index 2.7 is recovered to 8+ decimal
  places with a max log-flux residual below 1e-8, and a two-segment synthetic
  spectrum (index 2.7 below and 3.1 above a break at 4e15 eV, continuous at
  the break) has both indices and their difference recovered to 8+ decimal
  places by the segmented fit - while a single power law forced onto the same
  broken spectrum shows a residual more than 10x larger than either segment
  of the correct fit, confirming the tool actually distinguishes a genuine
  break from noise rather than trivially reporting a good fit either way. A
  weighted fit (per-point `sigma_flux` supplied) was confirmed to still
  recover the known index. Degenerate input (fewer than two distinct
  energies, non-positive energy/flux, too few points on one side of a
  requested break) was confirmed to raise a clear error, and the CLI was
  confirmed to match the library function on the shipped asset and to fail
  cleanly on a missing file.
- `xmax_gaisser_hillas.py` was checked against the profile's defining
  property `N(X_max) = N_max` to 1e-9 relative precision, confirmed to be
  smaller on both sides of `X_max` (unimodality), and confirmed undefined
  (`NaN`, not an exception) at or before the depth offset `X0`. The shower
  age was confirmed to equal exactly 1 at `X_max` and 0 at `X0`, and to
  increase monotonically with depth. The half-maximum-depth bisection was
  confirmed to bracket `X_max` (one root below, one above) and to land within
  0.01% of `N_max/2` at both roots. Geometrically invalid input
  (`X_max <= X0`) was confirmed to raise a clear error rather than producing
  a nonsensical or complex result, and the CLI was confirmed to match the
  library function and fail cleanly on bad geometry.
- 38 new tests were added in `tests/test_astroparticle.py` (98 pre-existing
  in `tests/test_helpers.py` + 38 new = 136 total,
  `python3 -m unittest discover -s tests -v`) covering all of the above.

Additional structural checks for this pass: every relative Markdown link in
the eight new reference files was confirmed to resolve to an existing file.
The new references were grepped for named real observatories (Pierre Auger
Observatory, Telescope Array, IceCube, KM3NeT, H.E.S.S., MAGIC, VERITAS, CTA,
AMS-02) - each appears only as a canonical, publicly documented example of a
detection *technique* (e.g. "hybrid surface-array/fluorescence design" or
"in-ice Cherenkov telescope"), never with a specific numeric value presented
as that facility's measurement, consistent with the same requirement enforced
in the detector/reconstruction/simulation pass above. The sources table's new
entries were checked to use plain-text citations (author/title/venue/year)
for books and pre-arXiv journal papers rather than a guessed URL, and
hyperlinks only for stable, well-known official homepages (PDG, Auger,
IceCube, CTA) rather than a specific document path not independently
confirmed.

## AMS-02 case study and cosmic-ray flux/statistics pass (2026-09-09)

Added one reference file, `references/40-ams02-case-study.md`, applying the
generic detector-technology references (`23`-`26`) and
[space-based direct detection](references/37-space-based-direct-detection.md) to the
Alpha Magnetic Spectrometer (AMS-02) on the ISS as a worked example: its
actual subsystem stack (permanent-magnet tracker, TRD, TOF, RICH, ECAL),
what is distinctive about a decade-plus space-based mission (no on-orbit
repair, orbital thermal cycling, a time-varying geomagnetic cutoff along the
orbit, a mission spanning multiple solar cycles), and the shared
rare-species-measurement pattern (positron fraction, antiproton/proton ratio,
antihelium search). Added four new standard-library scripts -
`scripts/orbit_averaged_geomagnetic_cutoff.py`,
`scripts/solar_modulation_force_field.py`,
`scripts/particle_ratio_with_uncertainty.py`, and `scripts/cosmic_ray_flux.py`
(the last per explicit request for general cosmic-ray flux calculation and
statistics, not AMS-02-specific) - plus `tests/test_ams02.py` (36 new tests).
`SKILL.md`'s frontmatter `description`, reference-routing table,
executable-resources list, two new analysis-invariant entries (exact Poisson
statistics for low-count flux, and correlation-aware ratio/fraction
uncertainty), and example requests; `README.md`'s quick checks, coverage
section, and example prompts; `references/13-sources.md` (an AMS-02 entry,
left without a pinned URL per this skill's sourcing discipline, since no
specific NASA/AMS page URL was independently confirmed in this pass); and
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` were all updated to
match (bundle now reports 94 files, up from 88). The sibling `skill-router`
skill and the repository README were extended with the same routing
keywords.

All four new scripts were verified numerically, not merely for syntax, and
two real defects were found and fixed during this pass:

- **Defect found and fixed**: `orbit_averaged_geomagnetic_cutoff.py`'s
  quadrature ceiling-search helper had its bracket-growth condition
  inverted - it grew the search bound while the tail probability was *above*
  a threshold instead of *below* it, which for `cosmic_ray_flux.py`'s exact
  Poisson interval search (reused independently, see below) caused every
  call to spuriously report the interval as unbounded. Fixed to grow the
  bracket only while the (monotonically increasing) tail has not yet reached
  the target probability, matching the standard bisection precondition.
- **Defect found and fixed**: `cosmic_ray_flux.py`'s exact Poisson interval
  had its lower- and upper-bound target probabilities swapped (using
  `1 - alpha/2` where the Garwood formula requires `alpha/2` for the lower
  bound, and vice versa for the upper bound), which silently produced a
  lower bound greater than the upper bound. Caught by cross-checking the
  n=42 interval against an independently computed `scipy.stats.chi2`
  Garwood-formula value during development (35.545043400971, 49.5323366625
  at 68.27% confidence) and confirming the two disagreed before the fix and
  matched to 9+ significant figures afterward; also re-checked at 90%
  confidence (31.938130721517, 54.323946486754) with the same exact
  agreement. `scipy` was used only for this one independent development-time
  cross-check and is not a dependency of the shipped script or test suite
  (both remain standard-library only; the test file hardcodes the
  cross-checked expected values).
- `orbit_averaged_geomagnetic_cutoff.py` was further checked to reduce to the
  single-latitude `geomagnetic_cutoff.py` value for a near-equatorial
  (1-degree) inclination, to have its minimum cutoff fall monotonically with
  increasing inclination, to bracket the equator-to-turning-point latitude
  range exactly, and to reject inclinations outside (0, 90] degrees.
- `solar_modulation_force_field.py` was checked for an exact round trip
  (`--modulate` then `--demodulate` on the resulting TOA flux recovers the
  original LIS flux to 8+ decimal places), for the `phi=0` identity (TOA
  flux equals LIS flux exactly when there is no modulation), for the
  modulation direction (a positive `phi` suppresses low-energy flux, as
  physically required), and for a larger energy shift at higher charge at
  fixed `phi` (consistent with `E_LIS = E_TOA + |Z|*phi`).
- `particle_ratio_with_uncertainty.py` was checked against direct arithmetic
  for the central ratio and fraction values, against the closed-form
  independent-quadrature uncertainty formula, for a zero uncertainty on both
  inputs giving exactly zero propagated uncertainty, and for a positive
  correlation coefficient reducing (not increasing) the propagated ratio
  uncertainty as the covariance term requires.
- `cosmic_ray_flux.py` was additionally checked for the flux central value
  matching direct division by exposure and bin width, for background
  subtraction correctly reducing the net count and the reported flux, for a
  larger exposure giving a smaller flux at fixed counts, for a count beyond
  the underlying exact tool's practical range raising a clear error rather
  than silently returning a truncated interval, and for the zero-observed
  case giving a zero lower bound with a positive upper bound.
- All four CLIs were exercised for invalid input (out-of-range inclination,
  missing required LIS parameters, nonpositive yields, a negative count) and
  confirmed to fail with a clear message and nonzero exit code rather than a
  raw traceback, and each CLI was confirmed to match its underlying library
  function's result exactly.

Additional structural checks: every relative Markdown link in
`references/40-ams02-case-study.md` was confirmed to resolve to an existing
file. The file was checked to distinguish real, named AMS-02 subsystems and
mission facts (a permanent, not superconducting, magnet; a TRD, TOF, RICH,
and ECAL; ISS orbital parameters used only descriptively) from any specific
numeric instrument parameter or published measurement value, none of which
are asserted here - the file explicitly directs a reader to verify any such
concrete value against an AMS collaboration publication before quoting it.

## Consistency audit (2026-09-10)

A "check and reorganize" pass with no new content: cross-checked
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` against every file
actually present under `references/`, `scripts/`, and `assets/` (no orphans,
no dangling entries either direction), cross-checked `SKILL.md`'s reference-
routing table against all 40 files under `references/` (every file linked
exactly once, no stale links), read every relative Markdown link's display
text against its actual target, re-ran all 17 standard-library-only quick-
check commands from `README.md` exactly as documented, and `py_compile`'d
every Python file in the package.

- Found and fixed **58 link-text/target mismatches across 19 files**
  (`20-physics-objects-jets-btagging-met.md`,
  `21-triggers-luminosity-pileup.md`, `22-multivariate-classifiers-bdt-nn.md`,
  `23-detector-systems-overview.md`, `24-tracking-and-vertexing.md`,
  `25-calorimetry-ecal-hcal.md`, `26-particle-identification.md`,
  `27-event-reconstruction.md`,
  `28-reconstruction-performance-and-truth-matching.md`,
  `29-event-generation.md`, `30-detector-simulation.md`,
  `31-calibration-and-alignment.md`,
  `32-cosmic-ray-spectrum-and-composition.md`,
  `33-extensive-air-showers.md`, `34-ground-based-detection-arrays.md`,
  `35-imaging-atmospheric-cherenkov.md`, `37-space-based-direct-detection.md`,
  `39-astroparticle-statistics.md`, `40-ams02-case-study.md`): each showed a
  `references/`-prefixed path as the link's visible text while the href
  (correctly, since these files live inside `references/` themselves)
  pointed at the bare sibling filename. Every one of these links already
  resolved correctly - this doesn't change or weaken any "every relative
  Markdown link resolves" claim made in the passes above - the fix is purely
  to the misleading display text, bringing it in line with the majority of
  cross-references in this same file set that already used the bare
  filename as both text and target. This is the same class of bug found and
  fixed in the sibling `agile-development` (3 occurrences) and
  `deep-learning` (17 occurrences) skills in this collection.
- Confirmed `references/19-cpp-balanced-design-guidelines.md` is **not**
  claimed byte-identical to `agile-development`'s/`deep-learning`'s shared
  copy of the same base file anywhere in this package's own docs (unlike
  those two skills, which do make and verify that claim of each other) - it
  legitimately carries an extra hep-analysis-specific scope-setting
  paragraph pointing to `14-cpp-root-coding.md`/`18-code-conventions.md`, so
  no inconsistency here; left untouched.
- All 17 standard-library quick-check commands in `README.md` still exit 0
  and match documented behavior; the ROOT/PyROOT-dependent scripts still
  only parse (`py_compile`) in this environment, consistent with the
  Limitations below (PyROOT itself fails to import here with an unrelated
  Python-ABI error, distinct from "ROOT not installed").
- Bundle validator and the full test suite (172 tests) re-run clean after
  the fixes.

## Example-authoring rollout pass (2026-09-10)

Added this skill's first `examples/` entry, per Phase 3 of `agile-development`'s
example-authoring initiative (see that skill's `references/example-authoring.md`
for the generation prompt and format spec this follows). One pilot example, not
a bulk batch.

- Added a one-line pointer to `agile-development`'s
  `references/example-authoring.md` to the "Reference routing" table in
  `SKILL.md`, explicitly noting the cross-skill dependency (requires
  `agile-development` installed alongside this skill), plus one new "Example
  requests" entry.
- Scaffolded `examples/01-jes-systematic-cutflow.md` with
  `agile-development`'s `generate_skill_example.py --skill hep-analysis --role
  "Senior Experimental Particle Physicist" --use-case "estimating the
  jet-energy-scale systematic uncertainty on a cutflow-based cross-section
  measurement"`, then filled it in by hand around the specific bug named in
  this skill's own `references/06-systematics.md`: "failing to recompute
  [selections] for a shape variation that moves objects across thresholds."
  The weak approach reuses the nominal selection mask for the JES up/down
  variations instead of recomputing it against the shifted jet `p_T`; the
  expert approach recomputes the selection independently per variation and
  reports the resulting migration counts.
- All numeric claims were independently executed with NumPy on a 200,000-event
  synthetic leading-jet `p_T` sample (seeded, `default_rng(20260910)`), not
  merely hand-derived:
  - Extracted both code blocks verbatim from the finished markdown file with a
    regex and imported them as real modules.
  - Weak approach: `eff_up = eff_down = eff_nominal = 0.3213` and a reported
    JES relative uncertainty of exactly `0.000%` - confirmed this is an
    artifact of the unapplied shift, not a coincidence, since `n_up`/`n_down`
    both reduce to `mask_nominal.sum()` by construction.
  - Expert approach: `eff_nominal=0.3213`, `eff_up=0.3340`, `eff_down=0.3079`,
    JES relative uncertainty `4.059%`, with 2,539 events migrating into the
    selection under the +3% shift and 2,677 migrating out under the −3% shift.
  - `python3 scripts/validate_skill_example.py` (from `agile-development`)
    reports `ok` - no structural or placeholder findings.
- No ROOT/PyROOT/uproot installation was available in this environment, so the
  example uses plain NumPy array masking as a dependency-free stand-in for the
  same columnar selection-mask logic `references/17-python-hep-coding.md`
  documents for uproot/awkward pipelines; this is stated explicitly in the
  file's `## Scenario` framing rather than presented as a ROOT-integrated
  analysis. This is a real limitation of this pass, not of the underlying
  physics point, which does not depend on the I/O layer.
- Added `examples/README.md` (one-row index table, linking back to
  `agile-development`'s reference) and added both new files to
  `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`. Bundle now reports 96
  files, up from 94.
- Re-ran `python3 scripts/validate_skill_bundle.py` (96 files OK) and
  `python3 -m unittest discover -s tests -v` (172 tests, unchanged - this pass
  added content, not new test code) after the change.

## Cross-repository consistency follow-up (2026-09-10)

A second "check and reorganize" pass across the whole collection (this skill plus
its four siblings) caught two things the same-day Consistency audit above missed:

- `references/22-multivariate-classifiers-bdt-nn.md` referenced `[[deep-learning]]`
  using `[[wiki-link]]` double-bracket syntax - the linking convention this
  repository's own memory files use, not skill markdown, and not the convention
  used anywhere else in this package (a plain backtick-quoted skill name, e.g.
  `` `deep-learning` ``). It rendered as literal double brackets rather than a
  link. Fixed to a plain backtick. A repository-wide `grep -rn '\[\['` confirmed
  this was the only such occurrence in this skill (two more were found and fixed
  the same way in the sibling `agile-development` and `deep-learning` packages).
- This file's own AMS-02 case-study entry linked
  `[space-based direct detection](37-space-based-direct-detection.md)` with no
  `references/` prefix. The earlier Consistency audit's link-text/target check
  only covered links *inside* `references/*.md` files (where a bare sibling
  filename is correct); it didn't catch this prose link inside `VALIDATION.md`
  itself, which sits at the skill root, one directory above the file it points to
  - so the link was genuinely broken, not just misleadingly labeled. Fixed to
  `references/37-space-based-direct-detection.md`. A full anchor-aware relative-
  link check (stripping `#fragment`s before resolving, unlike the quick check
  that first flagged this) was re-run across every `.md` file at the skill root
  and confirmed no other file-level links are broken.

Bundle validator and full test suite (172 tests) re-run clean after both fixes.

## Example expansion to three (2026-09-10)

Expanded this skill's `examples/` from the one pilot entry to three, per the
user's request to bring every installed skill's `examples/` up to three
entries with genuinely different content each.

- Scaffolded `examples/02-tag-and-probe-background-subtraction.md` (role
  "Senior Experimental Particle Physicist") and
  `examples/03-li-ma-significance-iact.md` (role "Astroparticle Physicist /
  IACT Analyst") with `agile-development`'s `generate_skill_example.py`, then
  filled both in by hand, grounded in this skill's own reference material
  rather than invented independently:
  - `02` is built on `references/04-histograms-efficiencies.md`'s guidance
    that "tag-and-probe requires background modeling ... and closure" and its
    stated efficiency-ratio propagation formula `Var(e) ~= Var(A)/B^2 +
    A^2*Var(B)/B^4 - 2*A*Cov(A,B)/B^3`. The weak approach counts raw
    pass/fail window totals as pure signal (efficiency 0.7761, no
    uncertainty); the expert approach sideband-subtracts the signal yield in
    each category first (efficiency 0.8800 +/- 0.0143) and reports a
    background-model systematic (+0.0098) from an alternative sideband
    extrapolation. All four numbers were independently re-executed from the
    finished markdown's own code blocks (not merely hand-derived) and matched
    to 4 decimal places. The weak-approach discussion also notes that the
    shipped `scripts/tag_and_probe_efficiency.py` (exact Clopper-Pearson on a
    pure binomial pass/total count) does not fix this scenario either, since
    it assumes a background-free count - checked by reading that script's own
    docstring rather than assumed.
  - `03` is built on `references/39-astroparticle-statistics.md`'s Li & Ma
    (1983) formula and its look-elsewhere-effect discussion. The weak
    approach uses the naive Gaussian `(N_on - alpha*N_off)/sqrt(N_on +
    alpha^2*N_off)` formula on `N_on=10, N_off=20, alpha=0.2` and reports an
    uncorrected single-trial 1.826 sigma; the expert approach uses the Li & Ma
    likelihood-ratio significance (2.222 sigma) and then applies a Sidak-style
    trials correction for 25 independent scan positions, collapsing it to a
    global 0.578 sigma. The Li & Ma implementation embedded in the example was
    cross-checked line-for-line against the shipped
    `scripts/li_ma_significance.py --on 10 --off 20 --alpha 0.2`, which
    returns the identical `2.2219814487593066` significance.
  - `python3 ../agile-development/scripts/validate_skill_example.py` reports
    `ok` for both files - no structural or placeholder findings.
- Added both new files to `examples/README.md`'s index table and to
  `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`. Bundle now reports 98
  files, up from 96.
- Re-ran `python3 scripts/validate_skill_bundle.py` (98 files OK) and
  `python3 -m unittest discover -s tests -v` (172 tests, unchanged - this pass
  added content, not new test code) after the changes.

## Example-authoring: Execution Trajectory pilot (2026-09-11)

Added this skill's first non-Contrast example, per Phase 3 of
`agile-development`'s four-archetype example-authoring revision (see that
skill's `references/example-authoring.md` for the full archetype spec; this
skill depends on `agile-development` being installed alongside it for the
tooling).

- Scaffolded and filled `examples/04-trajectory-cutflow-normalization-
  mismatch.md` (Execution Trajectory archetype, role "Senior Experimental
  Particle Physicist"): a signal MC cutflow yield measuring ~15% high,
  uniformly, at every selection step. Grounded the root cause directly in
  `references/03-weights-normalization.md`'s "Basic convention" (`w_event = (L
  x sigma x k x filter_efficiency / sum_full_gen_weights) x w_gen x
  product(corrections)`, and its explicit warning that "the denominator must
  cover the corresponding production... normally from preselection
  metadata"): a `sum_full_gen_weights` denominator computed from a metadata
  snapshot taken before 6 of 40 production jobs were resubmitted after a
  first-attempt failure, so the merged ntuples' numerator reflects all 40
  jobs while the denominator only reflected 34 - a shape-preserving, uniform
  normalization error rather than a selection-logic bug, which is why no
  single cutflow step was implicated.
- The worked arithmetic (a 1.15 ratio reproducing the reported ~15% excess at
  every step, and the corrected yields matching an independent validation
  skim within stated uncertainty) was checked for internal consistency across
  all four cutflow steps before being written into the example, not just
  asserted.
- `python3 ../agile-development/scripts/validate_skill_example.py
  examples/04-trajectory-cutflow-normalization-mismatch.md` passes with no
  structural or placeholder findings.
- Added one row to `examples/README.md`'s index (now four columns) and added
  the new file to `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`.
  Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 99 files
  present and non-empty.", up from 98) and
  `python3 -m unittest discover -s tests -v` ("Ran 172 tests" / "OK",
  unchanged - this pass added example content, not new test code).
- Also generalized the "Authoring a canonical worked example" pointer in
  `SKILL.md`'s reference table from "(Weak vs. Expert contrast)" to name all
  four archetypes, matching `agile-development`'s own updated wording.

**Backlog (explicitly deferred, not silently missing):** three archetypes
remain unpiloted for this skill, per the source initiative's Phase 3 backlog
table - Contrast (a systematics writeup, weak vs. expert - distinct from the
three Contrast examples already shipped), Gated Pipeline (systematic-
uncertainty estimation with a closure-test gate), and Decision-Tree (an
unexpected excess in a control region: background vs. new physics vs.
detector effect vs. statistical fluctuation). None were started in this pass.

**Superseded by the pass below (2026-09-11):** the Gated Pipeline and
Decision-Tree backlog items above were fulfilled the same day, each expanded
to three examples rather than a single pilot. The Contrast backlog item (a
systematics writeup) remains open.

## Archetype expansion to three examples each (2026-09-11)

Expanded Execution Trajectory, Gated Pipeline, and Decision-Tree from one
pilot each (the previous entry above) to three examples each, per an explicit
follow-up request that every skill's `examples/` carry three genuinely
different examples per archetype, matching the shape already established for
Contrast. Added 8 new files (`05`-`12`); this skill's `examples/` now holds
12 files total: 3 Contrast, 3 Trajectory, 3 Gated Pipeline, 3 Decision-Tree.

- **Trajectory** (`05`, `06`): a JES systematic template that looks inverted
  in its highest-pt bin - resisting the tempting "swap the Up/Down labels"
  fix per `references/06-systematics.md`'s explicit warning that migration
  can legitimately lower a bin for an Up variation, and instead finding a
  real correction-file copy-paste bug while independently confirming the one
  genuinely-inverted bin via generator-truth migration counts; and an ABCD
  background closure failure traced to a real correlation between the two
  discriminating variables, resolved with a `kappa` correction factor
  measured in an independent validation region (`references/05-backgrounds.md`'s
  "ABCD" section) and verified to reproduce that region's own observation
  exactly.
- **Gated Pipeline** (`07`-`09`): a b-tagging systematic-uncertainty budget
  with a closure-test gate (the backlog item), where the red-team phase finds
  a uniform era-correlation assumption was wrongly double-suppressing a
  calibration-statistics component (`references/06-systematics.md`'s "Source
  inventory" rule against blanket correlation assumptions); an unfolded
  cross-section measurement (`references/10-measurements-unfolding.md`) whose
  red-team phase finds genuine truth-model dependence in one bin via a
  rebuilt response matrix, and excludes that bin explicitly rather than
  quoting an ad hoc extra uncertainty; and an alignment-propagation pipeline
  (`references/31-calibration-and-alignment.md`) whose red-team phase finds a
  single cosmic-ray comparison cannot alone bound a charge-antisymmetric weak
  mode, adding an independent `E/p` symmetry check.
- **Decision-Tree** (`10`-`12`): the backlog's control-region-excess triage
  (background mismodeling vs. new physics vs. detector effect vs. statistical
  fluctuation), selecting the mismodeling branch and tracing it to sideband
  functional-form uncertainty; a tracking-efficiency-drop triage
  (`references/24-tracking-and-vertexing.md`, cross-linking
  `references/31-calibration-and-alignment.md`) selecting a pattern-
  recognition search-window branch and quantifying its efficiency/fake-rate
  tradeoff; and a multi-messenger alert triage
  (`references/38-multimessenger-analysis.md`) selecting the post-hoc-window
  branch and computing a trials-corrected p-value.
- All numeric/arithmetic claims were independently executed with Python
  before being written into the files, not just hand-derived - this caught
  one defect: the multi-messenger trials-corrected p-value was first
  mis-stated as 0.858 and corrected to the actual computed value, 0.847,
  after running `1 - (1 - 0.014)**133` rather than trusting mental
  arithmetic.
- Every new file was validated individually with
  `python3 ../agile-development/scripts/validate_skill_example.py <file>`
  (all report `ok`) before being wired up.
- Added all 8 new file paths to `scripts/validate_skill_bundle.py`'s
  `REQUIRED_PATHS` and one row per file to `examples/README.md`'s index.
  Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 107 files
  present and non-empty.", up from 99) and
  `python3 -m unittest discover -s tests -v` ("Ran 172 tests" / "OK",
  unchanged - this pass added example content, not new test code).

**Remaining backlog:** Contrast still has only its original 3 examples (a
systematics writeup, weak vs. expert, from the source initiative's backlog
table, remains unstarted); the other three archetypes are now at parity with
Contrast at 3 examples each.

## Consistency audit (2026-09-11)

A further "check and reorganize" pass, in the same spirit as the same-day
audits of the four sibling skills (each of which found and fixed a real
coverage-documentation gap in `README.md` or its equivalent). Diffed
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` against every real file
on disk, checked every relative Markdown link in the package for a broken
target (using an anchor-aware resolver, matching the method from the
2026-09-10 Cross-repository consistency follow-up above), swept for
`[[wiki-link]]` syntax, confirmed every `references/*.md`/`scripts/*`/
`assets/*` file is mentioned in `SKILL.md`, re-ran all 17 stdlib-only
README-documented quick-check commands plus `check_root_cpp_env.sh` live,
syntax-checked every `scripts/*.py` file, and validated all 12 shipped
`examples/*.md` files.

- **Found and fixed a real gap**, the same class found the same day in
  `agile-development`, `deep-learning`, and `academic-papers`:
  `README.md`'s "Coverage and boundaries" paragraph omitted two topics that
  `SKILL.md`'s own reference-routing table links to explicitly -
  `references/09-statistical-tools.md` (pyhf/HistFactory/Combine
  workspace-and-datacard model mapping: channels, `normfactor`/`normsys`/
  `histosys`/`shapesys`, shared-parameter naming) and
  `references/19-cpp-balanced-design-guidelines.md` (general C++ class/
  struct/RAII/ownership design, as distinct from the ROOT-specific coding
  conventions already named in the same sentence). The only pre-existing
  mentions of "pyhf"/"Combine" in `README.md` were in the "Quick checks"
  section's execution-environment caveat, not in the coverage description
  itself. Added one clause for each to the first coverage paragraph, in the
  same itemized style as the surrounding text; left `SKILL.md`'s own
  frontmatter `description` unchanged, since (unlike `deep-learning`'s, which
  is an exhaustive itemized list) it is already a deliberately terser summary
  that omits many other reference topics by name (debugging, code
  conventions, Python HEP coding) and already names pyhf/Combine once via
  "RooFit/RooStats/pyhf/Combine".
- Considered `references/13-sources.md` (primary-source/version-check
  methodology) for the same treatment and judged it out of scope: it is
  process guidance about how this package sources its own content, not a
  user-facing analysis topic the coverage paragraph enumerates elsewhere
  (comparable to `VALIDATION.md` itself not being described in coverage).
- No other inconsistencies found: `REQUIRED_PATHS` (107 entries) matches the
  file tree exactly in both directions; the one `VALIDATION.md` hit from a
  broken-link grep was a false positive - quoted historical text inside this
  file's own 2026-09-10 entry describing an already-fixed bug, not a live
  link (confirmed by reading the surrounding paragraph and the actual live
  link two paragraphs above it, which already carries the `references/`
  prefix); the one `[[wiki-link]]` hit was the same kind of historical quote
  inside that same entry; all 17 stdlib scripts plus `check_root_cpp_env.sh`
  ran exactly as documented; every `.py` file under `scripts/` parses with no
  syntax errors; all 12 examples pass `agile-development`'s
  `validate_skill_example.py`, 3 per archetype, `examples/README.md`'s index
  (12 rows) matches; `agents/openai.yaml` is a high-level category summary
  (same design choice as `deep-learning`'s and `skill-router`'s) and needed
  no change.
- Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 107 files
  present and non-empty.", unchanged - no new files) and
  `python3 -m unittest discover -s tests -v` ("Ran 172 tests" / "OK",
  unchanged) after the fix.

## Second-wave example-authoring pass: Elicitation, Test-First, Postmortem (2026-09-12)

Added three new canonical examples in `agile-development`'s second-wave
archetypes, continuing the four-archetype example-authoring plan (Contrast/
Trajectory/Gated Pipeline/Decision-Tree already covered this skill; this
pass adds Elicitation, Test-First, and Postmortem).

- `examples/13-elicitation-signal-search-ambiguous-request.md`: an
  underspecified "can you check if there's a signal in this dataset?"
  request resolved via 4 clarification questions grounded in
  `references/01-analysis-design.md` (channel, signal-region, background
  model) and `references/08-inference.md` (significance convention,
  look-elsewhere effect) to a fully-specified dijet bump-hunt analysis
  contract.
- `examples/14-test-first-selection-efficiency-numerical-tolerance.md`: a
  weighted-efficiency function (`e = A/B` with the shared-events covariance
  term from `references/04-histograms-efficiencies.md`) red on a naive
  independent-variance implementation (87% overstated uncertainty,
  numerically verified in-session) to green matching a hand-computed
  reference to floating-point precision.
- `examples/15-postmortem-mc-production-pipeline-crash.md`: an overnight
  MC-production crash traced through 5 Whys (no "human error" stop) to a
  batch-pool reconfiguration that silently broke an implicit scratch-cleanup
  assumption, per `references/02-data-pipelines.md`'s "do not silently skip
  failed remote files and report a complete sample" guidance; fixed with an
  automated `TFile::IsZombie()`/`kRecovered` output-integrity gate.
- All three pass `agile-development/scripts/validate_skill_example.py` and
  the diversity checker (`check_example_diversity.py`) shows no
  archetype/skill repeats across the 12-file second-wave batch.
- `examples/README.md`'s intro line updated from "four archetypes" to
  "eight archetypes"; three rows added to its index (15 rows total).
- `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` extended with the
  three new example files. Re-ran `python3 scripts/validate_skill_bundle.py`
  ("Bundle OK: 110 files present and non-empty") and
  `python3 -m unittest discover -s tests -v` (172 tests, all passing,
  unchanged from before this pass since no existing test hardcodes the
  example count) after the change.

## Expand all four second-wave archetypes to three examples per skill (2026-09-12)

Every archetype now ships 3 examples per skill (not 3 total, one per skill) -
matching how Contrast/Trajectory/Gated-Pipeline/Decision-Tree already work
here. Added 9 new examples (16-24) to close the gap: Elicitation, Test-First,
and Postmortem each had 1, now have 3; Adversarial Audit had none, now has 3.

- `examples/16-17` (Elicitation): "redo the background estimate", "unfold
  this spectrum" - two underspecified requests resolved via
  `references/05-backgrounds.md`/`06-systematics.md` (method, control
  region, systematic scope) and `references/10-measurements-unfolding.md`
  (method, binning, regularization, uncertainty scope).
- `examples/18-20` (Adversarial Audit): attack a "5.2 sigma - discovery"
  significance claim (uncorrected mass-window look-elsewhere effect, an
  unrecorded unblinding/refit step), a "validated, ready to apply" b-tagging
  scale factor (a kinematic mismatch between control and signal-region
  phase space, a same-sample closure test), and a "closure verified" ABCD
  background estimate (non-factorizable defining variables, a closure test
  performed away from the signal-region-overlapping bins) - grounded in
  `references/09-statistical-tools.md`,
  `references/04-histograms-efficiencies.md`/`31-calibration-and-alignment.md`,
  and `references/05-backgrounds.md`.
- `examples/21-22` (Test-First): a luminosity-weighted-yield numerical
  invariant (a dropped fb^-1 -> pb^-1 factor, understating every yield
  1000x) and a JES-idempotence invariant (a double-corrected jet 5.25 GeV
  high in pT), grounded in `references/03-weights-normalization.md` and
  `references/20-physics-objects-jets-btagging-met.md`.
- `examples/23-24` (Postmortem): a calibration-constant payload silently
  shifting the energy scale for a week, and a shared ntuple-production job's
  path-collision bug overwriting another group's output, grounded in
  `references/31-calibration-and-alignment.md` and
  `references/02-data-pipelines.md`; both 5-Whys chains terminate in a
  missing sanity-check/collision-prevention design gap, not "human error".
- All 9 pass `agile-development/scripts/validate_skill_example.py`; zero
  placeholder markers.
- `examples/README.md`: added 9 rows (16-24), 24 rows total.
- `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` extended with the 9
  new example files.
- `agile-development/scripts/check_example_diversity.py`'s cross-skill
  constraint no longer applies to this skill's second-wave archetypes (each
  now deliberately repeats this skill 3x per archetype) - see
  `agile-development/references/example-authoring.md`'s revised "Diversity
  rule". This batch was hand-curated instead: each trio targets a
  conceptually distinct method/claim/invariant/incident.
- Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 119 files
  present and non-empty") and `python3 -m unittest discover -s tests -v`
  (172 tests, all passing, unchanged) after the change.

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

- `16-elicitation-background-estimate-ambiguous-request.md` -> `14-elicitation-background-estimate-ambiguous-request.md`
- `17-elicitation-unfolding-ambiguous-request.md` -> `15-elicitation-unfolding-ambiguous-request.md`
- `18-adversarial-audit-discovery-significance-claim.md` -> `16-adversarial-audit-discovery-significance-claim.md`
- `19-adversarial-audit-btag-scale-factor-claim.md` -> `17-adversarial-audit-btag-scale-factor-claim.md`
- `20-adversarial-audit-abcd-closure-claim.md` -> `18-adversarial-audit-abcd-closure-claim.md`
- `14-test-first-selection-efficiency-numerical-tolerance.md` -> `19-test-first-selection-efficiency-numerical-tolerance.md`
- `21-test-first-luminosity-weight-invariant.md` -> `20-test-first-luminosity-weight-invariant.md`
- `22-test-first-jes-idempotence-invariant.md` -> `21-test-first-jes-idempotence-invariant.md`
- `15-postmortem-mc-production-pipeline-crash.md` -> `22-postmortem-mc-production-pipeline-crash.md`

Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 119 files present and non-empty") and `python3 -m unittest discover -s tests -v` (172 tests, all passing) after the rename. All 24 example files individually re-validated with `agile-development/scripts/validate_skill_example.py` ("ok").

## Add ROOT-specific design guidelines (2026-09-15)

Per explicit user request, added `references/41-root-balanced-design-guidelines.md`:
`TObject` inheritance decisions, class dictionaries and I/O (`ClassDef`/`ClassImp`,
`LinkDef.h`, streamer versioning), directory-based ownership (`SetDirectory`,
`TFile`/`TDirectory` lifetime, the double-free/use-after-free failure modes around
it), RAII vs. ROOT ownership, branch-buffer structs, inheritance/polymorphism and
template/dictionary limits specific to ROOT, error handling at the ROOT boundary
(`gErrorIgnoreLevel`/zombie objects vs. this codebase's own error-handling
convention), const-correctness caveats in older ROOT APIs, global-state
(`gDirectory`/`gRandom`/`gStyle`) testability, and file/build organization for
dictionary-bearing classes.

This was routed here rather than into `agile-development` (where it was first
requested) after `skill-router` flagged ROOT as this skill's domain and a
follow-up question to the user confirmed the choice: `agile-development`'s
`cpp-balanced-design-guidelines.md`/`python-balanced-design-guidelines.md`/
`bash-balanced-design-guidelines.md` family is general-purpose, Google-style-guide
language guidance with no framework tie-in, whereas ROOT is a HEP-specific C++
framework - the new file belongs alongside this skill's other ROOT-specific
references (`14-cpp-root-coding.md`, `15-cmake-and-build.md`,
`16-debugging-root.md`, `18-code-conventions.md`), not in that general-language
family. The new file explicitly builds on `19-cpp-balanced-design-guidelines.md`
(cross-linked both directions) rather than repeating its content: it covers only
where ROOT's ownership/dictionary/error-reporting model departs from general C++,
not general class-design guidance ROOT does not affect.

Wired into the bundle: `SKILL.md`'s reference-routing table (new row after the C++
design guidelines row), `README.md`'s Coverage and boundaries paragraph,
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`, and forward/back cross-links
in `14-cpp-root-coding.md`, `18-code-conventions.md`, and
`19-cpp-balanced-design-guidelines.md`. All internal anchor links (to sections
within `19-cpp-balanced-design-guidelines.md` and `14-cpp-root-coding.md`) were
checked by hand against each target file's actual heading text and GitHub's
slug convention; all resolve. Re-ran `python3 scripts/validate_skill_bundle.py`
("Bundle OK: 120 files present and non-empty") and
`python3 -m unittest discover -s tests -v` (172 tests, all passing) after the
change - no test references the new file's content directly (it is prose
guidance, like `19-cpp-balanced-design-guidelines.md`, not executable), so this
confirms bundle integrity, not the guidance's technical accuracy. The ROOT-specific
claims in the file (directory ownership semantics, `ClassDef`/dictionary
requirements, `SetDirectory` behavior) were not verified against a live ROOT
installation in this pass - see the Limitations entry below on ROOT not being
installed in the validation environment.

## Consolidate C++/ROOT references into 41-root-balanced-design-guidelines.md (2026-09-15)

Per explicit follow-up user request the same day, superseded the design from the
previous entry above: rather than `41-root-balanced-design-guidelines.md` being a
thin ROOT-specific delta on top of `14-cpp-root-coding.md`, `18-code-conventions.md`,
and `19-cpp-balanced-design-guidelines.md`, those three files were merged into it
and then deleted. `41-root-balanced-design-guidelines.md` is now the single,
self-contained C++/ROOT reference for this skill (concrete RDataFrame/TTreeReader
code patterns and build commands from `14`; naming/comments/file-documentation
conventions from `18`, minus its one Python-naming bullet, which was not
C++/ROOT-scoped and was moved to `17-python-hep-coding.md`'s new "Naming" section
instead of being dropped; and the full general C++ class/struct/RAII/inheritance/
ownership/templates/testing/error-handling/const-correctness/naming/file-
organization guidance from `19`), interleaved topic-by-topic with the
ROOT-specific material each topic already had (e.g. general "Ownership
Guidelines" immediately followed by ROOT's "Directory-Based Ownership", general
"Error Handling" by "Error Handling at the ROOT Boundary") rather than kept as
two separate blocks. Content was preserved, not summarized - full code examples
from all three source files carried over - confirmed by asking the user two
scoped questions first (merge-then-delete vs. drop, and whether this should
change `agile-development`'s shared copy of `19`'s content) before doing the
merge; the user chose "merge then delete" and "no change to `agile-development`",
so `agile-development/references/cpp-balanced-design-guidelines.md` (the file
`19` here was a fork of) was left untouched.

Updated to remove the three deleted filenames and consolidate: `SKILL.md`'s
reference-routing table (four rows collapsed into one pointing at `41`, plus the
"Code file requirement" section's pointer now targets
`41-root-balanced-design-guidelines.md#naming-comments-and-file-documentation`),
`README.md`'s "onward for the coding-level guidance" sentence (now names `41` and
`15-cmake-and-build.md` explicitly, since the numeric-onward phrasing no longer
works with `41` out of sequence), and `scripts/validate_skill_bundle.py`'s
`REQUIRED_PATHS`. Every internal anchor link inside the merged `41` file (over
1,300 lines, ~47 headings) was checked against GitHub's slug algorithm by hand
after a first pass introduced three wrong anchors (links that pointed at a
parent section instead of the specific subsection named in the link text); all
now resolve to their named subsection, not just the containing section. Confirmed
no other file in the repo (outside this file's own historical `VALIDATION.md`
entries, deliberately left as a record of what was true when written) still
references `14-cpp-root-coding.md`, `18-code-conventions.md`, or
`19-cpp-balanced-design-guidelines.md`. Re-ran
`python3 scripts/validate_skill_bundle.py` ("Bundle OK: 117 files present and
non-empty") and `python3 -m unittest discover -s tests -v` (172 tests, all
passing). As with the previous entry, the ROOT-specific technical claims were not
re-verified against a live ROOT installation in this pass.

## Check and reorganize: renumber references/ to close gaps (2026-09-15)

Per explicit user request to "check and reorganize" this skill, ran a full audit
before changing anything: a custom link/anchor checker (Python, slugifying every
Markdown heading the same way GitHub does and resolving every `[text](target)`
link's file path and `#anchor` against it) across all of `hep-analysis/`'s `.md`
files, plus a comparison of `SKILL.md`'s routing-table links, `README.md`'s links,
and `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` against what actually
exists on disk. Result: every real link and anchor resolved (the checker's two
flagged hits were both historical prose inside `VALIDATION.md` quoting a past bug
in backticks, not live links); `REQUIRED_PATHS` exactly matched the file list. The
one real finding: the two previous consolidation passes above left
`references/` with gaps at 14/18/19 (the three deleted files) and
`41-root-balanced-design-guidelines.md` sitting out of numeric sequence at the
end, even though `SKILL.md`'s routing table already ordered it right after
`13-sources.md` (the natural start of the coding cluster: cmake/debugging/
python). Asked the user to confirm before a large mechanical rename; they chose
to close the gaps.

Renumbered 22 files so `references/` is contiguous `01`-`38` again:

| Old name | New name |
| --- | --- |
| `41-root-balanced-design-guidelines.md` | `14-root-balanced-design-guidelines.md` |
| `20-physics-objects-jets-btagging-met.md` | `18-physics-objects-jets-btagging-met.md` |
| `21-triggers-luminosity-pileup.md` | `19-triggers-luminosity-pileup.md` |
| `22-multivariate-classifiers-bdt-nn.md` | `20-multivariate-classifiers-bdt-nn.md` |
| `23-detector-systems-overview.md` | `21-detector-systems-overview.md` |
| `24-tracking-and-vertexing.md` | `22-tracking-and-vertexing.md` |
| `25-calorimetry-ecal-hcal.md` | `23-calorimetry-ecal-hcal.md` |
| `26-particle-identification.md` | `24-particle-identification.md` |
| `27-event-reconstruction.md` | `25-event-reconstruction.md` |
| `28-reconstruction-performance-and-truth-matching.md` | `26-reconstruction-performance-and-truth-matching.md` |
| `29-event-generation.md` | `27-event-generation.md` |
| `30-detector-simulation.md` | `28-detector-simulation.md` |
| `31-calibration-and-alignment.md` | `29-calibration-and-alignment.md` |
| `32-cosmic-ray-spectrum-and-composition.md` | `30-cosmic-ray-spectrum-and-composition.md` |
| `33-extensive-air-showers.md` | `31-extensive-air-showers.md` |
| `34-ground-based-detection-arrays.md` | `32-ground-based-detection-arrays.md` |
| `35-imaging-atmospheric-cherenkov.md` | `33-imaging-atmospheric-cherenkov.md` |
| `36-neutrino-astronomy.md` | `34-neutrino-astronomy.md` |
| `37-space-based-direct-detection.md` | `35-space-based-direct-detection.md` |
| `38-multimessenger-analysis.md` | `36-multimessenger-analysis.md` |
| `39-astroparticle-statistics.md` | `37-astroparticle-statistics.md` |
| `40-ams02-case-study.md` | `38-ams02-case-study.md` |

Content was not touched, only filenames and the cross-references to them - same
convention as the earlier "Renumber examples into canonical per-archetype order"
pass. Every other file in the skill that named one of these filenames (`SKILL.md`,
`README.md`, `scripts/validate_skill_bundle.py`, 16 `references/*.md` files that
cross-link each other, 7 `examples/*.md` files, and 14 `scripts/*.py` files whose
docstrings cite a reference by name) was updated by exact-string substitution of
the full old basename to the full new basename - safe because each topic slug is
unique, so this cannot cross-match an unrelated number. This file's own prior
dated entries above were deliberately left unchanged, exactly as the examples
renumbering pass handled it: a filename named in an earlier entry refers to that
file's *former* name at the time that entry was written; use the mapping table
above (or the examples-renumbering entry's own table, for that unrelated earlier
rename) to resolve a historical name to its current one.

Verification, in order: (1) the custom link/anchor checker re-run clean (only the
same two pre-existing historical-prose hits in this file); (2) a targeted grep for
every one of the 22 old basenames confirmed zero remaining occurrences anywhere
in the skill except this file's own historical entries; (3)
`python3 scripts/validate_skill_bundle.py` ("Bundle OK: 117 files present and
non-empty"); (4) `python3 -m unittest discover -s tests -v` (172 tests, all
passing, unaffected since no test references a `references/*.md` path). One
process note for future passes in this repo: the interactive shell used for this
work had a corrupted `IFS` (a stray NUL byte appended to the default
space/tab/newline set), which silently broke `for f in $files`-style newline word
splitting without any error - `for` loops over a multi-line variable in this
environment should be run inside an explicit fresh `/bin/bash -c '...'`
subprocess (or `unset IFS` verified to actually take effect first) rather than
trusting the persistent tool shell's default field splitting.

## Check and reorganize: rename multivariate-analysis reference (2026-09-16)

Per explicit user request to "check and reorganize hep-analysis skill (also file
name)", following a prior conversation pass that added a `## Regression targets`
section to `references/20-multivariate-classifiers-bdt-nn.md` (retitling its
heading to "Multivariate Classifiers and Regression: BDTs and Neural Networks in
Analysis" but not yet its filename). Ran a full audit before changing anything: a
link/anchor checker (Python, slugifying every Markdown heading the same way GitHub
does and resolving every `[text](target)` link's file path and `#anchor` against
it) across all 68 `.md` files in `hep-analysis/`, plus `scripts/validate_skill_bundle.py`
and `python3 -m unittest discover -s tests -v`. Result: no gaps in the `references/`
numbering (01-38, already contiguous from the 2026-09-15 reorg) and no broken links
- the checker's three flagged hits were all historical prose inside this file
quoting past states/placeholders in backticks, not live links. The one real finding
matched the request: the filename `20-multivariate-classifiers-bdt-nn.md` no longer
matched its content's scope now that it covers regression as well as classification.

Renamed `references/20-multivariate-classifiers-bdt-nn.md` to
`references/20-multivariate-analysis-bdt-nn.md` (`git mv`, preserving history) and
updated every cross-reference: `SKILL.md`'s routing table (link text and task
description), `references/18-physics-objects-jets-btagging-met.md`,
`references/23-calorimetry-ecal-hcal.md`, `references/29-calibration-and-alignment.md`,
`examples/09-gated-pipeline-alignment-propagation.md`, and
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`. Also updated `README.md`'s
prose description of this reference to mention regression targets, since it had not
been touched when the section was added. Left this file's own historical rename-log
entries (e.g. the 2026-09-15 table naming `22-multivariate-classifiers-bdt-nn.md` /
`20-multivariate-classifiers-bdt-nn.md`) unchanged, since they document past
filenames rather than linking to current ones.

Verification, in order: (1) the link/anchor checker re-run clean (same three
historical-prose hits, no new breakage); (2) a targeted grep confirmed zero
remaining occurrences of `20-multivariate-classifiers-bdt-nn` anywhere in the
skill except this file's own historical entries; (3)
`python3 scripts/validate_skill_bundle.py` ("Bundle OK: 117 files present and
non-empty"); (4) `python3 -m unittest discover -s tests -v` (172 tests, all
passing, unaffected since no test references this path).

## Add unified detector-measurement references 39-50 (2026-09-20)

Added twelve references derived from a graduate-level detector-study task
specification: `39-detector-measurement-framework.md` through
`50-detector-glossary.md` (framework and 14-question template, signal formation and
readout, gaseous/specialized tracking, timing, muon systems, noble-liquid/neutrino/
rare-event, Cherenkov variants and photosensors, performance metrics and residual
diagnostics, validation/systematics/combination, eight case studies plus checklists,
comparison tables, glossary). Wired into SKILL.md routing, README, 13-sources.md, and
`scripts/validate_skill_bundle.py`.

- The worked acceptance/efficiency/purity/fake/mis-ID example and the 20-value
  bias/resolution example in reference 46 were recomputed with Python (mean 0.395%,
  RMS 1.56%, median 0.15%, 1.4826*MAD 0.74%, tail fraction 5%; without the tail entry
  mean 0.074%, RMS 0.63%); the count table sums were checked by hand.
- The detector references are qualitative: no experiment-specific performance number is
  asserted; case studies are generic mechanisms. Textbook/journal citations in
  13-sources.md were matched against Crossref on 2026-09-20 and now carry DOIs (see the
  standalone references.md in docs/detector-principles for the full annotated list); that
  each work supports its stated use was not re-checked by re-reading.
- Not done: no new scripts or tests (content is methodological); the task's separate
  summary/comparison-table/references/glossary files were folded into references 48-50
  and 13-sources.md rather than shipped as five standalone documents; no cross-reference
  link check beyond `validate_skill_bundle.py` file presence and the grep below.

## Limitations

- ROOT is not installed in the validation environment, so `check_root_cpp_env.sh`
  correctly reports it missing (exit 1) rather than being runnable end to end, and the
  PyROOT-dependent scripts (`inspect_root_file.py`, `check_systematic_variations.py`,
  `compare_root_histograms.py`, `summarize_histogram_statistics.py`,
  `roofit_workspace_summary.py`) and the `.cpp`/`.C` template assets were checked for
  Python syntax only, not executed or compiled against real ROOT headers/libraries.
  This mirrors the same limitation already recorded for RooFit/pyhf/Combine snippets
  before the merge.
- Geant4 is not installed in the validation environment, and no detector
  simulation, reconstruction framework, generator, or conditions database was run.
  The detector, reconstruction, and simulation references
  (`23`-`31`) are methodological guidance checked for internal consistency and
  against the cited PDG and Geant4 documentation; they were not validated against
  a running simulation or a real detector's performance. The four new scripts
  compute design-level analytic estimates (Highland/Gluckstern, the three-term
  calorimeter parameterization, Bethe-Bloch without the density effect, Cherenkov
  kinematics with a single refractive index) and are not substitutes for a track
  fit, a shower simulation, or a ring-reconstruction algorithm.
- The `pid_separation_power.py` dE/dx mode omits the density-effect correction, so
  its numbers above the ionization minimum are optimistic; this is flagged in the
  output rather than silently applied.
- No real experiment data, full-production regression, coverage study, or
  collaboration approval was available. Helper tests do not establish the physical
  correctness of arbitrary analyses.
- The counting reference intentionally limits observed counts and known background to
  at most 500. Extreme tails can underflow in floating-point arithmetic. It is not a
  general statistics package and does not calculate CLs.
- The skill-creator `quick_validate.py` was not run in this environment.
- `geomagnetic_cutoff.py` computes the idealized vertical Stormer dipole cutoff only;
  it does not backtrace particles through a real (non-dipolar, epoch-specific) field
  model, so it does not capture off-vertical arrival directions or the geomagnetic
  penumbra, both flagged explicitly in its docstring and in
  references/37-space-based-direct-detection.md.
- `xmax_gaisser_hillas.py` evaluates a given or externally supplied Gaisser-Hillas
  parameter set; it does not fit those four parameters from raw (X, N) shower-profile
  samples, since that is a nonlinear least-squares problem outside this skill's
  closed-form, no-minimizer script convention (see references/33-extensive-air-showers.md).
- `cr_spectrum_powerlaw_fit.py` fits a spectral index directly from flux points; it
  does not forward-fold through an instrument's energy migration matrix, so it should
  not be used as a substitute for the forward-folding analysis a steeply falling,
  finite-resolution measurement actually requires (see
  references/39-astroparticle-statistics.md).
- `li_ma_significance.py` computes a single ON/OFF significance only; it does not
  itself apply a trials/look-elsewhere correction for a scan over multiple positions,
  energy bins, or time windows (see references/39-astroparticle-statistics.md).
- No real air-shower simulation (CORSIKA or similar), neutrino-telescope Monte Carlo,
  or IACT instrument-response package was run; the astroparticle references
  (`32`-`39`) are methodological guidance checked for internal consistency and
  against the cited textbook/journal sources, not against a running simulation or a
  real observatory's performance.
- `orbit_averaged_geomagnetic_cutoff.py` treats orbital latitude as geomagnetic
  latitude (ignoring the real dipole's tilt/offset from the rotation axis) and
  assumes a circular orbit; it is a planning-level estimate, not a substitute for
  backtracing a real ephemeris through a full field model (see
  references/40-ams02-case-study.md).
- `solar_modulation_force_field.py` implements only the one-parameter force-field
  approximation; it does not capture charge-sign-dependent drift, heliolatitude
  dependence, or short-timescale transients (Forbush decreases, SEP events), all
  flagged in references/37-space-based-direct-detection.md.
- `particle_ratio_with_uncertainty.py` uses first-order (delta-method/Gaussian) error
  propagation; it is not reliable when either yield's relative uncertainty is large,
  per its own docstring caveat.
- `references/40-ams02-case-study.md` is a methodological case study, not a
  reproduction of any AMS collaboration technical specification or published result;
  no specific numeric instrument parameter or measurement value from AMS-02 is
  asserted in this package, and the sources table intentionally does not pin an
  unverified URL for it.

In an environment with ROOT/PyROOT and skill-creator, additionally run the
ROOT-dependent scripts against a real file and `quick_validate.py`. In the target
analysis environment, perform the relevant physical and statistical checks described
in references/12-validation.md.

## AMS-02 case study slimmed (2026-09-20)

`references/38-ams02-case-study.md` was reduced to a role-level overview plus generic
lessons (no AMS numbers, publication lists, hardware-history dates, or
primary/secondary species catalogue) and now points to the sibling `ams-analysis`
skill for AMS-specific work. Reason: the removed specifics were not re-verified in that
pass and some were likely imprecise, and `ams-analysis` now holds source-traced AMS facts
in one place. The SKILL.md routing row, README sentence, and the file's links from
`references/44-...` and the four scripts that cite it remain valid. `validate_skill_bundle.py`
and the 172 unit tests pass after the change.
