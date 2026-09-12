---
role: Principal Research Scientist
skill: academic-papers
archetype: elicitation
user_request: Can you make my paper better before I submit it?
---

## 1. Raw Ambiguous Input

The user attaches a LaTeX manuscript directory (`manuscript/main.tex`,
`manuscript/sections/*.tex`, `manuscript/refs.bib`, three figure files) titled
*"Measurement of the ttH Production Cross-Section in the Diphoton Channel"*
and writes only:

> Can you make my paper better before I submit it?

No target journal, no deadline, no statement of whether this is a first
submission or a resubmission, and no indication of which co-authors have
already reviewed the draft or which sections are still open for editing.

## 2. Missing Constraint Analysis

"Make it better" cannot be executed safely as a single, well-defined task —
per `references/paper-structure.md` and `references/submission-and-peer-review.md`,
at least four load-bearing constraints are missing, each of which would send
the edit in a materially different direction:

- **Target venue is unstated.** `paper-structure.md`'s title/abstract/length
  conventions and `submission-and-peer-review.md`'s pre-submission checklist
  both key off the venue: a Physical Review Letters submission has a strict
  ~4-page limit and a compressed structure (no separate Systematics section
  is typical), while a Physical Review D or JHEP submission has no such page
  cap and expects the full Detector/Analysis/Systematics/Results backbone.
  Trimming the Introduction to satisfy a PRL page count would be the wrong
  edit for a PRD submission, and vice versa.
- **Deadline is unstated.** Whether there is a hard external deadline (a
  conference proceedings cutoff, a collaboration-internal review calendar)
  determines how much can be attempted — a full pre-submission checklist pass
  plus a co-author circulation round takes materially longer than a same-day
  polish.
- **Resubmission status is unstated.** `submission-and-peer-review.md`'s
  "Responding to referee reports" workflow (quote each comment, state what
  changed, point to the exact revised location) only applies if this is a
  resubmission responding to a prior referee report or a prior rejection at
  another venue. For a fresh submission, "make it better" means a general
  argument-and-clarity pass per `paper-structure.md`, not a point-by-point
  response to comments that don't exist yet. Conflating the two would produce
  a response-letter-shaped edit with no report to respond to.
- **Co-author review scope is unstated.** The pre-submission checklist
  requires that "author list, affiliations, and acknowledgments match the
  current collaboration-approved list" and warns against hand-editing them
  "without the publications committee's sign-off." Whether the user is the
  sole author empowered to approve wording changes, or one of several
  co-authors on a collaboration paper where substantive edits need
  circulation first, determines whether edits can be finalized directly or
  must be delivered as a marked-up draft for review.

## 3. Socratic Clarification Round

1. What is the target venue for this submission, since the section structure
   and length limit differ substantially between them?
   a) Physical Review Letters (PRL) — ~4-page limit, compressed structure
   b) Physical Review D (PRD) — full-length article, no strict page cap
   c) A JHEP/JCAP-style journal — different LaTeX class and reference style
   d) Not yet decided — I'd like help choosing based on the result's scope

2. Is this a fresh submission, or are you resubmitting after prior reviews or
   a prior rejection?
   a) Fresh submission — no referee feedback exists yet
   b) Resubmission responding to a referee report from this same venue
   c) Resubmission to a different venue after rejection elsewhere
   d) A conference-proceedings version of an already-published result

3. Is there a hard deadline driving this pass?
   a) Yes — within about a week (e.g., a conference or proceedings deadline)
   b) Yes — within about a month
   c) No hard deadline; thoroughness matters more than speed
   d) The deadline is set by a collaboration-internal review calendar I don't
      control directly

4. Which parts of the manuscript are actually in scope for edits, and who
   needs to sign off before a change is final?
   a) The full manuscript, and I can approve wording changes directly
   b) The full manuscript, but co-authors must review any substantive change
      before it's final
   c) Only specific sections (e.g., Results and Systematics) — other sections
      are owned by other authors and are frozen for now
   d) This is a large-collaboration paper; the author list and acknowledgments
      are collaboration-approved and must not be hand-edited

## 4. User Feedback Integration

The user answers:

1. **(b)** — Physical Review D. "It's a full cross-section measurement with a
   dedicated systematics section; PRL's length limit would force us to cut
   material we want to keep."
2. **(a)** — Fresh submission. "No referee has seen this yet — this is the
   first time it's going out."
3. **(b)** — About a month. "We're aiming for a specific collaboration
   internal-review meeting, but there's some slack."
4. **(b)** — Full manuscript in scope, but co-authors must review. "I can
   flag suggested changes, but nothing goes in as final until the other three
   co-authors sign off, especially anything touching the Systematics section
   since that's not my analysis."

Resolution of each missing constraint from Section 2:
- Venue → PRD, so the full backbone (Title, Abstract, Introduction,
  Detector/Dataset, Analysis, Systematics, Results, Summary) applies with no
  page-count pressure, and the pre-submission checklist's full scope applies
  rather than a compressed-format subset.
- Deadline → about one month, which is enough time for a full checklist pass
  plus a co-author review round, but not enough to justify open-ended
  restructuring beyond what the checklist and argument review actually find.
- Resubmission status → fresh submission, so the edit is a general
  clarity/consistency/completeness pass against `paper-structure.md` and the
  pre-submission checklist, not a referee-response letter.
- Co-author scope → full manuscript in scope for review, but changes are
  delivered as marked-up suggestions, not finalized in place — and the
  Systematics section specifically is flagged as needing its owning
  co-author's sign-off before any suggested wording is treated as accepted.

## 5. Final Mutually-Agreed Specification Document

**Objective.** Produce a marked-up revision of the ttH→γγ cross-section
manuscript, in preparation for a fresh submission to Physical Review D within
approximately one month, ready for co-author circulation rather than final
submission.

**Scope of work:**
1. Run `scripts/check_manuscript.py` against the full manuscript directory
   and resolve every flagged issue (unresolved `\cite{}`, unused `.bib`
   entries, unresolved or duplicate `\label{}`/`\ref{}`, leftover
   drafting-stage placeholder text) before any prose editing begins.
2. Verify, per the pre-submission checklist: every number quoted in the
   Abstract matches the corresponding number in Results; statistical and
   systematic uncertainties are distinguished everywhere both apply (format:
   `value ± stat ± syst`, with units); figures and tables are numbered in
   first-reference order; the manuscript compiles cleanly from a clean
   checkout.
3. Apply `paper-structure.md`'s section-by-section guidance for a full PRD
   article: confirm the Title states the result rather than the method;
   confirm the Abstract's four-part structure (context, what was done, the
   result with uncertainty, comparison to the Standard Model prediction);
   confirm the Introduction states explicitly what this measurement adds
   over prior ttH cross-section measurements; confirm Results leads with the
   headline cross-section value before plot discussion and states the pull
   relative to the Standard Model prediction in standard deviations; confirm
   the Summary introduces no new numbers.
4. Treat the Systematics section as edit-suggestions-only: mark proposed
   wording changes with `\textcolor{}` tracked-change markup rather than
   applying them directly, since that section requires its owning
   co-author's sign-off per the agreed review scope.
5. Deliver the marked-up draft plus a short change log (per
   `submission-and-peer-review.md`'s "Tracking revisions") listing what
   changed and why, for circulation to the other three co-authors — not a
   finalized, resubmission-ready file. Do not touch the author list,
   affiliations, or acknowledgments block.
6. Explicitly out of scope for this pass: choosing a different target venue,
   restructuring the analysis itself, or resolving any disagreement among
   co-authors about the Systematics section's content (only the presentation
   of already-agreed content is in scope).
