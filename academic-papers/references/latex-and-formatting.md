# LaTeX and Formatting

How to set a manuscript up correctly for the major physics venues, and how to
avoid the compile errors and length-limit surprises that eat time late in
drafting.

## Table of contents
- [Getting the right class file](#getting-the-right-class-file)
- [REVTeX (PRL / PRD / PRX)](#revtex-prl--prd--prx)
- [JHEP](#jhep)
- [EPJC / Springer](#epjc--springer)
- [Astroparticle venues (JCAP / AASTeX / Elsevier)](#astroparticle-venues-jcap--aastex--elsevier)
- [Statistics and ML venues](#statistics-and-ml-venues)
- [arXiv-specific rules](#arxiv-specific-rules)
- [Units, numbers, and equations](#units-numbers-and-equations)
- [Cross-referencing and notation macros](#cross-referencing-and-notation-macros)
- [Table syntax specifics](#table-syntax-specifics)
- [Common compile errors](#common-compile-errors)
- [Length-limit tactics](#length-limit-tactics)
- [PDF accessibility (tagged PDF)](#pdf-accessibility-tagged-pdf)
- [Tracked changes and diffing](#tracked-changes-and-diffing)

## Getting the right class file

Never hand-copy a journal's `.cls`/`.bst` file from memory or reconstruct it —
these are maintained and versioned by the publisher/society. Get the current
version from the authoritative source:
- REVTeX 4.2 (APS: PRL, PRD, PRX, PRA, PRB, ...): APS's REVTeX page.
- JHEP: SISSA's JHEP author guidelines page (`JHEP3.cls`, `JHEP.bst`).
- EPJC: Springer's `svjour3`/`spphys` LaTeX package for Physics journals.
- Nature family: Nature's LaTeX template page (or submit in Word, per journal).
- JCAP / ApJ / Astroparticle Physics (Elsevier): see "Astroparticle venues" below.
- NeurIPS / ICML / ICLR / AAAI / ACL family / JMLR / TMLR: see "Statistics and ML
  venues" below.

If offline or unsure of the exact current filename/version, tell the user to
pull it fresh from the journal's site rather than guessing — a stale or
hand-reconstructed class file is a common source of subtle formatting bugs
that only show up after submission.

## REVTeX (PRL / PRD / PRX)

Minimal PRL skeleton:

```latex
\documentclass[aps,prl,twocolumn,showpacs,superscriptaddress]{revtex4-2}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{hyperref}

\begin{document}

\title{Measurement of ...}

\author{A.\ Researcher}
\affiliation{Department of Physics, University X}
\collaboration{The XYZ Collaboration}

\date{\today}

\begin{abstract}
...
\end{abstract}

\maketitle

% body sections use \section*{...} in PRL (no numbered sections)

\end{document}
```

Notes:
- PRL uses unnumbered `\section*{}` headings; PRD/PRX allow numbered sections.
- `\collaboration{}` and `\affiliation{}` handle large collaboration author
  lists — for genuinely large collaborations (hundreds of authors), APS
  provides a separate author-list macro package; ask the collaboration's
  publications committee for the current boilerplate rather than typing
  hundreds of `\author{}` lines by hand.
- `twocolumn` is required for PRL; PRD/PRX are typically single-column for
  submission and typeset two-column on publication.

## JHEP

```latex
\documentclass{JHEP3}
\usepackage{amsmath,amssymb,graphicx}

\title{...}
\author[a]{First Author}
\author[b]{Second Author}
\affiliation[a]{Institution A}
\affiliation[b]{Institution B}
\emailAdd{author@inst.edu}

\abstract{...}

\begin{document}
\maketitle
\flushbottom

\section{Introduction}
...

\bibliographystyle{JHEP}
\bibliography{references}
\end{document}
```

JHEP numbers all sections, expects `\flushbottom`, and its `JHEP.bst` style
formats INSPIRE-style BibTeX entries (with `eprint`/`archivePrefix` fields)
correctly — pull `.bib` entries from INSPIRE-HEP directly rather than
retyping them (see `citations-and-bibliography.md`).

## EPJC / Springer

Use Springer's `svjour3` class with the `spphys` style option. Structurally
closer to JHEP (numbered sections) than to REVTeX's PRL mode. Springer's
author guidelines page has the current template and a Word alternative if the
group doesn't use LaTeX.

## Astroparticle venues (JCAP / AASTeX / Elsevier)

- **JCAP** uses SISSA's `jcappub.cls`, structurally close to `JHEP3.cls` (numbered
  sections, `\flushbottom`, JHEP-compatible bibliography style) — pull the current
  class from JCAP's author-guidelines page.
- **ApJ / ApJL** use AASTeX (`\documentclass[modern]{aastexN}` for the current major
  version `N`) — get the exact current version from the AAS journals author-resources
  page, since AASTeX version bumps have changed author-list and table syntax before.
  `natbib`-style author-year citations (`\citep{}`/`\citet{}`) are the default, not
  the numbered style used by REVTeX/JHEP.
- **Astroparticle Physics (Elsevier)** uses `elsarticle.cls`; get it from Elsevier's
  author-support page along with the current citation-style option the journal
  specifies (Elsevier journals vary in numbered vs. author-year style by title).

See `astroparticle-and-cosmic-ray-papers.md` for the structural and citation-database
(ADS vs. INSPIRE-HEP) differences that go along with these venues, not just the class
files.

## Statistics and ML venues

- **NeurIPS / ICML / ICLR / AAAI** each publish a `.sty`/class file for that
  specific year's conference — pull the *current year's* template, not a cached
  one from a prior year: margins, font, and section-numbering rules change
  year to year and several of these venues run an automated formatting checker
  at submission that rejects a paper built on a stale template.
- **ACL / EMNLP / NAACL** share a common ACL Anthology style file
  (`acl.sty`/`emnlp.sty` depending on year), with `\citep`/`\citet` author-year
  citations via that same style — get it from the ACL Anthology's author
  resources, not a general LaTeX template site.
- **JMLR / TMLR** each have their own dedicated LaTeX template (JMLR's is a
  long-running stable style, closer to a journal's `article`-based class than a
  yearly-changing conference one).
- **Statistics journals** (JASA, Annals of Statistics, Biometrika, JRSS-B) rarely
  mandate a specific heavily-branded class file the way REVTeX/AASTeX do — most
  accept a plain `article`-based submission with the journal's own reference
  style; check the specific journal's current author guidelines rather than
  assuming a house class exists.

See `statistics-and-ml-papers.md` for the structural differences (Limitations and
Broader Impact/Ethics as required sections, reproducibility checklists, appendix
conventions) and the review-process differences (single-shot rebuttal vs. a
journal's multi-round revision) that go with these venues, not just the class
files.

## arXiv-specific rules

- arXiv strips or restricts some packages; prefer `hyperref` with `pdftex`
  driver and avoid exotic custom packages when possible to reduce upload
  failures.
- Upload all source files (`.tex`, `.bib` or the compiled `.bbl`, figure
  files) — arXiv recompiles from source, so a missing figure file or an
  un-uploaded `.bst`/custom `.cls` will break the build. When in doubt about
  a journal class file's arXiv-compatibility, upload the compiled `.bbl` and
  fall back to a plain `article`-based version for arXiv while keeping the
  journal-class version for submission.
- Category selection (e.g. `hep-ex`, `hep-ph`, `hep-th`, `astro-ph.HE`)
  determines the primary audience and moderation queue — pick the primary
  category that matches the paper's main claim, with cross-lists for
  secondary relevance.

## Units, numbers, and equations

- Use natural units (`\hbar = c = 1`) consistently in HEP papers unless the
  venue/subfield convention is SI; state the convention once, early.
- Number format: prefer `125.09 \pm 0.24$ GeV` style with explicit
  uncertainty, not `~125 GeV` in a Results section (approximations are fine
  in prose elsewhere).
- Use `siunitx` (`\SI{125.09}{\GeV}`) for consistent unit typesetting if the
  venue allows extra packages; otherwise typeset units in roman, values in
  math mode, with a non-breaking space (`~`) between them: `125~GeV`.
- Number all equations that are referenced later; do not number equations
  that are never cross-referenced (clutters the margin, and some venues
  penalize it in length-limited formats).

## Cross-referencing and notation macros

- Always `\label{}` immediately after `\section`, `\begin{equation}`,
  `\begin{figure}`, or `\begin{table}` — a label placed elsewhere (e.g.
  inside a table's caption but outside a figure's) can silently pick up the
  wrong number.
- Use `\eqref{}` for equations (adds parentheses automatically) and `\ref{}`
  for everything else; the `cleveref` package's `\cref{}`/`\Cref{}` picks the
  right word ("Eq.", "Fig.", "Table") automatically from the label prefix.
  Adopt a consistent prefix convention (`eq:`, `fig:`, `tab:`, `sec:`) from
  the first label onward so `cleveref` — or a human skimming the source —
  can tell what's referenced at a glance.
- `scripts/check_manuscript.py` catches undefined `\ref`/`\cite` targets and
  duplicate `\label`s mechanically, but not a label that resolves without
  error yet points at the wrong equation/figure after reordering — check
  numbering visually after any significant section reordering.
- Define a symbol once with `\newcommand{\mysymbol}{...}` in the preamble
  (or a separate `notation.tex` pulled in with `\input{}`) rather than
  retyping a multi-part symbol (a fit parameter, a cross-section variable)
  throughout the manuscript. This is what keeps a symbol's definition from
  silently drifting across a long derivation — exactly the failure
  `equation-and-notation-auditing.md` audits for — and lets a notation
  change be made once instead of via a manuscript-wide find-and-replace
  that a hyphenated or spaced variant would slip past.
- A `\newcommand` collision with an existing LaTeX/package command fails
  loudly at compile time — don't silence it with `\renewcommand` unless the
  override is intentional.

## Table syntax specifics

Beyond `booktabs`'s `\toprule`/`\midrule`/`\bottomrule` (see
`figures-and-tables.md` for table *design* conventions — this section is the
LaTeX syntax to build one):

- **Aligning numbers with uncertainties**: `siunitx`'s `S` column type
  (`\begin{tabular}{l S[separate-uncertainty]}`) aligns a column of
  `125.09(24)`- or `125.09 \pm 0.24`-style values on the decimal point
  automatically — don't hand-pad with `\phantom{}`, which breaks the moment
  a value's digit count changes during revision.
- **Spanning cells**: `\multicolumn{2}{c}{...}` for a header spanning
  several columns, `\multirow{2}{*}{...}` (from the `multirow` package) for
  a label spanning several rows. Don't fake either with merged-looking but
  structurally separate cells — this breaks screen readers and any
  `\label`-based reference into the table.
- **Long tables spanning pages**: use the `longtable` package rather than
  manually splitting one table into several `table` environments — a
  manually split table loses its single caption/label, and referencing a
  specific row becomes ambiguous.
- **Footnotes inside tables**: use `threeparttable` (keeps footnote markers
  scoped to the table and printed directly below it) rather than a regular
  `\footnote{}` inside a `tabular`, which can float to the bottom of the
  page detached from the table it annotates.

## Common compile errors

| Symptom | Likely cause |
|---|---|
| `Undefined control sequence` right after `\documentclass` | Wrong/missing class file, or a package loaded before its dependency |
| References show as `[?]` | Need to run `bibtex`/`biber` then `pdflatex` twice more (four-pass compile) |
| `\cite` shows `[??]` after full 4-pass compile | Citation key not in the `.bib` file, or the `.bib` file isn't listed in `\bibliography{}` |
| Figure "not found" | Path relative to `.tex` file, not to where the compiler is invoked; check `\graphicspath{}` |
| `Too many unprocessed floats` | Too many `\begin{figure}` without enough text between them; add `\clearpage` or reduce simultaneous floats |
| Overfull `\hbox` warnings | Usually cosmetic (line slightly too wide) but check for un-hyphenatable long words/URLs — wrap with `\url{}` or `\seqsplit{}` |

## Length-limit tactics

When a venue enforces a hard page/word limit (PRL's ~4 pages is the classic
case):
- Move derivation detail and extra validation plots to Supplemental
  Material, if the venue supports it, rather than cutting the physics.
- Combine multi-panel figures rather than using several single-panel
  figures — this often saves more space than trimming prose.
- Cut hedging and redundant transition phrases before cutting content (see
  `scientific-style.md`) — most first drafts have 10-20% removable words
  with no loss of information.
- Do not shrink font size or margins to cheat a page limit; venues check
  for this and it reads poorly to referees.

## PDF accessibility (tagged PDF)

Several venues (ACM already requires it; more are moving this direction)
now require a tagged, accessible PDF — a structural layer a screen reader
uses to navigate headings, read tables cell-by-cell, and announce a
figure's alt text — not just a visually correct PDF.

- `pdflatex`/`lualatex` alone do not produce a tagged PDF; use the `tagpdf`
  package (LaTeX3-based, actively maintained) or a document class with
  built-in tagging support if the venue's template provides one — check the
  venue's current author guidelines, since support and required packages
  change as tagging tooling matures.
- Attach the alt text written using `figures-and-tables.md`'s
  accessible-descriptions guidance to the actual figure via the tagging
  package's alt-text hooks — alt text that exists only in a separate
  document handed to the user is not embedded accessibility; it must be in
  the PDF's structure tree to be usable by a screen reader.
- Tag reading order explicitly for multi-column layouts (PRL's
  `twocolumn`; JHEP's single-column is simpler) — a naive tagging pass can
  read across columns left-to-right instead of down one column then the
  next. Verify reading order with a PDF accessibility checker (e.g. Adobe
  Acrobat's or PAC's checker) before submission, not just visually.
- This is a young, fast-moving area of LaTeX tooling — verify current
  package support against the specific venue's requirement rather than
  assuming a fixed recipe, and ask the user whether the target venue
  currently mandates this before investing time in it.

## Tracked changes and diffing

For a referee response or a co-author review round that needs a visible
diff against a prior revision (see `submission-and-peer-review.md`'s
referee-response guidance, and `revision-impact-tracking.md` for tracking
*what* changed and why):

```
latexdiff old_version.tex new_version.tex > diff.tex
pdflatex diff.tex   # compile diff.tex like any other .tex file
```

- `latexdiff` marks deletions with strikethrough and additions
  underlined/colored directly in the compiled PDF — this is what most
  physics/stats venues mean by a "marked-up" or "tracked-changes" version
  accompanying a resubmission, not a Word-style comment thread.
- Run it on the two `.tex` source files, not on rendered PDFs. It operates
  on LaTeX source and can misfire on heavily restructured text (a moved
  paragraph can show as a spurious delete-and-add pair) — check the diff
  output visually rather than trusting it blindly after a large
  reorganization.
- For multi-file documents (`\input{}`/`\include{}`), use `latexdiff-vc` or
  run `latexdiff` per included file and reassemble, rather than diffing
  only the top-level `.tex` file, which will miss changes inside included
  files entirely.
- Strip the diff markup before final submission — the diff version is for
  referees/co-authors during review, not the camera-ready submission;
  `submission-and-peer-review.md` covers when a marked-up version is
  expected versus a clean one.
