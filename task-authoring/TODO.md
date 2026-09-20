# TODO for future Claude sessions (task-authoring)

State at 2026-09-21: skill is on `main`; `python3 -m unittest discover -s tests` (78 tests) and
`python3 scripts/validate_skill_bundle.py` (25 files, 12-section template contract) pass. Verification so far is
structural (validators, link checks) plus one RED/GREEN fresh-subagent run for `loop-engineering.md`
(see `VALIDATION.md`). The rest of the skill (core task authoring, the 8 archetypes, the prompt-engineering
reference) has never been tested on a fresh model. Read `VALIDATION.md` first, then this file.

Working rules: work on a branch, run the tests and the validator before committing, keep `SKILL.md`, `README.md`,
`scripts/validate_skill_bundle.py` `REQUIRED_PATHS` and `agents/openai.yaml` in sync, and ask before pushing or
merging. The template's 12-section contract (`REQUIRED_TEMPLATE_SECTIONS`) is exact: do not add or remove a section
without saying so and updating the validator, tests, and all `examples/` together. Record every result (including
negative ones) in `VALIDATION.md`. Use `superpowers:writing-skills` (RED-GREEN with fresh, context-free subagents)
and `skill-creator` for behavior tests, not just unit tests.

## P1 - test that the skill actually changes model behavior
Only the loop-engineering path has a baseline-vs-skill run. Everything else is unproven.
- [ ] Write 12-15 realistic prompts in `tests/prompts.md`, each with expected behaviors (which reference is read,
      which rule fires). Cover: a bare one-line feature request; a bug report pasted verbatim; a performance request
      with no baseline (baseline/target must be TBD, not invented); a research/investigation request; a request in a
      repo that has its own task template (must follow the repo's, per the Core Workflow); a user-supplied format
      (user format wins); a request naming a file/module that does not exist (must say "not found", not cite it);
      a request with an inferable-but-unconfirmed detail (must be labelled Inferred); an agentic retry loop
      (iteration cap must be TBD if not given); a canonical-example request for each of 2-3 archetypes; a prompt-budget
      request; and a "now implement it" request (must hand off to `agile-development`, not implement).
- [ ] Run each prompt in a fresh subagent with and without the skill; compare against expectations; log pass/fail in
      `VALIDATION.md`. Repeat with Haiku (weaker) and Opus if possible. Fix `SKILL.md` where the skill did not help.
- [ ] Check the fabrication guard specifically: over 5+ runs, count invented paths, thresholds, dataset versions,
      or "Confirmed" labels on things that are only inferred. Any hit is a skill bug; tighten the wording.
- [ ] Check that generated tasks pass `references/task-quality-checklist.md` and the 12-section contract; consider a
      small script that lints a generated task (sections in order, non-empty Open Questions, every cited path exists).
- [ ] Trigger test for the frontmatter `description`: 20 should-trigger and 20 should-not-trigger queries. Include
      near-misses: ad-hoc scoping inside an active implementation chat (should stay with `agile-development`),
      "write a README", "write a commit message", generic "write a prompt" with no LLM-call design, and
      `academic-papers` drafting. Consider `skill-creator` description optimization; the description is ~1170 chars,
      so keep it from growing.
- [ ] Routing hygiene with sibling skills: `agile-development` vs `task-authoring` (live scoping vs a standalone
      written spec), and `skill-router`. Confirm the router's `task-authoring` bullet and `SKILL.md` description
      still match; run `skill-router`'s validator and tests after any description change.

## P2 - verify the shipped examples and archetype tooling
- [ ] Re-verify every Repository Context claim in `examples/*.md` against the current repo (paths, line counts,
      counts like "five times", "byte-identical duplication", "confirmed absent" tools). The repo has changed a lot
      since 2026-09-12 (new skills, moved files), so some claims may be stale. Fix or date them.
- [ ] `examples/README.md` says "Four worked Task Markdown outputs" but lists six, and still cites the unshipped
      `AI_Agent_Agnostic_Task_Authoring_Workflow.md` as a source. Fix the wording and reword the citation as
      provenance (the 2026-09-12 optimization pass did this for `performance-task.md` only).
- [ ] Run `check_template_sections` (the validator's function) over every file in `examples/`, not only the template,
      and add a test that does so if none exists.
- [ ] Generate one example per archetype (8) with `scripts/generate_skill_example.py`, then run
      `scripts/validate_skill_example.py` on each. Note where the generator's output needed manual fixing and where the
      validator missed a real defect. Add regression tests for what it missed.
- [ ] Try `scripts/generate_skill_example.py` / `validate_skill_example.py` on a skill that is not `agile-development`
      (for example `deep-learning` or `hep-analysis`, whose existing `examples/` follow the archetype rules) to
      confirm the cross-skill claim in `references/example-authoring.md` holds. Report any agile-specific assumptions.
- [ ] Decide on `scripts/check_example_diversity.py`: it is documented as retained-but-historical. Either run it on the
      current repo's examples and record the result, or remove it (then update `README.md`, `example-authoring.md`,
      `REQUIRED_PATHS`, and tests).
- [ ] Check all snippets and commands in `references/` (`prompt-engineering-and-token-optimization.md` token math,
      model names/tiers, pricing claims) for currency. Model IDs and prices go stale; use the `claude-api` skill as
      the source, and mark anything time-sensitive with a date or remove it.

## P3 - improve content and structure
- [ ] Progressive disclosure: `references/example-authoring.md` is ~335 lines and was flagged for a split only if a
      9th archetype is added. Measure how many references a typical task-authoring run actually loads; add
      "read only if" hints where a "When to Load References" bullet is vague.
- [ ] The skill covers three loosely related jobs (task docs, canonical examples, prompt design). Assess whether a
      fresh model over-loads references for a plain "write a task" request; if so, tighten the routing bullets.
- [ ] Add a worked example for a category with none today: a refactor/migration task, a data/ML task (ties to
      `deep-learning`), and an agentic-loop task (the loop-engineering path has a guide but no shipped example).
- [ ] Add tests for uncovered behavior: a generated-task linter (if built above), error paths of
      `validate_skill_bundle.py` (missing file, empty file, bad frontmatter), and the CLI exit codes.
- [ ] Multi-platform check (Codex, Antigravity, Cursor, Copilot): confirm `agents/openai.yaml` is current, that
      `references/adapters/*.md` install paths and invocation notes are still right, and that no instruction depends
      on Claude-only tools. Antigravity has format constraints; see the repo's multi-platform conventions and memory.
- [ ] Skill-doctor / skill-reviewer pass on `SKILL.md` and `README.md` (`plugin-dev:skill-reviewer`).

## P4 - housekeeping and decisions
- [ ] Update `VALIDATION.md` header date ("Validation date: 2026-09-12") and the file/test counts after each pass.
- [ ] Remove stray `scripts/__pycache__` and `tests/__pycache__` from the working tree if not ignored
      (`.gitignore` already lists `__pycache__/`, so just confirm they are untracked).
- [ ] Ask the user: which task consumers matter most (Claude Code, Codex, human engineers)? This sets which
      adapters and which P1 prompts to prioritise.
- [ ] Ask the user whether the 12-section template should stay fixed or gain an optional "Risks" / "Rollout" section
      (that would change the validator, tests, and every example).
