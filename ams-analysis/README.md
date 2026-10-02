# ams-analysis

An Agent Skill for the Alpha Magnetic Spectrometer (AMS-02) on the ISS: detector subsystems, rigidity/charge/velocity/mass observables, and AMS-style charged cosmic-ray analyses (fluxes, ratios, leptons, antimatter searches, isotopes). It gives analysis decisions and source-traceable knowledge from public AMS literature only; it has no access to internal AMS data, calibrations, pass names, trigger bits, good-run rules or cuts, and does not invent them. It is not a generic HEP or statistics skill. It needs no MCP server, cloud account or paid service, and the helper scripts use only the Python standard library. All maintained instructions are in English.

## Installation and invocation

Keep the complete `ams-analysis/` folder.

- **Codex:** copy to `~/.codex/skills/ams-analysis/` and invoke `$ams-analysis`. `agents/openai.yaml` holds optional UI metadata.
- **Claude Code:** copy to `~/.claude/skills/ams-analysis/` (personal) or `.claude/skills/ams-analysis/` (project); invoke `/ams-analysis` or describe an AMS task. See the [Claude Code skills documentation](https://code.claude.com/docs/en/skills).
- **Antigravity:** copy to `.agents/skills/ams-analysis/` (workspace) or `~/.gemini/config/skills/ams-analysis/` (global); it triggers from `name` and `description`. See the [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other agents:** tell the agent to read `SKILL.md` first and follow its routing table.

## Quick checks

From the skill directory:

```bash
python3 scripts/validate_skill_bundle.py
python3 -m unittest discover -s tests
```

Helper scripts (each has `--help`; exit code 0 ok, 1 defects found, 2 input unreadable or rejected):

```bash
python3 scripts/ams_kinematics.py convert --from rigidity --to kinetic_energy_per_nucleon --value 20 --Z 2 --A 4 --mass 3.7274
python3 scripts/audit_analysis_spec.py tests/fixtures/spec_valid.yaml --markdown
python3 scripts/poisson_diagnostics.py cls-limit --n 3 --b 3 --cl 0.95
python3 scripts/render_source_index.py      # regenerate references/source-index.md with --write
python3 scripts/fetch_papers.py check-manifest
```

Other scripts in `scripts/`: `validate_covariance.py`, `validate_response.py`, `validate_evidence_ledger.py`, `likelihood_limits.py`, `template_fit.py`, `unfolding_diagnostics.py`, `statistical_toys.py`, `crdb_query.py`. A passing validator shows internal consistency, not physical validity. Results from the validation rounds are in [VALIDATION.md](VALIDATION.md).

## Coverage and boundaries

Covers:
- Tracker/magnet, TOF, TRD, ECAL, RICH, ACC and their observables
- Data quality, efficiencies, acceptance, backgrounds, template fits
- Flux and ratio analyses, electrons/positrons, antiprotons, rare antimatter, nuclei and isotopes
- Likelihoods, unfolding, covariance, low-count limits, calibration and systematics
- Time-dependent (solar-cycle, periodicity) analyses
- Structured analysis specifications with a deterministic auditor, and source/currency checks backed by `data/sources.json` and `data/claims.json`

Defers or declines:
- Generic ROOT, statistics and detector questions: `hep-analysis`
- Paper writing and citations: `academic-papers`
- Other experiments, unpublished AMS information, and replacing collaboration review, blinding or peer review

Source rules are in [references/source-policy.md](references/source-policy.md); the ledger tables are in [references/source-index.md](references/source-index.md).

## Example prompts

- "How does the RICH measure isotope mass and what limits it at high rigidity?"
- "Review my proton flux analysis: I use a bin-by-bin MC correction."
- "Design a 10-500 GV positron flux analysis and list the missing inputs."
- "Build a symbolic antiproton template likelihood with charge confusion."
- "What is the latest AMS antihelium result?"
- "Is four Bayesian unfolding iterations enough?"
