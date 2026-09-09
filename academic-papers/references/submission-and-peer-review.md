# Submission and Peer Review

What to check immediately before submission, how to write a cover letter and an
arXiv submission, and how to structure a referee response once reviews come back.

## Table of contents
- [Pre-submission checklist](#pre-submission-checklist)
- [Cover letters](#cover-letters)
- [arXiv submission mechanics](#arxiv-submission-mechanics)
- [Responding to referee reports](#responding-to-referee-reports)
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

## Tracking revisions

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
