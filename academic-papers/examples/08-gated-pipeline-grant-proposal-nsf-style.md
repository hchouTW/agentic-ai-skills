---
role: Principal Research Scientist
skill: academic-papers
archetype: gated-pipeline
high_stakes_task: drafting an NSF-style research proposal under a page-limited Specific Aims format for a specific funding call
---

## Phase 1: Input Extraction & Gap Formulation

Per `references/grant-and-fellowship-proposal-writing.md`'s point 1, the
call's actual current requirements were retrieved rather than assumed from a
prior cycle: a 1-page Specific Aims, a 15-page Project Description, a
required Broader Impacts subsection, and this program's specific review
criteria (Intellectual Merit and Broader Impacts, each scored separately).

Gaps found when extracting the draft's current state against those
requirements:
- The draft's preliminary results section runs three pages, crowding out
  space for the actually-proposed work - the reference's point 3 warns
  against exactly this.
- No budget-justification figures have been supplied by the institution's
  grants office yet.
- The Broader Impacts subsection is a placeholder paragraph copied from a
  previous proposal to a different program.

**Gate:** proceed to Phase 2 only once the preliminary-results section is
scoped down to a stated page target, the grants office has supplied actual
budget figures (not estimated), and the Broader Impacts subsection is
flagged as needing a full rewrite rather than a light edit.

## Phase 2: Draft Synthesis

Drafted against `references/grant-and-fellowship-proposal-writing.md` point
by point: the Specific Aims page now leads with the problem and gap before
the proposed approach (point 2), is readable standalone, and trims
preliminary results to half a page of the Project Description, clearly
separated from the proposed work with its own subheading (point 3). Budget
justification uses the figures supplied by the institution's grants office
($412,000 total direct costs over three years, 58% negotiated indirect cost
rate) rather than an estimated number, per point 5's explicit prohibition on
inventing such figures. The Broader Impacts subsection was rewritten to
describe this proposal's specific plans - a summer research-experience slot
for two undergraduates from the institution's existing McNair Scholars
partnership, and release of the proposed software tool under an open license
- rather than the generic boilerplate it previously carried, per point 4.

**Gate:** proceed to Phase 3 only once every section matches the call's
actual required outline and page limits, and no budget or effort figure in
the draft is unsourced.

## Phase 3: Red-Team Review & Final Artifact Packaging

The assumption most worth stress-testing was: "the Broader Impacts rewrite
is now specific enough that a panel reviewer won't read it as generic." A
red-team read against `references/grant-and-fellowship-proposal-writing.md`'s
point 4 found this assumption **partly false**: the software-release plan was
specific, but the undergraduate research-experience plan still read as
generic ("students will gain valuable research experience") without stating
what they would actually do. Revised to name the specific task each student
would work on (one on the data-pipeline component, one on the analysis
validation suite) and the specific skill each would gain - closing the gap
the stress test found.

**Gate:** submit only once every Broader Impacts claim names a specific,
checkable activity rather than a general benefit, the budget figures are
confirmed final by the grants office (not a working draft number), and the
Specific Aims page has been read standalone by someone not involved in
drafting it, per the reference's note that some panelists read only that
page closely - this is the actual submission criterion, not an intermediate
one.
