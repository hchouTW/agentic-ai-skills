# Multivariate Classifiers: BDTs and Neural Networks in Analysis

Extends [references/11-ml-analysis.md](11-ml-analysis.md)'s splits/weights/validation
principles with concrete guidance on training and choosing between classifier
families. Read 11-ml-analysis.md first; this file assumes it.

## Choosing a classifier family

- **Boosted decision trees** (XGBoost, LightGBM, or TMVA's BDT) remain a strong
  default for tabular, engineered-feature inputs of the size typical in an analysis
  (tens of features, thousands to low millions of weighted events): they need
  comparatively little hyperparameter tuning to reach a reasonable operating point,
  train quickly enough for iterative feature engineering, and their feature-importance
  and single-tree outputs are easier to sanity-check against physical expectation
  than a neural network's internal representations.
- **Neural networks** are worth the additional complexity when the input is not
  naturally tabular (raw or lightly processed detector images, point clouds of
  reconstructed objects, sequences), when a specific architecture encodes a known
  symmetry the analysis wants to exploit (permutation invariance over jets, for
  example), or when combining many heterogeneous input types benefits from learned
  rather than hand-engineered combination. A plain feed-forward network on the same
  engineered features a BDT would use rarely outperforms a well-tuned BDT enough to
  justify its extra tuning and validation burden.
- Simple cuts remain preferable to either when the separating power comes from one or
  two variables with an intuitive, easily-communicated physical origin, and when the
  analysis's audience or later reinterpretation needs a transparent selection rather
  than an opaque score. A classifier that only marginally beats a two-variable cut
  is not automatically worth its added validation and correlation-with-mass burden.

## Feature engineering and selection

Prefer physically motivated features (masses, angular separations, kinematic
combinations with known discriminating power) over an undifferentiated dump of every
available low-level variable - beyond making the model more interpretable, this
reduces the chance of accidentally including a feature that encodes look-elsewhere
information about the signal region definition itself (a variable correlated with the
selection used to define signal/control regions can leak information across regions
in ways that are easy to miss until a closure test fails). Check pairwise correlation
and, more importantly, correlation of each candidate feature with the observable used
in the final fit (typically a mass) before including it - a feature with strong
correlation to the fit observable will sculpt the background shape after a selection
on the classifier score, which is the mass-sculpting concern already raised in
11-ml-analysis.md and needs the mitigation described there (decorrelation, or fitting
in categories with re-derived background shapes).

## Training practicalities: BDTs

- Tree depth and the minimum number of events per leaf are the primary
  overtraining controls; with limited weighted MC statistics, a deep tree can
  memorize individual high-weight events rather than learning a generalizable
  boundary - check the effective (weighted) statistics per leaf, not just the raw
  event count, especially in samples with large weight variance (see
  [references/03-weights-normalization.md](03-weights-normalization.md) on negative
  and highly variable weights).
- Use k-fold cross-training/application (train on k-1 folds, apply to the held-out
  fold, rotate) rather than a single train/test split when MC statistics are limited
  enough that a held-out test set would otherwise cost meaningful training statistics
  - this lets every event contribute to both training and (out-of-fold) application
  without any event being scored by a model that saw it during training.
- Compare training and validation-fold loss/AUC curves versus boosting round to pick
  the number of trees (early stopping on the validation fold) rather than a fixed
  round count decided in advance; a round count picked once and reused across
  reprocessing campaigns without rechecking silently drifts from optimal as input
  samples change.

## Training practicalities: neural networks

- Class imbalance between signal and background is common and is usually handled
  through the loss weighting scheme (matching the formal event weights - see
  11-ml-analysis.md's "Weights and objectives") rather than naive oversampling of the
  minority class, which can distort the effective statistical power of the training
  sample.
- Batch composition matters when using physics event weights: a batch that happens to
  contain a small number of very high-weight events can dominate the gradient for that
  step; monitor the effective sample size within batches (or pre-bin/cap extreme
  weights, documenting the cap) rather than assuming standard-deep-learning batching
  intuition transfers unchanged from unweighted computer-vision-style datasets. See
  [[deep-learning]] for general PyTorch training-loop and debugging practices (NaN
  losses, gradient clipping, evaluation-mode pitfalls) that apply here unchanged once
  the physics-specific weighting above is handled correctly.
- Prefer starting from a simple, shallow architecture and confirming it beats (or at
  least matches) a well-tuned BDT baseline before investing in a deeper/more exotic
  architecture - a complex network that underperforms a simple BDT baseline usually
  indicates a data or training-procedure problem, not that more capacity is needed.

## Calibration and combination

A classifier's raw output score is not automatically a calibrated probability, and
combining multiple classifiers' scores (or using a score as one input among several
observables in a combined fit) requires either calibrating scores against a common
reference (e.g. isotonic regression or Platt scaling against a validation sample) or
using the score only through its rank/selection threshold rather than its literal
value as though it were a probability. Document which convention is used, since
downstream statistical combination methods
([references/09-statistical-tools.md](09-statistical-tools.md)) may implicitly assume
one.

## Validation beyond 11-ml-analysis.md's checklist

- Compare feature distributions and the classifier score itself between the
  nominal MC sample and at least one systematic variation to confirm the classifier
  hasn't learned to key on a feature that is itself unstable under systematics (e.g.
  a variable whose modeling differs significantly between generators) - a classifier
  can achieve good nominal separation while being unexpectedly sensitive to a
  systematic uncertainty's variation, inflating that uncertainty's impact on the
  final result in a way that a nominal-only validation would miss.
- For a BDT, inspect feature importance and the highest-importance features' physical
  plausibility as a sanity check before trusting the model, not as a substitute for
  the statistical validation in 11-ml-analysis.md - a feature importance ranking that
  contradicts known physics (e.g. an ostensibly unrelated detector-region indicator
  ranking above a kinematic variable expected to dominate) is a signal to investigate
  for a labeling or leakage bug before proceeding.

## Deliverables

- Classifier family chosen and the comparison (if any) against a simpler baseline
  that justified it.
- Feature list with the physical motivation for each, and the correlation-with-fit-
  observable check performed.
- Cross-validation/k-folding scheme (or train/test split) and the effective
  (weighted) statistics per fold.
- Score calibration convention used, if scores are combined with other observables.
- Systematic-variation stability check for the classifier score, alongside the
  standard validation layers in 11-ml-analysis.md.
