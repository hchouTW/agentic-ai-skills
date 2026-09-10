---
role: Senior Platform / Developer-Experience Engineer
skill: skill-router
archetype: trajectory
problem_input: a request to write the abstract for a paper on a neutrino telescope search
---

## 1. Task Input & Context

A user asks: "Can you help me write the abstract for my paper on the
neutrino telescope search? I have the results but I'm not happy with how
they're currently summarized." No code, no ROOT/PyROOT, no PyTorch model, and
no ambiguity about the deliverable - the ask is specifically for manuscript
prose.

## 2. Root-Cause Triage & Action Plan

Per `SKILL.md`'s Behavior rule 1 ("Check the task against the rules above
before doing any other work"), each of the four routing-rule bullets is
checked against the request in full, not stopped at the first keyword hit:

- `academic-papers`: "drafting, restructuring, or polishing a paper or
  section" - matches directly; writing an abstract is exactly this.
- `agile-development`: "any non-trivial software change... Triggers on
  'implement', 'fix', 'add'... or 'update' code" - no code is involved here,
  so this does not match despite the request being a "task" in the loose
  sense.
- `deep-learning`: PyTorch engineering keywords - none present. "Neutrino
  telescope" alone does not imply a PyTorch training/analysis task.
- `hep-analysis`: "collider and particle-physics data and simulation...
  neutrino telescopes" is listed explicitly under its astroparticle-physics
  scope. This is the one genuinely close call: the subject matter (a
  neutrino telescope search) is squarely `hep-analysis` territory, but the
  *ask* is to write prose summarizing already-existing results, not to
  perform or re-derive the analysis - that reading/writing layer is exactly
  what `academic-papers`'s own carve-out claims ("Not for the underlying
  statistical/ML/physics analysis itself... this is the reading/writing/
  formatting layer on top of it").

Action plan: invoke `academic-papers` alone, since the request is unambiguous
about wanting manuscript prose rather than analysis work, and confirm this
was the right call by checking that the response stays entirely within the
writing layer (no new physics results, no recomputed numbers).

## 3. Surgical Execution

```
> Using `academic-papers` skill.
```

```python
# Verifying the routing decision against the actual rule text before
# committing to it - both rules quoted verbatim, not paraphrased from memory.
academic_papers_rule = (
    "drafting, restructuring, or polishing a paper or section"
)
hep_analysis_carveout_boundary = (
    "Not for the underlying statistical/ML/physics analysis itself - "
    "see `deep-learning` or `hep-analysis` for that; this is the "
    "reading/writing/formatting layer on top of it."
)
assert "abstract" not in hep_analysis_carveout_boundary  # confirms the ask is prose, not analysis
```

## 4. Verification Evidence

```
$ python3 -c "
import re
skill_md = open('SKILL.md').read()
m = re.search(r'\*\*academic-papers\*\*.*?(?=\n- \*\*|\n## )', skill_md, re.S)
rule = re.sub(r'\s+', ' ', m.group(0))  # collapse the bullet's line-wrapping
print('drafting, restructuring, or polishing a paper or section' in rule)
"
True
```

Confirms the exact phrase relied on for the routing decision is present in
`SKILL.md`'s live text, not a remembered paraphrase of it.

## 5. Final Deliverable Summary

Routed the request to `academic-papers` alone, having explicitly checked and
ruled out `hep-analysis` despite the physics-adjacent subject matter, because
the ask was for manuscript prose (`academic-papers`'s stated territory) and
not for re-deriving or performing the underlying analysis
(`hep-analysis`'s carve-out explicitly excludes writing that layer). No
secondary skill was needed - this was a clean, single-rule match, not an
overlap requiring rule 3's primary/secondary handling.
