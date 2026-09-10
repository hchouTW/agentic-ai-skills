---
name: academic-papers
description: Use when reading, critiquing, or writing anything in the scientific-paper lifecycle — summarizing/critiquing a paper, interpreting a figure/plot/graphic, building a lit review or related-work section, finding literature, verifying citations/claim support, auditing reproducibility/equations/consistency/logical-argument-uniformity, reviewing accompanying code, systematic-review screening, drafting/restructuring a section, formatting for a venue (REVTeX/JHEP/JCAP/AASTeX/NeurIPS/ICML/ACL/JMLR), managing a BibTeX/INSPIRE-HEP/ADS/DBLP bibliography, designing figures/tables, referee/rebuttal responses, a Comment/Reply or erratum, or an adjacent artifact (poster/talk, preregistration, grant proposal, thesis-by-publication, code/data release, COI/ethics statement). Covers physics/HEP, astroparticle, and statistics/ML conventions, plus general academic writing. Trigger for even one piece (e.g. "what does this paper claim", "write my abstract", "fix these referee comments").
---

# Academic Papers

A skill for the full lifecycle around scientific papers: reading and critically
understanding one or many papers, synthesizing them into a literature review or a
paper's own related-work section, and then drafting, formatting, and submitting a
manuscript of your own. It is written with physics conventions front and center —
collider/high-energy-physics (HEP) and astroparticle physics/cosmic-ray science
(ground-based air-shower arrays, imaging Cherenkov telescopes, neutrino
observatories, space-based direct detection), plus statistics and machine-learning
publishing conventions (NeurIPS/ICML/ICLR/ACL-family conferences, JMLR/TMLR,
statistics journals) — but the reading strategies, prose guidance, and structural
conventions apply to scientific writing generally.

Pairs well with `hep-analysis` (the physics content: cutflows, fits, systematics,
limits, and — for the astroparticle side — spectrum/composition/anisotropy analysis
and astroparticle statistics) and `deep-learning` (the ML/statistical rigor itself:
ablations, seed variance, matched-budget comparisons, evaluation-harness design —
not just a methods section to read through). This skill owns the *reading and
writing*, not the analysis itself — if the user still needs to run a fit, produce a
limit, prove an improvement is real, or debug a plot, hand that off to
`hep-analysis` or `deep-learning` first.

## When to use this skill

Use it for any of:

**Reading side**
- Summarizing a single paper, or extracting its method/dataset/result for reuse
- Critically evaluating a paper's claims, evidence, statistics, and comparisons
- Comparing several papers against each other (methods, datasets, results)
- Building a literature review, a "related work" section, or a paper's Introduction
- Triaging a reading backlog / arXiv listing to decide what's worth reading deeply
- Taking structured reading notes for later reuse in the user's own writing

**Writing side**
- Drafting a paper from scratch, given results/notes/plots the user already has
- Structuring or restructuring a section (abstract, intro, results, discussion, conclusion)
- Converting an internal analysis note into a paper draft, or a paper into a talk/proceedings
- Writing a plain-language public/outreach summary of a published result for a
  collaboration or institution website
- LaTeX formatting: REVTeX (PRL/PRD/PRX), JHEP class, EPJC/Springer, JCAP, AASTeX
  (ApJ/ApJL), Elsevier `elsarticle` (Astroparticle Physics journal), NeurIPS/ICML/
  ICLR/AAAI/ACL-family style files, JMLR/TMLR, general `article`
- Building, cleaning, or deduplicating a BibTeX file; fixing INSPIRE-HEP citation
  keys, pulling ADS/bibcode entries for astronomy-facing venues, or sourcing
  arXiv/DBLP/ACL-Anthology entries for statistics/ML venues
- Designing or captioning figures and tables for publication (including learning
  curves, ablation tables, and leaderboard tables)
- Tightening prose: cutting hedging, fixing tense/voice consistency, trimming
  length, or getting statistical/ML reporting language right (p-values, effect
  sizes, multiple-comparison correction)
- Drafting responses to referee reports, a cover letter to an editor, or a
  single-shot conference rebuttal
- A pre-submission pass: checking length limits, undefined references, missing
  labels, or a reproducibility checklist

**Adjacent document types** (related genres, not paper sections themselves)
- Converting a paper's results into a conference poster or a talk's slide deck
- Drafting a preregistration document or a registered report's Stage 1/Stage 2
- Packaging the user's own code and data for public release alongside a paper
- Drafting a grant or fellowship proposal (Specific Aims, budget justification,
  broader-impacts sections) — a related but distinct genre from a paper
- Assembling a thesis or dissertation from the user's own already-published papers

Do **not** reach for this skill for pure numerical/statistical work (fitting, limit
setting, unfolding — `hep-analysis`; ablations, seed variance, proving an ML result
is real — `deep-learning`). Do reach for it the moment that work needs to be
understood from someone else's paper, or turned into English prose,
a figure caption, or a formatted document of your own.

## Core workflow: reading

0. **Find the literature before triaging it**, when there isn't already a
   paper or stack in hand — pick the right database(s) for the field,
   formulate and vary search terms, and snowball citations forward and
   backward from strong seed papers rather than relying on one keyword
   search. See `references/literature-discovery-and-search.md`.
1. **Triage before deep-reading.** For any paper (or stack of papers), do a fast first
   pass — title, abstract, section headings, figures, conclusion — before deciding it's
   worth reading in full. Most papers only need this pass. See
   `references/reading-papers.md` for the full three-pass method.
2. **Read for claims and evidence separately.** What does the paper claim, and what
   evidence actually supports each claim (dataset, method, statistical test,
   comparison baseline)? Keep these visibly distinct in notes — conflating "the paper
   says X" with "X is well-supported" is the most common reading error. When the
   evidence is a figure, see `references/interpreting-scientific-graphics.md` for
   reading it correctly rather than taking its visual impression at face value.
3. **Take structured notes as you read**, not after — use
   `assets/templates/reading_notes_template.md` as a starting shape (claim / method /
   evidence / limitations / relevance-to-my-work). Notes taken during reading are far
   more reusable later than a memory of "a paper that showed something like this."
4. **When reading multiple papers toward a literature review**, build a comparison
   matrix (method, dataset, key result, year) as you go rather than after — 
   `scripts/build_lit_matrix.py` turns a simple CSV of these notes into a formatted
   markdown table ready to drop into a draft. See `references/literature-review.md`.
5. **Synthesize, don't list.** A literature review or related-work section groups
   papers by what they share or how they differ and states the gap this work fills —
   it is not "Paper A did X [1]. Paper B did Y [2]. Paper C did Z [3]." See
   `references/literature-review.md` for synthesis patterns.

## Focused verification and review modes

Use these modes when requested or needed to substantiate the paper's claims;
an ordinary summary does not require a full audit.

**Verification and auditing**
- **Citation verification:** check reference identity, version, publication status,
  and whether the cited text supports the manuscript's claim. Read
  `references/citation-verification.md`. A resolving DOI or valid BibTeX entry
  alone does not verify a claim.
- **Systematic-review screening:** define eligibility, log reproducible searches,
  deduplicate records, and record screening decisions and exclusions. Read
  `references/systematic-review-screening.md`. Keep narrative literature reviews
  lightweight unless a systematic process is requested.
- **Reproducibility auditing:** trace selected results to methods, data, code,
  configurations, and available execution evidence. Read
  `references/reproducibility-auditing.md`. Distinguish documentation inspection
  from an actual rerun; use `hep-analysis` or `deep-learning` for relevant execution.
- **Code review report:** review code accompanying a paper for paper-to-code
  alignment, documentation, and packaging, producing a severity-ranked findings
  report. Read `references/code-review-report.md`. Distinct from reproducibility
  auditing (execution evidence, not code review); delegate framework-specific
  correctness to `deep-learning` or `hep-analysis`.
- **Equation and notation auditing:** check definitions, dimensions, index/shape
  consistency, assumptions, and derivation steps. Read
  `references/equation-and-notation-auditing.md`.
- **Claim–evidence mapping:** connect central claims to results, derivations, and
  citations, and identify unsupported generalizations. Read
  `references/claim-evidence-mapping.md`.
- **Logical consistency and argument uniformity:** check for cross-section
  contradictions, dropped assumptions, fallacious inference, and definitional
  drift in the argument itself (not just numeric values) using
  `references/logical-consistency-and-argument-uniformity.md`.
- **Manuscript consistency auditing:** reconcile repeated results, uncertainty
  conventions, dataset descriptions, and conclusions across the paper using
  `references/manuscript-consistency-auditing.md`.
- **Plagiarism and text-reuse checking:** distinguish copied/paraphrased text
  from legitimate quotation, self-citation, or boilerplate using
  `references/plagiarism-and-text-reuse-checking.md`.

**Assessment and restructuring**
- **Reviewer-style assessment:** assess contribution, validity, comparisons, and
  actionable concerns using `references/reviewer-style-assessment.md`.
- **Research-gap and novelty assessment:** compare the proposed contribution with
  verified close prior work using the novelty-assessment section of
  `references/literature-review.md`.
- **Scientific argument restructuring:** identify missing logical steps and reorder
  sections around the evidence using the argument-restructuring section of
  `references/paper-structure.md`.
- **Abstract and title optimization:** create accurate variants for an audience,
  venue, or length limit using the abstract-and-title-variants section of
  `references/paper-structure.md`.
- **Supplementary-material planning:** allocate derivations, checks, and artifact
  details between the main paper and supplements using
  `references/supplementary-material-planning.md`.

**Tracking and cross-version reconciliation**
- **Revision-impact tracking:** trace changed results and reviewer requests through
  manuscript artifacts and response letters using
  `references/revision-impact-tracking.md`.
- **Preprint-to-journal reconciliation:** diff a preprint version against the
  published version and identify substantive differences using
  `references/preprint-to-journal-reconciliation.md`.
- **Multi-venue reformatting:** adapt one manuscript's content across two
  venues (conference/journal extension, letter/full-paper companion) using
  `references/multi-venue-reformatting.md`.
- **Comment/Reply exchange:** draft a formal post-publication Comment
  disputing a specific claim, or a Reply to one, using
  `references/comment-and-reply-exchange.md`.
- **Erratum and corrigendum drafting:** classify and draft a correction
  notice once the decision to correct the record is made, using
  `references/erratum-and-corrigendum-drafting.md`.

**Disclosure and compliance statements**
- **Data and code availability statements:** describe verified repositories,
  versions, restrictions, and missing artifacts using the availability-statements
  section of `references/citations-and-bibliography.md`.
- **Authorship and contribution statements:** organize supplied contributions,
  acknowledgments, and disclosures using the authorship-and-contributions section
  of `references/submission-and-peer-review.md`; do not infer credit or author order.
- **Conflict-of-interest and ethics statements:** draft COI, funding,
  IRB/ethics-approval, and consent statements using
  `references/conflict-of-interest-and-ethics-statements.md`.
- **Accessible scientific communication:** write figure descriptions and inspect
  visual encodings using the accessible-descriptions section of
  `references/figures-and-tables.md`.

## Core workflow: writing

1. **Scope the paper.** Before writing a word, pin down: target venue (PRL / PRD /
   JHEP / EPJC / JCAP / ApJ / NeurIPS / ICML / ACL / JMLR / thesis chapter /
   proceedings / internal note), length limit, single result or full analysis, and
   whether this is a from-scratch draft or an edit of existing text. Ambiguity here
   wastes the most time downstream — ask if it's genuinely unclear, but if the user
   has already given enough (e.g. "PRL letter on the Higgs mass measurement" or
   "NeurIPS submission on this method"), proceed without a clarifying round-trip.
2. **Build the skeleton first.** Write section headers and one-sentence placeholders for
   each ("This section will show the fit is consistent with SM at 1.2σ.") before
   writing full prose. This catches structural problems — missing systematics
   discussion, no comparison to prior measurements — while they're cheap to fix.
   See `references/paper-structure.md`.
3. **Draft section by section, result-first.** For physics papers, write the abstract
   *last* even though it's read first — it's a compressed version of everything else.
   Draft in this order: Results → Analysis/Methods → Introduction → Discussion/
   Conclusion → Abstract → Title. See `references/paper-structure.md` for what belongs
   in each section and `references/scientific-style.md` for sentence-level guidance.
4. **Build figures and tables alongside the text**, not after. A figure that needs a
   paragraph of caption to be understood usually needs redesigning, not more caption.
   See `references/figures-and-tables.md`.
5. **Manage citations as you write**, not in a final sweep — pull keys from the
   right source for the venue (INSPIRE-HEP, ADS, arXiv, DBLP, or ACL Anthology) as
   each claim is made, reusing any reading notes already gathered above, so nothing
   gets forgotten. See `references/citations-and-bibliography.md`.
6. **Typeset in the target class file** from early on if the venue is known (REVTeX,
   JHEP, etc.) — page/length limits interact with formatting in ways that are painful
   to discover after the fact. See `references/latex-and-formatting.md`.
7. **Run a pre-submission pass.** Use `scripts/check_manuscript.py` to catch undefined
   references, duplicate labels, leftover TODOs, and uncited or unused bib entries
   before the user sends the draft anywhere. Then do a human read-aloud pass for prose
   using `references/scientific-style.md`.
8. **If reviews come back**, use `references/submission-and-peer-review.md` for how to
   structure a referee response and cover letter, or a single-shot conference
   rebuttal if the venue uses that process instead.

## Physics/HEP paper structure (quick reference)

A typical experimental HEP paper (PRL/PRD/JHEP style) runs, roughly:

| Section | Purpose | Typical length |
|---|---|---|
| Title | States the result, not the method | ≤ 15 words |
| Abstract | Self-contained summary: context, method, result, significance | 150–250 words |
| Introduction | Physics motivation, prior measurements, what's new here | 0.5–1.5 pages |
| Detector & Dataset | What data, what detector, what luminosity/energy | 0.25–0.75 pages |
| Analysis / Event Selection | Cuts, reconstruction, background estimation | 1–3 pages |
| Systematic Uncertainties | Sources, sizes, correlations, how propagated | 0.5–1.5 pages |
| Results | The number(s), with statistical + systematic uncertainty, comparison to theory/prior results | 0.5–1.5 pages |
| Summary / Conclusion | Restate result, implications, outlook — no new claims | 3–8 sentences |
| Acknowledgments | Funding agencies, collaboration boilerplate | fixed by collaboration |

Full guidance, including how this differs for theory papers, review articles,
thesis chapters, astroparticle/cosmic-ray papers (exposure instead of luminosity,
arrival-direction/anisotropy sections, multi-messenger context), and statistics/ML
papers (required Limitations/Broader-Impact sections, reproducibility checklists,
single-shot rebuttals), is in `references/paper-structure.md`,
`references/astroparticle-and-cosmic-ray-papers.md`, and
`references/statistics-and-ml-papers.md`.

## Journal / venue conventions (quick reference)

| Venue | Class file | Typical length | Notes |
|---|---|---|---|
| PRL | `revtex4-2` (`\documentclass[aps,prl,twocolumn]{revtex4-2}`) | ~4 pages, ~3750 words | Letter format, no separate abstract heading |
| PRD / PRX | `revtex4-2` (`\documentclass[aps,prd]{revtex4-2}`) | No hard limit (PRD), longer form | Full methods allowed |
| JHEP | `JHEP3.cls` | No hard limit | SISSA house style, `\bibliographystyle{JHEP}` |
| EPJC | Springer `svjour3`/`spphys` | No hard limit | Springer LaTeX templates |
| Nature / Nat. Phys. | Nature LaTeX template or Word | ~2000–3000 words main text | Methods/refs often separate |
| JCAP (astroparticle) | SISSA's `jcappub.cls` | No hard limit | JHEP-family style; common venue for cosmic-ray/dark-matter theory and phenomenology |
| ApJ / ApJL (astroparticle) | AASTeX (current `aastexN.cls`) | ApJL is letter-length | natbib author-year citations by default |
| Astroparticle Physics (Elsevier) | `elsarticle.cls` | No hard limit | Elsevier house style |
| NeurIPS / ICML / ICLR / AAAI | Conference's current-year `.sty` | Hard page limit, unlimited appendix | Single-shot rebuttal, not a revision round; pull the current year's template |
| ACL / EMNLP / NAACL | Shared ACL Anthology style file | Hard page limit | `natbib` author-year; ACL Rolling Review has a different, revision-carrying cadence |
| JMLR / TMLR | Venue's own LaTeX template | No hard limit | Journal-style open review, closer to a physics journal's process |
| Statistics journals (JASA, Annals of Statistics, ...) | Usually plain `article`-based | No hard limit | Journal-specific reference style; theorem/proof structure for theory papers |
| arXiv preprint | Whatever the target journal uses, or `article` | Match target venue | Always include `\usepackage{hyperref}` sparingly per arXiv rules |

Details, obtaining the right class file, and common compile errors are in
`references/latex-and-formatting.md`; astroparticle-specific venues and author-list
conventions are in `references/astroparticle-and-cosmic-ray-papers.md`;
statistics/ML-specific venues, reproducibility checklists, and rebuttal mechanics
are in `references/statistics-and-ml-papers.md`. A generic starting skeleton (not
tied to any journal's copyrighted class file) is in
`assets/templates/paper_skeleton.tex`, paired with an example INSPIRE-HEP-formatted
entry in `assets/templates/references.bib` — copy the actual class file from the
journal/APS/SISSA/Springer/AAS/Elsevier/conference site once the venue is fixed.

## Reference files

Read these as needed — don't load them all up front unless doing a full draft or
review. Grouped by function; within a group, order roughly follows the workflow.

**Reading and discovery**
- `references/literature-discovery-and-search.md` — finding relevant papers
  before there's anything to triage: database/tool choice by field, query
  formulation, forward/backward citation snowballing, alerts, and knowing
  when search coverage is enough
- `references/reading-papers.md` — the three-pass reading method, separating claims
  from evidence, a critical-reading checklist (fair baselines, statistical rigor,
  reproducibility), HEP-specific things to check (dataset/luminosity, systematics
  treatment, look-elsewhere effect), astroparticle-specific things to check
  (exposure/livetime, trials factor, hadronic-model dependence), and
  statistics/ML-specific things to check (baseline fairness, cross-seed
  significance, train/test contamination)
- `references/interpreting-scientific-graphics.md` — the reading-side counterpart
  to figure design: reading common plot types correctly (exclusion contours,
  corner plots, ROC curves, skymaps, learning curves), extracting approximate
  values when no data table is given, spotting misleading visualization
  techniques, and separating visual impression from statistical significance
- `references/literature-review.md` — organizing a review or related-work section
  (chronological vs. thematic vs. methodological), building a comparison matrix,
  synthesis patterns vs. citation-stuffing, spotting research gaps

**Structure, venue, and formatting**
- `references/paper-structure.md` — section-by-section guidance, HEP vs. theory vs.
  thesis vs. proceedings vs. astroparticle vs. statistics/ML papers, what a referee
  expects in each section, plus writing a plain-language public/outreach summary
  and telling apart collaboration-voice outreach from syndicated third-party
  commentary (a journalist's recap, an APS Synopsis, an APS Viewpoint)
- `references/astroparticle-and-cosmic-ray-papers.md` — how structure, venues,
  author lists, citations, figures, and phrasing shift for astroparticle-physics
  and cosmic-ray papers (ground arrays, IACTs, neutrino observatories, space-based
  direct detection): exposure vs. luminosity, arrival-direction/anisotropy sections,
  JCAP/ApJ/Astroparticle Physics venues, ADS/bibcode citations, skymap conventions,
  pre-trial vs. post-trial significance, and a worked AMS-02 publication-pattern
  case study (letter-only/no-arXiv publishing, a Phys. Rept. review alongside PRL
  letters, 44-institution author-list scale, a web-only non-citable
  "advances-in-data-analysis" technical-progress genre, and syndicated vs.
  collaboration-authored outreach pages)
- `references/statistics-and-ml-papers.md` — how structure, venues, author-
  contribution statements, citations, and review process shift for statistics and
  machine-learning papers: required Limitations/Broader-Impact sections,
  reproducibility checklists and artifacts (model cards, datasheets), NeurIPS/
  ICML/ICLR/AAAI/ACL-family/JMLR/TMLR/statistics-journal venue landscape,
  arXiv-first citation culture (DBLP, ACL Anthology, Semantic Scholar), and
  single-shot OpenReview rebuttals vs. a journal's multi-round revision
- `references/latex-and-formatting.md` — REVTeX/JHEP/Springer/JCAP/AASTeX/
  Elsevier/NeurIPS/ICML/ICLR/ACL/JMLR venue-specific setup and skeletons,
  arXiv-specific rules, units/equation conventions, common compile errors,
  length-limit tricks
- `references/latex-mechanics-and-tooling.md` — cross-cutting LaTeX
  mechanics that apply regardless of venue: cross-referencing (`cleveref`)
  and `\newcommand` notation macros, `siunitx`/`multirow`/`longtable` table
  syntax, tagged-PDF accessibility, `latexdiff` tracked-changes diffing,
  `latexmk` build automation, bibtex-vs-biber/biblatex engine choice,
  `\include`/`\includeonly` multi-file document structuring, and non-ASCII
  author-name encoding

**Prose, figures, and citations**
- `references/figures-and-tables.md` — plot design for publication (following on from
  ROOT/matplotlib output made under `hep-analysis`), caption writing, table
  conventions, skymap/cosmic-ray-spectrum figures, and learning-curve/ablation/
  leaderboard tables
- `references/citations-and-bibliography.md` — INSPIRE-HEP, ADS, and arXiv/DBLP/
  ACL-Anthology workflows, BibTeX hygiene, managing a personal reference library
  (Zotero/JabRef) across papers/projects, citation style by venue, linking
  supplemental material/data, citing an accompanying Viewpoint or Synopsis
  separately from the primary paper, avoiding orphaned/duplicate entries
- `references/scientific-style.md` — sentence-level prose guidance: tense, voice,
  hedging, common non-native-English pitfalls, physics-specific,
  astroparticle-specific, and statistical/ML-specific (p-values, effect sizes,
  multiple-comparison correction) phrasing conventions

**Submission and peer review**
- `references/submission-and-peer-review.md` — pre-submission checklist, cover
  letters, referee response structure, revision tracking, arXiv submission
  mechanics (including collaborations that skip arXiv entirely), and single-shot
  conference rebuttals

**Verification and auditing**
- `references/citation-verification.md` — reference identity/version checks and
  whether cited text supports the manuscript's claim
- `references/systematic-review-screening.md` — eligibility criteria, reproducible
  search logs, deduplication, and screening-decision records
- `references/reproducibility-auditing.md` — tracing results to methods, data,
  code, configurations, and available execution evidence
- `references/code-review-report.md` — reviewing code accompanying a paper for
  paper-to-code alignment, documentation, and packaging, producing a
  severity-ranked findings report; delegates framework-specific correctness to
  `deep-learning`/`hep-analysis`
- `references/equation-and-notation-auditing.md` — definitions, dimensions,
  index/shape consistency, and derivation-step checks
- `references/claim-evidence-mapping.md` — connecting central claims to results,
  derivations, and citations; flagging unsupported generalizations
- `references/logical-consistency-and-argument-uniformity.md` — checking the
  argument's logical structure itself: cross-section contradictions, dropped/
  changed assumptions, fallacious inference patterns, definitional drift, and
  scope mismatch between the conclusion and what was actually argued
- `references/manuscript-consistency-auditing.md` — reconciling repeated results,
  uncertainty conventions, dataset descriptions, and conclusions across a paper
- `references/plagiarism-and-text-reuse-checking.md` — distinguishing verbatim
  copying, close paraphrase, and legitimate reuse (quotation, self-citation,
  boilerplate) in a manuscript or against the user's own prior publications

**Assessment and restructuring**
- `references/reviewer-style-assessment.md` — mock referee reports and
  submission-readiness reviews: contribution, validity, comparisons, concerns
- `references/supplementary-material-planning.md` — allocating derivations,
  checks, and artifact details between the main paper and supplements
- Research-gap/novelty assessment and scientific-argument restructuring are
  covered as sections within `references/literature-review.md` and
  `references/paper-structure.md` respectively, not standalone files — see
  those files' tables of contents

**Disclosure, reconciliation, and cross-venue**
- `references/conflict-of-interest-and-ethics-statements.md` — venue-specific
  COI/competing-interests, funding, IRB/ethics-approval, and consent
  statements, kept separate from authorship-and-contribution statements
- `references/revision-impact-tracking.md` — tracing a changed result or reviewer
  request through manuscript artifacts and response letters during an active
  revision
- `references/preprint-to-journal-reconciliation.md` — diffing an arXiv/
  preprint version against the published journal version, classifying
  differences, and updating preprint metadata after publication
- `references/multi-venue-reformatting.md` — adapting content across two
  venues with different class files or length limits (conference→journal
  extension, journal letter→full-paper companion), including duplicate-
  publication disclosure requirements
- `references/comment-and-reply-exchange.md` — drafting a formal
  post-publication Comment or Reply (PRL/PRD-family article type), distinct
  from a pre-publication referee response
- `references/erratum-and-corrigendum-drafting.md` — classifying and
  drafting an erratum/corrigendum/addendum once the decision to correct the
  published record has been made

**Adjacent document types**
- `references/poster-and-talk-design.md` — re-laying-out a paper's results
  for a conference poster (viewing-distance figures, walkable panel order)
  or a slide deck (one-idea-per-slide, matching depth to slot length)
- `references/preregistration-and-registered-reports.md` — writing a
  preregistration or a registered report's Stage 1/Stage 2, keeping
  confirmatory and exploratory analyses distinguishable
- `references/artifact-packaging-for-release.md` — preparing the user's own
  code/data repository for public release (README, pinned environment,
  license, verified end-to-end reproduction), as the writing-side
  counterpart to `reproducibility-auditing.md`
- `references/grant-and-fellowship-proposal-writing.md` — Specific Aims/
  research-statement structure, preliminary-results vs. proposed-work
  separation, broader-impacts sections, and budget-justification handling
  for a grant or fellowship proposal (a distinct genre from a paper)
- `references/thesis-by-publication-assembly.md` — assembling a thesis from
  the user's own already-published papers: institutional requirements,
  copyright/reuse permissions, connective-material synthesis, per-chapter
  contribution statements, and cross-paper inconsistency reconciliation

## Bundled scripts

- `scripts/build_lit_matrix.py` — turns a CSV of reading notes (one row per paper:
  key, year, method, dataset, result, notes — columns are flexible) into a formatted
  markdown comparison table, ready to drop into a literature review or related-work
  draft. Standard library only.

  ```
  python3 scripts/build_lit_matrix.py <notes.csv> [--sort-by year] [-o out.md]
  ```

- `scripts/check_manuscript.py` — scans a directory of `.tex`/`.bib` files and reports:
  undefined `\ref`/`\cite` targets, duplicate `\label`s, `\cite` keys missing from any
  `.bib` file, unused `.bib` entries, and leftover TODO/FIXME/placeholder markers.
  Read-only; standard library only. Run it near the end of a drafting session, not
  after every sentence.

  ```
  python3 scripts/check_manuscript.py <path-to-manuscript-dir>
  ```

- `scripts/validate_skill_bundle.py` — integrity checker for this skill bundle itself
  (not for the user's paper or reading notes). Run after editing this skill.

## Working style within this skill

- **Never misrepresent a paper being read.** Distinguish clearly, in notes and in any
  summary given to the user, between what a paper claims, what it actually
  demonstrates, and any interpretation being added — do not blur these together, and
  flag when a claim in the paper looks stronger than its own evidence supports.
- **Preserve the user's actual results when writing.** Never invent numbers,
  uncertainties, significances, or citations. If a value is missing, mark it clearly
  (`[VALUE NEEDED: signal efficiency]`) rather than guessing or rounding to something
  plausible-looking.
- **Match existing voice** when editing a draft rather than a blank page — improve
  clarity and correctness without rewriting a passage that already works, and flag
  the specific sentences changed rather than silently rewriting whole sections.
- **Default to the venue's convention**, not personal preference, once a venue is
  named (e.g. PRL wants short, punchy paragraphs; JHEP tolerates more derivation).
- **Ask, don't assume, about author list and acknowledgments** for collaboration
  papers — get these from the user or an existing template rather than guessing
  collaboration boilerplate.
