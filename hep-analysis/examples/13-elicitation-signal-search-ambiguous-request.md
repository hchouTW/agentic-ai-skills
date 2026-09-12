---
role: Principal Experimental Particle Physicist
skill: hep-analysis
archetype: elicitation
user_request: Can you check if there's a signal in this dataset?
---

## 1. Raw Ambiguous Input

Verbatim message from a collaborator, attached to a single ROOT file path on
the group's storage element:

> Can you check if there's a signal in this dataset?

No further text, no analysis note, no run range, and no indication of what
"signal" refers to.

## 2. Missing Constraint Analysis

Per `references/01-analysis-design.md`'s "Establish the analysis contract"
section, a measurement cannot be specified without the collision system,
energy, era, data format, target process, fiducial phase space, observables,
and POI - none of which are present here. Concretely, four constraints are
missing, each one blocking a specific downstream step:

1. **Channel / final state.** The dataset could contain any final state
   (dielectron, dimuon, dijet, multi-jet + MET, ...). Without it, no object
   definitions, triggers, or selection can be written, and per the contract's
   "Event and object definitions" section, correcting before ordering vs.
   ordering before correcting can already change results even once a channel
   is fixed - starting without one is worse than an ambiguous choice, it is
   no choice.

2. **Signal region / hypothesis definition.** "A signal" could mean a bump
   search at an unspecified mass point, a shape-based excess over a smooth
   background, or a signal-strength fit to a predefined signal model. Per
   `references/01-analysis-design.md`'s "Regions and categories" section, a
   signal region must be defined and recorded before any region-dependent
   quantity (yield, significance) means anything, and per the same section's
   blinding guidance, "Do not use the actual SR count to optimize the
   supposedly blinded model" - so the SR boundaries must be fixed *before*
   looking, not derived by scanning this file for whatever bump appears
   biggest.

3. **Background model.** `references/09-statistical-tools.md`'s "Model
   mapping" section requires a workspace to specify channels, observations,
   measurements, and named modifiers (`normfactor`, `normsys`, `histosys`,
   `shapesys`) before a fit means anything - "reusing names affects shared
   parameters and must match the correlation inventory." There is currently
   no background model, no control region, and no statement of which
   processes are irreducible vs. data-driven.

4. **Significance convention and threshold.** Per
   `references/08-inference.md`'s "Define the question" section, a p-value
   requires a stated null/alternative, one- or two-sided convention, and
   confidence level before it can be quoted as a sigma-level at all; and per
   its "Toys, coverage, and trials" section, "Searching across masses,
   channels, or cuts creates a look-elsewhere effect... a single-point local
   p-value is not global." Without knowing whether this is a single fixed
   hypothesis test or a scan, it is impossible to know whether a local
   p-value is even the right number to report, let alone what threshold
   ("evidence" at 3 sigma local, "discovery" at 5 sigma global) applies.

## 3. Socratic Clarification Round

1. Which final state and dataset era does this file correspond to?
   a) Dielectron/dimuon (dilepton resonance search)
   b) Dijet (dijet resonance search)
   c) Single lepton + missing transverse momentum
   d) I'm not sure - it's an unlabeled skim someone handed me
2. Is there a predefined signal region and signal hypothesis, or is this an open-ended scan over an unspecified mass range?
   a) Fixed signal region and a single predefined mass point
   b) A bump-hunt scan over a stated mass range with a stated step size
   c) No signal region yet - derive one from this file's own distribution
   d) Not sure; treat it as exploratory only, no region defined yet
3. What background model should be used, and is a control region available?
   a) A smooth analytic background fit to the sideband (function form to be specified)
   b) A simulated background estimate normalized in a dedicated control region
   c) A data-driven ABCD or similar estimate from an orthogonal region
   d) No background model exists yet - this is the first pass at the file
4. If an excess is found, what significance convention and threshold should be reported?
   a) Local significance only, no look-elsewhere correction (single fixed hypothesis)
   b) Local and global significance, with a stated trials factor for the scanned range
   c) CLs-based exclusion limit rather than a discovery significance
   d) Report only the raw event counts and defer any significance claim

## 4. User Feedback Integration

The collaborator's answers, received after the round above:

> 1b, 2b, 3b, 4b. It's the 2018 dijet skim, we're bump-hunting between 1.5
> and 6 TeV in 100 GeV steps, background is a smoothly-falling QCD fit
> validated in a low-mass control region, and yes we need the trials factor
> since we're scanning - use the same convention as the last dijet note.

Each answer resolves one open constraint from Section 2:

- Answer to Q1 (dijet, 2018) fixes the missing channel/final state - object
  definitions, triggers, and jet selection can now be pinned per
  `references/01-analysis-design.md`'s object-definition guidance.
- Answer to Q2 (bump-hunt scan, 1.5-6 TeV, 100 GeV steps) fixes the missing
  signal region definition - the scan grid is fixed *before* looking, per
  the blinding guidance in Section 2, rather than chosen after inspecting
  the spectrum.
- Answer to Q3 (smoothly-falling QCD fit, validated in a low-mass control
  region) fixes the missing background model, giving a concrete function
  family and a validation region rather than an unspecified background.
- Answer to Q4 (local and global, with a trials factor) fixes the missing
  significance convention, directly resolving the look-elsewhere-effect gap
  identified against `references/08-inference.md`.

## 5. Final Mutually-Agreed Specification Document

**Analysis contract** (per `references/01-analysis-design.md`):

- Collision system / era: pp collisions, 2018 dataset, dijet skim.
- Target process: generic dijet resonance (model-independent bump hunt).
- Fiducial phase space: two leading anti-kt R=0.4 jets, |eta| < 2.5 each,
  |delta-eta(jet1,jet2)| < 1.3 (angular cut to suppress QCD t-channel
  background while retaining s-channel resonance acceptance).
- Observable / POI: dijet invariant mass m_jj; POI is the signal cross
  section times branching ratio times acceptance at each scanned mass point.
- Signal region: a bump-hunt scan over m_jj from 1.5 TeV to 6.0 TeV in fixed
  100 GeV steps, grid fixed prior to inspecting the observed spectrum.

**Background model** (per `references/09-statistical-tools.md`'s "Model
mapping"): a single-channel workspace with one smoothly-falling QCD
background parameterization (function form and parameters fixed from the fit
to data outside the scan window plus the low-mass control region below 1.5
TeV), a `normfactor` for the overall background rate, and no signal
component in the background-only fit.

**Statistical procedure** (per `references/08-inference.md`): a profile
likelihood ratio discovery test (q0) at each scanned mass point, reporting
both the local significance at the most significant point and the global
significance after correcting for the look-elsewhere effect across the
1.5-6 TeV / 100 GeV grid, using the trials-factor convention from the prior
dijet analysis note as the reference procedure. Reporting threshold:
"evidence" requires local significance >= 3 sigma; "discovery" requires
global significance >= 5 sigma. No exclusion limit is computed under this
specification since Q4 selected significance reporting over CLs.

**Blinding status**: the scan window (1.5-6 TeV) is unblinded per the
collaborator's request; the low-mass control region used for background
validation was never blinded since it carries no signal sensitivity.
