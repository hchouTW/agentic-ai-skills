# HEP 7: Feynman-style interaction

**Request:** "Draw e⁺e⁻ → μ⁺μ⁻ via a virtual photon."
**Type:** Feynman diagram (s-channel, tree-level QED). Process is fully specified by the user, so a formal diagram is appropriate. If the process had been vague ("some Higgs process"), ask for it (and the model) rather than invent vertices.

Vertex checks: γ*e⁺e⁻ and γ*μ⁺μ⁻ are QED vertices; charge conserved (0 → +1 − 1); fermion-flow continuous on each line.

```latex
% Requires: \usepackage{tikz-feynman}; automatic layout requires LuaLaTeX. Not compiled here.
\feynmandiagram [horizontal=a to b] {
  i1 [particle=\(e^-\)] -- [fermion] a -- [fermion] i2 [particle=\(e^+\)],
  a -- [photon, edge label=\(\gamma^*\)] b,
  f1 [particle=\(\mu^+\)] -- [fermion] b -- [fermion] f2 [particle=\(\mu^-\)],
};
```
Channel: s-channel (propagator carries $s=(p_{e^-}+p_{e^+})^2$). Adding Z exchange would require stating the electroweak assumption.
**Caption:** Leading-order Feynman diagram for $e^+e^-\to\mu^+\mu^-$ through s-channel virtual-photon exchange. Time runs left to right; arrows on fermion lines indicate fermion-number flow.
