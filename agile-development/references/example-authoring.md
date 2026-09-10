# Authoring a Canonical Skill Example

How to produce a `<skill>/examples/` entry: a complete, production-ready worked
example for a realistic scenario in that skill's domain, in whichever of four
**archetypes** fits the scenario. Use this when asked to "author," "generate,"
or "add a canonical example" (in any archetype) for `agile-development` itself
or for another installed skill.

## Which archetype fits?

A quick triage before generating anything - itself formalized as this
package's own Decision-Tree archetype in miniature:

| Trigger | Archetype |
|---|---|
| Teaching one principle by contrasting a wrong way and a right way to do the same thing | **Contrast** |
| Walking a single raw input (a bug report, an incident page) start-to-finish through triage, execution, and verification | **[A] Execution Trajectory** |
| Building one complex artifact incrementally, where each stage must clear an explicit acceptance gate before the next starts | **[B] Gated Pipeline** |
| Choosing among several plausible responses to an ambiguous trigger, then committing to and executing one | **[C] Decision-Tree** |

If a scenario could fit two archetypes, prefer the one whose fixed sections
already match the scenario's natural shape (e.g. a scenario with real
pass/fail checkpoints is Gated Pipeline even if it could be flattened into a
Trajectory).

## The four generation prompts

The reusable core - each archetype's literal template, with its blanks bound
to concrete values before running it. All four share the same opening clause
and a seniority word that escalates with the archetype's scope and authority
(see "Role/seniority convention" below).

**Contrast**
```
Act as a senior {role} to create a standard example for `{skill}/examples/` in the
`{skill}` skill. Using a realistic {domain_use_case}, draft a complete,
production-ready artifact with zero placeholders. Format the artifact as a direct
contrast between a "Common Weak Approach" and an "Expert-Level Best Practice",
followed by {n} key takeaways explaining the architectural difference.
```

**[A] Execution Trajectory**
```
Act as a senior {role} to create a task-oriented execution trajectory example for
`{skill}/examples/` in the `{skill}` skill. Starting from a realistic, raw
{problem_input}, demonstrate a step-by-step resolution workflow. Structure the
artifact as: 1. Task Input & Context, 2. Root-Cause Triage & Action Plan,
3. Surgical Execution (exact commands, tool usage, or code modifications),
4. Verification Evidence (log outputs or automated test pass), and 5. Final
Deliverable Summary.
```

**[B] Gated Pipeline / Multi-Phase**
```
Act as a principal {role} to create a multi-phase workflow example for
`{skill}/examples/` in the `{skill}` skill. For a complex {high_stakes_task}, show
how to incrementally construct the artifact through explicit quality gates.
Structure the artifact across 3 distinct phases: Phase 1: Input Extraction & Gap
Formulation (with acceptance gate), Phase 2: Draft Synthesis (aligning with
specific regulatory/evaluation criteria), and Phase 3: Red-Team Review & Final
Artifact Packaging (stress-testing assumptions and final polish).
```

**[C] Decision-Tree / Branching Response**
```
Act as a lead {role} to create a branching decision-tree example for
`{skill}/examples/` in the `{skill}` skill. Given a complex
{challenging_scenario_with_edge_cases}, define a clear triage matrix mapping
triggers to resolution strategies. Select the most critical branch and provide a
complete, end-to-end execution script showing exact actions, communication
scripts, and fallback safeguards.
```

Common blanks:
- `{role}` - a specific seniority + specialty (e.g. "Staff Software Engineer",
  "Senior Experimental Particle Physicist"), not a generic "expert."
- `{skill}` - the target skill's folder name (e.g. `hep-analysis`).
- `{domain_use_case}` / `{problem_input}` / `{high_stakes_task}` /
  `{challenging_scenario_with_edge_cases}` - a concrete, narrow scenario
  grounded in that skill's own reference material, not invented or generic.
- `{n}` (Contrast only) - the number of key takeaways; default 4, minimum 3,
  maximum 6.

This step is content generation, not something a stdlib script can do
correctly for physics or ML domain content - domain correctness needs an agent
actually reasoning through the example with the target skill's own
`references/` loaded, the way a person would. The scaffold and validator
scripts below only produce and check structure; they do not write or judge the
domain content itself.

### Role/seniority convention (keep this, don't flatten it)

Each archetype escalates the actor's seniority on purpose:

| Archetype | Seniority word | Why |
|---|---|---|
| Contrast | senior | Teaching a single principle by comparison - individual-contributor judgment call. |
| Execution Trajectory | senior | Hands-on resolution of one concrete input - still IC-level, but end-to-end. |
| Gated Pipeline | **principal** | High-stakes, multi-phase construction against external (regulatory/evaluation) criteria - needs the authority to define acceptance gates. |
| Decision-Tree | **lead** | Requires the standing to define a triage matrix and commit to a branch on others' behalf, including fallback/communication responsibility. |

## Workflow

1. **Scaffold.** Run `scripts/generate_skill_example.py` with `--archetype`,
   `--skill`, `--role`, and that archetype's scenario flag (`--use-case` /
   `--problem-input` / `--high-stakes-task` / `--scenario`; `--takeaways` is
   valid only with `--archetype contrast`) to emit an empty skeleton with the
   right frontmatter and section headers at the right path - mirrors how
   `create_story_card.py` scaffolds a story card without inventing the story.
2. **Fill.** Replace every skeleton placeholder with real content per that
   archetype's format spec below. Zero placeholders (see below).
3. **Validate.** Run `scripts/validate_skill_example.py <file>` - it reads the
   `archetype:` frontmatter field to pick the rule set, then mechanically
   rejects structural defects and placeholder content. It cannot judge domain
   correctness (see Correctness review below).
4. **Index.** Add or update `<skill>/examples/README.md`, a one-row-per-example
   table: `Example | Archetype | Scenario | One-line takeaway`.
5. **Wire it up.** If this is the first example for that skill, add
   `examples/README.md` and the new example file to that skill's own
   `scripts/validate_skill_bundle.py` `REQUIRED_PATHS` (or, for a skill whose
   validator checks orphaned files by scanning `references/`/`scripts/`/`assets/`
   only, no change is needed there - confirm which kind the target skill has
   before assuming). Log the pass in that skill's `VALIDATION.md`.

## Format specification

Shared conventions across all four archetypes:

- **File location:** `<skill>/examples/<NN>-<archetype>-<slug>.md`, where
  `archetype` is one of `contrast`, `trajectory`, `gated-pipeline`,
  `decision-tree` - a two-digit prefix for stable ordering, plus one
  `<skill>/examples/README.md` index.
- **Frontmatter:** `role:`, `skill:`, `archetype:`, plus one archetype-specific
  scenario field (see below), so the validator and index generator can read it
  back without re-parsing prose. A file with no `archetype:` field is treated
  as `contrast` by the validator, for backward compatibility with examples
  written before this reference and its scripts became archetype-aware; new
  examples of any archetype, including Contrast, should set `archetype:`
  explicitly.
- **Zero-placeholder rule (all archetypes):** no `TODO`, `TBD`, `XXX`, `FIXME`,
  `Lorem ipsum`, bracketed stand-ins like `[Your ...]`, or trailing `...` where
  real content belongs; every command, log excerpt, or code fence must be
  complete and literal, not illustrative.
- **Language.** English, matching this repository's rule that all maintained
  instructions, templates, and metadata are in English.

**Contrast** - `## Scenario`, `## Common Weak Approach`, `## Expert-Level Best
Practice`, `## Key Takeaways` (bulleted, default N = 4, min 3 / max 6).
Frontmatter scenario field: `use_case:`.

**[A] Trajectory** - five fixed sections, in this exact order: `## 1. Task
Input & Context`, `## 2. Root-Cause Triage & Action Plan`, `## 3. Surgical
Execution`, `## 4. Verification Evidence`, `## 5. Final Deliverable Summary`.
Section 3 must contain at least one literal command/diff/code block; section 4
must contain a literal log excerpt or test-runner output, not a description of
one - the validator checks for a fenced code block in both sections, not just
prose. Frontmatter scenario field: `problem_input:`.

**[B] Gated Pipeline** - three fixed phase headings, each containing a
`**Gate:**` sub-line stating the explicit pass/fail criterion before moving on
(Phase 3's gate is the final release/merge criterion, not an intermediate
one): `## Phase 1: Input Extraction & Gap Formulation` (ends with `**Gate:**
...`), `## Phase 2: Draft Synthesis` (must name the specific
regulatory/evaluation criteria it aligns to - e.g. a cited section of
`references/...md` for that skill, not a vague "best practices"), `## Phase 3:
Red-Team Review & Final Artifact Packaging` (must list at least one assumption
it stress-tested and what changed as a result). Frontmatter scenario field:
`high_stakes_task:`.

**[C] Decision-Tree** - `## Triage Matrix` (a markdown table, columns `Trigger
| Resolution Strategy`, at least 3 rows so it's a real tree, not a single
if/else), `## Selected Branch` (states which row was chosen and why, given the
scenario), `## End-to-End Execution Script` (the full walkthrough for that
branch: actions, any communication script verbatim, not summarized), `##
Fallback Safeguards` (what happens if the chosen branch's primary action fails
or the trigger was misclassified). Frontmatter scenario field: `scenario:`.

## Correctness review

The validator enforces structure, per-archetype rules (gate lines, table
shape, code-fence presence), and rejects placeholders; it cannot verify that a
`hep-analysis` systematics example is physically correct, that a
`deep-learning` example's code actually runs, or that Gated Pipeline's Phase 2
cites a genuinely specific regulatory/evaluation criterion rather than a vague
"industry best practices" - that specificity check is a review responsibility,
not a mechanical one. Treat all of this as a review step, not something to
automate away: before merging a new example, have it read (or, for runnable
code, executed) by someone - or an agent with that skill's own `references/`
loaded - able to judge that domain.

## Cross-skill use

This reference lives only in `agile-development` and is shared by cross-link
rather than copied into each skill - the routing rule in
`skill-router/SKILL.md` and each rollout skill's own "When to Load
References"-equivalent section point back here. That means a skill installed
without `agile-development` alongside it cannot use this capability; call that
out explicitly wherever the pointer is added, matching how this repository's
root README already documents partial installs as supported.

Don't add `examples/` to a skill's `REQUIRED_PATHS` (or equivalent orphan
check) until that skill actually has a populated `examples/` directory - an
empty requirement would make the validator lie about coverage.
