# task-authoring Examples

Four worked Task Markdown outputs, one per category named in
`AI_Agent_Agnostic_Task_Authoring_Workflow.md`, each following
[../templates/task-template.md](../templates/task-template.md) exactly and
each demonstrating the Confirmed / Inferred / Unresolved distinction from
`SKILL.md`'s Core Workflow with a non-trivial Open Questions section - none
of them mark an unknown as resolved just to look complete.

All four target this repository (`agentic-ai-skills`) itself as the
inspected repository, so every Repository Context claim in them is a real,
verified fact about this repository rather than an invented one.

| Example | Category | Scenario | Open Questions highlight |
|---|---|---|---|
| [feature-task.md](feature-task.md) | Feature | Adding a `--format json` output mode to every skill's `validate_skill_bundle.py` | Whether the JSON shape should be factored into one shared module instead of duplicated five times, and whether there's a concrete consumer for it yet |
| [bug-task.md](bug-task.md) | Bug | `skill-router`'s routing-table regex only matches lowercase-kebab bullet names, silently under-counting anything else | Whether lowercase-kebab should become a documented, enforced convention or the extractor should tolerate other casing |
| [performance-task.md](performance-task.md) | Performance | "Create a task for RICH reconstruction performance analysis" - the authoring reference's own worked example, run against this repository | This repository has no RICH reconstruction code, dataset, or baseline at all - nearly every implementation detail is marked Unresolved rather than invented |
| [research-task.md](research-task.md) | Research | Investigating whether `cpp-balanced-design-guidelines.md`'s confirmed byte-identical duplication across two skills should be deduplicated | Whether any other duplicated reference file exists beyond the one already found, and whether a fix may break the single-folder `cp -r` installation model |

Two further examples target `hep-analysis` domain requests specifically -
still Task Markdown outputs against this same repository, but chosen to
contrast a request the repository genuinely cannot fulfill (no CMS analysis
code or data exists here) against one it already has real, working building
blocks for (the AMS-02 scripts and their tests):

| Example | Category | Scenario | Open Questions highlight |
|---|---|---|---|
| [cms-higgs-analysis-task.md](cms-higgs-analysis-task.md) | Research | "Create a task for a CMS experiment Higgs boson analysis" - this repository has no CMS dataset, MC, or channel-specific code, only generic Combine/pyhf templates and likelihood/inference guidance | Which Higgs channel to target, and whether `pyhf`/ROOT/Combine are expected to be installed in the execution environment (confirmed absent/broken in the one checked here) |
| [ams-antiproton-analysis-task.md](ams-antiproton-analysis-task.md) | Feature | Composing the five existing, individually-tested AMS-02 building-block scripts into one antiproton/proton-ratio worked pipeline - fully completable in this repository, unlike the RICH and CMS-Higgs examples above | Whether `--demodulate` support, a new `scripts/pipelines/` layout, and a matching `hep-analysis/examples/` entry are wanted alongside the script |
