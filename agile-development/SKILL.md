---
name: agile-development
description: "Use when making any non-trivial software change - features, bug fixes, refactors, endpoints, UI work, migrations, dependency updates - turning a request into a small, verified, reviewable increment with acceptance criteria and a validation plan. Also covers reviewing a PR, incident response/postmortems, working safely in legacy code without tests, architectural decisions (boundaries, dependency direction, data ownership, ADRs), design docs, estimation, and feature-flagged rollout planning. Triggers on 'implement', 'fix', 'add', 'refactor', 'migrate', 'update', or scoping/reviewing a change, without saying 'Agile'. Also covers implementation discipline (ask vs. assume on ambiguity, minimal changes, avoiding scope creep, verifiable done) - trigger for 'is this overcomplicated', 'am I over-engineering this'. Also covers authoring a canonical worked example - Contrast, Trajectory, Gated Pipeline, Decision-Tree, Elicitation, Adversarial Audit, Test-First, or Postmortem - for a skill's examples/ directory."
---

# Agile Development

Turn software requests into small, verified, reviewable increments: a clear
user-visible outcome, matching existing conventions, checked before you call it
done, reported honestly.

## Core Workflow

1. **Identify the outcome.** What user- or operator-visible behavior should change?
   Ask first only when a wrong guess is expensive or hard to undo (schema, migration,
   published contract, outward-facing behavior); otherwise state a reasonable
   assumption and proceed, presenting competing interpretations rather than silently
   picking one - see [references/implementation-discipline.md](references/implementation-discipline.md).
2. **Reconnoiter before editing.** Read repository instructions (CLAUDE.md, READMEs),
   nearby code, tests, fixtures, and tooling config to find existing conventions.
3. **Write acceptance criteria.** Make them observable and testable - see
   [references/product-framing.md](references/product-framing.md) for the
   given/when/then format and a user-story template.
4. **Pick the smallest coherent slice.** One end-to-end path beats a half-finished
   broad redesign. See "Slicing" in product-framing.md.
5. **Implement inside existing conventions.** Match style, naming, and structure;
   avoid unrelated refactors or formatting churn - see
   [references/implementation-discipline.md](references/implementation-discipline.md)
   for minimal-code guidance.
6. **Add or update tests** proportional to behavior, risk, and blast radius - see
   [references/validation-and-done.md](references/validation-and-done.md).
7. **Run validation**, narrowest first (the specific test), then broader checks
   (module tests, lint, type-check, build) when the change crosses boundaries.
8. **Review your own diff** for scope, clarity, security, privacy, compatibility, and
   accidental changes - see [references/risk-and-quality.md](references/risk-and-quality.md).
9. **Report honestly**: what changed, what passed, what wasn't run and why,
   assumptions made, and remaining risk - see [references/communication.md](references/communication.md).

## Decision Rules

- Prefer repository evidence over assumptions.
- Prefer one usable vertical slice over a broad unfinished redesign.
- Preserve existing behavior unless the request intentionally changes it.
- Make reversible choices when requirements are incomplete.
- Treat tests, type checks, linting, security checks, docs, and migration notes as
  part of "done" - not optional extras.
- Never claim a command passed unless it actually ran and you saw the result.
- Note discovered follow-up work explicitly instead of silently expanding scope.
- Write the minimum code that solves the problem. No speculative features,
  single-caller abstractions, unrequested configurability, or handling for impossible
  states.
- Remove what your change orphaned; mention (don't delete) pre-existing dead code.
  Every changed line should trace directly to the request.

## Code File Requirement

When creating or modifying **any** code file, add a comment block at the top (in the
target language's syntax, e.g. `#`, `//`, `/* */`, `<!-- -->`) briefly covering:

- **Purpose** - why the file exists.
- **What the code does** - its main behavior or responsibility.
- **Usage notes, dependencies, or assumptions** - how to run/import it, dependencies,
  preconditions.

For existing files, add or update this block if missing or outdated, proportional to
the file's complexity, and review it in the diff so it doesn't drift from the code.

## When to Load References

- **Ask vs. assume, keeping the change minimal and surgical, verifiable success criteria** -> [references/implementation-discipline.md](references/implementation-discipline.md)
- **Story framing, readiness, backlog slicing** -> [references/product-framing.md](references/product-framing.md)
- **Test strategy, validation ladder, definition of done** -> [references/validation-and-done.md](references/validation-and-done.md)
- **Scenario playbooks** (bug fix, new feature, new endpoint, UI feature, DB migration,
  dependency update, CLI change) -> [references/engineering-playbook.md](references/engineering-playbook.md)
- **Risk areas**: API/interface changes, data & persistence, security & privacy,
  dependencies, config, observability, performance, accessibility ->
  [references/risk-and-quality.md](references/risk-and-quality.md)
- **Status updates and completion summaries** -> [references/communication.md](references/communication.md)
- **C++ design** (classes vs. structs vs. free functions, ownership, RAII, composition
  vs. inheritance, error handling) -> [references/cpp-balanced-design-guidelines.md](references/cpp-balanced-design-guidelines.md)
- **Python design** (classes vs. dataclasses vs. free functions, context managers,
  protocols vs. inheritance, exceptions vs. sentinel returns) ->
  [references/python-balanced-design-guidelines.md](references/python-balanced-design-guidelines.md)
- **Bash design** (functions vs. associative arrays, avoiding simulated OOP,
  trap-based cleanup, quoting/`set -euo pipefail` discipline) ->
  [references/bash-balanced-design-guidelines.md](references/bash-balanced-design-guidelines.md)
- **Design docs/RFCs, estimation and spikes, feature flags and progressive rollout** ->
  [references/design-and-estimation.md](references/design-and-estimation.md)
- **Software architecture, component boundaries, dependency direction, data
  ownership, architectural tradeoffs, or ADRs** ->
  [references/software-architecture.md](references/software-architecture.md)
- **Production incidents/outages, working safely in legacy code without tests** ->
  see the Incident Response and Legacy Code Without Tests sections in
  [references/engineering-playbook.md](references/engineering-playbook.md)
- **Reviewing someone else's change** -> see the Reviewing Someone Else's Change
  section in [references/risk-and-quality.md](references/risk-and-quality.md)
- **Authoring a canonical worked example** in any of eight archetypes -
  Contrast (Weak vs. Expert), Execution Trajectory, Gated Pipeline,
  Decision-Tree, Interactive Elicitation ("Grill-Me"), Adversarial Audit /
  Red-Teaming, Test-First / Red-to-Green, or Incident Postmortem & RCA - for
  this or another skill's `examples/` directory ->
  [references/example-authoring.md](references/example-authoring.md)
- **Designing or budgeting a prompt for an LLM call** - agent skills, prompt
  templates, structured-output contracts, model-tier choice, token budgets ->
  [references/prompt-engineering-and-token-optimization.md](references/prompt-engineering-and-token-optimization.md)

## Reusable Templates

Copy these into a task when structured notes help:

- [assets/story-card.md](assets/story-card.md) - user story, acceptance criteria,
  assumptions, validation plan.
- [assets/definition-of-done.md](assets/definition-of-done.md) - completion checklist.
- [assets/risk-register.md](assets/risk-register.md) - lightweight risk/mitigation table.
- [assets/completion-summary.md](assets/completion-summary.md) - final response structure.

## Helper Scripts

- `scripts/create_story_card.py --actor "..." --capability "..." --outcome "..."` -
  generates a filled-in story card markdown file (repeat `--criteria`/`--validation`
  for multiple lines; optional `--assumption`, `--in-scope`, `--out-of-scope`, `--risk`,
  `--output`).
- `scripts/validate_agile_notes.py <file.md>` - checks a markdown note for the sections
  a complete Agile delivery note should have (story, acceptance criteria, validation,
  risks).
- `scripts/validate_skill_bundle.py` - check that this package's own files (SKILL.md,
  README.md, references, scripts, assets, tests) are all present and non-empty, and
  that SKILL.md/README.md have their expected structure (standard library only).
- `tests/test_agile_skill.py` - standard-library tests for `create_story_card.py`/
  `validate_agile_notes.py`. Run `python3 -m unittest discover -s tests -v`.

Run with `python3`. Read a script before changing it.

## Quick Checklists

### Before Editing
- [ ] The requested outcome and affected behavior are understood.
- [ ] Repository instructions and nearby patterns were inspected.
- [ ] The smallest useful slice is identified.
- [ ] The simplest implementation that satisfies the request was considered.
- [ ] Ambiguity was resolved by cost: asked where a wrong guess is expensive, assumed
      and stated otherwise.
- [ ] Tests/validation steps for this slice are known.
- [ ] Security, privacy, compatibility, and data risks were considered.

### Before Reporting Done
- [ ] Acceptance criteria are met, or deviations are stated clearly.
- [ ] Relevant tests and checks were actually run (not assumed).
- [ ] The diff was reviewed for scope and accidental changes.
- [ ] Every changed line traces to the request; orphans from this change were removed
      and pre-existing dead code was left alone.
- [ ] Edge cases and regression risk were considered.
- [ ] The response states changes, verification, assumptions, and residual risk.

## Example Prompts This Skill Handles Well

- "Add an endpoint that lets admins export a CSV of active users."
- "This refactor of the auth middleware shouldn't change behavior - help me do it safely."
- "Bump the `requests` dependency and make sure nothing breaks."
- "I have a bug report saying the cart total is wrong with discount codes - find and fix it."
- "Review my diff before I open a PR."
- "Generate a canonical `examples/` entry for the `hep-analysis` skill contrasting a
  weak vs. expert systematics writeup." (Contrast archetype)
- "Walk the cart-total discount-code bug report through a full triage-to-verified-fix
  trajectory for `agile-development/examples/`." (Execution Trajectory archetype)
- "Author a gated-pipeline example showing how to draft and red-team an RFC for a
  feature-flagged rollout." (Gated Pipeline archetype)
- "Author a decision-tree example for triaging an ambiguous production incident page."
  (Decision-Tree archetype)
- "Generate a Grill-Me elicitation example for `hep-analysis` starting from
  'can you check if there's a signal in this dataset?'" (Elicitation archetype)
- "Red-team this 'SOTA accuracy' training writeup for leakage or a cherry-picked
  seed." (Adversarial Audit archetype)
- "Write a test-first example for a DataLoader throughput invariant, red test
  through green with metrics." (Test-First archetype)
- "Author a postmortem example for a distributed training run that diverged at
  hour 30." (Postmortem archetype)

## Caveats

- This skill governs *how* to work, not *what* to build - pair it with
  domain skills (e.g. `deep-learning`, `hep-analysis`) for specialized code.
- If the user explicitly says not to run tests or not to use TDD, follow that -
  user instructions take precedence over this workflow.
- Don't pad small fixes with the full template structure; collapse the completion
  summary to one or two sentences plus a verification line for trivial changes.
