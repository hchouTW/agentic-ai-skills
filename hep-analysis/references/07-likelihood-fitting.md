# Likelihood Construction and Fitting

## Binned likelihoods

A common model is `L(mu,theta)=product_cb Pois(n_cb | nu_cb(mu,theta)) × L_aux(a | theta)`, where c denotes nonoverlapping channels and b bins. Expected counts combine processes and modifiers; interference or EFT models need not reduce to `mu*s+b`.

Auxiliary likelihood terms describe control measurements. In a frequentist treatment they should not simply be called Bayesian priors. A Bayesian analysis additionally specifies priors and avoids reusing the same information. List observables, global observables, POIs, nuisance parameters, fixed parameters, units, and bounds.

## Unbinned and extended likelihoods

A normalized shape-only likelihood omits total-rate information. To estimate rates, use an extended likelihood such as `exp(-nu)*nu^N/N! × product_i f(x_i)`, with appropriate mixtures/intensities for multiple processes. Normalize consistently over the fit range, especially for sidebands, disjoint ranges, and restricted mass windows.

A covariance correction for weighted unbinned fits does not automatically guarantee coverage. Signed weights and sWeights need suitable methods. Do not treat background-subtracted observations as independent pure-signal Poisson data.

## Identifiability

Check degeneracies before fitting: indistinguishable signal/background shapes, unconstrained CR normalizations, free per-bin backgrounds absorbing signal, or simultaneous freedom in rate and efficiency. Resolve these with justified information or constraints, not arbitrary tightening to make optimization succeed.

## RooFit/RooStats checks

Specify observable and yield ranges, extended mode, constraints, global observables, and ModelConfig. Preserve fit results and inspect status, covariance quality, EDM, invalid evaluations, and boundary hits. Check exact APIs against the installed release.

Use several reasonable initial values and scan POIs/nuisances to identify local minima. Hessian errors can be unreliable at boundaries or for nonquadratic likelihoods; supplement them with profile scans. State the method for asymmetric intervals. Optimizer bounds are not confidence intervals.

Preserve workspace data, PDFs, parameter snapshots, and name mappings, plus external payloads and versions. Ownership, scope, and automatic reuse of identically named objects can connect the wrong components; inspect the actual dependency graph.

Before using a workspace downstream, inspect: variables and their ranges, values,
errors, and constant flags; PDFs and their server dependencies; datasets and entry
counts; functions and normalization objects; and snapshots, named sets, and
categories. Confirm the expected model, data, and observable names match what the
statistical tool expects. `scripts/roofit_workspace_summary.py` prints this inventory
for a `RooWorkspace` inside a ROOT file.

## Diagnostics

Provide pre/postfit yields, residuals, estimates, correlations, and pulls/constraints. Define a pull convention, such as a shift divided by the prefit standard deviation, and acknowledge when non-Gaussian constraints make that scale inappropriate.

Use goodness-of-fit statistics consistent with the data model. Sparse counts do not automatically justify Gaussian per-bin chi-square tests. Treat zero-count terms in saturated deviance through their limits. Fitted parameters, boundaries, and nuisances affect the reference distribution; use refitted toys when needed. A good goodness-of-fit value does not establish absence of bias; perform closure or injection tests.
