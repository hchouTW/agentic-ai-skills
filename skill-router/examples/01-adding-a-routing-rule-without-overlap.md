---
role: Senior Platform / Developer-Experience Engineer
skill: skill-router
use_case: adding a new routing rule to the table without creating overlap or ambiguity with an existing rule
---

## Scenario

A new domain skill, `data-engineering`, is being added to this collection, and
it needs a routing rule in `skill-router/SKILL.md`'s "Routing rules" table so
tasks in its domain get triaged to it. Two existing rules already touch
adjacent territory: `deep-learning` covers "datasets and DataLoaders" and
"dataset design and split leakage," and `hep-analysis` covers "uproot/awkward
columnar pipelines" (its own `references/02-data-pipelines.md` is literally
titled "data pipelines"). The new rule has to be added without making a task
like "review my data pipeline" ambiguous between three rules.

## Common Weak Approach

```markdown
- **data-engineering** - working with data pipelines and datasets.
```

This is added to the table, `python3 scripts/validate_skill_bundle.py` is run,
and it passes. That pass is misleading: the validator's
`extract_routed_skill_names` only checks that a bullet matches the
`- **name** - ...` format and, separately, that the name has a matching
sibling folder - it has no way to detect that "working with data pipelines and
datasets" is also a fair one-line summary of what `deep-learning` and
`hep-analysis` already cover. A request like "review my data pipeline for
loading training data" now plausibly matches all three rules with nothing in
any of their text to break the tie, which is exactly the ambiguity `skill-router`
exists to prevent. The new rule also carries no "Not for..." boundary clause,
even though every other rule in the table has one precisely to head off this
kind of collision (`academic-papers`: "Not for the underlying statistical/ML/
physics analysis itself"; `deep-learning`: "Not for TensorFlow, JAX, or other
frameworks"; `hep-analysis`: "Not for unrelated uses of 'root'").

## Expert-Level Best Practice

```markdown
- **data-engineering** - building or operating data-engineering pipelines
  outside model training or physics-analysis code paths: ELT/ETL
  orchestration (Airflow/dbt/Spark job graphs), data-warehouse loading,
  pipeline scheduling/monitoring/backfills, and schema/contract management
  between upstream and downstream systems. Not for PyTorch `Dataset`/
  `DataLoader` code or ML dataset design - see `deep-learning`; not for
  ROOT/uproot/awkward event-level I/O pipelines - see `hep-analysis`.
```

Before writing this, the engineer read every existing rule specifically
looking for adjacent territory (not just skimmed the table), found the two
collisions named in the Scenario, and wrote the new rule to name what's
in-scope in terms that don't reuse `deep-learning`'s or `hep-analysis`'s own
vocabulary ("orchestration," "warehouse loading," "schema/contract
management" instead of "datasets and pipelines"), then added an explicit
"Not for" clause pointing each adjacent skill to where its territory actually
is - matching the pattern already used by every other rule in the table. This
was verified two ways, not just asserted: first, `extract_routed_skill_names`
(imported directly from the real `scripts/validate_skill_bundle.py`) parses
both the weak and the expert version of this bullet identically -
`['data-engineering']` either way - confirming that passing the structural
validator is not evidence the ambiguity is gone, since the validator cannot see
it in either case. Second, "review my data pipeline for loading training data"
was checked against the expert rule's text by hand: "training" and "loading
training data" fall under the `deep-learning` boundary clause explicitly, so
the rule text itself - not the validator - resolves the case a reader would
otherwise have to guess at.

## Key Takeaways

- A rule can be syntactically well-formed and still be semantically ambiguous;
  `skill-router`'s own bundle validator checks the former
  (`extract_routed_skill_names` matching `- **name** - ...`) and has no
  mechanism for the latter - verified directly: it parses the weak and expert
  versions of the same bullet identically. Passing the validator is not
  evidence a new rule is unambiguous.
- Read every existing rule for adjacent territory before adding a new one, not
  just to confirm the new skill's own name doesn't collide. The collisions
  here were with `deep-learning`'s dataset language and `hep-analysis`'s
  "data pipelines" reference title, not with anything about `data-engineering`
  itself - overlap is a property of the *pair* of rules, not either rule read
  alone.
- Give a new rule a "Not for X - see Y" boundary clause whenever its territory
  is adjacent to an existing rule, matching the pattern every existing rule in
  this table already uses. The clause does double duty: it scopes the new
  rule, and it also disambiguates the *old* rule for the specific case that
  would otherwise be ambiguous between the two.
- Word a rule's in-scope description using vocabulary distinct from its
  neighbors' descriptions, not just a distinct skill name. "Working with data
  pipelines and datasets" is generic enough to double as a summary of two other
  rules already in the table; "ELT/ETL orchestration, data-warehouse loading,
  pipeline scheduling" is specific enough that it doesn't accidentally describe
  someone else's territory too.
