---
role: Lead Platform / Developer-Experience Engineer
skill: skill-router
archetype: decision-tree
scenario: a request with several simultaneous surface keyword matches across multiple rules (LaTeX, fix, refactor, update) that, on inspection, is really about a personal resume and matches no rule's actual intent
---

## Triage Matrix

Extends example `03`'s single-carve-out lesson (a keyword can false-positive
even when the rule has no explicit carve-out for that exact case) to the
harder case where *several* rules' surface keywords all hit at once, and
none of the underlying intents actually match:

| Trigger | Resolution Strategy |
|---|---|
| Request mentions "LaTeX"/"manuscript"/"paper" in the context of an actual scientific paper, preprint, or journal submission | `academic-papers` applies - this is its actual territory |
| Request mentions "LaTeX" only in the context of a non-scientific document (a resume, CV, or personal website) with no manuscript/journal/paper context anywhere | `academic-papers` does not apply despite the keyword - its rule is about scientific-paper writing, not the LaTeX typesetting system in general |
| Request uses "fix"/"refactor"/"update" applied to a real software system with users, tests, or a deployment | `agile-development` applies - this is its actual territory |
| Request uses "fix"/"refactor"/"update" applied to prose or document content, not executable software | `agile-development` does not apply - those verbs describe an edit action in English generally, they are not themselves evidence of a software change |
| Several of the above surface matches are present in the same request, but every one of them resolves to "does not apply" on inspection | No rule applies; proceed per Behavior rule 4 and help directly with the actual, non-domain-skill task |

## Selected Branch

A request arrives: "I need to update my LaTeX resume, fix the formatting,
and refactor the code-samples section to remove some old projects." This
contains "LaTeX" (surface match on `academic-papers`), and "update," "fix,"
and "refactor" (surface matches on `agile-development`) - four keyword hits
across two different rules in one sentence. Checking each against the actual
subject matter: the document is a personal resume, not a scientific
manuscript (rules out row 1, lands on row 2); "fix the formatting" and
"refactor the code-samples section" both refer to editing resume content,
not to changing a running software system (rules out row 3, lands on row
4). Selected branch: row 5 - every surface match resolves to "does not
apply," so no rule is triggered.

## End-to-End Execution Script

> No routing rule applies. This is a LaTeX-formatting and content-editing
> request for a personal resume, not a scientific manuscript or a software
> change - proceeding directly per Behavior rule 4.
>
> [Help is given directly: tightening the LaTeX `\begin{itemize}` spacing in
> the experience section, and trimming the "Projects" section down to the
> three most recent entries as requested - ordinary document editing, with
> no mention of `skill-router`, `academic-papers`, or `agile-development`
> anywhere in the response.]

The check that mattered here was not "does any keyword match" (four did) but
"does the request's actual subject matter match what the rule is *for*" -
running that check once per surface hit, rather than stopping at the first
or most numerous match, is what correctly produced zero invocations instead
of an incorrect one or two.

## Fallback Safeguards

If it turns out the "resume" is actually an academic CV being prepared for a
grant or fellowship application with an attached research statement (a case
`academic-papers` does cover), the trigger was misclassified: re-triage
against row 1 rather than row 2, since the document type looked similar on
the surface but the context (an attached research statement, a funding
application) changes which row actually applies. If instead the
"code-samples section" turns out to reference a real, currently-deployed
personal project repository that the user also wants actively refactored
(not just trimmed from a list), that specific sub-request re-triages against
row 3 as a genuine `agile-development` case, handled separately from the
resume-editing request rather than folded into the same "no rule applies"
answer.
