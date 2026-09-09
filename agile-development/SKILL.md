---
name: agile-development
description: Use for any non-trivial software change - new features, bug fixes, refactors, endpoints, UI work, migrations, or dependency updates. Turns a request into a small, verified, reviewable increment with clear acceptance criteria and a validation plan. Also covers reviewing someone else's change/pull request, production incident response and postmortems, working safely in legacy code without tests, and writing a lightweight design doc, estimating work, or planning a feature-flagged/progressive rollout for larger or riskier changes. Invoke this whenever the user asks to "implement", "fix", "add", "refactor", "migrate", or "update" code, review a PR, respond to an outage, or asks how a change should be scoped, estimated, tested, or reviewed. Also covers implementation discipline: whether to ask or assume when a request is ambiguous, keeping a change minimal and surgical rather than overcomplicated or over-engineered, avoiding scope creep and unrelated refactors, and turning a vague task into verifiable success criteria - trigger it for "is this overcomplicated", "keep the change minimal", "am I over-engineering this", or "what does done mean here" - even if they don't mention "Agile" by name.
---

# Agile Development

Turn software requests into small, verified, reviewable increments. The goal is not
ceremony - it's making sure every change has a clear user-visible outcome, fits
existing conventions, is checked before you call it done, and is reported honestly.

## Core Workflow

1. **Identify the outcome.** What user-visible or operator-visible behavior should
   change? If it's ambiguous, decide by what being wrong costs: ask first when a wrong
   guess is expensive or hard to undo (schema, migration, published contract,
   user-visible behavior, anything outward-facing); otherwise state a reasonable
   assumption rather than blocking. Present competing interpretations instead of
   silently picking one - see
   [references/implementation-discipline.md](references/implementation-discipline.md).
2. **Reconnoiter before editing.** Read repository instructions (CLAUDE.md, READMEs),
   nearby code, tests, fixtures, and tooling config to find existing conventions.
3. **Write acceptance criteria.** Make them observable and testable - see
   [references/product-framing.md](references/product-framing.md) for the
   given/when/then format and a user-story template.
4. **Pick the smallest coherent slice.** One end-to-end path beats a half-finished
   broad redesign. See "Slicing" in product-framing.md.
5. **Implement inside existing conventions.** Match style, naming, and structure;
   avoid unrelated refactors or formatting churn. Write the minimum code that solves
   the problem - see
   [references/implementation-discipline.md](references/implementation-discipline.md).
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
- Remove what your change orphaned; mention pre-existing dead code rather than deleting
  it. Every changed line should trace directly to the request.

## Code File Requirement

When creating or modifying **any** code file, include a clear introductory explanation
at the top of the file, written as a comment block in the target language's syntax
(e.g. `#` for Python/shell, `//` or `/* */` for C/C++/Java/JS, `<!-- -->` for HTML).
Place it before the main code content. It should briefly cover:

- **Purpose** - why the file exists.
- **What the code does** - its main behavior or responsibility.
- **Usage notes, dependencies, or assumptions** - how to run or import it, what it
  depends on, and any preconditions.

For existing files, add the explanation if it is missing, or update it if it is
incomplete or outdated. Keep it proportional - a few lines for a small module, more for
a complex one - and treat it as part of the diff to review so it never drifts from the
code.

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
- **Design docs/RFCs, estimation and spikes, feature flags and progressive rollout** ->
  [references/design-and-estimation.md](references/design-and-estimation.md)
- **Production incidents/outages, working safely in legacy code without tests** ->
  see the Incident Response and Legacy Code Without Tests sections in
  [references/engineering-playbook.md](references/engineering-playbook.md)
- **Reviewing someone else's change** -> see the Reviewing Someone Else's Change
  section in [references/risk-and-quality.md](references/risk-and-quality.md)

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

## Caveats

- This skill governs *how* to work, not *what* to build - pair it with
  domain skills (e.g. [[deep-learning]], [[hep-analysis]]) for specialized code.
- If the user explicitly says not to run tests or not to use TDD, follow that -
  user instructions take precedence over this workflow.
- Don't pad small fixes with the full template structure; collapse the completion
  summary to one or two sentences plus a verification line for trivial changes.
