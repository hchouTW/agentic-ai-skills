---
role: Senior Research Scientist / Manuscript Editor
skill: academic-papers
use_case: responding to a referee report that questions a statistical-significance claim
---

## Scenario

A submitted paper reports a 3.5σ local excess found while scanning 20
approximately independent hypothesized mass points across a search range. A
referee writes: "The paper reports 3.5σ significance for the excess. Has the
look-elsewhere effect been accounted for? As stated, this claim may overstate
the significance." The authors must write a response-letter point addressing
this comment before the paper can be reconsidered.

## Common Weak Approach

> **Referee comment 2:** The paper reports 3.5σ significance for the excess.
> Has the look-elsewhere effect been accounted for? As stated, this claim may
> overstate the significance.
>
> **Response:** We thank the referee for the comment. We have re-examined our
> analysis and confirm the significance of 3.5σ is correct. No changes to the
> manuscript were made.

This response does not engage with what the referee actually asked. It
restates the original number rather than addressing whether that number is the
right one to quote, makes no distinction between a local and a global
significance, performs no calculation, and states that nothing was changed in
a case where the referee's concern - if valid - would require a change. Per
this skill's own guidance in `references/submission-and-peer-review.md`,
"silence on a disputed point reads as an oversight and invites a repeat
request in the next round" - and here there isn't even silence, there is an
assertion with nothing behind it, which reads worse: it looks like the comment
was not understood rather than that it was considered and rejected for a
stated reason.

## Expert-Level Best Practice

> **Referee comment 2:** The paper reports 3.5σ significance for the excess.
> Has the look-elsewhere effect been accounted for? As stated, this claim may
> overstate the significance.
>
> **Response:** The referee is correct, and we thank them for raising this.
> The originally quoted 3.5σ is the *local* significance, evaluated at the
> best-fit mass point; it did not include the look-elsewhere effect from
> scanning 20 approximately independent mass hypotheses across the search
> range. We have recomputed the global significance using a trials-factor
> correction appropriate for this number of independent trials:
>
> ```python
> import math
> from statistics import NormalDist
>
> def local_p_value(z_local: float) -> float:
>     return 0.5 * math.erfc(z_local / math.sqrt(2))
>
> def global_p_value(p_local: float, n_trials: int) -> float:
>     return 1 - (1 - p_local) ** n_trials
>
> def significance_from_p(p: float) -> float:
>     return NormalDist().inv_cdf(1 - p)
>
> z_local = 3.5
> n_trials = 20
>
> p_local = local_p_value(z_local)
> p_global = global_p_value(p_local, n_trials)
> z_global = significance_from_p(p_global)
> ```
>
> This gives `p_local = 2.33e-4` (`z_local = 3.5σ`) and, after the trials
> correction for 20 independent mass points, `p_global = 4.64e-3`
> (`z_global = 2.6σ`). The manuscript has been revised in Sec. IV, paragraph 3,
> which now reads: "The local significance of the excess is 3.5σ
> (p_local = 2.3 × 10⁻⁴). Accounting for the look-elsewhere effect from
> scanning 20 independent mass hypotheses across the search range, the global
> significance is 2.6σ (p_global = 4.6 × 10⁻³). We therefore describe this
> result as an indication rather than evidence of a signal." The abstract and
> summary have been updated to match, replacing "a 3.5σ excess" with "a 3.5σ
> local (2.6σ global) excess" throughout.

The response quotes the referee's comment in full, states plainly that the
referee is right rather than defending the original claim, shows the actual
calculation rather than asserting a conclusion, reports both the local and
corrected global numbers with their p-values, and points to the exact revised
location in the manuscript with the new wording - matching this skill's
structure for referee responses: quote the comment, state what changed with a
pointer to where, and keep the tone factual rather than defensive even though
the original claim was wrong.

## Key Takeaways

- Distinguish a local significance (evaluated at one specific, data-chosen
  location) from a global significance (corrected for having searched many
  locations) explicitly, in both the response letter and the manuscript text -
  conflating the two is the specific statistical error the referee's comment is
  naming, not a phrasing nitpick.
- Show the calculation, not just the conclusion. `p_global = 4.64e-3`
  (`z_global = 2.6σ`) is a number a referee, editor, or future reader can check
  against the stated method (20 independent trials, the formula above); "we
  re-examined our analysis and confirm the result" is not.
- When the referee is right, say so plainly and change the manuscript - the
  expert response opens with "the referee is correct," not a hedge. Per this
  skill's guidance, a calm, direct correction resolves a valid comment faster
  than a defensive restatement of the original claim, and disputing a comment
  that turns out to be correct just produces a second, harder round.
- Point to the exact revised location and quote the new wording, not just a
  description of what kind of change was made. A referee re-reviewing a
  revision has to find the change to verify it: "no changes were made" (weak)
  and "this has been clarified" with no pointer are both effectively
  unverifiable; "Sec. IV, paragraph 3, now reads: ..." is not.
