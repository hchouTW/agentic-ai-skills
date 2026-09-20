# Fresh-model behavior prompts for agile-development

Each prompt is run in a fresh subagent twice: once as a baseline (no skill) and once with `agile-development`
available. Score each expected behavior pass/fail; log results in `VALIDATION.md`. Give the subagent a small scratch
repo or a described repo context where the prompt needs one. "Reads" lists the reference the skill should send the
model to (a signal, not a hard requirement).

| # | Prompt | Reads | Expected behaviors (pass = all) |
|---|--------|-------|---------------------------------|
| 1 | "Users say the cart total is wrong sometimes. Fix it." | engineering-playbook (bug fix) | Reproduces or locates the failing case before editing; adds a regression test; smallest fix; no unrelated refactor; reports what was actually run. |
| 2 | "Add an endpoint for exports." (no format, auth, or size given) | implementation-discipline | Names the competing interpretations; asks only about the costly-to-reverse parts (published contract, auth); does not silently pick one. |
| 3 | "Rename the button label from Save to Submit." | implementation-discipline | States a one-line assumption if needed and proceeds; does not ask a string of questions; does not pad with the full template. |
| 4 | "Drop the `legacy_id` column from `orders`." | risk-and-quality, engineering-playbook (migration) | Flags irreversibility; proposes expand/contract or backup + rollback; checks readers of the column; asks or gates before running anything destructive. |
| 5 | "Bump `requests` from 2.28 to 2.32 and make sure nothing breaks." | engineering-playbook (dependency) | Reads the changelog for breaking changes; runs the test suite before and after; reports only what passed. |
| 6 | "Review my diff before I open a PR." (diff with an unrelated formatting change and a missing test) | risk-and-quality (reviewing) | Flags scope creep and the missing test; separates blocking from optional comments; cites lines. |
| 7 | "Prod checkout has been failing since the 14:00 deploy. Help." | engineering-playbook (incident) | Mitigate first (rollback / flag off), diagnose second; states what is known vs. guessed; offers a blameless postmortem outline afterwards. |
| 8 | "Change this 400-line function with no tests so it also handles refunds." | engineering-playbook (legacy) | Adds characterization tests before changing behavior; makes the change in small steps; does not rewrite the function. |
| 9 | "Is this overcomplicated?" (a factory + registry for one caller) | implementation-discipline | Says yes with specifics; proposes the minimal version; does not lecture on patterns. |
| 10 | "Should we split billing into its own service?" | software-architecture | Frames boundaries, data ownership and dependency direction; lists trade-offs; proposes an ADR; no code. |
| 11 | "How long will adding SSO take?" | design-and-estimation | Gives a range with assumptions and unknowns; suggests a time-boxed spike for the biggest unknown. |
| 12 | "Ship the new pricing page to 5% of users first." | design-and-estimation | Feature flag, exposure plan, metrics to watch, kill switch/rollback trigger. |
| 13 | "Fix the typo 'recieve' in README.md." | (none) | One-line fix and one-line report; no story card, no risk table. |
| 14 | "Add the retry logic, but do not run tests, I'll do it." | validation-and-done | Follows the user (no tests run); says plainly that nothing was verified; does not claim it works. |
| 15 | "Write a script that dedupes lines in a file." | SKILL.md (Code File Requirement) | New file starts with a Purpose / What it does / Usage-assumptions comment block; minimal code, no speculative options. |

## Trigger test (description)

Run each query with only the frontmatter descriptions visible (all installed skills) and record whether
`agile-development` is chosen. 20 should-trigger, 20 should-not-trigger.

Should trigger (write 20; examples): "add pagination to the users API", "fix this flaky checkout bug", "migrate
this table to a new schema", "is this over-engineered?", "write the postmortem for last night's outage".

Should not trigger (write 20; examples): "explain Python decorators", "write a PyTorch training loop"
(-> `deep-learning`), "draft a ticket for the SSO work" (-> `task-authoring`), "fit this histogram in ROOT"
(-> `hep-analysis`), "what does this regex do?".
