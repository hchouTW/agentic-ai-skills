# AMS-02 Detector and Physics Analysis Skill

A portable Agent Skill (English) for the Alpha Magnetic Spectrometer (AMS-02). Its core is `SKILL.md` (routing, workflow, invariants, source rules) plus references resolved through relative paths. It needs no MCP server, cloud account, or paid service. It supplies analysis decisions and source-traceable knowledge from **public** AMS literature only; it has no access to, and never invents, internal AMS data, calibrations, pass names, trigger bits, good-run rules, or cuts.

## Installation and invocation

Keep the complete `ams-analysis/` folder.

- **Claude Code:** copy to `~/.claude/skills/ams-analysis/` (personal) or `.claude/skills/ams-analysis/` (project); invoke `/ams-analysis` or describe an AMS task. See the [Claude Code skills documentation](https://code.claude.com/docs/en/skills).
- **Codex:** copy to `~/.codex/skills/ams-analysis/` and invoke `$ams-analysis`. `agents/openai.yaml` supplies optional UI metadata and leaves automatic discovery on.
- **Antigravity:** copy to `.agents/skills/ams-analysis/` (workspace) or `~/.gemini/config/skills/ams-analysis/` (global); it triggers from the `name`/`description`. See the [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other agents:** tell the agent to read `SKILL.md` first and follow its routing table.

Pairs with `hep-analysis` (generic ROOT/statistics/detector background; its reference 38 is a short AMS overview that this skill supersedes for depth) and `academic-papers` (paper writing/citations).

## Quick checks

From the skill directory:

```bash
python3 scripts/validate_skill_bundle.py
python3 -m unittest discover -s tests -v
```

Standard library only. The deterministic tools (each has `--help`; exit code 0 ok, 1 defects found, 2 input unreadable or rejected; none modifies user data):

```bash
python3 scripts/ams_kinematics.py convert --from rigidity --to kinetic_energy_per_nucleon --value 20 --Z 2 --A 4 --mass 3.7274
python3 scripts/validate_covariance.py tests/fixtures/cov_valid.json
python3 scripts/validate_response.py tests/fixtures/response_valid.json
python3 scripts/audit_analysis_spec.py tests/fixtures/spec_valid.json --markdown
python3 scripts/validate_evidence_ledger.py
python3 scripts/render_source_index.py          # add --write after editing data/*.json
```

`data/sources.json` and `data/claims.json` are the machine-readable source and claim ledger; the tables in `references/source-index.md` are generated from them. The kinematics results are general-method arithmetic, never measured AMS performance, and a passing validator shows internal consistency, not physical validity. See [VALIDATION.md](VALIDATION.md) for structural checks, behavioral test results, forward tests, gaps, and limitations.

## Coverage and boundaries

Covers: Tracker/permanent magnet, TOF, TRD, ECAL, RICH, ACC and cross-subsystem complementarity; rigidity, charge, velocity, mass, energy definitions and conversions; reconstruction, data quality and conditions model; charged cosmic-ray flux/ratio blueprints; electrons/positrons, antiprotons, rare antimatter; nuclei and isotopes; conditional efficiencies, acceptance, exposure, background ledgers, template fits; response/likelihood/covariance, unfolding vs forward folding, low-count inference; calibration, MC provenance, systematics; a structured analysis specification with a deterministic auditor; kinematics, covariance and response validators; time-dependent analysis decision logic; source tiers, currency checks, and a machine-readable claim-to-source ledger (verification date 2026-09-20).

Does not cover: generic HEP or generic statistics questions with no AMS tie (use `hep-analysis`); other experiments as AMS practice; unpublished AMS information; replacement of collaboration review, blinding, or peer review. Main-article full text was read for nine open-access Tier 1 papers (positron, electron, antiproton, proton, He/deuteron/Li isotopes, heavy nuclei; B/C for its data period only), so documented AMS practice is quoted with context for those; their Supplemental Material, the Phys. Rept. review, and the remaining ledger rows were not read. See [references/source-index.md](references/source-index.md).

| Reference | Purpose |
|---|---|
| [detector-and-observables](references/detector-and-observables.md) | subsystem response chains, observables, matrix |
| [reconstruction-and-data-quality](references/reconstruction-and-data-quality.md) | objects, cut ledger, conditions model |
| [charged-cosmic-rays](references/charged-cosmic-rays.md) | flux and ratio blueprints |
| [antimatter-and-leptons](references/antimatter-and-leptons.md) | e±, antiprotons, rare antimatter |
| [nuclei-and-isotopes](references/nuclei-and-isotopes.md) | charge ladder, isotopes |
| [efficiency-acceptance-backgrounds](references/efficiency-acceptance-backgrounds.md) | efficiencies, exposure, backgrounds, templates |
| [inference-and-unfolding](references/inference-and-unfolding.md) | likelihood, covariance, unfolding, limits |
| [calibration-mc-systematics](references/calibration-mc-systematics.md) | calibration, MC, systematic ledger |
| [analysis-artifacts](references/analysis-artifacts.md) | analysis specification, ledgers, response card, review report, checker scripts |
| [time-dependent-analysis](references/time-dependent-analysis.md) | temporal flux, solar modulation, periodicity, joint fits across periods |
| [source-policy](references/source-policy.md) / [source-index](references/source-index.md) | source rules and ledger |
| [tests-and-examples](references/tests-and-examples.md) | worked examples and rubric tests |

## Example prompts

- "How does the RICH measure isotope mass and what limits it at high rigidity?"
- "Review my proton flux analysis: I use a bin-by-bin MC correction."
- "Design a 10-500 GV positron flux analysis and list the missing inputs."
- "Build a symbolic antiproton template likelihood with charge confusion."
- "What is the latest AMS antihelium result?" (triggers the currency check)
- "Is four Bayesian unfolding iterations enough?"
