---
role: Principal Skill-Router Maintainer
skill: skill-router
archetype: elicitation
user_request: "Can you make the router better at catching edge cases?"
---

## 1. Raw Ambiguous Input

Message from a contributor filing a follow-up after a support thread:

> Can you make the router better at catching edge cases? Someone hit a bad
> route again.

No specific false-positive or false-negative example given, no named
routing rule, and no stated fix direction (carve-out, keyword addition, or
a brand-new rule).

## 2. Missing Constraint Analysis

Per `SKILL.md`'s routing rules, several existing bullets already carry
explicit carve-out language for known-overloaded terms (e.g. hep-analysis's
"Not for unrelated uses of 'root'"), added precisely because a bare keyword
match produces false positives. "Make the router better" without a
specific failing example gives no way to tell which class of fix applies:
a carve-out (the word is right but the domain is wrong), a keyword
addition (a real request in scope uses wording the rule doesn't currently
catch), or a new rule (no existing bullet covers the domain at all). Fixing
the wrong class wastes effort and risks a regression on already-correct
routing (per existing example
`skill-router/examples/03-negative-carve-out-not-a-match.md`, which
already covers one such carve-out case).

Specifically missing:
- **The specific example** - no request text is given; "someone hit a bad
  route" could describe any of dozens of possible ambiguous prompts.
- **False positive or false negative** - did the router route to a skill
  it shouldn't have, or fail to route to a skill it should have?
- **Which rule is implicated** - the fix targets a specific bullet's
  wording, not the router in the abstract.
- **Whether this duplicates an already-covered case** - `03-negative-
  carve-out-not-a-match.md` and `12-decision-tree-multiple-false-positive-
  keywords.md` already document two known overloaded-keyword patterns; a
  new fix should not re-solve an already-solved case.

## 3. Socratic Clarification Round

1. What was the exact request that produced a bad route?
   a) "Can you check if this fit converged?" - ambiguous between a
      statistical fit (hep-analysis) and a general-English "does this fit"
   b) A different request - would need the original support thread
   c) Not available - only a secondhand description exists
2. Was this a false positive (routed to a skill it shouldn't have) or a
   false negative (failed to route to a skill it should have)?
   a) False positive - it routed to `hep-analysis` for a request that
      turned out to be about a clothing-fit e-commerce feature, unrelated
      to physics
   b) False negative - it should have routed to `hep-analysis` but didn't
   c) Not yet determined
3. Which existing routing-rule bullet is implicated?
   a) `hep-analysis`'s bullet, specifically the word "fit" (used there for
      "RooFit/RooStats... likelihood-fitting")
   b) `deep-learning`'s bullet, for a different overloaded term
   c) Not yet determined
4. Does this duplicate an already-documented edge case in this skill's
   `examples/` directory?
   a) No - `03-negative-carve-out-not-a-match.md` and `12-decision-tree-
      multiple-false-positive-keywords.md` cover different overloaded
      terms ("root" and others), not "fit"
   b) Yes - it's the same pattern already covered
   c) Not yet checked

## 4. User Feedback Integration

The contributor's answers, after pulling the actual transcript:

- Q1 -> **a) Confirmed exact text**: "Can you check if this fit
  converged?" - sent in the context of an e-commerce team's clothing-size
  recommendation feature, not a physics analysis.
- Q2 -> **a) False positive.** The router matched "fit" against
  `hep-analysis`'s likelihood-fitting language and routed there, even
  though the actual context (checked from the surrounding conversation)
  was a size-recommendation model's convergence, which is a
  `deep-learning` question if it's about anything at all.
- Q3 -> **a) `hep-analysis`'s bullet**, specifically its bare mention of
  "fit"/"likelihood-fitting" with no surrounding context requirement.
- Q4 -> **a) No duplication confirmed** - a search of `examples/` confirms
  neither existing false-positive example covers the word "fit"; this is a
  genuinely new case.

Each answer resolves one gap from section 2: Q1 supplies the concrete
triggering text, Q2 classifies the failure as a false positive (not a
missed route), Q3 pinpoints the exact implicated bullet and term, and Q4
confirms this isn't already solved elsewhere, avoiding redundant work.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** Add a carve-out to `hep-analysis`'s routing-rule bullet for
the bare word "fit," analogous to the existing "root" carve-out, so a
generic or e-commerce/ML "fit" (convergence of a recommendation model,
whether something "fits" a requirement) does not alone trigger
`hep-analysis` routing without other physics-specific context
(RooFit/RooStats/likelihood/χ²/nuisance parameters).

**In scope:** Editing `hep-analysis`'s `SKILL.md` bullet to add explicit
carve-out language (e.g. "not a bare use of 'fit' outside a stated
statistical/physics context - see `deep-learning` if the fit in question is
a model-convergence question"); adding a new canonical example documenting
this specific false positive and its resolution, following the existing
`03-negative-carve-out-not-a-match.md` pattern.

**Out of scope:** Rewriting any other routing-rule bullet; addressing any
other overloaded term not confirmed by this specific report.

**Acceptance criteria (given/when/then):**
- Given the phrase "Can you check if this fit converged?" with e-commerce/
  size-recommendation context, when routed after the fix, then it does not
  route to `hep-analysis` on the word "fit" alone.
- Given a phrase like "the likelihood fit didn't converge, check the
  nuisance parameters," when routed after the fix, then it still correctly
  routes to `hep-analysis` - the carve-out must not create a false
  negative for genuine physics-fit requests.
- Given `python3 -m unittest discover -s tests -v` in `skill-router`, when
  run after the change, then all existing routing-table tests still pass,
  confirming no regression.

**Explicit non-goals:** This does not attempt to enumerate every possible
overloaded term across all four routing rules in one pass - only the
confirmed "fit" false positive is addressed; other terms are deferred
until a similar concrete report surfaces them.
