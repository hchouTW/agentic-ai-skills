# academic-papers

A portable [Agent Skill](https://code.claude.com/docs/en/skills) covering the full
lifecycle around scientific papers: reading and critically understanding one or many
papers, synthesizing them into a literature review, and drafting, formatting, and
submitting a manuscript of your own — plus verification/auditing modes (citation
verification, reproducibility, equation/notation, logical-consistency, plagiarism,
manuscript-consistency), cross-version reconciliation (revision tracking,
preprint-to-journal diffing, multi-venue reformatting, Comment/Reply, errata), and
adjacent document types (posters/talks, preregistration, grant proposals,
thesis-by-publication, artifact packaging, COI/ethics statements). Physics/HEP
conventions (REVTeX, JHEP, INSPIRE-HEP, PRL/PRD-style significance language,
look-elsewhere effect) are built in, alongside astroparticle-physics and cosmic-ray
conventions (JCAP/AASTeX/Elsevier venues, ADS/bibcode citations, exposure vs.
luminosity, pre-trial vs. post-trial significance, skymap and energy-spectrum
figures), statistics/machine-learning conventions (NeurIPS/ICML/ICLR/ACL-family/
JMLR/TMLR venues, reproducibility checklists, arXiv/DBLP/ACL-Anthology citations,
single-shot OpenReview rebuttals, p-value/effect-size reporting language), and
general academic reading and writing guidance. Self-contained: no MCP server, cloud
account, or paid service required.

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
├── agents/
│   └── openai.yaml                # optional Codex UI metadata (display name, short description, default prompt)
├── references/
│   ├── literature-discovery-and-search.md      # finding papers before there's anything to triage: databases, query formulation, citation snowballing
│   ├── reading-papers.md                        # three-pass reading method, claims-vs-evidence, critical-reading checklist
│   ├── interpreting-scientific-graphics.md      # reading exclusion contours/corner plots/ROC curves/skymaps correctly, spotting misleading visualization
│   ├── literature-review.md                     # organizing a review/related-work section, comparison matrices, synthesis, novelty assessment
│   ├── paper-structure.md                       # section-by-section writing guidance for the standard physics-paper backbone, argument restructuring
│   ├── paper-genre-variants.md                  # how the backbone shifts for theory/review/thesis/proceedings papers
│   ├── outreach-and-public-facing-summaries.md  # plain-language public summaries; collaboration voice vs. syndicated commentary (AMS-02 example)
│   ├── astroparticle-and-cosmic-ray-papers.md   # venue/structure/citation/figure conventions for cosmic-ray & astroparticle papers, AMS-02 case study
│   ├── statistics-and-ml-papers.md              # venue/structure/citation/review-process conventions for statistics & ML papers
│   ├── latex-and-formatting.md                  # venue-specific class-file setup and skeletons (REVTeX/JHEP/JCAP/AASTeX/Springer/NeurIPS/ICML/ICLR/ACL)
│   ├── latex-mechanics-and-tooling.md           # venue-agnostic LaTeX: cleveref, siunitx/longtable, latexdiff, latexmk, bibtex vs. biber, multi-file docs
│   ├── figures-and-tables.md                    # publication figure design, captions, table conventions, accessible descriptions
│   ├── citations-and-bibliography.md            # INSPIRE-HEP/ADS/arXiv/DBLP/ACL-Anthology workflow, BibTeX hygiene, Zotero/JabRef library management, availability statements
│   ├── scientific-style.md                      # sentence-level prose guidance, significance-language & statistical-reporting conventions
│   ├── submission-and-peer-review.md            # pre-submission checklist, cover letters, referee responses, conference rebuttals
│   ├── citation-verification.md                 # reference identity/version checks, whether cited text supports the claim
│   ├── systematic-review-screening.md           # eligibility criteria, reproducible search logs, deduplication, screening records
│   ├── reproducibility-auditing.md              # tracing results to methods, data, code, configs, and execution evidence
│   ├── code-review-report.md                    # paper-to-code alignment, documentation, and packaging review; delegates deep technical review to deep-learning/hep-analysis
│   ├── equation-and-notation-auditing.md        # definitions, dimensions, index/shape consistency, derivation-step checks
│   ├── mathematical-reasoning-and-proof.md      # proof-status taxonomy (formal through conjecture), approximation validity, counterexample search
│   ├── statistical-inference-for-physics.md     # likelihood/frequentist/Bayesian inference checks, significance-language calibration
│   ├── numerical-and-computational-methods.md   # numerical convergence, optimization pitfalls, MCMC validation, circular-validation/leakage detection
│   ├── claim-evidence-mapping.md                # connecting central claims to results/derivations/citations, flagging unsupported generalizations
│   ├── logical-consistency-and-argument-uniformity.md  # cross-section contradictions, dropped assumptions, fallacious inference, definitional drift
│   ├── manuscript-consistency-auditing.md       # reconciling repeated results, uncertainty conventions, and conclusions across a paper
│   ├── plagiarism-and-text-reuse-checking.md    # distinguishing copied/paraphrased text from legitimate quotation, self-citation, boilerplate
│   ├── reviewer-style-assessment.md             # mock referee reports and submission-readiness reviews
│   ├── supplementary-material-planning.md       # allocating derivations/checks/artifacts between the main paper and supplements
│   ├── conflict-of-interest-and-ethics-statements.md  # venue-specific COI, funding, IRB/ethics-approval, and consent statements
│   ├── revision-impact-tracking.md              # tracing a changed result or reviewer request through manuscript artifacts during revision
│   ├── preprint-to-journal-reconciliation.md    # diffing an arXiv/preprint version against the published journal version
│   ├── multi-venue-reformatting.md              # adapting one manuscript across two venues (conference/journal, letter/full-paper)
│   ├── comment-and-reply-exchange.md            # drafting a formal post-publication Comment or Reply
│   ├── erratum-and-corrigendum-drafting.md      # classifying and drafting an erratum/corrigendum/addendum
│   ├── poster-and-talk-design.md                # re-laying-out a paper's results for a conference poster or slide deck
│   ├── preregistration-and-registered-reports.md  # writing a preregistration or registered report's Stage 1/Stage 2
│   ├── artifact-packaging-for-release.md        # preparing code/data for public release: README, pinned environment, license
│   ├── grant-and-fellowship-proposal-writing.md # Specific Aims, preliminary-results vs. proposed-work, broader-impacts, budget justification
│   └── thesis-by-publication-assembly.md        # assembling a thesis from already-published papers, permissions, per-chapter contributions
├── examples/
│   ├── README.md                  # index of the 14 canonical worked examples below
│   └── 01-...14-*.md              # Contrast/Trajectory/Gated-Pipeline/Decision-Tree/Elicitation/Adversarial-Audit worked examples in this skill's own domain
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

# Antigravity (workspace-scoped; falls back to .agent/skills/ on older installs)
cp -r academic-papers .agents/skills/

# Antigravity (global)
cp -r academic-papers ~/.gemini/config/skills/
```

## Per-agent invocation

- **Claude Code / Claude.ai**: the skill triggers automatically when a request
  matches its `description` (summarizing/critiquing a paper, building a literature
  review, drafting or formatting a manuscript, bibliography cleanup, referee
  responses, etc.) — no explicit invocation needed. You can also just say "use the
  academic-papers skill".
- **Codex**: place the folder in the skill directory used by your environment,
  commonly `~/.codex/skills/`, or import it through the mechanism supported by your
  version. Reload skills and invoke `$academic-papers`. `agents/openai.yaml` supplies
  optional Codex UI metadata.
- **Antigravity**: place the folder in `.agents/skills/` (workspace) or
  `~/.gemini/config/skills/` (global). It triggers automatically - the agent reads
  every installed skill's `name`/`description` at session start and loads the full
  `SKILL.md` when a task matches, no explicit invocation needed. See the
  [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other skill-aware agents**: consult that agent's own documentation for how
  installed `SKILL.md` files are surfaced; the file format here follows the same
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
