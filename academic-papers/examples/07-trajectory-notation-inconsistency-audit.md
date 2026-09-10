---
role: Manuscript Consistency Editor
skill: academic-papers
archetype: trajectory
problem_input: a co-author flags that a late-manuscript equation appears to reuse a symbol already defined earlier in the paper for a different physical quantity
---

## 1. Task Input & Context

Co-author's note: "Something looks off in Eq. 12 - it reads like it's mixing
up two different things we call σ elsewhere in the paper. Can you check
before we submit?"

## 2. Root-Cause Triage & Action Plan

Per `references/equation-and-notation-auditing.md`, a symbol ledger was
built for σ across the manuscript before judging Eq. 12 in isolation:

| Location | Definition | Units |
|---|---|---|
| Sec. II, Eq. 3 | σ = production cross-section | pb |
| Sec. III, prose | "σ" used informally for "the cross-section" (consistent with Eq. 3) | pb |
| Sec. IV, Eq. 12 | σ appears again, this time as the fit uncertainty on a nuisance parameter θ | dimensionless |

Eq. 12 as typeset is:

`Z = (μ̂ - μ₀) / σ`, where the text below it says "σ is the cross-section
from Eq. 3."

This is a contradictory definition, not intentional local reuse: Eq. 12 is a
significance formula (signal strength divided by its own uncertainty), which
requires σ in the denominator to be the uncertainty on μ̂, not the
production cross-section from Eq. 3 - the equation is dimensionally
inconsistent as captioned, since a significance ratio must be dimensionless
throughout and Eq. 3's σ carries units of pb. Per the reference's guidance to
distinguish a definite inconsistency from a mere convention difference: this
is a definite inconsistency (it changes what the equation says, not just how
it's typeset), so it is reported and fixed, not left as a stylistic
difference.

Action plan: rename the fit-uncertainty symbol in Eq. 12 to σ_θ, correct the
text below it to describe σ_θ (not the Eq. 3 cross-section), and numerically
spot-check that the significance value quoted in the abstract is unaffected
by the renaming (it must be - the renaming only fixes the label, not the
underlying computed value).

## 3. Surgical Execution

```diff
--- a/manuscript/section4.tex
+++ b/manuscript/section4.tex
@@ -58,7 +58,9 @@
-Z = (\hat{\mu} - \mu_0) / \sigma
+Z = (\hat{\mu} - \mu_0) / \sigma_\theta
 %
-where $\sigma$ is the cross-section from Eq.~3.
+where $\sigma_\theta$ is the fitted uncertainty on $\hat{\mu}$ obtained from
+the profile likelihood scan of Sec.~IV.A, distinct from the production
+cross-section $\sigma$ defined in Eq.~3.
```

## 4. Verification Evidence

```
$ python3 -c "
mu_hat, mu_0, sigma_theta = 1.18, 0.0, 0.31
Z = (mu_hat - mu_0) / sigma_theta
print(f'Z = {Z:.2f}')
"
Z = 3.81
```

The recomputed significance (`Z = 3.81`) matches the value already quoted in
the abstract, confirming the renaming corrected only the label, not the
underlying numeric result - exactly the "minimal proposed correction" the
reference calls for, not a re-derivation.

## 5. Final Deliverable Summary

Traced a contradictory reuse of σ (production cross-section in Sec. II vs.
fit uncertainty in Sec. IV's Eq. 12) using a symbol ledger built across the
whole manuscript, confirmed it was a genuine inconsistency rather than a
convention difference, renamed the Eq. 12 symbol to σ_θ, corrected the
surrounding text, and numerically verified the abstract's quoted significance
(Z = 3.81) is unchanged by the fix.
