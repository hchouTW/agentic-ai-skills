# Submission and Peer Review

What to check immediately before submission, how to write a cover letter and an
arXiv submission, and how to structure a referee response once reviews come back.

## Table of contents
- [Pre-submission checklist](#pre-submission-checklist)
- [Cover letters](#cover-letters)
- [Authorship and contributions](#authorship-and-contributions)
- [arXiv submission mechanics](#arxiv-submission-mechanics)
- [Responding to referee reports](#responding-to-referee-reports)
- [Conference-style rebuttals](#conference-style-rebuttals)
- [Tracking revisions](#tracking-revisions)

## Pre-submission checklist

Run through this (and `scripts/check_manuscript.py`) before the user submits:

- [ ] Every number in the abstract matches the corresponding number in Results
- [ ] Every `\cite{}` resolves; every `.bib` entry is used (script-checkable)
- [ ] Every `\ref{}`/`\eqref{}` resolves; no duplicate `\label{}`s (script-checkable)
- [ ] Figures/tables are numbered in the order they're first referenced in text
- [ ] Units are stated on every quantitative result
- [ ] Statistical vs. systematic uncertainty is distinguished wherever both apply
- [ ] Length/page limit for the target venue is met
- [ ] Author list, affiliations, and acknowledgments match the current
      collaboration-approved list (for collaboration papers, do not
      hand-edit without the publications committee's sign-off)
- [ ] No leftover `TODO`/`FIXME`/placeholder text (script-checkable)
- [ ] Compiles cleanly from a fresh directory (catches missing files that
      happen to exist locally but weren't properly referenced)

## Cover letters

A cover letter to an editor is short (typically under one page) and states:
1. The paper title and a one-sentence summary of the result.
2. Why it's a good fit for this journal specifically (novelty, significance,
   scope match) — not a restatement of the abstract.
3. Any relevant context the editor should know before assigning referees:
   related submissions, conflicts of interest to avoid in referee selection,
   or if this is a resubmission, a one-line pointer to the response letter.

Keep it factual; avoid overselling ("groundbreaking," "unprecedented") —
editors read these constantly and plain, specific language is more
persuasive than superlatives.

## Authorship and contributions

Use to organize author-provided contributions, acknowledgments, funding, and
disclosures. Start from the supplied author list and contribution records or an
existing approved statement. Preserve names, order, affiliations, equal-contribution
notes, and corresponding-author designations unless the user supplies a correction.
Do not infer credit, seniority, author order, or authorship eligibility from job
titles, commit counts, or the amount of prose someone wrote.

Map supplied activities to the requested format. If a venue requests CRediT or
another taxonomy, consult its official current definitions and venue instructions;
roles describe contributions and do not themselves determine authorship. Several
authors may share a role and one author may have several roles. Flag ambiguous
mappings rather than assigning unstated work or imposing a contribution quota.

Keep authorship, acknowledged assistance, funding, and competing-interest
disclosures distinct. Use exact supplied funder names and grant identifiers.
Never infer "no competing interests" from silence or invent consent to be named
in acknowledgments. Record missing declarations as inputs needed from the relevant
authors; do not resolve an authorship dispute by choosing a side.

For large collaborations, use the provided collaboration convention and approved
boilerplate rather than forcing individual roles onto a collective author list.
If an AI-use disclosure is requested or required by the venue, describe the actual
assistance from known records without inventing tool versions or usage details.

Deliver the formatted statement, a role-to-author mapping when helpful, and
unresolved factual questions. Distinguish draft wording from author-confirmed
declarations; drafting does not authorize contacting authors or submitting forms.

## arXiv submission mechanics

- Submit source (not just a compiled PDF) so arXiv can recompile and readers
  can access the LaTeX source.
- Double-check the abstract text entered in arXiv's web form matches the
  paper's actual abstract exactly (these are edited independently and drift
  is a common, easily-avoided error).
- Choose categories carefully (primary + cross-lists) — this affects who sees
  the paper and which moderators review it; see
  `latex-and-formatting.md#arxiv-specific-rules`.
- For collaboration papers, follow the collaboration's internal approval
  process before arXiv submission — arXiv submission is often the public
  step *after* internal review, not a substitute for it.
- Don't assume every collaboration posts an arXiv preprint at all — some
  (e.g. AMS-02) publish directly to the journal with no arXiv companion, by
  policy, not oversight. Confirm the collaboration's own practice (check its
  recent papers on INSPIRE-HEP for a populated `arXiv:` field) before
  defaulting to "submit to arXiv first." See
  `astroparticle-and-cosmic-ray-papers.md`'s AMS-02 case study.

## Responding to referee reports

Structure a response letter point-by-point, in the same order as the
referee's report:

1. Quote (or closely paraphrase) each referee comment.
2. State clearly what was changed, with a pointer to the specific location
   in the revised manuscript ("This has been clarified in Sec. III,
   paragraph 2, now reading: ...").
3. If a comment is **not** being followed, say so explicitly and give the
   physics or editorial reason — silence on a disputed point reads as an
   oversight and invites a repeat request in the next round.
4. Keep tone factual and non-defensive even when the referee's comment seems
   to misunderstand the paper — a calm, precise clarification resolves this
   faster than a defensive tone, and referees are often right about
   something even when their specific framing is off.
5. End with a short summary of the overall changes if the revision was
   substantial, so the editor doesn't have to reconstruct it from the
   point-by-point list.

## Conference-style rebuttals

ML/AI conferences (NeurIPS, ICML, ICLR, AAAI, CVPR/ICCV/ECCV) replace the
multi-round referee-response cycle above with a single-shot rebuttal, and the
difference in mechanics changes how to write the response:

- **One window, no further revision round.** Unlike a journal, there is no
  "revise and resubmit" — the rebuttal is the only chance to respond before the
  accept/reject decision, so address every reviewer's concern concretely within
  the given space rather than promising a fix for "the camera-ready version"
  unless the venue explicitly allows that.
- **Strict length limits** (often a fixed word or character count, sometimes a
  single PDF page) mean prioritizing what could actually flip a borderline
  score over addressing every minor point exhaustively — triage the reviewer
  comments by which ones matter most to the final decision.
- **The rebuttal is often a public record** (OpenReview, for ICLR and
  increasingly other venues) — write it knowing it may be read by anyone, not
  as a private letter to an editor the way a journal response letter is.
- **Area chairs and meta-reviews sit above the raw reviewer scores** — a
  rebuttal that changes how one reviewer frames their concern can matter even if
  the numeric score doesn't move, since the meta-review weighs the discussion
  holistically.
- **Camera-ready deadlines are hard and non-negotiable** — unlike a journal's
  more flexible production schedule, missing it can mean the paper doesn't
  appear in the proceedings at all, so don't leave a promised post-acceptance
  fix until the last possible day.

See `statistics-and-ml-papers.md` for the fuller venue-by-venue picture,
including ACL Rolling Review's different (journal-like, revision-carrying)
cadence.

## Tracking revisions

For tracing a changed result or reviewer request across the paper, figures,
supplements, and response letter, use `revision-impact-tracking.md`. It provides
a dependency ledger and distinguishes edits made from changes actually verified.

- Keep a `CHANGES.md` or similar running log during revision, noting what
  changed and why — this becomes the raw material for the response letter
  and for the collaboration's internal review trail.
- Use `\textcolor{}` or `latexdiff`-style tracked changes for a version
  sent to co-authors/collaboration reviewers, but strip all tracked-change
  markup before the actual journal resubmission unless the venue explicitly
  requests a marked-up version.
- Version the `.bib` file alongside the `.tex` file in revisions — reference
  lists frequently need small additions in response to referee comments
  ("please cite prior measurement by...").
