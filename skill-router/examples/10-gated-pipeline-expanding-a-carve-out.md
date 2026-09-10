---
role: Principal Platform / Developer-Experience Engineer
skill: skill-router
archetype: gated-pipeline
high_stakes_task: expanding hep-analysis's existing root carve-out after a new false-positive category (a dental root canal question) was observed in production
---

## Phase 1: Input Extraction & Gap Formulation

A user asked "how long is root canal recovery time, and can I go back to
work the next day?" and the router matched `hep-analysis`'s bullet on the
bare substring "root," producing an answer about ROOT the physics-analysis
framework for a dental question. `hep-analysis`'s current carve-out reads
(verbatim, lines 68-69 of `SKILL.md`):

```
$ sed -n '66,69p' SKILL.md
  significance/trials-factor statistics, the AMS-02 (ISS spectrometer) case
  study, and cosmic-ray flux calculation from counts/exposure. Not for
  unrelated uses of "root" (Linux root users, Android rooting, certificates,
  math or plant roots).
```

The list is enumerated (four specific categories), and "dental root canal"
is not one of them - this is a real gap, not a hypothetical one, since it
was observed causing an actual misroute.

**Gate:** proceed to Phase 2 only once it's confirmed which convention this
carve-out follows - an enumerated list (as it currently is) versus a general
principle - by reading the actual live text (done above, not paraphrased
from memory), and the exact line range to edit is located precisely.

## Phase 2: Draft Synthesis

The existing carve-out is a comma-separated enumerated list, matching this
repository's established convention of concrete, specific exclusions rather
than a general principle (the same style used throughout `SKILL.md`'s other
bullets). Consistent with that convention, drafted a minimal addition rather
than rewording the whole clause:

```diff
-Not for
-unrelated uses of "root" (Linux root users, Android rooting, certificates,
-math or plant roots).
+Not for
+unrelated uses of "root" (Linux root users, Android rooting, certificates,
+math or plant roots, or a dental root canal).
```

**Gate:** proceed to Phase 3 only once the diff is confirmed to be a minimal,
surgical addition matching the exact existing style (comma-separated,
parenthetical, no rewording of the surrounding sentence), and a fresh grep
confirms no other rule's positive territory claims the word "canal" or
"dental" (`grep -n -i "canal\|dental" SKILL.md` returns no hits before this
edit), so the addition cannot itself create a new collision.

## Phase 3: Red-Team Review & Final Artifact Packaging

Stress-tested the assumption "adding one more item to the list closes the
gap." The deeper question: is this list actually closable at all, or is it
structurally incomplete by nature? "Root" appears in English idioms far
beyond the four-plus-one categories now listed - "root beer," "root of the
problem" (already implicitly covered by the CI-permissions example in
`examples/03-negative-carve-out-not-a-match.md`, which relies on the *reader*
recognizing "root cause" as excluded even though "root cause" itself isn't
in the enumerated list), "taking root" (gardening), "square root" (already
covered by "math... roots"). The assumption that a finite enumerated list
can ever be *exhaustive* against an open-ended set of English idioms
containing "root" is false - this is a structural limitation, not a bug to
be fully fixed by any single addition.

Rather than silently declaring the carve-out "complete" after adding one
item, logged this as an explicit, honest limitation: the enumerated-list
carve-out will keep needing case-by-case additions as new false positives
are observed in production, and that is expected and acceptable (each
addition is cheap and low-risk) rather than a sign the approach is broken -
but it should never be presented as a closed, exhaustive list.

**Gate:** merge only once the minimal diff above is applied *and* a
follow-up note recording this list's inherent incompleteness is added to
this skill's own tracked validation history - not silently treated as fully
solved - so a future false positive is recognized as an expected, addressable
case rather than a surprising regression.
