---
role: test-driven Research Software Engineer
skill: academic-papers
archetype: test-first
target: Citation checker must flag every dangling \cite key when no .bib file is found at all, and must not flag a key present in both .tex and .bib
---

## 1. Acceptance Invariants & Boundary Constraints

`scripts/check_manuscript.py`'s `scan(root)` must populate `missing_bib` with
every `\cite{}` key found in the `.tex` sources whenever those keys cannot be
resolved against a `.bib` file - including the boundary case where **no
`.bib` file exists in the directory at all** (a forgotten or misnamed
bibliography file, e.g. `refs.bibtex` instead of `refs.bib`). Per
`references/citations-and-bibliography.md` and
`references/citation-verification.md`, an unresolved citation is exactly the
class of defect this tool exists to catch before submission - a manuscript
with every citation dangling must never report "No issues found."

- A key present in both a `.tex` `\cite{}` and a `.bib` entry must **not**
  appear in `missing_bib` (no false positives).
- A key present in `.tex` with **zero** `.bib` files anywhere under the
  scanned directory must appear in `missing_bib` (the boundary this test
  targets - not just the case where a `.bib` file exists but is missing one
  entry).

## 2. Executable Failing Test (Red)

```python
# tests/test_check_manuscript_missing_bib_dir.py
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "scripts")
from check_manuscript import scan


def test_flags_every_cite_key_when_no_bib_file_exists():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "paper.tex").write_text(
            r"Observed excess consistent with \cite{Smith2020} and "
            r"\cite{Jones2019}.",
            encoding="utf-8",
        )
        # Deliberately no .bib file anywhere under root.

        results = scan(root)

        assert results["missing_bib"].keys() == {"Smith2020", "Jones2019"}, (
            f"expected both keys flagged with no .bib present, "
            f"got {sorted(results['missing_bib'].keys())}"
        )
```

```
$ python3 -m pytest tests/test_check_manuscript_missing_bib_dir.py -v
tests/test_check_manuscript_missing_bib_dir.py::test_flags_every_cite_key_when_no_bib_file_exists FAILED

================================== FAILURES ==================================
______ test_flags_every_cite_key_when_no_bib_file_exists ______
AssertionError: expected both keys flagged with no .bib present, got []
assert dict_keys([]) == {'Smith2020', 'Jones2019'}
1 failed in 0.03s
```

Current `scan()` (excerpt, pre-fix) guards the whole check on `bib_files`
being non-empty, so an entirely missing `.bib` file silently disables the
check instead of flagging every citation as unresolved:

```python
# scripts/check_manuscript.py (pre-fix excerpt)
missing_bib = {k: v for k, v in cite_keys.items() if bib_files and k not in bib_entries}
```

With `bib_files == []` (falsy), `bib_files and k not in bib_entries` is
`False` for every key, so `missing_bib` stays empty and `report()` prints
"No issues found" on a manuscript where literally every citation is
dangling.

## 3. Minimal Code Implementation

```python
# scripts/check_manuscript.py (fixed excerpt)
# A missing .bib entirely is not "nothing to check" - it means every cited
# key is unresolved by definition, so drop the `bib_files and` short-circuit.
missing_bib = {k: v for k, v in cite_keys.items() if k not in bib_entries}
```

`bib_entries` is already correctly empty when `bib_files == []` (the
`.bib`-scanning loop simply has nothing to iterate), so removing the guard
makes every cited key resolve against an empty set and correctly appear in
`missing_bib` - no other code path changes, since `k not in bib_entries` was
already the right condition once the short-circuit is gone.

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_check_manuscript_missing_bib_dir.py -v
tests/test_check_manuscript_missing_bib_dir.py::test_flags_every_cite_key_when_no_bib_file_exists PASSED
1 passed in 0.03s
```

```
$ python3 scripts/check_manuscript.py /tmp/no-bib-manuscript
Scanned 1 .tex file(s) and 0 .bib file(s).

[MISSING BIB ENTRY] 2 cite key(s) not found in any .bib file:
  - Jones2019  (paper.tex:1)
  - Smith2020  (paper.tex:1)

Total issues: 2
```

Full regression suite (existing `tests/test_check_manuscript.py` plus this
new test) passes in 0.11s with no change to the "key present in both" branch
- a follow-up regression check confirms a key present in a real `.bib` file
  is still correctly excluded from `missing_bib` (0 false positives, matched
  exactly).

## 5. Regression Guard Summary

This test guards against the exact silent-pass failure mode the "no `.bib`
file at all" boundary previously produced: a manuscript that would fail
peer review for having zero resolvable citations instead printed "No issues
found" and exited 0, which is precisely the false-confidence result
`references/citation-verification.md` warns a pre-submission checker must
never produce. Any future refactor that reintroduces a `bib_files and` (or
equivalent) short-circuit on the missing-bib check will fail this test
immediately, before it ships.
