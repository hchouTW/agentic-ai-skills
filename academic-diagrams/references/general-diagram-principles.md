# General Diagram Principles

## 1. Model before render

Write the logical graph first, in a neutral form, and validate it before choosing syntax:

```text
Nodes:   id | label | kind (process/data/store/agent/variable/particle) | status (known/inferred/assumed)
Edges:   src -> dst | semantic type | label | status
Groups:  name | members
```

Rendering choices (direction, color, shape) derive from `kind`, edge `semantic type`, and groups - not
the other way round.

## 2. Edge semantics

| Semantic | Typical style | Notes |
|---|---|---|
| data flow | solid arrow | what is passed, not just "flows to" |
| control flow | solid, different head or dashed | who invokes whom |
| causal influence | solid arrow, only if assumptions stated | DAG semantics |
| dependency | dashed arrow (A depends on B: A -> B) | state direction convention |
| temporal order | arrow along a time axis | sequence diagrams |
| mathematical mapping | labeled arrow, `f: X -> Y` | commutative diagrams |
| physical interaction | line style by species | Feynman / decay |
| message passing | solid = sync call, open head/dashed = async or return | sequence |

One meaning per style. Two or more semantics in one figure -> legend or separate figures.
An unlabeled arrow in a figure with a single declared semantic is fine; otherwise label it.

## 3. Choosing abstraction

| Level | Nodes | Use |
|---|---|---|
| Overview | 3-6 | abstract, graphical abstract, intro figure |
| Paper | 6-12 | Methods figure |
| Presentation | 3-7, large text, progressive reveal | talks |
| Detailed technical | 12-30, may be its own figure/appendix | docs, thesis appendix |
| Educational | paper level + annotations, worked labels | lecture notes |

Omit what does not serve the figure's message: implementation detail, obvious steps (e.g. "start"),
bookkeeping stages. Keep what a domain reader would be surprised to find missing.

## 4. Decomposition

Split when: more than ~12-15 nodes, two audiences, two arrow semantics that cannot be
distinguished visually, or two abstraction levels mixed (a physics stage next to a code module).
Typical split: (a) overall architecture, (b) data processing, (c) inference procedure.
Every panel needs one message and shared node names/styles across panels.

## 5. Layout

- LR for computational pipelines; TB for research processes and decision flows;
  hierarchical (rank layered) for dependencies; symmetric where the science is symmetric
  (e.g. detector barrel, t/t-bar decay sides).
- Align stages on a common rank; put feedback loops on the outside; avoid crossings by
  reordering nodes or duplicating a small shared node rather than routing long edges.
- Group with subgraphs/clusters/frames instead of color-only grouping.
- Keep node text short; move detail to caption or a legend.

## 6. Refactoring across abstraction levels

Detailed:
```text
Raw hits -> Track reconstruction -> Track fitting -> Primary vertex -> Particle flow -> Jet clustering -> JEC
```
Paper: `Detector data -> Event reconstruction -> Physics objects`.
Rule: collapsed nodes must be named for the union of what they hide, every collapsed edge must
still be true at the coarse level, and no new stage may appear. Keep ids stable so the versions
can be diffed.

## 7. Transformations between diagram types

| From | To | Key moves |
|---|---|---|
| Algorithm prose / pseudocode / code | flowchart | inputs/outputs as parallelograms; each `if`/`while` a decision with labeled exits; explicit termination; loop back-edge; exceptions as a separate exit |
| Methods section | workflow | one node per method step; note inputs/outputs; drop narrative order that is not dependency order |
| Software architecture | sequence | choose one scenario; lifelines = components; messages = calls; note sync/async |
| Bayesian model text | graphical model | variables -> nodes, `~` statements -> edges, indexed variables -> plates |
| HEP analysis text | analysis pipeline | apply HEP checklist, keep generator/reco/data levels separate |
| ML code | architecture | follow the `forward()` tensor path; mark trainable vs fixed, training-only vs inference |
| Pseudocode | flowchart | as above |
| API interaction | sequence | actors, ordered calls, returns, async, retries |
| DB schema | ER | tables -> entities, FKs -> relationships with cardinality |
| Rough sketch | logical graph | list what is unambiguous; ask about unclear glyphs before formalizing |

## 8. Flowchart conventions

Terminator (start/end), parallelogram (I/O), rectangle (process), diamond (decision, every exit
labeled), predefined subprocess (double-edged rectangle), fork/join bars for parallel branches, a
loop expressed as a back-edge to a decision with an explicit **stopping criterion** and (for
iterative numerics) a max-iteration guard. Exceptions get a distinct exit path, not a hidden `else`.

## 9. Ownership of claims

When a diagram states or implies "A causes B", "A is before B", "A uses B", trace the claim to
the source text/code. Unsupported edges are removed or drawn dashed and labeled "assumed".

## 10. Anti-patterns

Generic boxes with meaningless arrows; diagrams that just copy paragraph order; unexplained
arrow types; decorative icons; rainbow palettes; tiny text; long labels; unsupported causal
claims; invented components; mixing mathematical/physical/software semantics silently; a
conceptual sketch presented as an exact apparatus; a simplified process presented as a verified
Feynman diagram.
