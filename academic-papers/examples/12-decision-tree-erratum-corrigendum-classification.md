---
role: Manuscript Editor
skill: academic-papers
archetype: decision-tree
scenario: classifying a post-publication error report into the correct correction mechanism before drafting anything
---

## Triage Matrix

Formalizes `references/erratum-and-corrigendum-drafting.md`'s classification
step into an explicit trigger -> mechanism mapping, applied before any
correction text is drafted:

| Trigger | Resolution Strategy |
|---|---|
| Error was introduced during production (typesetting, a figure/table transposed or corrupted after acceptance), not present in the accepted manuscript | Classify as **erratum**; verify against the accepted-manuscript version before assuming this category |
| Error was present in the accepted manuscript itself - a calculation mistake, mislabeled dataset, or incorrect statistical test made by the authors | Classify as **corrigendum**; do not soften the language to make it read like a production error |
| New information supplements (does not correct) the published result, and the venue treats this as its own category | Classify as **addendum**; confirm with the venue's specific guidelines whether it is handled like a corrigendum or as distinct |
| Classification is genuinely ambiguous even after checking the accepted manuscript and the venue's guidelines | Ask the user or the journal's editor rather than defaulting to the less-serious-sounding label |
| The reported "error" turns out, on inspection, not to be an error at all (a convention difference, a reviewer misreading a correct statement) | Do not draft any correction notice; respond to the reporter explaining why, the same way a disputed referee comment is answered - factually, not defensively |

## Selected Branch

Report received: "Table 3's quoted branching fraction is 12% higher than it
should be; I think the acceptance correction was double-counted." Checking
the accepted manuscript's own file (not just the published PDF) shows the
double-counted acceptance correction is present in the accepted version
itself, not introduced during typesetting - matching the second row:
**corrigendum**, not erratum.

## End-to-End Execution Script

1. Confirm the error's actual impact per point 3 of the reference, using
   `revision-impact-tracking.md`'s dependency-tracing approach: the correct
   denominator already includes the acceptance correction once, giving
   `4.82 / 39.6 = 0.1217`; the published pipeline erroneously applied the
   0.893 acceptance factor a second time, shrinking the denominator to
   `39.6 * 0.893 = 35.36` and inflating the published value to
   `4.82 / 35.36 = 0.1363` - a genuine change to the headline number, not a
   presentational detail, so the notice must state the corrected conclusion,
   not just that an error occurred.
2. Draft the corrigendum stating the error and correction side by side, per
   point 2: "The acceptance correction factor of 0.893 was applied twice in
   computing the branching fraction quoted in Table 3 and the abstract. The
   corrected branching fraction is 0.1217 ± 0.0031 (statistical), compared to
   the originally published 0.1363 ± 0.0035."
3. Check whether the result was cited by other papers before this correction
   (per point 5): one citing paper is found; this is disclosed to the user
   as a fact about the correction's downstream reach, not something this
   notice itself attempts to fix in the citing paper.
4. Submit the corrigendum through the same production system as the original
   paper, per point 4, with co-author sign-off obtained on the correction
   text specifically (separate from the original paper's sign-off), and with
   the bidirectional DOI link confirmed once posted.

## Fallback Safeguards

If it later turned out the double-counting was introduced by the typesetter
during production (e.g. a macro substitution error not present in the
authors' submitted accepted manuscript file), re-triage immediately to the
first row instead: this would be an **erratum**, not a corrigendum, and using
the wrong label would misrepresent whose process failed. If, instead, further
checking showed the "12% high" claim was itself a misreading of the table
(the reporter compared the wrong column), re-triage to the fifth row: no
correction notice is drafted at all, and the reporter receives a factual
explanation of why the reported figure is correct as published.
