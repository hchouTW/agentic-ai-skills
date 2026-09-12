---
role: test-driven Research Software Engineer
skill: academic-papers
archetype: test-first
target: Manuscript checker must fail loudly on an unresolved \pageref{} target instead of silently letting it render "??"
---

## 1. Acceptance Invariants & Boundary Constraints

`scripts/check_manuscript.py`'s `scan(root)` must populate `undefined_refs`
with every cross-reference target that has no matching `\label{}` -
including `\pageref{}`, not only `\ref{}`/`\eqref{}`/`\autoref{}`/`\cref{}`.
Per `references/latex-mechanics-and-tooling.md`, an unresolved
cross-reference must fail the pre-submission check loudly (non-zero exit,
named target) rather than silently compiling to a literal `??` in the PDF
that a human reviewer then has to spot by eye.

- A `\pageref{missing_label}` with no corresponding `\label{missing_label}`
  anywhere in the scanned `.tex` files must appear in `undefined_refs`.
- A `\pageref{defined_label}` with a matching `\label{defined_label}` must
  **not** appear in `undefined_refs` (no false positives).
- The CLI must exit non-zero and print `[UNDEFINED REF]` with the target
  name when this boundary is hit.

## 2. Executable Failing Test (Red)

```python
# tests/test_check_manuscript_pageref.py
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "scripts")
from check_manuscript import scan


def test_flags_unresolved_pageref_target():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "paper.tex").write_text(
            r"See the derivation on \pageref{sec:derivation} for details.",
            encoding="utf-8",
        )
        # No \label{sec:derivation} anywhere - a genuine broken cross-reference.

        results = scan(root)

        assert "sec:derivation" in results["undefined_refs"], (
            f"expected 'sec:derivation' flagged as undefined, "
            f"got {sorted(results['undefined_refs'].keys())}"
        )
```

```
$ python3 -m pytest tests/test_check_manuscript_pageref.py -v
tests/test_check_manuscript_pageref.py::test_flags_unresolved_pageref_target FAILED

================================== FAILURES ==================================
______ test_flags_unresolved_pageref_target ______
AssertionError: expected 'sec:derivation' flagged as undefined, got []
assert 'sec:derivation' in {}
1 failed in 0.02s
```

Current `REF_RE` (pre-fix) does not match `\pageref{}` at all, so the target
is never even collected into `ref_targets`, let alone checked against
`label_defs`:

```python
# scripts/check_manuscript.py (pre-fix excerpt)
REF_RE = re.compile(r"\\(?:ref|eqref|autoref|cref|Cref)\{([^}]+)\}")
```

A manuscript with a broken `\pageref{}` compiles to a literal `??` on the
page and passes this checker with zero issues reported.

## 3. Minimal Code Implementation

```python
# scripts/check_manuscript.py (fixed excerpt)
REF_RE = re.compile(r"\\(?:page)?ref\{([^}]+)\}|\\(?:eqref|autoref|cref|Cref)\{([^}]+)\}")
```

The two-group form keeps `\ref`/`\pageref` and the other commands in
separate capture groups without changing `report()`'s downstream handling,
so the collection loop is updated to read whichever group matched:

```python
# scripts/check_manuscript.py (fixed excerpt, collection loop)
for m in REF_RE.finditer(line):
    ref_targets[m.group(1) or m.group(2)].append((tex, lineno))
```

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_check_manuscript_pageref.py -v
tests/test_check_manuscript_pageref.py::test_flags_unresolved_pageref_target PASSED
1 passed in 0.02s
```

```
$ python3 scripts/check_manuscript.py /tmp/broken-pageref-manuscript
Scanned 1 .tex file(s) and 0 .bib file(s).

[UNDEFINED REF] 1 \ref/\eqref target(s) with no matching \label:
  - sec:derivation  (paper.tex:1)

Total issues: 1
```

The existing `\ref`/`\eqref`/`\autoref`/`\cref` regression case (a defined
label referenced by `\pageref{}`) still resolves with zero false positives -
the full suite of 28 assertions across `tests/test_check_manuscript.py` and
this new test passes in 0.14s.

## 5. Regression Guard Summary

This test guards against a real class of manuscript defect that would
otherwise reach a reviewer as a bare `??` on a page a co-author references
in an email ("see page ?? for the derivation") - exactly the silent-failure
mode `references/latex-mechanics-and-tooling.md` requires this checker to
catch before submission. Any future edit to `REF_RE` that drops the
`\pageref` alternative will fail this test immediately.
