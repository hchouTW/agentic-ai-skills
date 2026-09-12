# Package Validation Record

Validation date: 2026-09-12. Helper test environment: Python 3, standard library only.

## Initial build (2026-09-12)

First delivery of `task-authoring`, implementing
`~/Downloads/AI_Agent_Agnostic_Task_Authoring_Workflow.md` as a skill bundle
matching this repository's sibling-skill convention (`SKILL.md`, `README.md`,
`VALIDATION.md`, `references/`, `templates/`, `examples/`, `scripts/`,
`tests/`, `agents/openai.yaml`).

- `scripts/validate_skill_bundle.py` was added, adapting
  `agile-development/scripts/validate_skill_bundle.py`'s file-presence/
  frontmatter/README-section checks and adding one check specific to this
  skill: `templates/task-template.md` must carry exactly the section
  contract from the source document's "Task Generation Requirements" (one
  top-level title, then Background / Objective / Scope / In Scope / Out of
  Scope / Repository Context / Technical Approach / Deliverables /
  Acceptance Criteria / Validation / Open Questions / References, in order)
  - no more, no fewer.
- `tests/test_task_authoring_skill.py` was added (standard library only,
  `python3 -m unittest discover -s tests -v`):
  - `extract_headings` was checked against a synthetic multi-level heading
    string and against a non-heading `#hashtag` line that must not be
    mistaken for a heading.
  - `check_template_sections` was checked against the actual shipped
    `templates/task-template.md`, a synthetic valid template, a template
    missing one required section, one with an unexpected extra section, one
    with two required sections swapped out of order, one with no top-level
    title, and one with two top-level titles.
  - The CLI was run end to end against the real shipped bundle (passes),
    against a scratch copy with a doctored `README.md` missing every
    required section (fails with the expected message), and against a
    scratch copy with a `templates/task-template.md` missing the
    `## Validation` section (fails with "section contract violated" and
    names the missing section).
- `python3 scripts/validate_skill_bundle.py` was run from
  `task-authoring/` and reports all 18 expected files present and non-empty,
  plus a clean pass of the template section-contract check.
- `python3 -m unittest discover -s tests -v` was run from `task-authoring/`
  and all tests pass.
- Every relative Markdown link in `SKILL.md` and `README.md` was checked
  against the file it names; all resolve.
- `SKILL.md`'s Core Workflow section was checked line-by-line against
  `AI_Agent_Agnostic_Task_Authoring_Workflow.md`'s "Required Agent Behavior"
  Steps 1-5 and its Confirmed/Inferred/Unresolved definitions: all five
  steps are present in order, none invented, and the three evidence
  categories keep their source definitions and examples (dataset version,
  production campaign, performance target, reference baseline, required
  hardware, expected threshold; `TBD` / `Open Question` / `Requires
  Confirmation`). The 13-point "Generic Agent Instruction" was checked the
  same way and reproduced verbatim as a numbered list.
- Each file under `references/adapters/` was reviewed to confirm it is
  discovery-only (install location, invocation mechanism, metadata file) and
  contains no restatement of the Core Workflow, the evidence model, or the
  template's section contract.
- Each of the four `examples/*.md` files was checked against
  `templates/task-template.md`'s exact section list (same check the bundle
  validator performs on the template itself) and confirmed to have a
  non-trivial Open Questions section - none left empty or filled with a
  placeholder.
- The "Expected User Experience" scenario from the source document
  ("Create a task for RICH reconstruction performance analysis") was
  hand-run against this same repository, per this task's own Validation
  requirement: `examples/performance-task.md` is that run's output. It cites
  only repository paths actually verified to exist (`hep-analysis/`), and it
  explicitly documents - rather than invents - that no RICH reconstruction
  pipeline, dataset, or baseline exists anywhere in this repository, marking
  the dataset, baseline, and target repository itself as Unresolved /
  Requires Confirmation.

No defects were found in this pass; the main design risk (a hand-maintained
template file silently drifting from the section contract acceptance
criteria depend on) is covered by `check_template_sections` and its CLI
regression test above.

## Absorb example-authoring and prompt-engineering-and-token-optimization from agile-development (2026-09-12)

Received `references/example-authoring.md`, `references/prompt-engineering-and-token-optimization.md`, and their tooling (`scripts/generate_skill_example.py`, `scripts/validate_skill_example.py`, `scripts/check_example_diversity.py`, `tests/test_example_authoring.py`) from `agile-development`, consolidating the repo's cross-skill "author a canonical worked example" / "design or budget a prompt" capability here instead of inside a single domain skill.

Fixed the two files' internal `agile-development`-specific assumptions rather than moving them verbatim: `example-authoring.md`'s "Cross-skill use" section and its own self-reference now name `task-authoring`; `prompt-engineering-and-token-optimization.md`'s "Extending the User Story Template" section now explicitly cross-links `agile-development`'s `assets/story-card.md` (that asset still lives there, not here, so the section notes it requires `agile-development` installed alongside this skill), and its Validation section's "this skill's Decision Rules" now names `agile-development` explicitly instead of referring to itself.

Updated `SKILL.md` (frontmatter description, two new "When to Load References" bullets, the 8 archetype-authoring example prompts plus one prompt-engineering prompt moved into "Example Prompts This Skill Handles Well"), `README.md` (Quick checks commands, Coverage and boundaries paragraphs, Example prompts), and `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` (added the 6 moved files, 18 -> 24).

Updated every other skill's cross-link to the old `agile-development/references/example-authoring.md` path: `academic-papers`, `deep-learning`, and `hep-analysis`'s `SKILL.md` and `examples/README.md`, `skill-router`'s `examples/README.md`, and the root `README.md`'s "examples/ worked examples" section - all now point at `task-authoring`. Trimmed `skill-router/SKILL.md`'s `agile-development` routing-rule bullet, which had described this capability, and added a note that it is a `task-authoring` capability not routed through that table (consistent with `task-authoring` remaining outside `skill-router`'s routing table, per this file's earlier Limitations entry).

Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 24 files present and non-empty, templates/task-template.md carries all 12 required sections in order") and `python3 -m unittest discover -s tests -v` (78 tests, all passing) here. Also re-ran each other touched skill's own `scripts/validate_skill_bundle.py` and `python3 -m unittest discover -s tests -v` to confirm the move introduced no regressions elsewhere: `agile-development` (48 files, 32 tests), `academic-papers` (27 tests), `deep-learning` (87 files, 106 tests), `hep-analysis` (119 files, 172 tests), `skill-router` (31 files, 7 tests) - all passing.

## Add loop engineering and autonomous iteration guidance (2026-09-12)

Added `references/loop-engineering.md`: when the work under authoring is an
agentic, autonomous, or iterative system, it requires naming the closed-loop
pattern (ReAct Thought-Action-Observation, or Plan-and-Solve), specifying
self-healing error-feedback handling (named failure classes fed back into
the next attempt, retryable vs. fatal), and fixing mandatory guardrails
(explicit termination condition, maximum-iteration limit, early stopping
distinct from it) - never inventing an iteration ceiling the requester
didn't give.

`templates/task-template.md`'s section contract (`REQUIRED_TEMPLATE_SECTIONS`
in `scripts/validate_skill_bundle.py`) is fixed and exact - no section was
added. The new guidance instead extends the existing HTML-comment guidance
inside Technical Approach, Acceptance Criteria, and Validation, and
`references/loop-engineering.md` carries a table mapping each requirement to
the section it belongs in.

Also updated: `SKILL.md` (frontmatter description, a new "When to Load
References" bullet, a new Decision Rule, a Caveats clarification that
authoring the spec for such a loop is in scope even though building the
agent itself is not, and a new worked example prompt), `references/
acceptance-criteria.md` (a new "Iteration and Loop Guardrails" section with
worked avoid/prefer examples), `references/task-quality-checklist.md` (a new
conditional checklist item, vacuously satisfied when the work isn't
iterative), `references/prompt-engineering-and-token-optimization.md` (cross-
references clarifying that file governs each call's cost while
`loop-engineering.md` governs the loop's shape and stopping conditions, plus
a note on bounding an open-ended loop's total cost via the maximum-iteration
limit), `README.md` (a new Coverage-and-boundaries paragraph and example
prompt), and `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` (added
`references/loop-engineering.md`, 24 -> 25).

Followed `superpowers:writing-skills`' RED-GREEN cycle using fresh,
context-free subagents rather than unit tests, since this is a coverage gap
in a reference/technique skill (what the generated task specifies) rather
than a discipline rule an agent might rationalize around under pressure:

- **RED (baseline, before this change)**: asked a fresh subagent to author a
  task via this skill for "an autonomous log-triage agent" that retries a
  flaky log-search API and refines its query until it finds a root cause.
  The unmodified skill produced a plausible loop description in Technical
  Approach, but pushed every stopping-related concern - termination
  condition, maximum-iteration limit, early stopping, and the specific
  error-feedback mechanism - into Open Questions with no requirement to
  state a fallback behavior; none of the three loaded references (`template.md`,
  `acceptance-criteria.md`, `task-quality-checklist.md`) mentioned iteration
  loops or guardrails at all.
- **GREEN (after this change)**: re-ran the identical request against the
  updated skill with a second fresh subagent. The generated task now names
  the ReAct pattern explicitly, distinguishes retryable (malformed JSON,
  timeout) from fatal (auth failure, permanently invalid query) failures
  with the error fed into the next attempt, states an explicit termination
  condition (the root-cause goal-check passing), marks the maximum-iteration
  limit as an Open Question rather than inventing a number (correct per the
  Confirmed/Inferred/Unresolved evidence model), and states an early-stopping
  condition (repeated identical observation, or no new evidence across N
  iterations) distinct from the iteration cap. All four loaded references
  (now including `loop-engineering.md`) covered iteration/guardrail content.
- `python3 -m unittest discover -s tests -v` (78 tests) and
  `python3 scripts/validate_skill_bundle.py` were re-run after the edits:
  both pass, with the validator now reporting 25 required files present and
  the template's 12-section contract still exact.
- Every new relative Markdown link (`SKILL.md`, `README.md`, and the four
  edited/added reference files) was checked programmatically against the
  file it names; all resolve.

## Optimization pass (2026-09-12)

Audited the full bundle for token efficiency, redundancy, and consistency
(SKILL.md's discovery-optimization rules: description = when-to-use only,
single source of truth per rule, no dead cross-references). Fixes:

- `SKILL.md`'s frontmatter description dropped the "the core authoring
  rules below are vendor-neutral; per-agent discovery notes live only in
  references/adapters/ and never duplicate them" clause (1310 -> 1172
  chars). That's internal file-organization detail, not a triggering
  condition, and it already lives - stated once - in the "When to Load
  References" section's adapters bullet; keeping it in both places was
  duplication with no discovery benefit.
- `references/prompt-engineering-and-token-optimization.md` had four
  unattributed mentions of `risk-and-quality.md` and one of
  `software-architecture.md`, both of which live in `agile-development/
  references/`, not this skill. Every other cross-skill reference in the
  same file names its owning skill (`agile-development`'s
  `assets/story-card.md`, the `claude-api` skill); these five didn't,
  inconsistent with the file's own pattern. Prefixed all five with
  `` `agile-development`'s ``.
- `examples/performance-task.md`'s References section cited
  `AI_Agent_Agnostic_Task_Authoring_Workflow.md` as if it were a resolvable
  repository path - it's the original, unshipped source document that this
  package's `templates/task-template.md` was built from, and citing it as
  a repository reference violates this skill's own "only cite repository
  paths that were actually verified to exist" rule (`SKILL.md`'s Decision
  Rules). Reworded to describe it as provenance rather than a citable path.
- `VALIDATION.md`'s own "24 -&gt; 25" entry above used an HTML entity
  (`-&gt;`) where every other count-delta in this file uses a plain `->`;
  normalized for consistency.

Considered and left unchanged:

- `scripts/check_example_diversity.py` is explicitly documented in three
  places (`README.md`, `references/example-authoring.md` x2) as retained
  for reference but historical, not run as a gate on new example batches.
  It is still fully tested and internally consistent with its own
  documentation - a deliberate prior decision, not an oversight - so it was
  left in place rather than removed as part of this pass.
- `references/example-authoring.md` (2798 words) is the largest file in the
  bundle by a wide margin. It is loaded on demand, not on every trigger, so
  the cost concern is lower; flagged for a future split (per-archetype
  format specs into their own file) only if a 9th archetype is added, not
  acted on now.

Re-ran `python3 scripts/validate_skill_bundle.py` (25 files, template
contract intact) and `python3 -m unittest discover -s tests -v` (78 tests)
after every edit in this section: both pass throughout.

## Limitations

- `SKILL.md`/`references/*.md` are process guidance for an LLM to follow,
  not independently executable code - verified for internal consistency
  (cross-links resolve, terminology matches the source document) rather than
  run, matching the verification approach documented in the sibling skills'
  own `VALIDATION.md` Limitations sections.
- The four `examples/*.md` files were authored by hand against this
  repository's actually-verified state (confirmed real paths, a confirmed
  real regex, a confirmed real file duplication) rather than generated by
  running this skill end-to-end through an external agent harness; the RICH
  scenario was cross-checked against the source document's own worked
  example as described above.
- No integration with `skill-router`'s routing table was made - see this
  task's Open Questions; `task-authoring` is not currently discoverable
  through `skill-router`'s automatic triage.
