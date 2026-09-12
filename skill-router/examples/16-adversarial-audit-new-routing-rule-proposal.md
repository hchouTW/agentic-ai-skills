---
role: ruthless Staff Prompt Engineer / Red-Teamer
skill: skill-router
archetype: adversarial-audit
candidate_artifact: "- **frontend-design** - building or styling UI components, layouts, and pages; choosing typography, color, and visual hierarchy; CSS/Tailwind styling work; responsive design and accessibility polish; creating mockups, wireframes, and design systems. Triggers on \"design this page\", \"make this UI nicer\", \"style this component\", or \"build a landing page\"."
---

## 1. Initial Candidate Artifact

A contributor proposes adding a sixth domain skill, `frontend-design`, and
drafts the following routing-rule bullet in the same style as the four
existing entries in `SKILL.md`'s `## Routing rules` section:

```
- **frontend-design** - building or styling UI components, layouts, and pages;
  choosing typography, color, and visual hierarchy; CSS/Tailwind styling work;
  responsive design and accessibility polish; creating mockups, wireframes,
  and design systems. Triggers on "design this page", "make this UI nicer",
  "style this component", or "build a landing page".
```

It reads as reasonable in isolation: it names concrete trigger vocabulary
(typography, CSS/Tailwind, mockups) rather than vague "helps with design"
language, and it follows the existing `- **name** - ...` bullet shape closely
enough that `validate_skill_bundle.py`'s `extract_routed_skill_names()`
(which only greps for `- **<name>**` at bullet position) would parse it
without complaint. The audit below shows that structural cleanliness is not
routing-safety.

## 2. Attack Vectors & Stress-Tests

**Attack Vector 1: Unacknowledged keyword collision with `agile-development`'s
own "UI work" trigger.**
`SKILL.md`'s existing `agile-development` bullet already claims UI work
outright:

```
- **agile-development** - any non-trivial software change: new features, bug
  fixes, refactors, endpoints, UI work, migrations, dependency updates; ...
```

The candidate bullet's own trigger phrases - "building or styling UI
components", "make this UI nicer", "build a landing page" - are not a
disjoint vocabulary from "UI work"; they are a strict subset of it. Every
existing rule in the table that shares surface vocabulary with another rule
(the `pipeline` collision between `deep-learning` and `hep-analysis` fixed in
`examples/08-gated-pipeline-adding-a-new-rule.md`, or the reading/writing vs.
analysis boundary between `academic-papers` and `hep-analysis`) carries an
explicit disambiguation clause. This candidate carries none. As drafted, any
request that touches a UI at all is a live collision, not an edge case.

**Attack Vector 2: Missing "Not for X" exclusion analogous to the ones every
existing rule already uses.**
Compare the candidate against `academic-papers`'s actual boundary clause:

```
Not the underlying statistical/ML/physics analysis - see `deep-learning`/
`hep-analysis` for that; this is the reading/writing/formatting layer on
top of it.
```

and `hep-analysis`'s:

```
Not for unrelated uses of "root" (Linux root users, Android rooting,
certificates, math or plant roots).
```

Both existing carve-outs draw a hard line between "this skill's actual
territory" and "a superficially similar thing that belongs elsewhere or
nowhere." The candidate bullet has no such line. It says "building ... UI
components" without excluding the non-visual half of building a UI
component - wiring up state, event handlers, form validation, API calls -
which is `agile-development`'s territory (a "non-trivial software change")
and has nothing to do with typography or visual hierarchy. Structurally, the
bullet under audit is the *only* one of five candidate/existing rules with
zero exclusion clause.

**Attack Vector 3: No primary/secondary resolution rule for the overlap the
first two vectors expose.**
`SKILL.md`'s Behavior rule 2 says: "Multiple relevant: state the primary and
any secondary skill(s) ... Invoke the primary first." That rule presumes the
routing-rule text itself gives the router enough information to *decide*
which is primary. `examples/04-decision-tree-multi-skill-ambiguous-routing.md`
does exactly this work for an existing overlap (a PyTorch-training-loop
refactor for a reproducibility section resolves to `deep-learning` primary /
`academic-papers` secondary, because the domain-specific rule subsumes
`agile-development`'s generic trigger). The candidate bullet does none of
this: it gives no rule for whether a UI request that is both "a non-trivial
change" and "a styling ask" should be `agile-development`-primary,
`frontend-design`-primary, or both-as-primary (which Behavior's own wording
does not permit - it says "the primary," singular). Whichever the router
picks becomes arbitrary and non-reproducible across two runs of the same
request.

## 3. Concrete Counter-Example / Exploit Proof

The following single, realistic request ambiguously satisfies both the
existing `agile-development` bullet and the candidate `frontend-design`
bullet as currently drafted, with the routing table giving no textual basis
to prefer one over the other or to name a primary:

```
Add a settings page to the dashboard, and make sure its UI looks clean and
modern - polished typography, good spacing, nothing cramped.
```

Checked against the *current* candidate text word-for-word:

- `agile-development` match: "any non-trivial software change: new features
  ... UI work" - adding a settings page is a new feature; "UI work" is named
  verbatim.
- `frontend-design` match: "building or styling UI components, layouts, and
  pages; choosing typography ... visual hierarchy" - "polished typography,
  good spacing" is named almost verbatim.

Both bullets fire on identical surface text ("UI", "typography" is implied by
"visual hierarchy" in one and stated outright by the user in the other), and
neither bullet states which is primary. Two independent router passes over
this exact request could legitimately emit "Using `agile-development` skill."
and "Using `frontend-design` skill (primary), with `agile-development` for
the underlying change." on different runs - a non-deterministic routing
outcome for one fixed input, which is precisely what Behavior rule 2 exists
to prevent.

## 4. Hardened Architectural Patch

```diff
-- **frontend-design** - building or styling UI components, layouts, and pages;
-  choosing typography, color, and visual hierarchy; CSS/Tailwind styling work;
-  responsive design and accessibility polish; creating mockups, wireframes,
-  and design systems. Triggers on "design this page", "make this UI nicer",
-  "style this component", or "build a landing page".
+- **frontend-design** - the visual/aesthetic layer of UI work: choosing
+  typography, color, spacing, and visual hierarchy; CSS/Tailwind styling
+  decisions; responsive-design and accessibility *polish* (contrast, focus
+  states, touch targets); creating mockups, wireframes, and design systems.
+  Triggers on "design this page", "make this UI nicer", "style this
+  component", or "build a landing page". Not the underlying component
+  implementation, state management, or event/data-handling logic - see
+  `agile-development` for that; this is the look-and-feel layer on top of
+  it. When a request both implements a UI feature and asks for it to look
+  good, `agile-development` is primary (it owns the change) and
+  `frontend-design` is secondary (it owns the aesthetic decisions), per
+  `SKILL.md`'s Behavior rule 2.
```

This mirrors the existing collection's own conventions exactly rather than
inventing a new pattern: the "Not the underlying X - see `Y` for that; this
is the Z layer on top of it" sentence is lifted structurally from
`academic-papers`'s real carve-out, and the explicit primary/secondary
assignment is lifted structurally from the resolution
`examples/04-decision-tree-multi-skill-ambiguous-routing.md` already
performs for a different overlap.

## 5. Proof of Robustness Post-Fix

Re-running Section 3's exploit request against the hardened bullet:

- "Add a settings page to the dashboard" (the change itself) still matches
  `agile-development`'s "any non-trivial software change ... new features."
- "make sure its UI looks clean and modern - polished typography, good
  spacing" now matches `frontend-design`'s explicitly-scoped "visual/
  aesthetic layer ... typography, color, spacing" - but the hardened bullet's
  new sentence directly states the ordering: `agile-development` primary,
  `frontend-design` secondary. The router now has one deterministic output
  regardless of run order:

```
> Using `agile-development` skill (primary), with `frontend-design` for the
> visual/aesthetic decisions.
```

Re-running Attack Vector 2's counter-example - a request with no aesthetic
component at all, e.g. "wire up the settings page's save button to call the
update-profile API and show a spinner while it's in flight" - against the
hardened bullet: no typography/color/spacing/mockup language is present, so
`frontend-design` does not fire at all, and only `agile-development` applies,
confirming the "Not the underlying component implementation ... logic" clause
now correctly excludes pure-logic requests that merely mention a UI element
in passing. Both attack vectors from Section 2 (the unflagged collision and
the missing exclusion) are closed by the same two-sentence addition; Attack
Vector 3 (non-deterministic primary) is closed by the explicit primary/
secondary sentence, not merely by writing the collision down.
