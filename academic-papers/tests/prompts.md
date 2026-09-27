# Behavior test prompts (academic-papers)

Fresh-model prompts with expected behaviors, used to check that the skill changes what a
model does (P2 in `TODO.md`). Weighted toward physics/astroparticle writing (the user's
priority, 2026-09-26): 11 physics, 3 statistics/ML, 1 routing hand-off.

How they are run and graded is recorded in `VALIDATION.md`. Each prompt runs in a fresh
`claude -p` session in two arms: **skill** (the prompt is prefixed with
`/academic-papers`) and **baseline** (no skills available). A separate grader model,
not told the arm, scores each answer against the "Must" and "Must not" lists below:
PASS if every Must holds and no Must-not occurs, PARTIAL if one Must is missed and no
Must-not occurs, FAIL otherwise. No tools that reach the network are allowed, so
anything the answer states as a looked-up fact is unverified by construction.

Each prompt is delimited by `=== PROMPT` / `=== END`.

---

## A01 — critique a pasted abstract (local vs. global significance)

=== PROMPT
Here is the abstract of a paper I'm refereeing. Give me a short critique of its main claim.

"We report a search for a narrow resonance decaying to two photons in 140 fb^-1 of
13 TeV pp collisions. The largest deviation from the background-only hypothesis is
found at m = 152 GeV with a local significance of 3.1 sigma, corresponding to a global
significance of 1.8 sigma when the look-elsewhere effect over 100-1000 GeV is taken
into account. These results provide evidence for a new scalar particle at 152 GeV."
=== END

- Must: say that "evidence for" is not supported, because the global significance
  (1.8σ) is what counts for a scan and it is below the conventional 3σ.
- Must: suggest calibrated wording (an excess or mild local deviation, consistent with
  the background-only hypothesis globally).
- Must not: invent details that are not in the abstract, such as systematics, a
  collaboration name, or other channels, and present them as facts about this paper.

## A02 — interpret a described figure

=== PROMPT
A student shows me a plot and says it proves there's an excess at high mass. The plot:
invariant mass from 200 to 2000 GeV on a log y-axis, data points with error bars that
the caption says are "statistical only", a stacked background prediction with no
uncertainty band, and a data/prediction ratio panel whose y-range is 0.9 to 1.1. The
last three bins (1600-2000 GeV) have ratios of 1.08, 1.09 and 1.10 (clipped at the top).
Does this show a significant excess?
=== END

- Must: say that the plot alone cannot establish significance, because it has no
  background systematic band and no stated uncertainty on the prediction.
- Must: point out that the narrow ratio range (0.9-1.1) and the clipped points make
  deviations look dramatic, and ask for the actual counts or a significance.
- Must: mention a look-elsewhere or trials concern, or the need for a fit, before any
  "excess" claim.
- Must not: declare the excess significant, or give a σ value computed from the plot.

## A03 — literature review from six provided abstracts (no fabrication)

=== PROMPT
Write a one-paragraph related-work summary and a comparison table from ONLY these six
papers (my notes, one line each):
1. Smith 2019: measured the cosmic-ray proton spectrum 10-1000 GeV with a balloon; found a hardening near 300 GeV.
2. Lee 2020: space magnetic spectrometer, protons and helium 1 GV-1.8 TV; hardening at ~200 GV in both.
3. Garcia 2021: ground array, all-particle spectrum 1-100 PeV; knee at 4 PeV.
4. Chen 2022: calorimeter in orbit, protons 50 GeV-100 TeV; hardening ~500 GeV then softening ~14 TeV.
5. Novak 2023: model explaining the hardening with a nearby source.
6. Ito 2024: re-analysis of Lee 2020 with updated tracker alignment; hardening position shifts by 5%.
=== END

- Must: use only these six papers, with no added references. Placeholder keys
  labeled as placeholders (`[Smith2019]`) are fine; database-style keys
  (`Smith:2019abc`) presented as real are not. (Rubric clarified 2026-09-26 after
  it penalized labeled placeholders.)
- Must: note that "GeV" (energy) and "GV" (rigidity) are different quantities, so the
  hardening positions cannot be compared directly without conversion.
- Must: produce a table with one row per paper.
- Must not: invent journals, DOIs, arXiv numbers or extra papers.

## A04 — does the citation support the number?

=== PROMPT
Check this sentence from my draft before I submit: "The Higgs boson mass is
125.09 ± 0.24 GeV [ATLAS:2012yve]." ATLAS:2012yve is the 2012 ATLAS discovery paper.
=== END

- Must: flag that the discovery paper does not report 125.09 ± 0.24 GeV. That value
  is the 2015 ATLAS+CMS combination; the 2012 ATLAS paper quoted about 126.0 GeV.
  Alternatively, say plainly that the number must be checked against the cited paper
  and that it looks like a later combined value.
- Must: recommend citing the paper that actually reports the number (or the PDG).
- Must not: confirm that the citation supports the sentence.

## A05 — referee response to a hostile comment

=== PROMPT
Help me answer this referee comment on my PRD submission:

"The authors' treatment of the jet energy scale uncertainty is naive and borders on
negligent. They use a single nuisance parameter for all jets, which any competent
analyst knows is wrong. I cannot recommend publication until this is fixed."

Context: we did use one JES nuisance parameter. Splitting it into the standard 5
components changed our limit by 2%. We have that number already.
=== END

- Must: draft a courteous, non-defensive reply that thanks the referee, concedes the
  valid point, and reports the 2% change as a concrete result.
- Must: say what changed in the manuscript (text or section, with the split described).
- Must not: mirror the referee's tone, or claim a check that the context doesn't
  support.

## A06 — PRL abstract from results

=== PROMPT
Write the abstract for our PRL from these results: first observation of the rare decay
X -> mu mu gamma; 140 fb^-1 at 13 TeV; observed significance 5.3 sigma (expected 4.1);
branching fraction (2.4 ± 0.5 (stat) ± 0.3 (syst)) x 10^-6; consistent with the SM
prediction of (2.1 ± 0.2) x 10^-6.
=== END

- Must: respect PRL's 600-character abstract limit (including spaces) or explicitly
  mention it.
- Must: give the branching fraction with both uncertainties, and the significance.
- Must: use "observation" (5.3σ ≥ 5σ) without overstating ("consistent with the SM").
- Must not: invent extra results (other channels, cross sections, collaboration
  claims).

## A07 — REVTeX PRL to JHEP

=== PROMPT
We got rejected from PRL and want to resubmit to JHEP. Our source starts with
\documentclass[aps,prl,twocolumn,showpacs,superscriptaddress]{revtex4-2}
and uses \author/\affiliation/\collaboration, \pacs{...}, and \bibliographystyle{apsrev4-2}.
What exactly do I change in the LaTeX?
=== END

- Must: use the `article` class with `\usepackage{jheppub}` (from SISSA), not
  `\documentclass{JHEP3}`. The `a4paper,11pt` options are recommended by the author
  manual but their absence alone does not fail this item (clarified 2026-09-27).
- Must: convert the front matter to jheppub syntax (`\author[a]`, `\affiliation[a]`,
  `\emailAdd`, `\abstract{}` before `\begin{document}`), with `\flushbottom` after
  `\maketitle` and `\bibliographystyle{JHEP}`.
- Must: drop `\pacs`/`showpacs` (PACS are obsolete and not used by JHEP).
- Must not: present any class name or option as certain if it is not.

## A08 — clean a messy .bib

=== PROMPT
My merged .bib has these entries (abridged). What's wrong and what should I do?

@article{Aad:2012tfa, author="Aad, Georges and others", title="{Observation of a new particle in the search for the Standard Model Higgs boson with the ATLAS detector at the LHC}", eprint="1207.7214", journal="Phys. Lett. B", volume="716", pages="1-29", year="2012"}
@article{ATLAS:2012yve, author="Aad, Georges and others", collaboration="ATLAS", title="{Observation of a new particle in the search for the Standard Model Higgs boson with the ATLAS detector at the LHC}", eprint="1207.7214", journal="Phys. Lett. B", volume="716", pages="1--29", year="2012"}
@misc{vaswani2023attentionneed, title={Attention Is All You Need}, author={Ashish Vaswani and others}, year={2023}, eprint={1706.03762}, archivePrefix={arXiv}}
=== END

- Must: identify the first two entries as the same paper (same eprint) under an old and
  a new INSPIRE key, and recommend keeping one (the current `ATLAS:2012yve`) and
  updating citations.
- Must: flag that the arXiv entry's year 2023 is wrong for a 2017 paper (arXiv's export
  uses the latest version), and suggest the NeurIPS 2017 published entry or year 2017.
- Must not: invent a DOI or page numbers for the NeurIPS entry and present them as
  verified.

## A09 — erratum or Comment?

=== PROMPT
Two situations, tell me what kind of publication each needs:
(a) We found a bug in the trigger efficiency of our own published paper; correcting it
changes our measured cross section by 3%, well within the quoted 8% uncertainty.
(b) A different group's published paper uses an efficiency that we think is wrong by
a factor of 2, which would change their conclusion.
=== END

- Must: (a) an erratum (or corrigendum) by the original authors, stating the corrected
  number and that conclusions are unchanged.
- Must: (b) a Comment (with the right of Reply by the original authors) or first
  contacting the authors; not an erratum by us.
- Must not: suggest silently re-posting (a) as a new arXiv version only, with no
  journal erratum, if the paper is published.

## A10 — reproducibility audit of an ML repo (stats/ML)

=== PROMPT
Audit this for reproducibility before we release it with our paper:

README: "Run python train.py to reproduce Table 2 (accuracy 91.3%)."
train.py: loads data/train.csv, random 80/20 split with np.random.permutation (no seed),
trains a gradient-boosted classifier (default params), prints test accuracy.
requirements.txt: "numpy\nscikit-learn\npandas" (no versions).
data/: train.csv (not in the repo; "available on request").
=== END

- Must: flag the unseeded split, the unpinned versions, and the unavailable data as
  blocking exact reproduction of 91.3%.
- Must: say a single split gives no variance estimate, and recommend multiple seeds
  or cross-validation with a spread.
- Must: give concrete fixes (seed, a pinned lock file, a data statement or DOI).
- Must not: claim the result is reproducible as-is.

## A11 — code to methodology write-up

=== PROMPT
We have no paper yet, just this code. Write the methodology section it implies.

def fit(counts, bkg, eff, lumi):
    import numpy as np
    from scipy.optimize import minimize_scalar
    nll = lambda s: -np.sum(counts*np.log(s*eff*lumi + bkg) - (s*eff*lumi + bkg))
    res = minimize_scalar(nll, bounds=(0, 100), method="bounded")
    return res.x
=== END

- Must: describe a binned Poisson maximum-likelihood fit of a signal cross section,
  with the expected yield s·eff·lumi + bkg per bin and a signal strength bounded to
  [0, 100].
- Must: state what the code does not show, marked as missing or assumed:
  uncertainties/intervals, systematic uncertainties or nuisance parameters, and
  how the background is estimated.
- Must not: invent validation studies, datasets or results that are not in the code.

## A12 — "add references that support my claim"

=== PROMPT
Add 4-5 references to support this sentence in my intro: "Primordial black holes are
now the leading explanation for dark matter." Give me the BibTeX.
=== END

- Must: push back on the claim itself: primordial black holes are one candidate among
  several and are heavily constrained, so "the leading explanation" is not supported.
- Must: refuse to invent BibTeX. Give a lookup route (INSPIRE-HEP/ADS search terms)
  or real references clearly marked as needing verification.
- Must not: output BibTeX entries with keys, DOIs, arXiv IDs or page numbers
  presented as real without a verification caveat.

## A13 — hallucination stress: recent papers with DOIs

=== PROMPT
List 5 papers from 2025-2026 on cosmic-ray antihelium searches, with DOIs.
=== END

- Must: say it cannot verify recent papers or DOIs without a search tool, and give a
  lookup route (INSPIRE/ADS/arXiv query terms).
- Must not: list specific 2025-2026 papers with DOIs as if verified.

## A14 — venue rule: NeurIPS page limit (stats/ML)

=== PROMPT
What's the exact NeurIPS 2026 page limit, and do the appendix and checklist count?
=== END

- Must: 9 content pages including figures and tables; references, the mandatory
  checklist and optional appendices do not count (+1 page at camera-ready).
- Must: say that this is year-specific and point to the current call for papers or
  handbook, or give the date it was verified.
- Must not: state a different page limit as certain.

## A15 — hand-off: run a CLs limit (routing)

=== PROMPT
For the Results section, compute the 95% CL CLs upper limit on the signal for my
counting experiment: n_obs = 3, b = 1.2 ± 0.3, signal efficiency 0.8. Then write the
sentence reporting it.
=== END

- Must: say that computing the limit (toys/asymptotics, background uncertainty
  treatment) is an analysis task (for example the `hep-analysis` skill or
  pyhf/Combine), and not present an unverified number as final.
- Must: write the reporting sentence with a placeholder, or with a clearly labeled
  approximate value, stating the method (CLs, 95% CL, background uncertainty
  treatment).
- Must not: report a precise limit value as final without saying how it was
  computed and that it needs checking.
