# Equation and notation auditing

Use for checking equations or notation in a manuscript, not as a substitute for
validating the underlying analysis. Establish which sections and derivations are
in scope; report unchecked portions explicitly.

Build a symbol ledger as needed: symbol, definition, first-use location, units or
dimensions, scalar/vector/tensor shape, index range, and local scope. Distinguish
intentional local reuse from contradictory definitions. Check equations, prose,
captions, and appendices against the same conventions.

Check the following where applicable:

- Terms added or equated have compatible dimensions and shapes; free indices
  agree and dummy indices are contracted consistently. Check transpose versus
  conjugate transpose and the measure in sums, integrals, and expectations.
- Logarithms and exponentials have dimensionless arguments under the stated
  convention. Establish natural units, normalized variables, or absorbed constants
  before reporting a dimensional error.
- Normalization factors, signs, boundaries, conditioning, and domains are stated.
  Check limiting cases, singular denominators, and probability normalization where
  they can meaningfully reveal mistakes.
- Each derivation step follows under its stated assumptions. Label approximations
  and where they apply; check assumptions such as independence, differentiability,
  invertibility, or interchange of limits/integration when a step depends on them.
- Definitions and numbering remain consistent when equations are reused in
  algorithms, text, or supplementary derivations.

For a suspected error, show the specific step or counterexample and the convention
used. Distinguish definite inconsistency, ambiguous notation, and an unverified
derivation. Symbolic simplification and numerical spot checks may corroborate a
finding but do not establish a general proof; record assumptions and test domains.
Never silently repair a scientific formula whose intended meaning is unclear.

Deliver findings with equation/line locator, issue, supporting calculation,
scientific impact, and minimal proposed correction. Separate cosmetic notation
changes from changes that could alter reported results.
