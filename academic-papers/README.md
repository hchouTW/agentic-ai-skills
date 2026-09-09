# academic-papers

A portable [Agent Skill](https://code.claude.com/docs/en/skills) covering the full
lifecycle around scientific papers: reading and critically understanding one or many
papers, synthesizing them into a literature review, and drafting, formatting, and
submitting a manuscript of your own. Physics/HEP conventions (REVTeX, JHEP,
INSPIRE-HEP, PRL/PRD-style significance language, look-elsewhere effect) are built in,
alongside astroparticle-physics and cosmic-ray conventions (JCAP/AASTeX/Elsevier
venues, ADS/bibcode citations, exposure vs. luminosity, pre-trial vs. post-trial
significance, skymap and energy-spectrum figures), statistics/machine-learning
conventions (NeurIPS/ICML/ICLR/ACL-family/JMLR/TMLR venues, reproducibility
checklists, arXiv/DBLP/ACL-Anthology citations, single-shot OpenReview rebuttals,
p-value/effect-size reporting language), and general academic reading and writing
guidance. Self-contained: no MCP server, cloud account, or paid service required.

Designed to sit alongside `hep-analysis` and `deep-learning` in the
[agentic-ai-skills](https://github.com/hchouTW/agentic-ai-skills) bundle — this skill
owns the reading/writing/formatting/submission side once there's a paper to
understand or a result to write up.

## What's inside

```
academic-papers/
├── SKILL.md                      # entry point: reading + writing workflows, quick-reference tables
├── README.md                     # this file
├── VALIDATION.md                 # what the integrity checker verifies
├── references/
│   ├── reading-papers.md         # three-pass reading method, claims-vs-evidence, critical-reading checklist
│   ├── literature-review.md      # organizing a review/related-work section, comparison matrices, synthesis
│   ├── paper-structure.md        # section-by-section writing guidance (+ theory/thesis/proceedings/astroparticle/statistics-ML/outreach variants)
│   ├── astroparticle-and-cosmic-ray-papers.md  # venue/structure/citation/figure conventions for cosmic-ray & astroparticle papers
│   ├── statistics-and-ml-papers.md  # venue/structure/citation/review-process conventions for statistics & ML papers
│   ├── latex-and-formatting.md   # REVTeX/JHEP/JCAP/AASTeX/Springer/NeurIPS/ICML/ICLR/ACL setup, compile errors, length-limit tactics
│   ├── figures-and-tables.md     # publication figure design, captions, table conventions, skymaps/spectra/learning curves/ablation tables
│   ├── citations-and-bibliography.md  # INSPIRE-HEP/ADS/arXiv/DBLP/ACL-Anthology workflow, BibTeX hygiene, supplemental-data linking
│   ├── scientific-style.md       # sentence-level prose guidance, significance-language & statistical-reporting conventions
│   └── submission-and-peer-review.md  # pre-submission checklist, cover letters, referee responses, conference rebuttals
├── scripts/
│   ├── build_lit_matrix.py       # CSV of reading notes -> formatted markdown comparison table
│   ├── check_manuscript.py       # pre-submission checker for the user's .tex/.bib files
│   └── validate_skill_bundle.py  # integrity checker for this skill bundle itself
├── tests/
│   ├── test_build_lit_matrix.py
│   ├── test_check_manuscript.py
│   └── test_skill_bundle.py
└── assets/templates/
    ├── reading_notes_template.md # structured single-paper reading notes shape
    ├── paper_skeleton.tex        # venue-agnostic starting skeleton
    └── references.bib            # example INSPIRE-HEP-style .bib entry
```

## Installation

Copy the folder into your agent's skill directory:

```bash
# Claude Code (personal)
cp -r academic-papers ~/.claude/skills/

# Claude Code (project-scoped)
cp -r academic-papers .claude/skills/

# Codex
cp -r academic-papers ~/.codex/skills/
```

## Per-agent invocation

- **Claude Code / Claude.ai**: the skill triggers automatically when a request
  matches its `description` (summarizing/critiquing a paper, building a literature
  review, drafting or formatting a manuscript, bibliography cleanup, referee
  responses, etc.) — no explicit invocation needed. You can also just say "use the
  academic-papers skill".
- **Codex** and other skill-aware agents: consult that agent's own documentation for
  how installed `SKILL.md` files are surfaced; the file format here follows the same
  portable convention used by the other skills in this bundle.

## Using the bundled scripts directly

`build_lit_matrix.py` and `check_manuscript.py` can both be run standalone,
independent of any agent:

```bash
# Turn reading notes into a comparison table for a literature review
python3 scripts/build_lit_matrix.py notes.csv --sort-by year -o lit_matrix.md

# Pre-submission check of a manuscript directory
python3 scripts/check_manuscript.py /path/to/manuscript-dir
```

`check_manuscript.py` exits `0` if nothing is found and `1` otherwise, so it's usable
as a pre-commit hook or CI step in a manuscript's own git repository.

## Verifying this skill bundle

Every skill in the parent repo ships an integrity checker and unit tests (Python
standard library only):

```bash
cd academic-papers
python3 scripts/validate_skill_bundle.py
python3 -m unittest discover -s tests -v
```

See `VALIDATION.md` for exactly what is checked.
