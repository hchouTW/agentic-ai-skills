# Behavioral test prompts for hep-analysis

Purpose: realistic user prompts to run on a fresh model with and without the skill, and grade
the answer against the expected behaviors. Results are logged in `VALIDATION.md`.
Balance (per the user, 2026-09-24): collider, space-based/AMS, and IACT/neutrino/air-shower work
weigh equally. Each prompt lists what a PASS must contain (**E**) and what counts as a
FAIL signal (**F**). The invariant names refer to `SKILL.md` "Analysis invariants".

Grading: PASS = every E item present and no F item. PARTIAL = most E items, no F.
FAIL = an F item, or most E items missing.

## Collider

### P01 RDataFrame cutflow with signed weights
> I have an NLO ttbar sample (MG5_aMC@NLO, about 20% negative weights) in NanoAOD. I'm writing an
> RDataFrame cutflow and normalizing to 138 fb^-1 with xsec 833.9 pb. Right now I scale by
> lumi*xsec/N where N is the number of events in the file after my skim. Is that right? Show the fix.

- E1: the normalization denominator is the sum of generator weights (signed) over the **full
  produced sample before any skim**, not the entry count, and not the post-skim count.
- E2: negative weights are kept (not abs'd or dropped); cutflow reports weighted sums per cut
  (sumw, and ideally sumw2), and not just raw counts.
- E3: gives RDataFrame code (e.g. `Sum("genWeight")` from the `Runs` tree or an unskimmed pass).
- F: using abs(weights); keeping N = entries; dropping negative-weight events.
- Reference: 03-weights-normalization.md.

### P02 uproot jagged selection
> Using uproot + awkward, select events with at least two jets with pt > 30 GeV and |eta| < 2.5,
> then histogram the invariant mass of the two leading selected jets. My jets are Jet_pt, Jet_eta,
> Jet_phi, Jet_mass (jagged). Weights in `genWeight`.

- E1: applies the jet mask **before** counting/choosing leading jets (index after masking), keeps
  jet ordering by pt, and handles events with < 2 jets without IndexError (e.g. `ak.num` filter).
- E2: computes mass with a 4-vector method (vector library or explicit formula) and weights the
  histogram, storing sum w^2 (or states that errors need sumw2).
- F: takes `Jet_pt[:,0]`/`[:,1]` from the unmasked array; ignores weights.
- Reference: 02/17.

### P03 JES systematic as a shape variation
> For the JES uncertainty, I plan to take my final m_jj histogram and multiply each bin by
> (1 +/- 0.02) to get the Up/Down templates. Fine?

- E1: No: JES is a kinematic variation; must shift jet pT (and propagate to MET, jet ordering,
  selection, category migration), then rerun the selection to build the Up/Down templates.
- E2: mentions that a flat bin scaling is only a normalization effect, and gives a way to
  check the result (compare yields per cut, nominal vs varied).
- F: agrees with bin scaling.
- Reference: 06-systematics.md, 18.

### P04 ABCD closure failure
> My ABCD estimate for QCD in region A gives 120 +/- 15, but in the MC closure test region A is
> 180. The variables are MET and lepton isolation. My advisor says just add a 50% systematic and
> move on. Thoughts?

- E1: identifies that the non-closure signals **correlation between the two ABCD variables**
  (MET and isolation both correlate with heavy-flavour/real-MET); investigate correlation and
  signal contamination in B/C/D before accepting an inflated systematic.
- E2: proposes a validation region/closure check in data (for example, inverted cuts) and a
  correction factor with its uncertainty rather than a hand-picked inflation. A systematic
  derived from the closure (e.g. the measured discrepancy) with justification is acceptable.
- F: simply endorses "add 50% and move on" with no investigation.
- Reference: 05-backgrounds.md.

### P05 Unblinding request on a masked region
> We are still blinded in the signal region (m > 1 TeV). Can you just make me a quick data/MC
> ratio plot of the full m spectrum so I can check the fit looks OK before the unblinding
> approval meeting next week?

- E1: refuses/declines to show data in the masked region; offers the plot with SR data masked,
  or MC-only / Asimov / control-region checks.
- F: produces code that plots SR data.
- Reference: 01-analysis-design.md (blinding invariant).

### P06 pyhf model with overlapping regions
> In pyhf I have a signal region SR (njet >= 4) and a control region CR (njet >= 3, same
> b-tag selection) that I use to constrain ttbar normalization. I fit both simultaneously. Is
> there a problem?

- E1: the regions **overlap** (njet >= 4 events are in both), so the same events enter the
  likelihood twice; make them orthogonal (CR njet == 3) or model jointly.
- F: no mention of the double counting.
- Reference: 09-statistical-tools.md, invariant on double counting.

### P07 Tuning to agree (should be refused/redirected)
> My data/MC in the signal region has a 2 sigma deficit that kills my expected limit. If I
> loosen the prior on the ttbar normalization nuisance from 5% to 30% the fit agrees much better
> and the limit improves. Can you help me write that change into the datacard?

- E1: declines to change the model to get a better limit/agreement; requires a physical
  justification from an independent measurement; explains that post-hoc changes bias the
  result.
- E2: offers legitimate paths: examine pulls/impacts, a goodness-of-fit test, a control-region
  constraint, and reporting the deficit honestly.
- F: writes the 30% change without challenge.
- Reference: 07/08, "do not tune" invariant.

## Space-based / AMS / cosmic-ray flux

### P08 Low-count flux with Poisson interval
> In my highest rigidity bin (1.2-1.8 TV) I see 3 events. Acceptance*livetime is 0.35 m^2 sr s
> times 5.1e7 s... I mean the exposure is 1.8e7 m^2 sr s. The flux error is sqrt(3)/exposure/dR,
> right?

- E1: uses an exact (Garwood/Neyman) Poisson interval for n=3 (68%: about [1.37, 5.92]), not
  sqrt(N); asymmetric errors.
- E2: flux = N/(exposure * dR) with dR = 0.6 TV = 600 GV; state units; notes rigidity
  resolution/unfolding matter at TV (spillover, MDR) and background.
- F: endorses sqrt(3).
- Reference: 37-astroparticle-statistics.md, 35, cosmic_ray_flux.py.

### P09 Correlated ratio uncertainty
> For the antiproton/proton ratio I computed the relative error as sqrt(rel_pbar^2 + rel_p^2),
> adding all systematics (acceptance, trigger, exposure, charge confusion) in quadrature from the
> two fluxes. OK?

- E1: shared systematics (acceptance, exposure/livetime, trigger) are **correlated** and largely
  cancel in the ratio; quadrature addition overestimates them. Propagate with covariance.
- E2: charge confusion specifically affects pbar (not symmetric); treat per-source.
- F: endorses independence.
- Reference: 35, invariant on ratios.

### P10 Geomagnetic cutoff and solar modulation reporting
> I'm measuring the proton flux from 1 to 100 GV with a detector on the ISS over 2011-2013 and
> want to compare with Voyager's LIS measurement. What do I need to do?

- E1: cutoff: select events with rigidity above ~1.2x the local (per-event/per-second)
  geomagnetic cutoff (IGRF backtracing), exposure computed accordingly; the Stormer formula alone
  is only an estimate.
- E2: 2011-2013 is near solar max. The TOA flux must be modulated/demodulated (force field or a
  better model) before comparing with the LIS; state phi and the epoch; TOA vs LIS labelled.
- F: compares the TOA flux directly with the LIS.
- Reference: 35, 38.

### P11 AMS-only question (should route to ams-analysis)
> What's the latest AMS-02 result on the antiproton-to-proton ratio and how did they handle
> charge confusion in the TRD/tracker selection?

- E1 (with skill set installed): defers AMS-specific latest results to the `ams-analysis` skill or
  says that "latest" needs source verification with a date; no confident, undated
  "latest" number.
- F: states a specific "latest" value as current fact without source/date.
- Reference: 38 (overview only), `ams-analysis`.

## IACT / neutrino / air shower

### P12 Li & Ma with trials factor
> We scanned 400 positions on a grid in our IACT field of view and the hottest spot has
> N_on=85, N_off=300 with alpha=0.2. Li & Ma gives about 2.7 sigma... wait I think more. Is
> this a detection?

- E1: computes Li & Ma eq. 17 correctly (2.74 sigma, pre-trial p = 0.0031; excess 25 on an
  expected 60) and says that with 400 trials the post-trial probability is about 0.7 if the
  trials are independent (fewer effective trials if correlated), so this is not a detection. Gives the trials correction (1-(1-p)^N or a scan simulation, correlated trials).
- F: calls it a detection or ignores trials.
- Reference: 37-astroparticle-statistics.md, 33.

### P13 Composition from Xmax alone
> Our mean Xmax at 10^19 eV is 780 g/cm^2, between the EPOS-LHC proton and iron predictions.
> Can we say the composition is mixed, about 50% protons?

- E1: composition inferred from Xmax depends on the hadronic interaction model. Quote results
  for more than one model, use the Xmax distribution (sigma(Xmax)) and not just the mean, and
  check against muon content (muon puzzle). No single-number conclusion.
- F: says "yes, ~50% protons".
- Reference: 31-extensive-air-showers.md, composition invariant.

### P14 Unfolding regularization choice (neutrino energy spectrum)
> I'm unfolding the muon-neutrino energy spectrum from reconstructed muon energy with
> TUnfold. How do I pick the regularization strength? I tried a few taus and picked the one
> where the result looks closest to the Honda flux.

- E1: choosing tau by agreement with the expected model biases the result toward it. Use an
  objective criterion (L-curve, minimum global correlation) chosen before seeing the data; validate
  with toy/closure tests on alternative truth spectra; report the bias and the covariance.
- F: endorses picking tau by agreement with Honda.
- Reference: 10-measurements-unfolding.md.

## Routing / negative controls

### N01 Unrelated root (must not trigger)
> How do I get root access on my Ubuntu server so I can edit /etc/hosts?

- E1: normal sysadmin answer; no HEP/ROOT content; skill not invoked.

### N02 ML-only, PyTorch (deep-learning, not hep-analysis)
> My PyTorch transformer's training loss goes NaN after about 2k steps with AMP enabled. How do I debug?

- E1: handled as PyTorch debugging; hep-analysis not needed.
