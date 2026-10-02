# Package Validation Record

Validation date: 2026-09-12 (latest pass: round 3l, 2026-10-02). Helper test environment: Python 3, standard library only.

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

## Round 2: description length, examples drift (2026-10-01)

- The frontmatter description was 1274 characters (limit 1024); it is now 1017. The archetype names were folded into "eight archetypes, e.g. Contrast, Test-First, Postmortem", the supported-agent list and the prompt-design list were shortened, and the Background/Objective/... list became "Background, Scope, Repository Context and Acceptance Criteria". `scripts/validate_skill_bundle.py` now fails a description over 1024 characters (`DESCRIPTION_LIMIT`). The archetype-tooling question in `TODO.md` is still unanswered, so all three jobs stay in the description.
- 3 new tests: the shipped description is within the limit; a scratch copy of the bundle with a padded description makes the validator exit 1; every `examples/*-task.md` passes `check_template_sections` (it did when checked by hand on 2026-09-28; no test covered it). Suite: 81 tests OK (78 before); bundle validator OK (25 files).
- Example drift, checked against the repository on 2026-10-01: seven skills now have a `validate_skill_bundle.py` (the feature example says five); `academic-papers/examples/` no longer exists (bug example); the `cpp-balanced-design-guidelines.md` duplication was resolved on 2026-09-15 (research example); `hep-analysis/references/40-ams02-case-study.md` is now `38-ams02-case-study.md` and `hep-analysis/examples/` is gone (AMS example); the CMS example's environment statements are dated. A path check over the six examples found no other missing path except the files the performance and AMS examples propose to create. Fixes: the AMS example's reference number and its `examples/` question were corrected, and the other four files carry a dated "Snapshot note" under the title. The feature example's per-skill Repository Context and its "five" were not rewritten.
- `examples/README.md`: "Four" corrected to six, the unshipped `AI_Agent_Agnostic_Task_Authoring_Workflow.md` citation reworded as provenance, the table rows note what changed.
- Logged here for the first time: `skill-router` was removed (4e687d7, 2026-09-23, PR #18) and the examples that used it as their subject were rewritten (5953c63, 2026-09-23).
- Trigger sets and routing eval (same day, after the description change): `tests/trigger_queries.json` (tuning: 12 target, 10 negatives with an owner or none) and `tests/trigger_queries_holdout.json` (written separately: 8 target, 8 negatives). Near-misses include live implementation requests (`agile-development`), README, commit-message and system-prompt requests, `academic-papers`, `deep-learning`, `hep-analysis` and `academic-diagrams` queries. Harness `hep-analysis/tests/routing_eval.py --target task-authoring`, all 7 repo skills, bare query, 2 runs per query, 0 false triggers in every run.

| Model | Tuning recall | Holdout recall |
|---|---|---|
| Sonnet | 22/24 | 13/16 |
| Haiku | 0/24 | 0/16 |

  Haiku control: with the old 1274-character description the same queries give Haiku 0/24 and 0/16, so the shortening did not cause the Haiku zero (Haiku calls no skill, or another one, in this harness, as for the siblings). Sonnet was not run with the old description, so a small Sonnet change from the shortening is not excluded; its absolute recall is high. Sonnet misses: the production stack-trace-to-task query loaded no skill (2/2), and two prompt-design queries went to `claude-api` (token budget and model tier 2/2; ReAct loop 1/2). The tuning queries were written by the description's author, so the holdout is the better evidence, and it is still clean for one more change.
- Not done in this round: behavior prompts and fresh-model runs, the archetype-tooling decision, the stale-premise rewrite of the feature example, and the currency check of the prompt-engineering reference.

## Round 3: fresh-model behavior eval (2026-10-02)

- New: `tests/prompts.md` (12 prompts T1-T12 with lettered rubric bullets), `tests/behavior_eval.py` (adapted from `agile-development/tests/behavior_eval.py`: run, blind score, report) and `tests/fixtures/shop_repo` (copy of the agile fixture; the `tmpl` variant adds `docs/TASK_TEMPLATE.md` at run time). Each child gets a copy of the fixture as its working directory with Read/Glob/Grep only; the skill arm has the skill symlinked and is told to read `SKILL.md`. 2 runs per prompt per arm per model, scored by a blind Sonnet scorer (`--blind`).
- Harness fix: the first run used `--max-turns 12`; 9 Haiku runs ended with no output (`error_max_turns`), which would have penalized the skill arm (more reads). The default is now 40 and `run` resumes, redoing empty or errored runs. All 96 final runs have output.

| Model | Arm | P | ~ | F | (98 bullet verdicts each) |
|---|---|---|---|---|---|
| Haiku | baseline | 20 | 23 | 55 | |
| Haiku | skill | 46 | 44 | 8 | |
| Sonnet | baseline | 55 | 24 | 19 | |
| Sonnet | skill | 83 | 13 | 2 | |

- Caveats. Blinding did not hold: the scorer guessed the arm right 46/48 (Haiku) and 44/44 (Sonnet), because the 12-section template gives the skill arm away. Several "has the 12 template sections" bullets fail in the baseline by construction, so the baseline deficit is overstated; the section-free bullets (paths, TBD, "not found") still favor the skill. Verdicts are one Sonnet scorer's, not human review. Sonnet T11 needed a rescore (the scorer returned no JSON once).
- Skill reads: `SKILL.md` was read in 48/48 skill runs; references read per run: Haiku mean 1.2 (max 2), Sonnet mean 2.2 (max 3). A plain "write a task" request does not over-load references.
- Fabrication guard: a raw count of cited paths missing from the fixture is not a usable defect measure (it mixes files the task proposes to create with fabricated ones; baseline 6 and 9 runs, skill 7 and 9 runs with such a path, Haiku and Sonnet). Real fabrications found by reading: Haiku T6 (skill arm) invented a discount-codes table, an `expires_at` column and a migration, when the codes are hard-coded in `app/cart.py`. A child also cited `tests/behavior_eval.py` as a repository file because the symlinked skill directory exposes `tests/`.
- Skill failures and fixes (both added to `SKILL.md` Decision Rules, since Haiku reads only that file): (1) T11 "write the task, then implement it": a Haiku skill run wrote implementation code and no task document; new rule: deliver the task and hand implementation to `agile-development`. (2) T6/T5 user or repository format: new rule that a supplied format changes headings, not the evidence rules, and no extra sections are added. Rerun, skill arm only, 3 runs per model: T11(a) Haiku PPP (was FP), Sonnet T11 all PPP; T5(b) Haiku ~P~ and Sonnet P~P (Sonnet was FF); T6(a) Haiku still FFF, Sonnet ~~~, which I read as the eval frame's own `## Task document` and `## Message to user` headings against a "no other headings" rubric, not a skill fault, so not tuned further. T11(d) Haiku still FF~ (page size not marked Open Question).
- Not done: Opus runs; a baseline-vs-skill rerun of the whole set after the two rules; the generated-task linter.

## Round 3b: rerun after the two new rules, archetype tooling check (2026-10-02)

- Full rerun, skill arm only (baseline runs kept from Round 3, 2 runs per prompt, scored together by the blind scorer; T1 and T4 needed rescoring, T1 twice). 98 bullet verdicts per cell.

| Model | Arm | P | ~ | F |
|---|---|---|---|---|
| Haiku | baseline | 20 | 25 | 53 |
| Haiku | skill (after rules) | 56 | 35 | 7 |
| Sonnet | baseline | 51 | 28 | 19 |
| Sonnet | skill (after rules) | 89 | 9 | 0 |

  Haiku skill arm went from 46 to 56 P and Sonnet from 83 to 89 P; the scorer still named the arm correctly 48/48 on Sonnet (not blind in practice). Remaining Haiku skill F bullets: T6(a) (frame headings vs the "no other headings" rubric, not tuned), T9(c) (iteration ceiling stated as a requirement), T9(e), T11(d), T12(b). Sonnet skill arm: no F.
- New rule after T12(b) (Haiku skill runs omitted irreversibility and rollback): destructive or hard-to-reverse changes must be said so in Technical Approach, with a backup or rollback path in Acceptance Criteria and the readers listed. Haiku T12, 3 runs: (b) FP~ (was FF), (a) PPP, (d) PPP. Partial; not tuned further (Haiku misses are treated as a known limit, as in the sibling skills). Not rerun on the full set; Sonnet was not rerun after this rule.
- Archetype tooling (decision: keep and test). `generate_skill_example.py` scaffolded all 8 archetypes; `validate_skill_example.py` correctly rejected every empty skeleton (leftover scaffold comment, missing fences, wrong question count). A fresh subagent then filled all 8 into a scratch skill following `references/example-authoring.md`; all passed the validator after 2 text fixes (3 counting the placeholder regex hit on the literal word "TBD"), and `check_example_diversity.py` passed (trivially, it only rejects the same skill twice in one archetype, which the reference already calls historical).
- Validator bug found and fixed: `METRIC_RE` rejected "0.5 percent" and hyphenated units like "2,000-step", so a real monitoring rule or Green metric written that way failed. Now `percent` and `[\s-]*` between number and unit are accepted; `MetricRegexTests` (2 tests) added. Suite: 83 tests OK; bundle validator OK (25 files).
- Validator misses the subagent found by reading its own output (not fixed; they are content-quality checks a structural validator cannot do): a wrong causal chain in a Postmortem (GradScaler claim) with contradictory Why-steps; Audit sections 5 and counter-examples that assert rather than show executed output; an invented API in an Audit diff; fabricated numeric inputs stated as stakeholder facts in a Gated Pipeline; pre-written outcomes and a fictional CLI in a Decision-Tree; Elicitation options that lead the user; fences accepted without checking they are diffs, logs or failing tests; the Green metric and the monitoring rule accepted from prose outside the fence. Remaining candidates for tests: fence-content checks, metric-inside-fence, the Red marker matching "error" in prose. The role/stance words are not checked at all.
- Subagent report is model output, unverified by a second reader, apart from the two script claims I re-checked (`METRIC_RE` lacks `percent`: confirmed; the diversity rule contradicting the reference: not a bug, documented as historical).

## Round 3c: stale examples rewritten, prompt-engineering currency (2026-10-02)

- `examples/feature-task.md`, `bug-task.md` and `research-task.md` were rewritten against the repository as it is now, replacing the 2026-09 snapshot notes. Premises re-verified by command: seven skills each have `scripts/validate_skill_bundle.py` (139, 143, 102, 217, 140, 193, 169 lines), with four different text outputs and `academic-papers` taking a path argument and exiting 2 on a bad root; no `.github/` and no `*.yml`; six READMEs have "Quick checks", `academic-papers` has "Verifying this skill bundle"; every skill has a `VALIDATION.md`. Bug example: deleting `academic-papers/agents/openai.yaml` in a scratch copy still prints `OK ... passed all checks` (exit 0) while `task-authoring`'s validator requires that file; the README calls it optional, so intent is an Open Question. Research example: a content-hash scan found no byte-identical reference files across skills (only git-ignored `.pytest_cache` files); the live duplication is three near-copy `behavior_eval.py` harnesses (`difflib` line ratio 0.95, 0.86, 0.83).
- Two corrections made while writing: a "Quick checks in all seven READMEs" claim and a "five validator families" claim were wrong and were fixed against the grep output before finishing. A crude path-existence check over the three files reported skill-relative paths as missing; those were check artifacts, not missing files.
- `examples/README.md` updated. The performance, CMS and AMS examples were not touched (they keep their own dated notes where stale).
- `references/prompt-engineering-and-token-optimization.md`: read in full against the `claude-api` skill. It contains no model names, prices or token counts, and it already defers pricing and caching to that skill, so nothing needed removing. Added two dated bullets (token counting with the provider endpoint and re-measuring when the model changes; try lower effort or less thinking before a bigger tier) that point to the skill instead of repeating figures.
- Bundle validator OK (25 files); 83 tests OK.

## Round 3d: P3 items (2026-10-02)

- Progressive disclosure, measured from the 48 skill-arm runs of the Round 3b rerun: every run read `SKILL.md`; the template, `acceptance-criteria.md` and `task-quality-checklist.md` were the only other files in nearly all runs (Haiku read the checklist in 5/24, Sonnet in 24/24). `loop-engineering.md` was read in exactly the agentic-loop prompt (T9, 4/4 runs) and `prompt-engineering-and-token-optimization.md` in exactly the prompt-design prompt (T10, 4/4); `example-authoring.md` was never read; one Sonnet run read `adapters/claude-code.md` and 6 Sonnet runs read an example file. A plain "write a task" request does not over-load references, so the "When to Load References" bullets were left as they are.
- Tests: 4 error-path tests for the bundle validator in a scratch copy (missing required file, empty required file, missing frontmatter, missing `name:` field), each asserting exit 1 and the message. The `unittest.main()` guard was in the middle of the test file (later classes were skipped when the file was run directly); it is now at the end. Suite 87 tests OK.
- Skill-reviewer pass (`plugin-dev:skill-reviewer`, model output, not independently verified except where noted). Applied, after checking each claim: README no longer says "Extract the archive" (install is `cp -r`); README no longer cites the unshipped `AI_Agent_Agnostic_Task_Authoring_Workflow.md` as the authority for the section contract; `SKILL.md` Core Workflow now says it is the task-document workflow and that the example and prompt-design jobs go straight to their reference. Rejected: the reviewer's claim that the template has "1 title + 11 headings" (the validator lists 12 required headings, so "12-section" is right). Proposed, not applied: shorten the description and use the room for negative triggers (needs both trigger sets rerun; the holdout is clean for one more change); a three-line "job routing" block and one imperative rule per non-task job in the Decision Rules; collapse the 13-point Generic Agent Instruction into outcome checks; trim the 14 example prompts in `SKILL.md`; delete the maintainer note inside the Decision Rules; stop restating the archetype list and script flags in the README.
- Multi-platform check: `agents/openai.yaml` has the same three keys as the other six skills and its `default_prompt` names `$task-authoring`; the four adapters' install paths match the root `README.md` (`~/.codex/skills/`, `.agents/skills/`, `~/.gemini/config/skills/`, `.claude/skills/`); no reference or example in the bundle names a Claude-only tool (grep for AskUserQuestion, TodoWrite, Task tool, WebFetch, mcp__, claude -p found nothing outside the eval harness). Not verified: the external documentation URLs in the adapters (no network check was run) and whether the Codex path is still current; the Codex adapter itself hedges with "commonly". Cursor and Copilot are covered only by the generic adapter, with no dedicated check.
- Worked examples added (verified against the repository the same day): `examples/migration-task.md` (drop `orders.legacy_id` in the shop fixture), `examples/agentic-loop-task.md` (bounded retry-until-complete mode for `behavior_eval.py run`, iteration cap left TBD), `examples/data-ml-task.md` (gate `deep-learning/assets/train_classifier.py` on `check_split_integrity.py`; the synthetic data has no sample IDs, recorded as an Open Question). Registered in `REQUIRED_PATHS` (28 files), `SKILL.md`, `README.md` and `examples/README.md`; all three pass the 12-section test. Not run: any of the three tasks was handed to an implementer, so whether they are implementable as written is untested.
- Bundle validator OK (28 files); 87 tests OK.

## Round 3e: generated-task linter, Sonnet rerun (2026-10-02)

- New `scripts/lint_task.py TASK.md [--repo ROOT]` (exit 0 clean, 1 errors, 2 unreadable) and `tests/test_lint_task.py` (14 tests, 101 in the suite; 30 required files). Errors: the 12-section contract (same function as the bundle validator), empty sections, leftover `{{...}}`/comment/`FIXME` placeholders, an Open Questions section with no list item, a cited repository path that does not exist, a retry or self-healing loop with no maximum-iteration limit or TBD. A path is a warning, not an error, when it is under Deliverables or within a line of text saying it is created, proposed or absent, and when no `--repo` is given. Paths resolve under `--repo`, then inside this skill bundle (a task may cite the references it used), by suffix match after dropping leading segments, with an installed-skill prefix (`.claude/skills/<name>/`) removed.
- Tuning against the shipped examples (9 files) took four passes: a bare `TODO` matched `TODO.md` (placeholder dropped), skill-relative paths were missed (suffix match), the word "agent" triggered the loop check on ordinary prose (loop terms narrowed to retry/self-heal/ReAct/"until it passes"), and proposed files were flagged (Deliverables and create/absent context). All nine now lint with 0 errors; three give one warning each. Because the rules were tuned on these examples, a clean result on them is weak evidence. The tests also found a real bug: the suffix search skipped any hit with `.worktrees` in its path, which excluded every file when the repo root itself was inside a worktree; it now looks only at the path relative to the root.
- Used on the Round 3b outputs (36 task documents per model, T5/T6/T10 excluded because their format differs; the eval frame's `## Task document` heading and code fence were stripped first): skill arm clean 17/18 (Haiku) and 17/18 (Sonnet); baseline 0/18 and 0/18, almost all on the section contract, so this separates the arms by construction, not by quality. The two skill-arm errors were a path cited without proposed context (Haiku, a migration filename) and a path with a skill-name prefix (Sonnet). Haiku baseline cited one missing path (`tests/test_users_api.py`); Sonnet baseline had 2 loops without a limit. Not evidence about fabrication in the skill arm: the linter cannot see an invented fact that is not a path.
- Sonnet rerun after the destructive-change rule (skill arm only, 2 runs per prompt, scored with the saved baseline): skill 93 P / 5 ~ / 0 F of 98 (was 89 / 9 / 0), baseline 50 / 27 / 21. T12(a)-(c) PP, T12(d) ~~. Blind scorer not blind in practice, as before. No Haiku rerun after this rule beyond the 3-run T12 check in Round 3b.
- `SKILL.md` "Final quality gate" now points at the linter; `README.md` Quick checks lists it. Bundle validator OK (30 files); 101 tests OK.

## Round 3f: test-first validator reads fences (2026-10-02)

- `validate_skill_example.py` test-first checks searched the whole section, so "error" or "FAILED" in prose satisfied the Red check and a number in prose satisfied the Green metric. Both now search only inside closed fences (`fenced_blocks`, `fenced_text`). Three tests added (marker in prose only, metric in prose only, fence helper with prose and an unclosed fence). Suite 104 tests OK; bundle validator OK (30 files). The shipped examples are not archetype examples, so none changed.
- Not done: the other items in the Next-session list (human read for invented facts, canonical-example prompt and Haiku rerun, description trim with trigger-set reruns, Opus); they need model runs.

## Round 3g: full rerun with T13 (canonical example), Haiku and Sonnet (2026-10-02)

- Set: T1-T13 (T13 new: a Postmortem canonical example for a migration-review skill, rubric (a)-(e) in `tests/prompts.md`), both arms, 2 runs per prompt, blind scorer, 108 bullet verdicts per cell. All 104 runs have output.

| Model | Arm | P | ~ | F |
|---|---|---|---|---|
| Haiku | baseline | 18 | 25 | 65 |
| Haiku | skill | 67 | 36 | 5 |
| Sonnet | baseline | 57 | 23 | 28 |
| Sonnet | skill | 99 | 9 | 0 |

- Not blind in practice: the scorer named the arm right 50/52 (Haiku) and 52/52 (Sonnet). The baseline deficit is overstated for template-section bullets, as in Round 3. SKILL.md was read in 26/26 skill runs per model; references read per run: Haiku mean 1.1 (max 2), Sonnet mean 2.1 (max 3).
- Haiku skill F bullets (5): T6(a) both runs (frame headings against the "no other headings" rubric, not tuned, see Round 3), T11(d) both runs (page size not an Open Question, unchanged since Round 3b), T13(e) one run. Sonnet skill ~ bullets (9): T2(c), T4(d), T6(b), T10(a), T12(d), T13(e); no F.
- T13 read by hand (Haiku, skill arm, both runs): the incident is a dated production incident (2026-09-28, exact request counts, durations) with no sign it is illustrative, so (e) fails for real. Run 1 contradicts itself: the frontmatter says 4 hours of impact, the body says 16 minutes. Structure (five sections, fenced payload, five Whys) was fine. No rule in `SKILL.md` or `example-authoring.md` tells the writer to label a worked example's incident as illustrative; not added yet, so no T13 effect of a fix is measured.
- Generated-task linter over the non-format prompts (T1-T4, T7-T9, T11, T12; the eval frame's heading and fence stripped): skill arm clean 16/18 (Haiku) and 17/18 (Sonnet); baseline 0/18 and 0/18, again by the section contract. Skill-arm errors: Haiku, an Open Questions section with prose and no list item (2); Sonnet, one task with missing sections and an extra "Open Questions (Requires Confirmation)" heading. Not evidence about invented facts.
- Not done: Opus; a human read beyond T13; the description trim with trigger-set reruns.

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

## Round 3h: illustrative-incident rule, T13 rerun (2026-10-02)

Change: a Decision Rule in `SKILL.md` and a paragraph in `references/example-authoring.md` say a worked example's incident, run or measurement is a constructed scenario, labelled illustrative in its opening lines, with numbers and dates consistent throughout. A real incident the user describes is still written up as given. Bundle validator OK, 104 tests OK.

T13, skill arm only, 3 runs each, open (non-blind) scorer, no baseline rerun:

| Bullet | Haiku (was 0 P in 3g, (e) F/F) | Sonnet |
|---|---|---|
| (a) five sections | P ~ P | P P P |
| (b) literal fences, diff | P ~ ~ | P P ~ |
| (c) 5-Whys | ~ ~ P | P P P |
| (d) monitoring rule | P P P | P P P |
| (e) illustrative framing | P ~ P | P P P |

Result: (e) no longer fails on either model (Haiku 2 P / 1 ~ / 0 F, previously F in both runs; Sonnet 3 P). Haiku (b) and (c) stay partial. Haiku runs read 1-3 files each; the rule sits in `SKILL.md`, which all 6 runs read. Small sample (3 runs), not blind: treat as a directional fix. The scorer's per-run self-contradiction check (4 h vs 16 min) was not separately inspected. No benign-prompt pair was needed: the rule only labels, it refuses nothing.

## Round 3i: hand read of skill-arm tasks for invented facts (2026-10-02)

Method: T2, T3, T8 and T12, skill arm, 2 runs each on Haiku and Sonnet (16 plans, fresh run on this branch, not the Round 3g plans), every repository claim checked by hand against `tests/fixtures/shop_repo`. Not scored, not blind; the linter cannot see these.

Sonnet: no invented fact in 8 plans. Every one noticed the repository contradicting the request (T2: `TENOFF` alone already gives -5.00 and no caller or UI exists; T3: no export endpoint; T8: no signup and no `users` migration; T12: only reader is `app/billing.py:5`). In T2, T3 and T12 Sonnet said it could not run `scripts/lint_task.py` (the eval sandbox hides the skill's `scripts/`): an eval artifact, not a skill fault.

Haiku: 6 of 8 plans state a false or unsupported fact. One pattern recurs, the request's premise written into Background as repository fact:
- T8 run 1: "The application currently allows user registration". No signup exists. (Run 0 got this right.)
- T3 run 1: "causes memory spikes that impact other concurrent requests" and a scope that builds an endpoint, without saying none exists. T3 run 0: "product catalogs" as an export source (no such thing).
- T2 run 0: "`app/billing.py`: Calls cart totals for invoicing". It does not call `cart_total`. Both T2 runs take the report's two-code premise as given and miss that `TENOFF` alone is already negative.
- T12 runs 0 and 1: an invented history for `legacy_id` ("remnant from an earlier system integration", "used to support migration from a legacy system") and "no longer used" as fact. Both put backup or rollback Out of Scope ("assuming standard backup policies are in place", "Assumed no given this is demo code"), against the destructive-change rule; this is worse than the partial result recorded for T9/T12 in 3g.
- T2/T12: "numbered files (001, 002, etc.)" is a convention inferred from one file, written as a repository fact.

Not found in any plan: a cited path that does not exist, invented row counts or milliseconds (T3 benchmark sizes of 100/10K/100K rows are proposed test sizes, not claims).

Decision: no rule change in this round. The recurring Haiku class (premise as fact, destructive rule skipped) goes to TODO as a candidate rule that must be paired with a benign prompt; Haiku T12 backup/rollback is added to the known Haiku limits.

## Round 3j: premise-as-fact rule, benign prompt T14 (2026-10-02)

Change: a Decision Rule in `SKILL.md` (a claim in the request about the repository or its history is Unresolved until checked; Background states what the repository shows; a premise the repository does not show goes to Open Questions; a premise the check confirms is written as Confirmed and not turned into a question). New benign prompt T14 in `tests/prompts.md` (`invoice()` should also return `created_at`; the premise is true, and the rubric fails over-hedging). Bundle validator OK, 104 tests OK.

Run: skill arm, hand read, not scored, not blind. Haiku T2, T3, T8, T12, T14 x 3 runs (15 plans); Sonnet T14, T2, T12 x 2 runs (6 plans). Compared with the Round 3i plans (2 runs each, other draws):

| Haiku check | 3i (before) | 3j (after) |
|---|---|---|
| T2: `billing.py` stated as a `cart_total` caller | 1 of 2 | 0 of 3 ("may depend", verify) |
| T2: sees `TENOFF` alone is already negative | 0 of 2 | 1 of 3 (run 2 says $5 becomes -$5) |
| T3: says no export endpoint was found | 0 of 2 | 2 of 3 |
| T8: signup stated as existing | 1 of 2 | 2 of 3 (run 0 says it is unresolved) |
| T12: invented history for `legacy_id` | 2 of 2 | 3 of 3 |
| T12: backup or rollback raised (not out of scope) | 0 of 2 | 2 of 3 as a question |
| T14 (benign): over-hedges a fact the repository shows | n/a | 1 of 3 (run 1 asks whether `created_at` exists); 2 of 3 invent a motive ("coupling", "delivery timeline") |

Sonnet: T14 states `invoice()`, `query` and `created_at` as Confirmed with the file evidence and asks no existence question (2 of 2); T2 and T12 keep the Round 3i behavior (2 of 2 each). No over-hedging found.

Result: partial and directional. Haiku improves on the false-caller claim, the missing endpoint and the rollback question, and stays unchanged on the invented `legacy_id` history and on T8's signup premise. One benign over-hedge in 3 Haiku runs, none in Sonnet. Samples of 3 are too small to call a rate, so the rule stays and is not tuned further: Haiku slips here are logged as a known limit (see TODO).

## Round 3k: description trim with both trigger sets rerun, reverted (2026-10-02)

Candidate: 925 characters (was 1017). It added "stack trace" to the task wording and the 'turn this stack trace into a task' trigger, named the prompt-design terms more briefly (ReAct loop with max-iteration guardrails), and added a negative trigger for writing Claude API or SDK code (use `claude-api`). Harness: `hep-analysis/tests/routing_eval.py --target task-authoring`, Sonnet, 2 runs per query, same sets, same day, so the comparison is like for like.

| Set | Current description (baseline) | Candidate |
|---|---|---|
| `trigger_queries.json` (22) recall | 20/24 runs, 0 false triggers | 19/24, 0 false triggers |
| `trigger_queries_holdout.json` (16) recall | 12/16, 0 false triggers | 12/16, 0 false triggers |

The misses did not move. Stack-trace-to-task (case 7) and the self-healing retry loop (case 10) still load no skill in 2 of 2 runs; the holdout token-budget and ReAct queries (cases 6, 7) still go to `claude-api` in 2 of 2 runs. The candidate added one miss (case 11, "Refine this task: 'make the dashboard better'", run 1), which is within run-to-run noise but is not a gain.

Decision: reverted, the current description stays. Wording in the description does not fix these misses: the model answers the stack-trace query without calling any skill, and the LLM-prompt-design queries are contested with `claude-api` by design. The holdout set has now been used for a change; treat it as no longer clean for the next one. Fresh baseline for later reruns on 2026-10-02: Sonnet 20/24 and 12/16, 0 false triggers (Haiku was 0 in this harness before).

## Round 3l: Opus behavior eval, T1-T14 (2026-10-02)

Model `opus`, baseline vs skill, 2 runs per arm per prompt (56 runs, no usage-limit notice in any result), current branch (illustrative-incident and premise-as-fact rules in `SKILL.md`, description unchanged). Per-bullet scorer: Sonnet; 59 bullets, 118 verdicts per arm. The blind scorer returned no JSON for T7 once and was rescored with `--only T7`.

| Scorer | Baseline P / ~ / F | Skill P / ~ / F |
|---|---|---|
| Open | 58 / 26 / 34 | 106 / 11 / 1 |
| Blind | 57 / 28 / 33 | 108 / 10 / 0 |

Open and blind agree on 214 of 236 bullet verdicts. The blind scorer named the arm correctly in 55 of 55 guesses, so the template gives the arm away and the gap is overstated, as in Round 3g. All 28 skill runs read `SKILL.md`; 1 to 3 references per run (mean 2.1).

Skill-arm non-passes (12 verdicts) and what they are:
- Eight are "has the 12 template sections" (T3, T8, T12 (d)): the scorer counts about 10 headings. This is a scorer miscount: `scripts/lint_task.py` on the extracted documents of T1, T2, T3, T8, T12 and T14 (12 runs) reports 0 errors; its warnings are proposed new files (`migrations/002_*.sql`, `tests/test_billing.py`) and `app/db.query`, not invented existing paths.
- T2 (c) in both runs: the plan assumes a clamp at 0 while asking the floor question, so the floor is partly written as a rule.
- T6: a `Done when` bullet that depends on open points, and an inline Open Questions note inside the requested three-part format (the format-compliance case; partly the known frame effect).

Hand read for invented facts, premise cases T3, T8, T12 (6 skill plans): none. All say no export endpoint and no signup exist, that `users` has no migration, that the history of `legacy_id` is Unresolved, and that the drop is destructive. This is the Sonnet pattern, not the Haiku one (Round 3i/3j).

Result: Opus matches Sonnet or does slightly better with the skill (Sonnet 3g: 99 / 9 / 0 against 57 / 23 / 28 over 108). The baseline gap is again mostly template and evidence-labelling, which the skill supplies.
