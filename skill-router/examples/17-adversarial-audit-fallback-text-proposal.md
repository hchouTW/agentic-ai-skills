---
role: ruthless Staff Prompt Engineer / Red-Teamer
skill: skill-router
archetype: adversarial-audit
candidate_artifact: "Proposed Behavior rule 3 rewrite: \"None relevant: state that no domain skill applies, briefly explaining why, before proceeding normally.\" (replacing the current \"None relevant: proceed normally without mentioning this skill.\")"
---

## 1. Initial Candidate Artifact

A contributor proposes changing `SKILL.md`'s Behavior rule 3 from its
current text:

```
3. None relevant: proceed normally without mentioning this skill.
```

to:

```
3. None relevant: state that no domain skill applies, briefly explaining
   why, before proceeding normally.
```

The stated motivation is transparency: a user watching the assistant's
reasoning might wonder whether routing was even considered on a request
that looks borderline, and an explicit "I checked; none apply, because X"
note would make the triage step visible rather than silent. This reads as a
reasonable usability improvement - visibility into a decision that
currently happens invisibly.

## 2. Attack Vectors & Stress-Tests

**Attack Vector 1: the proposed rule turns every single unrelated request
into a mandatory router self-mention, which is exactly the failure mode
`SKILL.md`'s own top-level `description` field exists to prevent.**
The `description` frontmatter field states this skill should trigger "even
if the user doesn't name a skill or use the word 'skill'" - meaning the
router is meant to run its triage on essentially every non-trivial request,
silently, and only surface itself when it actually routes somewhere. The
current rule 3's "proceed normally without mentioning this skill" is not an
afterthought - it is the mechanism that keeps this skill invisible on the
overwhelming majority of requests (anything unrelated to the four domain
skills: casual conversation, general research questions, requests about
unrelated tools). The proposed rewrite would make the assistant announce
"no domain skill applies, because this request is about X" on every one of
those, turning a triage step meant to be invisible into user-facing noise
on the majority case, not just the borderline one the motivation describes.

**Attack Vector 2: "briefly explaining why" has no defined scope, so it
under-specifies exactly the case it claims to help - a genuinely borderline
request - while over-triggering on the clear-cut case it doesn't need to.**
Compare to the existing Behavior section's rules 1 and 2, which are both
precise about what triggers them ("exactly one skill relevant," "multiple
relevant") and precise about what to say (name the skill(s), state
primary/secondary). The proposed rule 3 gives no criterion for when an
explanation is warranted (a genuinely close call between "this might be a
non-trivial software change" and "this is casual conversation") versus
when it is pure overhead (a request that obviously matches none of the four
domain areas, e.g. "what's a good recipe for banana bread"). Without that
distinction, an implementation of the literal rule text would explain on
both, defeating the contributor's own stated motivation (surfacing triage
specifically for the *borderline* case) by drowning it in explanations for
the *obvious* case too.

## 3. Concrete Counter-Example / Exploit Proof

Applying the proposed rule text literally to a request that is not remotely
borderline:

```
User: "What's a good recipe for banana bread?"
```

```
Assistant (per proposed rule 3, applied literally): "No domain skill
applies here - this request is about baking, not software development,
PyTorch/ML engineering, HEP/particle-physics analysis, or academic-paper
writing/formatting, so I'll proceed normally."
```

This is exactly the noise `description`'s "even if the user doesn't name a
skill" design is built to avoid surfacing - the whole point of running
triage silently is that a banana-bread question should get a banana-bread
answer with no mention of a skill-routing system the user never asked
about. Under the *current* rule 3, this exchange produces zero mention of
skill-router at all. Under the *proposed* rule 3, every single one of the
many-times-more-common "obviously unrelated" requests gains an unrequested
meta-comment about why no skill triggered - a regression on the common case
in service of a rare one.

## 4. Hardened Architectural Patch

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@
 1. Exactly one skill relevant: state "Using `<skill-name>` skill." and invoke
    it, then follow its workflow.
 2. Multiple relevant: state the primary and any secondary skill(s), e.g.
    "Using `deep-learning` skill (primary), with `agile-development` for task
    breakdown." Invoke the primary first.
-3. None relevant: proceed normally without mentioning this skill.
+3. None relevant: proceed normally without mentioning this skill. This
+   applies even to a request that briefly touched one of the routing
+   rules' keywords without actually matching its scope (e.g. mentioning
+   "root" in a non-physics sense, or "update" with no software-change
+   intent) - a near-miss is not a borderline case requiring explanation,
+   it is a correctly-resolved non-match.
```

Rather than adding a new user-facing explanation branch, the hardened
version keeps rule 3's behavior unchanged and instead makes explicit what
was previously only implicit: a near-miss keyword match is still "none
relevant," closing the actual ambiguity the original proposal was reaching
for (is a keyword-adjacent request "borderline"?) without introducing a
new failure mode on the common, unambiguous case.

## 5. Proof of Robustness Post-Fix

Re-running Section 3's exploit against the hardened rule 3: "What's a good
recipe for banana bread?" still produces zero mention of skill-router,
since the hardened text preserves "proceed normally without mentioning this
skill" verbatim - the common-case regression from the original proposal
does not occur. Re-running the motivating borderline case the original
proposal was trying to address - a request that mentions "root" in a
context that could plausibly be Linux-root or ROOT-the-physics-framework -
against the hardened rule: the added sentence directly states that a
near-miss keyword match (the existing `hep-analysis` bullet's own "Not for
unrelated uses of 'root'" carve-out) resolves to "none relevant" without
requiring a new explanation branch, because the disambiguation already
lives in the routing rule's own carve-out text, not in a Behavior-rule
narration layer. The transparency goal is met by making the *routing
rules* precise enough to answer the near-miss question, rather than by
making the *fallback behavior* narrate every non-match.
