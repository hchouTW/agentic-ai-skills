# Validation Report

Validation date: 2026-09-20. Environment: Python 3 standard library only.

## Files

`SKILL.md`; `README.md`; `agents/openai.yaml`; `data/sources.json`; `data/claims.json`; eight scripts (`poisson_diagnostics.py`, `validate_skill_bundle.py`, `ams_kinematics.py`, `validate_covariance.py`, `validate_response.py`, `validate_evidence_ledger.py`, `render_source_index.py`, `audit_analysis_spec.py`); seven test modules with `tests/fixtures/` (`test_poisson.py`, `test_bundle.py`, `test_kinematics.py`, `test_covariance.py`, `test_response.py`, `test_evidence_ledger.py`, `test_analysis_spec.py`); and fourteen references (the eleven below plus `analysis-artifacts`, `time-dependent-analysis` and `statistical-diagnostics`): `detector-and-observables`, `reconstruction-and-data-quality`, `charged-cosmic-rays`, `antimatter-and-leptons`, `nuclei-and-isotopes`, `efficiency-acceptance-backgrounds`, `inference-and-unfolding`, `calibration-mc-systematics`, `source-policy`, `source-index` (the source index and claim ledger, split from `source-policy`), and `tests-and-examples`. No assets.

## Structural checks

`python3 scripts/validate_skill_bundle.py` and `python3 -m unittest discover -s tests -v` (originally 7 tests: missing reference, orphaned reference, broken link, placeholder, unknown source ID, name drift, clean-bundle pass; now 224, see the extension section below). Checked: name equals folder, `agents/openai.yaml` matches, every reference linked from `SKILL.md`, all relative links and anchors resolve, every reference has the mandatory sections (when to read, contents, failure modes, required source classes, questions), every cited source ID exists in the index, at least 20 tests, no placeholders. No external skill validator was available in this environment; the repository's own bundle validator was used, and `skill-router`'s validator still passes with the new sibling folder.

## Source verification

Metadata for 30 AMS PRLs (2013-2026), the Phys. Rept. Part II review, detector NIM A papers and the antihelium/antideuteron literature came from INSPIRE-HEP (2026-09-20). The AMS detector page and the AMS publications page (dated list, most recent PRL 136, 241002 of 17 June 2026) were fetched (claims C13, C34). **Main-article full text was read** for nine open-access papers (Unpaywall/publisher PDFs, `pdftotext`): positron flux, electron flux, antiproton, proton, He isotopes, deuterons, Li isotopes, heavy nuclei P-Ca, and B/C for its data period only. Their **Supplemental Material was not opened**; the Phys. Rept. review could not be downloaded (HTML returned); S02 and every metadata-only row are unread. Ledger claims C20-C35 hold documented AMS practice with context (selection, cutoff factor 1.2, template fits, unfolding, isotope resolution functions). Unverified: NIM A 869 papers (S19), Read CLs (S40), hardware-history dates, the type of the antihelium talks/theses (S24-S25). Antihelium and antideuteron: no AMS peer-reviewed paper found in INSPIRE (search-limited absence claims C14, C19). Source count: 40 indexed rows (S01-S29, S30-S40); some rows group several papers.

## Behavioral results

Method: fresh sub-agents given only `SKILL.md` and the references (never the rubric) answered each prompt, loading references as routed; no web access. Rubric: five dimensions x 0-2 (max 10 per test).

**Round 1 (before full-text upgrade), author-graded (self-audit):** suite T01-T24, 235/240 = 97.9%, no blocking failure; forward set F1-F7, 65/70 = 92.9%, no blocking failure. Failures found and fixed (narrowest change each):

| Observed failure | Fix |
|---|---|
| "At most one reference" conflicted with "consult `source-index` before any number" | Routing paragraph allows `source-index` as the single exception |
| Ambiguous "+ species file" | Defined per species in `SKILL.md` |
| `tests-and-examples` presented as an ordinary reference though it holds rubrics | Routing row marked maintainer-only |
| No repair procedure for non-PSD covariance | New subsection in `inference-and-unfolding` |
| No guidance for fraction vs flux in a model constraint | New subsection in `antimatter-and-leptons` |
| No antideuteron search record | INSPIRE search run; S28/C19 added |
| Future-dated or ambiguous-year citation handling | Added to `source-policy` |
| Boundary/non-regular asymptotics, Fréchet bound, He/O "same selection", rest energies, charge-dependent transmission absent | Added to the responsible reference |
| Wording "e.g. four iterations" echoed a test prompt | Reworded |

**Round 2 (after full-text upgrade), graded by an independent Opus agent that held the rubric and the extracted paper text and grepped every AMS claim:** 16 answers (new documented-practice tests T25-T28, re-runs of T04, T17, T18, T19, and unseen forward prompts F8-F15 including a non-AMS boundary case): **156/160 = 97.5%, no blocking failure**; every quoted AMS number was located verbatim in the paper texts. The grader is a model, not a human, and shares a model family with the answerers.

Defects the grader found and what was done:

| Defect | Action |
|---|---|
| C23 mis-grouped the antiproton paper's four systematic sources | Rewritten to the paper's grouping, with a note to re-read before quoting a breakdown |
| C30 and a T18 answer over-scoped the L1 charge-template fit to all interaction background above L2 | Scoped to interactions between L1 and L2 in the ledger and `nuclei-and-isotopes` |
| C26 gave the electron range as 0.5 GeV-1 TeV | Corrected to 0.5 GeV-1.4 TeV (28.1 x 10^6 electrons) |
| C04-C12 still tagged "abstract only" though full text was read; an "S10 date only" note was copied onto eight rows | Limitation text and level column corrected |
| Positron cutoff significance stated only as ">4σ" | C35 added (4.07σ in the body; 5σ not supported) |
| One answer said the per-region fit variables were only in the Supplement; one attributed the BDT input list to S04 | Answer-side slips; ledger and `antimatter-and-leptons` already state them correctly (C22); not re-run |
| Two non-AMS ROOT slips in F15 (Crystal Ball tail sign convention; the ROOT version that added `RooCrystalBall`) | Outside the skill's scope; not corrected here |

Structural checks at that time: `python3 scripts/validate_skill_bundle.py` and 7 unit tests passed after the final edits; `skill-router` (now routing to `ams-analysis`) and its 7 tests pass.

## Extension: executable checks, structured ledger, artifacts (actual results)

Run on 2026-09-20 from the skill directory, Python 3 standard library only. Baseline before any edit: `python3 scripts/validate_skill_bundle.py` printed `Bundle OK: 17 required files present` and `python3 -m unittest discover -s tests` ran 7 tests, all OK.

| Command | Result |
|---|---|
| `python3 scripts/validate_skill_bundle.py` | `Bundle OK: 38 required files present, links and anchors resolve.` (exit 0, after the optional statistics phase was added; 35 before it) |
| `python3 -m unittest discover -s tests` | 238 tests, OK (bundle 18, kinematics 25, covariance 30, response 35, evidence ledger and renderer 38, analysis specification 78, Poisson diagnostics 14; 224 before the optional statistics phase) |
| `python3 scripts/validate_evidence_ledger.py --today 2026-09-20` | status pass; 47 sources, 50 claims (after the later S41-S47 / C36-C50 additions; the migration itself was 40 and 35); no errors, no warnings; 11 notes, all of the kind "no claim cites this source" (S03, S07, S11, S18, S19, S20, S21, S23, S27, S38, S40), no stale dates as of 2026-09-20 |
| `python3 scripts/render_source_index.py` | `source-index.md is in sync with data/*.json` (exit 0) |
| `python3 scripts/audit_analysis_spec.py tests/fixtures/spec_valid.json` | verdict `acceptable with open inputs` (0 errors, 0 warnings, 1 proposal, 2 unresolved) |
| `python3 scripts/validate_covariance.py` on `cov_valid.json` / `cov_indefinite.json` | pass (exit 0) / fail with `not_psd`, correlations inside bounds (exit 1) |
| `python3 scripts/validate_response.py tests/fixtures/response_valid.json` | pass (exit 0) |
| `skill-router` `scripts/validate_skill_bundle.py` and its 7 tests | OK |

Test design: every validator has a valid fixture and mutation tests that introduce one defect and assert the intended diagnostic code (asymmetric, indefinite, nearly singular, malformed and block-inconsistent covariances; transposed, inefficient, empty-bin, double-counted, lost-probability and non-identifiable responses; duplicate, broken, over-strong and cyclic ledger records; duplicated corrections, unsupported cancellations, invalid low-count and Gaussian-core assumptions, scale systematics on final values, undocumented AMS numbers). Kinematics reference values were computed by hand from `p = |Z|R` and `E = sqrt(p^2 + m^2)`, and Jacobians are checked against finite differences. The bundle validator additionally checks that the ledger is valid, that `source-index.md` is in sync, that every script documents usage and exit codes, prints `--help`, and has a test module, and that `SKILL.md` stays within 120 lines (86 now).

**Behavioral evaluations of the extension (round 3, self-graded).** Method: six fresh sub-agents, each given one of T29-T34 and told to read `SKILL.md` and only the references it routes to (never the rubric file); no web access; answers graded by the author against the observable decisions listed in `references/tests-and-examples.md`. The grader is the same model family as the answerers and knew the rubric, so this is a self-audit, not independent evidence. One sample per prompt.

| Test | Result | Observed failure and action |
|---|---|---|
| T29 measurement brief | Pass | Structured brief with species, A and mass stated, bins left unsupplied, AMS numbers claim-ID'd. Minor: attributed the cutoff-factor variation "1.0-1.4" to S06 and S08; the ledger has 1.2-1.4 for S08 (C23) and 1.0-1.4 for S13 (C27). Cause was loose wording in `charged-cosmic-rays`; reworded there. Not re-run. |
| T30 covariance/response review | Pass | Verdict first; called rho = -1.3 a construction error; refused to clip silently; flagged possible double-counted efficiency; pointed to both validators. |
| T31 correction chain | First run partial, re-run pass | First run did not propose the auditable specification fields and ranked the livetime-times-exposure defect fourth. Fix: one clause in the `SKILL.md` scripts block. Re-run after the fix named the exposure double count and proposed `effect_id`, `response.includes`, `estimator.applies`; one line ("removes the affected time twice") is loosely worded. |
| T32 time-dependent ratio | Pass | Per-bin exposure and per-sign cutoff, ratio cancellations classified, covariance over (time, rigidity), predefined period band with trial factor and control series, evidence gap stated, 108-day binning not presented as a rule. |
| T33 superseded or fabricated source | Pass | Declined "latest", did not summarize the 2029 citation, gave verification date and verified alternatives. Did not use the exact phrase "superseded in range and statistics by S03". |
| T34 non-AMS question | Pass | Did not use the skill; generic RooFit answer. |

After the ledger was extended with the full-text time-structure papers (C43-C49), T32 was re-run once: pass; it used C39-C48 with correct scope and kept the Supplemental-Material items unknown, with one slip (it said published AMS lepton results are binned in energy; the daily lepton papers use rigidity), fixed by a sentence in `time-dependent-analysis`; not re-run. No blocking failure occurred. **Regression spot-check after the routing and ledger edits (self-graded, one sample each):** five prompts from the original suite, T05 (proton flux review), T09 (helium conversion), T20 (false E/R premise), T21 (fabricated citation) and T24 (zero-event limit), all passed against their existing rubrics with no blocking failure; T09 ran `ams_kinematics.py` and matched the hand values.

A second regression batch ran ten more original tests (T02 RICH isotope mass, T07 deuteron/proton design, T08 antiproton review, T12 Wilks at a boundary, T13 two 99% efficiencies, T15 four unfolding iterations, T17 latest antihelium, T19 hallucination trap, T22 non-AMS Wilks, T23 ACC): all passed their existing rubrics with no blocking failure, self-graded, one sample each. Minor observations, none fixed: T23 was longer and more templated than its "short answer" rubric wants and attributed shower/backsplash rejection to a claim that only supports the side-entry veto role; T08 cited the antiproton template-fit practice to claim C26 (the electron-flux claim; C22 is the correct one) and called two event counts a "ratio"; T17 asserted the verification date was "today's date"; T19 floated "for example 90%" as an efficiency (labeled a proposal); T07 gave an unsourced "about 10^-2" for D/p while saying it quoted no AMS number.

A third batch ran the remaining thirteen originals (T01, T03, T04, T06, T10, T11, T14, T16, T18, T25, T26, T27, T28): all passed with no blocking failure (self-graded, one sample each). Minor observations: T01 described the quoted charge resolution as "inner-tracker" where the ledger (C21) says "tracker"; T26 opened with a generalization ("public AMS flux analyses ... 1.2") before its scoping caveats and listed S47 among supporting sources though only S41 states the variation; T10 cited the RICH velocity resolution to C28 (C21 holds it); T18 and T17 called the verification date "today's date". T03 quoted "17 radiation lengths" for the ECAL from `detector-and-observables`, a figure that had no ledger claim: it was checked against the S04 main article (which states it) and added as claim C50, and the reference row now cites it.

All 28 original tests and the six new ones (T31 and T32 twice) have now been re-run at least once since the extension; every run passed on its final attempt, with T31's first run partial (fixed).

**Independent grading (different model, rubric read by the grader, answers regenerated and saved to files; nine prompts: T05, T08, T24, T29-T34).** Result: 7 PASS (three borderline at exactly 90%) and 2 FAIL, core score 76/84 = 90.5%, but the suite fails on one blocking failure. This is stricter than the self-grades above, which had passed all nine; treat the self-grades as too lenient. Findings, each checked by the author against the answer file and the tools:

- **T29, FAIL (blocking):** the answer wrote "3 TV corresponds to pc = 3000 GeV" for helium (|Z| = 2), where `ams_kinematics.py` returns 6000 GeV/c, and its own T/A of 1499 GeV/n needs 6000: rigidity used as momentum at the top edge. Also cited claims without the specific IDs for the cutoff-factor variation (C27) and the quadrature combination (C33).
- **T24, FAIL (score, 80%):** it said the classical zero-count limit is independent of the background; the classical limit is `-ln(alpha) - b` (the script returns 1.996 for n=0, b=1). Also lumped S26 and S27 (third-party theory, reviews) with S24-S25 (unverified-type records).
- **T08, borderline pass:** attributed the antiproton template-fit facts to C26 and C25 (electron and positron claims) where C22 is correct.
- **T05, borderline pass:** attached the 0.1% unfolding convergence rule to S06 (it is C23, S08 only) and the 1.2 cutoff factor to S14 and S15, whose claims (C29, C30) contain no cutoff statement.
- **T32, borderline pass:** claim groupings partly wrong (C22 quoted for an S04/S05 method; C43-C47 called Bartels-rotation results though they are daily; C44 quoted without its proton, daily scope).
- **T33, borderline pass:** missed the publication-date versus data-taking-period distinction; one garbled sentence.
- **T30, T31, T34: pass** (T31 strongest; T34 has two small non-AMS RooFit inaccuracies).
- Patterns: correct fact with the wrong claim ID; a claim's scope widened to sibling papers. No answer invented an AMS cut, efficiency, systematic size, candidate count or publication.

Fixes made in response (narrow): one sentence in `statistical-diagnostics` that the classical zero-count limit shrinks with the expected background; in `SKILL.md`, a rule to state every converted value from the script output for that exact input, and a rule to cite the claim ID from its own row and check its scope covers the statement. T29, T24 and T08 were then re-run once, and the author checked only the specific defects the grader found (no second independent grading): T29 now gives p = 6000 GeV/c for 3 TV helium, consistent with T/A = 1499 GeV/n (fixed); T24 now states that the classical zero-count limit is `-ln(1-CL) - b` and not background-independent, after running the script (fixed); T08 now cites C22, but as the range "C22-C26", which still includes the positron and electron claims (only partly fixed).

**Independent grading, round 2 (same grader model; fresh answerers on the fixed prompts T05, T08, T24, T29, T32, after the reference citation fixes).** All five PASS at exactly the 90% bar (9/10 each; source discipline 1, the other four dimensions 2), no blocking failure; suite 45/50 = 90.0%, so it passes with no margin. The grader re-ran the scripts and confirmed the numbers attributed to them (for example 6000 GeV/c and 1499.07 GeV/n for 3 TV helium, and 1.996 for the n=0, b=1 classical limit). The two round-1 failures are no longer reproduced in this one sample. Remaining defects it listed, ranked, all in the answers and not blocking:

1. T24 said "neither species has a peer-reviewed AMS search paper" and then cited the AMS-01 antihelium limit (S22); C14 is the governing claim. Also a source range "S24-S28" mixing tiers.
2. T32 attached the 100 GeV data/MC template boundary of C24 to the background templates (it belongs to the positron signal template); cited C36, C40, C41 for "the 27-day term is the dominant variation" (not stated); cited C31 and C51 for a "varied" cutoff factor (the variation is C23, C27, C49).
3. T05 stated the 1.2 x cutoff as general practice without mentioning C51 (the daily proton analysis used a cutoff computed from AMS data).
4. T29 attached the estimator formula to C31 and C30 (it is in C43, C46, C49) and widened the TRD role beyond C13; its selection ledger was thin. T05 and T08 opened by saying no AMS numbers are quoted and then quoted ledger numbers; T08 labeled an inferred negative [Documented]; T05 did not ask for the track configuration.

The dominant residual pattern is still claim scope and claim-ID precision (source discipline), not physics. One sample per prompt at the threshold is weak evidence: it shows the earlier failures are not reproduced, not that they are gone.

Not done: repeated samples per prompt, and independent grading of the other 25 tests (only nine prompts were independently graded, five of them twice).

Optional statistics phase, implemented in a deliberately narrow form: `scripts/poisson_diagnostics.py` (exact Poisson upper limit for a known background, Garwood interval, seeded coverage; 14 tests against known values, e.g. the zero-count bound -ln 0.05, n=0 and n=1 intervals, and reproducible coverage) with `references/statistical-diagnostics.md`. Its output, a classical limit with a warning when it is unphysical, is not a Feldman-Cousins or CLs construction. No behavioral evaluation was run for it.

Not implemented: the optional network refresh of the ledger, and the rest of the statistical-validation phase (profile-likelihood boundary behavior, Feldman-Cousins and CLs, finite-template effects, unfolding closure/pull/prior/regularization scans, forward-fold versus unfolding comparison, correlated ratio toys), listed in `statistical-diagnostics` as deliberately left out.

### Ledger migration: differences requiring human review

The 40 source rows and 35 claim rows were parsed mechanically from the previous `source-index.md`, then structured by hand. Every ID, title, author, year, locator, tier, level, claim text, location, scope and limitation cell was carried over; the rendered tables equal the previous ones except for two cosmetic lines:

1. S10 level: `full-text downloaded; only its data period was read` is now `full-text (downloaded; only its data period was read)` (structured as level plus note).
2. C14 sources: `S22, S24-S26` is now `S22, S24, S25, S26` (ranges of fewer than four IDs are not collapsed).

Judgement calls a human should confirm (each is new structure, not new evidence):

- `verification_strength` per claim: C01-C12 abstract-level (their source may be full-text, as the old limitation text says); C13 and C34 `page`; C14, C15, C16, C17, C19 `metadata-only`; C18 `not-opened` (the old text says PDG was not opened); C20-C33 and C35 `full-text`.
- `numeric_quotation_allowed` is false for C13 (website numbers carry no selection context), C14, C15, C16, C17, C18, C19, and true elsewhere.
- `support_kind`: C14 and C19 `absence_search`; C15 `third_party_context` (it rests on Tier 5/6 titles); C17 and C18 `general_method`; all others `primary`.
- `tier`: for grouped or ranged rows the first tier is stored as `tier` and the range in `tier_range` (S26 `[5, 6]`, S28 `[3, 6]`); the original text is kept in `tier_text`.
- Supersession: S02 `superseded_by` S03 and S03 `supersedes` S02, taken from claim C03's limitation ("superseded in range/statistics by S03"); no other relation was added.
- `publication_date` is year-level except S09, S13, S14, S15, whose exact dates come from claim C34 (AMS publications page); `data_taking_period` is filled only where a claim states it (S04, S06, S08, S09, S10, S12-S15); `inspire_record_id` is null everywhere because the old ledger did not record it.
- S19 and S40 have `access_date: null` (the old index says not verified this session); every other row has 2026-09-20.
- DOIs for grouped rows S03 and S18 were expanded from the old shorthand (`.121102`, `.05.010`) to full DOIs; S16 and S20 keep only the one DOI the old ledger listed.
- Existing inconsistency, not resolved: the old "Items lacking verification" bullet listed S05 as metadata-only while its table row and claim C26 treat it as full-text (main article only). The table row was kept and a note added to S05.

## Unresolved gaps and limitations

- Supplemental Material of all papers, the Phys. Rept. review (S01), S02 and all metadata-only rows remain unread; per-cut definitions, tables, and the BDT charge-confusion input lists beyond what the main articles state are not in the skill.
- The ledger corrections after round 2 were not re-graded.
- Round-3 evaluations of T29-T34 are single-sample and self-graded; see the table above.
- The independent grader is a model; a human expert review of the physics and of the AMS-practice paragraphs is still advisable.
- Currency: the index is dated 2026-09-20; any "latest" question needs a live INSPIRE or ams02.space check (both were used to build the index).
- Hardware-era history, trigger/DAQ/thermal specifics, good-run rules, pass names, calibration constants: not public here and deliberately absent.
- `hep-analysis` reference 38 was not modified; it remains a short overview.
- Time-dependent evidence gap: the time-structure, periodicity and nuclei solar-modulation PRLs (S16, S20) were later read at main-article level (records S41-S47, publisher PDFs on 2026-09-20; claims C36-C42 abstract-level, C43-C49 method claims; Supplemental Material text of S41, S42, S44, S47 read later on 2026-09-21, claims C54-C58, tables not transcribed), so `time-dependent-analysis` now carries documented method items C43-C49 alongside C07, C09, C10, C16, C27, C29, C31 and C36-C42; AMS livetime, time-dependent efficiency, period correlation and periodicity-search practice are marked unknown.
- The audit and validators check internal consistency and completeness only; they do not establish that a covariance, response, or specification is physically right. The low-count threshold (20 expected counts) in the auditor is a triage proposal, and the response and covariance tolerances are configurable defaults, not derived values.
- The auditor scans free-text selection definitions for numeric thresholds only heuristically; AMS numbers must be registered in `parameters` to be traced.
- No human expert has reviewed the ledger structuring choices above or the new references.
