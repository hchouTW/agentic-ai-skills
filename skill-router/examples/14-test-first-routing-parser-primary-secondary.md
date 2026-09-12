---
role: test-driven Staff Prompt Engineer
skill: skill-router
archetype: test-first
target: Routing-table parser must resolve a request naming two overlapping domains to (primary, secondary) in the documented order
---

## 1. Acceptance Invariants & Boundary Constraints

`SKILL.md`'s Behavior rule 2 states: "Multiple relevant: state the primary
and any secondary skill(s) ... Invoke the primary first," and its own
worked example resolves a PyTorch-training-loop request to `deep-learning`
(primary) with `agile-development` (secondary) - the domain-specific rule
takes primary position over the generic `agile-development` bullet, never
the reverse. The invariant under test: given a set of matched skill names
that includes exactly one domain-specific skill (`academic-papers`,
`deep-learning`, or `hep-analysis`) plus the generic `agile-development`
fallback, `resolve_primary_secondary(matched)` must return
`(domain_specific_skill, "agile-development")`, in that order - never
`("agile-development", domain_specific_skill)`, and never both names in a
tuple with `agile-development` first regardless of match order in the
input. Boundary: a match set with two or more non-`agile-development`
domain skills (no single generic fallback to demote) is out of scope for
this invariant.

## 2. Executable Failing Test (Red)

```python
# tests/test_routing_resolution.py
from routing import resolve_primary_secondary

def test_domain_specific_skill_is_primary_over_agile_development():
    # Request: "refactor this PyTorch training loop to fix a tensor shape
    # mismatch bug" - matches both agile-development ("refactor", bug fix)
    # and deep-learning ("PyTorch", "tensor shape" errors).
    matched = ["agile-development", "deep-learning"]  # alphabetical match order
    primary, secondary = resolve_primary_secondary(matched)
    assert primary == "deep-learning", f"primary={primary}"
    assert secondary == "agile-development", f"secondary={secondary}"
```

Current `routing.resolve_primary_secondary` (naively returns matches in
their input order, which happens to be alphabetical):

```python
# routing.py (pre-fix)
def resolve_primary_secondary(matched_skills):
    if len(matched_skills) < 2:
        return (matched_skills[0], None) if matched_skills else (None, None)
    return (matched_skills[0], matched_skills[1])
```

```
$ python3 -m pytest tests/test_routing_resolution.py -v
tests/test_routing_resolution.py::test_domain_specific_skill_is_primary_over_agile_development FAILED

================================== FAILURES ==================================
_____ test_domain_specific_skill_is_primary_over_agile_development _____
AssertionError: primary=agile-development
assert 'agile-development' == 'deep-learning'
1 failed in 0.01s
```

Alphabetical order silently promotes `agile-development` to primary purely
because "a" sorts before "d" - a routing-table artifact, not a deliberate
choice, and the exact opposite of what Behavior rule 2's own worked example
requires.

## 3. Minimal Code Implementation

```python
# routing.py (fixed)
GENERIC_FALLBACK = "agile-development"

def resolve_primary_secondary(matched_skills):
    if len(matched_skills) < 2:
        return (matched_skills[0], None) if matched_skills else (None, None)
    domain_specific = [s for s in matched_skills if s != GENERIC_FALLBACK]
    if len(domain_specific) == 1 and GENERIC_FALLBACK in matched_skills:
        return (domain_specific[0], GENERIC_FALLBACK)
    # Two or more domain-specific matches with no generic fallback to
    # demote: out of scope for this invariant (see Boundary above).
    return (matched_skills[0], matched_skills[1])
```

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_routing_resolution.py -v
tests/test_routing_resolution.py::test_domain_specific_skill_is_primary_over_agile_development PASSED
1 passed in 0.01s
```

```python
>>> from routing import resolve_primary_secondary
>>> resolve_primary_secondary(["agile-development", "deep-learning"])
('deep-learning', 'agile-development')
>>> resolve_primary_secondary(["deep-learning", "agile-development"])
('deep-learning', 'agile-development')
```

The result is now identical regardless of which order the two names appear
in the input match set - the routing table's iteration order can no longer
silently determine which skill is announced as primary.

## 5. Regression Guard Summary

This test guards against re-introducing a resolver that orders matched
skills by scan order or alphabetical position instead of by the documented
domain-specific-over-generic convention - a regression that would pass any
test only checking "is `agile-development` mentioned at all," and would
otherwise surface only as a confusing session where the router announces
"Using `agile-development` skill (primary)" for a clearly domain-specific
request, contradicting `SKILL.md`'s own worked example.
