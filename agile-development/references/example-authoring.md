# Authoring a Canonical Skill Example

How to produce a `<skill>/examples/` entry: a worked contrast between a weak
approach and an expert one, for a realistic scenario in that skill's domain. Use
this when asked to "author," "generate," or "add a canonical example" for
`agile-development` itself or for another installed skill.

## The generation prompt

This is the reusable core - the literal template, with its blanks bound to
concrete values before running it:

```
Act as a senior {role} to create a standard example for `{skill}/examples/` in the
`{skill}` skill. Using a realistic {domain_use_case}, draft a complete,
production-ready artifact with zero placeholders. Format the artifact as a direct
contrast between a "Common Weak Approach" and an "Expert-Level Best Practice",
followed by {n} key takeaways explaining the architectural difference.
```

- `{role}` - a specific seniority + specialty (e.g. "Staff Software Engineer",
  "Senior Experimental Particle Physicist"), not a generic "expert."
- `{skill}` - the target skill's folder name (e.g. `hep-analysis`).
- `{domain_use_case}` - a concrete, narrow scenario grounded in that skill's own
  reference material, not an invented or generic one.
- `{n}` - the number of key takeaways; default 4, minimum 3, maximum 6.

This step is content generation, not something a stdlib script can do correctly
for physics or ML domain content - domain correctness needs an agent reasoning
through the example with the target skill's own `references/` loaded, the way a
person would. The scaffold and validator scripts below only produce and check
structure; they do not write or judge the domain content itself.

## Workflow

1. **Scaffold.** Run `scripts/generate_skill_example.py` with `--skill`, `--role`,
   `--use-case`, and `--takeaways` to emit an empty skeleton with the right
   frontmatter and section headers at the right path - mirrors how
   `create_story_card.py` scaffolds a story card without inventing the story.
2. **Fill.** Replace every skeleton placeholder with real content: a concrete
   scenario, a complete weak-approach artifact, a complete expert-approach
   artifact, and the takeaways explaining the architectural difference between
   them. Zero placeholders (see below).
3. **Validate.** Run `scripts/validate_skill_example.py <file>` - it mechanically
   rejects structural defects and placeholder content, but it cannot judge domain
   correctness (see Correctness review below).
4. **Index.** Add or update `<skill>/examples/README.md`, a one-row-per-example
   table: `Example | Domain Use Case | Contrast in one line`.
5. **Wire it up.** If this is the first example for that skill, add
   `examples/README.md` and the new example file to that skill's own
   `scripts/validate_skill_bundle.py` `REQUIRED_PATHS` (or, for a skill whose
   validator checks orphaned files by scanning `references/`/`scripts/`/`assets/`
   only, no change is needed there - confirm which kind the target skill has
   before assuming). Log the pass in that skill's `VALIDATION.md`.

## Format specification

- **File location:** `<skill>/examples/<NN>-<slug>.md` - a two-digit prefix for
  stable ordering (the convention `hep-analysis` already uses for its
  `references/`), plus one `<skill>/examples/README.md` index.
- **Required sections, in order:**
  - `## Scenario` - the realistic domain use case, 2-4 sentences.
  - `## Common Weak Approach` - a complete artifact showing the failure mode, not
    a caricature.
  - `## Expert-Level Best Practice` - a complete artifact solving the same
    scenario correctly.
  - `## Key Takeaways` - a bulleted list, default 4 items, minimum 3, maximum 6,
    each explaining *why* the expert approach differs architecturally, not just
    restating what changed.
- **Zero-placeholder rule.** No `TODO`, `TBD`, `XXX`, `FIXME`, `Lorem ipsum`,
  bracketed stand-ins like `[Your ...]` or `[insert ...]`, or a trailing `...`
  where real content belongs. Every code fence must be complete and
  runnable/compilable as shown, not an illustrative fragment.
- **Frontmatter.** A one-line YAML-ish header at the top of each example file so
  the validator and index generator can read it back without re-parsing prose:

  ```
  role: Staff Software Engineer
  skill: agile-development
  use_case: One-line description of the scenario
  ```

- **Language.** English, matching this repository's rule that all maintained
  instructions, templates, and metadata are in English.

## Correctness review

The validator enforces structure and rejects placeholders; it cannot verify that
a `hep-analysis` systematics example is physically correct or that a
`deep-learning` example's code actually runs. Treat that as a review step, not
something to automate away: before merging a new example, have it read (or, for
runnable code, executed) by someone - or an agent with that skill's own
`references/` loaded - able to judge that domain.

## Cross-skill use

This reference lives only in `agile-development` and is shared by cross-link
rather than copied into each skill - the routing rule in
`skill-router/SKILL.md` and each rollout skill's own "When to Load
References"-equivalent section point back here. That means a skill installed
without `agile-development` alongside it cannot use this capability; call that
out explicitly wherever the pointer is added, matching how this repository's root
README already documents partial installs as supported.

Don't add `examples/` to a skill's `REQUIRED_PATHS` (or equivalent orphan check)
until that skill actually has a populated `examples/` directory - an empty
requirement would make the validator lie about coverage.
