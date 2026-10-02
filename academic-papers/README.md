# academic-papers

An [Agent Skill](https://code.claude.com/docs/en/skills) for working with scientific
papers: reading and critiquing them, writing literature reviews, and drafting,
formatting, checking and submitting your own manuscript. Physics/HEP,
astroparticle and statistics/ML conventions are built in. It is not for running
fits or limits, AMS-02 analyses, or drawing diagrams (see the sibling skills below).
It needs no MCP server, cloud account or paid service.

## Install and invoke

Copy the `academic-papers` folder into your agent's skills directory.

- **Codex**: copy to `~/.codex/skills/`, reload skills, invoke `$academic-papers`.
  `agents/openai.yaml` supplies optional UI metadata.
- **Claude Code**: copy to `~/.claude/skills/` (personal) or `.claude/skills/`
  (project). Invoke `/academic-papers`, or let it trigger from the description.
- **Antigravity**: copy to `.agents/skills/` (workspace) or `~/.gemini/config/skills/`
  (global). It triggers automatically from the skill description; no explicit call
  is needed. See the [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other agents**: see that agent's documentation for how `SKILL.md` files are
  loaded. The format is the same portable one used by the other skills in this repo.

All maintained instructions are in English only.

## Quick checks

Python standard library only. Run from this directory.

```bash
python3 scripts/validate_skill_bundle.py      # bundle integrity
python3 -m unittest discover -s tests         # unit tests (add -v for detail)
```

Two helper scripts also run standalone, without any agent:

```bash
# Reading notes (CSV) -> markdown comparison table
python3 scripts/build_lit_matrix.py notes.csv --sort-by year -o lit_matrix.md

# Read-only pre-submission check of a directory of .tex/.bib files
python3 scripts/check_manuscript.py /path/to/manuscript-dir [--strict] [--style]
```

`check_manuscript.py` exits 0 when nothing is found and 1 otherwise, so it works as a
pre-commit or CI step. Run it with `-h` for what `--strict` and `--style` change.

Model-behavior checks call the model and cost money; results are in `VALIDATION.md`:

```bash
python3 tests/run_prompts.py --model sonnet --runs 2 --out /tmp/ap_runs
python3 ../hep-analysis/tests/routing_eval.py tests/trigger_queries.json \
    --target academic-papers --model haiku --runs 2
```

## Coverage and boundaries

Covers (one file per topic in `references/`, entry point `SKILL.md`):

- Finding, reading and critiquing papers; interpreting figures; literature reviews.
- Drafting and tightening sections; venue formatting (REVTeX, JHEP, JCAP, AASTeX,
  NeurIPS/ICML/ICLR/ACL, TMLR); LaTeX mechanics; figures and tables.
- Citations and BibTeX (INSPIRE-HEP, ADS, arXiv, DBLP); citation verification.
- Audits: reproducibility, equations and notation, logical and manuscript
  consistency, claim-to-evidence mapping, plagiarism and text reuse.
- Submission and review: cover letters, referee reports, rebuttals, revision
  tracking, preprint-to-journal diffs, Comments/Replies, errata.
- Related documents: posters and talks, preregistration, proposals,
  thesis-by-publication, release packaging, COI/ethics statements, and turning
  research code into a methodology write-up.

Defers to sibling skills:

- `hep-analysis`: running fits, limits, unfolding, ROOT/RooFit work.
- `ams-analysis`: AMS-02-specific analyses.
- `academic-diagrams`: drawing workflow, architecture and Feynman diagrams.
- `deep-learning`: PyTorch implementation and training questions.

Templates are in `assets/templates/`.

## Example prompts

- "Summarize this paper and tell me whether its significance claim is justified."
- "Build a related-work section from these ten papers and a comparison table."
- "Check that each citation in this introduction supports the claim it is attached to."
- "Reformat this manuscript from REVTeX to JHEP and list what changes."
- "Write a referee report for the attached PRD submission."
- "Draft a response to Reviewer 2 and track which sections the new result touches."
- "Clean up this BibTeX file against INSPIRE-HEP."
- "Turn this analysis code into a methodology section."
