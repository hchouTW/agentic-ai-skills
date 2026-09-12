---
role: Principal Platform / Developer-Experience Engineer
skill: skill-router
archetype: gated-pipeline
high_stakes_task: resolving a discovered routing ambiguity between academic-papers and hep-analysis for figure/plot-interpretation requests
---

## Phase 1: Input Extraction & Gap Formulation

Three real requests were misrouted in the past two weeks, all variants of
"can you explain this plot from my paper?":
1. "What does Figure 3 in my draft show?" - routed to `hep-analysis`
   (matched "plotting"), but the user only wanted the caption's claim
   restated for a lit-review summary, not a re-derivation.
2. "This histogram's uncertainty band looks too narrow - is that right?" -
   routed to `academic-papers` (matched "figures... for publication"), but
   the user actually wanted the uncertainty recomputed from the underlying
   counts, not prose about the figure.
3. "Read the attached plot and tell me if the quoted significance is
   overstated" - correctly triggered both skills via rule 3, but only after
   a user complaint that the first response only did half the job.

Extracted the gap: `academic-papers`'s bullet says "designing figures/tables
for publication" and `hep-analysis`'s says "HEP plotting" - both genuinely
overlap on "figure/plot," and neither bullet currently distinguishes
*restating what a figure already claims* from *recomputing what should be in
it*.

**Gate:** proceed to Phase 2 only once at least two concrete misrouted
requests are documented verbatim (not paraphrased), as above, so the fix is
grounded in real failures rather than a hypothetical concern.

## Phase 2: Draft Synthesis

Drafted symmetric additions to both bullets, matching the existing
carve-out convention (`hep-analysis`'s own "Not for unrelated uses of
'root'..." clause is the precedent cited):

```
academic-papers addition: "...designing figures/tables for publication...
  Figure/plot interpretation here means restating or critiquing what a
  paper's own published figure already claims - not re-deriving the
  underlying physics/statistics from raw data or counts, which is
  `hep-analysis`'s or `deep-learning`'s territory."

hep-analysis addition: "...HEP plotting... Not for restating or critiquing
  what a paper's own already-published figure claims with no
  recomputation requested - that reading/writing layer is
  `academic-papers`'s territory; see its carve-out."
```

**Gate:** proceed to Phase 3 only once both additions are checked for
symmetry (each names and points to the other) and re-grepped against all
four bullets for any new collision the added wording itself introduces:
`grep -n -i "recompute" SKILL.md` returns no hits (genuinely new
vocabulary), and `grep -n -i "underlying" SKILL.md` returns exactly one hit -
line 23, `academic-papers`'s own pre-existing carve-out ("Not for the
underlying statistical/ML/physics analysis itself"). That single hit is the
same rule reusing its own established word, not a collision with a
different rule, so it does not block this gate.

## Phase 3: Red-Team Review & Final Artifact Packaging

Stress-tested the assumption that "the new wording fully disambiguates every
figure/plot request." Applied it to real request 3 above ("read the attached
plot and tell me if the quoted significance is overstated") and found the
assumption **false**: this request asks to both read what the figure claims
*and* recompute the significance from the counts shown in it - both halves
of the new carve-out language apply at once, to the same request. The fix
was never meant to eliminate genuine two-layer requests, only to stop a
single-layer request from being sent to both skills or the wrong one; trying
to force this case into a single bullet would misrepresent it. Resolution:
documented explicitly, next to both new carve-outs, that a request naming
both "what does the figure show" and "is the underlying number right"
in the same ask should still trigger Behavior rule 3 (primary/secondary),
exactly as example `02-multi-skill-primary-secondary-routing.md` already
demonstrates - the new wording narrows the single-skill cases, it does not
and should not narrow the genuine two-skill case.

**Gate:** merge only once both bullets' additions are symmetric and
collision-free (confirmed above) and a note is added stating that a combined
"read + recompute" request remains a rule-3 case, not a new error condition -
this is the actual merge criterion, not an intermediate one.
