# Fix `skill-router`'s Bundle Validator Silently Ignoring Non-Lowercase Routing Names

## Background

`skill-router/scripts/validate_skill_bundle.py` parses `SKILL.md`'s routing
rules with a regular expression to (a) confirm the routing table actually
yielded at least one skill name, and (b) cross-check each routed name against
sibling folders on disk. The regex used is:

```python
ROUTING_ENTRY_RE = re.compile(r"^- \*\*([a-z0-9][a-z0-9-]*)\*\*", re.MULTILINE)
```

This only matches a bolded bullet name made up of lowercase letters, digits,
and hyphens. Every routing rule in the shipped `SKILL.md` today happens to be
lowercase-kebab (`academic-papers`, `agile-development`, `deep-learning`,
`hep-analysis`), so the bug has not manifested yet, but nothing in `SKILL.md`
or the validator documents "lowercase only" as a required naming convention
for routing entries - it's an accidental side effect of the regex character
class. A future routing-rule bullet using an uppercase letter or a leading
digit in an unusual way would be silently skipped by
`extract_routed_skill_names`, which would in turn make the "at least one
routing entry found" check under-count without failing, and would make the
sibling cross-check under-report unmatched entries rather than list them.

## Objective

`skill-router/scripts/validate_skill_bundle.py` either (a) matches any
routing-rule bullet regardless of letter case, or (b) the lowercase-kebab
convention is made an explicit, enforced, and documented requirement that a
non-conforming bullet fails loudly on - whichever is confirmed as the
intended behavior (see Open Questions).

## Scope

### In Scope

- Decide (with the maintainer) whether routing names may use characters
  outside `[a-z0-9-]`, or whether lowercase-kebab is a hard requirement.
- Update `ROUTING_ENTRY_RE` and/or add an explicit validation error for a
  non-conforming bullet, consistent with whichever answer is chosen.
- Add a regression test covering the previously-silent case.

### Out of Scope

- Renaming any of the five skills or changing their existing lowercase-kebab
  names - all current names already conform either way.
- Broader `SKILL.md` frontmatter validation beyond the routing-rule bullets
  themselves.

## Repository Context

Verified by direct inspection on 2026-09-12:

- `skill-router/scripts/validate_skill_bundle.py` contains
  `ROUTING_ENTRY_RE = re.compile(r"^- \*\*([a-z0-9][a-z0-9-]*)\*\*", re.MULTILINE)`
  and the `extract_routed_skill_names()` function that applies it.
- `skill-router/tests/test_skill_router.py`'s
  `ExtractRoutedSkillNamesTests` class exercises this function against the
  real `SKILL.md` and two synthetic strings, but every case used is already
  lowercase-kebab - no test currently exercises an uppercase or otherwise
  non-conforming bullet.
- `skill-router/SKILL.md`'s current "Routing rules" section lists exactly
  four bullets - `academic-papers`, `agile-development`, `deep-learning`,
  `hep-analysis` - all lowercase-kebab, so the bug is latent, not currently
  observable in the shipped bundle.

## Technical Approach

1. Confirm with the maintainer whether skill names in this repository are
   guaranteed lowercase-kebab going forward (matching every current skill
   folder name), or whether the routing table should tolerate other casing.
2. If lowercase-kebab is confirmed as the permanent convention: keep the
   regex as-is, but add an explicit check in `main()` that scans routing
   bullets for a bolded name the current regex does *not* match, and fails
   loudly (rather than silently under-counting) when one is found.
3. If arbitrary casing should be supported: broaden
   `ROUTING_ENTRY_RE`'s character class and re-verify
   `find_sibling_skill_dirs`'s comparison still behaves correctly against a
   non-lowercase folder name.
4. Add a test in `ExtractRoutedSkillNamesTests` (or a new test class, for
   the loud-failure branch) using a synthetic `SKILL.md` string with a
   non-lowercase bullet, asserting the chosen behavior.

## Deliverables

- Updated `skill-router/scripts/validate_skill_bundle.py`.
- A new regression test in `skill-router/tests/test_skill_router.py`.
- A short note in `skill-router/VALIDATION.md` describing the fix and which
  of the two resolutions (loud failure vs. broadened regex) was chosen.

## Acceptance Criteria

- A synthetic `SKILL.md` routing bullet using a character outside
  `[a-z0-9-]` no longer passes through `extract_routed_skill_names` silently
  uncounted and unreported - it is either correctly extracted, or the
  validator fails loudly and names the offending bullet.
- All four real routing entries (`academic-papers`, `agile-development`,
  `deep-learning`, `hep-analysis`) are still extracted exactly as before.
- `python3 scripts/validate_skill_bundle.py` still exits `0` on the current,
  unmodified `skill-router` bundle.
- `python3 -m unittest discover -s tests -v` passes, including the new
  regression test.

## Validation

- Run `python3 -m unittest discover -s tests -v` from `skill-router/` and
  confirm the new test and all existing tests pass.
- Run `python3 scripts/validate_skill_bundle.py` from `skill-router/` and
  confirm it still reports "Bundle OK" with the unmodified real `SKILL.md`.
- Manually construct a scratch `SKILL.md` string with a non-conforming
  bullet and confirm the chosen behavior (extraction or loud failure) by
  hand, matching the new test's assertion.

## Open Questions

- Should skill routing names be constrained to lowercase-kebab as a
  documented, enforced convention (option a), or should the extractor
  tolerate any bolded bullet name (option b)? **Requires Confirmation** -
  the source ticket that raised this only observed the latent bug; it did
  not state a preferred resolution.
- Is this worth fixing now given all four current entries already conform,
  or should it be tracked and deferred until a routing rule with unusual
  casing is actually proposed? **TBD.**

## References

- `agentic-ai-skills/skill-router/scripts/validate_skill_bundle.py` - the
  file containing the regex in question.
- `agentic-ai-skills/skill-router/tests/test_skill_router.py` - the existing
  test class to extend.
- `agentic-ai-skills/skill-router/SKILL.md` - the routing table the regex
  parses.
