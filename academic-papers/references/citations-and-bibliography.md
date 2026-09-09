# Citations and Bibliography

Where to source BibTeX entries, how to keep a `.bib` file clean as a paper evolves,
and venue-specific citation-style expectations.

## Table of contents
- [INSPIRE-HEP workflow](#inspire-hep-workflow)
- [ADS for astroparticle/astronomy-facing venues](#ads-for-astroparticleastronomy-facing-venues)
- [arXiv, DBLP, and ACL Anthology for statistics/ML venues](#arxiv-dblp-and-acl-anthology-for-statisticsml-venues)
- [BibTeX hygiene](#bibtex-hygiene)
- [Citation style by venue](#citation-style-by-venue)
- [What to cite, and how much](#what-to-cite-and-how-much)
- [Linking supplemental material and data](#linking-supplemental-material-and-data)
- [Avoiding common bibliography mistakes](#avoiding-common-bibliography-mistakes)

## INSPIRE-HEP workflow

For HEP papers, INSPIRE-HEP (inspirehep.net) is the standard source of BibTeX
entries — it is maintained, includes arXiv/journal cross-references, and its
keys are recognized by collaborators and referees. Workflow:

1. Search the paper on INSPIRE-HEP by title, author, or arXiv number.
2. Use INSPIRE's "Cite" / export feature to get a BibTeX entry with its
   standard key format (e.g. `Aad:2012tfa` — first author surname, year,
   short hash).
3. Paste the entry as-is into the `.bib` file rather than retyping it by
   hand — this preserves the `eprint`, `archivePrefix`, `doi`, and `journal`
   fields that different `.bst` styles rely on.
4. Keep INSPIRE's key format even if it looks unfamiliar — collaboration
   co-authors and referees often expect it, and it avoids key collisions
   across a large `.bib` file.

Never fabricate a citation or a plausible-looking INSPIRE key — if the exact
reference can't be located, mark it (`[CITATION NEEDED: original ATLAS
combined mass paper]`) rather than inventing one.

## ADS for astroparticle/astronomy-facing venues

For astroparticle-physics and cosmic-ray papers targeting ApJ/ApJL, A&A, or MNRAS
(rather than PRD/JHEP/JCAP), the NASA Astrophysics Data System (ADS,
`ui.adsabs.harvard.edu`) is the dominant citation database, not INSPIRE-HEP:

1. Search ADS by title, author, or arXiv number; export the BibTeX entry using its
   `bibcode` key format (e.g. `2017ApJ...848L..12A`), analogous to INSPIRE's
   `Aad:2012tfa`-style keys.
2. Keep the bibcode key as-is for the same reason INSPIRE keys are kept as-is —
   referees and co-authors on astronomy-side venues expect it.
3. When a paper needs both HEP-side and astronomy-side citations (common for
   multi-messenger or dark-matter-search papers), pull from whichever database
   covers that specific reference better and combine into one `.bib` file;
   deduplicate by DOI if the same paper is pulled from both databases under
   different keys.

See `astroparticle-and-cosmic-ray-papers.md` for when to prefer ADS vs. INSPIRE-HEP
by venue, and for the `natbib` author-year citation style common to these journals.

## arXiv, DBLP, and ACL Anthology for statistics/ML venues

Statistics and ML papers have no single dominant citation database the way
physics has INSPIRE-HEP — which source to use depends on where the specific paper
was actually published:

1. **arXiv's own BibTeX export** for a preprint that was never separately
   published, or when the point being made depends on a specific arXiv version
   (`v1`, `v2`, ...) — cite the version number explicitly if content changed
   between versions, since an arXiv preprint is mutable in a way a published
   paper is not.
2. **DBLP** (`dblp.org`) for a conference-proceedings paper — strong, clean
   per-paper BibTeX export with a stable key, especially good for ML/AI
   conferences (NeurIPS, ICML, ICLR, AAAI, CVPR/ICCV/ECCV).
3. **ACL Anthology** (`aclanthology.org`) for any ACL/EMNLP/NAACL paper — the
   canonical source for NLP-venue papers, with its own BibTeX export matching
   the venue's own citation key conventions.
4. **Semantic Scholar** (web export or API) as a fallback that covers most of the
   above plus general citation-graph lookups, useful when quickly locating a
   paper's canonical published venue is the actual blocker.

A large fraction of the field's own citations are to arXiv preprints that were
never formally published elsewhere, or where the arXiv version and the
camera-ready conference version differ non-trivially — this is normal here in a
way it isn't in physics, so don't treat an arXiv-only citation as necessarily
incomplete. See `statistics-and-ml-papers.md` for the venue-specific citation
*style* (numbered vs. `natbib` author-year) that goes with these sources.

## BibTeX hygiene

- One `.bib` file per paper (or per collaboration-shared library), not one
  per section — makes deduplication and `check_manuscript.py`-style
  validation possible.
- Deduplicate by INSPIRE key before dedup by title/author — two entries with
  slightly different formatting for the same paper is the most common
  bibliography bug.
- Every entry in the `.bib` file should be cited at least once in the final
  text, and every `\cite{}` in the text should resolve to an entry — see
  `scripts/check_manuscript.py` in this skill for an automated check.
- For preprints that were later published, prefer the published version's
  entry (with `doi`) once available, keeping the `eprint` field for the
  arXiv number as backup.

## Citation style by venue

| Venue | Style | Notes |
|---|---|---|
| PRL/PRD/PRX (APS) | Numbered, `\bibliographystyle{apsrev4-2}` | Author list style depends on entry count; APS's style handles this automatically |
| JHEP | Numbered, `\bibliographystyle{JHEP}` | Expects INSPIRE-formatted entries with `eprint`/`archivePrefix` |
| EPJC (Springer) | Numbered, Springer physics style | Similar expectations to JHEP |
| Nature family | Numbered, superscript, Nature `.bst` | Very compressed reference format; check current author guidelines for the exact fields required |
| JCAP (astroparticle) | Numbered, `\bibliographystyle{JHEP}` | Same expectations as JHEP; INSPIRE-formatted entries |
| ApJ/ApJL, A&A, MNRAS | `natbib` author-year (`\citep{}`/`\citet{}`) | ADS-sourced entries are the norm; check the venue's current `.bst` |
| NeurIPS/ICML/ICLR/AAAI/CVPR | Numbered, conference-specific `.bst` | DBLP-sourced entries are common; many entries are arXiv-only |
| ACL/EMNLP/NAACL | `natbib` author-year via shared ACL style file | ACL Anthology-sourced entries expected |
| JMLR/TMLR, statistics journals | Varies by venue; often `natbib` author-year | Check the specific journal/venue's current style |

Do not hand-adjust citation numbering or format — let the `.bst` style file
handle it; manual tweaks break on any bibliography addition/removal.

## What to cite, and how much

- Cite the original measurement/derivation, not just a review article that
  mentions it, when precision about *who* did *what* matters (e.g. "as first
  measured in [X]").
- Cite the specific detector/reconstruction paper being relied on (tracking
  algorithm, calibration paper) rather than only the general detector paper,
  when the analysis depends on that specific tool's performance.
- Cite Monte Carlo generators and tunes by version (e.g. Pythia 8.3 with a
  specific tune) — cite both the generator paper and the tune paper if they
  differ.
- Avoid citation stuffing (a string of 5+ references for an uncontroversial
  general statement) — pick the 1-2 most relevant/foundational.

## Linking supplemental material and data

Beyond the reference list itself, point readers to where the underlying numbers
live:

- **HEPData** (`hepdata.net`) is the standard repository for collider-physics
  digitized tables, cutflows, and machine-readable versions of a paper's plots —
  link it explicitly in the paper (footnote or a dedicated "Data availability"
  statement) rather than assuming a reader will find it by searching.
- **Some collaborations host supplemental data on their own site instead of, or in
  addition to, HEPData.** AMS-02 is a concrete example: its publications page
  (`ams02.space/publications`) links "supplemental material and data" per paper
  directly alongside the journal DOI, separate from any HEPData record. Check the
  specific collaboration's convention before assuming HEPData is the only place a
  result's tables will be published.
- State clearly in the paper *which* venue holds the data (HEPData record number,
  a collaboration data-release URL, or a Zenodo/institutional DOI) rather than a
  vague "data available upon request," which most venues now discourage or forbid.

## Avoiding common bibliography mistakes

- **Orphaned entries**: `.bib` entries never cited in the final text — these
  accumulate as drafts evolve; `check_manuscript.py` flags them.
- **Missing entries**: a `\cite{key}` with no matching `.bib` entry, often
  from a typo in the key or an entry deleted during cleanup.
- **Duplicate physical papers under different keys**: happens when co-authors
  independently pull the same INSPIRE entry with slightly different export
  settings — dedupe by INSPIRE key or arXiv number, not by BibTeX key string.
- **Self-citation imbalance**: a healthy reference list cites the field
  broadly, not disproportionately the authors' own prior work — referees
  notice and sometimes flag this explicitly.
