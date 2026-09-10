---
role: Principal Experimental Particle Physicist
skill: hep-analysis
archetype: gated-pipeline
high_stakes_task: performing an unfolded differential cross-section measurement, from response-matrix construction through a regularization choice to a published result
---

## Phase 1: Input Extraction & Gap Formulation

Extracted the measurement's inputs: a reconstructed-level spectrum, a
response matrix `R` built from the nominal MC sample per
`references/10-measurements-unfolding.md`'s "Response matrices" section
(`y_reco = R*x_truth + b`), and a proposed iterative-Bayesian unfolding.
Reviewing against that section's own caution - "Building the response and
testing closure on the same events may be optimistic; split samples or use
valid resampling" - found exactly that gap: the response matrix and the
closure test both used the full nominal MC sample with no train/test split.
A second gap: no predefined stopping-rule criterion existed yet for the
number of Bayesian iterations; the current draft chose 4 iterations because
"the spectrum looked smooth," which the "Unfolding methods" section
explicitly calls out as insufficient ("Use predefined criteria and
independent truth variations, not visual smoothness alone").

**Gate:** proceed to Phase 2 only once (a) the MC sample is split into an
independent response-building half and a closure-testing half, and (b) a
predefined, written stopping-rule criterion for the regularization strength
is defined before looking at the closure result.

## Phase 2: Draft Synthesis

Rebuilt the response matrix on one independent MC half and reserved the
other half for closure testing, closing Phase 1's first gap. Defined the
stopping-rule criterion per "Unfolding methods": select the smallest number
of iterations for which an alternative-truth-shape injection test (a
different generator's steeper falling spectrum, injected as pseudo-data and
unfolded) reproduces the injected truth within a pre-declared 5% bias
tolerance in every bin - a predefined, quantitative criterion rather than
"looked smooth."

Ran the validation battery that section requires: nominal closure on the
held-out half, the alternative-truth-shape injection above, and a check of
response-matrix conditioning and identifiable truth bins. Three iterations
satisfied the 5% bias tolerance in all bins except the highest-pt bin, which
required five iterations to reach tolerance there - so five iterations were
adopted globally, accepting slightly higher variance in the well-measured
low-pt bins to meet the predefined criterion everywhere.

**Gate:** proceed to Phase 3 only once the chosen regularization strength (5
iterations) passes the alternative-truth-shape injection test within the
predeclared 5% tolerance in every bin, using the response built on the
independent MC half.

## Phase 3: Red-Team Review & Final Artifact Packaging

The assumption most worth stress-testing was that the response matrix,
having passed closure and the alternative-truth-shape injection, is adequate
regardless of which generator's truth-level spectrum shape was used to
*build* it (as opposed to the shape used only to *test* it in Phase 2).
Rebuilding the response matrix itself with a different generator's harder
truth spectrum and repeating the closure test found this assumption **false**
in the highest-pt bin only: the purity and stability there (per "Response
matrices"' own diagnostic pair) both degrade by more than the quoted
statistical uncertainty when the truth-model input to the response changes,
meaning that bin's unfolded result depends on a generator choice the analysis
had treated as fixed, not just a smoothness input.

As a result, the highest-pt bin was excluded from the reported fiducial
differential cross section, with a note in the result explaining the
exclusion and the generator-dependence test that motivated it, rather than
either publishing it with an unquantified extra risk or silently assigning it
an ad hoc extra uncertainty band with no closure behind it.

**Gate:** publish only once the response's truth-model dependence has been
checked bin-by-bin (not just for the previously-flagged highest-pt bin, to
confirm no other bin has the same issue), any excluded bin is explicitly
documented with the test that motivated the exclusion, and the Phase 2
closure/injection tests are re-confirmed on the final response matrix used
for the published result - the actual publication criterion, not an
intermediate one.
