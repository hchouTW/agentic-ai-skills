---
role: Senior Platform / Developer-Experience Engineer
skill: skill-router
archetype: trajectory
problem_input: a ROOT macro that segfaults when a new branch is added, with the user asking to refactor it to fix the crash
---

## 1. Task Input & Context

A user asks: "My ROOT macro segfaults whenever I add a new branch to the
output tree - can you refactor it to fix the crash?" The request contains
"refactor" and "fix", the exact verbs `agile-development`'s rule names
("Triggers on 'implement', 'fix', 'add', 'refactor', 'migrate', or 'update'
code"), alongside "ROOT macro" and "branch" (`TTree`/`TBranch` territory).

## 2. Root-Cause Triage & Action Plan

A keyword-only scan would stop at "refactor... fix" and invoke
`agile-development` first, since those are its literal trigger words. Per
`SKILL.md`'s Behavior rule 1, the full rule text is checked instead of the
first keyword hit:

- `agile-development`'s rule is generic: "any non-trivial software change...
  Triggers on... 'fix', ... 'refactor', ... code." It says nothing about
  ROOT, ntuples, or ROOT's C++ macro execution model - it is written to
  cover code-change *process* in general, not this specific technology.
- `hep-analysis`'s rule explicitly names "ROOT C++, PyROOT, RDataFrame,
  uproot/awkward columnar pipelines, ntuples" and covers debugging within
  that stack - this is a strictly more specific match for a ROOT-macro
  segfault than the generic "fix... code" trigger is.

Per this skill's own established precedent (formalized in example
`04-decision-tree-multi-skill-ambiguous-routing.md`'s triage matrix: "a
request's code-change verb is fully covered by a domain skill's own more
specific rule for that exact code path... do not also invoke
`agile-development`'s generic code-change trigger on top of a domain skill
that already owns this path"), the same reasoning applies here:
`hep-analysis` is invoked alone, since it is a strictly more specific rule
for this exact code path than the generic refactor/fix trigger is.

Action plan: invoke `hep-analysis` only, and confirm the response actually
addresses the ROOT-specific mechanism of the segfault (a dangling branch
pointer after tree structure changes, a known ROOT I/O gotcha) rather than
generic refactoring advice that would apply to any language.

## 3. Surgical Execution

```
> Using `hep-analysis` skill.
```

```cpp
// The actual root cause hep-analysis identifies: a branch address set once
// via SetBranchAddress before the new branch existed, now stale after
// TTree::Branch() reallocates internal buffers. The fix rebinds addresses
// after every structural change to the tree, not a generic "refactor."
tree->Branch("new_variable", &new_variable, "new_variable/D");
tree->SetBranchAddress("existing_variable", &existing_variable);  // must be re-bound here, after Branch()
```

## 4. Verification Evidence

```
$ python3 -c "
import re
skill_md = open('SKILL.md').read()
agile_rule = re.sub(r'\s+', ' ', re.search(r'\*\*agile-development\*\*.*?(?=\n- \*\*|\n## )', skill_md, re.S).group(0))
hep_rule = re.sub(r'\s+', ' ', re.search(r'\*\*hep-analysis\*\*.*?(?=\n- \*\*|\n## )', skill_md, re.S).group(0))
print('ROOT' in agile_rule, 'ROOT C++' in hep_rule)
"
False True
```

Confirms the actual rule text, not a paraphrase: `agile-development`'s bullet
contains no ROOT-specific language, while `hep-analysis`'s does, supporting
the choice of `hep-analysis` as the strictly more specific match.

## 5. Final Deliverable Summary

Routed a "refactor... fix" request to `hep-analysis` rather than
`agile-development`, because the code path in question (a ROOT macro's
`TTree`/`TBranch` handling) is owned by a domain skill's own explicit,
technology-specific rule, which takes precedence over the generic
code-change trigger those same words would otherwise satisfy. No skill was
invoked twice, and the response addressed the actual ROOT-specific mechanism
rather than generic refactoring guidance.
