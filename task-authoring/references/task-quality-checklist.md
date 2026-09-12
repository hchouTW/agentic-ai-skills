# Quality Checks

Before finalizing a generated task, verify:

```text
[ ] The relevant authoring reference was consulted.
[ ] The repository was inspected where repository access was available.
[ ] Project-specific claims are supported by evidence.
[ ] Assumptions are clearly identified.
[ ] Unresolved details are not fabricated.
[ ] The objective is explicit.
[ ] In-scope and out-of-scope work are defined.
[ ] Deliverables are concrete.
[ ] Acceptance criteria are measurable.
[ ] Validation steps are present when applicable.
[ ] Repository paths are verified.
[ ] The task can be understood by another agent without the original
    conversation.
```

If any critical check fails, revise the task before writing it - do not
write a task you know fails one of these checks and note it as a caveat
instead.

## Notes on Applying Each Check

- **The relevant authoring reference was consulted** - this means actually
  reading `templates/task-template.md` and, when the target repository
  defines its own authoring conventions, reading those too, not recalling
  the shape of a task from memory.
- **The repository was inspected where repository access was available** -
  when there is no repository (a purely conceptual request) this check is
  vacuously satisfied; when a repository exists, skipping inspection is a
  failure even if the resulting task "looks" plausible.
- **Project-specific claims are supported by evidence** - every path,
  module name, or existing tool named in Repository Context or Technical
  Approach traces back to something actually read, not a plausible guess.
- **Assumptions are clearly identified** - an Inferred conclusion reads as
  inferred (e.g. "likely uses X, based on Y"), never as a flat repository
  fact.
- **Unresolved details are not fabricated** - dataset versions, baselines,
  performance targets, required hardware, and similar unknowns are marked
  `TBD` / `Open Question` / `Requires Confirmation`, not invented with a
  plausible-sounding value.
- **The task can be understood by another agent without the original
  conversation** - this is the overall bar: hand the finished Markdown to a
  different agent or a human who wasn't in the conversation, and check
  whether they'd need to ask a question the task should have already
  answered.
