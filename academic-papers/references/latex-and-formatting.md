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
- [arXiv-specific rules](#arxiv-specific-rules)
- [Units, numbers, and equations](#units-numbers-and-equations)
- [Common compile errors](#common-compile-errors)
- [Length-limit tactics](#length-limit-tactics)

## Getting the right class file

Never hand-copy a journal's `.cls`/`.bst` file from memory or reconstruct it —
these are maintained and versioned by the publisher/society. Get the current
version from the authoritative source:
- REVTeX 4.2 (APS: PRL, PRD, PRX, PRA, PRB, ...): APS's REVTeX page.
- JHEP: SISSA's JHEP author guidelines page (`JHEP3.cls`, `JHEP.bst`).
- EPJC: Springer's `svjour3`/`spphys` LaTeX package for Physics journals.
- Nature family: Nature's LaTeX template page (or submit in Word, per journal).

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
