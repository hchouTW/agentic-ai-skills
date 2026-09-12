---
role: Principal Research Scientist
skill: academic-papers
archetype: elicitation
user_request: "Can you write the related work section?"
---

## 1. Raw Ambiguous Input

Email from a postdoc co-author, sent the night before an internal draft
deadline:

> Can you write the related work section? I've attached the current draft
> (Introduction + Methods + Results, no Discussion yet) and our shared Zotero
> library.

No target venue, no length budget, no list of which papers must be engaged
in detail versus cited in passing, and no explicit statement of what this
paper claims is new.

## 2. Missing Constraint Analysis

Per `references/literature-review.md`, "related work" can mean three
different deliverables depending on venue and paper genre: a short
paragraph inside the Introduction (typical for a letter-format journal), a
standalone `## Related Work` section with a comparison table (typical for a
longer article or a methods paper), or a near-standalone mini-review
(typical when the field is small and referees expect full coverage). Writing
the wrong shape wastes the postdoc's review time and may need a full
rewrite once the actual venue and its norms are known.

Specifically missing:
- **Target venue and its related-work convention** - a 4-page PRL-style
  letter budgets ~3-5 sentences inside the Introduction; a 20-page PRD-style
  article budgets a standalone section with a comparison table.
- **Organizing principle** - the shared Zotero library spans at least two
  independent lines of prior work (an earlier measurement using a different
  method, and two more recent papers using the same method on a different
  dataset); chronological, thematic, and methodological organization would
  each tell a different story and only one matches what the paper argues.
- **The paper's own claimed novelty** - without knowing precisely what gap
  this paper claims to fill (per `literature-review.md`'s "Spotting the
  gap"), the related-work section cannot be written to set that gap up; it
  would just summarize prior work with no throughline.
- **Depth per paper** - which 2-3 papers need a full comparison-matrix
  treatment (method, dataset, result, limitation) versus a one-clause
  citation-stuffed mention, since not every paper in the shared library is
  equally central to the argument.

## 3. Socratic Clarification Round

1. What is the target venue and its approximate related-work length norm?
   a) PRL-style letter (~3-5 sentences inside the Introduction, no
      standalone section)
   b) PRD/JHEP-style article (~1 page standalone `## Related Work` section)
   c) A review article (multi-page, near-exhaustive coverage expected)
2. What is this paper's own claimed novelty, in one sentence?
   a) A precision improvement on a quantity others have already measured
      with larger uncertainty
   b) A new method that avoids an assumption the prior method(s) relied on
   c) The first measurement in a previously unprobed regime (no direct
      prior measurement exists)
3. Which organizing principle fits the shared Zotero library best?
   a) Chronological - the field's understanding evolved in a clear sequence
   b) Thematic - independent lines of work converge on the same question
   c) Methodological - our contribution is specifically a new method,
      compared against prior methods
4. Which papers need full comparison-matrix treatment (method, dataset,
   result, limitation) versus a brief citation-stuffed mention?
   a) Only the 2 papers using the same method on a different dataset
   b) All 5 papers in the shared library get equal, full treatment
   c) The 1 earlier measurement using a different method, plus the 2 same-
      method papers - the remaining 2 are tangential and get one clause

## 4. User Feedback Integration

The postdoc's answers, received the next morning:

- Q1 -> **b) PRD-style article.** The collaboration is targeting Physical
  Review D, so a standalone `## Related Work` section with a comparison
  table fits the venue's norm and word budget.
- Q2 -> **b) A new method that avoids an assumption.** The paper's core
  contribution is a background-estimation method that does not require the
  simulation-driven normalization the prior measurements assumed.
- Q3 -> **c) Methodological.** Since the claimed novelty is specifically
  "a new method," grouping prior work by *how* each measurement was made
  (rather than by date or sub-topic) directly sets up the comparison.
- Q4 -> **c) Full treatment for 3, brief mention for 2.** The earlier
  measurement (different method, same final state) and the two same-method,
  different-dataset papers get the comparison table; two loosely-related
  papers on an adjacent final state get one clause each in an opening
  sentence.

Each answer resolves one gap from section 2: Q1 fixes the shape (standalone
section, not an Introduction paragraph), Q2 supplies the exact novelty
claim the section must set up, Q3 picks the organizing principle that
matches that claim, and Q4 allocates depth so the section doesn't citation-
stuff five papers at equal weight.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** A standalone `## Related Work` section (~1 page, PRD-format)
organized methodologically: one paragraph on the prior simulation-driven
measurement, one paragraph synthesizing the two same-method/different-
dataset papers (per `literature-review.md`'s "synthesis, not a list"
guidance), a one-clause opening sentence covering the two adjacent-final-
state papers, and a closing gap statement naming the method-gap this paper
addresses (no prior measurement of this final state avoids the simulation-
driven normalization assumption).

**In scope:** A comparison table (paper, year, dataset, method, result with
uncertainty, limitation) for the 3 papers receiving full treatment, plus
prose synthesizing them per the methodological organizing principle.

**Out of scope:** A full mini-review of the adjacent final-state papers -
they get one clause each in the opening sentence, not their own paragraph
or table row, since they are not central to the method-gap argument.

**Acceptance criteria:**
- Given the comparison table, when a referee reads it, then the "method"
  column visibly differentiates the prior simulation-driven approach from
  this paper's data-driven approach - the differentiation must be legible
  from the table alone, not only from surrounding prose.
- Given the closing paragraph, when a reader reaches the end of Related
  Work, then the stated gap ("no prior measurement of this final state
  avoids the simulation-driven normalization assumption") is stated as a
  method gap per `literature-review.md`'s gap-pattern taxonomy, not as a
  vague "more work is needed" close.

**Explicit non-goals:** This does not attempt exhaustive coverage of every
paper in the shared Zotero library - the two adjacent-final-state papers
are deliberately compressed to one clause each, and no fourth "future
outlook" paragraph is added beyond the venue's ~1-page norm.
