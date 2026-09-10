---
role: Senior Platform / Developer-Experience Engineer
skill: skill-router
use_case: recognizing when a request only superficially matches a routed keyword and should not trigger that rule, per the rule's own stated negative carve-out
---

## Scenario

A user asks: "How do I fix the root cause of this failing CI job - the build
step keeps failing because the runner user doesn't have permission to write
to `/opt/build-cache`?" The request contains the word "root" (in "root
cause"), and `hep-analysis`'s routing rule covers "ROOT C++, PyROOT,
RDataFrame" - but the rule also carries its own explicit negative carve-out:
"Not for unrelated uses of 'root' (Linux root users, Android rooting,
certificates, math or plant roots)." The actual request is a generic
CI-permissions problem with no ROOT framework, physics data, or HEP content
anywhere in it.

## Common Weak Approach

The router pattern-matches on the bare substring "root" appearing in the
request, sees that `hep-analysis` is the rule naming "root" (ROOT C++,
PyROOT), and invokes it without reading past the keyword match:

> Using `hep-analysis` skill.
>
> [`hep-analysis` responds with guidance about `root-config` build flags,
> `TFile`/`TTree` I/O, or ROOT CMake integration - none of which has anything
> to do with a CI runner's filesystem permissions.]

This treats "contains the string 'root'" as sufficient to match the rule,
which is exactly the failure `hep-analysis`'s own carve-out exists to
prevent - the rule's text explicitly lists "Linux root users... certificates"
as excluded cases, and "root cause of a CI permissions failure" is squarely
inside that exclusion, not a borderline case requiring judgment. The user
receives an answer about a physics-analysis framework for a question that was
never about one, and has to restate the question to get a useful answer.

## Expert-Level Best Practice

The router reads the full rule text, including its stated carve-out, before
deciding whether it matches - not just the bolded skill name and its
positive description:

> Checked `hep-analysis`'s rule text in full: "ROOT C++, PyROOT,
> RDataFrame... Not for unrelated uses of 'root' (Linux root users, Android
> rooting, certificates, math or plant roots)." The request's "root cause"
> and "runner user doesn't have permission" describe a Linux
> file-permissions problem on a CI runner - exactly the excluded case named
> in the carve-out, not the ROOT data-analysis framework the positive half of
> the rule describes.
>
> No other routing rule in `SKILL.md` covers general CI/build tooling either,
> so per `SKILL.md`'s own rule 4 ("If none of the rules apply, proceed
> normally without mentioning this skill"), no domain skill is invoked. The
> request is answered directly: grant the runner user write access to
> `/opt/build-cache` (e.g. `chown` the cache directory to the runner's user,
> or relax its permissions to the minimum needed), with no mention of
> `skill-router` or `hep-analysis` anywhere in the response.

The router treats a rule's own "Not for..." clause as load-bearing rather
than decorative - a substring match on "root" is checked against the
carve-out before it is treated as a routing decision - and, finding no rule
actually applies, follows the explicit fallback behavior instead of forcing a
match onto the nearest keyword hit.

## Key Takeaways

- A keyword appearing in a request is necessary but not sufficient for a rule
  to match; every rule's own "Not for..." clause is part of the rule, not an
  edge-case footnote, and has to be checked before the rule is treated as a
  match - `hep-analysis`'s carve-out names this exact case ("Linux root
  users... certificates") explicitly.
- Silently forcing a match onto the nearest keyword hit produces a
  confidently wrong answer (ROOT-framework guidance for a filesystem-
  permissions question), which is worse for the user than the router
  correctly finding no match at all.
- Rule 4's "proceed normally without mentioning this skill" is not merely the
  default when no rule looks relevant - it is the *correct* outcome for a
  request whose only surface match is explicitly excluded by that rule's own
  text, and should be reached deliberately, not by omission.
- Checking a carve-out costs nothing extra: the same rule text that produced
  the false-positive keyword match also contains the clause that rules it
  out, so reading the full rule (not just its bolded name and positive
  description) is what the correct routing decision actually depends on.
