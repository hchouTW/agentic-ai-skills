---
role: Senior Platform / Developer-Experience Engineer
skill: skill-router
use_case: a single request that legitimately spans two domain skills and must be routed to both, with an explicit primary and secondary
---

## Scenario

A user asks: "Write the systematics paragraph for my paper's cutflow-based
cross-section measurement." The request has two distinct layers: estimating
and describing the jet-energy-scale/cutflow systematic itself (squarely
`hep-analysis` territory - the routing rule names "cutflows... systematic
uncertainties" explicitly) and producing polished, submission-ready manuscript
prose for a specific paragraph (squarely `academic-papers` territory - the
routing rule names "tightening scientific prose" and is the skill whose own
carve-out says it is "the reading/writing/formatting layer on top of" the
underlying analysis). Both rules match the same request at once.

## Common Weak Approach

The router reads the request, notices "cutflow" and "systematics" first,
invokes `hep-analysis` only, and treats the request as fully handled once that
skill produces a technically correct paragraph describing the JES systematic
estimate:

> Using `hep-analysis` skill.
>
> [`hep-analysis` produces a technically accurate paragraph describing the
> JES up/down variation and the resulting 4.06% cross-section uncertainty.]

The paragraph is scientifically correct but was never run through
`academic-papers`' manuscript-writing conventions - journal-appropriate tense
and hedging, whether the number belongs in-line or in a table with a pointer
from the text, and where this paragraph sits relative to the paper's existing
systematics section. The user, expecting submission-ready prose per their
literal request ("write the... paragraph for my paper"), now has to notice
the gap themselves and ask a second time. `skill-router/SKILL.md`'s own
Behavior section states directly that "If multiple skills are relevant, state
the primary skill and any secondary skill(s)... Invoke the primary skill
first" - this response never checked whether a second rule matched, it
stopped at the first one that did.

## Expert-Level Best Practice

The router checks the request against every rule before invoking any of
them, finds that both `hep-analysis` ("cutflows... systematic uncertainties")
and `academic-papers` ("tightening scientific prose") match, and follows the
literal rule-3 behavior for that case:

> Using `hep-analysis` skill (primary), with `academic-papers` for manuscript
> prose.
>
> [`hep-analysis` is invoked first and produces the systematic estimate and
> its technical justification: the JES up/down variation recomputed on the
> full selection, giving a 4.06% cross-section uncertainty, with the specific
> cause (migration across the selection boundary) stated.]
>
> [That technical content is then handed to `academic-papers`' conventions
> for manuscript prose: past-tense reporting of what was done, the number
> placed in-line with a pointer to the paper's existing systematics table
> rather than repeated as a new one, and phrasing that matches the paper's
> established register rather than the router's own explanatory style.]

The router states both skills and their roles *before* doing any other work,
exactly matching the example format `SKILL.md` itself gives ("Using
`deep-learning` skill (primary), with `agile-development` for task
breakdown"), invokes the primary skill first per that same rule, and only
then routes the primary's output through the secondary skill's own
conventions - so the deliverable matches what was actually asked for (a
paragraph ready to go in the paper) rather than a technically correct answer
to only half the request.

## Key Takeaways

- Check every rule against the request before invoking any of them, not just
  the first one that matches. `hep-analysis` matching first is an artifact of
  reading order, not evidence that `academic-papers` doesn't also apply -
  the weak approach's failure is stopping the check early, not misreading
  either rule.
- A request naming a deliverable ("paragraph for my paper") rather than only
  a technical task ("estimate the systematic") is itself a signal to check
  for a second, adjacent rule - here, the output-format layer that
  `academic-papers` explicitly owns per its own "reading/writing/formatting
  layer on top of" carve-out.
- State the primary/secondary split and invoke the primary first, per
  `SKILL.md`'s own rule 3 and its own worked example phrasing. Silently
  picking one skill and treating the request as fully handled removes the
  user's chance to notice, before any work is done, that only half the
  request is being addressed.
- The order matters, not just the pairing: the primary skill's technical
  output has to exist before the secondary skill has anything to apply its
  conventions to. Invoking `academic-papers` first would leave it with no
  systematic estimate yet to write prose about.
