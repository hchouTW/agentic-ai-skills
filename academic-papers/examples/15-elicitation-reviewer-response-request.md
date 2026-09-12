---
role: Principal Research Scientist
skill: academic-papers
archetype: elicitation
user_request: "Can you respond to the reviewers?"
---

## 1. Raw Ambiguous Input

Message from a corresponding author, forwarded from the journal's editorial
system with three attached PDF reports:

> Can you respond to the reviewers? Reports are attached. Need this back to
> the editor soon.

No venue named, no round number, no indication of which comments the
authors agree with, and no statement of whether new experiments are even
possible before whatever "soon" means.

## 2. Missing Constraint Analysis

Per `references/submission-and-peer-review.md`, "respond to the reviewers"
is a fundamentally different task depending on venue type: a journal
referee response is point-by-point, multi-round, and can request a further
revision cycle; a conference rebuttal (NeurIPS/ICML/ICLR-style) is a single
strict-length-limited shot with no further revision round, often public on
OpenReview. Drafting the wrong shape either overshoots a hard character
limit or under-delivers the point-by-point rigor an editor expects.

Specifically missing:
- **Venue and round** - three reports with no stated venue could mean a
  journal's first-round major-revision decision (multi-round, generous
  length) or an ML conference's single rebuttal window (strict length, no
  further round) - the response format is different in each case.
- **Deadline** - "soon" gives no actual date, and conference rebuttals in
  particular have hard, non-extendable windows (per
  `submission-and-peer-review.md`'s "hard and non-negotiable" note on
  camera-ready-adjacent deadlines).
- **Author agreement per comment** - the three reports raise several
  distinct technical objections; without knowing which the authors actually
  agree with, the response would either concede points the authors dispute
  or ignore points they've already decided to accept.
- **Feasibility of new work** - one reviewer's comment appears to request an
  additional experiment; whether that is feasible before the deadline
  determines whether the response commits to new results or explains why it
  is out of scope for this round.

## 3. Socratic Clarification Round

1. What is the venue and review stage?
   a) A physics/general-science journal, first-round major-revision reports
   b) A physics/general-science journal, second-round (post-revision) reports
   c) An ML conference single-shot rebuttal window (e.g. NeurIPS/ICLR)
2. What is the actual deadline?
   a) A firm date has been given: 8 days from today
   b) Soft - "when convenient," no firm date from the editor
   c) A hard, non-extendable rebuttal window closing in 3 days
3. Of the three reports' major objections, which does the author team
   actually agree with?
   a) All three - each report's main objection will be addressed with a
      manuscript change
   b) Only Report 2's objection (a missing baseline comparison); Reports 1
      and 3 raise points the authors believe are already addressed in the
      current text
   c) None - the authors believe all three reports misread the method
      section
4. Is the new baseline experiment Report 2 requests feasible before the
   deadline?
   a) Yes - it reuses an existing pipeline and can be run and added within
      the deadline
   b) No - it would require new data collection not possible in this window
   c) Partially - a smaller-scale version is feasible, a full version is not

## 4. User Feedback Integration

The corresponding author's answers, sent back within the hour:

- Q1 -> **a) Journal, first-round major revision.** This is a physics
  journal with a standard multi-round referee process, not an ML-conference
  single-shot rebuttal.
- Q2 -> **a) A firm date: 8 days from today.** The editor's cover email
  (not forwarded initially) states the revision is due in 8 days.
- Q3 -> **b) Only Report 2's objection is agreed.** Reports 1 and 3's
  concerns are believed already addressed in the submitted manuscript, but
  the author team acknowledges the response must say so explicitly rather
  than silently disagree, per `submission-and-peer-review.md`'s point
  4 (non-defensive, explicit disagreement with reasoning, never silence).
- Q4 -> **a) Yes, feasible.** The requested baseline reuses the existing
  training pipeline with only the comparison model swapped in; it can be
  run and the result added to the revision within the 8-day window.

Each answer resolves one gap from section 2: Q1 fixes the response's shape
(point-by-point journal letter, multi-round, not a length-capped
conference rebuttal), Q2 supplies a real deadline to plan around, Q3 tells
the response which comments get a manuscript change versus an explicit,
reasoned disagreement, and Q4 confirms the one substantive new-work
commitment is achievable in time.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** A point-by-point referee response letter, structured in report
order (Report 1, then Report 2, then Report 3), each comment quoted or
closely paraphrased per `submission-and-peer-review.md`'s five-point
structure, with Report 2's baseline-comparison request answered by an
actual new experiment added to the revised manuscript's Results section.

**In scope:** All three reports' comments addressed point-by-point;
Report 2's new baseline experiment run and its result folded into the
revision; a short closing summary paragraph per point 5 of the reference
doc's guidance, since the revision includes a substantive new result.

**Out of scope:** Rewriting sections the reports did not comment on;
treating Reports 1 and 3's concerns as requiring new experiments, since the
author team has judged the current text already addresses them and the
response will say so explicitly rather than silently or defensively.

**Acceptance criteria:**
- Given each of the three reports, when the response letter is read
  alongside them, then every individual comment has either a stated change
  with a specific manuscript location ("clarified in Sec. IV, paragraph 2")
  or an explicit, reasoned disagreement - no comment is silently dropped.
- Given the new baseline experiment for Report 2, when it is added to the
  manuscript, then the response letter points to its exact table/figure
  location in the revision, not just a promise that it exists.
- Given the 8-day deadline, when the response and revision are assembled,
  then they are ready for the corresponding author to review with at least
  1 day of buffer before submission.

**Explicit non-goals:** This does not draft new experiments for Reports 1
or 3 - the author team has already decided those are addressed in the
current text, and re-opening them without an explicit new request would
exceed the smallest coherent slice for this revision round.
