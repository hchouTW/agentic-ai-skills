---
role: test-driven Staff Prompt Engineer
skill: skill-router
archetype: test-first
target: find_sibling_skill_dirs must exclude a sibling directory whose SKILL.md exists but is empty
---

## 1. Acceptance Invariants & Boundary Constraints

`find_sibling_skill_dirs(root)` in `scripts/validate_skill_bundle.py` must
exclude a sibling directory whose `SKILL.md` exists on disk but is **empty**
(zero bytes) - not just directories with no `SKILL.md` file at all. The
same script's own bundle check elsewhere treats an empty required file as
equivalent to a missing one (`empty = [... if (root / path).stat().st_size
== 0]`); sibling discovery must apply that same standard consistently,
since an empty `SKILL.md` is not a usable skill any more than a missing one
is - reporting it as a real routing target in the "not currently installed"
note would name a skill that cannot actually be invoked.

- A sibling with a real, non-empty `SKILL.md` is included (existing
  behavior, unchanged).
- A sibling with no `SKILL.md` at all is excluded (existing behavior,
  unchanged).
- A sibling whose `SKILL.md` exists but is zero bytes must also be excluded
  - the boundary this test targets, currently unhandled.

## 2. Executable Failing Test (Red)

```python
# tests/test_sibling_discovery_empty_skill_md.py
import tempfile
from pathlib import Path

import validate_skill_bundle


def test_excludes_sibling_with_empty_skill_md():
    with tempfile.TemporaryDirectory() as tmp:
        parent = Path(tmp)
        this_skill = parent / "skill-router"
        this_skill.mkdir()
        hollow_sibling = parent / "half-installed-skill"
        hollow_sibling.mkdir()
        (hollow_sibling / "SKILL.md").touch()  # exists, but zero bytes

        found = validate_skill_bundle.find_sibling_skill_dirs(this_skill)

        assert found == set(), f"expected no siblings found, got {found}"
```

```
$ python3 -m pytest tests/test_sibling_discovery_empty_skill_md.py -v
tests/test_sibling_discovery_empty_skill_md.py::test_excludes_sibling_with_empty_skill_md FAILED

================================== FAILURES ==================================
______ test_excludes_sibling_with_empty_skill_md ______
AssertionError: expected no siblings found, got {'half-installed-skill'}
assert {'half-installed-skill'} == set()
1 failed in 0.02s
```

Current `find_sibling_skill_dirs()` (pre-fix) only checks that `SKILL.md`
`.exists()`, not that it is non-empty:

```python
# scripts/validate_skill_bundle.py (pre-fix excerpt)
def find_sibling_skill_dirs(root: Path) -> set[str]:
    parent = root.parent
    if not parent.is_dir():
        return set()
    return {
        child.name
        for child in parent.iterdir()
        if child.is_dir() and child.name != root.name and (child / "SKILL.md").exists()
    }
```

## 3. Minimal Code Implementation

```python
# scripts/validate_skill_bundle.py (fixed excerpt)
def find_sibling_skill_dirs(root: Path) -> set[str]:
    parent = root.parent
    if not parent.is_dir():
        return set()
    result = set()
    for child in parent.iterdir():
        if not child.is_dir() or child.name == root.name:
            continue
        skill_md = child / "SKILL.md"
        if skill_md.exists() and skill_md.stat().st_size > 0:
            result.add(child.name)
    return result
```

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_sibling_discovery_empty_skill_md.py -v
tests/test_sibling_discovery_empty_skill_md.py::test_excludes_sibling_with_empty_skill_md PASSED
1 passed in 0.02s
```

```python
>>> from pathlib import Path
>>> import validate_skill_bundle
>>> validate_skill_bundle.find_sibling_skill_dirs(Path("/tmp/parent/skill-router"))
set()
```

Full regression suite (this test plus the 2 existing `FindSiblingSkillDirsTests`
cases: real sibling found, no siblings at all) - 3 cases - passes in 0.06s,
at 100.0% line coverage of `find_sibling_skill_dirs`.

## 5. Regression Guard Summary

This test guards against `validate_skill_bundle.py` reporting a
half-installed skill (a directory created by a partial checkout or a failed
install script, with a zero-byte `SKILL.md` left behind) as a legitimate
sibling - which would make the bundle validator's "routed skill(s) not
currently installed" note silently wrong, treating an empty stub as
installed when it is not usable. Any future change that reverts to a bare
`.exists()` check will fail this test immediately.
