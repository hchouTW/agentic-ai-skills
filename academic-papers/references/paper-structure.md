# Paper Structure

Detailed section-by-section guidance for physics papers, plus notes on how the
structure shifts for theory papers, review articles, proceedings, thesis chapters,
astroparticle/cosmic-ray papers, statistics/ML papers, and public-facing outreach
summaries. Read the relevant subsection rather than the whole file when
time-pressed.

## Table of contents
- [Title](#title)
- [Abstract](#abstract)
- [Abstract and title variants](#abstract-and-title-variants)
- [Argument restructuring](#argument-restructuring)
- [Introduction](#introduction)
- [Detector / Dataset / Methods](#detector--dataset--methods)
- [Analysis](#analysis)
- [Systematic uncertainties](#systematic-uncertainties)
- [Results](#results)
- [Summary / Conclusion](#summary--conclusion)
- [Theory papers](#theory-papers)
- [Review articles](#review-articles)
- [Thesis chapters](#thesis-chapters)
- [Proceedings](#proceedings)
- [Astroparticle and cosmic-ray papers](#astroparticle-and-cosmic-ray-papers)
- [Statistics and ML papers](#statistics-and-ml-papers)
- [Outreach and public-facing summaries](#outreach-and-public-facing-summaries)
- [Outreach: collaboration voice vs. syndicated commentary](#outreach-collaboration-voice-vs-syndicated-commentary)

## Title

- States the *result*, not the method: "Measurement of the top-quark mass in
  ttbar events" beats "A study of ttbar events using kinematic reconstruction."
- Avoid acronyms unless they are field-standard (LHC, ATLAS is fine; a
  collaboration-internal acronym is not).
- No punctuation-heavy titles ("Results, revisited: a new look at...") for
  experimental papers; theory papers have more latitude.
- Keep it under ~15 words where the venue doesn't dictate otherwise.

## Abstract

The abstract is a self-contained paper in miniature. A referee, and most readers,
decide whether to keep reading based on this paragraph alone. Structure (roughly
one to two sentences each):

1. **Context** — what physics question, in one sentence, assuming an educated
   physicist reader but not a specialist in this exact sub-topic.
2. **What was done** — data source, method, in the fewest words that are still
   accurate ("Using 139 fb⁻¹ of pp collisions at √s = 13 TeV recorded by ATLAS...").
3. **The result** — the number, with uncertainty, and its statistical
   significance if relevant. This is the sentence people will quote.
4. **Significance / comparison** — how it compares to previous measurements or
   theory predictions, and why it matters.

Do not cite references in the abstract (most venues disallow it). Do not
introduce new terminology in the abstract that isn't defined in the main text.
Write the abstract *last*, after the results are final — it should never be
the place where a number is decided.

## Abstract and title variants

Use when asked to optimize a title/abstract or adapt it to a venue, audience, or
length limit. Establish the intended reader and constraints from the request;
verify current official venue rules when needed. Treat the generic conventions
above as defaults, not universal requirements. A methods paper can appropriately
foreground its method rather than a measurement.

Extract the factual core from the manuscript: question, approach, dataset/regime,
main result and uncertainty, and bounded implication. Preserve this core across
variants. If a result is missing, mark the missing input; do not invent a number or
convert a planned experiment into a completed one.

Produce meaningfully different variants only as useful or requested, such as one
for specialists and one for a broader scientific readership. Label the purpose
and give measured word/character counts when a limit applies, stating the counting
convention if ambiguous. Improve specificity and searchability with accurate field
terms, without keyword stuffing or claims of guaranteed discoverability.

Check each version against the Results and limitations: preserve qualifiers,
uncertainty conventions, tested scope, and the distinction between association
and causation or evidence and discovery. A shorter version may omit secondary
detail but must not broaden the conclusion. Recommend the version that fits the
stated constraints and explain any substantive wording tradeoff briefly.

## Argument restructuring

Use when a draft's logic or organization needs improvement. Build a reverse
outline: each paragraph/section's purpose, claim, evidence, and prerequisites.
Trace the central chain from question to method to result to interpretation using
`claim-evidence-mapping.md` when support is disputed, or
`logical-consistency-and-argument-uniformity.md` for a full diagnostic pass over
contradictions, fallacies, and dropped assumptions before restructuring.

Identify missing premises, circular reasoning, definitions introduced too late,
duplicated arguments, abrupt shifts, and conclusions broader than the evidence.
Distinguish a presentation gap from a missing analysis: rearranging text cannot
repair an unsupported scientific inference.

Propose a revised outline with each section's role and an old-to-new location map
for substantial moves. Put prerequisites before dependent claims while following
the target genre; a review, theory paper, and experimental report need different
structures. Preserve caveats beside the claims they qualify and avoid moving
essential evidence to supplements merely to simplify the narrative.

If editing is requested, make the structural changes, repair transitions and
cross-references, and preserve supported technical content and author voice.
Flag required evidence or author decisions rather than supplying invented bridges.
Deliver the revised draft/outline with a brief explanation of the consequential
moves and remaining logical gaps.

## Introduction

- Open with the physics motivation in 2-4 sentences: why does this measurement or
  calculation matter, aimed at a broad-but-expert reader.
- Summarize the state of the art: what has been measured/calculated before, with
  citations, and what its limitations were (precision, assumptions, energy regime).
- State explicitly what this paper adds that is new — do not make the reader infer
  it from the rest of the paper.
- End with a one-sentence roadmap only if the paper is long or has an unusual
  structure; for a 4-page PRL this is often unnecessary.
- Avoid a literature-review tone that reads as padding — every citation here should
  be doing work (establishing precedent, motivating the measurement, or setting up
  a comparison used later in Results).

## Detector / Dataset / Methods

- State the experiment/detector, the dataset (collision energy, integrated
  luminosity, run period), and any triggers or preselection, in enough detail that
  an expert in the field could judge whether the dataset is adequate — not enough
  to re-derive the detector design.
- For theory/phenomenology papers, this section becomes "Methods" or
  "Theoretical Framework": the model, approximations, and tools (generators,
  codes) used, with version numbers and citations.
- Cite the detector paper and any relevant Monte Carlo generator papers here, not
  scattered through the analysis section.

## Analysis

- Describe the event selection / calculation pipeline as a narrative, not a list
  of every cut ever tried — the reader needs the selection that produced the final
  result, plus enough of the *why* to trust it (e.g. "electrons are required to
  have pT > 25 GeV to suppress QCD background, as validated in Sec. X").
- State background estimation methods explicitly, including whether they are
  data-driven or simulation-based, and validate with a control region if one
  exists.
- Use a cutflow table when it clarifies rather than clutters — see
  `figures-and-tables.md`.
- Keep derivations that are standard (well-known formulas, standard fit
  functions) brief with a citation; reserve full derivation space for anything
  novel to this paper.

## Systematic uncertainties

- Organize by source (detector calibration, theoretical modeling, background
  estimation, luminosity, statistical) not by which cut they affect.
- State how each systematic was evaluated (envelope of variations, alternate
  generator comparison, data/MC scale factor uncertainty propagated) — "assigned
  as X%" without justification invites referee pushback.
- Summarize in a table (source → size → whether correlated across bins/channels)
  even if the accompanying text is short.
- Distinguish clearly, in both text and any result quoted, statistical vs.
  systematic uncertainty (e.g. `125.3 ± 0.4 (stat) ± 0.6 (syst) GeV`).

## Results

- Lead with the headline number, stated plainly, before any supporting plot
  discussion.
- Compare explicitly to the Standard Model prediction or the previous best
  measurement — state the pull/tension in standard deviations if that's the
  relevant metric, and avoid over- or under-stating significance (see
  `scientific-style.md` for phrasing conventions around "evidence" vs.
  "observation" vs. "excess").
- If there are multiple channels/bins, a summary figure (often the paper's
  Figure 1 candidate) usually communicates more than a results table alone —
  but include both if space allows.

## Summary / Conclusion

- Restate the result in one or two sentences, without new numbers not already
  given in Results.
- One sentence on implications (what this constrains or rules out) and,
  optionally, one on outlook (what would improve it — more data, next-gen
  detector). Do not oversell; referees notice.
- No new citations here except perhaps a forward pointer to planned/ongoing work.

---

## Theory papers

The template shifts: Introduction → Model/Formalism → Calculation → Results/
Phenomenology → Discussion. Expect (and budget space for):
- A longer, self-contained derivation section — theory referees expect to be
  able to follow the calculation, not just cite the result.
- Explicit statement of assumptions and their validity range early, since the
  entire paper's conclusions are conditional on them.
- A phenomenology section translating the formal result into observable
  predictions, ideally compared against existing or near-future experimental
  sensitivity.

## Review articles

Structured more like a textbook chapter: broad Introduction, then organized by
sub-topic rather than by "what we did" — since there is no single "we did X."
Expect a much larger reference list, an explicit statement of scope (what is
and isn't covered, and why), and a closing "open questions" section rather than
a conclusion restating a single result.

## Thesis chapters

Similar backbone to a paper but expanded: include material a paper would cut
for space (fuller derivations, more validation plots, negative results/things
tried that didn't work, more detail on personal contribution vs.
collaboration-wide work). A thesis chapter based on a published paper should
still be written in the author's own words, not pasted from the paper, both
for originality and because the fuller thesis context changes what needs
explaining.

## Proceedings

Short (often 4-10 pages), summarizing a talk rather than presenting a full new
result: Introduction (brief) → the one or two key plots/results shown at the
conference → brief conclusion. Assume the reader has seen, or could look up,
the full paper this proceeding is based on — proceedings should not duplicate
a full paper's derivations.

## Astroparticle and cosmic-ray papers

The same backbone applies, with "Detector" becoming "Instrument"/"Observatory"/
"Array," "luminosity" becoming "exposure," and — for point-source or anisotropy
searches — an arrival-direction section with its own pre-trial/post-trial
significance treatment, separate from the energy-spectrum section. Atmospheric and
hadronic-interaction-model systematics (QGSJET, EPOS, Sibyll, ...) typically dominate
the systematics section for air-shower analyses, in place of detector-alignment
systematics. See `astroparticle-and-cosmic-ray-papers.md` for the full treatment,
including venue-specific conventions (JCAP, ApJ/ApJL, Astroparticle Physics),
collaboration author-list handling for ground arrays/IACTs/space detectors, and
skymap/energy-spectrum figure conventions.

## Statistics and ML papers

The backbone shifts more here than for any other variant in this file: Related
Work is usually its own section rather than woven into the Introduction, and
Limitations and (at several venues) a Broader Impact/Ethics Statement are
required, separately-labeled sections rather than closing remarks. A
reproducibility checklist is often a required submission component, not optional
prose, and the appendix routinely carries full hyperparameter tables and
additional experiments that reviewers are expected to actually read - unlike a
physics paper's supplemental material, which a referee may or may not open. See
`statistics-and-ml-papers.md` for the full treatment, including venue-specific
conventions (NeurIPS/ICML/ICLR/ACL vs. JMLR/TMLR vs. statistics journals),
author-contribution statements, arXiv-first citation practice, and the
single-shot rebuttal process that replaces a journal's multi-round revision.

## Outreach and public-facing summaries

A different document from the paper itself: a plain-language summary for a
collaboration or institution website, aimed at a general audience rather than
referees. Structure:

1. **One headline sentence in plain language** — the result, not the method, with
   jargon either cut or immediately explained ("cosmic rays — high-energy particles
   from space — ...").
2. **One analogy or framing sentence** for the physics question, aimed at a reader
   with no physics background.
3. **One figure**, usually the paper's own headline plot, simplified or re-labeled
   if the original axis labels assume physics literacy.
4. **A short "why it matters" close** — connects to a bigger open question (dark
   matter, the origin of cosmic rays, antimatter in the universe) without
   overselling.

Rules that don't relax just because the audience is general:
- **Never state a number, uncertainty, or significance not in the paper itself** —
  a public summary can omit precision, not invent it.
- **Match the paper's own significance language**: if the paper says "excess" or
  "hint," the public summary should not upgrade that to "discovery" — see
  `scientific-style.md`'s significance-language table, which applies to outreach
  writing just as much as the paper itself.
- Simplify the *explanation*, not the *claim* — a public summary that makes the
  result sound bigger than the paper's own abstract is a form of overstating
  significance, even without a technical error in it.

## Outreach: collaboration voice vs. syndicated commentary

Not every "physics highlight" page on a collaboration's own website is written by
the collaboration. AMS-02's `ams02.space/physics/*` pages are a useful worked
example precisely because checking the actual byline on each one — rather than
assuming collaboration authorship because the page lives on the collaboration's
domain — turns up three different genres:

- **Journalist-written recap**, e.g. "AMS Releases New Cosmic-Ray Measurements"
  (byline: Emma Hattersley, dated 2026-06-26) — third-person journalistic voice
  ("reports," "describes"), built around direct quotes from collaboration
  spokespeople (Samuel Ting, Sunil Gupta) rather than a first-person collaboration
  statement.
- **APS *Physics Magazine* Synopsis**, e.g. "Lithium Cosmic Rays Are Not
  Primordial" (byline: Rachel Berkowitz, "Corresponding Editor for *Physics
  Magazine*") — a neutral staff-written recap syndicated from `physics.aps.org`,
  not authored by the collaboration at all.
- **APS *Physics Magazine* Viewpoint**, e.g. "Antiprotons Beyond the Solar
  System" (byline: N. Eugene Engelbrecht and R. Du Toit Strauss, Centre for Space
  Research, North-West University, cited as *Physics* 18, 19 (2025)) — an
  *invited outside expert's* independent commentary and context, carrying its
  own citable byline, affiliation, and issue number, distinct from both the
  collaboration's and a journalist's voice.

All three end with a "Publication" call-out box giving the underlying PRL's full
citation and DOI — a reusable design pattern regardless of which of the three
voices is in use.

Why this distinction matters when drafting one of these for a user:
- **Ask which of the three is actually wanted** before drafting: an in-house
  collaboration-voice press release ("we report...") is a different document,
  with a different acceptable level of first-person collaboration claims, than a
  pitch written in third-person journalistic voice, or a Viewpoint — which only
  an actual outside expert can author, not something to draft on someone else's
  behalf and attribute to them.
- **Never draft one of these and attribute it to the wrong voice** — labeling a
  drafted Viewpoint or Synopsis as collaboration-authored (or vice versa)
  misrepresents its independence to a reader.
- **When citing one**, treat it as secondary commentary, not primary literature —
  see `citations-and-bibliography.md`'s note on citing an accompanying Viewpoint
  or Synopsis.

(Verified 2026-09-10 by checking each page's own byline directly rather than
assuming authorship from the hosting domain — re-check before reusing this as a
current example, since AMS periodically publishes new physics-highlight pages
and the mix of voices may change.)
