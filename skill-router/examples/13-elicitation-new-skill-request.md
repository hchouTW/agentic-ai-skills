---
role: Principal Skill-Router Maintainer
skill: skill-router
archetype: elicitation
user_request: "Add a new skill for technical writing"
---

## 1. Raw Ambiguous Input

Message from a repository maintainer, posted in the skills-maintenance
channel:

> Add a new skill for technical writing. We keep getting docs requests and
> nothing routes to it.

No proposed routing-rule wording, no keyword list, no carve-outs against
existing rules, and no example trigger phrases to validate the new rule
against.

## 2. Missing Constraint Analysis

Per `SKILL.md`'s routing-rules format, each bullet is a carefully scoped
paragraph naming what the skill covers *and* explicitly what it does not
(e.g. `academic-papers`'s "Not the underlying statistical/ML/physics
analysis"), because overlapping wording between rules is exactly what
produces a wrong or ambiguous route. "Technical writing" as a bare label
risks colliding with `academic-papers` (scientific writing/formatting) and
`agile-development` (design docs, ADRs, communication) - both already
mention writing-adjacent work. Adding a new rule without checking for that
overlap could create a genuine ambiguity the router can't resolve.

Specifically missing:
- **Exact scope** - "technical writing" could mean API reference docs,
  user-facing how-to guides, internal design docs, or release notes; each
  overlaps differently with the two existing writing-adjacent rules.
- **Carve-outs against existing rules** - `academic-papers` already covers
  "tightening scientific prose" and `agile-development` already covers
  "design docs" - the new rule needs explicit language distinguishing
  itself from both, or requests will double-route or mis-route.
- **Concrete trigger phrases** - without 2-3 example prompts the new rule
  is meant to catch, there's no way to check it actually improves routing
  versus just adding an untested bullet.
- **Whether this needs a new skill folder at all** - if the actual gap is
  narrow (e.g. only API reference docs), extending an existing skill's
  scope might be simpler than standing up a whole new skill package.

## 3. Socratic Clarification Round

1. What is the precise scope of "technical writing" being requested?
   a) API reference documentation and docstring/comment quality
   b) User-facing how-to guides and tutorials (product documentation, not
      code-adjacent)
   c) Both, treated as one skill
2. How should this be distinguished from `academic-papers`'s existing
   "tightening scientific prose" language?
   a) Explicitly: `academic-papers` stays scoped to scientific-paper prose;
      the new skill covers non-paper technical prose (docs, guides, READMEs)
   b) No distinction needed - the two are different enough contexts that
      overlap isn't a real risk
   c) Merge the new scope into `academic-papers` instead of a new skill
3. How should this be distinguished from `agile-development`'s existing
   "design docs" coverage?
   a) Explicitly: `agile-development` stays scoped to docs that record an
      engineering decision (ADRs, design docs); the new skill covers
      docs written *for an external audience* (users, API consumers)
   b) No distinction needed
   c) Merge the new scope into `agile-development` instead of a new skill
4. What are 2-3 concrete trigger phrases the new rule must correctly route?
   a) "Write the API docs for this endpoint", "improve this README",
      "draft a user-facing changelog entry"
   b) A different, narrower set focused only on one of the above
   c) Not yet decided - would need to survey actual past requests first

## 4. User Feedback Integration

The maintainer's answers, after reviewing three recent misrouted requests:

- Q1 -> **c) Both, treated as one skill.** All three recent requests span
  API docs and user-facing guides; splitting them into two skills now would
  be premature given the current request volume.
- Q2 -> **a) Explicit carve-out from `academic-papers`.** The new skill's
  routing bullet will state it does not cover scientific-paper prose,
  matching `academic-papers`'s existing "not the underlying analysis"
  carve-out pattern.
- Q3 -> **a) Explicit carve-out from `agile-development`.** The new
  skill's bullet will state it covers externally-facing documentation, not
  internal decision records (ADRs/design docs), which stay with
  `agile-development`.
- Q4 -> **a) The three given trigger phrases**, confirmed as the actual
  requests that prompted this ask - each currently fails to route to any
  skill.

Each answer resolves one gap from section 2: Q1 fixes the scope as a
single unified skill rather than two narrower ones, Q2 and Q3 supply the
explicit carve-out language needed to avoid colliding with the two
existing writing-adjacent rules, and Q4 gives concrete phrases to validate
the new rule against once written.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** A new `technical-writing` skill and a corresponding
`SKILL.md` routing-rule bullet in `skill-router`, scoped to externally-
facing developer and product documentation, with explicit carve-outs
against `academic-papers` and `agile-development`.

**In scope:** A routing bullet reading approximately: "**technical-writing**
- API reference documentation, docstrings/code comments meant for external
consumers, user-facing how-to guides, tutorials, READMEs, and release
notes. Not scientific-paper prose (see `academic-papers`) and not internal
engineering decision records like ADRs or design docs (see
`agile-development`)." Validating the bullet against the three confirmed
trigger phrases.

**Out of scope:** Splitting technical writing into separate API-docs and
user-guide skills; modifying `academic-papers` or `agile-development`'s
existing bullets beyond what's needed to cross-reference the new carve-out
language.

**Acceptance criteria (given/when/then):**
- Given the phrase "Write the API docs for this endpoint," when routed,
  then it resolves to `technical-writing`, not `agile-development`.
- Given the phrase "tighten the prose in section 3 of my manuscript," when
  routed, then it still resolves to `academic-papers` - the new rule must
  not regress this existing routing.
- Given the phrase "write an ADR for this database migration," when
  routed, then it still resolves to `agile-development` - the new rule's
  carve-out must not swallow this existing case.
- Given `scripts/validate_skill_bundle.py`, when run after adding the new
  skill folder, then the routing table's skill names line up with the
  newly-installed sibling folder with no reported mismatch.

**Explicit non-goals:** This does not attempt to migrate any existing
`academic-papers` or `agile-development` example content into the new
skill - only new, genuinely externally-facing documentation requests route
here going forward.
