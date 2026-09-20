# Validation Report

Validation date: 2026-09-20. Environment: Python 3 standard library only.

## Files

`SKILL.md`; `README.md`; `agents/openai.yaml`; `scripts/validate_skill_bundle.py`; `tests/test_bundle.py`; and eleven references: `detector-and-observables`, `reconstruction-and-data-quality`, `charged-cosmic-rays`, `antimatter-and-leptons`, `nuclei-and-isotopes`, `efficiency-acceptance-backgrounds`, `inference-and-unfolding`, `calibration-mc-systematics`, `source-policy`, `source-index` (the source index and claim ledger, split from `source-policy`), and `tests-and-examples`. No assets. The validator script is the only script; it exists because this repository ships one per skill.

## Structural checks

`python3 scripts/validate_skill_bundle.py` and `python3 -m unittest discover -s tests -v` (7 tests, each induced defect caught: missing reference, orphaned reference, broken link, placeholder, unknown source ID, name drift; plus a clean-bundle pass). Checked: name equals folder, `agents/openai.yaml` matches, every reference linked from `SKILL.md`, all relative links and anchors resolve, every reference has the mandatory sections (when to read, contents, failure modes, required source classes, questions), every cited source ID exists in the index, at least 20 tests, no placeholders. No external skill validator was available in this environment; the repository's own bundle validator was used, and `skill-router`'s validator still passes with the new sibling folder.

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

Structural checks: `python3 scripts/validate_skill_bundle.py` and 7 unit tests pass after the final edits; `skill-router` (now routing to `ams-analysis`) and its 7 tests pass.

## Unresolved gaps and limitations

- Supplemental Material of all papers, the Phys. Rept. review (S01), S02 and all metadata-only rows remain unread; per-cut definitions, tables, and the BDT charge-confusion input lists beyond what the main articles state are not in the skill.
- The ledger corrections after round 2 were not re-graded.
- The independent grader is a model; a human expert review of the physics and of the AMS-practice paragraphs is still advisable.
- Currency: the index is dated 2026-09-20; any "latest" question needs a live INSPIRE or ams02.space check (both were used to build the index).
- Hardware-era history, trigger/DAQ/thermal specifics, good-run rules, pass names, calibration constants: not public here and deliberately absent.
- `hep-analysis` reference 38 was not modified; it remains a short overview.
